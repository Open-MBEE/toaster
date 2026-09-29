# tests/test_diagram_study_real_fixture_study.py
import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "diagram_study" / "run_real_fixture_study.py"


def _load_script():
    """Import scripts/diagram_study/run_real_fixture_study.py as a module (it is a
    script, not a package). The module itself does `from scripts.diagram_study import
    harness`, a package-relative import that only resolves if the repo root is on
    sys.path -- unlike Task 1/2's modules, which have no internal scripts.* imports,
    so ensure ROOT is present before exec_module runs it."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location("run_real_fixture_study_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_script = _load_script()
FIXTURE_TABLE = _script.FIXTURE_TABLE
render_fixture = _script.render_fixture


def test_fixture_table_covers_ch05_ch06_ch07_ch08():
    fixtures_covered = {row[0] for row in FIXTURE_TABLE}
    assert fixtures_covered == {"ch05", "ch06", "ch07", "ch08"}


def test_fixture_table_targets_the_untested_feature_per_fixture():
    views_by_fixture = {}
    for fixture, view, _element in FIXTURE_TABLE:
        views_by_fixture.setdefault(fixture, set()).add(view)
    assert "interconnection" in views_by_fixture["ch05"]
    assert "state" in views_by_fixture["ch07"]
    assert "tree" in views_by_fixture["ch06"]
    assert "tree" in views_by_fixture["ch08"]


def test_render_fixture_records_exit_code_and_hash_per_tool(tmp_path):
    fake_svg = tmp_path / "out.svg"
    fake_svg.write_bytes(b"<svg>ok</svg>")
    with patch.object(
        _script,
        "_render_one_tool",
        return_value={"exit_code": 0, "svg_path": str(fake_svg), "sha256": "abc"},
    ):
        result = render_fixture(
            "ch05", "tree", "ToasterDemo::Toaster",
            tools={"opensysml": "x", "toolkit": "y", "java": "z", "pilot_jar": "p",
                   "pilot_render_class": "c", "pilot_library": "l"},
            evidence_dir=tmp_path,
        )
    assert set(result.keys()) >= {"opensysml-puml", "opensysml-dot", "toolkit", "pilot"}
    for tool_result in result.values():
        assert "exit_code" in tool_result and "sha256" in tool_result


def test_missing_binary_is_caught_and_recorded_not_raised(tmp_path):
    """Review Focus item 1 / CORRECTIONS item 3: a FileNotFoundError from a missing
    tool binary must be captured as a result dict, not propagate and crash the run."""
    with patch.object(
        _script.harness,
        "run_and_log",
        side_effect=FileNotFoundError("no such file: /path/does/not/exist"),
    ):
        result = _script._render_one_tool(
            "toolkit", "ch05", "tree", "ToasterDemo::Toaster",
            Path("decisions/diagram-study-real-fixtures/fixtures/ch05.sysml"),
            tools={"toolkit": "/path/does/not/exist"},
            evidence_dir=tmp_path,
        )
    assert result["exit_code"] is None
    assert "error" in result
    assert "FileNotFoundError" in result["error"]
    exception_logs = list(tmp_path.glob("*-exception.log"))
    assert len(exception_logs) == 1
    assert "FileNotFoundError" in exception_logs[0].read_text()


def test_timeout_is_caught_and_recorded_not_raised(tmp_path):
    """Same guarantee for a hung process (subprocess.TimeoutExpired)."""
    import subprocess

    with patch.object(
        _script.harness,
        "run_and_log",
        side_effect=subprocess.TimeoutExpired(cmd=["toolkit"], timeout=120),
    ):
        result = _script._render_one_tool(
            "toolkit", "ch05", "tree", "ToasterDemo::Toaster",
            Path("decisions/diagram-study-real-fixtures/fixtures/ch05.sysml"),
            tools={"toolkit": "/path/to/sysmlv2"},
            evidence_dir=tmp_path,
        )
    assert result["exit_code"] is None
    assert "error" in result
    assert "TimeoutExpired" in result["error"]
    exception_logs = list(tmp_path.glob("*-exception.log"))
    assert len(exception_logs) == 1


def test_happy_path_unaffected_by_exception_handling(tmp_path):
    """The try/except wrapping must not change happy-path behavior at all."""
    import subprocess as sp
    from unittest.mock import MagicMock

    completed = MagicMock(spec=sp.CompletedProcess)
    completed.returncode = 0
    # PlantUML writes {stem}.svg next to {stem}.puml -- the render call is mocked,
    # so create the .svg output it would have produced, at the path _render_one_tool
    # expects for an intermediate-form tool ("toolkit" -> plantuml -> .svg).
    fake_svg = tmp_path / "ch05-tree-toolkit.svg"
    fake_svg.write_bytes(b"<fake>content</fake>")

    with patch.object(_script.harness, "run_and_log", return_value=completed):
        result = _script._render_one_tool(
            "toolkit", "ch05", "tree", "ToasterDemo::Toaster",
            Path("decisions/diagram-study-real-fixtures/fixtures/ch05.sysml"),
            tools={"toolkit": "/path/to/sysmlv2", "java": "/path/to/java", "plantuml_jar": "/path/to/plantuml.jar"},
            evidence_dir=tmp_path,
        )
    assert result["exit_code"] == 0
    assert result["sha256"] is not None
    assert "error" not in result
