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
    raw = query.get_satisfy_relationships(ch08)
    assert raw and all(e["@type"] == "SatisfyRequirementUsage" for e in raw)
    got = {(s["requirement"], s["subject"]) for s in query.satisfy_relationships(ch08)}
    assert ("ToasterDemo::timely", "ToasterDemo::nominal") in got
    assert ("ToasterDemo::timely", "ToasterDemo::slow") in got


def test_find_allocations_sees_unnamed_allocate(ch08) -> None:
    allocs = query.find_allocations(ch08)
    assert [a["ends"] for a in allocs] == [[["ToasterDemo::ApplyHeat"], ["ToasterDemo::HeatingSystem"]]]


def test_allocations_for_follows_supertypes(ch08) -> None:
    assert query.allocations_for(ch08, "ToasterDemo::HeatingSystem", inherit=False)
    assert query.allocations_for(ch08, "ToasterDemo::HeatingAssembly")          # inherits HeatingSystem's allocation
    assert not query.allocations_for(ch08, "ToasterDemo::HeatingAssembly", inherit=False)


def test_flows_and_connector_ends(ch08) -> None:
    flows = query.find_connectors(ch08, "FlowUsage")
    assert flows[0]["ends"][0] == ["ToasterDemo::BreadHandling::loader", "ToasterDemo::BreadLoader::bread"]


def test_specialization_closure_finds_realizers(ch08) -> None:
    realizers = query.specializes_transitively(ch08, "ToasterDemo::ToastingSystem")
    assert {"ToasterDemo::HeatingSystem", "ToasterDemo::ControlSystem", "ToasterDemo::HeatingAssembly"} <= realizers
    assert "ToasterDemo::ToastingSystem" in query.supertypes_transitively(ch08, "ToasterDemo::HeatingAssembly")


def test_requirement_coverage_joins_satisfy_to_requirements(ch08) -> None:
    cov = {c["requirement"]: c for c in query.requirement_coverage(ch08)}
    assert cov["ToasterDemo::timely"]["covered"]
    assert cov["ToasterDemo::timely"]["satisfied_by"] == ["ToasterDemo::nominal", "ToasterDemo::slow"]


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
