"""
check_conformance.py [MODEL_FILE...] [--json] [--stage CH,SEC]

CLI report surface for the two-tier conformance model in `src/toaster/conformance.py`
(AGENTS.md 1.9). For each model given (or, by default, every committed cumulative fixture),
calls `toaster.conformance.report(model, stage, REGISTRY)` and prints the result: the
always-on language tier (ok, diagnostics, gap_findings) and the staged project checks
(id, status, reason, unblock_when).

Default (no MODEL_FILE args): load every models/chNN-cumulative.sysml in order (ch01
through ch08, whichever exist). The stage for each model defaults to (N, 0), where N is
the chapter number parsed from its filename (the `chNN` prefix); `--stage CH,SEC`
overrides that default for every model named on the command line, whether default or
explicit.

Exit code: 1 if any project check on any model has status "failed"; 0 otherwise ("open",
"blocked", "wont-do" and "passed" are not failures, per the status semantics documented at
the top of conformance.py).

Follows the argparse / REPO_ROOT / opensysml.connect-and-close style of
scripts/check_construction.py, and the --json convention of glossary/cli.py
(`json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)`).
"""
import argparse
import json
import re
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

import opensysml

from toaster import conformance

REPO_ROOT = Path(__file__).parent.parent

_CHAPTER_RE = re.compile(r"ch(\d+)", re.IGNORECASE)


def _default_model_files() -> list[Path]:
    """models/ch01-cumulative.sysml through models/ch08-cumulative.sysml, whichever exist."""
    files = []
    for ch in range(1, 9):
        p = REPO_ROOT / f"models/ch0{ch}-cumulative.sysml"
        if p.exists():
            files.append(p)
    return files


def parse_stage(text: str) -> conformance.Stage:
    """Parse a ``--stage CH,SEC`` value into a ``(chapter, section)`` tuple."""
    parts = text.split(",")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(f"--stage must be CH,SEC (got {text!r})")
    try:
        return (int(parts[0]), int(parts[1]))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"--stage must be CH,SEC integers (got {text!r})"
        ) from exc


def _stage_from_filename(path: Path) -> conformance.Stage:
    """Default stage (N, 0), where N is the chapter number parsed from a ``chNN`` filename prefix."""
    m = _CHAPTER_RE.search(path.stem)
    if not m:
        raise SystemExit(
            f"cannot infer a chapter/stage from filename {path.name!r}: pass --stage CH,SEC"
        )
    return (int(m.group(1)), 0)


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _project_dict(result: conformance.Result) -> dict:
    d = asdict(result)
    d["id"] = d.pop("check_id")
    return d


def build_report(
    conn: Any, path: Path, stage: conformance.Stage
) -> dict:
    """Load ``path`` and return one model's conformance report as a plain dict."""
    model = conn.load_from_content(path.read_text(), strict=False)
    raw = conformance.report(model, stage, conformance.REGISTRY)
    return {
        "path": _display_path(path),
        "stage": list(stage),
        "language": raw["language"],
        "project": [_project_dict(c) for c in raw["project"]],
    }


def _print_text(reports: list[dict]) -> None:
    for r in reports:
        stage = r["stage"]
        print(f"== {r['path']} (stage {stage[0]}.{stage[1]}) ==")
        lang = r["language"]
        print(f"  language: ok={lang['ok']}")
        if lang["diagnostics"]:
            print("    diagnostics:")
            for d in lang["diagnostics"]:
                print(f"      - {d}")
        else:
            print("    diagnostics: (none)")
        if lang["gap_findings"]:
            print("    gap_findings:")
            for f in lang["gap_findings"]:
                print(f"      - [{f.get('rule')}] {f.get('element')}: {f.get('message')}")
        else:
            print("    gap_findings: (none)")
        print("  project checks:")
        if not r["project"]:
            print("    (none registered)")
        for c in r["project"]:
            line = f"    - {c['id']}: {c['status']}"
            if c.get("reason"):
                line += f" (reason: {c['reason']})"
            if c.get("unblock_when"):
                line += f" (unblock_when: {c['unblock_when']})"
            print(line)
            for finding in c.get("findings") or []:
                print(f"        finding: {finding}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report language and project conformance for toaster models."
    )
    parser.add_argument(
        "model_files",
        nargs="*",
        metavar="MODEL_FILE",
        help="Model file(s) to check (default: models/ch01..ch08-cumulative.sysml, whichever exist).",
    )
    parser.add_argument("--json", action="store_true", help="Machine-readable output.")
    parser.add_argument(
        "--stage",
        type=parse_stage,
        default=None,
        metavar="CH,SEC",
        help="Override the stage for every model given on the command line.",
    )
    args = parser.parse_args()

    paths = [Path(p) for p in args.model_files] if args.model_files else _default_model_files()

    conn = opensysml.connect(version="v0.9.0")
    reports: list[dict] = []
    try:
        for path in paths:
            stage = args.stage if args.stage is not None else _stage_from_filename(path)
            reports.append(build_report(conn, path, stage))
    finally:
        conn.close()

    any_failed = any(c["status"] == "failed" for r in reports for c in r["project"])

    if args.json:
        print(json.dumps(reports, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        _print_text(reports)

    return 1 if any_failed else 0


if __name__ == "__main__":
    sys.exit(main())
