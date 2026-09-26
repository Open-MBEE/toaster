"""
check_construction.py --check [--chapter=N]

Verify that construction cells (cell-02 in construct-introducing notebooks) are
consistent with the committed models/chXX-cumulative.sysml fixtures.

Does NOT reconstruct cumulative files. Read-only — never writes to models/.

Design (from decisions/declarative-construction-plan.md Phase 1c):
- For each construct-introducing notebook (in chapter order):
  1. Parse cell-02 source from the notebook JSON.
  2. Identify pattern: Pattern A (contains 'editor.') or Pattern B (TOASTER_INCREMENT string).
  3. Execute cell-02 in a prepared namespace; capture TOASTER_INCREMENT.
  4. Validate:
     Pattern A: load TOASTER_INCREMENT via conn.load_from_content(); assert model.ok.
       If this is the last Pattern A notebook in the chapter: compare against the committed
       cumulative (whitespace-normalized).
     Pattern B: wrap fragment in a minimal package; load; assert model.ok.
- Exit 1 and print all failures at end.

TOASTER_INCREMENT convention (probed 2026-09-25):
  Pattern A: str(editor.apply()) = full cumulative model (all prior + new declarations)
  Pattern B: new SysML fragment only
"""
import argparse
import json
import re
import sys
from pathlib import Path

import opensysml

REPO_ROOT = Path(__file__).parent.parent

# Map: chapter number → list of (notebook_path, pattern)
# Pattern A: Editor API; Pattern B: SysML string fragment (gap construct)
CONSTRUCTION_NOTEBOOKS = {
    1: [
        ("chapters/ch01-system-purpose/01-abstract-def.ipynb", "B"),
        ("chapters/ch01-system-purpose/02-part-def.ipynb", "A"),
        ("chapters/ch01-system-purpose/03-specialization.ipynb", "A"),
        ("chapters/ch01-system-purpose/04-composition.ipynb", "A"),
    ],
    2: [
        ("chapters/ch02-requirements/01-requirement-def.ipynb", "B"),
        ("chapters/ch02-requirements/02-assumptions.ipynb", "B"),
    ],
    3: [
        ("chapters/ch03-measures/01-moe-definition.ipynb", "B"),
        ("chapters/ch03-measures/02-mop-candidate-eval.ipynb", "A"),
    ],
    4: [
        ("chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb", "A"),
        ("chapters/ch04-functional-decomp/02-heating-refinement.ipynb", "A"),
    ],
    5: [
        ("chapters/ch05-architecture/02-allocate.ipynb", "B"),
        ("chapters/ch05-architecture/03-interfaces.ipynb", "B"),
    ],
    7: [
        ("chapters/ch07-execution/02-state-traces.ipynb", "B"),
    ],
}

CUMULATIVE_FILES = {
    ch: REPO_ROOT / f"models/ch0{ch}-cumulative.sysml"
    for ch in range(1, 9)
}


def _normalize(text: str) -> str:
    """Normalize whitespace for comparison."""
    return re.sub(r"\s+", " ", text).strip()


def _extract_cell02(nb_path: Path) -> str | None:
    """Return the source of cell-02 (index 2) from a notebook JSON."""
    nb = json.loads(nb_path.read_text())
    cells = nb.get("cells", [])
    if len(cells) < 3:
        return None
    cell = cells[2]
    source = cell.get("source", [])
    if isinstance(source, list):
        return "".join(source)
    return source


def _detect_pattern(cell_source: str) -> str:
    """Detect Pattern A (editor.apply()) or Pattern B (fragment string)."""
    if "editor." in cell_source and "editor.apply()" in cell_source:
        return "A"
    return "B"


def check_chapter(chapter: int, conn: opensysml.Connection) -> list[str]:
    """Check one chapter's construction notebooks. Returns list of failure strings."""
    failures = []
    notebooks = CONSTRUCTION_NOTEBOOKS.get(chapter, [])
    last_pattern_a_result = None

    for nb_rel, declared_pattern in notebooks:
        nb_path = REPO_ROOT / nb_rel
        if not nb_path.exists():
            failures.append(f"MISSING notebook: {nb_rel}")
            continue

        cell_src = _extract_cell02(nb_path)
        if cell_src is None:
            failures.append(f"NO cell-02: {nb_rel}")
            continue

        if "TOASTER_INCREMENT" not in cell_src:
            failures.append(f"NO TOASTER_INCREMENT in cell-02: {nb_rel}")
            continue

        detected = _detect_pattern(cell_src)
        if detected != declared_pattern:
            failures.append(
                f"PATTERN MISMATCH in {nb_rel}: declared={declared_pattern}, detected={detected}"
            )

        # Execute cell-02 in a controlled namespace
        ns: dict = {
            "__file__": str(nb_path),
            "Path": Path,
        }
        # Change working directory context for Path("../../models/...") to resolve correctly
        import os
        orig_dir = os.getcwd()
        try:
            os.chdir(nb_path.parent)
            exec(compile(cell_src, str(nb_path), "exec"), ns)  # noqa: S102
        except Exception as exc:
            failures.append(f"EXEC ERROR in {nb_rel}: {type(exc).__name__}: {exc}")
            continue
        finally:
            os.chdir(orig_dir)

        increment = ns.get("TOASTER_INCREMENT")
        if increment is None:
            failures.append(f"TOASTER_INCREMENT not set after exec: {nb_rel}")
            continue

        if declared_pattern == "A":
            # Validate: the full model string must parse
            check = conn.load_from_content(increment, strict=False)
            if not check.ok:
                failures.append(
                    f"PATTERN A model invalid in {nb_rel}: {check.diagnostics}"
                )
            else:
                last_pattern_a_result = (nb_rel, increment)

        else:  # Pattern B: validate the fragment parses in a minimal package
            fragment_pkg = (
                f"package _check_{chapter} {{\n"
                f"    private import ScalarValues::*;\n"
                f"    private import SI::*;\n"
                f"    private import ISQ::*;\n"
                f"    private import MeasurementReferences::*;\n"
                f"{increment}\n"
                f"}}"
            )
            check = conn.load_from_content(fragment_pkg, strict=False)
            if not check.ok:
                failures.append(
                    f"PATTERN B fragment invalid in {nb_rel}: {check.diagnostics}"
                )

    # For the last Pattern A notebook in this chapter: compare against committed fixture
    if last_pattern_a_result is not None:
        nb_rel, increment = last_pattern_a_result
        cumulative_path = CUMULATIVE_FILES.get(chapter)
        if cumulative_path and cumulative_path.exists():
            committed = cumulative_path.read_text()
            if _normalize(increment) != _normalize(committed):
                failures.append(
                    f"FIXTURE DRIFT in ch{chapter}: last Pattern A TOASTER_INCREMENT "
                    f"does not match {cumulative_path.name}.\n"
                    f"  Source notebook: {nb_rel}\n"
                    f"  Increment (normalized): {_normalize(increment)[:120]}...\n"
                    f"  Fixture (normalized):   {_normalize(committed)[:120]}..."
                )

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify construction cell consistency.")
    parser.add_argument("--check", action="store_true", required=True)
    parser.add_argument("--chapter", type=int, default=None,
                        help="Check one chapter only (1–8)")
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
