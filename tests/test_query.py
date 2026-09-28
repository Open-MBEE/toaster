"""src/toaster/query.py against the ch08 cumulative model and small probe models."""

from pathlib import Path

import opensysml
import pytest

from toaster import query

ROOT = Path(__file__).resolve().parents[1]
LAYERS = ROOT / ".claude" / "skills" / "architecture-layers" / "example-layers.sysml"


@pytest.fixture(scope="module")
def conn():
    c = opensysml.connect(version="v0.9.0")
    yield c
    c.close()


@pytest.fixture(scope="module")
def ch08(conn):
    m = conn.load_from_content((ROOT / "models" / "ch08-cumulative.sysml").read_text(), strict=False)
    assert m.ok
    return m


def test_satisfy_relationships_read_the_json_content(ch08) -> None:
    """PASS4-008: the real, current model (rebased onto ch07) carries forward only
    `assert not satisfy timely by slow` (Chapter 3) and `assert satisfy` / `assert not
    satisfy heatGenerationReq` (Chapter 6); there is no `assert satisfy timely by
    nominal` in the real model at all, unlike the stale fixture this test used to read."""
    raw = query.get_satisfy_relationships(ch08)
    assert raw and all(e["@type"] == "SatisfyRequirementUsage" for e in raw)
    got = {(s["requirement"], s["subject"]) for s in query.satisfy_relationships(ch08)}
    assert ("ToasterDemo::timely", "ToasterDemo::slow") in got
    assert ("ToasterDemo::heatGenerationReq", "ToasterDemo::rated") in got
    assert ("ToasterDemo::heatGenerationReq", "ToasterDemo::weak") in got


UNNAMED_ALLOCATE = """
package P {
  action def ApplyHeat;
  part def HeatingSystem;
  action doApply : ApplyHeat;
  part heater : HeatingSystem;
  allocate doApply to heater;
}
"""


def test_find_allocations_sees_unnamed_allocate(conn) -> None:
    """PASS4-008: the real ch08 model no longer has an unnamed allocate (its own two
    allocations, `heatAllocation` and `heatGenAllocation`, are both named, usage-level
    AllocationUsages per DL-039's own fix), so this capability (find_connectors sees an
    unnamed connector, unlike model.query()) is demonstrated on a small standalone
    fixture instead; see test_find_allocations_sees_named_allocations below for ch08's
    own, now-named allocations."""
    m = conn.load_from_content(UNNAMED_ALLOCATE, strict=False)
    assert m.ok
    allocs = query.find_allocations(m)
    assert [a["ends"] for a in allocs] == [[["P::doApply"], ["P::heater"]]]


def test_find_allocations_sees_named_allocations(ch08) -> None:
    """The real model's two allocations, both named per DL-039's fix of the old
    definition-level `allocate` gap."""
    allocs = {a["id"]: a["ends"] for a in query.find_allocations(ch08)}
    assert allocs == {
        "ToasterDemo::heatAllocation": [
            ["ToasterDemo::ToastBread::applyHeat"],
            ["ToasterDemo::Toaster::heating"],
        ],
        "ToasterDemo::heatGenAllocation": [
            ["ToasterDemo::ApplyHeat::generateHeat"],
            ["ToasterDemo::HeatingAssembly::heatGen"],
        ],
    }


INHERITED_ALLOCATION = """
package P {
  action def ApplyHeat;
  part def HeatingSystem;
  part def HeatingAssembly :> HeatingSystem;
  action doApply : ApplyHeat;
  allocation alloc allocate doApply to HeatingSystem;
}
"""


def test_allocations_for_follows_supertypes(conn) -> None:
    """PASS4-008: the real ch08 model's two allocations are usage-level (`heatAllocation`
    targets the usage `Toaster::heating`, `heatGenAllocation` targets the usage
    `HeatingAssembly::heatGen`), not definition-level, so neither `HeatingSystem` nor
    `HeatingAssembly` (the definitions) is ever itself an allocation end any more, and
    `inherit=True` has nothing to add over the bare definitions in the real model (see
    test_allocations_for_on_ch08_usage_level_allocations below). The definition-level,
    supertype-following shape this test's own name promises (a subtype definition
    inheriting an allocation declared on its supertype definition) still exists as a
    capability of `allocations_for` and is demonstrated here on a small standalone
    fixture built the same shape as the old, stale ch08 fixture used to have."""
    m = conn.load_from_content(INHERITED_ALLOCATION, strict=False)
    assert m.ok
    assert query.allocations_for(m, "P::HeatingSystem", inherit=False)
    assert query.allocations_for(m, "P::HeatingAssembly")  # inherits HeatingSystem's allocation
    assert not query.allocations_for(m, "P::HeatingAssembly", inherit=False)


