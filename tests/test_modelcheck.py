"""src/toaster/modelcheck.py: parses real sysml-toolkit `verify` CLI output (DEFERRED.md D-025, DL-046).

Every test here runs the real `sysmlv2` binary — this module's whole job is correctly parsing real CLI
output, so mocking the subprocess would test nothing. `BINARY`/`LIB` point at the local build described in
the work contract; if they are not present on this machine, that is itself something to report, not paper
over.
"""

import os
import time
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

# Structure only, no constraint/requirement/invariant body at all (PASS2-012 F1).
ZERO_CONSTRAINTS = """
package P {
  part def T;
}
"""

# One of each status together (PASS2-012 F4/F2): "ok" trivially satisfied, "bad" a constant-fold
# contradiction (VIOLATED, no z3 needed), "unsure" unbound and left undecided (with a z3 witness).
MIXED_STATUSES = """
package P {
  private import ScalarValues::*;
  constraint ok { true }
  constraint bad { 1 == 2 }
  part def Toaster {
    attribute w : Real;
  }
  part t : Toaster;
  constraint unsure { t.w > 0 }
}
"""

# Genuinely unsatisfiable over an unbound feature (not a constant-fold contradiction like
# MIXED_STATUSES's "bad"): z3 must prove no value of cycleTime can ever make this hold (PASS2-012 F2).
Z3_VIOLATED = """
package P {
  private import ScalarValues::*;
  part def Toaster {
    attribute cycleTime : Real;
  }
  part t : Toaster;
  constraint c { t.cycleTime > t.cycleTime + 1.0 }
}
"""

# Interval-propagation-resolved case (CLI.md "--ranges — interval propagation" example, reproduced
# verbatim): z3 is never invoked, --ranges alone narrows wingSpan to prove span_lo/span_hi satisfied
# and count's domain to prove bad VIOLATED (PASS2-012 F2). Deliberately uses no --lib, matching the
# CLI.md example (ScalarValues isn't needed for `attribute def Real`/`attribute def Integer`).
PROPAGATION_DEMO = """
package Demo {
    attribute def Real;
    attribute def Integer;
    attribute wingSpan : Real;
    attribute count : Integer;

    assert constraint span_lo { wingSpan >= 10 }
    assert constraint span_hi { wingSpan <= 200 }
    assert constraint bad { count > 5 & count < 4 }
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


def test_witness_but_undecided_reason_has_both_segments(tmp_path):
    """PASS2-012 F2/OQ-1: with --solve, an unbound feature with no other constraint on it is left
    undecided but z3 can still exhibit a witness — the CLI prints this as two segments (the base
    "indeterminate" text, then an em-dash-joined witness), and `reason` keeps both verbatim (OQ-1)."""
    f = _write(tmp_path, "undetermined.sysml", UNDETERMINED)
    verdicts = mc.verify_holds(f, lib=str(LIB), binary=str(BINARY), solve=True)
    assert len(verdicts) == 1
    v = verdicts[0]
    assert v.status == "undecided"
    assert "indeterminate over unbound features" in v.reason
    assert "z3: satisfiable" in v.reason


def test_z3_resolved_violated_not_constant_fold(tmp_path):
    """PASS2-012 F2: a VIOLATED verdict z3 had to actually resolve (unsatisfiable over an unbound
    feature), distinct from CONTRADICTION's `1 == 2`, which is a trivial constant fold needing no z3."""
    f = _write(tmp_path, "z3_violated.sysml", Z3_VIOLATED)
    verdicts = mc.verify_holds(f, lib=str(LIB), binary=str(BINARY), solve=True)
    assert len(verdicts) == 1
    v = verdicts[0]
    assert v.status == "violated"
    assert "z3" in v.reason
    assert "unsatisfiable" in v.reason


def test_propagation_resolved_case(tmp_path):
    """PASS2-012 F2: interval propagation (--ranges) alone resolves every verdict here, without z3 —
    also exercises stdout's trailing "narrowed ranges:" report (present whenever --ranges narrows a
    feature), which trails the summary line rather than being the last line of stdout."""
    f = _write(tmp_path, "propagation.sysml", PROPAGATION_DEMO)
    verdicts = mc.verify_holds(f, binary=str(BINARY), solve=False, ranges=True)
    assert len(verdicts) == 3
    by_name = {v.element: v for v in verdicts}
    assert by_name["span_lo"].status == "satisfied"
    assert "propagation:" in by_name["span_lo"].reason
    assert by_name["span_hi"].status == "satisfied"
    assert "propagation:" in by_name["span_hi"].reason
    assert by_name["bad"].status == "violated"
    assert "propagation:" in by_name["bad"].reason


def test_multiple_statuses_together(tmp_path):
    """PASS2-012 F2/F4: a file with satisfied, violated and undecided verdicts together, reused by the
    holds() precedence test below."""
    f = _write(tmp_path, "mixed.sysml", MIXED_STATUSES)
    verdicts = mc.verify_holds(f, lib=str(LIB), binary=str(BINARY), solve=True)
    assert len(verdicts) == 3
    statuses = {v.status for v in verdicts}
    assert statuses == {"satisfied", "violated", "undecided"}


def test_missing_binary_raises_modelcheckerror(tmp_path):
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    with pytest.raises(mc.ModelCheckError):
        mc.verify_holds(f, lib=str(LIB), binary="/nonexistent/path/to/sysmlv2")


