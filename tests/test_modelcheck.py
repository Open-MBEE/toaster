"""src/toaster/modelcheck.py: parses real sysml-toolkit `verify` CLI output (DEFERRED.md D-025, DL-046).

Every test here runs the real `sysmlv2` binary — this module's whole job is correctly parsing real CLI
output, so mocking the subprocess would test nothing. `BINARY`/`LIB` point at the local build described in
the work contract; if they are not present on this machine, that is itself something to report, not paper
over.
"""

from pathlib import Path

import pytest

from toaster import modelcheck as mc

BINARY = Path.home() / "Documents/GitHub/sysml-toolkit/target/release/sysmlv2"
LIB = (
    Path.home()
    / "Documents/GitHub/sysml-toolkit/spec-refs/SysML-v2-Release/sysml.library"
)

pytestmark = pytest.mark.skipif(
    not BINARY.exists(),
    reason=f"sysmlv2 binary not found at {BINARY} (see work contract PASS2-012)",
)

TAUTOLOGY = """
package P {
  private import ScalarValues::*;
  constraint def AlwaysTrue { x : Real; }
  constraint c : AlwaysTrue { true }
}
"""

CONTRADICTION = """
package P {
  private import ScalarValues::*;
  constraint c { 1 == 2 }
}
"""

# Unbound feature, no binding at all: without --solve the CLI can only report "undecided".
UNDETERMINED = """
package P {
  private import ScalarValues::*;
  part def Toaster {
    attribute w : Real;
  }
  part t : Toaster;
  constraint c { t.w > 0 }
}
"""

# TimelyToast-shaped bounded-range example (decisions/probes.md, 2026-09-27 DL-046 probe correction):
# cycleTime is unbound; the constraint is a range implication that only Z3 can prove holds for every
# value of the unbound feature, not a value that is itself bound (which would make it a trivial fold).
TIMELY_TOAST = """
package P {
  private import ScalarValues::*;
  part def Toaster {
    attribute cycleTime : Real;
  }
  part t : Toaster;
  constraint c { (t.cycleTime >= 90.0 and t.cycleTime <= 150.0) implies t.cycleTime <= 180.0 }
}
"""

SYNTAX_ERROR = """
package P {
  this is not valid sysml @@@
}
"""


def _write(tmp_path: Path, name: str, content: str) -> str:
    p = tmp_path / name
    p.write_text(content)
    return str(p)


# --- verify_holds: parsing real CLI output ------------------------------------------------------------


def test_tautology_satisfied_with_solve(tmp_path):
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    verdicts = mc.verify_holds(f, lib=str(LIB), binary=str(BINARY), solve=True)
    assert len(verdicts) == 1
    v = verdicts[0]
    assert v.element == "c"
    assert v.location.startswith(f) and v.location.count(":") == 2
    assert v.status == "satisfied"


def test_contradiction_violated(tmp_path):
    f = _write(tmp_path, "contradiction.sysml", CONTRADICTION)
    verdicts = mc.verify_holds(f, lib=str(LIB), binary=str(BINARY), solve=True)
    assert len(verdicts) == 1
    v = verdicts[0]
    assert v.element == "c"
    assert v.status == "violated"


def test_underdetermined_without_solve_is_undecided(tmp_path):
    f = _write(tmp_path, "undetermined.sysml", UNDETERMINED)
    verdicts = mc.verify_holds(f, lib=str(LIB), binary=str(BINARY), solve=False)
    assert len(verdicts) == 1
    v = verdicts[0]
    assert v.status == "undecided"
    assert "indeterminate" in v.reason


def test_bounded_range_satisfied_with_solve(tmp_path):
    """Reproduces the TimelyToast-shaped example from decisions/probes.md: a range implication over an
    unbound feature that --solve proves holds for all values (Z3), where plain evaluation (no --solve)
    leaves it undecided."""
    f = _write(tmp_path, "timely.sysml", TIMELY_TOAST)

    unsolved = mc.verify_holds(f, lib=str(LIB), binary=str(BINARY), solve=False)
    assert len(unsolved) == 1
    assert unsolved[0].status == "undecided"

    solved = mc.verify_holds(f, lib=str(LIB), binary=str(BINARY), solve=True)
    assert len(solved) == 1
    v = solved[0]
    assert v.status == "satisfied"
    assert v.reason == "z3: holds for all values of unbound features"


