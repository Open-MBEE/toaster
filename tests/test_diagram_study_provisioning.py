# tests/test_diagram_study_provisioning.py
from scripts.diagram_study.provision_check import compare_pinned_versions, PINNED


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
