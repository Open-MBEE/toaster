"""Two-tier conformance (AGENTS.md 1.9, DL-025, DL-039).

Language conformance is always on and reported separately. It now has two parts (DL-039): `ok` (`model.ok`, the
loader's own proxy for language conformance) and `gap_findings` (`language_gap_findings`), constructs OpenSysML
v0.9.0 accepts but the spec forbids. `model.ok` is a proxy, not the definition: a model can have `ok` True and
still be language non-conformant if `gap_findings` is non-empty. Project conformance checks carry five statuses:

- open: not yet applied, because the check is unscheduled (`applies_from` is None) or its stage has not been
  reached — only when the model passes language conformance; see blocked below for when it does not.
- passed: applied to a loaded model and found nothing.
- failed: applied to a loaded model and found something.
- blocked: cannot be applied until a stated condition holds. When the model fails language conformance (`model.ok`
  is False, or `gap_findings` is non-empty) every non-wont-do project check is blocked instead, with a reason and
  `unblock_when` naming the failure — scheduled or not, and whether or not its stage has been reached.
- wont-do: dropped because something changed and the check is no longer needed; the check's `wont_do` records the
  reason and the change that removed the need. It holds at any stage and whatever the language result.

`run` is called only for passed and failed.
"""

import difflib
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from toaster import query

Stage = tuple[int, int]  # (chapter, section), ordered lexicographically


@dataclass(frozen=True)
class WontDo:
    reason: str
    changed: str  # the change that removed the need


@dataclass(frozen=True)
class ConformanceCheck:
    id: str
    description: str
    run: Callable[[Any], list[dict]]
    applies_from: Stage | None
    negative_control: (
        str  # SysML source that must load ok and produce at least one finding
    )
    wont_do: WontDo | None = None


@dataclass(frozen=True)
class GapRule:
    """A language-gap rule (DL-039): a construct OpenSysML v0.9.0 accepts but the spec forbids."""

    name: str
    constraint: str  # the spec constraint enforced, citable
    check: Callable[[Any, "query.ApiIndex"], list[dict]]
    negative_control: (
        str  # SysML source that must load ok and produce at least one finding
    )


@dataclass
class Result:
    check_id: str
    status: str  # "open" | "passed" | "failed" | "blocked" | "wont-do"
    findings: list[dict] = field(default_factory=list)
    applies_from: Stage | None = None
    reason: str | None = None
    unblock_when: str | None = None


LANGUAGE_BLOCK_REASON = "not applied: language conformance failed"
LANGUAGE_UNBLOCK_WHEN = "language conformance passes (model.ok is True)"


def _wont_do_result(check: ConformanceCheck) -> Result:
    w = check.wont_do
    assert w is not None
    return Result(
        check.id,
        "wont-do",
        [],
        check.applies_from,
        f"{w.reason} (changed: {w.changed})",
    )


def evaluate(check: ConformanceCheck, model: Any, stage: Stage) -> Result:
    if check.wont_do is not None:
        return _wont_do_result(check)
    if check.applies_from is None:
        return Result(check.id, "open", [], None, "not applied: unscheduled")
    if stage < check.applies_from:
        return Result(
            check.id, "open", [], check.applies_from, "not applied: stage not reached"
        )
    findings = check.run(model)
    return Result(
        check.id, "failed" if findings else "passed", findings, check.applies_from
    )


def _allocate_between_definitions(
    model: Any, index: "query.ApiIndex | None" = None
) -> list[dict]:
    """Rule (DL-039): an AllocationUsage whose connector ends resolve to Definitions, not Features.

    KerML 8.3.3.3.9 ReferenceSubsetting requires the referenced element to be a Feature. OpenSysML v0.9.0
    accepts `allocate ActionDef to PartDef;` (both ends definitions) with no diagnostic.

    Resolves each connector end itself, one at a time, rather than through `query.find_allocations` (which
    resolves every end of every allocation in one list comprehension): a single end whose referenced element
    is missing from the API-JSON export raises `KeyError` inside `ApiIndex.end_path`, and going through
    `find_allocations` would let that propagate out of the whole check. Here it is caught per end, so only
    that one unresolvable end is skipped (F2) instead of crashing the check for every allocation.
    """
    idx = index or query.ApiIndex(model)
    findings = []
    for a in idx.of_type("AllocationUsage"):
        a_id = a.get("qualifiedName")
        for end_ref in a.get("connectorEnd", []):
            try:
                end = idx.end_path(end_ref)
            except KeyError:
                continue
            if not end:
                continue
            target_qn = end[-1]
            target_type = idx.by_qn.get(target_qn, {}).get("@type", "")
            if target_type.endswith("Definition"):
                findings.append(
                    {
                        "rule": "allocate-between-definitions",
                        "constraint": (
                            "KerML 8.3.3.3.9 ReferenceSubsetting requires the "
                            "referenced element to be a Feature"
                        ),
                        "element": a_id,
                        "message": (
                            f"allocation {a_id} end resolves to {target_type} "
                            f"{target_qn}, not a Feature"
                        ),
                    }
                )
    return findings


# SysML/KerML metamodel supertypes of a metaclass (fixed by the language grammar, not the model's own
# specialization tree): ConnectionDefinition, InterfaceDefinition and AllocationDefinition are all kinds of
# PartDefinition per the spec, even though OpenSysML's API-JSON `@type` names them distinctly from a plain
# `part def`. A user `part def` chain needs no entry here: its own `@type` is already "PartDefinition".
# ViewDefinition and RenderingDefinition are likewise kinds of PartDefinition (SysML v2.0 formal/2026-03-02
# 7.26.1: "A view definition is a kind of part definition (see 7.11)" and "A rendering definition is a kind
# of part definition (see 7.11)").
_METACLASS_SUPERTYPES: dict[str, set[str]] = {
    "ConnectionDefinition": {"PartDefinition"},
    "InterfaceDefinition": {"PartDefinition"},
    "AllocationDefinition": {"PartDefinition"},
    "ViewDefinition": {"PartDefinition"},
    "RenderingDefinition": {"PartDefinition"},
}


