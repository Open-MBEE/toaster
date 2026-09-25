"""WP-1 diagram pipeline probe: Python-generated DOT from model queries.

opensysml v0.9.0 has no native render-form DOT. This test confirms the
alternative: model.query() → model_to_dot() → render_dot() → SVG.
"""

import subprocess
import tempfile
from pathlib import Path

import opensysml

from toaster.render import model_to_dot, render_dot


_SRC = """
package ToasterProbe {
    abstract part def ToastingSystem;
    part def HeatingSystem :> ToastingSystem;
    part def ControlSystem :> ToastingSystem;
    part def Toaster {
        part heater : HeatingSystem;
        part control : ControlSystem;
    }
}
"""


def test_model_to_dot_structure():
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_SRC, strict=False)
    assert model.ok

    dot = model_to_dot(model, title="ToasterProbe")

    assert "digraph" in dot
    assert "ToasterProbe::Toaster" in dot
    assert "ToasterProbe::HeatingSystem" in dot
    assert "diamond" in dot  # composition edge present
    conn.close()


def test_render_dot_produces_svg():
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_SRC, strict=False)
    assert model.ok

    dot_src = model_to_dot(model, title="ToasterProbe")
    conn.close()

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "probe.svg"
        render_dot(dot_src, out)
        assert out.exists(), "render_dot did not produce output file"
        content = out.read_text()
        assert "<svg" in content, "Output does not look like an SVG"
