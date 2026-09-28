"""scripts/check_construction.py: check_predecessor_containment, standalone (PASS2-010 Task B).

Runs the real committed fixtures (models/chNN-cumulative.sysml), not constructed
models, because this check's whole point is a real finding. The check compares
NAMED elements only (see `_named_elements` in check_construction.py); an UNNAMED
element (e.g. a `doc`) that changes or drops is a known, separate blind spot this
check does NOT catch (see DEFERRED.md D-022). ch04->ch05, ch05->ch06, ch06->ch07
and ch07->ch08 are confirmed clean.

This gap moves rather than closes, one chapter at a time, as each chapter's own
re-derivation lands (a rhythm recorded starting with PASS4-002,
`decisions/pass4-run-002.md`):

- ch01->ch02 was a known gap opened by PASS4-001 (Chapter 1's re-derivation added
  `item def Bread`/`Toast`, `action def ToastBread`, and
  `ToastingSystem::toastBread` ahead of Chapter 2) and closed by PASS4-002
  (Chapter 2's own re-derivation, which rebased `ch02-cumulative.sysml` onto
  Chapter 1's new content). ch01->ch02 is clean.
- PASS4-002 opened the same gap one chapter further down, ch02->ch03:
  `ch02-cumulative.sysml` carried `Bread`/`Toast`/`ToastBread`/
  `ToastingSystem::toastBread` forward, but `ch03-cumulative.sysml` had not
  itself been re-derived yet.
- PASS4-003 (Chapter 3's own re-derivation) closed ch02->ch03 the same way, by
  rebasing `ch03-cumulative.sysml` onto `ch02-cumulative.sysml`'s current
  content (see `decisions/audits/ch03-layer-audit.md`). ch02->ch03 is clean.
  ch03-cumulative.sysml now carries forward the functional constructs Chapter
  2's own rebase added (`Bread`, `Toast`, `ToastBread` and
  `ToastingSystem::toastBread`), the same way `ch02-cumulative.sysml` already
  did; `ch04-cumulative.sysml` is not touched by PASS4-003 (a non-goal) and
  was built against the old, stale ch03 fixture, so it now drops those same
  functional constructs too, in addition to the pre-existing `TimelyToastTest`
  wholesale drop PASS2-010 first recorded (`decisions/audits/ch04-layer-audit.md`
  F-5). ch04-cumulative.sysml keeps its own `requirement timely : TimelyToast`
  and satisfy claims, so those are not part of this drop. Expected and
  temporary, pending Chapter 4's own re-derivation; not touched here, same
  treatment ch02->ch03 received until PASS4-003 closed it.

The constructed-pair tests below (type-change, unnamed-element, and
check_chapter wiring) point `CUMULATIVE_FILES` at small standalone SysML strings
under `tmp_path`, isolated from the real committed fixtures above, using
sentinel chapter numbers (91/92) that are not keys in the real
`CUMULATIVE_FILES`/`CONSTRUCTION_NOTEBOOKS` dicts.
"""
import importlib.util
from pathlib import Path

import opensysml
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "check_construction.py"


