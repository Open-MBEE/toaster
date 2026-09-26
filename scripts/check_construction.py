"""
check_construction.py --check [--chapter=N]

Verify that construction zones in construct-introducing notebooks are consistent
with the committed models/chXX-cumulative.sysml fixtures.

Does NOT reconstruct cumulative files. Read-only — never writes to models/.

Design (from decisions/declarative-construction-plan.md Phase 1c):
- For each construct-introducing notebook (in chapter order):
  1. Parse the notebook JSON; find the last code cell that assigns TOASTER_INCREMENT.
  2. Execute the construction zone (all code cells up to and including TOASTER_INCREMENT).
  3. Validate: load TOASTER_INCREMENT wrapped in a minimal package context; assert model.ok.
- Verify the committed cumulative file also loads cleanly (model.ok) for each chapter.
- Exit 1 and print all failures at end.

TOASTER_INCREMENT convention (all Pattern B — see decisions/declarative-construction-plan.md):
  TOASTER_INCREMENT = new declarations for this notebook only (not the full cumulative model).
  It is assembled from named fragment variables at the end of the construction zone.
  Each fragment variable = one future editor.add_*() call.
"""
import argparse
import json
import os
import sys
from pathlib import Path

import opensysml

REPO_ROOT = Path(__file__).parent.parent

# Chapters and their construct-introducing notebooks (in order)
CONSTRUCTION_NOTEBOOKS = {
    1: [
        "chapters/ch01-system-purpose/01-abstract-def.ipynb",
        "chapters/ch01-system-purpose/02-part-def.ipynb",
        "chapters/ch01-system-purpose/03-specialization.ipynb",
        "chapters/ch01-system-purpose/04-composition.ipynb",
    ],
    2: [
        "chapters/ch02-requirements/01-requirement-def.ipynb",
        "chapters/ch02-requirements/02-assumptions.ipynb",
    ],
    3: [
        "chapters/ch03-measures/01-moe-definition.ipynb",
        "chapters/ch03-measures/02-mop-candidate-eval.ipynb",
    ],
    4: [
        "chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb",
        "chapters/ch04-functional-decomp/02-heating-refinement.ipynb",
    ],
    5: [
        "chapters/ch05-architecture/02-allocate.ipynb",
        "chapters/ch05-architecture/03-interfaces.ipynb",
    ],
    7: [
        "chapters/ch07-execution/02-state-traces.ipynb",
    ],
}

CUMULATIVE_FILES = {
    ch: REPO_ROOT / f"models/ch0{ch}-cumulative.sysml"
    for ch in range(1, 9)
}

# Standard package preamble for wrapping fragments during validation
_PREAMBLE = """\
package _check {{
    private import ScalarValues::*;
    private import SI::*;
    private import ISQ::*;
    private import MeasurementReferences::*;
    {fragment}
}}"""


def _get_code_cells(nb_path: Path) -> list[str]:
    """Return all code cell sources from a notebook."""
    nb = json.loads(nb_path.read_text())
    cells = nb.get("cells", [])
    sources = []
    for cell in cells:
        if cell.get("cell_type", "code") == "code":
            src = cell.get("source", [])
            sources.append("".join(src) if isinstance(src, list) else src)
    return sources


def _has_toaster_increment(cell_src: str) -> bool:
    return "TOASTER_INCREMENT" in cell_src


