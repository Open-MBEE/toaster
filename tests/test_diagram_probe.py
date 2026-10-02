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


def test_model_to_dot_excludes_requirement_subject_on_real_ch02_fixture():
    """The real correctness bug this fix addresses: a requirement's declared
    `subject` (TimelyToast's `subject toaster : Toaster`) is internally a
    PartUsage owned by the RequirementDefinition, not real part composition.
    Unscoped model_to_dot() must not draw it, or TimelyToast at all, while
    still drawing the legitimate part-composition content of this fixture."""
    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch02-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok
    dot = model_to_dot(model, title="Ch2")
    conn.close()

    assert "TimelyToast" not in dot
    # Real node-declaration lines, not a bare substring check -- every
    # qualified name in this tutorial starts with "ToasterDemo::", so
    # asserting "Toaster" in dot would pass almost regardless of content.
    assert '"ToasterDemo::Toaster" [label="Toaster"];' in dot
    assert '"ToasterDemo::HeatingSystem" [label="HeatingSystem"];' in dot
    assert '"ToasterDemo::ControlSystem" [label="ControlSystem"];' in dot
    for present in ("nominal", "slow"):
        assert present in dot


def test_model_to_dot_excludes_verification_case_subject_on_real_ch03_fixture():
    """The same bug, via a different owner kind: Ch3 introduces
    `verification def TimelyToastTest { subject toaster : Toaster; ... }`.
    `subject` means the same reference-binding thing on a
    VerificationCaseDefinition as it does on a RequirementDefinition (both
    specialize the same KerML semantics), so the fix must skip this owner
    kind too. Confirmed directly: TimelyToastTest::toaster is a PartUsage
    owned by TimelyToastTest, whose own @type is VerificationCaseDefinition."""
    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch03-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok
    dot = model_to_dot(model, title="Ch3")
    conn.close()

    assert "TimelyToastTest" not in dot
    # Ch3's cumulative fixture carries forward Ch2's own requirement
    # (`requirement timely : TimelyToast;`), so this fixture exercises both
    # subject-bearing elements it contains -- not just the verification case.
    assert "TimelyToast" not in dot
    # Real, legitimate content this diagram should still show.
    assert '"ToasterDemo::Toaster" [label="Toaster"];' in dot
    assert '"ToasterDemo::HeatingSystem" [label="HeatingSystem"];' in dot
    assert '"ToasterDemo::ControlSystem" [label="ControlSystem"];' in dot
    for present in ("nominal", "slow"):
        assert present in dot


_COMPOSITION_SRC = """
package CompositionProbe {
    part def Outer {
        part inner : Inner;
    }
    part def Inner;
}
"""


def test_model_to_dot_real_composition_is_unaffected():
    """Negative control: a PartUsage owned by a genuine PartDefinition must
    still draw its composition diamond and typing dash -- the requirement-
    subject fix must not over-correct and suppress real composition."""
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_COMPOSITION_SRC, strict=False)
    assert model.ok

    dot = model_to_dot(model, title="CompositionProbe")
    conn.close()

    assert 'CompositionProbe::Outer" -> "CompositionProbe::Outer::inner"' in dot
    assert "arrowhead=diamond" in dot
    assert 'CompositionProbe::Outer::inner" -> "CompositionProbe::Inner"' in dot
    assert "arrowhead=open" in dot


def test_model_to_dot_draws_specialization_edge_on_real_ch08_fixture():
    """DEFECT 2 FIX: `part def ResistanceCoil :> HeatGenerator` in
    models/ch08-cumulative.sysml must be drawn as a real specialization edge,
    not left invisible. Styled distinctly from the typing edges also present
    in the same output (dashed line, open arrowhead): a solid line with a
    hollow/open triangle arrowhead (arrowhead=empty), asserted on the literal
    DOT line, not merely on both names appearing somewhere in the string."""
    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch08-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok
    dot = model_to_dot(model, title="Ch8")
    conn.close()

    assert (
        '"ToasterDemo::ResistanceCoil" -> "ToasterDemo::HeatGenerator" [arrowhead=empty];'
        in dot
    )
    # The existing typing edges to/from these same two elements must still be
    # present, and styled differently (dashed, open) from the specialization
    # edge above (solid, empty/hollow triangle) -- same two qualified names,
    # a different, distinguishable DOT line.
    assert (
        '"ToasterDemo::HeatingAssembly::heatGen" -> "ToasterDemo::HeatGenerator" '
        "[style=dashed arrowhead=open];" in dot
    )
    assert (
        '"ToasterDemo::rated" -> "ToasterDemo::ResistanceCoil" '
        "[style=dashed arrowhead=open];" in dot
    )
    # The specialization edge's own line must not also carry the typing
    # edge's dashed style or open arrowhead.
    spec_line = (
        '  "ToasterDemo::ResistanceCoil" -> "ToasterDemo::HeatGenerator" '
        "[arrowhead=empty];"
    )
    assert spec_line in dot.splitlines()
    assert "style=dashed arrowhead=open" not in spec_line
    assert "arrowhead=diamond" not in spec_line


def test_model_to_dot_excludes_package_composition_on_real_ch02_fixture():
    """DEFECT 1 FIX: a PartUsage owned directly by a Package (`nominal`,
    `slow` in models/ch02-cumulative.sysml) is not real part composition --
    a Package does not compose anything. Unscoped model_to_dot() must not
    draw the false composition edge from "ToasterDemo" to "ToasterDemo::nominal"
    (or ::slow), while still drawing each usage's own typing edge so the node
    still appears, and still drawing the real, legitimate part composition
    elsewhere in this fixture."""
    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch02-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok
    dot = model_to_dot(model, title="Ch2")
    conn.close()

    assert '"ToasterDemo" -> "ToasterDemo::nominal" [label="nominal" arrowhead=diamond];' not in dot
    assert '"ToasterDemo" -> "ToasterDemo::slow" [label="slow" arrowhead=diamond];' not in dot
    assert "arrowhead=diamond" not in "\n".join(
        line for line in dot.splitlines() if "nominal" in line or "::slow" in line
    )
    # The usages still appear, via their own typing edge to Toaster.
    assert '"ToasterDemo::nominal" -> "ToasterDemo::Toaster" [style=dashed arrowhead=open];' in dot
    assert '"ToasterDemo::slow" -> "ToasterDemo::Toaster" [style=dashed arrowhead=open];' in dot
    # Real, legitimate composition elsewhere in this fixture is unaffected:
    # Toaster really does compose heating/control PartUsages owned by the
    # PartDefinition Toaster, not by the package.
    assert "arrowhead=diamond" in dot


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
