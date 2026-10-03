#!/usr/bin/env python3
"""Pre-flight: check required tool versions before running the tutorial.

Reports where each external tool resolves (via `toaster.tools`) and its version, then runs the
OpenSysML pre-flight (`toaster.bootstrap.provision`: checks `dot`, downloads the OpenSysML binaries).
Exits non-zero, naming `scripts/provision-tools.py`, if any tool cannot be resolved.
"""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

from toaster import tools
from toaster.bootstrap import provision


def _first_line(cmd: list[str]) -> str:
    """First non-empty line of a command's stdout or stderr (java prints its version on stderr)."""
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError(f"`{' '.join(cmd)}` failed: {exc}") from exc
    lines = [ln.strip() for ln in (done.stdout + "\n" + done.stderr).splitlines() if ln.strip()]
    if done.returncode != 0:
        # e.g. the macOS /usr/bin/java stub, which is on PATH and executable but is not a JRE
        raise RuntimeError(f"`{' '.join(cmd)}` exited {done.returncode}: {lines[0] if lines else 'no output'}")
    return lines[0] if lines else "(no version output)"


def _library_version(path: Path) -> str:
    return "Systems Library present" if (path / "Systems Library").is_dir() else "(no Systems Library)"


def report_tools(echo: Callable[[str], None] = print) -> bool:
    """Print each resolved tool and its version; return True if every tool resolved."""
    ok = True
    java: Path | None = None
    checks: list[tuple[str, Callable[[], Path], Callable[[Path], str]]] = [
        ("sysmlv2", tools.resolve_sysmlv2, lambda p: _first_line([str(p), "--version"])),
        ("sysml.library", tools.resolve_library, _library_version),
        ("z3", tools.resolve_z3, lambda p: _first_line([str(p), "--version"])),
        ("java", tools.resolve_java, lambda p: _first_line([str(p), "-version"])),
    ]
    for name, resolve, version in checks:
        try:
            path = resolve()
        except tools.ToolNotFoundError as exc:
            ok = False
            echo(f"{name}: MISSING -- {exc}")
            continue
        if name == "java":
            java = path
        try:
            echo(f"{name}: {path}  [{version(path)}]")
        except RuntimeError as exc:
            ok = False
            java = None if name == "java" else java
            echo(f"{name}: BROKEN -- {path}: {exc}")
    try:
        jar = tools.resolve_plantuml_jar()
    except tools.ToolNotFoundError as exc:
        ok = False
        echo(f"plantuml jar: MISSING -- {exc}")
    else:
        try:
            detail = _first_line([str(java), "-jar", str(jar), "-version"]) if java else "(needs a working java to report a version)"
        except RuntimeError as exc:
            ok = False
            detail = f"BROKEN: {exc}"
        echo(f"plantuml jar: {jar}  [{detail}]")
    return ok


if __name__ == "__main__":
    tools_ok = report_tools()
    provision()
    if not tools_ok:
        print("Some tools are missing or broken. Provision them with: uv run python scripts/provision-tools.py")
        sys.exit(1)
    print("All tools verified.")
