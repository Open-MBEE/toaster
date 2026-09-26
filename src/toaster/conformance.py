"""Two-tier conformance (AGENTS.md 1.9).

Language conformance is always on and reported separately. Project conformance checks are staged: a check with no
`applies_from`, or one whose stage has not been reached, is reported open, never passed.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from toaster import query

Stage = tuple[int, int]  # (chapter, section), ordered lexicographically


@dataclass(frozen=True)
class ConformanceCheck:
    id: str
    description: str
    run: Callable[[Any], list[dict]]
    applies_from: Stage | None
    negative_control: str  # SysML source that must load ok and produce at least one finding


@dataclass
class Result:
    check_id: str
    status: str  # "open" | "passed" | "failed"
    findings: list[dict] = field(default_factory=list)
    applies_from: Stage | None = None


def evaluate(check: ConformanceCheck, model: Any, stage: Stage) -> Result:
    if check.applies_from is None or stage < check.applies_from:
        return Result(check.id, "open", [], check.applies_from)
    findings = check.run(model)
    return Result(check.id, "failed" if findings else "passed", findings, check.applies_from)


def language_conformance(model: Any) -> dict:
    return {"ok": model.ok, "diagnostics": [str(getattr(d, "message", d)) for d in model.diagnostics]}


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


def report(model: Any, stage: Stage, registry: list[ConformanceCheck] | None = None) -> dict:
    checks = REGISTRY if registry is None else registry
    return {"language": language_conformance(model), "project": [evaluate(c, model, stage) for c in checks]}