def _load_script():
    """Import scripts/check_construction.py as a module (it is a script, not a package)."""
    spec = importlib.util.spec_from_file_location("check_construction_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def cc():
    return _load_script()


@pytest.fixture(scope="module")
def conn():
    c = opensysml.connect(version="v0.9.0")
    yield c
    c.close()


def test_ch03_to_ch04_reports_the_known_dropped_elements(cc, conn):
    """PASS4-003 rebased ch03-cumulative.sysml onto ch02-cumulative.sysml's current
    content (closing ch02->ch03, see the test below), so ch03-cumulative.sysml now
    carries forward the functional constructs Chapter 2's own rebase added (`Bread`,
    `Toast`, `ToastBread`, `ToastingSystem::toastBread`). ch04-cumulative.sysml is
    not touched by PASS4-003 (a non-goal) and was built against the old, stale ch03
    fixture, so it drops those same functional constructs, plus TimelyToastTest, the
    pre-existing drop PASS2-010 first recorded (F-5). `timely` and the `slow`
    satisfaction claim are not part of this drop: ch04-cumulative.sysml already
    carries its own `requirement timely : TimelyToast` and satisfy claims (the
    assert itself is unnamed, so this NAMED-only check does not compare it)."""
    failures = cc.check_predecessor_containment(4, conn)
    assert failures, (
        "expected the predecessor-containment check to catch ch04 dropping ch03 elements"
    )
    joined = "\n".join(failures)
    for qname in (
        "ToasterDemo::Bread",
        "ToasterDemo::Toast",
        "ToasterDemo::ToastBread",
        "ToasterDemo::ToastBread::bread",
        "ToasterDemo::ToastBread::toast",
        "ToasterDemo::ToastingSystem::toastBread",
        "ToasterDemo::TimelyToastTest",
        "ToasterDemo::TimelyToastTest::toaster",
    ):
        assert qname in joined, f"expected {qname} to be reported missing"
    assert "ch03-cumulative.sysml" in joined and "ch04-cumulative.sysml" in joined
    # Every reported failure is a *missing* element (nothing changed @type here).
    assert all("is missing from" in f for f in failures)
    # timely is not part of the drop: ch04-cumulative.sysml already carries its own
    # requirement usage independently (the docstring's claim, pinned as a real assertion).
    assert "ToasterDemo::timely" not in joined


@pytest.mark.parametrize("chapter", [2, 3, 5, 6, 7, 8])
def test_other_adjacent_pairs_report_no_failures(cc, conn, chapter):
    """ch01->ch02 (clean since PASS4-002), ch02->ch03 (clean since PASS4-003, which
    rebased ch03-cumulative.sysml onto ch02-cumulative.sysml's current content),
    ch04->ch05, ch05->ch06, ch06->ch07 and ch07->ch08 are each clean."""
    failures = cc.check_predecessor_containment(chapter, conn)
    assert failures == []


def test_chapter_1_has_no_predecessor_to_check(cc, conn):
    assert cc.check_predecessor_containment(1, conn) == []


def test_type_change_is_flagged_with_both_types(cc, conn, tmp_path, monkeypatch):
    """A named element whose @type CHANGES between chapters (not merely dropped) is
    flagged, and the message names both types (contract: "same qualified name and same
    @type"). Constructed pair, isolated from the real fixtures via sentinel chapters."""
    prev_path = tmp_path / "prev.sysml"
    cur_path = tmp_path / "cur.sysml"
    prev_path.write_text("package Test {\n    part def Widget;\n}\n")
    cur_path.write_text("package Test {\n    item def Widget;\n}\n")
    monkeypatch.setitem(cc.CUMULATIVE_FILES, 91, prev_path)
    monkeypatch.setitem(cc.CUMULATIVE_FILES, 92, cur_path)

    failures = cc.check_predecessor_containment(92, conn)

    assert len(failures) == 1
    msg = failures[0]
    assert "Test::Widget" in msg
    assert "PartDefinition" in msg
    assert "ItemDefinition" in msg
    assert "changed @type" in msg


def test_unnamed_element_change_is_not_flagged(cc, conn, tmp_path, monkeypatch):
    """An UNNAMED element (e.g. a `doc`) that changes or disappears between chapters is
    NOT flagged: only named elements are compared (see `_named_elements`). Constructed
    pair: `Widget` keeps its name and @type across chapters; only its unnamed doc drops."""
    prev_path = tmp_path / "prev.sysml"
    cur_path = tmp_path / "cur.sysml"
    prev_path.write_text(
        "package Test {\n    part def Widget {\n        doc /* hello */\n    }\n}\n"
    )
    cur_path.write_text("package Test {\n    part def Widget;\n}\n")
    monkeypatch.setitem(cc.CUMULATIVE_FILES, 91, prev_path)
    monkeypatch.setitem(cc.CUMULATIVE_FILES, 92, cur_path)

    failures = cc.check_predecessor_containment(92, conn)

    assert failures == []


def test_check_chapter_surfaces_predecessor_containment_failures(cc, conn, tmp_path, monkeypatch):
    """check_chapter (the wired entry point, not the standalone function) surfaces the
    predecessor-containment check's failures in its own returned failure list."""
    prev_path = tmp_path / "prev.sysml"
    cur_path = tmp_path / "cur.sysml"
    prev_path.write_text("package Test {\n    part def Widget;\n}\n")
    cur_path.write_text("package Test {\n}\n")
    monkeypatch.setitem(cc.CUMULATIVE_FILES, 91, prev_path)
    monkeypatch.setitem(cc.CUMULATIVE_FILES, 92, cur_path)

    failures = cc.check_chapter(92, conn)

    assert any(
        "PREDECESSOR CONTAINMENT" in f and "Test::Widget" in f for f in failures
    )
