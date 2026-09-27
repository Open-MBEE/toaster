"""src/toaster/conformance.py: staged project checks, always-on language tier."""

from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import opensysml
import pytest

from toaster import conformance as cf
from toaster.conformance import ConformanceCheck, WontDo

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
    m = conn.load_from_content(
        (ROOT / "models" / "ch08-cumulative.sysml").read_text(), strict=False
    )
    assert m.ok
    return m


@pytest.fixture(scope="module")
def mismatch(conn):
    m = conn.load_from_content(MISMATCH, strict=False)
    assert m.ok
    return m


UNBLOCK = "language conformance passes (model.ok is True)"
BAD = "package P { part def A :> Missing; }"
WONT = WontDo("no longer needed", "DL-099")


def _check(findings, applies_from, calls=None, wont_do=None):
    def run(_model):
        if calls is not None:
            calls.append(1)
        return list(findings)

    return ConformanceCheck("c", "d", run, applies_from, MISMATCH, wont_do)


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
    assert (
        cf.evaluate(_check([{"x": 1}], None, calls), mismatch, (99, 99)).status
        == "open"
    )
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
    assert rep["language"]["diagnostics"] and all(
        isinstance(d, str) for d in rep["language"]["diagnostics"]
    )
    assert [r.status for r in rep["project"]] == ["blocked"]
    assert [r.reason for r in rep["project"]] == [
        "not applied: language conformance failed"
    ]
    assert [r.unblock_when for r in rep["project"]] == [UNBLOCK]
    assert [r.findings for r in rep["project"]] == [[]]


def test_run_not_called_on_language_failed_model(conn) -> None:
    bad = conn.load_from_content("package P { part def A :> Missing; }", strict=False)
    calls: list[int] = []
    rep = cf.report(bad, (9, 9), [_check([{"x": 1}], (1, 1), calls)])
    assert calls == []
    assert [(r.status, r.findings) for r in rep["project"]] == [("blocked", [])]


def test_open_reasons_distinguish_stage_and_unscheduled() -> None:
    assert (
        cf.evaluate(_check([], (2, 3)), None, (2, 2)).reason
        == "not applied: stage not reached"
    )
    assert (
        cf.evaluate(_check([], None), None, (9, 9)).reason == "not applied: unscheduled"
    )
    assert cf.evaluate(_check([], (2, 3)), None, (2, 3)).reason is None


def test_language_ok_on_valid_model(ch08) -> None:
    assert cf.language_conformance(ch08)["ok"] is True


def test_prove_negative_control(conn) -> None:
    assert cf.prove_negative_control(cf.REGISTRY[0], conn) is True
    assert (
        cf.prove_negative_control(
            replace(_check([], (1, 1)), negative_control=MISMATCH), conn
        )
        is False
    )


def test_prove_negative_control_requires_load_ok(conn) -> None:
    broken = replace(
        cf.REGISTRY[0], negative_control="package P { part def A :> Missing; }"
    )
    assert cf.prove_negative_control(broken, conn) is False


def test_registry_port_type_entry() -> None:
    assert [c.id for c in cf.REGISTRY] == ["port-type"]
    assert cf.REGISTRY[0].applies_from is None
    assert cf.REGISTRY[0].run is cf.query.port_type_mismatches


def test_report_shape(ch08) -> None:
    rep = cf.report(ch08, (1, 1))
    assert set(rep) == {"language", "project"}
    assert set(rep["language"]) == {"ok", "diagnostics", "gap_findings"}
    assert [(r.check_id, r.status) for r in rep["project"]] == [("port-type", "open")]


def test_port_type_check_scheduled(ch08, mismatch) -> None:
    scheduled = replace(cf.REGISTRY[0], applies_from=(1, 1))
    assert cf.evaluate(scheduled, ch08, (2, 1)).status == "passed"
    assert cf.evaluate(scheduled, mismatch, (2, 1)).status == "failed"


def test_blocked_for_unscheduled_check_on_language_failure(conn) -> None:
    bad = conn.load_from_content(BAD, strict=False)
    r = cf.report(bad, (9, 9), [_check([], None)])["project"][0]
    assert (r.status, r.unblock_when, r.applies_from) == ("blocked", UNBLOCK, None)


