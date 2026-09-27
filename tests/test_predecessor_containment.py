"""scripts/check_construction.py: check_predecessor_containment, standalone (PASS2-010 Task B).

Runs the real committed fixtures (models/chNN-cumulative.sysml), not constructed models,
because this check's whole point is a real finding: the pre-existing, undesired drop of the
entire `TimelyToastTest` verification def (a NAMED element, including its `toaster` subject
reference) between ch03 and ch04 (decisions/audits/ch04-layer-audit.md F-5). The check
compares NAMED elements only (see `_named_elements` in check_construction.py); the same
audit's drop of `TimelyToast`'s doc/rationale is an UNNAMED element and is a known, separate
blind spot this check does NOT catch (see DEFERRED.md D-022). This is expected and desired
output, not a bug (see DEFERRED.md and PASS2-010's Task B non-goals: the fixture is not
touched here). The other adjacent pairs listed in the contract's acceptance check 4
(ch02->ch03, ch04->ch05, ch05->ch06, ch06->ch07, ch07->ch08) are confirmed clean.

ch01->ch02 is a second known, real gap, of the same shape as ch03->ch04 above: PASS4-001
re-derived Chapter 1 (item def Bread/Toast, action def ToastBread, and ToastingSystem's
perform) ahead of Chapter 2, so ch02-cumulative.sysml (not yet re-derived) does not carry
those named elements forward. Expected and temporary, pending Chapter 2's own re-derivation;
not touched here, same as ch03->ch04.

The constructed-pair tests below (type-change, unnamed-element, and check_chapter wiring)
point `CUMULATIVE_FILES` at small standalone SysML strings under `tmp_path`, isolated from
the real committed fixtures above, using sentinel chapter numbers (91/92) that are not keys
in the real `CUMULATIVE_FILES`/`CONSTRUCTION_NOTEBOOKS` dicts.
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
    """The known, pre-existing, real failure (F-5): ch04 drops TimelyToastTest wholesale."""
    failures = cc.check_predecessor_containment(4, conn)
    assert failures, "expected the predecessor-containment check to catch ch04 dropping ch03 elements"
    joined = "\n".join(failures)
    assert "ToasterDemo::TimelyToastTest" in joined
    assert "ch03-cumulative.sysml" in joined and "ch04-cumulative.sysml" in joined
    # Every reported failure is a *missing* element (nothing changed @type here).
    assert all("is missing from" in f for f in failures)


def test_ch01_to_ch02_reports_the_known_dropped_elements(cc, conn):
    """The known, real, PASS4-001 gap: ch02 does not yet carry forward the functional
    construct Ch1 was re-derived to add (item def Bread/Toast, action def ToastBread,
    and ToastingSystem's perform), because ch02-cumulative.sysml has not itself been
    re-derived yet. Same shape as ch03->ch04 above; expected to close when Chapter 2
    is re-derived, not fixed here."""
    failures = cc.check_predecessor_containment(2, conn)
    assert failures, "expected the predecessor-containment check to catch ch02 dropping ch01's new functional elements"
    joined = "\n".join(failures)
    for qname in (
        "ToasterDemo::Bread",
        "ToasterDemo::Toast",
        "ToasterDemo::ToastBread",
        "ToasterDemo::ToastBread::bread",
        "ToasterDemo::ToastBread::toast",
        "ToasterDemo::ToastingSystem::toastBread",
    ):
        assert qname in joined, f"expected {qname} to be reported missing"
    assert "ch01-cumulative.sysml" in joined and "ch02-cumulative.sysml" in joined
    # Every reported failure is a *missing* element (nothing changed @type here).
    assert all("is missing from" in f for f in failures)


@pytest.mark.parametrize("chapter", [3, 5, 6, 7, 8])
def test_other_adjacent_pairs_report_no_failures(cc, conn, chapter):
    """ch02->ch03, ch04->ch05, ch05->ch06, ch06->ch07, ch07->ch08 are each clean."""
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
