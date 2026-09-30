"""src/toaster/query.py against the ch08 cumulative model and small probe models."""

from pathlib import Path

import opensysml
import pytest

from toaster import conformance, query

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
    """The real model's two allocations, both named and nested per DL-058's fix of the
    package-level qualified-name non-conformance (see decisions/log.md DL-058)."""
    allocs = {a["id"]: a["ends"] for a in query.find_allocations(ch08)}
    assert allocs == {
        "ToasterDemo::Toaster::heatAllocation": [
            ["ToasterDemo::ToastingSystem::toastBread", "ToasterDemo::ToastBread::applyHeat"],
            ["ToasterDemo::Toaster::heating"],
        ],
        "ToasterDemo::HeatingAssembly::heatGenAllocation": [
            ["ToasterDemo::HeatingSystem::applyHeat", "ToasterDemo::ApplyHeat::generateHeat"],
            ["ToasterDemo::HeatingAssembly::heatGen"],
        ],
    }


INHERITED_ALLOCATION = """
package P {
  action def ApplyHeat;
  part def HeatingSystem;
  part def HeatingAssembly :> HeatingSystem;
  action doApply : ApplyHeat;
  part def Toaster {
    part heater : HeatingSystem;
    allocation alloc allocate doApply to heater;
  }
  part def BetterToaster :> Toaster {
    part :>> heater : HeatingAssembly;
  }
}
"""


