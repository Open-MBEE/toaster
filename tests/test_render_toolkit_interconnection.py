"""src/toaster/render.py's render_toolkit_interconnection(): sysml-toolkit's real `viz` CLI
+ PlantUML, used specifically when port identity itself is the pedagogical point (Ch5's
conjugated port). This is a real external-tool pipeline (sysmlv2 binary, sysml.library, the
PlantUML jar, a working `java`), not a packaged dependency -- every test here is skipped, with
a clear reason, if any of the four is not resolvable by toaster.tools on the machine running it.
"""

import os
import subprocess
from pathlib import Path

import pytest

from toaster.render import ToolkitRenderError, render_toolkit_interconnection
from toaster.tools import (
    ToolNotFoundError,
    resolve_java,
    resolve_library,
    resolve_plantuml_jar,
    resolve_sysmlv2,
)

MODEL = Path("models/ch05-cumulative.sysml")

_PROVISION_HINT = "uv run python scripts/provision-tools.py"


def _skip_reason(exc: ToolNotFoundError) -> str:
    return str(exc) if _PROVISION_HINT in str(exc) else f"{exc}; provision with `{_PROVISION_HINT}`"


def _require_tools() -> bool:
    """TOASTER_REQUIRE_TOOLS=1 turns "tool missing, skip" into "tool missing, fail" (for CI)."""
    return os.environ.get("TOASTER_REQUIRE_TOOLS") == "1"


def _working_java() -> Path:
    """The resolved java, proven to run: a PATH `java` can be a macOS stub that resolves but fails."""
    java = resolve_java()
    try:
        proc = subprocess.run([str(java), "-version"], capture_output=True, text=True, timeout=15, check=False)
        failure = None if proc.returncode == 0 else f"exited {proc.returncode}"
    except (OSError, subprocess.TimeoutExpired) as exc:
        failure = str(exc)
    if failure:
        raise ToolNotFoundError(
            f"java at {str(java)!r} does not run (`java -version`: {failure}); "
            "set the JAVA environment variable to a working java"
        )
    return java


def _resolve_tools(resolvers, require=None):
    """Call each resolver; return (their results, None), or (None, the actionable skip reason).

    With `require` true (default: TOASTER_REQUIRE_TOOLS=1) an unresolved tool raises instead, so the
    module fails to collect and CI cannot go green on silent skips.
    """
    if require is None:
        require = _require_tools()
    try:
        return tuple(resolver() for resolver in resolvers), None
    except ToolNotFoundError as exc:
        reason = _skip_reason(exc)
        if require:
            raise ToolNotFoundError(
                f"{reason} (TOASTER_REQUIRE_TOOLS=1: a missing tool is a failure, not a skip)"
            ) from exc
        return None, reason


_TOOLS, _SKIP_REASON = _resolve_tools(
    (resolve_sysmlv2, resolve_library, resolve_plantuml_jar, _working_java)
)
BINARY, LIB, PLANTUML_JAR, JAVA = _TOOLS if _TOOLS else (None, None, None, None)

pytestmark = pytest.mark.skipif(_TOOLS is None, reason=_SKIP_REASON or "")


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
    # render_toolkit_interconnection() wraps each port's own label at " : " (a presentation-only
    # line break, see _apply_interconnection_layout_fixes()) to keep it clear of neighboring
    # box borders; undo that one cosmetic transform before asserting on content, so this check
    # depends on what the label says, not on how it happens to be line-wrapped today.
    content = puml.replace("\\n", " ")
    # The whole point of this upgrade over the in-house render_interconnection(): real port
    # names drawn as their own boxes, not folded into a single edge label. Asserting the full
    # declaration text (not a bare "durationIn" in puml) matters: "durationIn" is itself a
    # substring of "durationInterface", so a bare substring check would still pass even if
    # the port boxes vanished and only the interface-level edge label remained -- exactly the
    # regression this upgrade exists to catch.
    assert "durationIn : ~DurationPort" in content
    assert "durationOut : DurationPort" in content
    assert "durationInterface" in content  # the connector label is still present too


def test_puml_has_ortho_routing_to_keep_connector_off_box_labels(tmp_path):
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
    # Without this, PlantUML's default diagonal connector between the two ports cuts straight
    # through the nearer part's own <<part>> stereotype and title text (confirmed by rendering
    # and rasterizing the real output before this fix) -- a real presentation defect in a
    # figure that ships in the chapter, not merely a style preference.
    assert "skinparam linetype ortho" in puml


def test_missing_binary_raises_clear_error_not_raw_subprocess_traceback(tmp_path):
    out = tmp_path / "interconnection.svg"
    with pytest.raises(ToolkitRenderError, match="is not an executable file"):
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


def test_binary_as_a_directory_raises_clear_error_not_a_permission_error(tmp_path):
    # A directory (or an empty string) passes a bare Path.exists() check, which would then
    # surface as a raw PermissionError/NotADirectoryError from the subprocess call instead of
    # this function's own named error -- check against a real directory, not just a missing
    # path, so this regression is actually exercised.
    out = tmp_path / "interconnection.svg"
    with pytest.raises(ToolkitRenderError, match="is not an executable file"):
        render_toolkit_interconnection(
            MODEL,
            "ToasterDemo::Toaster",
            out,
            lib=LIB,
            binary=LIB,  # LIB is a real, existing directory, not a file
            plantuml_jar=PLANTUML_JAR,
            java=JAVA,
        )
    assert not out.exists()
