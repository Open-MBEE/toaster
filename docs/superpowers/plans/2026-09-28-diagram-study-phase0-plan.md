# Diagram Study Phase 0 (Real-Fixture Trade-Study Rerun) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-run the original diagram-tool trade study's own method (pinned versions, hash/raster comparison, and the mutation-control test that caught SysMLD's silent staleness) against four real toaster chapter models instead of the study's simplified toy fixture, so the tool-capability conclusions the diagram survey (Phase 1) will lean on are grounded in real model complexity.

**Architecture:** A small, testable Python harness (`scripts/diagram_study/`) generalizes the original study's `run_study.py`/`check_sysmld_mutation.py` scripts from one fixture to four real fixtures (`models/ch05/06/07/08-cumulative.sysml`, copied verbatim into versioned trade-study inputs). Four tool pipelines (OpenSysML→PlantUML, OpenSysML→DOT/Graphviz, sysml-toolkit, OMG pilot) render known view types against all four fixtures; SysMLD gets hand-authored diagram-intent JSON for the two views its schema actually fits (Ch5 interconnection, Ch7 state) and is rendered the same way the original study proved it out. Every fixture gets a one-element "mutated" sibling; re-rendering against the mutated sibling and diffing the SVG is the mutation-control check, run for every tool that renders that fixture's view — not just the ones expected to pass. Findings are compiled into `decisions/diagram-study-real-fixtures.md`, mirroring the original study's `report.md` structure.

**Tech Stack:** Python 3 (stdlib `subprocess`/`hashlib`/`json`), `opensysml` (already a toaster dependency, v0.9.0), `pytest`. External tool binaries used as throwaway trade-study tooling only, never added to `pyproject.toml`/`uv.lock`: OpenSysML CLI binary, `sysml-toolkit` (Rust CLI, already built locally at `~/Documents/GitHub/sysml-toolkit`), the OMG pilot (`jupyter-sysml-kernel` JAR via `java`), SysMLD/`sysml2d` (Python package), Graphviz `dot`, PlantUML JAR.

**Spec:** [`docs/superpowers/specs/2026-09-28-diagram-survey-design.md`](../specs/2026-09-28-diagram-survey-design.md) — this plan implements **Phase 0 only** (§"Phase 0: re-run the trade study against real fixtures"). Phase 1 (the per-chapter diagram survey) and any implementation work are explicitly out of scope (spec §"Non-goals") and stay unspecced until Phase 0's findings exist and Z has reviewed them.

## Global Constraints

