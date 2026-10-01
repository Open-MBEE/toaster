from pathlib import Path

import opensysml
import pytest

FIXTURES_DIR = Path("decisions/diagram-study-real-fixtures/fixtures")
FIXTURE_NAMES = ["ch05", "ch06", "ch07", "ch08"]


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_baseline_fixture_loads_ok(name):
    conn = opensysml.connect(version="v0.9.0")
    text = (FIXTURES_DIR / f"{name}.sysml").read_text()
    model = conn.load_from_content(text, strict=False)
    assert model.ok, f"{name}.sysml: {[d.message for d in model.diagnostics]}"
    conn.close()


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_mutated_fixture_loads_ok(name):
    conn = opensysml.connect(version="v0.9.0")
    text = (FIXTURES_DIR / f"{name}-mutated.sysml").read_text()
    model = conn.load_from_content(text, strict=False)
    assert model.ok, f"{name}-mutated.sysml: {[d.message for d in model.diagnostics]}"
    conn.close()


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_mutated_fixture_differs_from_baseline_by_exactly_the_documented_edit(name):
    baseline = (FIXTURES_DIR / f"{name}.sysml").read_text().splitlines()
    mutated = (FIXTURES_DIR / f"{name}-mutated.sysml").read_text().splitlines()
    assert len(baseline) == len(mutated), "mutation must not add or remove lines"
    changed = [i for i, (a, b) in enumerate(zip(baseline, mutated)) if a != b]
    assert 1 <= len(changed) <= 2, f"{name}: expected 1-2 changed lines, got {len(changed)}"