def test_open_carries_no_unblock_when() -> None:
    assert cf.evaluate(_check([], (2, 3)), None, (2, 2)).unblock_when is None
    assert cf.evaluate(_check([], None), None, (2, 2)).unblock_when is None


def test_wont_do_at_any_stage_and_run_not_called() -> None:
    calls: list[int] = []
    c = _check([{"x": 1}], (2, 3), calls, WONT)
    for stage in [(1, 1), (2, 3), (9, 9)]:
        r = cf.evaluate(c, None, stage)
        assert (r.status, r.findings, r.unblock_when) == ("wont-do", [], None)
        assert r.reason == "no longer needed (changed: DL-099)"
    assert calls == []
    assert cf.evaluate(_check([], None, wont_do=WONT), None, (1, 1)).status == "wont-do"


def test_wont_do_overrides_fault_and_language_failure(conn, mismatch) -> None:
    calls: list[int] = []
    c = _check([{"x": 1}], (1, 1), calls, WONT)
    assert cf.evaluate(c, mismatch, (9, 9)).status == "wont-do"
    bad = conn.load_from_content(BAD, strict=False)
    rep = cf.report(bad, (9, 9), [c, _check([], (1, 1), calls)])
    assert [r.status for r in rep["project"]] == ["wont-do", "blocked"]
    assert rep["project"][0].reason == "no longer needed (changed: DL-099)"
    assert rep["project"][0].unblock_when is None
    assert calls == []


def test_wont_do_dataclass_frozen() -> None:
    with pytest.raises(FrozenInstanceError):
        WONT.reason = "x"  # type: ignore[misc]


def test_blocked_keeps_applies_from(conn) -> None:
    bad = conn.load_from_content(BAD, strict=False)
    r = cf.report(bad, (9, 9), [_check([], (1, 1))])["project"][0]
    assert (r.status, r.applies_from) == ("blocked", (1, 1))


def test_wont_do_keeps_applies_from(ch08, conn) -> None:
    bad = conn.load_from_content(BAD, strict=False)
    for model in (ch08, bad):
        r = cf.report(model, (1, 1), [_check([], (2, 3), wont_do=WONT)])["project"][0]
        assert (r.status, r.applies_from) == ("wont-do", (2, 3))


def test_blocked_when_stage_not_reached_on_language_failure(conn) -> None:
    bad = conn.load_from_content(BAD, strict=False)
    calls: list[int] = []
    r = cf.report(bad, (1, 1), [_check([], (5, 5), calls)])["project"][0]
    assert (r.status, r.unblock_when, r.applies_from) == ("blocked", UNBLOCK, (5, 5))
    assert calls == []


def test_unscheduled_wont_do_on_language_failure(conn) -> None:
    bad = conn.load_from_content(BAD, strict=False)
    calls: list[int] = []
    c = _check([{"x": 1}], None, calls, WONT)
    r = cf.report(bad, (9, 9), [c])["project"][0]
    assert (r.status, r.unblock_when, r.applies_from) == ("wont-do", None, None)
    assert calls == []


def test_empty_registry_means_no_checks(ch08, conn) -> None:
    bad = conn.load_from_content(BAD, strict=False)
    for model in (ch08, bad):
        assert cf.report(model, (9, 9), [])["project"] == []


# --- language gap findings (DL-039) ---

CLEAN_LANGUAGE_MODEL = """
package P {
  action def ApplyHeat;
  part def HeatingSystem;
  part heater : HeatingSystem;
  action doApply : ApplyHeat;
  allocate doApply to heater;
  item def Start;
  part def BreadLoader;
  part bread : BreadLoader;
}
"""


def test_allocate_between_definitions_control_triggers_finding(conn) -> None:
    rule = next(r for r in cf.GAP_RULES if r.name == "allocate-between-definitions")
    model = conn.load_from_content(rule.negative_control, strict=False)
    assert model.ok
    findings = rule.check(model)
    assert findings
    assert all(f["rule"] == "allocate-between-definitions" for f in findings)
    assert all({"rule", "constraint", "element", "message"} <= f.keys() for f in findings)


def test_part_typed_only_by_item_def_control_triggers_finding(conn) -> None:
    rule = next(r for r in cf.GAP_RULES if r.name == "part-typed-only-by-item-def")
    model = conn.load_from_content(rule.negative_control, strict=False)
    assert model.ok
    findings = rule.check(model)
    assert findings
    assert all(f["rule"] == "part-typed-only-by-item-def" for f in findings)
    assert all({"rule", "constraint", "element", "message"} <= f.keys() for f in findings)


