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
def ch07(conn):
    m = conn.load_from_content(
        (ROOT / "models" / "ch07-cumulative.sysml").read_text(), strict=False
    )
    assert m.ok
    return m


@pytest.fixture(scope="module")
def mismatch(conn):
    m = conn.load_from_content(MISMATCH, strict=False)
    assert m.ok
    return m


@pytest.fixture(scope="module")
def ch03(conn):
    m = conn.load_from_content(
        (ROOT / "models" / "ch03-cumulative.sysml").read_text(), strict=False
    )
    assert m.ok
    return m


@pytest.fixture(scope="module")
def ch04(conn):
    m = conn.load_from_content(
        (ROOT / "models" / "ch04-cumulative.sysml").read_text(), strict=False
    )
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
    assert [c.id for c in cf.REGISTRY] == ["port-type", "satisfaction-claims-evaluated"]
    assert cf.REGISTRY[0].applies_from is None
    assert cf.REGISTRY[0].run is cf.query.port_type_mismatches


def test_report_shape(ch08) -> None:
    # ch08 carries known gap findings (test_language_gap_findings_on_real_fixture; Pass 4's job to
    # re-derive, not this task's), so both REGISTRY checks are blocked, not open — port-type because
    # it is unscheduled, satisfaction-claims-evaluated because a language failure blocks it regardless
    # of schedule or stage reached (DL-048; see test_satisfaction_claims_evaluated_scheduled_* below).
    rep = cf.report(ch08, (1, 1))
    assert set(rep) == {"language", "project"}
    assert set(rep["language"]) == {"ok", "diagnostics", "gap_findings"}
    assert [(r.check_id, r.status) for r in rep["project"]] == [
        ("port-type", "blocked"),
        ("satisfaction-claims-evaluated", "blocked"),
    ]
    assert all(
        r.reason
        == "language conformance failed: allocate-between-definitions, "
        "part-typed-only-by-item-def"
        for r in rep["project"]
    )


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


UNRESOLVED_TRANSITION_TRIGGER_CLEAN = """
package P {
  item def Start;
  item def Finish;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    state ready;
    transition first idle accept Start then heating;
    transition first heating accept Finish then ready;
  }
}
"""

# F3 (review of PASS4-000-B): a bare `when <expr>` transition (no `accept`) is not valid SysML —
# sysml-toolkit rejects it ("expected `then`, found `when`") even though OpenSysML silently accepts it
# (itself an unrecorded gap, not this rule's job to guard). The real spec form of a change trigger is
# `accept when <expr>`. Both this and a time trigger (`accept after <duration>`) are expressions, not
# names, and must not be flagged even though neither resolves to a declared element (F2).
UNRESOLVED_TRANSITION_TRIGGER_CHANGE_TRIGGER = """
package P {
  private import ScalarValues::*;
  item def Start;
  attribute someFlag : Boolean;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Start then heating;
    transition first heating accept when someFlag then idle;
  }
}
"""

UNRESOLVED_TRANSITION_TRIGGER_TIME_TRIGGER = """
package P {
  private import ScalarValues::*;
  private import SI::*;
  item def Start;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Start then heating;
    transition first heating accept after 5 [s] then idle;
  }
}
"""

UNRESOLVED_TRANSITION_TRIGGER_UNCONDITIONAL = """
package P {
  item def Start;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Start then heating;
    transition first heating then idle;
  }
}
"""

# F2 (review of PASS4-000-B): a qualified trigger name must resolve against fully-qualified names
# anywhere in the model (F4's scope ruling), not just the same package.
UNRESOLVED_TRANSITION_TRIGGER_QUALIFIED_NAME = """
package Outer {
  item def Start;
}
package P {
  private import Outer::Start;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Outer::Start then heating;
  }
}
"""

# F2: a named payload ("s : Start") resolves the part after the colon, not the whole string.
UNRESOLVED_TRANSITION_TRIGGER_NAMED_PAYLOAD = """
package P {
  item def Start;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept s : Start then heating;
  }
}
"""

# F2: the payload type need not be an ItemDefinition — any kind with a declaredName (here: part def,
# port def, attribute def, enum def, and an existing item usage referenced by name) is a legal payload
# type per the grammar and must resolve.
UNRESOLVED_TRANSITION_TRIGGER_NON_ITEM_DEF_PAYLOADS = """
package P {
  item def Start;
  item existingStart : Start;
  part def Widget;
  port def PortyThing;
  attribute def AttrThing;
  enum def EnumThing { enum a; }
  state Cycle {
    entry; then a1;
    state a1; state a2; state a3; state a4; state a5;
    transition first a1 accept existingStart then a2;
    transition first a2 accept Widget then a3;
    transition first a3 accept PortyThing then a4;
    transition first a4 accept AttrThing then a5;
  }
  state Cycle2 {
    entry; then b1;
    state b1; state b2;
    transition first b1 accept EnumThing then b2;
  }
}
"""

