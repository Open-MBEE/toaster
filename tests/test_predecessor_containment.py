"""scripts/check_construction.py: check_predecessor_containment, standalone (PASS2-010 Task B).

Runs the real committed fixtures (models/chNN-cumulative.sysml), not constructed models,
because this check's whole point is a real finding: the pre-existing, undesired drop of
`TimelyToast`'s doc/rationale and the entire `TimelyToastTest` verification def between
ch03 and ch04 (decisions/audits/ch04-layer-audit.md F-5). This is expected and desired
output, not a bug (see decisions/DEFERRED.md and PASS2-010's Task B non-goals: the fixture
is not touched here). The other adjacent pairs listed in the contract's acceptance check 4
(ch01->ch02, ch02->ch03, ch05->ch06, ch06->ch07, ch07->ch08) are confirmed clean.
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


@pytest.mark.parametrize("chapter", [2, 3, 6, 7, 8])
def test_other_adjacent_pairs_report_no_failures(cc, conn, chapter):
    """ch01->ch02, ch02->ch03, ch05->ch06, ch06->ch07, ch07->ch08 are each clean."""
    failures = cc.check_predecessor_containment(chapter, conn)
    assert failures == []


def test_chapter_1_has_no_predecessor_to_check(cc, conn):
    assert cc.check_predecessor_containment(1, conn) == []