- **No chapter, model, or notebook file is ever edited.** `models/ch05/06/07/08-cumulative.sysml` are read-only inputs; every fixture used by this plan is a verbatim *copy* under `decisions/diagram-study-real-fixtures/`.
- **Zero new dependencies added to the tutorial itself.** Nothing in this plan touches `pyproject.toml`, `uv.lock`, or any chapter/notebook dependency. The four trade-study tools are throwaway comparison tooling (per spec decision 1, only 2 of them — OpenSysML+Graphviz/DOT and sysml-toolkit — are even being carried forward as real candidates).
- **Pinned tool versions** (from the original study's `versions.json` and `manifest.json`, `/Users/z/Downloads/toaster/diagram-study/`): OpenSysML `v0.9.0` / commit `ee54ea03ea3ca8fb2c796ecda364adf748c40304`; `sysml-toolkit` commit `af839f0d22723772676e509213c65756d1e08ef2` (already checked out at `~/Documents/GitHub/sysml-toolkit`, confirmed via `git log -1` — no rebuild needed); OMG pilot `2026-08` / `jupyter-sysml-kernel-0.62.0`; `sysml2d` commit `1af88250d355f4e218f6653ef934e93ac8319cd6`. Task 1 verifies these are what's actually provisioned before any render runs.
- **Every mutated fixture must pass a load-validity gate** (`conn.load_from_content(text, strict=False)` → `model.ok is True`) before it is used in any render step. This is the plan's own "probe before you assert" safety net for the hand-authored mutations in Task 3.
- **Match the original study's rigor, not a lighter spot-check** (spec decision 6): pinned versions recorded, per-run timing/exit-code/hash capture, raster comparison, and a real-model mutation-control test for every candidate that renders a given fixture's view — the exact discipline that caught SysMLD's staleness the first time.
- **DEMA SysML2Tools is out of scope.** The approved spec's Phase 0 method names exactly four tools to rerun ("OpenSysML+Graphviz/DOT and sysml-toolkit ... plus the OMG pilot and SysMLD"); DEMA is not one of them, even though the original study also tested it. This plan does not render DEMA.

## Review Focus

- A render CLI failing on real content that never appeared in the toy fixture (multi-line `private import` blocks, `calc def`, Z3 `assert constraint` bodies) must be captured as a real, recordable matrix finding (exit code + stderr logged), never silently swallowed or allowed to abort the whole run — Task 4's driver step and Task 1's provisioning test both assert on captured exit codes, not on "the script didn't crash."
- A tool "succeeding" (exit 0, SVG produced) while silently dropping the exact feature a fixture exists to test (e.g., a conjugated port collapsing to a part-level line the way OpenSysML did on the toy fixture) must be caught by inspecting rendered SVG/PUML/DOT text for the expected element name, not just asserting the file is non-empty — Task 4's tests check for the fixture's target element name inside the emitted source, matching the original study's own qualitative inspection.
- The mutation-control test must not pass vacuously because both the "before" and "after" renders failed — Task 7's check asserts the *baseline* render succeeded (real SVG bytes, `exit_code == 0`) before it is ever compared to the mutated render, mirroring `check_sysmld_mutation.py`'s own `p.check_returncode()` gate before its byte comparison.
- A hand-authored SysMLD intent file drifting from what the real fixture actually contains (a typo in an alias, an element name that no longer exists) is the same "model-to-picture integrity" risk the mutation-control test exists to catch, one level earlier — Task 6 requires every alias in the two new intent files to be copied verbatim from the real fixture text (not retyped from memory), and its own load-validity/compose/validate steps are the check that would catch drift.
- A tool or view type from the original 4-view comparison having no real-fixture analog in this phase (action-flow already existed from Ch4 onward, so it isn't one of the untested gaps this rerun targets) must be explicitly marked "not rerun in Phase 0, see original study" in the compiled deliverable, not silently omitted — Task 8's self-check verifies the deliverable states its own scope boundary against the four original view types × five original tools.

---

## Task 1: Verify the Phase 0 toolchain against the original study's pinned versions

**Files:**
- Create: `scripts/diagram_study/__init__.py`
- Create: `scripts/diagram_study/provision_check.py`
- Test: `tests/test_diagram_study_provisioning.py`

**Interfaces:**
- Produces: `compare_pinned_versions(reported: dict[str, str], pinned: dict[str, str]) -> list[str]` (pure; returns a list of human-readable mismatch strings, empty if everything matches) and `PINNED = {"opensysml": "...", "sysml-toolkit": "...", "pilot": "...", "sysml2d": "..."}` (module-level dict of the pinned versions above), both consumed by Task 2's `harness.py` and Task 8's deliverable-writing step.

- [ ] **Step 1: Write the failing test for the pure comparison function**

```python
# tests/test_diagram_study_provisioning.py
from scripts.diagram_study.provision_check import compare_pinned_versions, PINNED


def test_matching_versions_report_no_mismatches():
    reported = dict(PINNED)
    assert compare_pinned_versions(reported, PINNED) == []


def test_mismatched_version_is_reported():
    reported = dict(PINNED)
    reported["sysml-toolkit"] = "deadbeef"
    mismatches = compare_pinned_versions(reported, PINNED)
    assert len(mismatches) == 1
    assert "sysml-toolkit" in mismatches[0]
    assert "deadbeef" in mismatches[0]
    assert PINNED["sysml-toolkit"] in mismatches[0]


def test_missing_tool_is_reported_as_a_mismatch():
    reported = {k: v for k, v in PINNED.items() if k != "pilot"}
    mismatches = compare_pinned_versions(reported, PINNED)
    assert any("pilot" in m and "not provisioned" in m for m in mismatches)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_diagram_study_provisioning.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.diagram_study'`

- [ ] **Step 3: Write `scripts/diagram_study/__init__.py` (empty) and `scripts/diagram_study/provision_check.py`**

```python
# scripts/diagram_study/provision_check.py
"""Phase 0 toolchain provisioning check: confirms the four trade-study tools
match the original study's pinned versions (versions.json / manifest.json at
/Users/z/Downloads/toaster/diagram-study/) before any real-fixture render runs.
"""
import json
import os
import subprocess
from pathlib import Path

STUDY_ROOT = Path(os.environ.get("STUDY_ROOT", "/private/tmp/toaster-diagram-study"))

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

    toolkit_dir = Path.home() / "Documents/GitHub/sysml-toolkit"
    commit = _git_commit(toolkit_dir)
    if commit:
        reported["sysml-toolkit"] = commit

    sysml2d_dir = STUDY_ROOT / "sysml2d"
    commit = _git_commit(sysml2d_dir)
    if commit:
        reported["sysml2d"] = commit

    opensysml_bin = STUDY_ROOT / "opensysml-current"
    if opensysml_bin.exists():
        result = subprocess.run([str(opensysml_bin), "-version"], capture_output=True, text=True, timeout=10)
        if "v0.9.0" in (result.stdout + result.stderr):
            reported["opensysml"] = "v0.9.0"

    pilot_jar = STUDY_ROOT / "pilot/sysml/jupyter-sysml-kernel-0.62.0-all.jar"
    if pilot_jar.exists():
        reported["pilot"] = "jupyter-sysml-kernel-0.62.0"

    return reported


def main() -> int:
    reported = gather_reported_versions()
    mismatches = compare_pinned_versions(reported, PINNED)
    report = {"study_root": str(STUDY_ROOT), "reported": reported, "pinned": PINNED, "mismatches": mismatches}
    out = Path("decisions/diagram-study-real-fixtures/evidence")
    out.mkdir(parents=True, exist_ok=True)
    (out / "provisioning-report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_diagram_study_provisioning.py -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Run the provisioning check for real and record what's actually on this machine**

Run: `mkdir -p decisions/diagram-study-real-fixtures/evidence && uv run python -m scripts.diagram_study.provision_check`

At the time this plan was written, `/private/tmp/toaster-diagram-study` (the original study's own `STUDY_ROOT`) was still present on disk with `sysml-toolkit/`, `sysml2d/`, `pilot/sysml/jupyter-sysml-kernel-0.62.0-all.jar`, and `opensysml-current` all intact, and `~/Documents/GitHub/sysml-toolkit` was checked out exactly at the pinned commit. `/private/tmp` is not durable — if it has been cleared by the time this task runs, `gather_reported_versions()` will report those tools as absent (not silently skip them) and `main()` returns exit code 1 with the specific missing tools named in `provisioning-report.json`. **If any tool is reported missing, re-provision it before continuing to Task 4**, using the original study's own sources as the reference: `sysml-toolkit` — already present, no action needed unless the git check fails; `sysml2d` — `git clone <the sysml2d repo> STUDY_ROOT/sysml2d && git -C STUDY_ROOT/sysml2d checkout 1af88250d355f4e218f6653ef934e93ac8319cd6`; pilot — re-extract `pilot.zip` if still present in `STUDY_ROOT`, else re-download the `2026-08` release referenced in `report.md`; OpenSysML — already a toaster dependency (`opensysml` Python package via `ensure_binary(version="v0.9.0")`, per the `opensysml-api` skill), independent of `STUDY_ROOT`.

- [ ] **Step 6: Commit**

```bash
git add scripts/diagram_study/__init__.py scripts/diagram_study/provision_check.py tests/test_diagram_study_provisioning.py decisions/diagram-study-real-fixtures/evidence/provisioning-report.json
git commit -m "Phase 0 diagram study: verify toolchain against original study's pinned versions"
```

## Task 2: Extract a reusable, testable render/run harness module

**Files:**
- Create: `scripts/diagram_study/harness.py`
- Test: `tests/test_diagram_study_harness.py`

**Interfaces:**
- Consumes: nothing from Task 1 directly (the harness takes resolved tool paths as arguments, it does not re-discover them).
- Produces: `build_render_command(tool: str, view: str, element: str, model_path: Path, source_path: Path, tools: dict) -> list[str]` (pure), `hash_bytes(data: bytes) -> str`, `svgs_differ(before: bytes, after: bytes) -> bool`, `run_and_log(name: str, cmd: list[str], out_dir: Path, env: dict | None = None) -> subprocess.CompletedProcess` (writes `{out_dir}/{name}.log`, does not raise on nonzero exit — callers decide). Consumed by Task 4 (`run_real_fixture_study.py`) and Task 7 (mutation-control driver).

- [ ] **Step 1: Write the failing tests for the pure command-building and comparison functions**

```python
# tests/test_diagram_study_harness.py
from pathlib import Path

from scripts.diagram_study.harness import build_render_command, hash_bytes, svgs_differ


TOOLS = {
    "opensysml": "/path/to/opensysml-current",
    "toolkit": "/path/to/sysmlv2",
}


def test_opensysml_dot_command_shape():
    cmd = build_render_command(
        "opensysml-dot", "tree", "ToasterDemo::Toaster",
        Path("fixtures/ch06.sysml"), Path("evidence/ch06-tree.dot"), TOOLS,
    )
    assert cmd[0] == TOOLS["opensysml"]
    assert "fixtures/ch06.sysml" in cmd
    assert "-render" in cmd
    assert "#tree:ToasterDemo::Toaster" in cmd
    assert "-render-form" in cmd and "dot" in cmd
    assert cmd[-1] == "evidence/ch06-tree.dot"


def test_toolkit_command_shape():
    cmd = build_render_command(
        "toolkit", "interconnection", "ToasterDemo::Toaster",
        Path("fixtures/ch05.sysml"), Path("evidence/ch05-interconnection.puml"), TOOLS,
    )
    assert cmd[0] == TOOLS["toolkit"]
    assert cmd[1] == "viz"
    assert "fixtures/ch05.sysml" in cmd
    assert "--view" in cmd and "interconnection" in cmd
    assert "--element" in cmd and "ToasterDemo::Toaster" in cmd
    assert "-o" in cmd and "evidence/ch05-interconnection.puml" in cmd


def test_unknown_tool_raises():
    import pytest
    with pytest.raises(ValueError, match="unknown tool"):
        build_render_command("nope", "tree", "X", Path("a"), Path("b"), TOOLS)


def test_hash_bytes_is_stable_sha256():
    import hashlib
    data = b"hello"
    assert hash_bytes(data) == hashlib.sha256(data).hexdigest()


def test_svgs_differ_true_on_change_false_on_repeat():
    a = b"<svg>one</svg>"
    b = b"<svg>two</svg>"
    assert svgs_differ(a, b) is True
    assert svgs_differ(a, a) is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_diagram_study_harness.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.diagram_study.harness'`

- [ ] **Step 3: Write `scripts/diagram_study/harness.py`**

```python
"""Reusable render/run helpers for the Phase 0 real-fixture diagram study.
Generalizes the original study's run_study.py (run(), render()) from one
fixture to a (tool, view, element, model) table over real chapter models.
"""
import hashlib
import subprocess
import time
from pathlib import Path


def build_render_command(
    tool: str, view: str, element: str, model_path: Path, source_path: Path, tools: dict
) -> list[str]:
    if tool == "opensysml-puml":
        return [tools["opensysml"], str(model_path), "-render", f"#{view}:{element}",
                "-render-form", "plantuml", "-o", str(source_path)]
    if tool == "opensysml-dot":
        return [tools["opensysml"], str(model_path), "-render", f"#{view}:{element}",
                "-render-form", "dot", "-o", str(source_path)]
    if tool == "toolkit":
        return [tools["toolkit"], "viz", str(model_path), "--view", view,
                "--element", element, "-o", str(source_path)]
    if tool == "pilot":
        # args: library, model, element, view, dest-svg (see PilotRender.java)
        return [tools["java"], "-Djava.awt.headless=true", "-cp", tools["pilot_jar"],
                tools["pilot_render_class"], tools["pilot_library"], str(model_path),
                element, view, str(source_path)]
    raise ValueError(f"unknown tool: {tool!r}")


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def svgs_differ(before: bytes, after: bytes) -> bool:
    return before != after


def run_and_log(name: str, cmd: list[str], out_dir: Path, env: dict | None = None) -> subprocess.CompletedProcess:
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic()
    result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=120)
    elapsed = round(time.monotonic() - t0, 3)
    (out_dir / f"{name}.log").write_text(
        f"$ {' '.join(cmd)}\nexit_code={result.returncode} elapsed_seconds={elapsed}\n\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}\n"
    )
    return result
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_diagram_study_harness.py -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/diagram_study/harness.py tests/test_diagram_study_harness.py
git commit -m "Phase 0 diagram study: reusable render/run harness generalized from run_study.py"
```

## Task 3: Author the four real fixtures and their one-element mutated counterparts

**Files:**
- Create: `decisions/diagram-study-real-fixtures/fixtures/ch05.sysml` (verbatim copy of `models/ch05-cumulative.sysml`)
- Create: `decisions/diagram-study-real-fixtures/fixtures/ch06.sysml` (verbatim copy of `models/ch06-cumulative.sysml`)
- Create: `decisions/diagram-study-real-fixtures/fixtures/ch07.sysml` (verbatim copy of `models/ch07-cumulative.sysml`)
- Create: `decisions/diagram-study-real-fixtures/fixtures/ch08.sysml` (verbatim copy of `models/ch08-cumulative.sysml`)
- Create: `decisions/diagram-study-real-fixtures/fixtures/ch05-mutated.sysml`
- Create: `decisions/diagram-study-real-fixtures/fixtures/ch06-mutated.sysml`
- Create: `decisions/diagram-study-real-fixtures/fixtures/ch07-mutated.sysml`
- Create: `decisions/diagram-study-real-fixtures/fixtures/ch08-mutated.sysml`
- Test: `tests/test_diagram_study_fixtures.py`

**Interfaces:**
- Produces: eight `.sysml` files under `decisions/diagram-study-real-fixtures/fixtures/`, consumed by Tasks 4, 5, 6, 7 as render inputs.

Each fixture is copied byte-for-byte from `models/chNN-cumulative.sysml` (read-only source, never edited). Each `-mutated.sysml` sibling is that same copy with exactly one real, existing element renamed or retargeted — never a new element added — chosen per fixture to be visible in the view that fixture is used for:

| Fixture | Mutation | Exact edit |
|---|---|---|
| `ch05.sysml` | rename the `ControlSystem` port `durationOut` (visible in the interconnection view) | `port durationOut : DurationPort;` → `port durationOutRenamed : DurationPort;`  **and**  `interface durationInterface connect control.durationOut to heating.durationIn;` → `interface durationInterface connect control.durationOutRenamed to heating.durationIn;` |
| `ch06.sysml` | rename the recursive `heatGen` part (visible in the tree/structure view) | `part heatGen : HeatGenerator;` → `part heatGenRenamed : HeatGenerator;`  **and**  `allocation heatGenAllocation allocate ApplyHeat::generateHeat to HeatingAssembly::heatGen;` → `allocation heatGenAllocation allocate ApplyHeat::generateHeat to HeatingAssembly::heatGenRenamed;` |
| `ch07.sysml` | retarget the `Finish` transition (visible in the state view) — the same kind of edit, on the same kind of element, as the original study's own `finishCycle: ready → cancelled` mutation | `transition first heating accept Finish then ready;` → `transition first heating accept Finish then cancelled;` |
| `ch08.sysml` | rename the `rated` part (visible in the tree view and the target of `assert satisfy heatGenerationReq`) | `part rated : ResistanceCoil {` → `part ratedRenamed : ResistanceCoil {`  **and**  `assert satisfy heatGenerationReq by rated;` → `assert satisfy heatGenerationReq by ratedRenamed;` |

- [ ] **Step 1: Write the failing load-validity test for all eight fixtures**

```python
# tests/test_diagram_study_fixtures.py
from pathlib import Path

import opensysml
import pytest

FIXTURES_DIR = Path("decisions/diagram-study-real-fixtures/fixtures")
FIXTURE_NAMES = ["ch05", "ch06", "ch07", "ch08"]


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_baseline_fixture_loads_ok(name):
    conn = opensysml.connect(version="v0.9.0")
    text = (FIXTURES_DIR / f"{name}.sysml").read_text()
    model = conn.load_from_content(text, strict=False)
    assert model.ok, f"{name}.sysml: {[d.message for d in model.diagnostics]}"
    conn.close()


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_mutated_fixture_loads_ok(name):
    conn = opensysml.connect(version="v0.9.0")
    text = (FIXTURES_DIR / f"{name}-mutated.sysml").read_text()
    model = conn.load_from_content(text, strict=False)
    assert model.ok, f"{name}-mutated.sysml: {[d.message for d in model.diagnostics]}"
    conn.close()


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_mutated_fixture_differs_from_baseline_by_exactly_the_documented_edit(name):
    baseline = (FIXTURES_DIR / f"{name}.sysml").read_text().splitlines()
    mutated = (FIXTURES_DIR / f"{name}-mutated.sysml").read_text().splitlines()
    assert len(baseline) == len(mutated), "mutation must not add or remove lines"
    changed = [i for i, (a, b) in enumerate(zip(baseline, mutated)) if a != b]
    assert 1 <= len(changed) <= 2, f"{name}: expected 1-2 changed lines, got {len(changed)}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_diagram_study_fixtures.py -v`
Expected: FAIL — `FileNotFoundError` (fixtures directory doesn't exist yet)

- [ ] **Step 3: Create the fixtures directory and copy the four baseline files verbatim**

```bash
mkdir -p decisions/diagram-study-real-fixtures/fixtures
cp models/ch05-cumulative.sysml decisions/diagram-study-real-fixtures/fixtures/ch05.sysml
cp models/ch06-cumulative.sysml decisions/diagram-study-real-fixtures/fixtures/ch06.sysml
cp models/ch07-cumulative.sysml decisions/diagram-study-real-fixtures/fixtures/ch07.sysml
cp models/ch08-cumulative.sysml decisions/diagram-study-real-fixtures/fixtures/ch08.sysml
```

- [ ] **Step 4: Create each `-mutated.sysml` sibling by applying exactly the one documented edit from the table above to a copy of the corresponding baseline file** (use the Edit tool / `sed` on a copy — never on the baseline itself)

```bash
for n in ch05 ch06 ch07 ch08; do
  cp decisions/diagram-study-real-fixtures/fixtures/$n.sysml decisions/diagram-study-real-fixtures/fixtures/$n-mutated.sysml
done
```

Then apply, to each `-mutated.sysml` file only, exactly the edit(s) shown in the table above (two-line edits for ch05/ch06/ch08, one-line for ch07).

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/test_diagram_study_fixtures.py -v`
Expected: PASS (12 tests)

- [ ] **Step 6: Commit**

```bash
git add decisions/diagram-study-real-fixtures/fixtures/ tests/test_diagram_study_fixtures.py
git commit -m "Phase 0 diagram study: real fixture set (Ch5/6/7/8) plus one-element mutated siblings"
```

## Task 4: Render the four common-model tools against the real-fixture baseline views

**Files:**
- Create: `scripts/diagram_study/run_real_fixture_study.py`
- Test: `tests/test_diagram_study_real_fixture_study.py`

**Interfaces:**
- Consumes: `harness.build_render_command`, `harness.run_and_log`, `harness.hash_bytes` (Task 2); fixture files (Task 3); `provision_check.gather_reported_versions` (Task 1, to resolve tool paths).
- Produces: `FIXTURE_TABLE: list[tuple[str, str, str]]` (fixture name, view, element) and `render_fixture(fixture: str, view: str, element: str, tools: dict, evidence_dir: Path) -> dict` (renders with all applicable tools for that view, returns a per-tool result dict with `exit_code`, `svg_path`, `sha256`), consumed by Task 8's compiled report.

Baseline view table (no mutation yet — that's Task 7):

| Fixture | View | Element | Tools |
|---|---|---|---|
| ch05 | tree | `ToasterDemo::Toaster` | opensysml-puml, opensysml-dot, toolkit, pilot |
| ch05 | interconnection | `ToasterDemo::Toaster` | opensysml-puml, opensysml-dot, toolkit, pilot |
| ch06 | tree | `ToasterDemo::Toaster` | opensysml-puml, opensysml-dot, toolkit, pilot |
| ch07 | tree | `ToasterDemo::Toaster` | opensysml-puml, opensysml-dot, toolkit, pilot |
| ch07 | state | `ToasterDemo::Cycle` | opensysml-puml, opensysml-dot, toolkit, pilot |
| ch08 | tree | `ToasterDemo::Toaster` | opensysml-puml, opensysml-dot, toolkit, pilot |

(action-flow is not retested here: it already existed on the original toy fixture from Ch4 onward and is not one of the features the spec's fixture table names as untested — see Review Focus item 5 and Task 8's scope note.)

- [ ] **Step 1: Write the failing test for the fixture table and a mocked single-tool render**

```python
# tests/test_diagram_study_real_fixture_study.py
from pathlib import Path
from unittest.mock import patch

from scripts.diagram_study.run_real_fixture_study import FIXTURE_TABLE, render_fixture


def test_fixture_table_covers_ch05_ch06_ch07_ch08():
    fixtures_covered = {row[0] for row in FIXTURE_TABLE}
    assert fixtures_covered == {"ch05", "ch06", "ch07", "ch08"}


def test_fixture_table_targets_the_untested_feature_per_fixture():
    views_by_fixture = {}
    for fixture, view, _element in FIXTURE_TABLE:
        views_by_fixture.setdefault(fixture, set()).add(view)
    assert "interconnection" in views_by_fixture["ch05"]
    assert "state" in views_by_fixture["ch07"]
    assert "tree" in views_by_fixture["ch06"]
    assert "tree" in views_by_fixture["ch08"]


def test_render_fixture_records_exit_code_and_hash_per_tool(tmp_path):
    fake_svg = tmp_path / "out.svg"
    with patch("scripts.diagram_study.run_real_fixture_study.harness.run_and_log") as run_mock:
        run_mock.return_value.returncode = 0
        fake_svg.write_bytes(b"<svg>ok</svg>")
        with patch(
            "scripts.diagram_study.run_real_fixture_study._render_one_tool",
            return_value={"exit_code": 0, "svg_path": str(fake_svg), "sha256": "abc"},
        ):
            result = render_fixture(
                "ch05", "tree", "ToasterDemo::Toaster",
                tools={"opensysml": "x", "toolkit": "y", "java": "z", "pilot_jar": "p",
                       "pilot_render_class": "c", "pilot_library": "l"},
                evidence_dir=tmp_path,
            )
    assert set(result.keys()) >= {"opensysml-puml", "opensysml-dot", "toolkit", "pilot"}
    for tool_result in result.values():
        assert "exit_code" in tool_result and "sha256" in tool_result
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_diagram_study_real_fixture_study.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Write `scripts/diagram_study/run_real_fixture_study.py`**

```python
"""Phase 0 driver: renders the real Ch5/6/7/8 fixtures with the four
common-model tools (OpenSysML x2 render-forms, sysml-toolkit, OMG pilot),
at the view/element each fixture exists to test. SysMLD is handled
separately in Task 6 (its schema needs hand-authored intent, not a
model-path CLI argument)."""
import json
from pathlib import Path

from scripts.diagram_study import harness

FIXTURES_DIR = Path("decisions/diagram-study-real-fixtures/fixtures")
EVIDENCE_DIR = Path("decisions/diagram-study-real-fixtures/evidence")

FIXTURE_TABLE: list[tuple[str, str, str]] = [
    ("ch05", "tree", "ToasterDemo::Toaster"),
    ("ch05", "interconnection", "ToasterDemo::Toaster"),
    ("ch06", "tree", "ToasterDemo::Toaster"),
    ("ch07", "tree", "ToasterDemo::Toaster"),
    ("ch07", "state", "ToasterDemo::Cycle"),
    ("ch08", "tree", "ToasterDemo::Toaster"),
]

COMMON_TOOLS = ["opensysml-puml", "opensysml-dot", "toolkit", "pilot"]


def _render_one_tool(tool: str, fixture: str, view: str, element: str, model_path: Path, tools: dict, evidence_dir: Path) -> dict:
    stem = f"{fixture}-{view}-{tool}"
    is_intermediate_form = tool in ("opensysml-puml", "toolkit")
    source_ext = {"opensysml-puml": "puml", "opensysml-dot": "dot", "toolkit": "puml", "pilot": "svg"}[tool]
    source_path = evidence_dir / f"{stem}.{source_ext}"
    cmd = harness.build_render_command(tool, view, element, model_path, source_path, tools)
    emit = harness.run_and_log(f"{stem}-emit", cmd, evidence_dir)
    result = {"exit_code": emit.returncode, "svg_path": None, "sha256": None}
    if emit.returncode != 0:
        return result

    svg_path = evidence_dir / f"{stem}.svg"
    if tool == "opensysml-dot":
        render = harness.run_and_log(f"{stem}-render", ["dot", "-Tsvg", str(source_path), "-o", str(svg_path)], evidence_dir)
        if render.returncode != 0:
            result["exit_code"] = render.returncode
            return result
    elif is_intermediate_form:
        render = harness.run_and_log(
            f"{stem}-render",
            [tools["java"], "-Djava.awt.headless=true", "-jar", tools["plantuml_jar"], "-tsvg", str(source_path)],
            evidence_dir,
        )
        if render.returncode != 0:
            result["exit_code"] = render.returncode
            return result
        # PlantUML writes {stem}.svg next to {stem}.puml, i.e. exactly svg_path already.
    else:
        svg_path = source_path  # pilot writes SVG directly

    if svg_path.exists():
        data = svg_path.read_bytes()
        result["svg_path"] = str(svg_path)
        result["sha256"] = harness.hash_bytes(data)
    return result


def render_fixture(fixture: str, view: str, element: str, tools: dict, evidence_dir: Path) -> dict:
    model_path = FIXTURES_DIR / f"{fixture}.sysml"
    return {
        tool: _render_one_tool(tool, fixture, view, element, model_path, tools, evidence_dir)
        for tool in COMMON_TOOLS
    }


def main(tools: dict) -> dict:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for fixture, view, element in FIXTURE_TABLE:
        manifest[f"{fixture}-{view}"] = render_fixture(fixture, view, element, tools, EVIDENCE_DIR)
    (EVIDENCE_DIR / "real-fixture-results.json").write_text(json.dumps(manifest, indent=2))
    return manifest


if __name__ == "__main__":
    # tools dict must be filled in from Task 1's provisioning report before running for real
    raise SystemExit("run via a small wrapper that resolves `tools` from provisioning-report.json")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_diagram_study_real_fixture_study.py -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Run the driver for real, using the tool binary paths confirmed present by Task 1's provisioning check** (`provisioning-report.json` records *versions*, not paths — the paths below are the ones Task 1 Step 5 confirmed exist at those pinned versions)

```bash
uv run python -c "
import json
from pathlib import Path
from scripts.diagram_study.run_real_fixture_study import main

report = json.loads(Path('decisions/diagram-study-real-fixtures/evidence/provisioning-report.json').read_text())
tools = {
    'opensysml': '/private/tmp/toaster-diagram-study/opensysml-current',
    'toolkit': str(Path.home() / 'Documents/GitHub/sysml-toolkit/target/release/sysmlv2'),
    'java': '/usr/bin/java',
    'plantuml_jar': '/opt/homebrew/opt/plantuml/libexec/plantuml.jar',
    'pilot_jar': '/private/tmp/toaster-diagram-study/pilot/sysml/jupyter-sysml-kernel-0.62.0-all.jar',
    'pilot_render_class': '/private/tmp/toaster-diagram-study/PilotRender.java',
    'pilot_library': '/private/tmp/toaster-diagram-study/pilot/sysml/sysml.library',
}
main(tools)
"
```

Inspect `decisions/diagram-study-real-fixtures/evidence/real-fixture-results.json`: every `exit_code` should be recorded (0 or not — a nonzero exit for a given tool/fixture/view combination is itself a valid Phase 0 finding, not a script bug). For any tool that fails on a real fixture, read its `.log` file and record the failure reason in Task 8's deliverable rather than treating it as blocking — this is expected per Review Focus item 1: real content may break a tool the toy fixture never stressed.

- [ ] **Step 6: For every successful render, confirm the fixture's target element name actually appears in the emitted source** (catches Review Focus item 2 — a tool that "succeeds" while dropping the feature)

```bash
for f in decisions/diagram-study-real-fixtures/evidence/ch05-interconnection-*.puml decisions/diagram-study-real-fixtures/evidence/ch05-interconnection-*.dot; do
  [ -f "$f" ] && grep -l "durationIn\|durationOut" "$f" || echo "MISSING port reference in $f"
done
```

Record any `MISSING` line in Task 8's deliverable as a real, named capability gap (matching the original study's own honest reporting of the OpenSysML port-collapse limitation).

- [ ] **Step 7: Commit**

```bash
git add scripts/diagram_study/run_real_fixture_study.py tests/test_diagram_study_real_fixture_study.py decisions/diagram-study-real-fixtures/evidence/real-fixture-results.json
git commit -m "Phase 0 diagram study: render OpenSysML/toolkit/pilot against real Ch5/6/7/8 baseline views"
```

## Task 5: Probe allocation/requirement-view support on Ch6/Ch8 (untested territory)

**Files:**
- Create: `scripts/diagram_study/probe_new_view_types.py`
- (writes to) `decisions/diagram-study-real-fixtures/evidence/view-type-probe.json`

The original toy fixture never exercised an allocation view or a requirement-satisfaction view with any of the four common-model tools — the spec names this directly as untested territory. **One answer is already known from evidence gathered while writing this plan:** `sysml-toolkit viz --help` (v0.9.1, the exact pinned build) lists exactly seven `--view` values — `tree, interconnection, state, action, sequence, case, mixed` — with no `allocation` or `requirement` kind. sysml-toolkit does not support either view type; record this directly, no live probe needed for that tool.

- [ ] **Step 1: Record the already-known sysml-toolkit finding**

```bash
mkdir -p decisions/diagram-study-real-fixtures/evidence
cat > decisions/diagram-study-real-fixtures/evidence/toolkit-view-help.log <<'EOF'
$ sysmlv2 viz --help (v0.9.1, commit af839f0d22723772676e509213c65756d1e08ef2)
Possible --view values: tree, interconnection, state, action, sequence, case, mixed
No allocation or requirement view kind exists in this CLI.
EOF
```

- [ ] **Step 2: Probe OpenSysML's render-form/view support**

```bash
/private/tmp/toaster-diagram-study/opensysml-current -help 2>&1 | tee decisions/diagram-study-real-fixtures/evidence/opensysml-help.log
```

Read the output for any view kind resembling `allocation` or `requirement` alongside the already-known `tree`/`interconnection`/`action`/`state`. Record the answer (present or absent) in `view-type-probe.json` (Step 4).

- [ ] **Step 3: Probe the pilot's supported `viz` kinds**

```bash
java -Djava.awt.headless=true -cp /private/tmp/toaster-diagram-study/pilot/sysml/jupyter-sysml-kernel-0.62.0-all.jar \
  /private/tmp/toaster-diagram-study/PilotRender.java 2>&1 | tee decisions/diagram-study-real-fixtures/evidence/pilot-help.log
```

(`PilotRender.java`'s own `args.length==0` branch prints `s.help("viz")` — this is a ready-made hook for exactly this probe, no new tool code needed.) Record the answer in `view-type-probe.json`.

- [ ] **Step 4: Write `scripts/diagram_study/probe_new_view_types.py` compiling the three findings**

```python
"""Records whether each of the four common-model tools has an allocation-view
or requirement-view kind at all — untested territory the original toy fixture
never exercised. sysml-toolkit's answer is already known (see Step 1's log);
opensysml and pilot are read from their captured --help output (Steps 2-3)."""
import json
from pathlib import Path

EVIDENCE_DIR = Path("decisions/diagram-study-real-fixtures/evidence")


def compile_probe_result(opensysml_supports: dict, pilot_supports: dict) -> dict:
    return {
        "sysml-toolkit": {"allocation": False, "requirement": False,
                           "source": "toolkit-view-help.log (v0.9.1 --help, seven view kinds, neither present)"},
        "opensysml": opensysml_supports,
        "pilot": pilot_supports,
        "sysmld": {"allocation": True, "requirement": True,
                   "source": "sysml2d/src/sysmld/allocation_view.py and requirement_view.py exist; "
                              "see Task 6 for why Phase 0 does not author real-fixture intent for either "
                              "(scoped out — see Review Focus item 5 in the plan)"},
    }


def main() -> None:
    # opensysml_supports / pilot_supports are filled in by hand after reading
    # evidence/opensysml-help.log and evidence/pilot-help.log (Steps 2-3) —
    # there is no automatic parser for either tool's free-text help output.
    result = compile_probe_result(
        opensysml_supports={"allocation": None, "requirement": None, "source": "see opensysml-help.log"},
        pilot_supports={"allocation": None, "requirement": None, "source": "see pilot-help.log"},
    )
    (EVIDENCE_DIR / "view-type-probe.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
```

Run it, then hand-edit the `None` placeholders in `view-type-probe.json` to `true`/`false` based on what Steps 2-3's logs actually show (this is intentionally a recorded-by-hand step, not automated text parsing of two different tools' free-text help output — automating a parser for output you're reading once is not worth the maintenance cost).

Run: `uv run python -m scripts.diagram_study.probe_new_view_types`

- [ ] **Step 5: Commit**

```bash
git add scripts/diagram_study/probe_new_view_types.py decisions/diagram-study-real-fixtures/evidence/toolkit-view-help.log decisions/diagram-study-real-fixtures/evidence/opensysml-help.log decisions/diagram-study-real-fixtures/evidence/pilot-help.log decisions/diagram-study-real-fixtures/evidence/view-type-probe.json
git commit -m "Phase 0 diagram study: probe allocation/requirement-view support across all four common tools"
```

## Task 6: Author SysMLD intent files for Ch5 interconnection and Ch7 state, render both

SysMLD/sysml2d needs hand-authored diagram-intent JSON (its `compose` step), not a bare model path. The original study proved out exactly two view kinds end-to-end with real compose→render→validate success: `InterconnectionView` (`toaster-mech-composed.json`) and `StateView` (`toaster-stm.json`) — both read in full while writing this plan. `AllocationView` and `RequirementView` exist in `sysml2d`'s source but neither has a worked example to authors against, and `RequirementView`'s actual schema (rank/order-based requirement-derivation nodes with `derive`/`refine`/`trace` edges) doesn't fit what Ch8's real content has (two independent requirements, each satisfied or not by a specific part usage — no derivation relationship between them at all). **This task deliberately scopes SysMLD to the two view kinds the original study actually validated**, on the two real fixtures those view kinds map to (Ch5 interconnection, Ch7 state); `AllocationView`/`RequirementView` against real content is named as an explicit gap in Task 8's deliverable, not attempted here.

`sysmld`'s CLI resolves `model_files` relative to the process's current working directory (confirmed from `check_sysmld_mutation.py`, which copies its target `.sysml` file into the same temp directory as the intent JSON before invoking `compose`/`render`/`validate`). This task colocates copies of the Ch5 and Ch7 fixtures inside `sysml2d-intent/` for exactly that reason — a second, deliberate copy alongside Task 3's canonical ones under `fixtures/`, not a duplication oversight.

**Files:**
- Create: `decisions/diagram-study-real-fixtures/sysml2d-intent/ch05-interconnection.json`
- Create: `decisions/diagram-study-real-fixtures/sysml2d-intent/ch07-state.json`
- Create: `decisions/diagram-study-real-fixtures/sysml2d-intent/ch05.sysml` (copy, for sysmld's cwd-relative `model_files` resolution)
- Create: `decisions/diagram-study-real-fixtures/sysml2d-intent/ch07.sysml` (copy, same reason)
- Create: `decisions/diagram-study-real-fixtures/sysml2d-intent/ch07-mutated.sysml` (copy of Task 3's `ch07-mutated.sysml`, same reason — used in Task 7)

- [ ] **Step 1: Copy the two fixtures sysmld needs alongside where its intent JSON will live**

```bash
mkdir -p decisions/diagram-study-real-fixtures/sysml2d-intent
cp decisions/diagram-study-real-fixtures/fixtures/ch05.sysml decisions/diagram-study-real-fixtures/sysml2d-intent/ch05.sysml
cp decisions/diagram-study-real-fixtures/fixtures/ch07.sysml decisions/diagram-study-real-fixtures/sysml2d-intent/ch07.sysml
cp decisions/diagram-study-real-fixtures/fixtures/ch07-mutated.sysml decisions/diagram-study-real-fixtures/sysml2d-intent/ch07-mutated.sysml
```

- [ ] **Step 2: Author `ch05-interconnection.json`**, following `toaster-mech-composed.json`'s schema, with every alias copied verbatim from the real `ch05.sysml` text (Review Focus item 4 — no retyped-from-memory element names):

```json
{
  "diagram": "ch05-interconnection",
  "kind": "InterconnectionView",
  "name": "Ch5 Duration Interface (Real Fixture)",
  "subject": "toaster",
  "model_files": ["ch05.sysml"],
  "direction": "left-right",
  "default_w": 160,
  "default_h": 80,
  "aliases": {
    "toaster": "ToasterDemo::Toaster",
    "heating": "ToasterDemo::Toaster::heating",
    "control": "ToasterDemo::Toaster::control",
    "conn-control-heating": "ToasterDemo::Toaster::durationInterface"
  },
  "nodes": {
    "heating": {"label": "heating : HeatingSystem", "style": "part.mechanical"},
    "control": {"label": "control : ControlSystem", "style": "part.control"}
  },
  "edges": [
    {"from": "control", "to": "heating", "label": "duration", "model_ref": "conn-control-heating"}
  ],
  "styles": {
    "part.mechanical": {"fill": "#E8F5E9", "stroke": "#2E7D32", "stroke_width": 2, "corner_radius": 10},
    "part.control": {"fill": "#E3F2FD", "stroke": "#1565C0", "stroke_width": 2, "corner_radius": 10}
  }
}
```

- [ ] **Step 3: Author `ch07-state.json`**, following `toaster-stm.json`'s schema, with every alias copied verbatim from the real `ch07.sysml` text. The two triggerless transitions (`ready → idle`, `cancelled → idle`) get no `model_ref`, matching the original example's own `initial → idle` transition (which also has no `model_ref`):

```json
{
  "diagram": "ch07-state",
  "kind": "StateView",
  "name": "Ch7 Toasting Cycle (Real Fixture)",
  "subject": "cycle",
  "model_files": ["ch07.sysml"],
  "direction": "left-right",
  "default_w": 130,
  "default_h": 60,
  "aliases": {
    "cycle": "ToasterDemo::Cycle",
    "idle": "ToasterDemo::Cycle::idle",
    "heating": "ToasterDemo::Cycle::heating",
    "ready": "ToasterDemo::Cycle::ready",
    "cancelled": "ToasterDemo::Cycle::cancelled",
    "start": "ToasterDemo::Start",
    "finish": "ToasterDemo::Finish",
    "cancel": "ToasterDemo::Cancel"
  },
  "states": {
    "initial": {"initial": true},
    "idle": {"label": "Idle", "model_ref": "idle"},
    "heating": {"label": "Heating", "model_ref": "heating"},
    "ready": {"label": "Ready", "model_ref": "ready"},
    "cancelled": {"label": "Cancelled", "model_ref": "cancelled"}
  },
  "transitions": [
    {"from": "initial", "to": "idle", "label": ""},
    {"from": "idle", "to": "heating", "label": "Start", "model_ref": "start"},
    {"from": "heating", "to": "ready", "label": "Finish", "model_ref": "finish"},
    {"from": "heating", "to": "cancelled", "label": "Cancel", "model_ref": "cancel"},
    {"from": "ready", "to": "idle", "label": ""},
    {"from": "cancelled", "to": "idle", "label": ""}
  ]
}
```

- [ ] **Step 4: Compose, render, and strict-validate both, exactly mirroring `run_study.py`'s own sysml2d loop**

```bash
cd decisions/diagram-study-real-fixtures/sysml2d-intent
PYTHONPATH=/private/tmp/toaster-diagram-study/sysml2d/src python3 -c "from sysmld.cli import main; raise SystemExit(main())" interconnection ch05-interconnection.json
PYTHONPATH=/private/tmp/toaster-diagram-study/sysml2d/src python3 -c "from sysmld.cli import main; raise SystemExit(main())" render ch05-interconnection.sysmld
PYTHONPATH=/private/tmp/toaster-diagram-study/sysml2d/src python3 -c "from sysmld.cli import main; raise SystemExit(main())" validate ch05-interconnection.sysmld --strict

PYTHONPATH=/private/tmp/toaster-diagram-study/sysml2d/src python3 -c "from sysmld.cli import main; raise SystemExit(main())" state ch07-state.json
PYTHONPATH=/private/tmp/toaster-diagram-study/sysml2d/src python3 -c "from sysmld.cli import main; raise SystemExit(main())" render ch07-state.sysmld
PYTHONPATH=/private/tmp/toaster-diagram-study/sysml2d/src python3 -c "from sysmld.cli import main; raise SystemExit(main())" validate ch07-state.sysmld --strict
cd -
```

Expected: all six commands exit 0; `ch05-interconnection.svg` and `ch07-state.svg` exist in `sysml2d-intent/`. If `validate --strict` reports an unresolved alias, the alias's target name was copied wrong from the real fixture — re-check it against `fixtures/ch05.sysml`/`ch07.sysml` directly, don't guess.

- [ ] **Step 5: Copy the two SVGs and compose/render/validate logs into the evidence folder**

```bash
mkdir -p ../evidence
cp decisions/diagram-study-real-fixtures/sysml2d-intent/ch05-interconnection.svg decisions/diagram-study-real-fixtures/evidence/sysmld-ch05-interconnection.svg
cp decisions/diagram-study-real-fixtures/sysml2d-intent/ch07-state.svg decisions/diagram-study-real-fixtures/evidence/sysmld-ch07-state.svg
```

- [ ] **Step 6: Commit**

```bash
git add decisions/diagram-study-real-fixtures/sysml2d-intent/ decisions/diagram-study-real-fixtures/evidence/sysmld-*.svg
git commit -m "Phase 0 diagram study: SysMLD intent files and renders for Ch5 interconnection and Ch7 state"
```

## Task 7: Run the mutation-control test for every tool that rendered Ch5/Ch7

**Files:**
- Create: `scripts/diagram_study/mutation_control.py`
- Test: `tests/test_diagram_study_mutation_control.py`

**Interfaces:**
- Consumes: `harness.svgs_differ`, `harness.hash_bytes` (Task 2); Task 4's baseline SVGs and Task 6's SysMLD SVGs; `ch05-mutated.sysml`/`ch07-mutated.sysml` (Task 3).
- Produces: `mutation_control_result(tool: str, baseline_svg: bytes, mutated_svg: bytes) -> dict` (pure — the Review Focus item 3 gate lives here: asserts the baseline SVG is non-trivial before comparing).

This is the check that caught SysMLD's silent staleness on the toy fixture. It runs here for every candidate that rendered Ch5 (interconnection: opensysml-puml, opensysml-dot, toolkit, pilot, sysmld) and Ch7 (state: the same five), against each fixture's mutated sibling from Task 3/Task 6.

- [ ] **Step 1: Write the failing test for the pure result function, including the vacuous-pass guard**

```python
# tests/test_diagram_study_mutation_control.py
import pytest

from scripts.diagram_study.mutation_control import mutation_control_result


def test_changed_svg_is_reported_as_a_catch():
    result = mutation_control_result("opensysml-dot", b"<svg>before-content-here</svg>", b"<svg>after-content-different</svg>")
    assert result["baseline_rendered"] is True
    assert result["svg_changed"] is True
    assert result["verdict"] == "reflects the mutation"


def test_unchanged_svg_is_reported_as_stale():
    same = b"<svg>identical-content</svg>"
    result = mutation_control_result("sysmld", same, same)
    assert result["baseline_rendered"] is True
    assert result["svg_changed"] is False
    assert result["verdict"] == "STALE: picture unchanged after a real model edit"


def test_empty_baseline_raises_instead_of_a_vacuous_pass():
    with pytest.raises(ValueError, match="baseline render is empty"):
        mutation_control_result("pilot", b"", b"<svg>after</svg>")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_diagram_study_mutation_control.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Write `scripts/diagram_study/mutation_control.py`**

```python
"""The real-fixture mutation-control test: change one real element, re-render,
diff. This is the exact check that caught SysMLD's silent staleness on the
original toy fixture (see check_sysmld_mutation.py); it runs here for every
tool that rendered a mutable view, not just the ones expected to pass."""
from scripts.diagram_study.harness import svgs_differ


def mutation_control_result(tool: str, baseline_svg: bytes, mutated_svg: bytes) -> dict:
    if not baseline_svg:
        raise ValueError(f"{tool}: baseline render is empty — cannot run a meaningful mutation-control comparison")
    changed = svgs_differ(baseline_svg, mutated_svg)
    return {
        "tool": tool,
        "baseline_rendered": True,
        "svg_changed": changed,
        "verdict": "reflects the mutation" if changed else "STALE: picture unchanged after a real model edit",
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_diagram_study_mutation_control.py -v`
Expected: PASS (3 tests)

- [ ] **Step 5: Re-render the four common tools against `ch05-mutated.sysml` (interconnection) and `ch07-mutated.sysml` (state)**, reusing Task 4's `render_fixture`:

```bash
uv run python -c "
import json
from pathlib import Path
from scripts.diagram_study.run_real_fixture_study import render_fixture

tools = {  # same dict as Task 4 Step 5
    'opensysml': '/private/tmp/toaster-diagram-study/opensysml-current',
    'toolkit': str(Path.home() / 'Documents/GitHub/sysml-toolkit/target/release/sysmlv2'),
    'java': '/usr/bin/java', 'plantuml_jar': '/opt/homebrew/opt/plantuml/libexec/plantuml.jar',
    'pilot_jar': '/private/tmp/toaster-diagram-study/pilot/sysml/jupyter-sysml-kernel-0.62.0-all.jar',
    'pilot_render_class': '/private/tmp/toaster-diagram-study/PilotRender.java',
    'pilot_library': '/private/tmp/toaster-diagram-study/pilot/sysml/sysml.library',
}
evidence = Path('decisions/diagram-study-real-fixtures/evidence')
mutated_dir = Path('decisions/diagram-study-real-fixtures/fixtures')
# render_fixture reads FIXTURES_DIR/{fixture}.sysml; point it at the mutated copy by fixture-naming it ch05-mutated / ch07-mutated
import scripts.diagram_study.run_real_fixture_study as rfs
rfs.FIXTURES_DIR = mutated_dir
result_i = rfs.render_fixture('ch05-mutated', 'interconnection', 'ToasterDemo::Toaster', tools, evidence)
result_s = rfs.render_fixture('ch07-mutated', 'state', 'ToasterDemo::Cycle', tools, evidence)
(evidence / 'mutation-rerenders.json').write_text(json.dumps({'ch05': result_i, 'ch07': result_s}, indent=2))
"
```

- [ ] **Step 6: Re-render SysMLD against `ch07-mutated.sysml`** (same intent JSON — the transition's `to` target stays literally `"ready"` in the intent file even though the real model now points `Finish` at `cancelled`; if the picture doesn't change, that mismatch is exactly what the check is designed to catch):

```bash
cd decisions/diagram-study-real-fixtures/sysml2d-intent
cp ch07-mutated.sysml ch07.sysml.bak_swap && mv ch07.sysml ch07.sysml.orig && cp ch07-mutated.sysml ch07.sysml
PYTHONPATH=/private/tmp/toaster-diagram-study/sysml2d/src python3 -c "from sysmld.cli import main; raise SystemExit(main())" state ch07-state.json
PYTHONPATH=/private/tmp/toaster-diagram-study/sysml2d/src python3 -c "from sysmld.cli import main; raise SystemExit(main())" render ch07-state.sysmld
mv ch07-state.svg ../evidence/sysmld-ch07-state-mutated.svg
mv ch07.sysml.orig ch07.sysml && rm ch07.sysml.bak_swap
cd -
```

- [ ] **Step 7: Compute every `mutation_control_result` and write the compiled verdicts**

```python
# run interactively or as a short one-off script
import json
from pathlib import Path
from scripts.diagram_study.mutation_control import mutation_control_result

evidence = Path("decisions/diagram-study-real-fixtures/evidence")
baseline = json.loads((evidence / "real-fixture-results.json").read_text())
mutated = json.loads((evidence / "mutation-rerenders.json").read_text())

results = {}
for tool in ["opensysml-puml", "opensysml-dot", "toolkit", "pilot"]:
    b_path = baseline["ch05-interconnection"][tool]["svg_path"]
    m_path = mutated["ch05"][tool]["svg_path"]
    if b_path and m_path:
        results[f"ch05-interconnection-{tool}"] = mutation_control_result(
            tool, Path(b_path).read_bytes(), Path(m_path).read_bytes()
        )
    b_path = baseline["ch07-state"][tool]["svg_path"]
    m_path = mutated["ch07"][tool]["svg_path"]
    if b_path and m_path:
        results[f"ch07-state-{tool}"] = mutation_control_result(
            tool, Path(b_path).read_bytes(), Path(m_path).read_bytes()
        )

results["ch07-state-sysmld"] = mutation_control_result(
    "sysmld",
    (evidence / "sysmld-ch07-state.svg").read_bytes(),
    (evidence / "sysmld-ch07-state-mutated.svg").read_bytes(),
)

(evidence / "mutation-control-results.json").write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
```

Read the printed output. **The `sysmld` verdict is the headline result this task exists to reproduce or refute against real content** — the original study found it STALE on the toy fixture; confirm whether that holds here too, and record whichever answer the evidence actually shows (this is a real trade-study finding, not a foregone conclusion — do not assume the toy-fixture result carries over without checking).

- [ ] **Step 8: Commit**

```bash
git add scripts/diagram_study/mutation_control.py tests/test_diagram_study_mutation_control.py decisions/diagram-study-real-fixtures/evidence/mutation-rerenders.json decisions/diagram-study-real-fixtures/evidence/mutation-control-results.json decisions/diagram-study-real-fixtures/evidence/sysmld-ch07-state-mutated.svg
git commit -m "Phase 0 diagram study: mutation-control test against real fixtures, all five candidates"
```

## Task 8: Compile the deliverable and log a decision entry

**Files:**
- Create: `decisions/diagram-study-real-fixtures.md`
- Modify: `decisions/log.md` (append one new DL entry — re-check the file's current tail with `grep -o "^## DL-[0-9]*" decisions/log.md | sort -t- -k2 -n | tail -3` immediately before writing, since other work may have landed on this branch since this plan was written)

**Interfaces:**
- Consumes: every `evidence/*.json` file from Tasks 1, 4, 5, 7, and the two `sysmld-*.svg` outputs from Task 6.

- [ ] **Step 1: Write `decisions/diagram-study-real-fixtures.md`**, mirroring the original study's `report.md` structure (Decision brief / Method and evidence / Alternatives exercised table / Model-to-picture integrity / scope boundary). Pull the actual exit codes, hashes, and verdicts from the four `evidence/*.json` files written by Tasks 1/4/5/7 rather than re-describing them from memory. The document must include, as its own explicit section (Review Focus item 5): which of the original study's 4 view types × 5 tools were rerun here (interconnection+state on the four common tools plus SysMLD, tree everywhere, allocation/requirement-view probed but not rendered) and which were not (action-flow; DEMA SysML2Tools entirely; AllocationView/RequirementView content-authoring for SysMLD).

- [ ] **Step 2: Self-check the deliverable against the evidence files**

```bash
uv run python -c "
import json
from pathlib import Path
evidence = Path('decisions/diagram-study-real-fixtures/evidence')
for f in ['real-fixture-results.json', 'mutation-control-results.json', 'view-type-probe.json', 'provisioning-report.json']:
    data = json.loads((evidence / f).read_text())
    print(f, '- present, ', len(json.dumps(data)), 'bytes')
"
```

Confirm every number/verdict cited in `decisions/diagram-study-real-fixtures.md` traces back to one of these four files.

- [ ] **Step 3: Log the decision entry** — after re-checking the current DL tail per the file note above, append a `## DL-0NN` entry recording: Phase 0 complete, real-fixture capability matrix at `decisions/diagram-study-real-fixtures.md`, and — critically — whether the original SysMLD mutation-control finding held or was refuted against real content (Task 7 Step 7's headline result), since that's the fact Phase 1's tool recommendations will most directly depend on.

- [ ] **Step 4: Commit**

```bash
git add decisions/diagram-study-real-fixtures.md decisions/log.md
git commit -m "Phase 0 diagram study: compiled real-fixture capability matrix and decision log entry"
```

---

## Self-Review Notes

**Spec coverage:** Every "Why needed" / fixture-table row / Method / Deliverable line in the spec's Phase 0 section maps to a task above (fixtures → Task 3; all four originally-covered tools → Tasks 4/6; mutation-control for every candidate → Task 7; `decisions/diagram-study-real-fixtures.md` + evidence folder mirroring the original study's structure → Task 8). Phase 1 and implementation are untouched, per the spec's own Non-goals.

**Known scope boundaries, stated here so a later reader doesn't assume more happened than did:** DEMA SysML2Tools is not rendered anywhere in this plan (the approved spec's own Phase 0 method names four tools, not five). SysMLD's `AllocationView`/`RequirementView` kinds are not authored against real content (Task 6) — only `InterconnectionView` and `StateView`, the two the original study actually proved out end-to-end. Action-flow views are not rerun on real fixtures (not one of the spec's named untested gaps). These three boundaries are exactly the kind of thing Review Focus item 5 exists to keep visible in the compiled deliverable.
