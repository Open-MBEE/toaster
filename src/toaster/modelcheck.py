"""Wrapper around sysml-toolkit's `sysmlv2 verify --solve` CLI (DEFERRED.md D-025, decisions/log.md DL-046).

sysml-toolkit's Python binding (`sysmlv2.Session`) has no `verify`/`solve` method: only the Rust CLI
(`sysmlv2 verify --solve`) proves a constraint holds for all values of an unbound feature via Z3. This
module shells out to that CLI and parses its stable text output into `ConstraintVerdict` values, so a
chapter notebook sees a plain Python function call (`verify_holds(...)`) and never a subprocess. Per Z's
ruling this is a toolchain patch, intended for deletion once sysml-toolkit's Python binding (or OpenSysML)
exposes the capability natively (D-025).

The CLI's exact text format (verified directly against the real binary, not assumed):

    <file>:<line>:<col>  <name-or-"<anonymous>"> (<Kind>): <status>[ (<reason>)][ — <extra>]
    N satisfied, N violated, N undecided

`<Kind>` (e.g. "ConstraintUsage", "AssertConstraintUsage") is parsed but not part of `ConstraintVerdict`,
which has no field for it. `status` is printed by the CLI as `satisfied`, `VIOLATED` or `undecided`;
this module lowercases it to match the three values this module's own API promises. Not every verdict
line carries a parenthetical reason (a trivially-decided `satisfied`/`VIOLATED` has none at all), and a
`--solve` run that leaves a constraint `undecided` while finding a witness prints a second segment after
an em dash, outside the first parenthetical (e.g. `undecided (result is indeterminate over unbound
features) — z3: satisfiable, e.g. t.w = 1`) rather than folding "z3: " into a single reason as one
might assume without checking. This module's `reason` is that trailing text verbatim (parens of the first
group stripped, any dash-appended segment kept), or `""` when the CLI printed none.

With `--ranges`, the summary line is not always the last line of stdout: whenever interval propagation
actually narrows a feature, a trailing `narrowed ranges:` report follows it (verified directly, not
assumed). This module locates the summary line by scanning backward for it rather than indexing the
last line, and ignores anything after it.
"""

from __future__ import annotations

import os
import re
import signal
import subprocess
from dataclasses import dataclass

_LINE_RE = re.compile(
    r"^(?P<file>.+):(?P<line>\d+):(?P<col>\d+)  (?P<name>.+) \((?P<kind>\w+)\): "
    r"(?P<status>satisfied|VIOLATED|undecided)"
    r"(?: \((?P<reason1>[^)]*)\))?"
    r"(?: — (?P<reason2>.*))?$"
)
_SUMMARY_RE = re.compile(
    r"^(?P<satisfied>\d+) satisfied, (?P<violated>\d+) violated, (?P<undecided>\d+) undecided$"
)


class ModelCheckError(Exception):
    """Raised when the CLI itself could not produce a verdict: missing binary, bad --lib path, or a
    parse the CLI rejects (e.g. a syntax error in the model). Never raised for a normal violated
    outcome, which is a `ConstraintVerdict` with status "violated", not an exception."""


class ModelCheckTimeoutError(ModelCheckError):
    """Raised when the CLI subprocess did not finish within `timeout` seconds."""


class ModelCheckInconclusiveError(ModelCheckError):
    """Raised by `holds()` when there is nothing decided to report either way: no constraints were
    found to check at all (an empty verdict list would otherwise read as vacuously True), or there is
    at least one "undecided" verdict and no "violated" one. See `holds()`'s docstring for the full
    satisfied/violated/undecided precedence."""


@dataclass(frozen=True)
class ConstraintVerdict:
    element: str  # e.g. "c" or "<anonymous>", from the CLI's own naming
    location: str  # "file:line:col" as the CLI reports it
    status: str  # "satisfied" | "violated" | "undecided"
    reason: str  # the CLI's trailing text for this verdict, or "" if it printed none


def _resolve_binary(binary: str | None) -> str:
    if binary:
        return binary
    env_binary = os.environ.get("SYSMLV2_BINARY")
    if env_binary:
        return env_binary
    raise ModelCheckError(
        "no sysmlv2 binary given: pass binary=... or set the SYSMLV2_BINARY "
        "environment variable to the sysmlv2 executable's path (it is a local "
        "build artifact, not installed on PATH)"
    )