def test_clean_model_has_no_gap_findings(conn) -> None:
    model = conn.load_from_content(CLEAN_LANGUAGE_MODEL, strict=False)
    assert model.ok
    assert cf.language_gap_findings(model) == []


def test_language_gap_findings_on_real_fixture(ch08) -> None:
    # ch05/ch08 keep their violations (Pass 4's job to re-derive them; not this task's).
    findings = cf.language_gap_findings(ch08)
    rules = {f["rule"] for f in findings}
    assert rules == {"allocate-between-definitions", "part-typed-only-by-item-def"}


def test_language_conformance_reports_gap_findings(conn) -> None:
    rule = next(r for r in cf.GAP_RULES if r.name == "allocate-between-definitions")
    model = conn.load_from_content(rule.negative_control, strict=False)
    lc = cf.language_conformance(model)
    assert lc["ok"] is True
    assert lc["gap_findings"]


def test_prove_negative_control_covers_both_gap_rules(conn) -> None:
    for rule in cf.GAP_RULES:
        model = conn.load_from_content(rule.negative_control, strict=False)
        assert model.ok
        assert rule.check(model)


# --- report() blocks on gap findings even when model.ok is True (DL-039) ---


def test_report_blocks_scheduled_check_with_specific_reason(conn) -> None:
    rule = next(r for r in cf.GAP_RULES if r.name == "allocate-between-definitions")
    gapped = conn.load_from_content(rule.negative_control, strict=False)
    scheduled = _check([], (1, 1))
    r = cf.report(gapped, (2, 1), [scheduled])["project"][0]
    assert r.status == "blocked"
    assert r.reason == "language conformance failed: allocate-between-definitions"
    assert r.reason != cf.LANGUAGE_BLOCK_REASON
    assert r.findings == []


def test_report_does_not_run_scheduled_check_on_gap_findings(conn) -> None:
    rule = next(r for r in cf.GAP_RULES if r.name == "allocate-between-definitions")
    gapped = conn.load_from_content(rule.negative_control, strict=False)
    calls: list[int] = []
    scheduled = _check([{"x": 1}], (1, 1), calls)
    cf.report(gapped, (2, 1), [scheduled])
    assert calls == []


def test_report_open_check_unaffected_by_gap_findings(conn) -> None:
    rule = next(r for r in cf.GAP_RULES if r.name == "allocate-between-definitions")
    gapped = conn.load_from_content(rule.negative_control, strict=False)
    unscheduled = _check([], None)
    not_yet = _check([], (5, 5))
    r_unscheduled = cf.report(gapped, (1, 1), [unscheduled])["project"][0]
    r_not_yet = cf.report(gapped, (1, 1), [not_yet])["project"][0]
    assert r_unscheduled.status == "open"
    assert r_not_yet.status == "open"


def test_report_wont_do_unaffected_by_gap_findings(conn) -> None:
    rule = next(r for r in cf.GAP_RULES if r.name == "allocate-between-definitions")
    gapped = conn.load_from_content(rule.negative_control, strict=False)
    c = _check([{"x": 1}], (1, 1), wont_do=WONT)
    r = cf.report(gapped, (9, 9), [c])["project"][0]
    assert r.status == "wont-do"


def test_report_gap_reason_lists_multiple_violated_rules(conn) -> None:
    both = conn.load_from_content(
        """
        package P {
          action def ApplyHeat;
          part def HeatingSystem;
          allocate ApplyHeat to HeatingSystem;
          item def Start;
          part def BreadLoader { part bread : Start; }
        }
        """,
        strict=False,
    )
    assert both.ok
    scheduled = _check([], (1, 1))
    r = cf.report(both, (2, 1), [scheduled])["project"][0]
    assert r.status == "blocked"
    assert r.reason == (
        "language conformance failed: allocate-between-definitions, "
        "part-typed-only-by-item-def"
    )


def test_report_clean_model_not_blocked_by_gap_findings(conn) -> None:
    clean = conn.load_from_content(CLEAN_LANGUAGE_MODEL, strict=False)
    scheduled = _check([], (1, 1))
    r = cf.report(clean, (2, 1), [scheduled])["project"][0]
    assert r.status == "passed"