def _is_or_specializes_part_definition(type_kind: str | None) -> bool:
    """Whether the metaclass ``type_kind`` (e.g. from an element's ``@type``) is PartDefinition or, per the
    fixed SysML/KerML metamodel, transitively specializes it. Uses the same `_closure` traversal the
    port-type check (`port_type_mismatches`) uses over `specialization_graph`, applied here to the static
    metaclass hierarchy in `_METACLASS_SUPERTYPES` instead of the model's own named specializations.
    """
    if type_kind is None:
        return False
    return type_kind == "PartDefinition" or "PartDefinition" in query._closure(
        type_kind, _METACLASS_SUPERTYPES
    )


def _part_typed_only_by_item_def(
    model: Any, index: "query.ApiIndex | None" = None
) -> list[dict]:
    """Rule (DL-039): a PartUsage none of whose types is a PartDefinition (or a subtype of one).

    SysML `validatePartUsagePartDefinition` (formal/2026-03-02 p. 323): "At least one of the itemDefinitions
    of a PartUsage must be a PartDefinition." A PartUsage with no declared type at all is out of scope for
    this rule (there is no itemDefinition to check). A connection def, interface def or allocation def IS a
    kind of PartDefinition per the metamodel (F4), so any of those satisfies the constraint too, as does a
    user part def that specializes another part def at any depth (its own `@type` is already
    "PartDefinition"). A type reference that cannot be resolved (missing from the API-JSON export, e.g. an
    unresolved library type) cannot be judged either way, so it is skipped rather than flagged (F4): this
    rule only flags a PartUsage whose types are *all* resolved and *none* is a PartDefinition or subtype.
    """
    idx = index or query.ApiIndex(model)
    findings = []
    for e in idx.of_type("PartUsage"):
        e_qn = e.get("qualifiedName")
        type_qns = idx.type_names(e_qn) if e_qn else []
        if not type_qns:
            continue
        resolved_kinds = [
            idx.by_qn.get(tq, {}).get("@type") for tq in type_qns if tq is not None
        ]
        if any(_is_or_specializes_part_definition(k) for k in resolved_kinds):
            continue
        if len(resolved_kinds) < len(type_qns):
            # at least one type is missing from the export: cannot determine, not a violation
            continue
        findings.append(
            {
                "rule": "part-typed-only-by-item-def",
                "constraint": (
                    "SysML validatePartUsagePartDefinition (formal/2026-03-02 "
                    "p. 323): at least one of the itemDefinitions of a "
                    "PartUsage must be a PartDefinition"
                ),
                "element": e_qn,
                "message": (
                    f"{e_qn} is typed only by {resolved_kinds}, none a "
                    "PartDefinition or subtype"
                ),
            }
        )
    return findings


# F7 (review of PASS4-000-B): the spec citation for AcceptActionUsage lives here ONCE, and both the
# GapRule.constraint and the per-finding "constraint" field use this same constant, so the two copies
# cannot drift apart the way the earlier duplicated text did (F1: AcceptActionUsage is 8.3.17.2, PDF
# p. 341-342 — NOT 8.3.16, which is Flow Abstract Syntax; matches the citation already corrected in
# decisions/gap-issue-drafts.md Draft 9, which this task does not otherwise touch).
_UNRESOLVED_TRANSITION_TRIGGER_CONSTRAINT = (
    "SysML v2.0 formal/2026-03-02: 8.3.18.9 TransitionUsage "
    "(/triggerAction : AcceptActionUsage), 8.3.18.8 TransitionFeatureMembership "
    "(validateTransitionFeatureMembershipTriggerAction), 8.3.17.2 AcceptActionUsage "
    "(PDF p. 341-342, payloadParameter) — a trigger is a structured, resolvable "
    "element, so an `accept` trigger's payload name must resolve to a defined "
    "element in scope"
)

# F2/F4 round 2: "after" (time trigger) and "when" (change trigger) are expressions, not names; round 2
# adds "at" (also a time trigger, `accept at <clock-feature>`, confirmed against the tool: F4).
_TRIGGER_EXPRESSION_KEYWORDS = ("after", "when", "at")

# A named payload ("s : Start", "s :> sig" (F4 round 2: subsetting), or "s : Outer::Start" with a
# qualified type) uses a single colon or ":>" , spaced on both sides in the export; a qualified name
# ("Outer::Start") uses an unspaced "::". The alternation (literal ":>" , or a lone ":" not immediately
# followed by another ":") keeps the two apart, so "Outer::Start" is correctly rejected as a whole (see
# the check's docstring for the scratch-model shapes this was verified against).
_NAMED_PAYLOAD = re.compile(r"^[A-Za-z_]\w*\s*(?::>|:(?!:))\s*(.+)$")

# Round 2 F4: the standard-library packages this repo's own models actually import (models/*.sysml:
# ScalarValues, SI, ISQ, MeasurementReferences), plus Time (named directly in the round-2 push-back).
# Not exhaustive of the OMG SysML standard library: a reference into a standard-library package not on
# this list is still flagged (a known false-positive risk, symmetric with the false-negative risk of
# the "any local package" branch below — both are guesses, in opposite directions, about a name this
# rule cannot verify either way). Expanding the list is a one-line follow-up when a new standard import
# is introduced.
_KNOWN_EXTERNAL_LIBRARY_PACKAGES = frozenset(
    {"ScalarValues", "SI", "ISQ", "MeasurementReferences", "Time"}
)

