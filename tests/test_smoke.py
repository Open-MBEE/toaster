"""WP-0 smoke test: binary provision + probe reference value + allocate/flow extension."""

import opensysml
import opensysml.binary

from toaster.bootstrap import provision


def test_smoke():
    provision()

    conn = opensysml.connect(version="v0.9.0")

    # basic parse
    model = conn.load_from_content("part def Smoke;", strict=False)
    assert model.ok, f"Basic parse failed: {model.diagnostics}"

    # probe reference value: Q = 800W × 120s × 0.7 = 67200 J
    probe_src = open("tests/fixtures/probe.sysml").read()
    model2 = conn.load_from_content(probe_src, strict=False)
    assert model2.ok, f"Probe load failed: {model2.diagnostics}"

    result = model2.eval("ToasterDemo::DeliveredEnergy(800.0, 120.0, 0.7)")
    assert abs(float(result) - 67200.0) < 1.0, f"Reference value wrong: {result}"

    # allocate and flow: same probe file includes constructs 11 and 12
    model3 = conn.load_from_content(probe_src, strict=False)
    assert model3.ok, f"Extended probe (allocate/flow) failed: {model3.diagnostics}"

    conn.close()
