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

_TRIGGER_EXPRESSION_KEYWORDS = ("after", "when")

# A named payload ("s : Start", or "s : Outer::Start" with a qualified type) uses a single colon,
# spaced on both sides in the export; a qualified name ("Outer::Start") uses an unspaced "::". The
# negative lookahead keeps the two apart: it requires the colon after the leading name NOT be
# immediately followed by a second colon, so "Outer::Start" is correctly rejected as a whole (see the
# check's docstring for the scratch-model shapes this was verified against).
_NAMED_PAYLOAD = re.compile(r"^[A-Za-z_]\w*\s*:(?!:)\s*(.+)$")


def _trigger_payload_name(trigger: str) -> str | None:
    """The identifier or qualified name an `accept` trigger's ``sysx:trigger`` string denotes, or
    ``None`` if the string is a time/change-trigger expression (an ``after <duration>`` or
    ``when <expr>`` form), which names no type at all and so is out of scope for this rule (F2/F3).
    """
    first_word = trigger.split(None, 1)[0]
    if first_word in _TRIGGER_EXPRESSION_KEYWORDS:
        return None
    named_payload = _NAMED_PAYLOAD.match(trigger)
    return named_payload.group(1).strip() if named_payload else trigger


def _owning_package_qn(idx: "query.ApiIndex", qn: str | None) -> str | None:
    """Qualified name of the nearest enclosing Package of the element named ``qn``, walking the
    ``owner``/``owningNamespace`` chain up from it. ``None`` if ``qn`` is not indexed, or the chain
    does not reach a Package (should not happen for a well-formed model; skipped rather than raised,
    matching the other gap rules' "cannot judge, don't flag" posture, F4).
    """
    if qn is None:
        return None
    seen: set[str] = set()
    e = idx.by_qn.get(qn)
    while e is not None:
        if e.get("@type") == "Package":
            return e.get("qualifiedName")
        owner_ref = e.get("owningNamespace") or e.get("owner")
        if owner_ref is None:
            return None
        owner_id = owner_ref["@id"] if isinstance(owner_ref, dict) else owner_ref
        if owner_id in seen:
            return None
        seen.add(owner_id)
        e = idx.by_id.get(owner_id)
    return None


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
      qualified type in a named payload, ``"s : Outer::Start"``, resolves the same way)
    - time trigger: ``"after 5 [s]"`` — an expression, not a name; no payload to resolve
    - change trigger: ``"when someFlag"`` — an expression naming an attribute, not a name to resolve
      against a type; also no payload to resolve
    - untriggered (unconditional) transition: neither ``sysx:trigger`` nor ``sysx:triggerKeyword`` at
      all

    ``_trigger_payload_name`` turns the first three into the name to resolve and the rest into
    ``None`` (skipped, not flagged). The payload type can be any kind that has a ``declaredName`` —
    ``ItemDefinition``, ``PartDefinition``, ``PortDefinition``, ``AttributeDefinition``,
    ``EnumerationDefinition``, an existing usage referenced by name — not only ``ItemDefinition``
    (confirmed: OpenSysML accepts every one of these as a payload type with ``ok=True``), so this rule
    matches against the ``declaredName`` of *any* element, not a fixed enum of kinds.

    Scope (F4, a builder-scope design call under DL-039(3)): an unqualified name is resolved only
    against declared names in the *same package* as the transition itself (walking the ownership chain
    to the nearest enclosing Package, ``_owning_package_qn``); a qualified name (``"Outer::Start"``) is
    resolved against every element's qualified name anywhere in the model. This is narrower than
    resolving an unqualified name against the whole model: OpenSysML's own reference resolution
    elsewhere (e.g. `perform`) does not resolve an unqualified cross-package name either, so matching
    that posture is more consistent with the tool's actual behavior than treating "anywhere in the
    model" as equivalent to "in scope" would be. The accepted limitation this narrowing carries — an
    unqualified reference to a name legitimately brought into scope by an explicit import from another
    package is a false negative this rule cannot currently detect as *unresolved if it in fact isn't* —
    is recorded in DEFERRED.md D-023: implementing full import-graph resolution is out of this rule's
    scope, so an import case is not attempted at all rather than guessed at (same "skip rather than
    falsely flag" posture the other two gap rules already take, their own F4).

    Both real fixtures (ch07, ch08) are single-package models, so this cannot be exercised by them one
    way or the other; they produce zero findings from this rule regardless, because their own triggers
    (`Start`, `Finish`, `Cancel`) resolve within their own package either way.
    """
    idx = index or query.ApiIndex(model)

    all_qualified_names: set[str] = set()
    declared_by_package: dict[str | None, set[str]] = {}
    for e in idx.elements:
        qn = e.get("qualifiedName")
        if qn:
            all_qualified_names.add(qn)
        name = e.get("declaredName")
        if name:
            pkg = _owning_package_qn(idx, qn)
            declared_by_package.setdefault(pkg, set()).add(name)

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
            resolved = payload_name in all_qualified_names
        else:
            pkg = _owning_package_qn(idx, t_id)
            resolved = payload_name in declared_by_package.get(pkg, set())
        if resolved:
            continue
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
        applies_from=None,
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
