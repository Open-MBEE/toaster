# tests/test_diagram_study_harness.py
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "diagram_study" / "harness.py"


def _load_script():
    """Import scripts/diagram_study/harness.py as a module (it is a script, not a package)."""
    spec = importlib.util.spec_from_file_location("harness_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_harness = _load_script()
build_render_command = _harness.build_render_command
hash_bytes = _harness.hash_bytes
svgs_differ = _harness.svgs_differ


TOOLS = {
    "opensysml": "/path/to/opensysml-current",
    "toolkit": "/path/to/sysmlv2",
}


def test_opensysml_dot_command_shape():
    cmd = build_render_command(
        "opensysml-dot", "tree", "ToasterDemo::Toaster",
        Path("fixtures/ch06.sysml"), Path("evidence/ch06-tree.dot"), TOOLS,
    )
    assert cmd[0] == TOOLS["opensysml"]
    assert "fixtures/ch06.sysml" in cmd
    assert "-render" in cmd
    assert "#tree:ToasterDemo::Toaster" in cmd
    assert "-render-form" in cmd and "dot" in cmd
    assert cmd[-1] == "evidence/ch06-tree.dot"


def test_toolkit_command_shape():
    cmd = build_render_command(
        "toolkit", "interconnection", "ToasterDemo::Toaster",
        Path("fixtures/ch05.sysml"), Path("evidence/ch05-interconnection.puml"), TOOLS,
    )
    assert cmd[0] == TOOLS["toolkit"]
    assert cmd[1] == "viz"
    assert "fixtures/ch05.sysml" in cmd
    assert "--view" in cmd and "interconnection" in cmd
    assert "--element" in cmd and "ToasterDemo::Toaster" in cmd
    assert "-o" in cmd and "evidence/ch05-interconnection.puml" in cmd


def test_unknown_tool_raises():
    import pytest
    with pytest.raises(ValueError, match="unknown tool"):
        build_render_command("nope", "tree", "X", Path("a"), Path("b"), TOOLS)


def test_hash_bytes_is_stable_sha256():
    import hashlib
    data = b"hello"
    assert hash_bytes(data) == hashlib.sha256(data).hexdigest()


def test_svgs_differ_true_on_change_false_on_repeat():
    a = b"<svg>one</svg>"
    b = b"<svg>two</svg>"
    assert svgs_differ(a, b) is True
    assert svgs_differ(a, a) is False