def test_allocations_for_follows_supertypes(conn) -> None:
    """PASS4-008 round 2 review: the first version of this fixture allocated directly to
    a bare PartDefinition (`allocate doApply to HeatingSystem;`), which is language
    non-conformant (KerML 8.3.3.3.9 ReferenceSubsetting requires a Feature, not a
    Definition; DL-039's own `allocate-between-definitions` gap rule flags exactly this,
    confirmed directly), reintroducing by accident the pattern this project's own
    conformance checks exist to catch. A later version allocated to a genuine usage but
    by a package-level qualified path (`allocate doApply to Toaster::heater;`), which
    DL-058 later ruled non-conformant too (the `Toaster::heater` end reaches into
    `Toaster`'s own nested feature with no featuring context making it accessible,
    caught directly by `allocate-connector-end-accessibility`, DL-058/D-032). This
    version nests the allocation inside `Toaster` itself, alongside `heater` (matching
    the conformant idiom Tasks 1-3 of the DL-058 remediation established for the real
    chapter models), and demonstrates `inherit=True` following a redefinition
    (`BetterToaster`'s own `:>> heater`), a real, conformant supertype-chain
    relationship (confirmed: `model.ok` is True, `language_gap_findings` is empty), the
    same shape the real ch08 model's own allocations are usage-level (see
    test_allocations_for_on_ch08_usage_level_allocations below, where neither
    `HeatingSystem` nor `HeatingAssembly` is itself ever an allocation end)."""
    m = conn.load_from_content(INHERITED_ALLOCATION, strict=False)
    assert m.ok
    assert conformance.language_gap_findings(m) == []
    assert query.allocations_for(m, "P::Toaster::heater", inherit=False)
    assert query.allocations_for(m, "P::BetterToaster::heater")  # inherits Toaster::heater's allocation via redefinition
    assert not query.allocations_for(m, "P::BetterToaster::heater", inherit=False)


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
  part def Loader { item bread : Bread; }
  part def Ejector { item bread : Bread; }
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
    fixture had. PASS4-008 round 2 review: the first version of this fixture typed
    `bread` as `part bread : Bread` (a part usage typed only by an item def), which is
    language non-conformant (SysML validatePartUsagePartDefinition; DL-039's own
    `part-typed-only-by-item-def` gap rule flags exactly this, confirmed directly),
    reintroducing by accident the pattern this project's own conformance checks exist
    to catch. `item bread : Bread` (confirmed: `model.ok` is True, `language_gap_findings`
    is empty) exercises the identical flow-resolution path without that defect."""
    m = conn.load_from_content(FLOW_MODEL, strict=False)
    assert m.ok
    assert conformance.language_gap_findings(m) == []
    flows = query.find_connectors(m, "FlowUsage")
    assert flows[0]["ends"][0] == ["P::Handling::loader", "P::Loader::bread"]


def test_specialization_closure_finds_realizers(ch08) -> None:
    """PASS4-008: in the real model, `HeatingSystem` and `ControlSystem` no longer
    specialize `ToastingSystem` directly (DL-019's own fix of the F-3 finding it
    named: a logical component specializing the whole's purpose type contradicted the
    subject reading), so only `Toaster` and its own usages realize `ToastingSystem` now.
    PASS4-008 round 2 review restored the genuine two-hop chain the previous round's
    rewrite dropped: `rated`'s own supertypes are `ResistanceCoil` and, one hop further,
    `HeatGenerator` (`ResistanceCoil :> HeatGenerator`), confirmed directly against the
    real model, giving `supertypes_transitively` a real multi-hop closure to walk, not
    only the single-hop `HeatingAssembly :> HeatingSystem` case."""
    realizers = query.specializes_transitively(ch08, "ToasterDemo::ToastingSystem")
    assert {"ToasterDemo::Toaster", "ToasterDemo::nominal", "ToasterDemo::slow"} <= realizers
    assert "ToasterDemo::HeatingSystem" in query.supertypes_transitively(ch08, "ToasterDemo::HeatingAssembly")
    assert query.supertypes_transitively(ch08, "ToasterDemo::rated") == {
        "ToasterDemo::ResistanceCoil",
        "ToasterDemo::HeatGenerator",
    }


def test_requirement_coverage_joins_satisfy_to_requirements(ch08) -> None:
    """PASS4-009 round 2 (fixing a bug reported live in
    decisions/audits/ch06-layer-audit.md and never fixed): `requirement_coverage` must
    split by polarity, not just by requirement. Against the real ch08 model, `timely`
    has only a NEGATIVE claim (`assert not satisfy timely by slow`) and a `verify`
    objective with no bound subject -- no candidate has ever been positively claimed to
    satisfy it, so `covered` must be False, not True. `heatGenerationReq` has one real
    positive claim (`rated`) and one real negative claim (`weak`): `satisfied_by` must
    contain only `rated`, and `weak` must appear in `failed_by` instead, never counted
    as coverage."""
    cov = {c["requirement"]: c for c in query.requirement_coverage(ch08)}

    assert cov["ToasterDemo::timely"]["covered"] is False
    assert cov["ToasterDemo::timely"]["satisfied_by"] == []
    assert cov["ToasterDemo::timely"]["failed_by"] == ["ToasterDemo::slow"]

    assert cov["ToasterDemo::heatGenerationReq"]["covered"] is True
    assert cov["ToasterDemo::heatGenerationReq"]["satisfied_by"] == ["ToasterDemo::rated"]
    assert cov["ToasterDemo::heatGenerationReq"]["failed_by"] == ["ToasterDemo::weak"]


def test_requirement_coverage_excludes_verification_case_objective(ch08) -> None:
    """A `verification def`'s own `objective { verify X; }` block is exported as its own
    unnamed `RequirementUsage` (`ToasterDemo::TimelyToastTest::@2`, no `declaredName`):
    the objective's own auto-synthesized wrapper, not a design requirement. It must not
    appear in the coverage report at all (a bare bookkeeping artifact reported as an
    uncovered requirement would be noise, not a finding)."""
    reqs = {c["requirement"] for c in query.requirement_coverage(ch08)}
    assert reqs == {"ToasterDemo::timely", "ToasterDemo::heatGenerationReq"}
    assert not any(r.startswith("ToasterDemo::TimelyToastTest") for r in reqs)


def test_satisfy_relationships_reports_is_negated(ch08) -> None:
    """`satisfy_relationships` exposes `is_negated` so callers can distinguish a
    positive claim from a negative one; a `verify` objective (no subject) is
    `is_negated=False`, since it asserts nothing about any subject to negate."""
    by_id = {s["id"]: s for s in query.satisfy_relationships(ch08)}
    assert by_id["ToasterDemo::slow::@1"]["is_negated"] is True
    assert by_id["ToasterDemo::rated::@1"]["is_negated"] is False
    assert by_id["ToasterDemo::weak::@1"]["is_negated"] is True
    assert by_id["ToasterDemo::TimelyToastTest::@2::@0"]["is_negated"] is False
    assert by_id["ToasterDemo::TimelyToastTest::@2::@0"]["subject"] is None


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


@pytest.fixture(scope="module")
def ch10(conn):
    m = conn.load_from_content((ROOT / "models" / "ch10-cumulative.sysml").read_text(), strict=False)
    assert m.ok
    return m


LEMMA = "ToasterDemo::deliveredEnergyBoundedBySupply"


def test_requirement_ties_negative_control_real_model(ch10) -> None:
    """decisions/next-passes.md item 29 / decisions/log.md DL-070: the real, current model has
    no genuine tie from any requirement to `deliveredEnergyBoundedBySupply`. Confirm this is for
    the right reason -- a real, exhaustive search over every element's own `subsets`/`redefines`/
    `references` field found nothing -- not because the search itself is narrow."""
    idx = query.ApiIndex(ch10)
    assert query.requirement_ties(ch10, LEMMA, idx) == []
    assert query.tied_to_any_requirement(ch10, LEMMA, idx) is False


REQUIREMENT_SUBSETS_TIE = """
package TieFixture {
    private import ToasterDemo::*;
    requirement def EnergyReq {
        subject t : Toaster;
        require constraint c :> deliveredEnergyBoundedBySupply;
    }
}
"""


def test_requirement_ties_positive_control_subsets(conn, ch10) -> None:
    """A `requirement def`'s own `require constraint c :> deliveredEnergyBoundedBySupply;` is a
    real, constructible tie the old `SatisfyRequirementUsage.subsets`-only check could never see
    (its target is a bare `ConstraintUsage`, not a `SatisfyRequirementUsage` at all): confirm the
    broader search finds it, via `c`'s own `subsets` field, owned by `TieFixture::EnergyReq`."""
    source = (ROOT / "models" / "ch10-cumulative.sysml").read_text() + REQUIREMENT_SUBSETS_TIE
    m = conn.load_from_content(source, strict=False)
    assert m.ok
    idx = query.ApiIndex(m)
    ties = query.requirement_ties(m, LEMMA, idx)
    assert ties == [{"tying_element": "TieFixture::EnergyReq::c", "field": "subsets", "requirement": "TieFixture::EnergyReq"}]
    assert query.tied_to_any_requirement(m, LEMMA, idx) is True


