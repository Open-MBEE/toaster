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
#
# DL-059 ADDENDUM (Task 5, allocate-fix/task5-harden-guard): the original fixture's
# `allocation heatAllocation allocate ApplyHeat to Toaster::heating;` carried BOTH a
# pre-existing `allocate-between-definitions` (D-019) violation (`ApplyHeat` resolves to a
# Definition, not a Feature) and the `allocate-connector-end-accessibility` (DL-058) violation
# next-passes.md item 23 anticipated (`Toaster::heating`'s declaring context, `ToasterDemo::Toaster`,
# is neither the allocation's own owner, `ToasterDemo`, nor a plain package). Item 24 in
# next-passes.md asked whether a conformant rewrite exists without losing this fixture's own point
# (a fully-qualified-path allocation end must dedup against the owned-part node); it does: promoting
# a named `action doApply : ApplyHeat;` to package level fixes the source-is-a-Definition problem,
# and nesting the allocation inside `Toaster` makes `Toaster::heating`'s declaring context equal the
# allocation's own new owner (`ToasterDemo::Toaster`) -- both gap rules are now clean, and the
# qualified-path target ('Toaster::heating') is unchanged, so the dedup-against-the-owned-part
# behavior this fixture exists to exercise is still genuinely tested.
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
    action doApply : ApplyHeat;
    part def Toaster {
        part control : ControlSystem;
        part heating : HeatingSystem;
        interface durationInterface connect control.durationOut to heating.durationIn;
        allocation heatAllocation allocate doApply to Toaster::heating;
    }
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


NESTED_SOURCE = """
package ToasterDemo {
    private import ScalarValues::*;
    item def Signal;
    part def Inner {
        part sensor : Signal;
    }
    part def Outer {
        part inner : Inner;
    }
    part def Top {
        part outer : Outer;
    }
}
"""


@pytest.fixture(scope="module")
def nested_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(NESTED_SOURCE, strict=False)
    assert model.ok, f"Nested model failed: {model.diagnostics}"
    yield model
    conn.close()


def test_default_depth_is_unchanged_direct_parts_only(nested_model):
    intent = build_interconnection_intent(nested_model, "ToasterDemo::Top")
    names = {p["name"] for p in intent["parts"]}
    assert names == {"outer"}


def test_depth_two_reaches_nested_composition(nested_model):
    intent = build_interconnection_intent(nested_model, "ToasterDemo::Top", depth=2)
    names = {p["name"] for p in intent["parts"]}
    assert "outer" in names
    assert "inner" in names


def test_depth_three_reaches_the_full_chain(nested_model):
    intent = build_interconnection_intent(nested_model, "ToasterDemo::Top", depth=3)
    names = {p["name"] for p in intent["parts"]}
    assert names == {"outer", "inner", "sensor"}


def test_negative_depth_raises_value_error(nested_model):
    with pytest.raises(ValueError):
        build_interconnection_intent(nested_model, "ToasterDemo::Top", depth=-1)


def test_none_depth_raises_value_error(nested_model):
    with pytest.raises(ValueError):
        build_interconnection_intent(nested_model, "ToasterDemo::Top", depth=None)


REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="module")
def ch06_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch06-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok, f"Ch06 model failed: {model.diagnostics}"
    yield model
    conn.close()


@pytest.fixture(scope="module")
def ch05_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch05-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok, f"Ch05 model failed: {model.diagnostics}"
    yield model
    conn.close()


def test_allocs_scoped_to_own_subtree_excludes_unrelated_owner(ch06_model):
    """Cross-cutting bug (independent review of CONTRACT DIAGRAM-PHASE2-TASK7):
    a HeatingAssembly-scoped interconnection diagram must not draw
    `ToasterDemo::Toaster::heatAllocation` (owned by Toaster, a different,
    unrelated element) just because one of its textual endpoints ('heating')
    happens to coincide with a Toaster part's short name. Only the real,
    in-scope `heatGenAllocation` (owned by HeatingAssembly itself) belongs
    here."""
    intent = build_interconnection_intent(
        ch06_model, "ToasterDemo::HeatingAssembly", depth=1
    )
    allocs = intent["allocs"]
    assert allocs == [{"source": "applyHeat.generateHeat", "target": "heatGen"}]
    assert {"source": "toastBread.applyHeat", "target": "heating"} not in allocs
    assert not any(a["target"] == "heating" for a in allocs)


def test_allocs_in_scope_allocation_still_included(ch05_model):
    """Negative control: an allocation that genuinely belongs to the diagram's
    own root (`ToasterDemo::Toaster::heatAllocation`, owned by Toaster itself)
    must be completely unaffected by the owner-scoping fix."""
    intent = build_interconnection_intent(ch05_model, "ToasterDemo::Toaster", depth=1)
    allocs = intent["allocs"]
    assert {"source": "toastBread.applyHeat", "target": "heating"} in allocs


def test_render_heatingassembly_excludes_heating_node_and_toaster_edge(ch06_model):
    """Rendered-output confirmation of the same fix: the SVG for a
    HeatingAssembly-scoped interconnection diagram must contain `heatGen` and
    must not contain a `heating` node or any Toaster-owned allocation edge."""
    intent = build_interconnection_intent(
        ch06_model, "ToasterDemo::HeatingAssembly", depth=1
    )
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "heatingassembly.svg"
        render_interconnection(intent, out)
        content = out.read_text()
        titles = [
            line.split(">")[1].split("<")[0]
            for line in content.splitlines()
            if "<title>" in line
        ]
        assert "heatGen" in titles
        assert "heating" not in titles
        assert "toastBread.applyHeat" not in titles
        assert not any(
            "toastBread.applyHeat" in t and "heating" in t for t in titles
        )