# F2/F4: a qualified reference to something that genuinely does not exist must still be flagged.
UNRESOLVED_TRANSITION_TRIGGER_QUALIFIED_NONEXISTENT = """
package Outer {
  item def Start;
}
package P {
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Outer::Nope then heating;
  }
}
"""


def test_registry_includes_unresolved_transition_trigger() -> None:
    rule = next(r for r in cf.GAP_RULES if r.name == "unresolved-transition-trigger")
    assert rule.check is cf._unresolved_transition_trigger


def test_unresolved_transition_trigger_control_triggers_finding(conn) -> None:
    rule = next(r for r in cf.GAP_RULES if r.name == "unresolved-transition-trigger")
    model = conn.load_from_content(rule.negative_control, strict=False)
    assert model.ok
    findings = rule.check(model)
    assert len(findings) == 1
    f = findings[0]
    assert {"rule", "constraint", "element", "message"} <= f.keys()
    assert f["rule"] == "unresolved-transition-trigger"
    assert f["element"] == "P::Cycle::@4"
    assert "Strat" in f["message"]


def test_unresolved_transition_trigger_clean_model_has_no_findings(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_CLEAN, strict=False
    )
    assert model.ok
    assert cf._unresolved_transition_trigger(model) == []


def test_unresolved_transition_trigger_ignores_expression_and_untriggered(conn) -> None:
    # F2/F3: a real `accept when <expr>` change trigger, a real `accept after <duration>` time
    # trigger, and an untriggered (unconditional) transition are none of them a name to resolve, and
    # must not be flagged.
    for src in (
        UNRESOLVED_TRANSITION_TRIGGER_CHANGE_TRIGGER,
        UNRESOLVED_TRANSITION_TRIGGER_TIME_TRIGGER,
        UNRESOLVED_TRANSITION_TRIGGER_UNCONDITIONAL,
    ):
        model = conn.load_from_content(src, strict=False)
        assert model.ok
        assert cf._unresolved_transition_trigger(model) == []


def test_unresolved_transition_trigger_qualified_name_resolves(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_QUALIFIED_NAME, strict=False
    )
    assert model.ok
    assert cf._unresolved_transition_trigger(model) == []


def test_unresolved_transition_trigger_named_payload_resolves(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_NAMED_PAYLOAD, strict=False
    )
    assert model.ok
    assert cf._unresolved_transition_trigger(model) == []


def test_unresolved_transition_trigger_non_item_def_payloads_resolve(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_NON_ITEM_DEF_PAYLOADS, strict=False
    )
    assert model.ok
    assert cf._unresolved_transition_trigger(model) == []


def test_unresolved_transition_trigger_qualified_nonexistent_is_flagged(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_QUALIFIED_NONEXISTENT, strict=False
    )
    assert model.ok
    findings = cf._unresolved_transition_trigger(model)
    assert len(findings) == 1
    assert findings[0]["message"].count("Outer::Nope") == 2


# --- round 2 (F4 corrected: same-package-only scoping was wrong; see the check's docstring) ---

# A same-package-only reading would flag this (item def Start lives in a *different* package, A, and
# is brought into scope only by the wildcard import). Distinct from the plain same-package clean model
# above: this is the specific case round 1's scoping broke.
UNRESOLVED_TRANSITION_TRIGGER_CROSS_PACKAGE_WILDCARD_IMPORT = """
package A {
  item def Start;
}
package B {
  private import A::*;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Start then heating;
  }
}
"""

UNRESOLVED_TRANSITION_TRIGGER_CROSS_PACKAGE_MEMBER_IMPORT = """
package A {
  item def Start;
}
package B {
  private import A::Start;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Start then heating;
  }
}
"""

# Round 2, final ruling: a genuine no-import cross-package reference is NOT flagged by this rule. This
# is a deliberate, accepted false negative, not an oversight or a regression waiting to happen: getting
# it right needs real import-graph resolution, judged disproportionate for a guard against a defect
# that doesn't exist in any real fixture today (ch07/ch08 both give zero findings from this rule). It
# is the direct, accepted cost of resolving an unqualified name against the whole model (point 1) to
# correctly handle the cross-package-WITH-import and nested-package cases above, which are the ones
# that actually occur in real chapter content. This test exists so a future change cannot silently
# regress those legitimate cases back to same-package-only scoping (round 1's mistake) without
# consciously overriding this documented choice.
UNRESOLVED_TRANSITION_TRIGGER_CROSS_PACKAGE_NO_IMPORT = """
package A {
  item def Start;
}
package B {
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Start then heating;
  }
}
"""

# A relative qualification (Inner::Start) whose full path is P::Inner::Start: the suffix match, not
# just an exact qualifiedName match, is what resolves it.
UNRESOLVED_TRANSITION_TRIGGER_RELATIVE_QUALIFIED = """
package P {
  package Inner {
    item def Start;
  }
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Inner::Start then heating;
  }
}
"""

