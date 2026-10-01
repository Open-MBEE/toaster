"""scripts/check_conformance.py: the CLI's exit-code logic, against CONSTRUCTED models.

Not the real chapter fixtures for most of this file (their behavior against
`satisfaction-claims-evaluated`, scheduled per DL-048, is covered directly in
tests/test_conformance.py's ch03/ch04/ch08 fixture tests). These tests monkeypatch
`toaster.conformance.REGISTRY` with small constructed checks to exercise the exit-code
branch that a "failed" status takes 1, and that "open"/"blocked"/"wont-do" (no "failed")
take 0, per the status semantics documented at the top of conformance.py.
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

from toaster import conformance

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "check_conformance.py"

MINIMAL_MODEL = "package P {\n  part def A;\n}\n"

# Loads ok=True but trips the always-on language-gap guard (GAP_RULES, DL-039): an
# allocate whose ends both resolve to Definitions. This is independent of REGISTRY, so it
# forces every non-wont-do project check to "blocked" regardless of what REGISTRY holds.
GAP_MODEL = """
package P {
  action def ApplyHeat;
  part def HeatingSystem;
  allocate ApplyHeat to HeatingSystem;
}
"""


def _load_script():
    """Import scripts/check_conformance.py as a module (it is a script, not a package)."""
    spec = importlib.util.spec_from_file_location("check_conformance_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def cc():
    return _load_script()


def _write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(content)
    return p


def test_exit_code_1_when_a_check_is_failed(tmp_path, monkeypatch, cc):
    """A constructed model with a "failed" check exits 1."""
    failing = conformance.ConformanceCheck(
        id="always-fails",
        description="test-only check that always fails",
        run=lambda model: [{"rule": "test", "element": "x", "message": "boom"}],
        applies_from=(0, 0),
        negative_control=MINIMAL_MODEL,
    )
    monkeypatch.setattr(conformance, "REGISTRY", [failing])
    model_path = _write(tmp_path, "ch99-cumulative.sysml", MINIMAL_MODEL)
    monkeypatch.setattr(
        sys, "argv", ["check_conformance.py", str(model_path), "--stage", "0,0"]
    )
    assert cc.main() == 1


def test_exit_code_0_for_open_blocked_and_wont_do_with_no_failed(tmp_path, monkeypatch, cc):
    """A run touching only open, blocked and wont-do statuses (no failed) exits 0.

    One model (ok, no language gap) makes the unscheduled check "open" and the wont-do
    check "wont-do"; the other (GAP_MODEL) makes every non-wont-do check "blocked" and
    the wont-do check still "wont-do" (wont-do is checked first in `evaluate`/`report`,
    regardless of language state). Passed together in one invocation, the three
    non-failing statuses named in the acceptance check are all exercised and no check is
    ever "failed".
    """
    open_check = conformance.ConformanceCheck(
        id="never-scheduled",
        description="test-only check left open (unscheduled)",
        run=lambda model: [],
        applies_from=None,
        negative_control=MINIMAL_MODEL,
    )
    wontdo_check = conformance.ConformanceCheck(
        id="dropped",
        description="test-only check dropped",
        run=lambda model: [],
        applies_from=(0, 0),
        negative_control=MINIMAL_MODEL,
        wont_do=conformance.WontDo("no longer needed", "test-only change"),
    )
    monkeypatch.setattr(conformance, "REGISTRY", [open_check, wontdo_check])

    clean_path = _write(tmp_path, "ch01-cumulative.sysml", MINIMAL_MODEL)
    gap_path = _write(tmp_path, "ch02-cumulative.sysml", GAP_MODEL)
    monkeypatch.setattr(
        sys,
        "argv",
        ["check_conformance.py", str(clean_path), str(gap_path), "--stage", "0,0"],
    )
    assert cc.main() == 0


def test_exit_code_0_when_a_check_passes(tmp_path, monkeypatch, capsys, cc):
    """A constructed model with a "passed" check (scheduled, run, found nothing) exits 0,
    not just because "failed" is absent but because "passed" itself is not a failure."""
    passing = conformance.ConformanceCheck(
        id="always-passes",
        description="test-only check that always passes",
        run=lambda model: [],
        applies_from=(0, 0),
        negative_control=MINIMAL_MODEL,
    )
    monkeypatch.setattr(conformance, "REGISTRY", [passing])
    model_path = _write(tmp_path, "ch99-cumulative.sysml", MINIMAL_MODEL)
    monkeypatch.setattr(
        sys,
        "argv",
        ["check_conformance.py", str(model_path), "--stage", "0,0", "--json"],
    )

    assert cc.main() == 0

    report = json.loads(capsys.readouterr().out)
    assert report[0]["project"][0]["id"] == "always-passes"
    assert report[0]["project"][0]["status"] == "passed"


def test_default_stage_is_chapter_from_filename_end_of_chapter(tmp_path, monkeypatch, cc):
    """With no --stage, the stage passed into conformance.report() is (N, END_OF_CHAPTER),
    N the chapter number parsed from the model's ``chNN`` filename prefix — a cumulative
    fixture already carries every section of chapter N, so the default must not understate
    that — asserted on the actual stage tuple used (not just on printed text)."""
    captured_stages = []
    original_report = conformance.report

    def spy_report(model, stage, registry=None):
        captured_stages.append(stage)
        return original_report(model, stage, registry)

    monkeypatch.setattr(conformance, "report", spy_report)
    model_path = _write(tmp_path, "ch05-cumulative.sysml", MINIMAL_MODEL)
    monkeypatch.setattr(sys, "argv", ["check_conformance.py", str(model_path)])

    cc.main()

    assert captured_stages == [(5, cc.END_OF_CHAPTER)]


def test_stage_flag_overrides_the_default(tmp_path, monkeypatch, cc):
    """--stage CH,SEC overrides the filename-derived default, for the stage tuple actually
    passed into conformance.report()."""
    captured_stages = []
    original_report = conformance.report

    def spy_report(model, stage, registry=None):
        captured_stages.append(stage)
        return original_report(model, stage, registry)

    monkeypatch.setattr(conformance, "report", spy_report)
    model_path = _write(tmp_path, "ch05-cumulative.sysml", MINIMAL_MODEL)
    monkeypatch.setattr(
        sys, "argv", ["check_conformance.py", str(model_path), "--stage", "2,3"]
    )

    cc.main()

    assert captured_stages == [(2, 3)]
