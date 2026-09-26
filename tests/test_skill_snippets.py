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