# A real local nested package (Inner) with no member named Nope: the top segment IS visible locally,
# so this is a genuine broken reference, not a probable external one — still flagged, distinct from a
# qualified reference whose top segment matches no local package at all (below).
UNRESOLVED_TRANSITION_TRIGGER_RELATIVE_QUALIFIED_BAD = """
package P {
  package Inner {
    item def Start;
  }
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Inner::Nope then heating;
  }
}
"""

# The top segment ("Q") matches no local package AND no recognized external library: nothing backs
# reading it as external, so it is flagged, unlike a genuine library-qualified reference (below).
UNRESOLVED_TRANSITION_TRIGGER_WRONG_UNKNOWN_PACKAGE = """
package P {
  item def Start;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Q::Start then heating;
  }
}
"""

# A qualified reference into a recognized standard-library package this document never declares
# locally: skipped as a probable external reference, not flagged (contrast with Q::Start above, whose
# top segment is not on the recognized list at all).
UNRESOLVED_TRANSITION_TRIGGER_LIBRARY_QUALIFIED = """
package P {
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept ScalarValues::Boolean then heating;
  }
}
"""

# An unqualified name that fails to resolve locally, with a wildcard import of a recognized external
# library present: skipped, since the name might be a member of that import (round 2's corrected F4).
UNRESOLVED_TRANSITION_TRIGGER_LIBRARY_UNQUALIFIED_VIA_IMPORT = """
package P {
  private import ScalarValues::*;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Boolean then heating;
  }
}
"""

# Round 2 F4: `at` is a third time-trigger keyword (alongside `after`), an expression, not a name.
UNRESOLVED_TRANSITION_TRIGGER_AT_TIME = """
package P {
  attribute t : Time::TimeInstantValue;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept at t then heating;
  }
}
"""

# Round 2 F4: a subsetting named payload (`s :> sig`) resolves `sig`, not the whole string.
UNRESOLVED_TRANSITION_TRIGGER_SUBSETTING_PAYLOAD = """
package P {
  item def Start;
  item sig : Start;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept s :> sig then heating;
  }
}
"""


def test_unresolved_transition_trigger_cross_package_wildcard_import_resolves(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_CROSS_PACKAGE_WILDCARD_IMPORT, strict=False
    )
    assert model.ok
    assert cf._unresolved_transition_trigger(model) == []


def test_unresolved_transition_trigger_cross_package_member_import_resolves(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_CROSS_PACKAGE_MEMBER_IMPORT, strict=False
    )
    assert model.ok
    assert cf._unresolved_transition_trigger(model) == []


def test_unresolved_transition_trigger_no_import_cross_package_not_flagged(conn) -> None:
    # Deliberate, accepted false negative (round 2 final ruling, PASS4-000-B): a genuine no-import
    # cross-package reference is not flagged. See UNRESOLVED_TRANSITION_TRIGGER_CROSS_PACKAGE_NO_IMPORT
    # above and the check's own docstring for why. This is not an oversight to "fix" by reintroducing
    # same-package scoping — that regresses the cross-package/import and nested-package cases above.
    # Note: this resolves at step 1 (the flat, package-blind exact match), the same step that resolves
    # the legitimate with-import case above — it never reaches the step 2/3 logic below at all, because
    # "Start" really is, verbatim, declared somewhere in this model.
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_CROSS_PACKAGE_NO_IMPORT, strict=False
    )
    assert model.ok
    assert cf._unresolved_transition_trigger(model) == []


# Round 3 (F4): an unqualified name that matches nothing exactly, resembles nothing local closely
# enough (step 2), AND has no import to blame it on (step 3's fallback) must still be flagged as
# broken — this exercises step 3's own "no close match, no import -> flag" branch specifically,
# distinct from every other flagged case above, which are all caught earlier, at step 2 (a close
# match) or in the qualified-name path.
UNRESOLVED_TRANSITION_TRIGGER_UNRELATED_NAME_NO_IMPORT = """
package P {
  item def Start;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Zephyr then heating;
  }
}
"""


def test_unresolved_transition_trigger_unrelated_name_no_import_is_flagged(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_UNRELATED_NAME_NO_IMPORT, strict=False
    )
    assert model.ok
    findings = cf._unresolved_transition_trigger(model)
    assert len(findings) == 1
    assert "Zephyr" in findings[0]["message"]


def test_unresolved_transition_trigger_relative_qualified_resolves(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_RELATIVE_QUALIFIED, strict=False
    )
    assert model.ok
    assert cf._unresolved_transition_trigger(model) == []


def test_unresolved_transition_trigger_relative_qualified_bad_is_flagged(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_RELATIVE_QUALIFIED_BAD, strict=False
    )
    assert model.ok
    findings = cf._unresolved_transition_trigger(model)
    assert len(findings) == 1
    assert "Inner::Nope" in findings[0]["message"]


def test_unresolved_transition_trigger_wrong_unknown_package_is_flagged(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_WRONG_UNKNOWN_PACKAGE, strict=False
    )
    assert model.ok
    findings = cf._unresolved_transition_trigger(model)
    assert len(findings) == 1
    assert "Q::Start" in findings[0]["message"]