# Round 2 follow-up (F4, replacing the blanket "any unresolvable import -> skip" rule for an unqualified
# name, which the reviewer found defeats this rule's entire purpose: every real chapter fixture imports
# ScalarValues/SI/ISQ/MeasurementReferences, so it silently skipped unqualified-name checking in every
# real chapter, including D-023's own headline case, a plain typo of a locally-declared name).
#
# Chosen and verified empirically against the real ch07 fixture's own declared-name vocabulary (48
# names: item/part/attribute/state names, etc. — see `test_unresolved_transition_trigger_...` for the
# exact figures) rather than picked arbitrarily:
#   - Every one-letter-off or transposition-style typo tried (`Strat`/`Start` 0.800, `Cancle`/`Cancel`
#     0.833, `Finsh`/`Finish` 0.909, `Staart`/`Start` 0.909, `Fnish`/`Finish` 0.909) scores at or above
#     0.8.
#   - Of 22 plausible standard-library member names tried against that same vocabulary (`Boolean`,
#     `Integer`, `Real`, `Vector`, `PowerValue`, `TimeInstantValue`, ...), the single closest is `Vector`
#     vs. the locally-declared part `ejector` at 0.769 — below 0.8. At a lower cutoff (0.75, tried
#     first) that pair is a false match; 0.8 is the smallest round threshold that excludes it while
#     still keeping every typo case above.
# This is an empirical fit to one real fixture's vocabulary, not a proof for all possible names; a
# future chapter's vocabulary could in principle need re-tuning if it produces its own false match.
_TRIGGER_TYPO_SIMILARITY_CUTOFF = 0.8


def _trigger_payload_name(trigger: str) -> str | None:
    """The identifier or qualified name an `accept` trigger's ``sysx:trigger`` string denotes, or
    ``None`` if the string is a time/change-trigger expression (an ``after <duration>``,
    ``at <clock-feature>`` or ``when <expr>`` form), which names no type at all and so is out of scope
    for this rule (F2/F3, F4 round 2).
    """
    first_word = trigger.split(None, 1)[0]
    if first_word in _TRIGGER_EXPRESSION_KEYWORDS:
        return None
    named_payload = _NAMED_PAYLOAD.match(trigger)
    return named_payload.group(1).strip() if named_payload else trigger


def _has_unresolvable_import(idx: "query.ApiIndex") -> bool:
    """Whether this document has at least one ``NamespaceImport``/``MembershipImport`` whose target
    does not resolve to any element present in this document's own API-JSON export — i.e. a genuinely
    external import (a standard-library package, or any other document this rule cannot see into).

    Deliberately does not try to recover *which* package the import names: the export's only handle on
    an unresolved import's target is an opaque id with no ``declaredName`` at all, and the one place a
    human-readable name might come from, ``sysx:sourceText``, is not reliable (confirmed directly: it
    is present for every import in the real ch07 fixture, which formats one import per line, but is
    empty for an otherwise-identical import packed onto one source line with other statements — a
    single-formatting-dependent signal is not something this rule should key correctness on).

    Used only as a narrow, secondary signal for the unqualified-name case, and only once a name has
    already failed both the flat declared-name match AND the similarity check
    (`_TRIGGER_TYPO_SIMILARITY_CUTOFF`) against every declared name in the document — never as a
    blanket "this document has *some* import, so skip every unresolved unqualified name" rule. An
    earlier version of this rule used it that way; the reviewer found it defeats the rule's whole
    purpose, since every real chapter fixture imports at least one external library, which would have
    silently skipped unqualified-name checking everywhere, including a plain typo of a locally-declared
    name (D-023's own headline case). See the check's docstring for the corrected three-step order.
    """
    for e in idx.elements:
        if e.get("@type") not in ("NamespaceImport", "MembershipImport"):
            continue
        target = e.get("importedNamespace") or e.get("importedMembership")
        target_id = target["@id"] if isinstance(target, dict) else target
        if target_id not in idx.by_id:
            return True
    return False


