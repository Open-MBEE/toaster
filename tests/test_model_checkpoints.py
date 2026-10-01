"""
Checkpoint tests: verify that construction cells are consistent with committed fixtures.

Skipped by default (addopts = -m 'not checkpoint' in pyproject.toml).
Run explicitly in CI: pytest -m checkpoint
"""
import subprocess
import sys
import pytest


@pytest.mark.checkpoint
def test_construction_consistency_all():
    """Run check_construction.py --check across all chapters."""
    result = subprocess.run(
        [sys.executable, "scripts/check_construction.py", "--check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Construction inconsistency detected:\n{result.stdout}\n{result.stderr}"
    )


@pytest.mark.checkpoint
@pytest.mark.parametrize("chapter", [1, 2, 3, 4, 5, 7])
def test_construction_consistency_chapter(chapter):
    """Run check_construction.py --check for one chapter."""
    result = subprocess.run(
        [sys.executable, "scripts/check_construction.py", "--check", f"--chapter={chapter}"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Ch{chapter} construction inconsistency:\n{result.stdout}\n{result.stderr}"
    )
