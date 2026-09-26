"""Snippets shipped in skills must stay runnable: load them with OpenSysML and require ok."""

from pathlib import Path

import pytest

opensysml = pytest.importorskip("opensysml")

SKILLS = Path(__file__).resolve().parents[1] / ".claude" / "skills"


@pytest.fixture(scope="module")
def conn():
    c = opensysml.connect(version="v0.9.0")
    yield c
    c.close()


def test_architecture_layers_example_loads(conn) -> None:
    model = conn.load_from_content((SKILLS / "architecture-layers" / "example-layers.sysml").read_text(), strict=False)
    assert model.ok, [d.message for d in model.diagnostics]


def python_blocks(path: Path) -> list[str]:
    lines, out, cur = path.read_text().splitlines(), [], None
    for line in lines:
        if line.strip() == "```python":
            cur = []
        elif line.strip() == "```" and cur is not None:
            out.append("\n".join(cur))
            cur = None
        elif cur is not None:
            cur.append(line)
    return out


def test_opensysml_query_recipes_run_against_ch08(monkeypatch) -> None:
    root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(root)
    ns: dict = {}
    for i, block in enumerate(python_blocks(SKILLS / "opensysml-query" / "SKILL.md")):
        exec(compile(block, f"opensysml-query block {i}", "exec"), ns)  # noqa: S102


def test_opensysml_query_perform_recipe_on_layers_example(monkeypatch) -> None:
    root = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(root)
    blocks = python_blocks(SKILLS / "opensysml-query" / "SKILL.md")
    ns: dict = {}
    exec(compile(blocks[0], "setup", "exec"), ns)  # noqa: S102
    model = ns["conn"].load_from_content((SKILLS / "architecture-layers" / "example-layers.sysml").read_text(), strict=False)
    ns["model"], ns["els"] = model, ns["api_elements"](model)
    ns["by_id"] = {e["@id"]: e for e in ns["els"]}
    exec(compile(blocks[4].replace("assert satisfies()", ""), "recipe4", "exec"), ns)  # noqa: S102
    assert ns["performs"]() == [{"performer": "ToasterLayers::HeatSource", "action": "ToasterLayers::ApplyHeat"}]