def _unresolved_transition_trigger(
    model: Any, index: "query.ApiIndex | None" = None
) -> list[dict]:
    """Rule (DL-039, D-023): an ``accept`` trigger's payload name that resolves to no element in scope.

    See ``_UNRESOLVED_TRANSITION_TRIGGER_CONSTRAINT`` for the spec citation. OpenSysML v0.9.0 keeps the
    trigger only as the bare string ``sysx:trigger`` in the API-JSON export — never a reference — and
    accepts an undefined or misspelled name with ``ok=True`` and no diagnostic (D-023): the transition
    then silently never fires at execution.

    ``sysx:trigger`` is not always a plain name. Confirmed directly against the tool (scratch models,
    not assumed):

    - plain identifier: ``"Start"``
    - qualified name: ``"Outer::Start"``
    - named payload: ``"s : Start"`` (resolve the part after the colon, not the whole string; a
      qualified type in a named payload, ``"s : Outer::Start"``, resolves the same way); a subsetting
      named payload, ``"s :> sig"``, resolves ``sig`` the same way (F4 round 2)
    - time trigger: ``"after 5 [s]"`` or ``"at t"`` — an expression, not a name; no payload to resolve
      (round 2 adds ``at``, confirmed against the tool: F4)
    - change trigger: ``"when someFlag"`` — an expression naming an attribute, not a name to resolve
      against a type; also no payload to resolve
    - untriggered (unconditional) transition: neither ``sysx:trigger`` nor ``sysx:triggerKeyword`` at
      all

    ``_trigger_payload_name`` turns the first three into the name to resolve and the rest into
    ``None`` (skipped, not flagged). The payload type can be any kind that has a ``declaredName`` —
    ``ItemDefinition``, ``PartDefinition``, ``PortDefinition``, ``AttributeDefinition``,
    ``EnumerationDefinition``, an existing usage referenced by name — not only ``ItemDefinition``
    (confirmed: OpenSysML accepts every one of these as a payload type with ``ok=True``), so this rule
    matches against the ``declaredName`` of *any* element, not a fixed enum of kinds. Round 2 (R4): this
    also means an unqualified match is not restricted to type-like ``@type``s at all — a trigger that
    happens to spell a state's or an attribute's own ``declaredName`` (e.g. ``accept idle``) resolves
    too, even though neither is a type. This is an intentional, already-reviewed leniency: enumerating
    every ``@type`` that is a legal payload type is exactly the fragile, drift-prone approach F2 (round
    1) rejected for the payload side of this check, and the same reasoning applies symmetrically here.

    Scope (round 2 corrects round 1's ruling, which was wrong — verified empirically before ruling
    again, not assumed: the real ch07 fixture itself wildcard-imports four external packages, so a
    same-package-only restriction would have silently stopped checking exactly the fixture this guard
    exists to protect):

    An unqualified name is resolved in three steps, in this order (rewritten after the reviewer found
    the previous, second-round version defeated the whole rule — see below):

    1. **Exact match.** Resolved against the ``declaredName`` of *any* element anywhere in the loaded
       model, full stop — no package or import modeling at all. This is deliberately coarser than real
       name resolution (it does not require, or check for, an import that would make the name actually
       visible where the trigger is written), but it is the only reading that handles a same-document,
       different-package reference through a wildcard or member import (that package's elements ARE
       all in the API-JSON export, confirmed directly) or a nested/outer-package reference, without
       attempting to model imports or namespace visibility at all — which round 1 showed is not
       reliably possible from the flat export.
    2. **Similarity match (typo detection).** If step 1 finds nothing, ``difflib.get_close_matches``
       (stdlib, no new dependency) is tried against every declared name in the model, at
       ``_TRIGGER_TYPO_SIMILARITY_CUTOFF`` (0.8; see that constant for the empirical case behind the
       number). A close match is **flagged** — this is D-023's own headline case: `accept Strat` for a
       locally-declared `Start` is a near-miss (ratio 0.8) of a real local name, so it is a plausible
       typo, not a plausible import.
    3. **External-import fallback.** Only if steps 1 and 2 both find nothing does the presence of an
       unresolvable import (`_has_unresolvable_import`) matter: if the document has at least one import
       that does not itself resolve to a local element, the failing name might be a member of that
       import and is skipped, not flagged (the export gives no reliable way to name the import's target
       to check further — see that function's docstring). With no such import either, the name is
       flagged as broken (``accept Zephyr`` with no local match and no import at all —
       `test_unresolved_transition_trigger_unrelated_name_no_import_is_flagged`).

    Note what step 1 alone, independent of steps 2 and 3, still means: the round-2 final ruling on a
    genuine no-import cross-package reference (an unqualified name declared only in a *different*
    package, with no import at all bringing it into scope) is unchanged by this round's fix — it is
    resolved at step 1 already, the same package-blind exact match that resolves the legitimate
    with-import case, since step 1 never checks for an import either way
    (`test_unresolved_transition_trigger_no_import_cross_package_not_flagged`). It never reaches steps
    2 or 3 at all, because the name it names really is, verbatim, declared somewhere in the model.

    **Why step 2 had to be added, not just documented:** round 2's version skipped every step
    1-failing unqualified name whenever *any* unresolvable import was present in the document, with no
    similarity check at all — i.e. step 3 with no step 2 in between. The reviewer found this defeats
    the rule's entire purpose: every real chapter model imports at least one external library
    (ScalarValues, SI, ISQ, MeasurementReferences), so that blanket rule silently skipped
    unqualified-name checking in every real chapter, including a plain `accept Strat` typo of a
    locally-declared `Start` — confirmed directly: replacing `Start` with `Strat` in the real ch07 and
    ch08 fixtures gave zero findings under round 2's rule
    (`test_unresolved_transition_trigger_real_fixture_typo_is_flagged`, parametrized over both).
    Step 2 fixes this: a name that closely resembles something declared right here is flagged before
    the import fallback is even consulted, regardless of what else the document imports
    (`test_unresolved_transition_trigger_local_typo_still_flagged_with_unrelated_import` pins the exact
    combination that broke); the import fallback in step 3 now only ever applies to a name that
    resembles nothing local at all (a genuine external-library member, e.g. `Boolean`).

    A qualified name is unaffected by this round's change:

    - It is first tried for an exact match against every element's ``qualifiedName`` anywhere in the
      model, then a suffix match (``qualifiedName == name`` or ``qualifiedName.endswith("::" + name)``),
      so a legitimate *relative* qualification (e.g. ``Inner::Start`` when the full path is
      ``P::Inner::Start``) also resolves.
    - If neither matches, the qualified name's own top-level segment decides whether the reference is
      judged at all: if that segment names a real local ``Package`` in this document (by
      ``declaredName``, any nesting depth), the document CAN see into that package, so a name that
      still isn't found under it is a genuine broken reference — flagged. If the segment does not name
      a local package but is a recognized external/standard-library package name
      (``_KNOWN_EXTERNAL_LIBRARY_PACKAGES``), it is treated as a probable external reference this rule
      cannot verify either way — skipped, not flagged, per the same "skip rather than falsely flag"
      posture the other two gap rules already take (their own F4). Anything else (a top segment that is
      neither a visible local package nor a recognized library name) is flagged as broken: there is
      nothing to back reading it as external.
    """
    idx = index or query.ApiIndex(model)

    all_declared_names: set[str] = set()
    all_qualified_names: set[str] = set()
    local_package_declared_names: set[str] = set()
    for e in idx.elements:
        qn = e.get("qualifiedName")
        if qn:
            all_qualified_names.add(qn)
        name = e.get("declaredName")
        if name:
            all_declared_names.add(name)
            if e.get("@type") == "Package":
                local_package_declared_names.add(name)

    has_unresolvable_import = _has_unresolvable_import(idx)

    findings = []
    for t in idx.of_type("TransitionUsage"):
        if t.get("sysx:triggerKeyword") != "accept":
            continue
        trigger = t.get("sysx:trigger")
        if not trigger:
            continue
        payload_name = _trigger_payload_name(trigger)
        if payload_name is None:
            continue  # time/change-trigger expression: not a name, nothing to resolve (F2/F3)
        t_id = t.get("qualifiedName")

        if "::" in payload_name:
            top = payload_name.split("::")[0]
            resolved = payload_name in all_qualified_names or any(
                qn.endswith("::" + payload_name) for qn in all_qualified_names
            )
            if resolved:
                continue
            if top not in local_package_declared_names and (
                top in _KNOWN_EXTERNAL_LIBRARY_PACKAGES
            ):
                continue  # probable external library reference; can't verify, don't flag (F4)
        else:
            if payload_name in all_declared_names:
                continue  # step 1: exact match
            close_match = difflib.get_close_matches(
                payload_name, all_declared_names, n=1, cutoff=_TRIGGER_TYPO_SIMILARITY_CUTOFF
            )
            if not close_match and has_unresolvable_import:
                continue  # step 3: no local resemblance at all; might be an external import member
            # step 2 (close_match): flag as a plausible typo of a real local name, regardless of any
            # import present — a name that resembles something declared right here is not given the
            # benefit of the doubt just because the document also imports a library (F4 round 2 fix)

        findings.append(
            {
                "rule": "unresolved-transition-trigger",
                "constraint": _UNRESOLVED_TRANSITION_TRIGGER_CONSTRAINT,
                "element": t_id,
                "message": (
                    f"transition {t_id} accepts trigger {trigger!r}, whose payload "
                    f"{payload_name!r} resolves to no element in scope"
                ),
            }
        )
    return findings