def test_unresolved_transition_trigger_library_qualified_resolves(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_LIBRARY_QUALIFIED, strict=False
    )
    assert model.ok
    assert cf._unresolved_transition_trigger(model) == []


def test_unresolved_transition_trigger_library_unqualified_via_import_resolves(
    conn,
) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_LIBRARY_UNQUALIFIED_VIA_IMPORT, strict=False
    )
    assert model.ok
    assert cf._unresolved_transition_trigger(model) == []


def test_unresolved_transition_trigger_at_time_is_expression(conn) -> None:
    model = conn.load_from_content(UNRESOLVED_TRANSITION_TRIGGER_AT_TIME, strict=False)
    assert model.ok
    assert cf._unresolved_transition_trigger(model) == []


def test_unresolved_transition_trigger_subsetting_payload_resolves(conn) -> None:
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_SUBSETTING_PAYLOAD, strict=False
    )
    assert model.ok
    assert cf._unresolved_transition_trigger(model) == []


def test_unresolved_transition_trigger_real_fixture_has_no_findings(ch07) -> None:
    # The real ch07 fixture's own triggers (Start, Finish, Cancel) all resolve today (D-023): this
    # proves the new rule does not false-positive on it, not that anything was broken before.
    assert cf._unresolved_transition_trigger(ch07) == []


# --- F4 round 3: the reviewer's own regression test, made permanent (this is exactly what caught the
# "any unresolvable import -> skip" bug: it silently defeated the rule on every real chapter model,
# since every one imports ScalarValues/SI/ISQ/MeasurementReferences). Uses the real fixture files
# themselves, not a synthetic model, because a synthetic model with the same shape did not catch it --
# only the real fixture's actual vocabulary and imports did.


@pytest.mark.parametrize("chapter", ["ch07", "ch08"])
def test_unresolved_transition_trigger_real_fixture_typo_is_flagged(conn, chapter) -> None:
    src = (ROOT / "models" / f"{chapter}-cumulative.sysml").read_text()
    typo_src = src.replace("accept Start then", "accept Strat then", 1)
    assert typo_src != src  # the replacement actually happened
    model = conn.load_from_content(typo_src, strict=False)
    assert model.ok
    findings = cf._unresolved_transition_trigger(model)
    assert len(findings) == 1
    assert "Strat" in findings[0]["message"]


UNRESOLVED_TRANSITION_TRIGGER_LOCAL_TYPO_WITH_UNRELATED_IMPORT = """
package P {
  private import ScalarValues::*;
  item def Start;
  state Cycle {
    entry; then idle;
    state idle;
    state heating;
    transition first idle accept Strat then heating;
  }
}
"""


def test_unresolved_transition_trigger_local_typo_still_flagged_with_unrelated_import(
    conn,
) -> None:
    # The exact combination the round-2 bug missed: a genuine local typo (Strat for Start) must still
    # be flagged even though the document also has an external library import (which, on its own,
    # would make an unrelated unresolved name like Boolean a probable import member and get skipped --
    # see test_unresolved_transition_trigger_library_unqualified_via_import_resolves above). The
    # similarity match (step 2) takes priority over the import fallback (step 3).
    model = conn.load_from_content(
        UNRESOLVED_TRANSITION_TRIGGER_LOCAL_TYPO_WITH_UNRELATED_IMPORT, strict=False
    )
    assert model.ok
    findings = cf._unresolved_transition_trigger(model)
    assert len(findings) == 1
    assert "Strat" in findings[0]["message"]


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


# --- F2: language_gap_findings must not crash on model.ok=False or an unresolvable connector end ---


def test_language_gap_findings_empty_when_model_not_ok(conn) -> None:
    bad = conn.load_from_content(BAD, strict=False)
    assert bad.ok is False
    assert cf.language_gap_findings(bad) == []


def test_language_conformance_does_not_crash_when_model_not_ok(conn) -> None:
    bad = conn.load_from_content(BAD, strict=False)
    lc = cf.language_conformance(bad)
    assert lc["ok"] is False
    assert lc["gap_findings"] == []


NOT_OK_MODEL_WITH_GAP_CONSTRUCTS = """
package P {
  action def A;
  part def B;
  allocate A to B;
  item def I;
  part def H { part x : I; }
  part y : Nope;
}
"""


def test_language_gap_findings_guard_holds_on_not_ok_model_with_gap_constructs(
    conn,
) -> None:
    # F8: the existing not-ok-model tests (above) use a BAD model with no gap constructs at all
    # (a broken specialization, no allocation, no item-typed part), so removing the
    # `if not model.ok: return []` guard entirely still passes them. This model is not-ok for an
    # unrelated reason (the unresolved `Nope` reference) but DOES contain a definition-level
    # allocate and an item-typed part — the guard must still return [] without attempting to run
    # the gap rules over it, not crash and not spuriously flag anything.
    model = conn.load_from_content(NOT_OK_MODEL_WITH_GAP_CONSTRUCTS, strict=False)
    assert model.ok is False
    assert cf.language_gap_findings(model) == []