REQUIREMENT_REFERENCES_AND_USAGE_TIE = """
package TieFixture2 {
    private import ToasterDemo::*;
    requirement def EnergyReq2 {
        subject t : Toaster;
        ref altName references deliveredEnergyBoundedBySupply;
    }
    requirement usageTie : EnergyReq2 {
        require constraint c2 :> deliveredEnergyBoundedBySupply;
    }
}
"""


def test_requirement_ties_positive_control_references_and_usage_owner(conn, ch10) -> None:
    """The search also covers the `references` field (a `ref ... references target;` inside a
    requirement) and a `RequirementUsage` (not just a `RequirementDefinition`) as the owning
    requirement -- both real, distinct ways a tie can be made that a `subsets`-only,
    `SatisfyRequirementUsage`-only search would miss."""
    source = (ROOT / "models" / "ch10-cumulative.sysml").read_text() + REQUIREMENT_REFERENCES_AND_USAGE_TIE
    m = conn.load_from_content(source, strict=False)
    assert m.ok
    idx = query.ApiIndex(m)
    ties = {(t["tying_element"], t["field"]): t["requirement"] for t in query.requirement_ties(m, LEMMA, idx)}
    assert ties == {
        ("TieFixture2::EnergyReq2::altName", "references"): "TieFixture2::EnergyReq2",
        ("TieFixture2::usageTie::c2", "subsets"): "TieFixture2::usageTie",
    }
    assert query.tied_to_any_requirement(m, LEMMA, idx) is True


NON_REQUIREMENT_TIE = """
package NonReqTie {
    private import ToasterDemo::*;
    part def Widget {
        constraint c3 :> deliveredEnergyBoundedBySupply;
    }
}
"""


def test_requirement_ties_reports_none_when_not_requirement_owned(conn, ch10) -> None:
    """A `subsets` tie owned by an unrelated part (not any requirement) is found by the search,
    but reported with `requirement=None`, and `tied_to_any_requirement` stays `False`: a tie is
    only a traceability tie when a requirement actually owns it."""
    source = (ROOT / "models" / "ch10-cumulative.sysml").read_text() + NON_REQUIREMENT_TIE
    m = conn.load_from_content(source, strict=False)
    assert m.ok
    idx = query.ApiIndex(m)
    ties = query.requirement_ties(m, LEMMA, idx)
    assert ties == [{"tying_element": "NonReqTie::Widget::c3", "field": "subsets", "requirement": None}]
    assert query.tied_to_any_requirement(m, LEMMA, idx) is False


def test_requirement_ties_mutation_old_narrow_check_misses_real_tie(conn, ch10) -> None:
    """Mutation test: the OLD, narrow check (does the lemma's own id ever appear as any
    `SatisfyRequirementUsage`'s own `subsets` target?) still reports `False` against the fixture
    above, which contains a genuine, constructed tie -- proving the old check is blind to it, and
    that the new, broader `requirement_ties`/`tied_to_any_requirement` is not itself vacuous."""
    source = (ROOT / "models" / "ch10-cumulative.sysml").read_text() + REQUIREMENT_SUBSETS_TIE
    m = conn.load_from_content(source, strict=False)
    assert m.ok
    idx = query.ApiIndex(m)
    satisfy_targets = {s["subsets"]["@id"] for s in idx.of_type("SatisfyRequirementUsage") if "subsets" in s}
    lemma = idx.by_qn[LEMMA]
    old_check_result = lemma["@id"] in satisfy_targets
    assert old_check_result is False
    assert query.tied_to_any_requirement(m, LEMMA, idx) is True