_ALLOCATE_CONNECTOR_END_ACCESSIBILITY_CONSTRAINT = (
    "KerML 1.1 Beta 2: canAccess 8.3.3.3.4 (p. 188), isFeaturedWithin (p. 190), "
    "validateSubsettingFeaturingTypes (p. 204); 8.3.4.5.3 Connector "
    "checkConnectorTypeFeaturing and defaultFeaturingType (pp. 214-215)"
)


def _allocate_connector_end_accessibility(
    model: Any, index: "query.ApiIndex | None" = None
) -> list[dict]:
    """Rule (DL-058, hardened DL-059 ADDENDUM/Task 5): an AllocationUsage connector end that reaches into a
    Definition or Usage the allocation's own owner cannot access.

    DL-058 ruled that `allocate <Def>::<usage> to <Def>::<usage>;` at package level (the tutorial's own
    ch05-ch08 fixtures, before this effort's fix) violates KerML's validateSubsettingFeaturingTypes (the
    referenced feature must be accessible: `subsettingFeature.canAccess(subsettedFeature)`, which requires
    `isFeaturedWithin` one of the end's featuringTypes) and checkConnectorTypeFeaturing (no featuringType in
    common between the two definitions, so no implied TypeFeaturing rescues it either). OpenSysML v0.9.0 and
    sysml-toolkit v0.9.1 both accept the construct with no diagnostic (DL-058's two tool holes); this rule is
    the tutorial-supplied guard against a regression back into that non-conformant idiom.

    Task 4's first cut had two bugs, found by an independent review and confirmed against the OMG pilot
    (ground truth) rather than merely re-derived, both fixed here:

    **F1 (false positives — accessibility ignored specialization and typing).** `canAccess`/`isFeaturedWithin`
    treat a featuring type as accessible not only when it IS the declaring context, but also when it
    (transitively) SPECIALIZES that declaring context, or — for a Usage owner — is TYPED by it (KerML treats
    FeatureTyping as a kind of Specialization). Task 4's check only ever compared the declaring context
    against the owner's own qualified name by exact identity, so `part def BetterToaster :> Toaster { allocate
    doApply to heater; }` and `part toaster : Toaster { allocate doApply to heater; }` were both wrongly
    flagged (the pilot accepts both, exit 0). Fixed by additionally accepting a declaring context that appears
    in `query.supertypes_transitively(model, owner_qn)` — confirmed empirically (this task) that this single
    helper call already covers BOTH cases without any separate "resolve the owner's own type" branch: KerML's
    own FeatureTyping-is-Specialization rule is already reflected in `Symbol.specializations`, so
    `supertypes_transitively(model, "P::toaster")` (a PartUsage typed by `P::Toaster`, no `:>` at all) already
    returns `{"P::Toaster"}`, identically to the `:>` specialization case.

    **F2 (false negatives — a dot-chain's first segment isn't automatically safe).** Task 4's docstring and
    D-032/DL-059 claimed a multi-segment end is "already structurally proven accessible by the tool's own
    parser" — this is FALSE. OpenSysML accepts `Toaster.heater` (dot after a bare Definition name) and
    `Outer::box.t` (dot after a qualified path into an inaccessible Usage) as loadable, multi-segment
    `end_path` chains, but the pilot rejects both ("Couldn't resolve reference to Feature ..."). Fixed by
    running the SAME accessibility test against the FIRST segment of every end, whether single- or
    multi-segment — only the REMAINDER of a chain past its first segment (member existence and typing within
    an already-accessible feature) is genuinely proven by successful loading; the first hop's accessibility
    is not. A first segment whose own `@type` is itself a Definition (e.g. `Toaster` in `Toaster.heater`) is a
    distinct failure from an inaccessible Feature: a Definition can never be an accessible Feature at all, so
    it is flagged directly rather than falling through to the declaring-context comparison (which would
    wrongly treat `Toaster`'s own owning Package as its "declaring context" and pass it) — this check applies
    only to a CHAIN ROOT (`len(end) > 1`), not to an ordinary single-segment end resolving whole to a
    Definition, which is `allocate-between-definitions`'s (D-019's) own job (checked against `end[-1]`); this
    rule and that one must not double-flag the same construct.

    An allocation end is written one of two ways once loaded and indexed via `ApiIndex`:

    - **A dot-chain** (`toastBread.applyHeat`, or the non-conformant `Toaster.heater` / `Outer::box.t`):
      `end_path` returns MULTIPLE segments (`ownedReferenceSubsetting` -> `chainingFeature`). The first
      segment is checked exactly as a single-segment end would be (see below); only the segments after it are
      trusted to the tool's own parser.
    - **A bare qualified-name reference** (`ToastBread::applyHeat` or `P::doApply`): `end_path` returns
      exactly ONE segment, the target's own `qualifiedName`. OpenSysML accepts ANY resolvable qualified name
      here, whether or not it is a feature the allocation's own context can see — this is where the gap
      lives.

    For the first segment, its qualified name minus its last `::`-separated component is its **declaring
    context**. Compare it against the AllocationUsage's own **owner** (`idx.qn(a["owner"])`, the same field
    `perform_relationships` already reads on `PerformActionUsage`; confirmed present on `AllocationUsage` too,
    empirically, not assumed):

    - Declaring context IS the owner, or resolves to a plain `Package` (the ordinary top-level pattern,
      `allocate P::doApply to P::heater;`, matching `tests/test_query.py`'s `UNNAMED_ALLOCATE` fixture) ->
      NOT a violation.
    - Declaring context (transitively) specializes, or types, the owner (`query.supertypes_transitively`) ->
      NOT a violation (F1 fix).
    - Declaring context resolves to anything else (a Definition or Usage that is neither the allocation's own
      owner nor one of its supertypes) -> VIOLATION: the end reaches into another type's nested member by
      qualified name instead of through an accessible feature chain rooted in the allocation's own context.
    - Declaring context does not resolve to any element in this document's own export at all (an external
      reference this rule cannot see into) -> cannot be judged either way, skipped rather than flagged, per
      the same "skip rather than falsely flag" posture the other gap rules in this file already take (F4).

    Empirically validated against `models/ch01-cumulative.sysml` through `ch10-cumulative.sysml` (no ch09
    fixture): zero findings on every one, all already fixed to the conformant idiom. Also validated against
    `tests/test_interconnection.py`'s own inline fixtures: `FLOW_SOURCE`, `ALLOC_SOURCE` and `NESTED_SOURCE`
    are clean, but `QUALIFIED_ALLOC_AND_INTERFACE_SOURCE`'s (now rewritten, DL-059 ADDENDUM) previous
    `allocate ApplyHeat to Toaster::heating;` DID trip this rule before its fixture fix.
    """
    idx = index or query.ApiIndex(model)
    findings = []
    supertypes_cache: dict[str, set[str]] = {}

    def owner_supertypes(owner_qn: str | None) -> set[str]:
        if owner_qn is None:
            return set()
        if owner_qn not in supertypes_cache:
            supertypes_cache[owner_qn] = query.supertypes_transitively(model, owner_qn)
        return supertypes_cache[owner_qn]

    for a in idx.of_type("AllocationUsage"):
        a_id = a.get("qualifiedName")
        owner_qn = idx.qn(a["owner"]) if "owner" in a else None
        for end_ref in a.get("connectorEnd", []):
            try:
                end = idx.end_path(end_ref)
            except KeyError:
                continue
            if not end:
                continue
            first_qn = end[0]
            if not first_qn or "::" not in first_qn:
                continue  # no owning context to compare (e.g. a top-level, unqualified single name)
            if len(end) > 1:
                # Chain root: a Definition here can never be an accessible Feature at all (a distinct
                # failure from an inaccessible-but-still-a-Feature declaring context, and distinct from
                # `allocate-between-definitions`, which only checks the chain's LAST segment).
                first_element = idx.by_qn.get(first_qn)
                if first_element is not None and first_element.get("@type", "").endswith("Definition"):
                    findings.append(
                        {
                            "rule": "allocate-connector-end-accessibility",
                            "constraint": _ALLOCATE_CONNECTOR_END_ACCESSIBILITY_CONSTRAINT,
                            "element": a_id,
                            "message": (
                                f"allocation {a_id} end chain {'.'.join(end)!r} starts at "
                                f"{first_element.get('@type')} {first_qn}, not an accessible Feature"
                            ),
                        }
                    )
                    continue
            declaring_context = first_qn.rsplit("::", 1)[0]
            if declaring_context == owner_qn:
                continue
            context_element = idx.by_qn.get(declaring_context)
            if context_element is None:
                continue  # cannot resolve the declaring context in this document: cannot judge (F4)
            if context_element.get("@type") == "Package":
                continue
            if declaring_context in owner_supertypes(owner_qn):
                continue  # F1 fix: owner (trans.) specializes, or is typed by, the declaring context
            findings.append(
                {
                    "rule": "allocate-connector-end-accessibility",
                    "constraint": _ALLOCATE_CONNECTOR_END_ACCESSIBILITY_CONSTRAINT,
                    "element": a_id,
                    "message": (
                        f"allocation {a_id} end {first_qn!r} reaches into "
                        f"{context_element.get('@type')} {declaring_context}, which is "
                        "neither the allocation's own owner nor a package or supertype of it"
                    ),
                }
            )
    return findings


