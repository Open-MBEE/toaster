"""
check_construction.py --check [--chapter=N]

Verify that construction zones in construct-introducing notebooks are consistent
with the committed models/chXX-cumulative.sysml fixtures.

Does NOT reconstruct cumulative files. Read-only — never writes to models/.

Design (from decisions/declarative-construction-plan.md Phase 1c):
- For each construct-introducing notebook (in chapter order):
  1. Parse the notebook JSON; find the last code cell that assigns TOASTER_INCREMENT.
  2. Execute the construction zone (all code cells up to and including TOASTER_INCREMENT).
  3. Validate: load TOASTER_INCREMENT wrapped in the declared validation context; assert model.ok.
- Verify the committed cumulative file also loads cleanly (model.ok) for each chapter.
- Exit 1 and print all failures at end.

TOASTER_INCREMENT convention (all Pattern B — see decisions/declarative-construction-plan.md):
  TOASTER_INCREMENT = new declarations for this notebook only (not the full cumulative model).
  It is assembled from named fragment variables at the end of the construction zone.
  Each fragment variable = one future editor.add_*() call.

Validation scope — context_stubs:
  Each notebook entry declares the minimal type stubs needed for its TOASTER_INCREMENT to parse
  in isolation. These stubs stand in for declarations from prior notebooks in the same chapter
  (or prior chapters). The stubs are explicit so the validation scope is on the record. Stubs
  must be the minimal stub needed — no full model copy-pastes. The cumulative fixture validation
  below is the authoritative correctness check; per-notebook fragment validation detects
  structural/syntax errors in the SysML strings early.
"""
import argparse
import json
import os
import sys
from pathlib import Path

import opensysml

REPO_ROOT = Path(__file__).parent.parent

# Chapters and their construct-introducing notebooks (in order).
# Each entry: {path, context_stubs}.
#   path         — repo-relative path to the notebook
#   context_stubs — minimal SysML declarations for types referenced by this notebook's
#                   TOASTER_INCREMENT that are defined in prior notebooks. The stubs are
#                   included in the validation package context so the fragment parses cleanly.
#                   Stubs must be kept minimal (bare declarations only, no bodies unless the
#                   fragment accesses a member of that type).
CONSTRUCTION_NOTEBOOKS: dict[int, list[dict]] = {
    1: [
        {
            "path": "chapters/ch01-system-purpose/01-abstract-def.ipynb",
            "context_stubs": [],
        },
        {
            "path": "chapters/ch01-system-purpose/02-part-def.ipynb",
            "context_stubs": [],
        },
        {
            "path": "chapters/ch01-system-purpose/03-specialization.ipynb",
            # :> specialization references ToastingSystem (defined in nb01)
            "context_stubs": [
                "abstract part def ToastingSystem;",
            ],
        },
        {
            "path": "chapters/ch01-system-purpose/04-composition.ipynb",
            # part usages reference HeatingSystem and ControlSystem (defined in nb02)
            "context_stubs": [
                "part def HeatingSystem;",
                "part def ControlSystem;",
            ],
        },
    ],
    2: [
        {
            "path": "chapters/ch02-requirements/01-requirement-def.ipynb",
            # TimelyToast references Toaster.cycleTime; nominal references Toaster
            "context_stubs": [
                "part def Toaster { attribute cycleTime : ISQ::DurationValue default = 120.0 [SI::s]; }",
            ],
        },
        {
            "path": "chapters/ch02-requirements/02-assumptions.ipynb",
            # slow :>> cycleTime requires Toaster to have cycleTime in its type chain
            "context_stubs": [
                "part def Toaster { attribute cycleTime : ISQ::DurationValue default = 120.0 [SI::s]; }",
            ],
        },
    ],
    3: [
        {
            "path": "chapters/ch03-measures/01-moe-definition.ipynb",
            # timely : TimelyToast, assert satisfy by nominal/slow require prior-chapter types
            "context_stubs": [
                "requirement def TimelyToast;",
                "part nominal;",
                "part slow;",
            ],
        },
        {
            "path": "chapters/ch03-measures/02-mop-candidate-eval.ipynb",
            "context_stubs": [],
        },
    ],
    4: [
        {
            "path": "chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb",
            # ApplyHeat calls DeliveredEnergy (defined in Ch3)
            "context_stubs": [
                "calc def DeliveredEnergy { in power : ISQ::PowerValue; in duration : ISQ::DurationValue; in efficiency : DimensionOneValue; return : ISQ::EnergyValue = power * duration * efficiency; }",
            ],
        },
        {
            "path": "chapters/ch04-functional-decomp/02-heating-refinement.ipynb",
            "context_stubs": [],
        },
    ],
    5: [
        {
            "path": "chapters/ch05-architecture/02-allocate.ipynb",
            # allocate references ApplyHeat (Ch4) and HeatingSystem (Ch1)
            "context_stubs": [
                "action def ApplyHeat;",
                "part def HeatingSystem;",
            ],
        },
        {
            "path": "chapters/ch05-architecture/03-interfaces.ipynb",
            # BreadLoader/Ejector use Start/Finish item defs (defined in Ch4)
            "context_stubs": [
                "item def Start;",
                "item def Finish;",
            ],
        },
    ],
    7: [
        {
            "path": "chapters/ch07-execution/02-state-traces.ipynb",
            # transitions accept Start/Finish/Cancel item defs (defined in Ch4)
            "context_stubs": [
                "item def Start;",
                "item def Finish;",
                "item def Cancel;",
            ],
        },
    ],
}