def _resolve_lib(lib: str | None) -> str | None:
    if lib:
        return lib
    return os.environ.get("SYSMLV2_LIB_DIR") or None


def _parse_output(verdict_lines: list[str]) -> list[ConstraintVerdict]:
    """Parse the verdict lines that precede the summary line (the caller has already located and
    stripped the summary line, and anything after it — see `verify_holds`'s `--ranges` note)."""
    verdicts = []
    for line in verdict_lines:
        m = _LINE_RE.match(line)
        if not m:
            raise ModelCheckError(f"could not parse verdict line {line!r}")
        reason1 = m.group("reason1") or ""
        reason2 = m.group("reason2")
        # Kept verbatim, both segments joined with " — ", rather than split further (OQ-1, deliberate,
        # not an oversight): the CLI also has a fourth shape, a ";"-joined single parenthetical with no
        # em dash at all, which a rule splitting on "reason1 vs reason2" alone cannot represent without
        # becoming fragile. Lossless is the right default for a wrapper intended for deletion (D-025).
        reason = f"{reason1} — {reason2}" if reason2 else reason1
        verdicts.append(
            ConstraintVerdict(
                element=m.group("name"),
                location=f"{m.group('file')}:{m.group('line')}:{m.group('col')}",
                status=m.group("status").lower(),
                reason=reason,
            )
        )
    return verdicts


