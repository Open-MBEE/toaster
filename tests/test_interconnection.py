"""Tests for build_interconnection_intent and render_interconnection (WP-4)."""
import json
import sys
import tempfile
import warnings
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from toaster.render import build_interconnection_intent, render_interconnection

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

# PASS4-005 push-back (Finding 9): the allocation target used a fully-qualified path
# ('Toaster::heating') while the owned-part extraction used the short name ('heating'),
# so the two were drawn as separate nodes for the same model element. Also exercises
# the InterfaceUsage recognition OQ-1 added (a connection whose ends are all ports).
QUALIFIED_ALLOC_AND_INTERFACE_SOURCE = """
package ToasterDemo {
    private import ScalarValues::*;
    private import SI::*;
    private import ISQ::*;
    port def DurationPort { out duration : ISQ::DurationValue[0..*]; }
    action def ApplyHeat;
    part def ControlSystem { port durationOut : DurationPort; }
    part def HeatingSystem {
        perform action applyHeat : ApplyHeat;
        port durationIn : ~DurationPort;
    }
    part def Toaster {
        part control : ControlSystem;
        part heating : HeatingSystem;
        interface durationInterface connect control.durationOut to heating.durationIn;
    }
    allocation heatAllocation allocate ApplyHeat to Toaster::heating;
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


@pytest.fixture(scope="module")
def qualified_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(
        QUALIFIED_ALLOC_AND_INTERFACE_SOURCE, strict=False
    )
    assert model.ok, f"Qualified model failed: {model.diagnostics}"
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


def test_render_interconnection_produces_svg(flow_model):
    intent = build_interconnection_intent(flow_model, "ToasterDemo::BreadHandling")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.svg"
        render_interconnection(intent, out)
        assert out.exists()
        content = out.read_text()
        assert "<svg" in content


def test_render_interconnection_svg_contains_parts(flow_model):
    intent = build_interconnection_intent(flow_model, "ToasterDemo::BreadHandling")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.svg"
        render_interconnection(intent, out)
        content = out.read_text()
        assert "loader" in content
        assert "ejector" in content


def test_intent_flows_includes_interface_usage(qualified_model):
    """OQ-1: build_interconnection_intent must recognize InterfaceUsage (a
    connection whose ends are all ports, SysML v2 formal/2026-03-02 §7.14.1),
    not only FlowUsage."""
    intent = build_interconnection_intent(qualified_model, "ToasterDemo::Toaster")
    assert len(intent["flows"]) == 1
    flow = intent["flows"][0]
    assert flow["source"] == "control.durationOut"
    assert flow["target"] == "heating.durationIn"


def test_qualified_allocation_target_reuses_the_part_node(qualified_model):
    """Finding 9: an allocation end written as a fully-qualified path
    ('Toaster::heating') must resolve to the same node the owned-part extraction
    already created ('heating'), not a separate, duplicate box for the same
    model element."""
    intent = build_interconnection_intent(qualified_model, "ToasterDemo::Toaster")
    part_names = {p["name"] for p in intent["parts"]}
    assert "heating" in part_names
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.svg"
        render_interconnection(intent, out)
        content = out.read_text()
        titles = [
            line.split(">")[1].split("<")[0]
            for line in content.splitlines()
            if "<title>" in line
        ]
        # Exactly one node is titled "heating"; "Toaster::heating" never appears
        # as its own node.
        assert titles.count("heating") == 1
        assert "Toaster::heating" not in titles


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
        render_interconnection(intent1, out1)
        render_interconnection(intent2, out2)
        assert out1.read_text() != out2.read_text()