def test_allocations_for_on_ch08_usage_level_allocations(ch08) -> None:
    """The real model's allocations resolve directly at the usage level; querying the
    bare definitions with inherit=True finds nothing, because neither definition is
    itself ever an allocation end (the settable-result pattern this project's audits
    watch for does not recur here in a different guise: it simply does not apply, since
    the model never puts an allocation on a definition to begin with)."""
    assert query.allocations_for(ch08, "ToasterDemo::Toaster::heating", inherit=False)
    assert query.allocations_for(ch08, "ToasterDemo::HeatingAssembly::heatGen", inherit=False)
    assert not query.allocations_for(ch08, "ToasterDemo::HeatingSystem", inherit=True)
    assert not query.allocations_for(ch08, "ToasterDemo::HeatingAssembly", inherit=True)


FLOW_MODEL = """
package P {
  item def Bread;
  part def Loader { part bread : Bread; }
  part def Ejector { part bread : Bread; }
  part def Handling {
    part loader : Loader;
    part ejector : Ejector;
    flow loader.bread to ejector.bread;
  }
}
"""


def test_flows_and_connector_ends(conn) -> None:
    """PASS4-008: the real ch08 model has no FlowUsage at all (BreadLoader, BreadEjector
    and BreadHandling, the old stale fixture's flow endpoints, do not exist in the
    current model), so this capability (find_connectors resolving a chained flow end
    through ApiIndex.end_path) is demonstrated on a small standalone fixture instead,
    built the same shape (a loader's bread flowing to an ejector's bread) the old
    fixture had."""
    m = conn.load_from_content(FLOW_MODEL, strict=False)
    assert m.ok
    flows = query.find_connectors(m, "FlowUsage")
    assert flows[0]["ends"][0] == ["P::Handling::loader", "P::Loader::bread"]


def test_specialization_closure_finds_realizers(ch08) -> None:
    """PASS4-008: in the real model, `HeatingSystem` and `ControlSystem` no longer
    specialize `ToastingSystem` directly (DL-019's own fix of the F-3 finding it
    named: a logical component specializing the whole's purpose type contradicted the
    subject reading), so only `Toaster` and its own usages realize `ToastingSystem` now.
    `HeatingAssembly :> HeatingSystem` is a real, unchanged specialization."""
    realizers = query.specializes_transitively(ch08, "ToasterDemo::ToastingSystem")
    assert {"ToasterDemo::Toaster", "ToasterDemo::nominal", "ToasterDemo::slow"} <= realizers
    assert "ToasterDemo::HeatingSystem" in query.supertypes_transitively(ch08, "ToasterDemo::HeatingAssembly")


def test_requirement_coverage_joins_satisfy_to_requirements(ch08) -> None:
    """PASS4-008: `timely` is covered by `slow` only (no `nominal` claim exists in the
    real model); `heatGenerationReq` is covered by both `rated` and `weak`, the real
    model's second requirement-coverage pair, not exercised by the old stale fixture's
    single covered requirement."""
    cov = {c["requirement"]: c for c in query.requirement_coverage(ch08)}
    assert cov["ToasterDemo::timely"]["covered"]
    assert cov["ToasterDemo::timely"]["satisfied_by"] == ["ToasterDemo::slow"]
    assert cov["ToasterDemo::heatGenerationReq"]["covered"]
    assert cov["ToasterDemo::heatGenerationReq"]["satisfied_by"] == [
        "ToasterDemo::rated",
        "ToasterDemo::weak",
    ]


def test_perform_relationships_on_layers_example(conn) -> None:
    m = conn.load_from_content(LAYERS.read_text(), strict=False)
    assert query.perform_relationships(m) == [{"performer": "ToasterLayers::HeatSource", "action": "ToasterLayers::ApplyHeat"}]


MISMATCH = """
package P {
  port def PowerPort; port def FuelPort; port def GasPort :> FuelPort;
  part def Outlet { port o : PowerPort; }
  part def Torch { port fuelIn : FuelPort; }
  part def Tank { port f : GasPort; }
  part outlet : Outlet; part torch : Torch; part tank : Tank;
  connect outlet.o to torch.fuelIn;
  connect tank.f to torch.fuelIn;
}
"""


def test_port_type_check_flags_only_the_unrelated_pair(conn) -> None:
    m = conn.load_from_content(MISMATCH, strict=False)
    bad = query.port_type_mismatches(m)
    assert len(bad) == 1 and bad[0]["types"] == [["P::PowerPort"], ["P::FuelPort"]]   # GasPort specializes FuelPort: fine


def test_port_type_check_is_clean_on_ch08(ch08) -> None:
    assert query.port_type_mismatches(ch08) == []
