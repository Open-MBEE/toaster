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

from toaster import query

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
            # Toaster :> ToastingSystem (defined in nb01); part usages reference
            # HeatingSystem and ControlSystem (defined in nb02)
            "context_stubs": [
                "abstract part def ToastingSystem;",
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
            # timely : TimelyToast requires the requirement def from Chapter 2
            "context_stubs": [
                "requirement def TimelyToast;",
            ],
        },
        {
            "path": "chapters/ch03-measures/02-mop-candidate-eval.ipynb",
            # the reopened slow body with its assert not satisfy requires Toaster,
            # TimelyToast (with its subject and constraint) and timely : TimelyToast
            "context_stubs": [
                "part def Toaster { attribute cycleTime : ISQ::DurationValue; }",
                "requirement def TimelyToast { subject toaster : Toaster; require constraint { toaster.cycleTime <= 180.0 [SI::s] } }",
                "requirement timely : TimelyToast;",
            ],
        },
        {
            "path": "chapters/ch03-measures/04-verification-case.ipynb",
            # verify timely requires timely : TimelyToast (req usage) and Toaster part def in scope
            "context_stubs": [
                "requirement def TimelyToast { subject toaster : Toaster; require constraint { toaster.cycleTime <= 180.0; } }",
                "requirement timely : TimelyToast;",
                "part def Toaster { attribute cycleTime : Real default = 120.0; }",
            ],
        },
    ],
    4: [
        {
            "path": "chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb",
            # ApplyHeat and the reopened ToastBread both reference Bread/Toast (Ch1).
            # PASS4-004 removed calc def DeliveredEnergy from ApplyHeat's body (DL-030);
            # it does not originate in this chapter and is not reintroduced here.
            "context_stubs": [
                "item def Bread;",
                "item def Toast;",
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
            # HeatingSystem's `perform` references ApplyHeat (Ch4). It carries no
            # supertype (DL-019/DL-020: ToastingSystem is the subject, not something
            # a logical component specializes). The allocation references
            # ToastBread::applyHeat (Ch4, a nested action usage) and
            # Toaster::heating (Ch1); this notebook's own fragment declares
            # HeatingSystem itself, so it is not stubbed here.
            "context_stubs": [
                "action def ApplyHeat;",
                "action def ToastBread { action applyHeat : ApplyHeat; }",
                "part def Toaster { part heating; }",
            ],
        },
        {
            "path": "chapters/ch05-architecture/03-interfaces.ipynb",
            # HeatingSystem's `perform` references ApplyHeat (Ch4) and carries no
            # supertype (DL-019/DL-020). Toaster's own `:> ToastingSystem`
            # (Ch1, unchanged) still needs the ToastingSystem stub. This
            # notebook's own fragment declares DurationPort, HeatingSystem,
            # ControlSystem and Toaster completely, so none of those is stubbed.
            "context_stubs": [
                "abstract part def ToastingSystem;",
                "action def ApplyHeat;",
            ],
        },
    ],
    6: [
        {
            "path": "chapters/ch06-recursive-decomp/01-subsystem-requirements.ipynb",
            # HeatingAssembly :> HeatingSystem (ch05); ApplyHeat's rewritten body
            # references Bread/Toast (ch01/ch04). GenerateHeat, EnergyPort and
            # HeatGenerator are declared by this notebook's own fragment.
            "context_stubs": [
                "item def Bread;",
                "item def Toast;",
                "abstract part def HeatingSystem;",
            ],
        },
        {
            "path": "chapters/ch06-recursive-decomp/02-second-level.ipynb",
            # ResistanceCoil :> HeatGenerator (nb01); HeatGenerationReq's subject
            # is HeatGenerator, and rated/weak are typed by ResistanceCoil, this
            # notebook's own fragment.
            "context_stubs": [
                "abstract part def HeatGenerator { attribute power : ISQ::PowerValue; }",
            ],
        },
    ],
    7: [
        {
            "path": "chapters/ch07-execution/01-calc-energy.ipynb",
            # HeatGenerator is reprinted in full with efficiency/deliveredEnergy added
            # (Ch6); rated is reprinted in full with its new efficiency value (Ch6),
            # referencing ResistanceCoil and heatGenerationReq (both Ch6).
            "context_stubs": [
                "action def GenerateHeat;",
                "port def EnergyPort;",
                "part def ResistanceCoil :> HeatGenerator { attribute :>> power default = 800.0 [SI::W]; }",
                "requirement def HeatGenerationReq { subject heatGen : HeatGenerator; require constraint { heatGen.power >= 600.0 [SI::W] } }",
                "requirement heatGenerationReq : HeatGenerationReq;",
            ],
        },
        {
            "path": "chapters/ch07-execution/02-state-traces.ipynb",
            # Cycle's do action references GenerateHeat (Ch6); ToastingSystem (the
            # abstract subject, Ch1) is reprinted in full with the new exhibit line,
            # referencing its own existing perform (ToastBread, Ch4). Toaster itself is
            # not touched: the exhibit lives on ToastingSystem, inherited by Toaster and
            # any usage of it (DL-019/DL-044). Start/Finish/Cancel (Ch4) are accepted
            # triggers OpenSysML does not resolve at load time (D-023), so a stub for
            # them is not required for this fragment to validate, but they are kept for
            # documentation: the accept clauses are still real references.
            "context_stubs": [
                "item def Start;",
                "item def Finish;",
                "item def Cancel;",
                "action def GenerateHeat;",
                "action def ToastBread;",
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


def _named_elements(index: "query.ApiIndex") -> dict[str, str]:
    """``{qualifiedName: @type}`` for every NAMED element in an API-JSON export.

    Identity is restricted to elements that carry their own declared name (the export's
    ``declaredName`` key, not None; the export has no ``name`` key at all, only
    ``declaredName`` — confirmed by inspection, not assumed). An unnamed member (e.g. a
    ``doc``, or a bare constraint body) gets a synthetic ``@N`` qualifiedName segment
    assigned by its position among its owner's members (e.g.
    ``ToasterDemo::TimelyToast::@2``); that position shifts when a sibling member is
    added or removed, so it is not a stable identity to compare across two
    separately-edited chapter fixtures (see decisions/audits/ch04-layer-audit.md F-5,
    where removing `TimelyToast`'s `doc` renumbers the following `ConstraintUsage` from
    `@2` to `@1`). A NAMED element's qualifiedName is built from its own declared name and
    its owners' declared names, not from sibling position, and was confirmed stable
    across two separately-loaded `opensysml.Connection`s of the same content (the
    API-JSON `@id` is derived deterministically from the qualifiedName). This matches the
    contract's "every NAMED element" wording.
    """
    return {
        e["qualifiedName"]: e["@type"]
        for e in index.elements
        if e.get("qualifiedName") and e.get("declaredName") is not None
    }


def check_predecessor_containment(chapter: int, conn: opensysml.Connection) -> list[str]:
    """For ch{chapter}, verify every NAMED element of ch{chapter-1} is still present, same @type.

    Only runs when chapter > 1 and both ch{chapter-1} and ch{chapter} cumulative fixtures
    exist. Identity is by qualified name via the API-JSON export (`toaster.query.ApiIndex`),
    restricted to named elements (see `_named_elements`). Loads both fixtures fresh on the
    given connection rather than reusing a model `check_chapter` may already have loaded,
    so this function also works standalone (e.g. from a test or a one-off script).
    """
    failures: list[str] = []
    if chapter <= 1:
        return failures

    prev_path = CUMULATIVE_FILES.get(chapter - 1)
    cur_path = CUMULATIVE_FILES.get(chapter)
    if not prev_path or not cur_path or not prev_path.exists() or not cur_path.exists():
        return failures

    prev_model = conn.load_from_content(prev_path.read_text(), strict=False)
    cur_model = conn.load_from_content(cur_path.read_text(), strict=False)
    if not prev_model.ok or not cur_model.ok:
        # A model that fails to load is reported by the cumulative-fixture-loads check
        # above; comparing element sets of a model that did not load is not meaningful.
        return failures

    prev_named = _named_elements(query.ApiIndex(prev_model))
    cur_named = _named_elements(query.ApiIndex(cur_model))

    prev_label = f"ch{chapter - 1:02d}-cumulative.sysml"
    cur_label = f"ch{chapter:02d}-cumulative.sysml"
    for qn in sorted(prev_named):
        prev_type = prev_named[qn]
        if qn not in cur_named:
            failures.append(
                f"PREDECESSOR CONTAINMENT {prev_label} -> {cur_label}: "
                f"{qn} ({prev_type}) is missing from {cur_label}"
            )
        elif cur_named[qn] != prev_type:
            failures.append(
                f"PREDECESSOR CONTAINMENT {prev_label} -> {cur_label}: "
                f"{qn} changed @type from {prev_type} (in {prev_label}) to "
                f"{cur_named[qn]} (in {cur_label})"
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

    # Verify ch{chapter} still contains every named element of ch{chapter-1} (same
    # qualified name, same @type). Not gated on the cumulative-fixture-loads check
    # above (a fresh pair of loads is used), but naturally produces no findings when
    # either fixture failed to load, per the guard in check_predecessor_containment.
    failures.extend(check_predecessor_containment(chapter, conn))

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
