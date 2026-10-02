"""Tests for render_action_flow() and render_state_flow() (Phase 2 Task 1)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from toaster.bootstrap import ensure_cli_binary
from toaster.render import render_action_flow, render_state_flow

REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="module")
def cli_binary():
    return ensure_cli_binary(version="v0.9.0")


@pytest.fixture(scope="module")
def ch06_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch06-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok, f"Ch6 fixture failed to load: {model.diagnostics}"
    yield model
    conn.close()


@pytest.fixture(scope="module")
def ch07_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch07-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok, f"Ch7 fixture failed to load: {model.diagnostics}"
    yield model
    conn.close()


def test_render_action_flow_produces_real_svg(ch06_model, cli_binary, tmp_path):
    out = tmp_path / "apply_heat.svg"
    render_action_flow(ch06_model, "ToasterDemo::ApplyHeat", out, binary=cli_binary)
    assert out.exists()
    svg = out.read_text()
    assert "<svg" in svg
    assert "generateHeat" in svg


def test_render_state_flow_produces_real_svg_with_trigger_labels(ch07_model, cli_binary, tmp_path):
    out = tmp_path / "cycle.svg"
    render_state_flow(ch07_model, "ToasterDemo::Cycle", out, binary=cli_binary)
    assert out.exists()
    svg = out.read_text()
    assert "<svg" in svg
    assert "heating" in svg
    assert "accept Start" in svg


def test_render_action_flow_renders_what_the_model_object_holds_not_the_committed_file(
    tmp_path, cli_binary
):
    """The function must serialize the IN-MEMORY model (model.to_sysml()), not
    silently re-read models/ch06-cumulative.sysml from disk -- proven by loading
    a small synthetic model that doesn't exist as a committed file at all."""
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    src = """
    package SynthTest {
        action def Outer {
            first start;
            then action inner : Inner;
            then done;
        }
        action def Inner;
    }
    """
    model = conn.load_from_content(src, strict=False)
    assert model.ok
    out = tmp_path / "outer.svg"
    render_action_flow(model, "SynthTest::Outer", out, binary=cli_binary)
    assert out.exists()
    assert "inner" in out.read_text()
    conn.close()


def test_render_action_flow_missing_binary_raises_clear_error(ch06_model, tmp_path):
    with pytest.raises(FileNotFoundError, match="sysml"):
        render_action_flow(
            ch06_model, "ToasterDemo::ApplyHeat", tmp_path / "x.svg",
            binary=tmp_path / "does-not-exist",
        )