_ALLOCATE_BETWEEN_DEFINITIONS_CONTROL = """
package P {
  action def ApplyHeat;
  part def HeatingSystem;
  allocate ApplyHeat to HeatingSystem;
}
"""

_PART_TYPED_ONLY_BY_ITEM_DEF_CONTROL = """
package P {
  item def Start;
  part def BreadLoader { part bread : Start; }
}
"""

_UNRESOLVED_TRANSITION_TRIGGER_CONTROL = """
package P {
  item def Start;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Strat then heating;
  }
}
"""

# DL-058's own real-world pattern (a package-level allocate whose ends are qualified paths into a
# feature nested in another definition), reduced to a minimal, isolated demonstration: `applyHeat`
# and `control` are both Features (a PerformActionUsage and a PartUsage), not Definitions, so this
# does NOT also trip `allocate-between-definitions` (confirmed:
# `test_gap_rule_negative_controls_are_isolated`); no item-typed part is involved either, so it does
# not trip `part-typed-only-by-item-def`.
_ALLOCATE_CONNECTOR_END_ACCESSIBILITY_CONTROL = """
package P {
  action def ApplyHeat;
  part def ControlSystem {
    perform action applyHeat : ApplyHeat;
  }
  part def Toaster {
    part control : ControlSystem;
  }
  allocate ControlSystem::applyHeat to Toaster::control;
}
"""

