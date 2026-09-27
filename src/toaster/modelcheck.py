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
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass

_LINE_RE = re.compile(
    r"^(?P<file>.+):(?P<line>\d+):(?P<col>\d+)  (?P<name>.+) \((?P<kind>\w+)\): "
    r"(?P<status>satisfied|VIOLATED|undecided)"
    r"(?: \((?P<reason1>[^)]*)\))?"
    r"(?: — (?P<reason2>.*))?$"
)
_SUMMARY_RE = re.compile(r"^\d+ satisfied, \d+ violated, \d+ undecided$")


class ModelCheckError(Exception):
    """Raised when the CLI itself could not produce a verdict: missing binary, bad --lib path, or a
    parse the CLI rejects (e.g. a syntax error in the model). Never raised for a normal violated
    outcome, which is a `ConstraintVerdict` with status "violated", not an exception."""


class ModelCheckTimeoutError(ModelCheckError):
    """Raised when the CLI subprocess did not finish within `timeout` seconds."""


class ModelCheckInconclusiveError(ModelCheckError):
    """Raised by `holds()` when any verdict's status is "undecided": an unproven property, distinct
    from a "violated" result (which `holds()` returns False for, cleanly, not as an exception)."""


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


def _parse_output(stdout: str) -> list[ConstraintVerdict]:
    """Parse a stdout that already ends with a summary line (checked by the caller) into verdicts."""
    lines = stdout.splitlines()
    verdicts = []
    for line in lines[:-1]:
        m = _LINE_RE.match(line)
        if not m:
            raise ModelCheckError(f"could not parse verdict line {line!r}")
        reason1 = m.group("reason1") or ""
        reason2 = m.group("reason2")
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

    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout, check=False
        )
    except FileNotFoundError as exc:
        raise ModelCheckError(
            f"sysmlv2 binary not found at {resolved_binary!r} (from "
            f"{'binary=...' if binary else 'SYSMLV2_BINARY'}): {exc}"
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise ModelCheckTimeoutError(
            f"`{' '.join(command)}` did not finish within {timeout}s"
        ) from exc

    stdout = result.stdout
    lines = stdout.splitlines()
    if not lines or not _SUMMARY_RE.match(lines[-1]):
        # No parseable verdict/summary shape in stdout: the CLI rejected the model or the call itself
        # (bad --lib, syntax error), not a normal "some constraint violated" outcome (which still prints
        # a full verdict list and a summary line, just with exit code 1).
        raise ModelCheckError(
            f"`{' '.join(command)}` exited {result.returncode} without a parseable "
            f"verdict: {result.stderr.strip() or '(no stderr)'}"
        )
    return _parse_output(stdout)


def holds(*sysml_files: str, **kwargs) -> bool:
    """True only if every verdict's status is "satisfied". A "violated" verdict makes this return False
    cleanly, not an exception. Raises `ModelCheckInconclusiveError` if any verdict is "undecided": an
    unproven property is not something a learner should read as "passed"."""
    verdicts = verify_holds(*sysml_files, **kwargs)
    undecided = [v for v in verdicts if v.status == "undecided"]
    if undecided:
        names = ", ".join(f"{v.element} ({v.location})" for v in undecided)
        raise ModelCheckInconclusiveError(
            f"undecided, not proven either way: {names}"
        )
    return all(v.status == "satisfied" for v in verdicts)
