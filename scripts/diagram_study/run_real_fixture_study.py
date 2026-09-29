"""Phase 0 driver: renders the real Ch5/6/7/8 fixtures with the four
common-model tools (OpenSysML x2 render-forms, sysml-toolkit, OMG pilot),
at the view/element each fixture exists to test. SysMLD is handled
separately in Task 6 (its schema needs hand-authored intent, not a
model-path CLI argument)."""
import json
import subprocess
from pathlib import Path

from scripts.diagram_study import harness

FIXTURES_DIR = Path("decisions/diagram-study-real-fixtures/fixtures")
EVIDENCE_DIR = Path("decisions/diagram-study-real-fixtures/evidence")

FIXTURE_TABLE: list[tuple[str, str, str]] = [
    ("ch05", "tree", "ToasterDemo::Toaster"),
    ("ch05", "interconnection", "ToasterDemo::Toaster"),
    ("ch06", "tree", "ToasterDemo::Toaster"),
    ("ch07", "tree", "ToasterDemo::Toaster"),
    ("ch07", "state", "ToasterDemo::Cycle"),
    ("ch08", "tree", "ToasterDemo::Toaster"),
]

COMMON_TOOLS = ["opensysml-puml", "opensysml-dot", "toolkit", "pilot"]


def _record_exception(stem: str, step: str, evidence_dir: Path, exc: Exception) -> dict:
    """Records a tool-invocation exception (missing binary, timeout, etc.) as a
    real, recordable matrix finding rather than letting it propagate and abort
    the whole run (Review Focus item 1). Writes {stem}-{step}-exception.log and
    returns a result dict with exit_code: None and an "error" key describing
    what happened, distinguishable from a normal nonzero exit code."""
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / f"{stem}-{step}-exception.log").write_text(
        f"{type(exc).__name__}: {exc}\n"
    )
    return {
        "exit_code": None,
        "svg_path": None,
        "sha256": None,
        "error": f"{type(exc).__name__}: {exc}",
    }


def _render_one_tool(tool: str, fixture: str, view: str, element: str, model_path: Path, tools: dict, evidence_dir: Path) -> dict:
    stem = f"{fixture}-{view}-{tool}"
    is_intermediate_form = tool in ("opensysml-puml", "toolkit")
    source_ext = {"opensysml-puml": "puml", "opensysml-dot": "dot", "toolkit": "puml", "pilot": "svg"}[tool]
    source_path = evidence_dir / f"{stem}.{source_ext}"
    cmd = harness.build_render_command(tool, view, element, model_path, source_path, tools)
    try:
        emit = harness.run_and_log(f"{stem}-emit", cmd, evidence_dir)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
        return _record_exception(stem, "emit", evidence_dir, exc)
    result = {"exit_code": emit.returncode, "svg_path": None, "sha256": None}
    if emit.returncode != 0:
        return result

    svg_path = evidence_dir / f"{stem}.svg"
    if tool == "opensysml-dot":
        try:
            render = harness.run_and_log(f"{stem}-render", ["dot", "-Tsvg", str(source_path), "-o", str(svg_path)], evidence_dir)
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
            return _record_exception(stem, "render", evidence_dir, exc)
        if render.returncode != 0:
            result["exit_code"] = render.returncode
            return result
    elif is_intermediate_form:
        try:
            render = harness.run_and_log(
                f"{stem}-render",
                [tools["java"], "-Djava.awt.headless=true", "-jar", tools["plantuml_jar"], "-tsvg", str(source_path)],
                evidence_dir,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
            return _record_exception(stem, "render", evidence_dir, exc)
        if render.returncode != 0:
            result["exit_code"] = render.returncode
            return result
        # PlantUML writes {stem}.svg next to {stem}.puml, i.e. exactly svg_path already.
    else:
        svg_path = source_path  # pilot writes SVG directly

    if svg_path.exists():
        data = svg_path.read_bytes()
        result["svg_path"] = str(svg_path)
        result["sha256"] = harness.hash_bytes(data)
    return result


def render_fixture(fixture: str, view: str, element: str, tools: dict, evidence_dir: Path) -> dict:
    model_path = FIXTURES_DIR / f"{fixture}.sysml"
    return {
        tool: _render_one_tool(tool, fixture, view, element, model_path, tools, evidence_dir)
        for tool in COMMON_TOOLS
    }


def main(tools: dict) -> dict:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for fixture, view, element in FIXTURE_TABLE:
        manifest[f"{fixture}-{view}"] = render_fixture(fixture, view, element, tools, EVIDENCE_DIR)
    (EVIDENCE_DIR / "real-fixture-results.json").write_text(json.dumps(manifest, indent=2))
    return manifest


if __name__ == "__main__":
    # tools dict must be filled in from Task 1's provisioning report before running for real
    raise SystemExit("run via a small wrapper that resolves `tools` from provisioning-report.json")
