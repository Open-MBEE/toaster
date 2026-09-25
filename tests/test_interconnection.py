"""Tests for build_interconnection_intent and render_sysmld (WP-4)."""
import json
import sys
import tempfile
import warnings
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from toaster.render import build_interconnection_intent, render_sysmld

FLOW_SOURCE = """
package ToasterDemo {
    private import ScalarValues::*;
    item def Start;
    item def Finish;
    part def BreadLoader { part bread : Start; }
    part def BreadEjector { part bread : Finish; }
    part def BreadHandling {
        part loader : BreadLoader;
        part ejector : BreadEjector;
        flow loader.bread to ejector.bread;
    }
    action def ApplyHeat;
    part def HeatingSystem;
    allocate ApplyHeat to HeatingSystem;
}
"""

ALLOC_SOURCE = """
package ToasterDemo {
    action def ApplyHeat;
    part def HeatingSystem;
    allocate ApplyHeat to HeatingSystem;
}
"""


@pytest.fixture(scope="module")
def flow_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(FLOW_SOURCE, strict=False)
    assert model.ok, f"Flow model failed: {model.diagnostics}"
    yield model
    conn.close()


@pytest.fixture(scope="module")
def alloc_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(ALLOC_SOURCE, strict=False)
    assert model.ok, f"Alloc model failed: {model.diagnostics}"
    yield model
    conn.close()


def test_intent_parts(flow_model):
    intent = build_interconnection_intent(flow_model, "ToasterDemo::BreadHandling")
    names = [p["name"] for p in intent["parts"]]
    assert "loader" in names
    assert "ejector" in names


def test_intent_flows(flow_model):
    intent = build_interconnection_intent(flow_model, "ToasterDemo::BreadHandling")
    assert len(intent["flows"]) == 1
    flow = intent["flows"][0]
    assert flow["source"] == "loader.bread"
    assert flow["target"] == "ejector.bread"


def test_intent_title(flow_model):
    intent = build_interconnection_intent(flow_model, "ToasterDemo::BreadHandling")
    assert intent["title"] == "ToasterDemo::BreadHandling"


def test_intent_allocs(alloc_model):
    intent = build_interconnection_intent(alloc_model, "ToasterDemo")
    allocs = intent["allocs"]
    assert len(allocs) >= 1
    sources = [a["source"] for a in allocs]
    targets = [a["target"] for a in allocs]
    assert "ApplyHeat" in sources
    assert "HeatingSystem" in targets


def test_render_sysmld_produces_svg(flow_model):
    intent = build_interconnection_intent(flow_model, "ToasterDemo::BreadHandling")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.svg"
        render_sysmld(intent, out)
        assert out.exists()
        content = out.read_text()
        assert "<svg" in content


def test_render_sysmld_svg_contains_parts(flow_model):
    intent = build_interconnection_intent(flow_model, "ToasterDemo::BreadHandling")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.svg"
        render_sysmld(intent, out)
        content = out.read_text()
        assert "loader" in content
        assert "ejector" in content


def test_mutation_changes_diagram(flow_model):
    """Semantic correspondence check: a model change must produce a different SVG."""
    intent1 = build_interconnection_intent(flow_model, "ToasterDemo::BreadHandling")
    # Mutate intent: add a spurious part
    import copy
    intent2 = copy.deepcopy(intent1)
    intent2["parts"].append({"name": "extra", "type": "ExtraPart"})
    with tempfile.TemporaryDirectory() as tmp:
        out1 = Path(tmp) / "a.svg"
        out2 = Path(tmp) / "b.svg"
        render_sysmld(intent1, out1)
        render_sysmld(intent2, out2)
        assert out1.read_text() != out2.read_text()