def test_allocate_between_definitions_skips_unresolvable_connector_end(conn) -> None:
    # F2: model.ok is True, but one connector end's own element is missing from the API-JSON
    # export (a constructed export gap) — ApiIndex.end_path raises KeyError for it. The check
    # must catch that per end and skip it, not crash for every allocation.
    rule = next(r for r in cf.GAP_RULES if r.name == "allocate-between-definitions")
    model = conn.load_from_content(rule.negative_control, strict=False)
    assert model.ok
    baseline = cf._allocate_between_definitions(model)
    assert len(baseline) == 2  # both ends of `allocate ApplyHeat to HeatingSystem` are Definitions

    idx = cf.query.ApiIndex(model)
    allocation = next(e for e in idx.elements if e.get("@type") == "AllocationUsage")
    end_ref = allocation["connectorEnd"][0]
    end_id = end_ref["@id"] if isinstance(end_ref, dict) else end_ref
    del idx.by_id[end_id]
    with pytest.raises(KeyError):
        idx.end_path(end_ref)  # confirms this really does reproduce the underlying failure

    findings = cf._allocate_between_definitions(model, index=idx)
    # no crash, and the other, still-resolvable end's finding survives — only the unresolvable
    # end itself is skipped, not the whole check
    assert len(findings) == 1


def test_allocate_between_definitions_skips_end_without_reference_subsetting(conn) -> None:
    # A connector end whose own element has no `ownedReferenceSubsetting` (end_path returns []
    # rather than raising): the `if not end: continue` branch, distinct from the KeyError case
    # above (there, the end's own element is missing from the export entirely).
    rule = next(r for r in cf.GAP_RULES if r.name == "allocate-between-definitions")
    model = conn.load_from_content(rule.negative_control, strict=False)
    assert model.ok
    idx = cf.query.ApiIndex(model)
    allocation = next(e for e in idx.elements if e.get("@type") == "AllocationUsage")
    end_ref = allocation["connectorEnd"][0]
    end_id = end_ref["@id"] if isinstance(end_ref, dict) else end_ref
    idx.by_id[end_id].pop("ownedReferenceSubsetting", None)
    assert idx.end_path(end_ref) == []  # confirms this reproduces the no-subsetting case

    findings = cf._allocate_between_definitions(model, index=idx)
    # no crash, and the other end's finding survives — only the end with no subsetting is
    # skipped, not the whole check
    assert len(findings) == 1


def test_prove_negative_control_covers_both_gap_rules(conn) -> None:
    for rule in cf.GAP_RULES:
        model = conn.load_from_content(rule.negative_control, strict=False)
        assert model.ok
        assert rule.check(model)


# --- F4: part-typed-only-by-item-def must not flag valid SysML ---

PART_TYPED_BY_SUBTYPES_MODEL = """
package P {
  item def Start;
  part def Base;
  part def Mid :> Base;
  part def Deep :> Mid;
  part def X;
  part def Y;
  connection def Conn { end x : X; end y : Y; }
  interface def Iface { end x2 : X; end y2 : Y; }
  allocation def Alloc { end x3 : X; end y3 : Y; }
  part a : Conn;
  part b : Iface;
  part c : Alloc;
  part d : Deep;
  part e : Start;
  part combo : Start, Base;
  part untyped;
}
"""


@pytest.fixture(scope="module")
def subtypes_model(conn):
    m = conn.load_from_content(PART_TYPED_BY_SUBTYPES_MODEL, strict=False)
    assert m.ok
    return m


def test_part_typed_by_connection_def_not_flagged(subtypes_model) -> None:
    flagged = {f["element"] for f in cf._part_typed_only_by_item_def(subtypes_model)}
    assert "P::a" not in flagged


def test_part_typed_by_interface_def_not_flagged(subtypes_model) -> None:
    flagged = {f["element"] for f in cf._part_typed_only_by_item_def(subtypes_model)}
    assert "P::b" not in flagged


def test_part_typed_by_allocation_def_not_flagged(subtypes_model) -> None:
    flagged = {f["element"] for f in cf._part_typed_only_by_item_def(subtypes_model)}
    assert "P::c" not in flagged


def test_part_typed_by_two_level_specializing_part_def_not_flagged(subtypes_model) -> None:
    flagged = {f["element"] for f in cf._part_typed_only_by_item_def(subtypes_model)}
    assert "P::d" not in flagged


def test_part_typed_only_by_item_def_still_flagged(subtypes_model) -> None:
    flagged = {f["element"] for f in cf._part_typed_only_by_item_def(subtypes_model)}
    assert "P::e" in flagged