CUMULATIVE_FILES = {
    ch: REPO_ROOT / f"models/ch0{ch}-cumulative.sysml"
    for ch in range(1, 9)
}

# Standard package preamble for wrapping fragments during validation.
# {stubs} is replaced with the notebook's declared context_stubs (may be empty).
# {fragment} is replaced with TOASTER_INCREMENT.
_PREAMBLE = """\
package _check {{
    private import ScalarValues::*;
    private import SI::*;
    private import ISQ::*;
    private import MeasurementReferences::*;
{stubs}    {fragment}
}}"""


def _build_wrapped(fragment: str, context_stubs: list[str]) -> str:
    stubs = "".join(f"    {s}\n" for s in context_stubs)
    return _PREAMBLE.format(stubs=stubs, fragment=fragment)


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


def check_notebook(entry: dict, conn: opensysml.Connection) -> list[str]:
    """Check one construct-introducing notebook. Returns list of failure strings."""
    nb_path = REPO_ROOT / entry["path"]
    context_stubs: list[str] = entry.get("context_stubs", [])
    failures = []

    if not nb_path.exists():
        failures.append(f"MISSING: {entry['path']}")
        return failures

    code_cells = _get_code_cells(nb_path)

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
            try:
                exec(compile(cell_src, str(nb_path), "exec"), ns)  # noqa: S102
            except Exception as exc:
                if "TOASTER_INCREMENT" in cell_src and "TOASTER_INCREMENT" not in ns:
                    failures.append(
                        f"EXEC ERROR in {nb_path.name}: {type(exc).__name__}: {exc}"
                    )
                    return failures
            if "TOASTER_INCREMENT" in ns:
                break
    finally:
        os.chdir(orig_dir)

    increment = ns.get("TOASTER_INCREMENT")
    if not increment:
        failures.append(f"TOASTER_INCREMENT is empty after exec: {nb_path.name}")
        return failures

    # Validate: wrap fragment in declared context and load.
    # context_stubs provide the minimal type declarations for cross-notebook dependencies.
    wrapped = _build_wrapped(increment, context_stubs)
    check = conn.load_from_content(wrapped, strict=False)
    if not check.ok:
        failures.append(
            f"TOASTER_INCREMENT does not parse in {nb_path.name}:\n"
            f"  {[str(d) for d in check.diagnostics[:3]]}"
        )

    return failures


def check_chapter(chapter: int, conn: opensysml.Connection) -> list[str]:
    """Check all construction notebooks for one chapter plus the cumulative fixture."""
    failures = []

    for entry in CONSTRUCTION_NOTEBOOKS.get(chapter, []):
        failures.extend(check_notebook(entry, conn))

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