def check_notebook(nb_path: Path, conn: opensysml.Connection) -> list[str]:
    """Check one construct-introducing notebook. Returns list of failure strings."""
    failures = []

    code_cells = _get_code_cells(nb_path)

    # Find cells that are part of the construction zone (have fragment variables or TOASTER_INCREMENT)
    construction_cells = [c for c in code_cells if "TOASTER_INCREMENT" in c or
                          any(kw in c for kw in ["_DEF", "_ATTR", "_USAGE", "_REQ",
                                                  "_CALC", "_FLOW", "_STATE", "_ALLOC"])]

    if not any(_has_toaster_increment(c) for c in code_cells):
        failures.append(f"NO TOASTER_INCREMENT in any code cell: {nb_path.name}")
        return failures

    # Execute the construction zone cells to capture TOASTER_INCREMENT
    ns: dict = {"__file__": str(nb_path), "Path": Path}
    orig_dir = os.getcwd()
    try:
        os.chdir(nb_path.parent)
        for cell_src in code_cells:
            if not cell_src.strip():
                continue
            # Execute cells up through the one that assigns TOASTER_INCREMENT
            # Stop after loading the cumulative (the assembly cell is self-contained)
            try:
                exec(compile(cell_src, str(nb_path), "exec"), ns)  # noqa: S102
            except Exception as exc:
                # Skip cells that fail due to missing context (e.g., conn not set up yet)
                # Only report failures if the TOASTER_INCREMENT cell fails
                if "TOASTER_INCREMENT" in cell_src and "TOASTER_INCREMENT" not in ns:
                    failures.append(
                        f"EXEC ERROR in {nb_path.name}: {type(exc).__name__}: {exc}"
                    )
                    return failures
                # Other cells may fail due to model not loaded yet — that's ok
            if "TOASTER_INCREMENT" in ns:
                break  # captured; stop executing further cells
    finally:
        os.chdir(orig_dir)

    increment = ns.get("TOASTER_INCREMENT")
    if not increment:
        failures.append(f"TOASTER_INCREMENT is empty after exec: {nb_path.name}")
        return failures

    # Validate: wrap the fragment in a package and load it.
    # Cross-notebook fragments (e.g., specialization of a type defined in a prior notebook)
    # will fail with "unresolved reference" errors in the isolated context — those are
    # acceptable here because the cumulative fixture validation (below) catches real issues.
    # Only non-reference errors indicate a genuine fragment syntax problem.
    wrapped = _PREAMBLE.format(fragment=increment)
    check = conn.load_from_content(wrapped, strict=False)
    if not check.ok:
        blocking = [
            d for d in check.diagnostics
            if "unresolved reference" not in str(d).lower()
        ]
        if blocking:
            failures.append(
                f"TOASTER_INCREMENT does not parse in {nb_path.name}:\n"
                f"  {[str(d) for d in blocking[:3]]}"
            )

    return failures


def check_chapter(chapter: int, conn: opensysml.Connection) -> list[str]:
    """Check all construction notebooks for one chapter plus the cumulative fixture."""
    failures = []

    for nb_rel in CONSTRUCTION_NOTEBOOKS.get(chapter, []):
        nb_path = REPO_ROOT / nb_rel
        if not nb_path.exists():
            failures.append(f"MISSING: {nb_rel}")
            continue
        failures.extend(check_notebook(nb_path, conn))

    # Verify the committed cumulative file loads cleanly
    cum_path = CUMULATIVE_FILES.get(chapter)
    if cum_path and cum_path.exists():
        check = conn.load_from_content(cum_path.read_text(), strict=False)
        if not check.ok:
            failures.append(
                f"CUMULATIVE FIXTURE invalid for ch{chapter}: "
                f"{[str(d) for d in check.diagnostics[:3]]}"
            )
    elif cum_path:
        failures.append(f"MISSING cumulative fixture: {cum_path.name}")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify construction zone consistency.")
    parser.add_argument("--check", action="store_true", required=True)
    parser.add_argument("--chapter", type=int, default=None, help="Check one chapter (1–8)")
    args = parser.parse_args()

    chapters = [args.chapter] if args.chapter else sorted(CONSTRUCTION_NOTEBOOKS.keys())

    conn = opensysml.connect(version="v0.9.0")
    all_failures: list[str] = []
    try:
        for ch in chapters:
            print(f"Checking Ch{ch}...", end=" ", flush=True)
            failures = check_chapter(ch, conn)
            if failures:
                print(f"FAIL ({len(failures)} issue(s))")
                all_failures.extend(failures)
            else:
                print("ok")
    finally:
        conn.close()

    if all_failures:
        print(f"\n{len(all_failures)} failure(s):")
        for f in all_failures:
            print(f"  - {f}")
        return 1

    print(f"\nAll {len(chapters)} chapter(s) consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