def verify_holds(
    *sysml_files: str,
    lib: str | None = None,
    solve: bool = True,
    ranges: bool = False,
    binary: str | None = None,
    z3: str | None = None,
    timeout: float = 30,
) -> list[ConstraintVerdict]:
    """Run sysml-toolkit's `verify` over the given SysML file(s) and return one `ConstraintVerdict` per
    constraint/requirement/invariant body found, parsed from the CLI's text output.

    `binary`: path to the sysmlv2 executable. Resolution order: explicit arg, then SYSMLV2_BINARY env
      var, then a clear `ModelCheckError` (never silently searched on PATH or guessed).
    `lib`: path to the standard library directory (sysml.library). Resolution order: explicit arg, then
      SYSMLV2_LIB_DIR env var, then omitted from the CLI call (matches the CLI's own `--lib` being
      optional).
    `solve`: pass --solve to the CLI (default True: bounded proof via Z3, the point of this wrapper).
    `ranges`: pass --ranges (interval propagation). Both can be combined per the CLI's own semantics.
    `z3`: path to the z3 binary, forwarded as --z3 if given.
    `timeout`: seconds before killing the subprocess; raises `ModelCheckTimeoutError` naming the command
      on expiry, not a raw `subprocess.TimeoutExpired`.

    Raises `ModelCheckError` if the binary is missing/not found, if `--lib` names a path the CLI cannot
    load, or if the CLI rejects the model outright (e.g. a syntax error) — in each of those cases stdout
    has no parseable verdict/summary shape, and the CLI's stderr is included in the message. Exiting 1
    because a constraint was violated is a normal outcome carried in the returned verdicts, not raised.
    """
    resolved_binary = _resolve_binary(binary)
    resolved_lib = _resolve_lib(lib)
    command = [resolved_binary, "verify", *sysml_files]
    if resolved_lib:
        command += ["--lib", resolved_lib]
    if solve:
        command.append("--solve")
    if ranges:
        command.append("--ranges")
    if z3:
        command += ["--z3", z3]

    # start_new_session=True makes this process (and anything it forks, e.g. a z3 subprocess) the
    # leader of its own process group, so a timeout can kill the whole group instead of leaving a
    # grandchild orphaned and running (D-025/F5). subprocess.run()'s own TimeoutExpired handling only
    # kills the immediate child and does not expose its pid to us, so the process is managed by hand
    # with Popen here instead of subprocess.run.
    try:
        proc_cm = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
    except (FileNotFoundError, PermissionError, NotADirectoryError) as exc:
        raise ModelCheckError(
            f"sysmlv2 binary not found or not runnable at {resolved_binary!r} (from "
            f"{'binary=...' if binary else 'SYSMLV2_BINARY'}): {exc}"
        ) from exc

    with proc_cm as proc:
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except ProcessLookupError:
                pass  # already exited between the timeout firing and us getting here
            proc.wait()  # reap the process now that its group has been killed
            raise ModelCheckTimeoutError(
                f"`{' '.join(command)}` did not finish within {timeout}s"
            ) from exc
        returncode = proc.returncode

    lines = stdout.splitlines()
    # The summary line is not always the last line of stdout: with --ranges, a "narrowed ranges:"
    # report trails it whenever any feature actually narrowed (verified against the real CLI — not
    # assumed), so this searches backward for the last line matching the summary shape rather than
    # indexing lines[-1]. A verdict line can never itself match `_SUMMARY_RE` (it always starts with a
    # file path, not a bare digit), so this is unambiguous.
    summary_idx = next(
        (i for i in range(len(lines) - 1, -1, -1) if _SUMMARY_RE.match(lines[i])), None
    )
    if summary_idx is None:
        # No parseable verdict/summary shape in stdout: the CLI rejected the model or the call itself
        # (bad --lib, syntax error), not a normal "some constraint violated" outcome (which still prints
        # a full verdict list and a summary line, just with exit code 1).
        raise ModelCheckError(
            f"`{' '.join(command)}` exited {returncode} without a parseable "
            f"verdict: {stderr.strip() or '(no stderr)'}"
        )
    summary_match = _SUMMARY_RE.match(lines[summary_idx])

    # A parseable summary line alone is not enough to trust: it could arrive alongside an unrelated
    # CLI error. Only exit 0 (clean run) or exit 1 with at least one violation (the CLI's own signal
    # for "a constraint failed") are accepted; and the number of verdict lines actually parsed must
    # match the summary's own declared total, or something is inconsistent between the two and neither
    # should be trusted silently.
    satisfied = int(summary_match.group("satisfied"))
    violated = int(summary_match.group("violated"))
    undecided = int(summary_match.group("undecided"))
    total = satisfied + violated + undecided
    if not (returncode == 0 or (returncode == 1 and violated > 0)):
        raise ModelCheckError(
            f"`{' '.join(command)}` printed a parseable summary line but exited "
            f"{returncode}, which is not a trustworthy combination (clean exit, or exit 1 "
            f"with a violation): stdout:\n{stdout}\nstderr:\n{stderr}"
        )
    verdicts = _parse_output(lines[:summary_idx])
    if len(verdicts) != total:
        raise ModelCheckError(
            f"`{' '.join(command)}` summary line declares {total} verdict(s) "
            f"({satisfied} satisfied, {violated} violated, {undecided} undecided) but "
            f"{len(verdicts)} verdict line(s) were parsed: stdout:\n{stdout}\nstderr:\n{stderr}"
        )
    return verdicts


def holds(*sysml_files: str, **kwargs) -> bool:
    """Reduces `verify_holds(...)`'s verdicts to a single bool, or raises when there is nothing decided
    to report. Precedence, checked in this order: violated > undecided > satisfied.

    - If there are no verdicts at all (no constraints found to check), raises
      `ModelCheckInconclusiveError`: nothing was verified, so nothing can be reported as holding. An
      empty list must never read as vacuously True.
    - Else if ANY verdict is "violated", returns False — regardless of any undecided verdicts also
      present. A definite violation is a definite failure; it is never hidden behind "unproven".
    - Else if any verdict is "undecided" (and none are "violated"), raises
      `ModelCheckInconclusiveError`: an unproven property is not something a learner should read as
      "passed".
    - Else (every verdict is "satisfied"), returns True.
    """
    verdicts = verify_holds(*sysml_files, **kwargs)
    if not verdicts:
        raise ModelCheckInconclusiveError(
            "no constraints were found to check: nothing was verified, so nothing can be "
            "reported as holding"
        )
    violated = [v for v in verdicts if v.status == "violated"]
    if violated:
        return False
    undecided = [v for v in verdicts if v.status == "undecided"]
    if undecided:
        names = ", ".join(f"{v.element} ({v.location})" for v in undecided)
        raise ModelCheckInconclusiveError(
            f"undecided, not proven either way: {names}"
        )
    return all(v.status == "satisfied" for v in verdicts)
