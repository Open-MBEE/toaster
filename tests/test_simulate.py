"""WP-5 targeted tests: sweep_1d and check_stale."""
import numpy as np
import sympy as sp
import pytest

from toaster.simulate import sweep_1d
from toaster.evidence import ReviewRecord, hash_content, check_stale, validate_record


# ── sweep_1d ─────────────────────────────────────────────────────────────────

def _make_q_fn():
    P, t, eta = sp.symbols("P t eta", positive=True)
    return sp.lambdify([P, t, eta], P * t * eta, "numpy")


def test_sweep_1d_reference_value():
    Q_fn = _make_q_fn()
    ref = float(Q_fn(800.0, 120.0, 0.7))
    assert abs(ref - 67200.0) < 1.0


def test_sweep_1d_produces_array():
    Q_fn = _make_q_fn()
    P_vals = np.linspace(500, 1200, 50)
    Q_vals = sweep_1d(Q_fn, P_vals, t=120.0, eta=0.7)
    assert isinstance(Q_vals, np.ndarray)
    assert Q_vals.shape == (50,)


def test_sweep_1d_monotone():
    """Delivered energy is monotone in power at fixed t and eta."""
    Q_fn = _make_q_fn()
    P_vals = np.linspace(500, 1200, 50)
    Q_vals = sweep_1d(Q_fn, P_vals, t=120.0, eta=0.7)
    assert all(Q_vals[i] < Q_vals[i + 1] for i in range(len(Q_vals) - 1))


def test_sweep_1d_threshold_crossing():
    Q_fn = _make_q_fn()
    P_vals = np.linspace(500, 1200, 50)
    Q_vals = sweep_1d(Q_fn, P_vals, t=120.0, eta=0.7)
    threshold = 50_000.0
    crossings = P_vals[Q_vals >= threshold]
    assert len(crossings) > 0, "No power value meets the 50 kJ threshold"
    assert crossings[0] < 700.0, "Threshold should be crossed well below 700 W"


# ── check_stale ───────────────────────────────────────────────────────────────

SOURCE_A = "package T { private import ScalarValues::*; part def X { attribute v : Real default = 5.0; } }"
SOURCE_B = SOURCE_A.replace("5.0", "10.0")


def _make_record(source: str) -> ReviewRecord:
    return ReviewRecord(
        identifier="TS-01",
        kind="asserted_solution",
        claim="X.v satisfies the threshold.",
        model_ref="T::X",
        content_hash=hash_content(source),
        scope="T",
        criteria="X.v >= 3.0",
        rationale="X.v=5.0 is above the threshold of 3.0.",
        counterevidence="This only checks the default attribute value.",
        record_kind="worked_example",
    )


def test_check_stale_current():
    r = _make_record(SOURCE_A)
    assert not check_stale(r, SOURCE_A)


def test_check_stale_after_change():
    r = _make_record(SOURCE_A)
    assert check_stale(r, SOURCE_B)


def test_validate_record_clean():
    r = _make_record(SOURCE_A)
    assert validate_record(r) == []


def test_validate_record_empty_identifier():
    r = _make_record(SOURCE_A)
    r.identifier = ""
    errors = validate_record(r)
    assert any("identifier" in e for e in errors)


def test_validate_record_asserted_inference_requires_premises():
    r = _make_record(SOURCE_A)
    r.kind = "asserted_inference"
    r.premises = []
    errors = validate_record(r)
    assert any("premise" in e.lower() for e in errors)


def test_validate_record_inference_with_premises_ok():
    r = _make_record(SOURCE_A)
    r.kind = "asserted_inference"
    r.premises = ["AS-C03"]
    assert validate_record(r) == []