def test_part_typed_by_both_item_def_and_part_def_not_flagged(subtypes_model) -> None:
    # F6 mutation survivor: a part typed by BOTH an item def and a part def is satisfied by the
    # part def alone and must not be flagged.
    flagged = {f["element"] for f in cf._part_typed_only_by_item_def(subtypes_model)}
    assert "P::combo" not in flagged


def test_untyped_part_not_flagged(subtypes_model) -> None:
    # F6 mutation survivor: an untyped part (no type at all) is out of scope for this rule.
    flagged = {f["element"] for f in cf._part_typed_only_by_item_def(subtypes_model)}
    assert "P::untyped" not in flagged


def test_part_typed_by_view_def_not_flagged(conn) -> None:
    # F7: a view definition is a kind of part definition (SysML v2.0 formal/2026-03-02 7.26.1).
    model = conn.load_from_content(
        "package P { view def V; part a : V; }", strict=False
    )
    assert model.ok
    flagged = {f["element"] for f in cf._part_typed_only_by_item_def(model)}
    assert "P::a" not in flagged


def test_part_typed_by_rendering_def_not_flagged(conn) -> None:
    # F7: a rendering definition is a kind of part definition (SysML v2.0 formal/2026-03-02 7.26.1).
    model = conn.load_from_content(
        "package P { rendering def R; part b : R; }", strict=False
    )
    assert model.ok
    flagged = {f["element"] for f in cf._part_typed_only_by_item_def(model)}
    assert "P::b" not in flagged


def test_part_typed_by_unresolved_library_type_not_flagged(subtypes_model) -> None:
    # A type missing from the export (a library type not resolved) cannot be judged either way,
    # so it must not be flagged: construct that export gap by removing the type's own entry.
    idx = cf.query.ApiIndex(subtypes_model)
    start = idx.by_qn["P::Start"]
    del idx.by_id[start["@id"]]
    assert idx.type_names("P::e") == [None]  # confirms the gap: unresolved, not just missing
    flagged = {
        f["element"]
        for f in cf._part_typed_only_by_item_def(subtypes_model, index=idx)
    }
    assert "P::e" not in flagged


def test_only_part_definition_control_still_flagged_exactly(conn) -> None:
    rule = next(r for r in cf.GAP_RULES if r.name == "part-typed-only-by-item-def")
    model = conn.load_from_content(rule.negative_control, strict=False)
    assert model.ok
    findings = rule.check(model)
    assert [f["element"] for f in findings] == ["P::BreadLoader::bread"]


# --- F6 mutation survivor: pin GAP_BLOCK_UNBLOCK_WHEN's literal text, not just equality-to-constant ---


def test_gap_block_unblock_when_text() -> None:
    assert (
        cf.GAP_BLOCK_UNBLOCK_WHEN
        == "no language-tier violation, per the spec, is present (gap_findings is empty)"
    )


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


def test_report_blocks_unscheduled_and_stage_not_reached_checks_on_gap_findings(
    conn,
) -> None:
    # Symmetric with model.ok is False (PASS2-009 reading B): gap_findings blocks every non-wont-do
    # check, including one that is unscheduled or whose stage has not been reached.
    rule = next(r for r in cf.GAP_RULES if r.name == "allocate-between-definitions")
    gapped = conn.load_from_content(rule.negative_control, strict=False)
    reason = "language conformance failed: allocate-between-definitions"
    unscheduled = _check([], None)
    not_yet = _check([], (5, 5))
    r_unscheduled = cf.report(gapped, (1, 1), [unscheduled])["project"][0]
    r_not_yet = cf.report(gapped, (1, 1), [not_yet])["project"][0]
    assert (r_unscheduled.status, r_unscheduled.reason, r_unscheduled.applies_from) == (
        "blocked",
        reason,
        None,
    )
    assert (r_not_yet.status, r_not_yet.reason, r_not_yet.applies_from) == (
        "blocked",
        reason,
        (5, 5),
    )
    assert r_unscheduled.unblock_when == cf.GAP_BLOCK_UNBLOCK_WHEN
    assert r_not_yet.unblock_when == cf.GAP_BLOCK_UNBLOCK_WHEN


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


# --- satisfaction-claims-evaluated (DL-039 part 4) ---

SATISFY_TRUE_MODEL = """
package P {
  private import ScalarValues::*;
  part def Toaster {
    attribute cycleTime : Real = 100.0;
  }
  part fast : Toaster;
  requirement def TimelyToast {
    subject toaster : Toaster;
    require constraint { toaster.cycleTime <= 180.0 }
  }
  requirement timely : TimelyToast;
  assert satisfy timely by fast;
}
"""


def test_satisfaction_claims_evaluated_registered() -> None:
    check = next(c for c in cf.REGISTRY if c.id == "satisfaction-claims-evaluated")
    assert check.applies_from == (3, 1)  # DL-048
    assert check.run is cf.satisfaction_claims_evaluated


