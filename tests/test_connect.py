"""WP-1: context manager lifecycle test."""

import opensysml

from toaster.connect import opensysml_session


def test_session_opens_and_closes():
    with opensysml_session(version="v0.9.0") as conn:
        model = conn.load_from_content("part def T;", strict=False)
        assert model.ok, f"Expected ok model inside session: {model.diagnostics}"
    # conn is closed after the with block; re-opening should still work
    with opensysml_session(version="v0.9.0") as conn2:
        model2 = conn2.load_from_content("part def U;", strict=False)
        assert model2.ok


def test_session_closes_on_error():
    """Context manager must close even when the body raises."""
    raised = False
    try:
        with opensysml_session(version="v0.9.0") as conn:
            _ = conn.load_from_content("part def T;", strict=False)
            raise RuntimeError("deliberate error")
    except RuntimeError:
        raised = True
    assert raised
    # If conn is closed, a new session should open cleanly
    with opensysml_session(version="v0.9.0") as conn3:
        m = conn3.load_from_content("part def V;", strict=False)
        assert m.ok