def test_non_executable_binary_raises_modelcheckerror(tmp_path):
    not_executable = tmp_path / "not_a_binary.sh"
    not_executable.write_text("#!/bin/sh\necho hi\n")  # no chmod +x
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    with pytest.raises(mc.ModelCheckError):
        mc.verify_holds(f, lib=str(LIB), binary=str(not_executable))


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


def test_summary_line_with_wrong_exit_code_raises(tmp_path):
    """PASS2-012 F3: a fake binary (not the real one — this is about the wrapper's own disambiguation
    logic, not CLI text parsing) that prints a well-formed, internally-consistent summary line but
    exits with a code that is neither 0 nor "1 with a violation" must not be trusted."""
    script = tmp_path / "fake_wrong_exit.sh"
    script.write_text(
        "#!/bin/sh\n"
        'echo "somefile.sysml:1:1  c (ConstraintUsage): satisfied"\n'
        'echo "1 satisfied, 0 violated, 0 undecided"\n'
        "exit 2\n"
    )
    script.chmod(0o755)
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    with pytest.raises(mc.ModelCheckError) as exc_info:
        mc.verify_holds(f, binary=str(script))
    assert "exited 2" in str(exc_info.value)


def test_exit_1_with_zero_violated_raises(tmp_path):
    """PASS2-012 F3, closing the N1 gap: the other half of the disambiguation. A fake binary that
    exits 1 (which the CLI otherwise uses to mean "a constraint was violated") but whose own
    summary line declares zero violated must not be trusted either — exit 1 alone isn't enough;
    it must be exit 1 together with violated > 0."""
    script = tmp_path / "fake_exit1_no_violation.sh"
    script.write_text(
        "#!/bin/sh\n"
        'echo "somefile.sysml:1:1  c (ConstraintUsage): undecided (z3: satisfiable, e.g. x = 1)"\n'
        'echo "0 satisfied, 0 violated, 1 undecided"\n'
        "exit 1\n"
    )
    script.chmod(0o755)
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    with pytest.raises(mc.ModelCheckError) as exc_info:
        mc.verify_holds(f, binary=str(script))
    assert "exited 1" in str(exc_info.value)


def test_summary_line_verdict_count_mismatch_raises(tmp_path):
    """PASS2-012 F3: a fake binary whose summary line's declared total does not match the number of
    verdict lines actually parsed must not be trusted, even though the exit code looks fine."""
    script = tmp_path / "fake_count_mismatch.sh"
    script.write_text(
        "#!/bin/sh\n"
        'echo "somefile.sysml:1:1  c (ConstraintUsage): satisfied"\n'
        'echo "2 satisfied, 0 violated, 0 undecided"\n'
        "exit 0\n"
    )
    script.chmod(0o755)
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)
    with pytest.raises(mc.ModelCheckError) as exc_info:
        mc.verify_holds(f, binary=str(script))
    assert "2 verdict(s)" in str(exc_info.value)
    assert "1 verdict line(s) were parsed" in str(exc_info.value)


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


def test_timeout_kills_process_group_no_lingering_child(tmp_path):
    """PASS2-012 F5: the timed-out process is run in its own process group (start_new_session=True) and
    that whole group is killed, not just the immediate process — so a grandchild (standing in for an
    orphaned z3) does not survive the timeout. Best-effort: polls briefly for the child to actually
    disappear rather than asserting it is gone the instant the exception is raised."""
    pidfile = tmp_path / "child.pid"
    script = tmp_path / "slow_with_child.sh"
    script.write_text(
        "#!/bin/sh\n"
        "sleep 5 &\n"
        "echo $! > " + str(pidfile) + "\n"
        "wait\n"
    )
    script.chmod(0o755)
    f = _write(tmp_path, "tautology.sysml", TAUTOLOGY)

    with pytest.raises(mc.ModelCheckTimeoutError):
        mc.verify_holds(f, binary=str(script), timeout=0.5)

    # Give the grandchild's pid file a moment to appear (it's written right at process start, well
    # before our 0.5s timeout, but process creation isn't instantaneous — observed empirically to need
    # more slack than the plain-timeout test above, which does no forking of its own).
    for _ in range(20):
        if pidfile.exists():
            break
        time.sleep(0.05)
    assert pidfile.exists(), "fake binary never wrote the child pid file"
    child_pid = int(pidfile.read_text().strip())

    # Poll for the child to actually exit; SIGKILL delivery isn't instantaneous either.
    child_alive = True
    for _ in range(20):
        try:
            os.kill(child_pid, 0)
        except ProcessLookupError:
            child_alive = False
            break
        time.sleep(0.05)
    assert not child_alive, f"child process {child_pid} survived the timeout (orphaned, not killed)"


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


def test_holds_raises_inconclusive_for_zero_constraints(tmp_path):
    """PASS2-012 F1: a structure-only file with no constraint bodies at all yields zero verdicts.
    holds() must not read an empty verdict list as vacuously True — nothing was verified, so nothing
    can be reported as holding."""
    f = _write(tmp_path, "zero.sysml", ZERO_CONSTRAINTS)
    with pytest.raises(mc.ModelCheckInconclusiveError):
        mc.holds(f, lib=str(LIB), binary=str(BINARY), solve=True)


def test_holds_false_for_mixed_violated_and_undecided(tmp_path):
    """PASS2-012 F4: a definite VIOLATED must win over an undecided verdict — holds() returns False,
    not ModelCheckInconclusiveError, when the verdicts are a mix of satisfied, violated and undecided
    together (MIXED_STATUSES has one of each)."""
    f = _write(tmp_path, "mixed.sysml", MIXED_STATUSES)
    assert mc.holds(f, lib=str(LIB), binary=str(BINARY), solve=True) is False


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
