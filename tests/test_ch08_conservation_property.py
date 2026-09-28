"""Chapter 8's new construct: `deliveredEnergyBoundedBySupply`, a real `assert constraint`
in `models/ch08-cumulative.sysml`, proved by `toaster.modelcheck.verify_holds()` (real
`sysmlv2 verify --solve`, Z3) rather than evaluated at one point (work contract PASS4-008).

Like `tests/test_modelcheck.py`, every test here runs the real `sysmlv2` binary and is
skipped when it is not present on this machine, per the same rationale: mocking the
subprocess would test nothing about whether the CLI actually proves this property.
"""

from pathlib import Path

import opensysml
import pytest

from toaster import modelcheck as mc

ROOT = Path(__file__).resolve().parents[1]
BINARY = Path.home() / "Documents/GitHub/sysml-toolkit/target/release/sysmlv2"
LIB = (
    Path.home()
    / "Documents/GitHub/sysml-toolkit/spec-refs/SysML-v2-Release/sysml.library"
)

pytestmark = pytest.mark.skipif(
    not BINARY.exists(),
    reason=f"sysmlv2 binary not found at {BINARY} (see work contract PASS4-008)",
)

# Restates deliveredEnergyBoundedBySupply exactly as committed in ch08-cumulative.sysml,
# with a minimal HeatGenerator stub, and no assert satisfy declaration. A companion
# restatement is used rather than the committed cumulative file directly because
# toaster.modelcheck's own line parser cannot yet read a verdict line for a constraint
# that is also the subject of an assert satisfy / assert not satisfy declaration, which
# the real cumulative model carries forward from Chapter 3 and Chapter 6
# (DEFERRED.md D-029).
COMPANION_POSITIVE = """
package ConservationCheck {
    private import ScalarValues::*;
    private import SI::*;
    private import ISQ::*;
    private import MeasurementReferences::*;

    abstract part def HeatGenerator {
        attribute power : ISQ::PowerValue;
        attribute efficiency : DimensionOneValue;
    }
    part heatGenCheck : HeatGenerator;
    attribute heatGenCheckDuration : ISQ::DurationValue;

    assert constraint deliveredEnergyBoundedBySupply {
        (heatGenCheck.efficiency >= 0.0 and heatGenCheck.efficiency <= 1.0
         and heatGenCheck.power >= 0.0 [SI::W] and heatGenCheckDuration >= 0.0 [SI::s])
        implies (heatGenCheck.power * heatGenCheckDuration * heatGenCheck.efficiency)
                <= heatGenCheck.power * heatGenCheckDuration
    }
}
"""

# Same shape, conclusion deliberately negated: given the same bounded hypothesis,
# delivered energy can never strictly exceed supplied energy, so this is unsatisfiable.
# Z3 must actually resolve a product of three bounded unbound features to see this, not
# fold a literal constant the way a `1 == 2` contradiction would.
COMPANION_NEGATIVE = """
package ConservationCheckBroken {
    private import ScalarValues::*;
    private import SI::*;
    private import ISQ::*;
    private import MeasurementReferences::*;

    abstract part def HeatGenerator {
        attribute power : ISQ::PowerValue;
        attribute efficiency : DimensionOneValue;
    }
    part heatGenCheck : HeatGenerator;
    attribute heatGenCheckDuration : ISQ::DurationValue;

    assert constraint deliveredEnergyExceedsSupply {
        (heatGenCheck.efficiency >= 0.0 and heatGenCheck.efficiency <= 1.0
         and heatGenCheck.power >= 0.0 [SI::W] and heatGenCheckDuration >= 0.0 [SI::s])
        and (heatGenCheck.power * heatGenCheckDuration * heatGenCheck.efficiency)
            > heatGenCheck.power * heatGenCheckDuration
    }
}
"""


def _write(tmp_path: Path, name: str, content: str) -> str:
    p = tmp_path / name
    p.write_text(content)
    return str(p)


@pytest.fixture(scope="module")
def conn():
    c = opensysml.connect(version="v0.9.0")
    yield c
    c.close()


def test_construct_is_in_the_committed_fixture(conn) -> None:
    """`deliveredEnergyBoundedBySupply` is a real, committed element of
    `models/ch08-cumulative.sysml`, not only of the companion restatement used to run
    `verify_holds` (F4: a property checked by a formal engine must be in the model to be
    checkable)."""
    source = (ROOT / "models" / "ch08-cumulative.sysml").read_text()
    model = conn.load_from_content(source, strict=False)
    assert model.ok

    sym = model.find("ToasterDemo::deliveredEnergyBoundedBySupply")
    assert sym is not None

    named = [
        e.as_dict()["qualifiedName"]
        for e in model.query()
        if e.as_dict().get("@type") == "ConstraintUsage"
    ]
    assert "ToasterDemo::deliveredEnergyBoundedBySupply" in named


def test_conservation_entailment_proved_for_all_values(tmp_path) -> None:
    """verify_holds proves the entailment holds for every value of efficiency, power and
    duration the companion's unbound features admit, not merely at one point."""
    f = _write(tmp_path, "conservation.sysml", COMPANION_POSITIVE)
    verdicts = mc.verify_holds(f, lib=str(LIB), binary=str(BINARY), solve=True)
    assert len(verdicts) == 1
    v = verdicts[0]
    assert v.element == "deliveredEnergyBoundedBySupply"
    assert v.status == "satisfied"
    assert "z3" in v.reason
    assert mc.holds(f, lib=str(LIB), binary=str(BINARY), solve=True) is True


def test_broken_entailment_reported_violated(tmp_path) -> None:
    """DL-047's negative control: a genuinely broken variant of the same shape (Z3 must
    resolve a product of three bounded unbound features, not fold a constant) is reported
    violated, not undecided and not silently accepted."""
    f = _write(tmp_path, "conservation_broken.sysml", COMPANION_NEGATIVE)
    verdicts = mc.verify_holds(f, lib=str(LIB), binary=str(BINARY), solve=True)
    assert len(verdicts) == 1
    v = verdicts[0]
    assert v.element == "deliveredEnergyExceedsSupply"
    assert v.status == "violated"
    assert "unsatisfiable" in v.reason
    assert mc.holds(f, lib=str(LIB), binary=str(BINARY), solve=True) is False


def test_real_cumulative_file_trips_the_satisfy_line_parsing_gap(conn) -> None:
    """DEFERRED.md D-029: the real, committed `ch08-cumulative.sysml` carries forward
    `assert satisfy` / `assert not satisfy` declarations from Chapter 3 and Chapter 6, so
    `verify_holds` cannot yet run directly against it; this is why the chapter's own
    notebook and the tests above use a companion restatement instead. This test pins the
    gap down so a future fix to the parser is verified against a real regression, not
    just against the small fixtures in `tests/test_modelcheck.py`."""
    source = (ROOT / "models" / "ch08-cumulative.sysml").read_text()
    assert "assert not satisfy timely by slow" in source
    with pytest.raises(mc.ModelCheckError, match="could not parse verdict line"):
        mc.verify_holds(
            str(ROOT / "models" / "ch08-cumulative.sysml"),
            lib=str(LIB),
            binary=str(BINARY),
            solve=True,
        )
