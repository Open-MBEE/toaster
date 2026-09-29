"""Tests for containment_subgraph() (diagram generation strategy, Task 1)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from toaster.render import containment_subgraph

REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="module")
def ch06_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch06-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok, f"Ch6 fixture failed to load: {model.diagnostics}"
    yield model
    conn.close()


def _qnames(elements):
    return {e.as_dict().get("qualifiedName", e.as_dict().get("@id", "")) for e in elements}


def test_unknown_root_returns_empty_list(ch06_model):
    result = containment_subgraph(ch06_model, "ToasterDemo::NoSuchElement")
    assert result == []


def test_unrecognized_relation_raises_value_error(ch06_model):
    with pytest.raises(ValueError, match=r"unknown relation kind: 'compositon'"):
        containment_subgraph(ch06_model, "ToasterDemo::Toaster", relations=("compositon",))


def test_negative_depth_raises_value_error(ch06_model):
    with pytest.raises(ValueError, match=r"depth must be >= 0 or None, got -1"):
        containment_subgraph(ch06_model, "ToasterDemo::Toaster", depth=-1)


def test_depth_zero_returns_only_the_root(ch06_model):
    result = containment_subgraph(ch06_model, "ToasterDemo::Toaster", depth=0)
    assert _qnames(result) == {"ToasterDemo::Toaster"}


def test_toaster_reaches_direct_composition_and_typing_at_depth_two(ch06_model):
    # depth=1: Toaster's own composition children (heating, control).
    # depth=2: each child's typing target (HeatingSystem, ControlSystem) --
    # a node discovered via composition has its own typing edge explored on
    # the NEXT hop, per this function's pinned semantics.
    result = containment_subgraph(ch06_model, "ToasterDemo::Toaster", depth=2)
    names = _qnames(result)
    assert "ToasterDemo::Toaster" in names
    assert "ToasterDemo::Toaster::heating" in names
    assert "ToasterDemo::Toaster::control" in names
    assert "ToasterDemo::HeatingSystem" in names
    assert "ToasterDemo::ControlSystem" in names


def test_toaster_never_reaches_heatgen_at_any_depth(ch06_model):
    """The real finding from Phase 0's own review: Toaster::heating is typed
    by the abstract HeatingSystem, not the concrete HeatingAssembly that owns
    heatGen -- there is no composition or typing edge connecting them, so no
    depth value reaches heatGen from this root. This is the required
    negative-case test, not an optional one."""
    result = containment_subgraph(ch06_model, "ToasterDemo::Toaster", depth=None)
    names = _qnames(result)
    assert "ToasterDemo::HeatingAssembly::heatGen" not in names
    assert "ToasterDemo::HeatGenerator" not in names
    # Confirm the traversal actually terminated (returned, didn't hang) and
    # found the expected, smaller set -- not an accidentally-empty result.
    assert "ToasterDemo::Toaster" in names
    assert "ToasterDemo::HeatingSystem" in names


def test_heating_assembly_reaches_heatgen_at_depth_one(ch06_model):
    """The positive case: rooting directly at the definition that owns
    heatGen reaches it in exactly one composition hop."""
    result = containment_subgraph(ch06_model, "ToasterDemo::HeatingAssembly", depth=1)
    names = _qnames(result)
    assert "ToasterDemo::HeatingAssembly" in names
    assert "ToasterDemo::HeatingAssembly::heatGen" in names
    # HeatGenerator (heatGen's own type) is a second hop, not reached at depth=1.
    assert "ToasterDemo::HeatGenerator" not in names


def test_heating_assembly_reaches_heatgen_type_at_depth_two(ch06_model):
    result = containment_subgraph(ch06_model, "ToasterDemo::HeatingAssembly", depth=2)
    names = _qnames(result)
    assert "ToasterDemo::HeatGenerator" in names


def test_composition_only_excludes_typing_targets(ch06_model):
    result = containment_subgraph(
        ch06_model, "ToasterDemo::Toaster", relations=("composition",), depth=None
    )
    names = _qnames(result)
    assert "ToasterDemo::Toaster::heating" in names
    assert "ToasterDemo::HeatingSystem" not in names


def test_no_infinite_loop_on_a_flat_leaf_root(ch06_model):
    """A root with no composition children and no type field (a leaf) must
    terminate immediately, not hang."""
    result = containment_subgraph(ch06_model, "ToasterDemo::Bread", depth=None)
    assert _qnames(result) == {"ToasterDemo::Bread"}


CYCLE_SOURCE = """
package CycleTest {
    part def A { part b : B; }
    part def B { part a : A; }
}
"""


def test_no_infinite_loop_on_a_genuine_mutual_reference_cycle():
    """A (real, if unusual) mutual type reference -- A contains a part typed
    B, B contains a part typed back to A -- must not loop back to the root
    forever. This is the actual Review Focus case: a leaf root proves the
    stop condition fires when there's nothing left to find; this proves it
    fires when the SAME element would otherwise be rediscovered forever."""
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(CYCLE_SOURCE, strict=False)
    assert model.ok, f"Cycle model failed: {model.diagnostics}"
    result = containment_subgraph(model, "CycleTest::A", depth=None)
    conn.close()
    names = {e.as_dict().get("qualifiedName", e.as_dict().get("@id", "")) for e in result}
    assert names == {"CycleTest::A", "CycleTest::A::b", "CycleTest::B", "CycleTest::B::a"}