def test_satisfaction_claims_evaluated_false_control_is_a_finding(conn) -> None:
    check = next(c for c in cf.REGISTRY if c.id == "satisfaction-claims-evaluated")
    model = conn.load_from_content(check.negative_control, strict=False)
    assert model.ok
    findings = check.run(model)
    assert findings
    assert findings[0]["requirement"] == "P::timely"
    assert findings[0]["subject"] == "P::slow"
    assert findings[0]["result"] is False


def test_satisfaction_claims_evaluated_clean_model_has_no_findings(conn) -> None:
    model = conn.load_from_content(SATISFY_TRUE_MODEL, strict=False)
    assert model.ok
    assert cf.satisfaction_claims_evaluated(model) == []


def test_satisfaction_claims_evaluated_prove_negative_control(conn) -> None:
    check = next(c for c in cf.REGISTRY if c.id == "satisfaction-claims-evaluated")
    assert cf.prove_negative_control(check, conn) is True


def test_satisfaction_claims_evaluated_scheduled_reports_slow_claim_on_ch03(ch03) -> None:
    # DL-048: scheduled from (3, 1), and ch03 passes language conformance, so at its own
    # chapter the check runs for real. Chapter 3's re-derivation (PASS4-003, per
    # DL-039(4)/DL-049) states the `slow` claim as `assert not satisfy`, which correctly
    # holds (slow's fixed 200 s cycle time fails `timely`'s 180 s bound), so the check
    # reports `passed` with no findings: the one claim in the model evaluates as its own
    # negation states, not as a fault to report.
    r = cf.report(ch03, (3, 1))["project"][1]
    assert r.check_id == "satisfaction-claims-evaluated"
    assert r.status == "passed"
    assert r.findings == []

    from toaster.query import satisfy_relationships

    claims = satisfy_relationships(ch03)
    # TimelyToastTest's `verify timely;` is also a SatisfyRequirementUsage
    # (declaredKeyword "verify"), with no subject; it is not itself a claim about a
    # usage and the check skips it. The one claim with a subject is `slow`'s.
    with_subject = [c for c in claims if c["subject"]]
    assert len(with_subject) == 1
    assert with_subject[0]["subject"] == "ToasterDemo::slow"
    assert with_subject[0]["requirement"] == "ToasterDemo::timely"


def test_satisfaction_claims_evaluated_scheduled_reports_slow_claim_on_ch04(ch04) -> None:
    r = cf.report(ch04, (4, 1))["project"][1]
    assert r.check_id == "satisfaction-claims-evaluated"
    assert r.status == "failed"
    assert any(f["subject"] == "ToasterDemo::slow" for f in r.findings)


def test_satisfaction_claims_evaluated_stays_blocked_on_ch08_despite_stage_reached(
    ch08,
) -> None:
    # DL-048: ch05-ch08 carry the DL-039 language-tier violations, so the check stays blocked
    # there regardless of scheduling — reaching its stage does not run it past a language failure.
    r = cf.report(ch08, (8, 1))["project"][1]
    assert r.check_id == "satisfaction-claims-evaluated"
    assert r.status == "blocked"


def test_satisfaction_claims_evaluated_skips_verify_without_subject(ch08) -> None:
    # A `verify` relationship has no subject and is not itself a satisfy claim about one.
    findings = cf.satisfaction_claims_evaluated(ch08)
    assert all(f["subject"] for f in findings)


def test_satisfaction_claims_evaluated_error_is_a_finding(conn, monkeypatch) -> None:
    model = conn.load_from_content(SATISFY_TRUE_MODEL, strict=False)

    def boom(expr):
        raise RuntimeError("evaluation exploded")

    monkeypatch.setattr(model, "eval", boom)
    findings = cf.satisfaction_claims_evaluated(model)
    assert len(findings) == 1
    assert findings[0]["error"] == "evaluation exploded"


# --- F3: satisfaction_claims_evaluated must respect isNegated ---
# Reviewer's exact case: temp>=200 requirement, negated claim, temp=150 subject should NOT be a
# finding, temp=250 subject SHOULD be a finding.

NEGATED_SATISFY_SUBJECT_FAILS_CONSTRAINT = """
package P {
  private import ScalarValues::*;
  part def Toaster {
    attribute temp : Real = 150.0;
  }
  part subject1 : Toaster;
  requirement def HotEnough {
    subject t : Toaster;
    require constraint { t.temp >= 200.0 }
  }
  requirement req : HotEnough;
  assert not satisfy req by subject1;
}
"""

NEGATED_SATISFY_SUBJECT_MEETS_CONSTRAINT = """
package P {
  private import ScalarValues::*;
  part def Toaster {
    attribute temp : Real = 250.0;
  }
  part subject1 : Toaster;
  requirement def HotEnough {
    subject t : Toaster;
    require constraint { t.temp >= 200.0 }
  }
  requirement req : HotEnough;
  assert not satisfy req by subject1;
}
"""


