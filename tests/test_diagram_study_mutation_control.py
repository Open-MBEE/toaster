# tests/test_diagram_study_mutation_control.py
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "diagram_study" / "mutation_control.py"


def _load_script():
    """Import scripts/diagram_study/mutation_control.py as a module (it is a
    script, not a package). The module itself does `from scripts.diagram_study
    import harness`... svgs_differ, a package-relative import that only resolves
    if the repo root is on sys.path -- same precedent as
    run_real_fixture_study.py's test (see test_diagram_study_real_fixture_study.py)."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location("mutation_control_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_script = _load_script()
mutation_control_result = _script.mutation_control_result


def test_changed_svg_is_reported_as_a_catch():
    result = mutation_control_result("opensysml-dot", b"<svg>before-content-here</svg>", b"<svg>after-content-different</svg>")
    assert result["baseline_rendered"] is True
    assert result["svg_changed"] is True
    assert result["verdict"] == "reflects the mutation"


def test_unchanged_svg_is_reported_as_stale():
    same = b"<svg>identical-content</svg>"
    result = mutation_control_result("sysmld", same, same)
    assert result["baseline_rendered"] is True
    assert result["svg_changed"] is False
    assert result["verdict"] == "STALE: picture unchanged after a real model edit"


def test_empty_baseline_raises_instead_of_a_vacuous_pass():
    with pytest.raises(ValueError, match="baseline render is empty"):
        mutation_control_result("pilot", b"", b"<svg>after</svg>")
