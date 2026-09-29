"""WP-1 diagram pipeline probe: Python-generated DOT from model queries.

opensysml v0.9.0 has no native render-form DOT. This test confirms the
alternative: model.query() → model_to_dot() → render_dot() → SVG.
"""

import subprocess
import tempfile
from pathlib import Path

import opensysml

from toaster.render import containment_subgraph, model_to_dot, render_dot

REPO_ROOT = Path(__file__).parent.parent


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


def test_model_to_dot_default_behavior_unchanged():
    """elements=None, layout=None must produce byte-for-byte the same output
    as before this plan -- the existing, unmodified test above already pins
    the shape of this output; this test pins that passing the new parameters'
    default values changes nothing."""
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_SRC, strict=False)
    assert model.ok
    without_new_params = model_to_dot(model, title="ToasterProbe")
    with_defaults_explicit = model_to_dot(
        model, title="ToasterProbe", elements=None, layout=None
    )
    assert without_new_params == with_defaults_explicit
    conn.close()


def test_model_to_dot_elements_scopes_the_output():
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_SRC, strict=False)
    assert model.ok
    scoped = containment_subgraph(model, "ToasterProbe::Toaster", depth=1)
    dot = model_to_dot(model, title="ToasterProbe", elements=scoped)
    assert "ToasterProbe::Toaster" in dot
    conn.close()


def test_model_to_dot_empty_elements_list_is_a_valid_empty_diagram():
    """elements=[] means 'nothing in scope' -- a real, different outcome from
    elements=None ('everything'), not an error and not silently the same
    as the default."""
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_SRC, strict=False)
    assert model.ok
    dot = model_to_dot(model, title="Empty", elements=[])
    assert "digraph" in dot
    assert "ToasterProbe::Toaster" not in dot
    conn.close()


def test_model_to_dot_excludes_unreachable_elements_on_real_ch08_fixture():
    """The real problem this plan exists to fix: on Ch8's real, larger model,
    scoping to Toaster's own containment excludes the unrelated test-fixture
    islands (nominal, slow, rated, weak, heatGenCheck, TimelyToast) that made
    the unscoped diagram unreadably wide."""
    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch08-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok
    scoped = containment_subgraph(model, "ToasterDemo::Toaster", depth=2)
    dot = model_to_dot(model, title="Ch8 scoped", elements=scoped)
    assert "ToasterDemo::Toaster::heating" in dot
    for excluded in ("ToasterDemo::nominal", "ToasterDemo::slow", "ToasterDemo::rated",
                     "ToasterDemo::weak", "ToasterDemo::heatGenCheck"):
        assert excluded not in dot
    conn.close()


def test_model_to_dot_layout_rankdir_override():
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_SRC, strict=False)
    assert model.ok
    default_dot = model_to_dot(model, title="ToasterProbe")
    lr_dot = model_to_dot(model, title="ToasterProbe", layout={"rankdir": "LR"})
    assert "rankdir=TB" in default_dot
    assert "rankdir=LR" in lr_dot
    assert "rankdir=TB" not in lr_dot
    conn.close()
