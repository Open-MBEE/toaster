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


def _unresolved_transition_trigger(
    model: Any, index: "query.ApiIndex | None" = None
) -> list[dict]:
    """Rule (DL-039, D-023): a TransitionUsage's ``accept`` trigger name that resolves to no ItemDefinition.

    SysML v2.0 (formal/2026-03-02) makes ``accept <name>`` a full, structured element, not a string:
    8.3.18.9 TransitionUsage declares ``/triggerAction : AcceptActionUsage [0..*]``, derived from an
    owned TransitionFeatureMembership (`deriveTransitionUsageTriggerAction`); 8.3.18.8
    TransitionFeatureMembership's `validateTransitionFeatureMembershipTriggerAction` requires that
    element to be a kind of AcceptActionUsage; 8.3.16 AcceptActionUsage gives it a
    `payloadParameter : ReferenceUsage`, exactly where a payload/signal type is resolved and checked.
    No single named constraint says in so many words "the trigger name must resolve to a declared
    type" — the case rests on the structural fact that the spec models a trigger as a resolvable,
    typed element throughout (gap-issue-drafts.md Draft 9). OpenSysML v0.9.0 keeps the trigger only as
    the bare string `sysx:trigger` in the API-JSON export — never a reference — and accepts an
    undefined or misspelled name with `ok=True` and no diagnostic (D-023): the transition then
    silently never fires at execution.

    Only ``sysx:triggerKeyword == "accept"`` is in scope. A transition can also trigger on a boolean
    guard (`when <expr>`, `sysx:triggerKeyword == "when"`) or have no trigger at all (an unconditional
    transition, `sysx:trigger` absent) — confirmed directly against the tool: a `when` trigger's
    `sysx:trigger` string names an attribute/expression, not an item def, and would false-positive here
    if treated the same as `accept`; an untriggered transition carries neither key at all. Both are
    skipped by construction (the `.get(...) != "accept"` guard), not flagged.

    "In scope" for resolution is taken as *any* ItemDefinition anywhere in the loaded model, not scoped to
    the trigger's own package: the flat API-JSON export carries no reliable per-element import/visibility
    information for a lightweight index-based check (unlike a type reference, which the tool resolves to
    a concrete element itself), and a narrower same-package rule would false-positive on a legitimate
    cross-package import, contrary to the "skip rather than falsely flag" posture the other two gap rules
    already take (F4). The real ch07 fixture cannot distinguish the two readings (its three item defs and
    its state machine are declared in the same package), so both give the same, empty result there; it
    produces zero findings from this rule either way.
    """
    idx = index or query.ApiIndex(model)
    item_def_names = {
        e["declaredName"] for e in idx.of_type("ItemDefinition") if e.get("declaredName")
    }
    findings = []
    for t in idx.of_type("TransitionUsage"):
        if t.get("sysx:triggerKeyword") != "accept":
            continue
        trigger = t.get("sysx:trigger")
        if not trigger or trigger in item_def_names:
            continue
        t_id = t.get("qualifiedName")
        findings.append(
            {
                "rule": "unresolved-transition-trigger",
                "constraint": (
                    "SysML v2.0 formal/2026-03-02: 8.3.18.9 TransitionUsage "
                    "(/triggerAction : AcceptActionUsage), 8.3.18.8 "
                    "TransitionFeatureMembership (validateTransitionFeatureMembershipTriggerAction), "
                    "8.3.16 AcceptActionUsage (payloadParameter) — a trigger is a structured, "
                    "resolvable element, so its name must resolve to a defined type in scope"
                ),
                "element": t_id,
                "message": (
                    f"transition {t_id} accepts trigger {trigger!r}, which "
                    "resolves to no ItemDefinition in the model"
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
        constraint=(
            "SysML v2.0 formal/2026-03-02: 8.3.18.9 TransitionUsage "
            "(/triggerAction : AcceptActionUsage), 8.3.18.8 TransitionFeatureMembership "
            "(validateTransitionFeatureMembershipTriggerAction), 8.3.16 AcceptActionUsage "
            "(payloadParameter) — a trigger is a structured, resolvable element, so its "
            "name must resolve to a defined type in scope"
        ),
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
