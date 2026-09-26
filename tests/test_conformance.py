"""src/toaster/conformance.py: staged project checks, always-on language tier."""

from dataclasses import replace
from pathlib import Path

import opensysml
import pytest

from toaster import conformance as cf
from toaster.conformance import ConformanceCheck

ROOT = Path(__file__).resolve().parents[1]

MISMATCH = """
package P {
  port def PowerPort; port def FuelPort;
  part def Outlet { port o : PowerPort; }
  part def Torch { port fuelIn : FuelPort; }
  part outlet : Outlet; part torch : Torch;
  connect outlet.o to torch.fuelIn;
}
"""


@pytest.fixture(scope="module")
def conn():
    c = opensysml.connect(version="v0.9.0")
    yield c
    c.close()


@pytest.fixture(scope="module")
def ch08(conn):
    m = conn.load_from_content((ROOT / "models" / "ch08-cumulative.sysml").read_text(), strict=False)
    assert m.ok
    return m


@pytest.fixture(scope="module")
def mismatch(conn):
    m = conn.load_from_content(MISMATCH, strict=False)
    assert m.ok
    return m


def _check(findings, applies_from, calls=None):
    def run(_model):
        if calls is not None:
            calls.append(1)
        return list(findings)

    return ConformanceCheck("c", "d", run, applies_from, MISMATCH)


def test_open_before_applies_from_and_run_not_called() -> None:
    calls: list[int] = []
    r = cf.evaluate(_check([{"x": 1}], (2, 3), calls), None, (2, 2))
    assert (r.status, r.findings, r.applies_from, calls) == ("open", [], (2, 3), [])


def test_passed_or_failed_at_and_after_applies_from() -> None:
    assert cf.evaluate(_check([], (2, 3)), None, (2, 3)).status == "passed"
    assert cf.evaluate(_check([], (2, 3)), None, (5, 1)).status == "passed"
    r = cf.evaluate(_check([{"x": 1}], (2, 3)), None, (2, 3))
    assert r.status == "failed" and r.findings == [{"x": 1}]


def test_open_when_unscheduled_even_if_fault_exists(mismatch) -> None:
    calls: list[int] = []
    assert cf.evaluate(_check([{"x": 1}], None, calls), mismatch, (99, 99)).status == "open"
    assert calls == []
    assert cf.query.port_type_mismatches(mismatch)  # the fault is real
    assert cf.evaluate(cf.REGISTRY[0], mismatch, (99, 99)).status == "open"


def test_stage_ordering_across_chapters_and_sections() -> None:
    c = _check([], (2, 3))
    status = lambda s: cf.evaluate(c, None, s).status
    assert status((1, 9)) == "open"
    assert status((2, 2)) == "open"
    assert status((2, 3)) == "passed"
    assert status((3, 1)) == "passed"


def test_language_failure_reported_separately(conn) -> None:
    bad = conn.load_from_content("package P { part def A :> Missing; }", strict=False)
    rep = cf.report(bad, (1, 1), [_check([], (1, 1))])
    assert rep["language"]["ok"] is False
    assert rep["language"]["diagnostics"] and all(isinstance(d, str) for d in rep["language"]["diagnostics"])
    assert [r.status for r in rep["project"]] == ["open"]
    assert [r.reason for r in rep["project"]] == ["not applied: language conformance failed"]
    assert [r.findings for r in rep["project"]] == [[]]


def test_run_not_called_on_language_failed_model(conn) -> None:
    bad = conn.load_from_content("package P { part def A :> Missing; }", strict=False)
    calls: list[int] = []
    rep = cf.report(bad, (9, 9), [_check([{"x": 1}], (1, 1), calls)])
    assert calls == []
    assert [(r.status, r.findings) for r in rep["project"]] == [("open", [])]


def test_open_reasons_distinguish_stage_and_unscheduled() -> None:
    assert cf.evaluate(_check([], (2, 3)), None, (2, 2)).reason == "not applied: stage not reached"
    assert cf.evaluate(_check([], None), None, (9, 9)).reason == "not applied: unscheduled"
    assert cf.evaluate(_check([], (2, 3)), None, (2, 3)).reason is None


def test_language_ok_on_valid_model(ch08) -> None:
    assert cf.language_conformance(ch08)["ok"] is True


def test_prove_negative_control(conn) -> None:
    assert cf.prove_negative_control(cf.REGISTRY[0], conn) is True
    assert cf.prove_negative_control(replace(_check([], (1, 1)), negative_control=MISMATCH), conn) is False


def test_prove_negative_control_requires_load_ok(conn) -> None:
    broken = replace(cf.REGISTRY[0], negative_control="package P { part def A :> Missing; }")
    assert cf.prove_negative_control(broken, conn) is False


def test_registry_port_type_entry() -> None:
    assert [c.id for c in cf.REGISTRY] == ["port-type"]
    assert cf.REGISTRY[0].applies_from is None
    assert cf.REGISTRY[0].run is cf.query.port_type_mismatches


def test_report_shape(ch08) -> None:
    rep = cf.report(ch08, (1, 1))
    assert set(rep) == {"language", "project"}
    assert set(rep["language"]) == {"ok", "diagnostics"}
    assert [(r.check_id, r.status) for r in rep["project"]] == [("port-type", "open")]


def test_port_type_check_scheduled(ch08, mismatch) -> None:
    scheduled = replace(cf.REGISTRY[0], applies_from=(1, 1))
    assert cf.evaluate(scheduled, ch08, (2, 1)).status == "passed"
    assert cf.evaluate(scheduled, mismatch, (2, 1)).status == "failed"