def test_missing_binary_raises_modelcheckerror(tmp_path):
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    with pytest.raises(mc.ModelCheckError):
        mc.verify_holds(f, lib=str(LIB), binary="/nonexistent/path/to/sysmlv2")


def test_syntax_error_raises_modelcheckerror_with_stderr(tmp_path):
    f = _write(tmp_path, "syntax_error.sysml", SYNTAX_ERROR)
    with pytest.raises(mc.ModelCheckError) as exc_info:
        mc.verify_holds(f, lib=str(LIB), binary=str(BINARY))
    message = str(exc_info.value)
    assert "expected" in message  # the CLI's own stderr text is included


def test_bad_lib_path_raises_modelcheckerror(tmp_path):
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    with pytest.raises(mc.ModelCheckError) as exc_info:
        mc.verify_holds(f, lib="/nonexistent/lib/dir", binary=str(BINARY))
    assert "cannot load library" in str(exc_info.value)


def test_timeout_raises_modelcheck_timeout_error(tmp_path):
    """A slow fake binary, not the real one: this exercises the wrapper's own subprocess timeout
    handling, which has nothing to do with parsing real CLI text and would otherwise make this test
    depend on the real solver being slow (flaky)."""
    script = tmp_path / "slow_sysmlv2.sh"
    script.write_text("#!/bin/sh\nsleep 5\n")
    script.chmod(0o755)
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    with pytest.raises(mc.ModelCheckTimeoutError):
        mc.verify_holds(f, binary=str(script), timeout=0.2)


# --- holds() -------------------------------------------------------------------------------------------


def test_holds_true_for_satisfied(tmp_path):
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    assert mc.holds(f, lib=str(LIB), binary=str(BINARY), solve=True) is True


def test_holds_false_for_violated(tmp_path):
    f = _write(tmp_path, "contradiction.sysml", CONTRADICTION)
    assert mc.holds(f, lib=str(LIB), binary=str(BINARY), solve=True) is False


def test_holds_raises_inconclusive_for_undecided(tmp_path):
    f = _write(tmp_path, "undetermined.sysml", UNDETERMINED)
    with pytest.raises(mc.ModelCheckInconclusiveError):
        mc.holds(f, lib=str(LIB), binary=str(BINARY), solve=False)


# --- env var resolution ---------------------------------------------------------------------------------


def test_binary_env_var_resolution(tmp_path, monkeypatch):
    monkeypatch.setenv("SYSMLV2_BINARY", str(BINARY))
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    verdicts = mc.verify_holds(f, lib=str(LIB), solve=True)  # no binary= arg
    assert verdicts[0].status == "satisfied"


def test_lib_env_var_resolution(tmp_path, monkeypatch):
    monkeypatch.setenv("SYSMLV2_LIB_DIR", str(LIB))
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    verdicts = mc.verify_holds(f, binary=str(BINARY), solve=True)  # no lib= arg
    assert verdicts[0].status == "satisfied"


def test_no_binary_given_raises_clear_error(tmp_path, monkeypatch):
    monkeypatch.delenv("SYSMLV2_BINARY", raising=False)
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    with pytest.raises(mc.ModelCheckError, match="SYSMLV2_BINARY"):
        mc.verify_holds(f, lib=str(LIB))


# --- notebook-facing shape -------------------------------------------------------------------------------


def test_notebook_call_shape(tmp_path):
    """What a notebook cell actually calls: a plain Python function, no subprocess visible."""
    f = _write(tmp_path, "timely.sysml", TIMELY_TOAST)
    verdicts = mc.verify_holds(f, lib=str(LIB), binary=str(BINARY))
    assert all(v.status in ("satisfied", "violated", "undecided") for v in verdicts)
