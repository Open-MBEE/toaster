# tests/test_diagram_study_provisioning.py
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "diagram_study" / "provision_check.py"


def _load_script():
    """Import scripts/diagram_study/provision_check.py as a module (it is a script, not a package)."""
    spec = importlib.util.spec_from_file_location("provision_check_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_provision_check = _load_script()
compare_pinned_versions = _provision_check.compare_pinned_versions
PINNED = _provision_check.PINNED


def test_matching_versions_report_no_mismatches():
    reported = dict(PINNED)
    assert compare_pinned_versions(reported, PINNED) == []


def test_mismatched_version_is_reported():
    reported = dict(PINNED)
    reported["sysml-toolkit"] = "deadbeef"
    mismatches = compare_pinned_versions(reported, PINNED)
    assert len(mismatches) == 1
    assert "sysml-toolkit" in mismatches[0]
    assert "deadbeef" in mismatches[0]
    assert PINNED["sysml-toolkit"] in mismatches[0]


def test_missing_tool_is_reported_as_a_mismatch():
    reported = {k: v for k, v in PINNED.items() if k != "pilot"}
    mismatches = compare_pinned_versions(reported, PINNED)
    assert any("pilot" in m and "not provisioned" in m for m in mismatches)