REQUIREMENT_REFERENT_TIE = """
package TieFixture3 {
    private import ToasterDemo::*;
    requirement def EnergyReq3 {
        subject t : Toaster;
        require deliveredEnergyBoundedBySupply;
    }
}
"""


def test_requirement_ties_positive_control_referent(conn, ch10) -> None:
    """F1 (round-2 review): a bare `require target;` (a requirement reference to an
    already-existing constraint, not declaring a new one) exports as a `FeatureReferenceExpression`
    whose own `referent` field holds the target's id directly -- a different shape from
    `subsets`/`redefines`/`references`, which the pre-round-2 search never looked at, and which
    `require deliveredEnergyBoundedBySupply;` (as opposed to `require constraint c :>
    deliveredEnergyBoundedBySupply;`, already covered by the `subsets` control above) is confirmed
    to produce. Confirm the search now finds it, owned by `TieFixture3::EnergyReq3` (walking up
    through the `FeatureReferenceExpression`'s own owning `ConstraintUsage`)."""
    source = (ROOT / "models" / "ch10-cumulative.sysml").read_text() + REQUIREMENT_REFERENT_TIE
    m = conn.load_from_content(source, strict=False)
    assert m.ok
    idx = query.ApiIndex(m)
    ties = query.requirement_ties(m, LEMMA, idx)
    assert len(ties) == 1
    assert ties[0]["field"] == "referent"
    assert ties[0]["requirement"] == "TieFixture3::EnergyReq3"
    assert query.tied_to_any_requirement(m, LEMMA, idx) is True


REQUIREMENT_REDEFINES_TIE = """
package TieFixture4 {
    private import ToasterDemo::*;
    requirement def EnergyReq4 {
        subject t : Toaster;
        require constraint c :>> deliveredEnergyBoundedBySupply;
    }
}
"""


def test_requirement_ties_positive_control_redefines(conn, ch10) -> None:
    """F3 (round-2 review): the reviewer's own confirmed-working `redefines` construct
    (`require constraint c :>> deliveredEnergyBoundedBySupply;`) was a real, working code path in
    `requirement_ties` with no test of its own. Confirm it is found via `c`'s own `redefines`
    field, owned by `TieFixture4::EnergyReq4`."""
    source = (ROOT / "models" / "ch10-cumulative.sysml").read_text() + REQUIREMENT_REDEFINES_TIE
    m = conn.load_from_content(source, strict=False)
    assert m.ok
    idx = query.ApiIndex(m)
    ties = query.requirement_ties(m, LEMMA, idx)
    assert ties == [{"tying_element": "TieFixture4::EnergyReq4::c", "field": "redefines", "requirement": "TieFixture4::EnergyReq4"}]
    assert query.tied_to_any_requirement(m, LEMMA, idx) is True


REQUIREMENT_USAGE_DIRECT_TIE = """
package TieFixture5 {
    private import ToasterDemo::*;
    requirement r :> deliveredEnergyBoundedBySupply;
}
"""


def test_requirement_ties_positive_control_usage_is_tying_element_itself(conn, ch10) -> None:
    """F3 (round-2 review): the reviewer's own confirmed-working construct where the tying
    element is ITSELF a `RequirementUsage` (not a constraint nested inside one):
    `requirement r :> deliveredEnergyBoundedBySupply;` puts `subsets` directly on `r`, a
    `RequirementUsage`. `_nearest_requirement_owner`'s inclusive walk must find `r` as its own
    nearest requirement ancestor, not `None`."""
    source = (ROOT / "models" / "ch10-cumulative.sysml").read_text() + REQUIREMENT_USAGE_DIRECT_TIE
    m = conn.load_from_content(source, strict=False)
    assert m.ok
    idx = query.ApiIndex(m)
    ties = query.requirement_ties(m, LEMMA, idx)
    assert ties == [{"tying_element": "TieFixture5::r", "field": "subsets", "requirement": "TieFixture5::r"}]
    assert query.tied_to_any_requirement(m, LEMMA, idx) is True


def test_requirement_ties_raises_on_unknown_target(ch10) -> None:
    """F4: a target that does not resolve to any real element in the model must raise loudly,
    not silently report an empty result -- the same "passes for the wrong reason" shape the
    original bug had, just at a different layer. This also demonstrates the fix actually catches
    a hypothetical future typo/rename of the lemma: confirm the real target exists first, then
    confirm a nonexistent one raises."""
    idx = query.ApiIndex(ch10)
    assert idx.by_qn.get(LEMMA) is not None
    with pytest.raises(KeyError):
        query.requirement_ties(ch10, "ToasterDemo::NonexistentThing", idx)
    with pytest.raises(KeyError):
        query.tied_to_any_requirement(ch10, "ToasterDemo::NonexistentThing", idx)
