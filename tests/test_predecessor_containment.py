"""scripts/check_construction.py: check_predecessor_containment, standalone (PASS2-010 Task B).

Runs the real committed fixtures (models/chNN-cumulative.sysml), not constructed
models, because this check's whole point is a real finding. The check compares
NAMED elements only (see `_named_elements` in check_construction.py); an UNNAMED
element (e.g. a `doc`) that changes or drops is a known, separate blind spot this
check does NOT catch (see DEFERRED.md D-022). ch06->ch07 is confirmed clean;
ch07->ch08 now opens the gap one chapter further down (see below).

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
  did; `ch04-cumulative.sysml` was not touched by PASS4-003 (a non-goal) and
  had been built against the old, stale ch03 fixture, so it dropped those same
  functional constructs too, in addition to the pre-existing `TimelyToastTest`
  wholesale drop PASS2-010 first recorded (`decisions/audits/ch04-layer-audit.md`
  F-5).
- PASS4-004 (Chapter 4's own re-derivation) closed ch03->ch04 the same way, by
  rebasing `ch04-cumulative.sysml` onto `ch03-cumulative.sysml`'s current
  content. ch03->ch04 is clean: every named element ch03-cumulative.sysml
  carries (`Bread`, `Toast`, `ToastBread` and its `bread`/`toast` parameters,
  `ToastingSystem::toastBread`, `TimelyToastTest` and its `toaster` subject,
  and everything else) is present in ch04-cumulative.sysml with the same
  `@type`. `ch05-cumulative.sysml` is not touched by PASS4-004 (a non-goal) and
  was built against the old, stale ch04 fixture (an unallocated `ApplyHeat`
  with `power`/`efficiency` parameters, a `DeliveredEnergy` invocation, and no
  `Bread`/`Toast`/`ToastBread`), so ch04->ch05 opened the same gap one chapter
  further down: expected and temporary, pending Chapter 5's own re-derivation,
  the same treatment ch03->ch04 received until PASS4-004 closed it.
- PASS4-005 (Chapter 5's own re-derivation) closed ch04->ch05 the same way, by
  rebasing `ch05-cumulative.sysml` onto `ch04-cumulative.sysml`'s current
  content. ch04->ch05 is clean: every named element ch04-cumulative.sysml
  carries is present in ch05-cumulative.sysml with the same `@type`.
  `ch06-cumulative.sysml` is not touched by PASS4-005 (a non-goal, `models/
  ch06-cumulative.sysml` belongs to whichever contract re-derives Chapter 6)
  and was built against the old, stale ch05 fixture (the invalid
  definition-level `allocate`, the ungrounded `BreadLoader`/`BreadEjector`/
  `BreadHandling`, and none of Chapter 4's or the new Chapter 5's functional
  and interface constructs), so ch05->ch06 opened the same gap one chapter
  further down: expected and temporary, pending Chapter 6's own re-derivation,
  the same treatment ch04->ch05 received until PASS4-005 closed it.
- PASS4-006 (Chapter 6's own re-derivation) closed ch05->ch06 the same way, by
  rebasing `ch06-cumulative.sysml` onto `ch05-cumulative.sysml`'s current
  content. ch05->ch06 is clean: every named element ch05-cumulative.sysml
  carries is present in ch06-cumulative.sysml with the same `@type`.
  `ch07-cumulative.sysml` is not touched by PASS4-006 (a non-goal) and was
  built against the old, stale ch06 fixture (`Heater`, `HeatingElement`,
  `PowerWire`, none of Chapter 5's port/interface constructs and none of
  Chapter 6's new function, logical carrier, allocation and physical
  realization for `GenerateHeat`), so ch06->ch07 now opens the same gap one
  chapter further down: expected and temporary, pending Chapter 7's own
  re-derivation, the same treatment ch05->ch06 received until PASS4-006
  closed it.
- PASS4-007 (Chapter 7's own re-derivation) closed ch06->ch07 the same way, by
  rebasing `ch07-cumulative.sysml` onto `ch06-cumulative.sysml`'s current
  content. ch06->ch07 is clean: every named element ch06-cumulative.sysml
  carries is present in ch07-cumulative.sysml with the same `@type`, plus
  Chapter 7's own new `deliveredEnergy`, `efficiency` and `efficiencyBounded`
  on `HeatGenerator`, `rated`'s own efficiency value, and `Cycle` rebuilt as a
  real `state def` that `ToastingSystem` exhibits, inherited and executable through `Toaster`. `ch08-cumulative.sysml` is not
  touched by PASS4-007 (a non-goal) and was built against the old, stale ch07
  fixture (`state Cycle` as an undifferentiated package-level usage with no
  owner, no `do` action and no return-to-idle transitions, and none of Chapter
  4's, 5's or 6's functional, interface, logical-carrier or allocation
  constructs), so ch07->ch08 opened the same gap one chapter further down:
  expected and temporary, pending Chapter 8's own re-derivation, the same
  treatment ch06->ch07 received until PASS4-007 closed it.
- PASS4-008 (Chapter 8's own re-derivation) closed ch07->ch08 the same way, by
  rebasing `ch08-cumulative.sysml` onto `ch07-cumulative.sysml`'s current
  content (its own file-header comment, "chapter 8's construct-introducing
  notebooks", was already true in name, false in fact, until this pass made it
  true: the fixture was previously a verbatim copy of ch07's content with only
  the comment's chapter number edited). ch07->ch08 is clean: every named
  element ch07-cumulative.sysml carries is present in ch08-cumulative.sysml
  with the same `@type`, plus Chapter 8's own new `heatGenCheck`,
  `heatGenCheckDuration` and `deliveredEnergyBoundedBySupply` on
  `ToasterDemo` (the conservation entailment `efficiencyBounded` and
  `deliveredEnergy` already imply, proved for every value of efficiency in its
  bound rather than evaluated at rated's one checked value).

- PASS4-009 (Chapter 9, Coverage and Sufficiency) added no
  `ch09-cumulative.sysml` at all: an analysis-only chapter over the real,
  current ch08 fixture (a deliberate design choice, see
  `decisions/pass4-run-009.md`), so `ch08->ch09` containment is a documented
  no-op rather than a real check (`test_ch08_to_ch09_predecessor_containment_
  is_a_noop_by_design` below), and `check_predecessor_containment(10, ...)`
  would have looked only at the missing ch09 fixture and no-opped too,
  silently, the exact gap `decisions/next-passes.md` item 21 named.
- PASS4-010 (Chapter 10, Traceability and Sign-off) resolved that gap for
  real rather than inheriting it: `check_predecessor_containment` now falls
  back to the nearest earlier chapter with a real cumulative fixture
  (`_nearest_predecessor_fixture`) when the immediate predecessor has none,
  and Chapter 10 commits its own `ch10-cumulative.sysml` (byte-identical in
  body to ch08's, since this chapter also adds no new named model element)
  specifically so that fallback has a real ch10 file to compare ch08's named
  elements against. `ch08->ch10` is clean: every named element
  ch08-cumulative.sysml carries is present in ch10-cumulative.sysml with the
  same `@type` (see `test_ch08_to_ch10_predecessor_containment_via_fallback_
  is_clean` below; the companion test `..._is_real_not_vacuous` is what proves
  the fallback is real, not vacuous, by showing it catches a genuine removal).

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


def test_ch07_to_ch08_is_clean(cc, conn):
    """PASS4-008 rebased ch08-cumulative.sysml onto ch07-cumulative.sysml's current
    content, closing ch07->ch08 the same way every prior chapter's own re-derivation
    closed the gap one chapter down: every named element ch07-cumulative.sysml
    carries (`Bread`, `Toast`, `ToastBread`, `TimelyToastTest`, `HeatingSystem`
    performing `ApplyHeat`, `heatAllocation`, the `DurationPort` interface,
    `GenerateHeat`, `EnergyPort`, `HeatGenerator` with its `deliveredEnergy`,
    `efficiency` and `efficiencyBounded`, `HeatingAssembly::heatGen`,
    `heatGenAllocation`, `HeatGenerationReq`/`heatGenerationReq`, `rated`, and
    `Cycle` as a real `state def` `ToastingSystem` exhibits) is present in
    ch08-cumulative.sysml with the same `@type`, plus Chapter 8's own new
    `heatGenCheck`, `heatGenCheckDuration` and `deliveredEnergyBoundedBySupply`."""
    failures = cc.check_predecessor_containment(8, conn)
    assert failures == []


@pytest.mark.parametrize("chapter", [2, 3, 4, 5, 6, 7, 8])
def test_other_adjacent_pairs_report_no_failures(cc, conn, chapter):
    """ch01->ch02 (clean since PASS4-002), ch02->ch03 (clean since PASS4-003, which
    rebased ch03-cumulative.sysml onto ch02-cumulative.sysml's current content),
    ch03->ch04 (clean since PASS4-004, which rebased ch04-cumulative.sysml onto
    ch03-cumulative.sysml's current content), ch04->ch05 (clean since PASS4-005,
    which rebased ch05-cumulative.sysml onto ch04-cumulative.sysml's current
    content), ch05->ch06 (clean since PASS4-006, which rebased
    ch06-cumulative.sysml onto ch05-cumulative.sysml's current content),
    ch06->ch07 (clean since PASS4-007, which rebased ch07-cumulative.sysml onto
    ch06-cumulative.sysml's current content), and ch07->ch08 (clean since
    PASS4-008, which rebased ch08-cumulative.sysml onto ch07-cumulative.sysml's
    current content; see test_ch07_to_ch08_is_clean for the detail) are each
    clean."""
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


def test_ch09_has_no_cumulative_fixture(cc):
    """PASS4-009 (Chapter 9, Coverage and Sufficiency) is deliberately built as an
    analysis chapter: its coverage, sufficiency and staleness notebooks query
    models/ch08-cumulative.sysml directly and add no new named model element (see
    chapters/ch09-coverage-sufficiency/index.md). Checked against the real
    filesystem directly, not just against CUMULATIVE_FILES (which could disagree
    with reality if the dict and the repo's own files ever drifted apart): no
    models/ch09-cumulative.sysml exists, and CUMULATIVE_FILES carries no chapter-9
    entry either, consistently."""
    ch09_path = cc.REPO_ROOT / "models" / "ch09-cumulative.sysml"
    assert not ch09_path.exists()
    assert 9 not in cc.CUMULATIVE_FILES


def test_ch08_to_ch09_predecessor_containment_is_a_noop_by_design(cc, conn, monkeypatch):
    """check_predecessor_containment(9, ...) returns no failures, but not because
    ch08->ch09 containment was genuinely checked and found clean: it is a no-op,
    guarded by the function's own early return when chapter 9's OWN cumulative
    fixture doesn't exist (CUMULATIVE_FILES has no entry for 9 at all -- see
    test_ch09_has_no_cumulative_fixture). That early return fires before the
    function ever calls _nearest_predecessor_fixture to look for a predecessor,
    let alone loads anything. Proved here, not just asserted: conn's own
    load_from_content is monkeypatched to raise, so if that early return were
    ever bypassed, this test would fail loudly instead of silently returning []
    for an unrelated reason. Documented separately from the real, checked
    "clean" results above so the two are never conflated."""

    def _must_not_be_called(*args, **kwargs):
        raise AssertionError(
            "check_predecessor_containment(9, ...) must never call "
            "load_from_content at all: chapter 9 has no cumulative fixture of "
            "its own, so the function's early return on its own cur_path check "
            "must fire before it ever looks for a predecessor, let alone loads "
            "either file."
        )

    monkeypatch.setattr(conn, "load_from_content", _must_not_be_called)
    assert cc.check_predecessor_containment(9, conn) == []


def test_ch10_has_a_cumulative_fixture(cc):
    """PASS4-010 (Chapter 10, Traceability and Sign-off), unlike Chapter 9, DOES commit
    its own models/ch10-cumulative.sysml, precisely so check_predecessor_containment's
    own nearest-earlier-fixture fallback has a real ch10 file to compare ch08's named
    elements against (decisions/next-passes.md item 21). Checked against the real
    filesystem directly, matching test_ch09_has_no_cumulative_fixture's own method."""
    ch10_path = cc.REPO_ROOT / "models" / "ch10-cumulative.sysml"
    assert ch10_path.exists()
    assert cc.CUMULATIVE_FILES.get(10) == ch10_path


def test_nearest_predecessor_fixture_skips_ch09_and_finds_ch08(cc):
    """_nearest_predecessor_fixture(10) must walk past chapter 9 (no fixture) and land on
    chapter 8 (a real one), not merely return something. Checked directly against the
    real, unmodified CUMULATIVE_FILES dict, not a constructed stand-in."""
    assert 9 not in cc.CUMULATIVE_FILES
    found = cc._nearest_predecessor_fixture(10)
    assert found is not None
    chapter, path = found
    assert chapter == 8
    assert path == cc.CUMULATIVE_FILES[8]


def test_nearest_predecessor_fixture_general_fallback_skips_a_gap(cc, tmp_path, monkeypatch):
    """The fallback is general, not special-cased to chapter 9, and skips BOTH real ways a
    gap can occur, walking through both before landing on a real fixture: chapter 97, a key
    genuinely absent from CUMULATIVE_FILES (confirmed with `not in`, not merely assumed),
    and chapter 96, a key that IS present but whose file does not exist on disk (a stale
    dict entry). Only chapter 95, with a real, existing file, is returned."""
    assert 97 not in cc.CUMULATIVE_FILES
    stale_96 = tmp_path / "ch96-does-not-exist.sysml"
    assert not stale_96.exists()
    fixture_95 = tmp_path / "ch95.sysml"
    fixture_95.write_text("package Test95 {\n}\n")
    monkeypatch.setitem(cc.CUMULATIVE_FILES, 96, stale_96)
    monkeypatch.setitem(cc.CUMULATIVE_FILES, 95, fixture_95)

    found = cc._nearest_predecessor_fixture(98)

    assert found == (95, fixture_95)


def test_ch08_to_ch10_predecessor_containment_via_fallback_is_clean(cc, conn):
    """check_predecessor_containment(10, ...) falls back past the missing ch09 fixture to
    the real ch08 one (test_nearest_predecessor_fixture_skips_ch09_and_finds_ch08), and
    that real ch08->ch10 comparison is clean: ch10-cumulative.sysml carries every named
    element ch08-cumulative.sysml does, with the same @type, since this chapter's own
    fixture is byte-identical in body to ch08's (see that file's own header comment) and
    adds no new named model element, the same design choice Chapter 9 made."""
    failures = cc.check_predecessor_containment(10, conn)
    assert failures == []


def test_ch08_to_ch10_predecessor_containment_via_fallback_is_real_not_vacuous(cc, conn, tmp_path):
    """The clean result above is not another silent no-op: point CUMULATIVE_FILES[10] at a
    scratch copy of the real ch10 fixture with one real named element (rated, and its own
    satisfy claim) removed, and confirm the fallback check catches it, naming ch08 (not
    ch09) as the predecessor it compared against. The real CUMULATIVE_FILES dict is
    restored afterward without monkeypatch, since this test edits it directly to avoid
    monkeypatch's fixture-scope subtleties around a plain dict item already present."""
    real_ch10_path = cc.CUMULATIVE_FILES[10]
    original_source = real_ch10_path.read_text()
    assert "assert satisfy heatGenerationReq by rated;" in original_source

    truncated = original_source.replace(
        "    part rated : ResistanceCoil {\n"
        "        attribute :>> efficiency = 0.7;\n"
        "        assert satisfy heatGenerationReq by rated;\n"
        "    }\n",
        "",
    )
    assert truncated != original_source, "Expected the replacement to remove `rated`"

    scratch_path = tmp_path / "ch10-scratch.sysml"
    scratch_path.write_text(truncated)
    cc.CUMULATIVE_FILES[10] = scratch_path
    try:
        failures = cc.check_predecessor_containment(10, conn)
    finally:
        cc.CUMULATIVE_FILES[10] = real_ch10_path

    assert len(failures) == 1
    assert "ch08-cumulative.sysml -> ch10-cumulative.sysml" in failures[0]
    assert "ToasterDemo::rated" in failures[0]
    assert "missing from ch10-cumulative.sysml" in failures[0]


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
