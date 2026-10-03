# scripts/diagram_study/provision_check.py
"""Phase 0 toolchain provisioning check: confirms the four trade-study tools
match the original study's pinned versions (versions.json / manifest.json in the original
study's diagram-study directory) before any real-fixture render runs.
"""
import json
import os
import subprocess
from pathlib import Path

from toaster.tools import ToolNotFoundError, resolve_sysmlv2

STUDY_ROOT = Path(os.environ.get("STUDY_ROOT", "/private/tmp/toaster-diagram-study"))

# The raw `-render #view:element -render-form X -o file` CLI binary Task 4's render
# pipeline actually invokes -- not STUDY_ROOT/opensysml-current (a stray dev build whose
# -version never reports a release string) and not the toaster package's own gRPC service
# binary under ~/.opensysml/bin (a different invocation style, used via opensysml.connect()).
# Same default path run_study.py itself uses for its STUDY_OPENSYSML.
OPENSYSML_CLI = Path(os.environ.get("STUDY_OPENSYSML", "/private/tmp/functional-toaster-design/sysml"))

PINNED = {
    "opensysml": "v0.9.0",
    "sysml-toolkit": "af839f0d22723772676e509213c65756d1e08ef2",
    "pilot": "jupyter-sysml-kernel-0.62.0",
    "sysml2d": "1af88250d355f4e218f6653ef934e93ac8319cd6",
}


def compare_pinned_versions(reported: dict[str, str], pinned: dict[str, str]) -> list[str]:
    mismatches = []
    for tool, expected in pinned.items():
        if tool not in reported:
            mismatches.append(f"{tool}: not provisioned (expected {expected})")
        elif reported[tool] != expected:
            mismatches.append(f"{tool}: reported {reported[tool]!r}, pinned {expected!r}")
    return mismatches


def _git_commit(repo_dir: Path) -> str | None:
    if not repo_dir.is_dir():
        return None
    result = subprocess.run(
        ["git", "-C", str(repo_dir), "rev-parse", "HEAD"],
        capture_output=True, text=True, timeout=10,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def gather_reported_versions() -> dict[str, str]:
    """Inspects the environment for each tool. Returns whatever it can find;
    callers pass the result to compare_pinned_versions() to see what's missing."""
    reported: dict[str, str] = {}

    # A source build keeps its binary at <checkout>/target/release/sysmlv2, so the checkout (and its
    # git commit) is recoverable from the resolved binary. A provisioned release binary has no
    # checkout around it, so no commit is reported and the pinned comparison says "not provisioned".
    toolkit_dir = None
    try:
        binary = resolve_sysmlv2().resolve()
        if binary.parent.name == "release" and binary.parent.parent.name == "target":
            toolkit_dir = binary.parents[2]
    except ToolNotFoundError:
        pass
    if toolkit_dir is not None and (toolkit_dir / ".git").exists():
        commit = _git_commit(toolkit_dir)
        if commit:
            reported["sysml-toolkit"] = commit

    sysml2d_dir = STUDY_ROOT / "sysml2d"
    commit = _git_commit(sysml2d_dir)
    if commit:
        reported["sysml2d"] = commit

    if OPENSYSML_CLI.exists():
        result = subprocess.run([str(OPENSYSML_CLI), "-version"], capture_output=True, text=True, timeout=10)
        if "v0.9.0" in (result.stdout + result.stderr):
            reported["opensysml"] = "v0.9.0"

    pilot_jar = STUDY_ROOT / "pilot/sysml/jupyter-sysml-kernel-0.62.0-all.jar"
    if pilot_jar.exists():
        reported["pilot"] = "jupyter-sysml-kernel-0.62.0"

    return reported


def main() -> int:
    reported = gather_reported_versions()
    mismatches = compare_pinned_versions(reported, PINNED)
    report = {
        "study_root": str(STUDY_ROOT),
        "opensysml_cli_path": str(OPENSYSML_CLI),
        "reported": reported,
        "pinned": PINNED,
        "mismatches": mismatches,
    }
    out = Path("decisions/diagram-study-real-fixtures/evidence")
    out.mkdir(parents=True, exist_ok=True)
    (out / "provisioning-report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
