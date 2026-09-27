"""Two-tier conformance (AGENTS.md 1.9, DL-025, DL-039).

Language conformance is always on and reported separately. It now has two parts (DL-039): `ok` (`model.ok`, the
loader's own proxy for language conformance) and `gap_findings` (`language_gap_findings`), constructs OpenSysML
v0.9.0 accepts but the spec forbids. `model.ok` is a proxy, not the definition: a model can have `ok` True and
still be language non-conformant if `gap_findings` is non-empty. Project conformance checks carry five statuses:

- open: not yet applied, because the check is unscheduled (`applies_from` is None) or its stage has not been reached.
- passed: applied to a loaded model and found nothing.
- failed: applied to a loaded model and found something.
- blocked: cannot be applied until a stated condition holds. When the model fails language conformance (`model.ok`
  is False, or `gap_findings` is non-empty) every project check that would otherwise run (scheduled, stage reached,
  not wont-do) is blocked instead, with a reason and `unblock_when` naming the failure.
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
    """
    idx = index or query.ApiIndex(model)
    findings = []
    for a in query.find_allocations(model, index=idx):
        for end in a["ends"]:
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
                        "element": a["id"],
                        "message": (
                            f"allocation {a['id']} end resolves to {target_type} "
                            f"{target_qn}, not a Feature"
                        ),
                    }
                )
    return findings


def _part_typed_only_by_item_def(
    model: Any, index: "query.ApiIndex | None" = None
) -> list[dict]:
    """Rule (DL-039): a PartUsage none of whose types is a PartDefinition.

    SysML `validatePartUsagePartDefinition` (formal/2026-03-02 p. 323): "At least one of the itemDefinitions
    of a PartUsage must be a PartDefinition." A PartUsage with no declared type at all is out of scope for
    this rule (there is no itemDefinition to check).
    """
    idx = index or query.ApiIndex(model)
    findings = []
    for e in idx.of_type("PartUsage"):
        e_qn = e.get("qualifiedName")
        type_qns = idx.type_names(e_qn) if e_qn else []
        if not type_qns:
            continue
        type_kinds = [idx.by_qn.get(tq, {}).get("@type") for tq in type_qns]
        if "PartDefinition" not in type_kinds:
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
                        f"{e_qn} is typed only by {type_kinds}, none a PartDefinition"
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
]


def language_gap_findings(model: Any) -> list[dict]:
    """Always-on language-gap check (AGENTS.md 1.9, DL-039), not a staged project check.

    Runs every rule in `GAP_RULES` against `model` and returns the concatenated findings. Each finding is a
    dict with at least `rule`, `constraint`, `element` and `message` keys. Flags constructs OpenSysML v0.9.0
    accepts (`model.ok` is True) but the spec forbids; part of language conformance, so it runs regardless
    of stage.
    """
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

REGISTRY: list[ConformanceCheck] = [
    ConformanceCheck(
        id="port-type",
        description="Connected ports have related declared types (OpenSysML v0.9.0 gap G4).",
        run=query.port_type_mismatches,
        applies_from=None,
        negative_control=_PORT_TYPE_CONTROL,
    ),
]

GAP_BLOCK_UNBLOCK_WHEN = "no language-tier violation, per the spec, is present (gap_findings is empty)"


def _gap_block_reason(gap_findings: list[dict]) -> str:
    rules = sorted({f["rule"] for f in gap_findings})
    return "language conformance failed: " + ", ".join(rules)


def _evaluate_with_gap_block(
    check: ConformanceCheck, model: Any, stage: Stage, reason: str
) -> Result:
    """Like `evaluate`, but a check that would run (scheduled, stage reached) is blocked instead.

    `wont-do` and `open` (unscheduled, or stage not reached) are unaffected: nothing they would have run is
    skipped that was not already skipped, so `evaluate`'s own logic applies unchanged.
    """
    if check.wont_do is not None or check.applies_from is None or stage < check.applies_from:
        return evaluate(check, model, stage)
    return Result(
        check.id, "blocked", [], check.applies_from, reason, GAP_BLOCK_UNBLOCK_WHEN
    )


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
        # language non-conformant too, and block every check that would otherwise run.
        reason = _gap_block_reason(language["gap_findings"])
        project = [_evaluate_with_gap_block(c, model, stage, reason) for c in checks]
    else:
        project = [evaluate(c, model, stage) for c in checks]
    return {"language": language, "project": project}
