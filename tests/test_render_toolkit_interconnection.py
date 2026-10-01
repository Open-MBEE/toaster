"""src/toaster/render.py's render_toolkit_interconnection(): sysml-toolkit's real `viz` CLI
+ PlantUML, used specifically when port identity itself is the pedagogical point (Ch5's
conjugated port). This is a real external-tool pipeline (sysmlv2 binary, sysml.library, the
PlantUML jar, a working `java`), not a packaged dependency -- every test here is skipped, with
a clear reason, if any of the four real paths below is missing on the machine running it.
"""

from pathlib import Path

import pytest

from toaster.render import ToolkitRenderError, render_toolkit_interconnection

BINARY = Path.home() / "Documents/GitHub/sysml-toolkit/target/release/sysmlv2"
LIB = (
    Path.home()
    / "Documents/GitHub/sysml-toolkit/spec-refs/SysML-v2-Release/sysml.library"
)
PLANTUML_JAR = Path("/opt/homebrew/opt/plantuml/libexec/plantuml.jar")
JAVA = Path(
    "/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home/bin/java"
)

MODEL = Path("models/ch05-cumulative.sysml")

pytestmark = pytest.mark.skipif(
    not (BINARY.exists() and LIB.exists() and PLANTUML_JAR.exists() and JAVA.exists()),
    reason=(
        "sysml-toolkit binary, sysml.library, PlantUML jar or java not found at the real "
        f"paths this test requires (binary={BINARY}, lib={LIB}, plantuml_jar={PLANTUML_JAR}, "
        f"java={JAVA}); see work contract CH05-TOOLKIT-VIZ"
    ),
)


def test_renders_real_svg(tmp_path):
    out = tmp_path / "interconnection.svg"
    render_toolkit_interconnection(
        MODEL,
        "ToasterDemo::Toaster",
        out,
        lib=LIB,
        binary=BINARY,
        plantuml_jar=PLANTUML_JAR,
        java=JAVA,
    )
    assert out.exists()
    svg_bytes = out.read_bytes()
    assert len(svg_bytes) > 0
    assert svg_bytes.startswith(b"<?xml") or b"<svg" in svg_bytes[:200]


def test_puml_contains_real_port_names_not_just_interface_label(tmp_path):
    out = tmp_path / "interconnection.svg"
    render_toolkit_interconnection(
        MODEL,
        "ToasterDemo::Toaster",
        out,
        lib=LIB,
        binary=BINARY,
        plantuml_jar=PLANTUML_JAR,
        java=JAVA,
    )
    puml = out.with_suffix(".puml").read_text()
    # The whole point of this upgrade over the in-house render_interconnection(): real port
    # names drawn as their own boxes, not folded into a single edge label.
    assert "durationIn" in puml
    assert "durationOut" in puml
    assert "durationInterface" in puml  # the connector label is still present too


def test_missing_binary_raises_clear_error_not_raw_subprocess_traceback(tmp_path):
    out = tmp_path / "interconnection.svg"
    with pytest.raises(ToolkitRenderError, match="does not exist"):
        render_toolkit_interconnection(
            MODEL,
            "ToasterDemo::Toaster",
            out,
            lib=LIB,
            binary=Path("/nonexistent/sysmlv2"),
            plantuml_jar=PLANTUML_JAR,
            java=JAVA,
        )
    assert not out.exists()