GAP_RULES: list[GapRule] = [
    GapRule(
        name="allocate-between-definitions",
        constraint=(
            "KerML 8.3.3.3.9 ReferenceSubsetting requires the referenced element "
            "to be a Feature"
        ),
        check=_allocate_between_definitions,
        negative_control=_ALLOCATE_BETWEEN_DEFINITIONS_CONTROL,
    ),
    GapRule(
        name="part-typed-only-by-item-def",
        constraint=(
            "SysML validatePartUsagePartDefinition (formal/2026-03-02 p. 323): at "
            "least one of the itemDefinitions of a PartUsage must be a PartDefinition"
        ),
        check=_part_typed_only_by_item_def,
        negative_control=_PART_TYPED_ONLY_BY_ITEM_DEF_CONTROL,
    ),
    GapRule(
        name="unresolved-transition-trigger",
        constraint=_UNRESOLVED_TRANSITION_TRIGGER_CONSTRAINT,
        check=_unresolved_transition_trigger,
        negative_control=_UNRESOLVED_TRANSITION_TRIGGER_CONTROL,
    ),
    GapRule(
        name="allocate-connector-end-accessibility",
        constraint=_ALLOCATE_CONNECTOR_END_ACCESSIBILITY_CONSTRAINT,
        check=_allocate_connector_end_accessibility,
        negative_control=_ALLOCATE_CONNECTOR_END_ACCESSIBILITY_CONTROL,
    ),
]


def language_gap_findings(model: Any) -> list[dict]:
    """Always-on language-gap check (AGENTS.md 1.9, DL-039), not a staged project check.

    Runs every rule in `GAP_RULES` against `model` and returns the concatenated findings. Each finding is a
    dict with at least `rule`, `constraint`, `element` and `message` keys. Flags constructs OpenSysML v0.9.0
    accepts (`model.ok` is True) but the spec forbids; part of language conformance, so it runs regardless
    of stage.

    The gap rules target constructs the tool accepts: when `model.ok` is False the model never reached a
    state where allocation/part-def resolution is meaningful, so this returns `[]` without attempting it
    (F2). `report()`'s existing model.ok=False branch already blocks every project check in that case.
    """
    if not model.ok:
        return []
    idx = query.ApiIndex(model)
    findings: list[dict] = []
    for rule in GAP_RULES:
        findings.extend(rule.check(model, idx))
    return findings


def language_conformance(model: Any) -> dict:
    """Language-tier conformance (AGENTS.md 1.9, DL-039): always on, reported separately from project checks.

    `ok`: whether the model loaded (`model.ok`), the available proxy for language conformance.
    `diagnostics`: the loader's own diagnostic messages.
    `gap_findings`: constructs the tool accepts (`ok` True) but the spec forbids (`language_gap_findings`).
    Non-empty `gap_findings` means the model is language non-conformant per DL-039's amendment to DL-025,
    even when `ok` is True: `model.ok` is a proxy for language conformance, not its definition.
    """
    return {
        "ok": model.ok,
        "diagnostics": [str(getattr(d, "message", d)) for d in model.diagnostics],
        "gap_findings": language_gap_findings(model),
    }


def prove_negative_control(check: ConformanceCheck, conn: Any) -> bool:
    model = conn.load_from_content(check.negative_control, strict=False)
    return bool(model.ok) and len(check.run(model)) > 0


_PORT_TYPE_CONTROL = """
package P {
  port def PowerPort; port def FuelPort;
  part def Outlet { port o : PowerPort; }
  part def Torch { port fuelIn : FuelPort; }
  part outlet : Outlet; part torch : Torch;
  connect outlet.o to torch.fuelIn;
}
"""