def test_negated_satisfy_constraint_false_is_not_a_finding(conn) -> None:
    # subject temp=150 fails the >= 200 constraint, so `assert not satisfy` (isNegated=True) is
    # correctly NOT violated: the constraint really does not hold for this subject.
    model = conn.load_from_content(NEGATED_SATISFY_SUBJECT_FAILS_CONSTRAINT, strict=False)
    assert model.ok
    assert cf.satisfaction_claims_evaluated(model) == []


def test_negated_satisfy_constraint_true_is_a_finding(conn) -> None:
    # subject temp=250 meets the >= 200 constraint, so `assert not satisfy` (isNegated=True) IS
    # violated: the model claims this should not hold, but it does.
    model = conn.load_from_content(NEGATED_SATISFY_SUBJECT_MEETS_CONSTRAINT, strict=False)
    assert model.ok
    findings = cf.satisfaction_claims_evaluated(model)
    assert len(findings) == 1
    assert findings[0]["requirement"] == "P::req"
    assert findings[0]["subject"] == "P::subject1"
    assert findings[0]["result"] is True
    assert findings[0]["negated"] is True


def test_plain_satisfy_unaffected_by_isnegated_handling(conn) -> None:
    # A plain `assert satisfy` (isNegated absent/False) keeps the pre-existing logic: finding
    # when the expression evaluates False, none when it evaluates True.
    check = next(c for c in cf.REGISTRY if c.id == "satisfaction-claims-evaluated")
    false_model = conn.load_from_content(check.negative_control, strict=False)
    findings = cf.satisfaction_claims_evaluated(false_model)
    assert findings[0]["negated"] is False
    true_model = conn.load_from_content(SATISFY_TRUE_MODEL, strict=False)
    assert cf.satisfaction_claims_evaluated(true_model) == []


# --- open question 2: bare `satisfy R;` (implicit subject) is a distinguishable finding, not silently
# skipped; a `verify` relationship (also no subject) keeps being skipped, since it is not itself a claim
# about a subject ---

BARE_SATISFY_IMPLICIT_SUBJECT_MODEL = """
package P {
  private import ScalarValues::*;
  part def Toaster {
    attribute cycleTime : Real = 100.0;
  }
  requirement def TimelyToast {
    subject toaster : Toaster;
    require constraint { toaster.cycleTime <= 180.0 }
  }
  requirement timely : TimelyToast;
  part fast : Toaster {
    satisfy timely;
  }
}
"""

BARE_VERIFY_NO_SUBJECT_MODEL = """
package P {
  private import ScalarValues::*;
  part def Toaster {
    attribute cycleTime : Real = 100.0;
  }
  part fast : Toaster;
  requirement def TimelyToast {
    subject toaster : Toaster;
    require constraint { toaster.cycleTime <= 180.0 }
  }
  requirement timely : TimelyToast;
  verification def CheckTimely {
    subject toaster : Toaster;
    objective { verify timely; }
  }
  verification checkTimely : CheckTimely;
}
"""


def test_bare_satisfy_implicit_subject_is_a_distinguishable_finding(conn) -> None:
    model = conn.load_from_content(BARE_SATISFY_IMPLICIT_SUBJECT_MODEL, strict=False)
    assert model.ok
    findings = cf.satisfaction_claims_evaluated(model)
    assert len(findings) == 1
    assert findings[0]["requirement"] == "P::timely"
    assert findings[0]["subject"] is None
    assert findings[0]["status"] == cf.NOT_EVALUATED_NO_SUBJECT
    assert "result" not in findings[0]
    assert "error" not in findings[0]


def test_not_evaluated_no_subject_text() -> None:
    # Same pattern as test_gap_block_unblock_when_text: pin the literal text, not just
    # equality-to-constant (the earlier bare-satisfy test only compared against the constant
    # itself, which survives a mutation of the string).
    assert cf.NOT_EVALUATED_NO_SUBJECT == "not evaluated: no explicit subject"


def test_bare_verify_without_subject_is_skipped_not_crashed(conn) -> None:
    # ch08 has no `verify` relationship to exercise this branch (its docstring comment describes
    # a case the fixture doesn't actually contain), so this is a standalone model built for it.
    model = conn.load_from_content(BARE_VERIFY_NO_SUBJECT_MODEL, strict=False)
    assert model.ok
    assert cf.satisfaction_claims_evaluated(model) == []


def test_missing_requirement_reference_skipped_not_crashed(conn, monkeypatch) -> None:
    # A SatisfyRequirementUsage with a subject but no resolvable requirement reference: the
    # `if not requirement: continue` branch must skip it, not crash or produce a spurious
    # finding. A valid `satisfy` always carries a resolvable target in practice, so this is
    # constructed via monkeypatch, same style as test_satisfaction_claims_evaluated_error_is_a_finding.
    model = conn.load_from_content(SATISFY_TRUE_MODEL, strict=False)
    monkeypatch.setattr(
        cf.query,
        "satisfy_relationships",
        lambda model, index=None: [
            {"id": "P::fake", "requirement": None, "subject": "P::fast"}
        ],
    )
    assert cf.satisfaction_claims_evaluated(model) == []