NOT_EVALUATED_NO_SUBJECT = "not evaluated: no explicit subject"


def satisfaction_claims_evaluated(model: Any) -> list[dict]:
    """Staged project check (DL-039 part 4): every asserted satisfy relationship, evaluated.

    For every SatisfyRequirementUsage with both a requirement and a subject, calls
    `model.eval(f"{requirement_qualified_name}({subject_qualified_name})")`. A plain `assert satisfy`
    (`isNegated` False or absent) is a finding when the expression evaluates False. An `assert not satisfy`
    (`isNegated` True) asserts the opposite: it is a finding when the expression evaluates True, since the
    model claims it should NOT hold (F3). An evaluation error is not silently dropped either way: it is
    itself a finding, reported with its message.

    A `verify` relationship (`sysx:declaredKeyword` "verify") has no subject and is not a claim about one:
    it is skipped, not reported. A bare `satisfy R;` with an implicit subject is a satisfy claim, just one
    this check cannot evaluate without a resolved subject; per DL-039's open question 2, that is recorded as
    a finding with a distinguishable status (`NOT_EVALUATED_NO_SUBJECT`) rather than silently skipped, so it
    stays visible instead of looking indistinguishable from "no claim here at all".
    """
    idx = query.ApiIndex(model)
    findings = []
    for s in query.satisfy_relationships(model, index=idx):
        requirement, subject = s["requirement"], s["subject"]
        if not requirement:
            continue
        raw = idx.by_qn.get(s["id"], {})
        if not subject:
            if raw.get("sysx:declaredKeyword") == "verify":
                continue
            findings.append(
                {
                    "id": s["id"],
                    "requirement": requirement,
                    "subject": None,
                    "status": NOT_EVALUATED_NO_SUBJECT,
                }
            )
            continue
        is_negated = bool(raw.get("isNegated", False))
        expression = f"{requirement}({subject})"
        try:
            holds = bool(model.eval(expression))
        except Exception as exc:  # noqa: BLE001 — any eval failure is itself a finding, per DL-039
            findings.append(
                {
                    "id": s["id"],
                    "requirement": requirement,
                    "subject": subject,
                    "expression": expression,
                    "error": str(exc),
                }
            )
            continue
        fails = holds if is_negated else not holds
        if fails:
            findings.append(
                {
                    "id": s["id"],
                    "requirement": requirement,
                    "subject": subject,
                    "expression": expression,
                    "result": holds,
                    "negated": is_negated,
                }
            )
    return findings


_SATISFACTION_CLAIM_CONTROL = """
package P {
  private import ScalarValues::*;
  part def Toaster {
    attribute cycleTime : Real = 200.0;
  }
  part slow : Toaster;
  requirement def TimelyToast {
    subject toaster : Toaster;
    require constraint { toaster.cycleTime <= 180.0 }
  }
  requirement timely : TimelyToast;
  assert satisfy timely by slow;
}
"""

REGISTRY: list[ConformanceCheck] = [
    ConformanceCheck(
        id="port-type",
        description="Connected ports have related declared types (OpenSysML v0.9.0 gap G4).",
        run=query.port_type_mismatches,
        # DL-038: applies from the chapter/section that first declares a port-typed
        # connection: in the current sequence, ch05-architecture/03-interfaces.ipynb
        # (ControlSystem-HeatingSystem DurationPort interface). Re-derivation follows
        # the criterion, not this literal stage.
        applies_from=(5, 3),
        negative_control=_PORT_TYPE_CONTROL,
    ),
    ConformanceCheck(
        id="satisfaction-claims-evaluated",
        description="Every asserted satisfy relationship evaluates to True (DL-039 part 4).",
        run=satisfaction_claims_evaluated,
        # DL-048: applies from the chapter/section that first declares an `assert satisfy` — in the
        # current sequence, ch03-measures/01-moe-definition.ipynb. Re-derivation follows the criterion,
        # not this literal stage.
        applies_from=(3, 1),
        negative_control=_SATISFACTION_CLAIM_CONTROL,
    ),
]

GAP_BLOCK_UNBLOCK_WHEN = "no language-tier violation, per the spec, is present (gap_findings is empty)"


def _gap_block_reason(gap_findings: list[dict]) -> str:
    rules = sorted({f["rule"] for f in gap_findings})
    return "language conformance failed: " + ", ".join(rules)


def report(
    model: Any, stage: Stage, registry: list[ConformanceCheck] | None = None
) -> dict:
    checks = REGISTRY if registry is None else registry
    language = language_conformance(model)
    if not language["ok"]:
        # A check cannot be applied to a model that did not load (DL-024, DL-025): blocked, never passed.
        project = [
            _wont_do_result(c)
            if c.wont_do is not None
            else Result(
                c.id,
                "blocked",
                [],
                c.applies_from,
                LANGUAGE_BLOCK_REASON,
                LANGUAGE_UNBLOCK_WHEN,
            )
            for c in checks
        ]
    elif language["gap_findings"]:
        # The model loaded but violates a spec constraint the tool does not enforce (DL-039): treat it as
        # language non-conformant too, symmetrically with the model.ok is False branch above (PASS2-009
        # reading B) — every non-wont-do check is blocked, whether or not it is scheduled or its stage
        # reached, not just the ones that would otherwise run.
        reason = _gap_block_reason(language["gap_findings"])
        project = [
            _wont_do_result(c)
            if c.wont_do is not None
            else Result(
                c.id,
                "blocked",
                [],
                c.applies_from,
                reason,
                GAP_BLOCK_UNBLOCK_WHEN,
            )
            for c in checks
        ]
    else:
        project = [evaluate(c, model, stage) for c in checks]
    return {"language": language, "project": project}
