# Diagram Survey Phase 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: execute this plan through this repository's own orchestrator/builder/reviewer harness, **not** a generic subagent skill — one `decisions/work-contract-template.md` contract per task below, a `builder` (`.claude/agents/builder.md`) implementing it in its own worktree on a pinned model, and a `reviewer` (`.claude/agents/reviewer.md`) on a *different* pinned model re-running every acceptance check independently before merge, per `.claude/skills/orchestrator-protocol/SKILL.md`'s "Plan-driven non-chapter work" section. This is the exact mechanism `CONTRACT CH05-TOOLKIT-VIZ` already used (`decisions/log.md` DL-086): that one task's own review cycle caught a vacuous test assertion and two unflagged visual-quality defects a build-only pass missed entirely. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the 16 diagrams `decisions/diagram-survey.md` already recommends into Chapters 1-4, 6-8, and 10's shipped notebooks, replacing or supplementing the text-heavy outputs it identified, using only tools and placements that document already specifies.

**Architecture:** One shared infrastructure task (Task 1) closes a real, newly-discovered reproducibility gap — OpenSysML's `-render` CLI, needed for every action-flow and state-transition diagram, has never been provisioned through this tutorial's own `uv sync`/`scripts/check-tools.py` path — then adds `render_action_flow()`/`render_state_flow()` to `src/toaster/render.py`, completing a function that has been a `NotImplementedError` stub since the chapter-build era. Tasks 2-10, one per chapter, each insert exactly the diagrams `decisions/diagram-survey.md` specifies, using that function plus the three renderers Phase 1's own tooling already proved (`model_to_dot`/`containment_subgraph`, `render_interconnection`/`build_interconnection_intent`, and — for Chapter 5's one remaining candidate only — `model_to_dot` unscoped), re-executing each notebook end to end and updating exactly the narration cells the survey calls for.

**Tech Stack:** Python (`src/toaster/render.py`, `src/toaster/bootstrap.py`), OpenSysML's pinned `v0.9.0` CLI binary (new: provisioned from its own GitHub release asset, distinct from the `sysml-grpc` service binary `opensysml.binary` already provisions), Graphviz (already a dependency, unchanged), `jupyter nbconvert` for end-to-end notebook re-execution.

**Spec:** [`docs/superpowers/specs/2026-09-28-diagram-survey-design.md`](../specs/2026-09-28-diagram-survey-design.md) (Phase 2 — Phase 1's own Non-goals explicitly left this unspecced). Source of truth for every diagram's exact cell, tool, and add-vs-replace decision: [`decisions/diagram-survey.md`](../../../decisions/diagram-survey.md) — tasks below implement it; they do not re-derive placements.

## Global Constraints

- Never use the OMG pilot or SysMLD/sysml2d for any diagram — both confirmed to fail on all real content (`decisions/diagram-study-real-fixtures.md`).
- Never invent a diagram for content `decisions/diagram-survey.md` already found has no tool support in this tutorial (Ch2's requirement/override content, Ch3's requirement/verification-case content, Ch8's satisfy/verify/proof content, Ch9 entirely, Ch10's allocation/judgment/sign-off content) — each chapter's task below carries that chapter's own specific exclusions forward verbatim.
- Every notebook edit touches already-shipped, already-reviewed content — the same class of work `CONTRACT CH05-TOOLKIT-VIZ` already did once. Every chapter task's acceptance criteria require re-executing the full notebook via `nbconvert` and confirming exit 0 with no cell errors, not just that the new cell's own code runs in isolation.
- Diagrams are presentation only — a diagram may never assert something the model does not already state, and layout/palette choices never carry engineering content (`AGENTS.md`'s diagrams-as-derived-views principle, already applied throughout `render.py`).
- `uv run pytest tests/ glossary/tests/ -q` (423 passed, 7 deselected, before this plan) and `uv run python scripts/check_construction.py --check` must stay clean after every task.
- Every new or modified function keeps the file's existing style: no new third-party dependency (Task 1 adds `tarfile`, stdlib only), explicit required arguments over silent environment-variable resolution where `render_toolkit_interconnection` already established that pattern (`ToolkitRenderError`-style named errors, not raw exceptions).

## Review Focus

- **A chapter's own diagram root choice reaching the wrong content.** `decisions/diagram-study-real-fixtures.md`'s own "wrong root chosen" finding (rooting at `Toaster` never reaches `heatGen`) is a real, already-proven failure mode — Task 7 (Ch6) and Task 10 (Ch10) both root away from the default `Toaster`/package level for exactly this reason; each task's own acceptance criteria assert the specific qualified names the diagram must (and must not) contain, not just that *a* diagram rendered.
- **A narration cell left describing the old figure after the tool or content changes.** `CONTRACT CH05-TOOLKIT-VIZ`'s own revision cycle fixed exactly this once already. Every task below names the exact narration text to update and what it must say instead.
- **The CLI binary silently resolving to the wrong build.** Task 1's own binary is pinned by version and SHA256, cached at a stable path distinct from `sysml-grpc`; a chapter task must never hardcode `/private/tmp/...` or any other machine-specific path (the exact mistake this plan's own investigation found and is fixing).
- **An "add" diagram accidentally becoming a silent "replace."** Most of `decisions/diagram-survey.md`'s placements are "add" (insert a new cell, keep the existing text cell) — a task that deletes or shrinks the existing narration while adding a diagram has gone beyond its own brief; each task states explicitly which existing cells must survive unchanged.
- **A diagram rendered once but never actually inspected.** `CONTRACT CH05-TOOLKIT-VIZ`'s own real defects (a connector crossing a label, a vacuous test) were both things that "looked done" from exit code 0 alone. Every chapter task requires an actual content check of the rendered output (a specific string present in the `.dot`/`.svg`/`.puml`, not just that a file was written), matching the survey's own cited evidence style.

---

## Task 1: OpenSysML CLI provisioning, `render_action_flow()`, `render_state_flow()`

**Files:**
- Modify: `src/toaster/bootstrap.py` (add CLI binary provisioning)
- Modify: `src/toaster/render.py:481` (implement the `render_action_flow` stub; add `render_state_flow`)
- Modify: `docs/setup.md` (document the new provisioning step)
- Test: `tests/test_bootstrap_cli_binary.py` (new)
- Test: `tests/test_render_action_state_flow.py` (new)

**Interfaces:**
- Produces: `toaster.bootstrap.ensure_cli_binary(version: str = "v0.9.0") -> Path` — downloads, SHA256-verifies, and caches OpenSysML's render-capable CLI binary (distinct from `opensysml.binary.ensure_binary()`, which provisions the unrelated `sysml-grpc` service binary), returns its path. Cache hit returns immediately without a network call.
- Produces: `toaster.render.render_action_flow(model: Any, name: str, out: str | Path, *, binary: str | Path | None = None) -> None` — the stub's own original signature, now implemented. `binary=None` (the default) calls `ensure_cli_binary()`; an explicit path skips provisioning (matches the chapter notebooks' own existing `BINARY = Path.home() / "Documents/GitHub/sysml-toolkit/..."`-style explicit-path convention where a chapter wants to pin a specific local build).
- Produces: `toaster.render.render_state_flow(model: Any, name: str, out: str | Path, *, binary: str | Path | None = None) -> None` — identical shape and shared implementation, `#state:` instead of `#action:`.
- Consumes (Tasks 5, 7, 8): both of the above.

### Background this task's implementer needs (already verified directly in this session, not to be re-derived)

OpenSysML's `v0.9.0` GitHub release (`Open-MBEE/OpenSysML`) publishes a CLI binary as a *separate* asset from the `sysml-grpc` service binary `opensysml.binary.ensure_binary()` already provisions — named `sysml-<os>-<arch>.tar.gz`, not `sysml-grpc-<os>-<arch>`. Confirmed by downloading and testing the real `darwin-arm64` asset in this session: it reports `sysml v0.9.0`, commit `ee54ea03ea3ca8fb2c796ecda364adf748c40304` (the exact same build Phase 0's own capability matrix, `decisions/diagram-study-real-fixtures.md`, used), and correctly renders both `-render '#action:ToasterDemo::ApplyHeat' -render-form dot` (against the real `models/ch06-cumulative.sysml`) and `-render '#state:ToasterDemo::Cycle' -render-form dot` (against the real `models/ch07-cumulative.sysml`), with transition edges labeled by their real trigger text (confirmed: `"n1" -> "n2" [label="accept Start"]`).

The tarball extracts to a single file at its top level, named `sysml-<os>-<arch>` (platform-suffixed, not bare `sysml`) — confirmed directly: `tar -tzf sysml-darwin-arm64.tar.gz` → `sysml-darwin-arm64`.

Real, verified SHA256 hashes from the release's own `SHA256SUMS.txt`, pinned for `v0.9.0`:

```
darwin-amd64: c4efdbcfd698ac9adb1ba64aca5adcd2d4caecf6299140da77eb9c2a8f1a4874
darwin-arm64: 0129f277bd10c73ca09c7ce643cf7ae9b6b496250925d1a640ef1e2930340efb
linux-amd64:  3e9a2070261cd08bd7363abf3a836c3adb5b92f488668548734bdce7b6bd8fa1
linux-arm64:  c74dbd818e1cf2aa082bf6f0c23759a661ed4af7b30e29959c2b8d9126162384
windows-amd64: a95cc65062c7f7cd070d75c52adbba4763dfced950acc518e2b50aae0749a15b
```

`opensysml.binary.detect_platform()` already exists and returns exactly the `(os_name, arch)` pair needed (`('darwin', 'arm64')` on this machine) — call it directly rather than re-deriving platform detection; it is a stable, already-depended-on function (`src/toaster/bootstrap.py` already imports `opensysml.binary`).

The real, previously-used-but-non-reproducible binary that proved this capability (`/private/tmp/functional-toaster-design/sysml`) must never be referenced by any code this task writes — it is a scratch path on one machine, already shown this session (`decisions/log.md` DL-064) to be at real risk of being wiped by an environmental `/tmp` cleanup.

- [ ] **Step 1: Write the failing provisioning test**

```python
# tests/test_bootstrap_cli_binary.py
"""Tests for toaster.bootstrap.ensure_cli_binary() (Phase 2 Task 1)."""
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from toaster.bootstrap import ensure_cli_binary, _CLI_SUMS, _cli_cache_dir


def test_sha256_pins_cover_darwin_and_linux():
    """The pins this task's own implementation ships must cover at least the
    platforms this repo's own contributors actually use."""
    assert ("darwin", "amd64") in _CLI_SUMS
    assert ("darwin", "arm64") in _CLI_SUMS
    assert ("linux", "amd64") in _CLI_SUMS
    assert _CLI_SUMS[("darwin", "arm64")] == (
        "0129f277bd10c73ca09c7ce643cf7ae9b6b496250925d1a640ef1e2930340efb"
    )


def test_ensure_cli_binary_downloads_verifies_and_caches():
    """End-to-end: a real network call against the real pinned v0.9.0 release.
    This is the one test in this file that touches the network -- skip it only
    if explicitly offline, never silently."""
    path = ensure_cli_binary(version="v0.9.0")
    assert path.exists()
    assert path.is_file()
    result = subprocess.run([str(path), "-version"], capture_output=True, text=True, timeout=10)
    assert "sysml v0.9.0" in result.stdout
    assert "ee54ea03ea3ca8fb2c796ecda364adf748c40304" in result.stdout


def test_ensure_cli_binary_is_idempotent_and_skips_network_on_cache_hit():
    """A second call must return the same path without re-downloading -- verified
    by checking the cached file's own mtime is unchanged across the two calls."""
    first = ensure_cli_binary(version="v0.9.0")
    mtime_before = first.stat().st_mtime
    second = ensure_cli_binary(version="v0.9.0")
    assert second == first
    assert second.stat().st_mtime == mtime_before


def test_ensure_cli_binary_rejects_a_tampered_download(monkeypatch, tmp_path):
    """A SHA256 mismatch must raise, not silently install a wrong binary --
    simulated by pointing the cache dir at a scratch location and corrupting
    the pin table for this one test only."""
    import toaster.bootstrap as bootstrap_mod

    monkeypatch.setattr(bootstrap_mod, "_cli_cache_dir", lambda: tmp_path)
    bad_sums = dict(bootstrap_mod._CLI_SUMS)
    bad_sums[("darwin", "arm64")] = "0" * 64
    monkeypatch.setattr(bootstrap_mod, "_CLI_SUMS", bad_sums)
    with pytest.raises(RuntimeError, match="sha256 mismatch"):
        ensure_cli_binary(version="v0.9.0")
    assert not (tmp_path / "sysml").exists()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_bootstrap_cli_binary.py -v`
Expected: FAIL with `ImportError: cannot import name 'ensure_cli_binary'`

- [ ] **Step 3: Implement `ensure_cli_binary()` in `src/toaster/bootstrap.py`**

Add after the existing imports, before `check_tool_versions`:

```python
import hashlib
import tarfile
import urllib.request

_CLI_SUMS = {
    ("darwin", "amd64"): "c4efdbcfd698ac9adb1ba64aca5adcd2d4caecf6299140da77eb9c2a8f1a4874",
    ("darwin", "arm64"): "0129f277bd10c73ca09c7ce643cf7ae9b6b496250925d1a640ef1e2930340efb",
    ("linux", "amd64"): "3e9a2070261cd08bd7363abf3a836c3adb5b92f488668548734bdce7b6bd8fa1",
    ("linux", "arm64"): "c74dbd818e1cf2aa082bf6f0c23759a661ed4af7b30e29959c2b8d9126162384",
    ("windows", "amd64"): "a95cc65062c7f7cd070d75c52adbba4763dfced950acc518e2b50aae0749a15b",
}


def _cli_cache_dir() -> Path:
    return Path.home() / ".opensysml" / "bin"


def ensure_cli_binary(version: str = "v0.9.0") -> Path:
    """Download, SHA256-verify, and cache OpenSysML's render-capable CLI binary.

    Distinct from opensysml.binary.ensure_binary(), which provisions the
    unrelated sysml-grpc SERVICE binary (no -render support at all, confirmed
    directly: `sysml-grpc -help` lists no -render flag). This provisions the
    separate `sysml-<os>-<arch>.tar.gz` asset the same v0.9.0 release also
    publishes, which does support -render (confirmed against the real pinned
    commit ee54ea03ea3ca8fb2c796ecda364adf748c40304).

    Cached at ~/.opensysml/bin/sysml, sibling to (but never overwriting)
    sysml-grpc's own cache in the same directory. A cache hit returns
    immediately with no network call.
    """
    import opensysml.binary as ob

    os_name, arch = ob.detect_platform()
    key = (os_name, arch)
    if key not in _CLI_SUMS:
        raise RuntimeError(
            f"No pinned sha256 for platform {os_name}-{arch}; "
            f"supported: {sorted(_CLI_SUMS)}"
        )

    cache_dir = _cli_cache_dir()
    target = cache_dir / ("sysml.exe" if os_name == "windows" else "sysml")
    if target.exists():
        return target

    cache_dir.mkdir(parents=True, exist_ok=True)
    asset_name = f"sysml-{os_name}-{arch}" + (".zip" if os_name == "windows" else ".tar.gz")
    url = (
        f"https://github.com/Open-MBEE/OpenSysML/releases/download/"
        f"{version}/{asset_name}"
    )
    archive_path = cache_dir / asset_name
    urllib.request.urlretrieve(url, archive_path)

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    expected = _CLI_SUMS[key]
    if digest != expected:
        archive_path.unlink()
        raise RuntimeError(
            f"sha256 mismatch for {asset_name}: got {digest}, expected {expected} "
            f"-- refusing to install a binary that doesn't match the pinned release"
        )

    if os_name == "windows":
        import zipfile

        with zipfile.ZipFile(archive_path) as zf:
            zf.extractall(cache_dir)
        extracted = cache_dir / f"sysml-{os_name}-{arch}.exe"
    else:
        with tarfile.open(archive_path) as tf:
            tf.extractall(cache_dir)
        extracted = cache_dir / f"sysml-{os_name}-{arch}"

    extracted.rename(target)
    target.chmod(0o755)
    archive_path.unlink()
    return target
```

Also add to `provision()`:

```python
def provision(version: str = "v0.9.0") -> None:
    """Run full pre-flight: check tool versions then ensure binaries."""
    check_tool_versions()
    ensure_binary(version=version)
    ensure_cli_binary(version=version)
```

- [ ] **Step 4: Run the provisioning tests to verify they pass**

Run: `uv run pytest tests/test_bootstrap_cli_binary.py -v`
Expected: PASS (4 tests)

- [ ] **Step 5: Write the failing render tests, grounded in the real Ch6/Ch7 fixtures**

```python
# tests/test_render_action_state_flow.py
"""Tests for render_action_flow() and render_state_flow() (Phase 2 Task 1)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from toaster.bootstrap import ensure_cli_binary
from toaster.render import render_action_flow, render_state_flow

REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="module")
def cli_binary():
    return ensure_cli_binary(version="v0.9.0")


@pytest.fixture(scope="module")
def ch06_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch06-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok, f"Ch6 fixture failed to load: {model.diagnostics}"
    yield model
    conn.close()


@pytest.fixture(scope="module")
def ch07_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch07-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok, f"Ch7 fixture failed to load: {model.diagnostics}"
    yield model
    conn.close()


def test_render_action_flow_produces_real_svg(ch06_model, cli_binary, tmp_path):
    out = tmp_path / "apply_heat.svg"
    render_action_flow(ch06_model, "ToasterDemo::ApplyHeat", out, binary=cli_binary)
    assert out.exists()
    svg = out.read_text()
    assert "<svg" in svg
    assert "generateHeat" in svg


def test_render_state_flow_produces_real_svg_with_trigger_labels(ch07_model, cli_binary, tmp_path):
    out = tmp_path / "cycle.svg"
    render_state_flow(ch07_model, "ToasterDemo::Cycle", out, binary=cli_binary)
    assert out.exists()
    svg = out.read_text()
    assert "<svg" in svg
    assert "heating" in svg
    assert "accept Start" in svg


def test_render_action_flow_renders_what_the_model_object_holds_not_the_committed_file(
    tmp_path, cli_binary
):
    """The function must serialize the IN-MEMORY model (model.to_sysml()), not
    silently re-read models/ch06-cumulative.sysml from disk -- proven by loading
    a small synthetic model that doesn't exist as a committed file at all."""
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    src = """
    package SynthTest {
        action def Outer {
            then action inner : Inner;
        }
        action def Inner;
    }
    """
    model = conn.load_from_content(src, strict=False)
    assert model.ok
    out = tmp_path / "outer.svg"
    render_action_flow(model, "SynthTest::Outer", out, binary=cli_binary)
    assert out.exists()
    assert "inner" in out.read_text()
    conn.close()


def test_render_action_flow_missing_binary_raises_clear_error(ch06_model, tmp_path):
    with pytest.raises(FileNotFoundError, match="sysml"):
        render_action_flow(
            ch06_model, "ToasterDemo::ApplyHeat", tmp_path / "x.svg",
            binary=tmp_path / "does-not-exist",
        )
```

- [ ] **Step 6: Run the render tests to verify they fail**

Run: `uv run pytest tests/test_render_action_state_flow.py -v`
Expected: FAIL with `NotImplementedError: render_action_flow: implement in WP-5`

- [ ] **Step 7: Implement `render_action_flow()` and `render_state_flow()` in `src/toaster/render.py:481`**

Replace the existing stub entirely with:

```python
def _render_opensysml_view(
    model: Any, name: str, out: str | Path, kind: str, *, binary: str | Path | None = None
) -> None:
    """Shared implementation for render_action_flow (kind="action") and
    render_state_flow (kind="state"): both use the identical OpenSysML CLI
    mechanism, differing only in the #kind: prefix.

    Serializes the ALREADY-LOADED model (model.to_sysml()) to a temp file and
    renders that, not the committed models/chXX-cumulative.sysml -- this
    renders exactly what the notebook's own model object represents, which
    may differ from disk in a notebook that applies an edit before rendering.
    """
    import subprocess
    import tempfile

    if binary is None:
        from toaster.bootstrap import ensure_cli_binary

        binary = ensure_cli_binary()
    binary = Path(binary)
    if not binary.exists():
        raise FileNotFoundError(f"sysml CLI binary not found at {binary}")

    out = Path(out)
    with tempfile.TemporaryDirectory() as tmp:
        src_path = Path(tmp) / "model.sysml"
        src_path.write_text(model.to_sysml())
        dot_path = Path(tmp) / "view.dot"
        subprocess.run(
            [str(binary), str(src_path), "-render", f"#{kind}:{name}",
             "-render-form", "dot", "-o", str(dot_path)],
            check=True, capture_output=True, text=True,
        )
        render_dot(dot_path, out)


def render_action_flow(
    model: Any, name: str, out: str | Path, *, binary: str | Path | None = None
) -> None:
    """Render an action-flow diagram for a named action def to SVG, via
    OpenSysML's own `-render #action:` CLI form (no in-house equivalent exists
    -- confirmed working on real content, decisions/diagram-study-real-fixtures.md).

    `binary=None` (default) provisions the CLI automatically via
    toaster.bootstrap.ensure_cli_binary(); pass an explicit path to pin a
    specific local build instead.
    """
    _render_opensysml_view(model, name, out, "action", binary=binary)


def render_state_flow(
    model: Any, name: str, out: str | Path, *, binary: str | Path | None = None
) -> None:
    """Render a state-transition diagram for a named state def to SVG, via
    OpenSysML's own `-render #state:` CLI form. Transition edges are labeled
    by their real trigger text (confirmed directly against Ch7's real Cycle
    state machine: `label="accept Start"`), so a renamed or mistyped trigger
    is visible in the figure, not just in printed diagnostics.

    `binary=None` (default) provisions the CLI automatically via
    toaster.bootstrap.ensure_cli_binary(); pass an explicit path to pin a
    specific local build instead.
    """
    _render_opensysml_view(model, name, out, "state", binary=binary)
```

- [ ] **Step 8: Run the render tests to verify they pass**

Run: `uv run pytest tests/test_render_action_state_flow.py -v`
Expected: PASS (5 tests)

- [ ] **Step 9: Update `docs/setup.md`'s tools section**

Add a sentence to the existing "OpenSysML" paragraph (after the sentence ending "Every chapter needs it."):

```markdown
`scripts/check-tools.py` also provisions a second OpenSysML binary, the
render-capable CLI (distinct from the service binary the Python package
itself talks to) — chapters that render an action-flow or state-transition
diagram need it; nothing else does.
```

- [ ] **Step 10: Run the full suite**

Run: `uv run pytest tests/ glossary/tests/ -q`
Expected: 423 + 9 = 432 passed, 7 deselected, no regressions.

- [ ] **Step 11: Commit**

```bash
git add src/toaster/bootstrap.py src/toaster/render.py docs/setup.md \
  tests/test_bootstrap_cli_binary.py tests/test_render_action_state_flow.py
git commit -m "Provision OpenSysML's render-capable CLI; implement render_action_flow/render_state_flow"
```

---

## Task 2: Chapter 1 — two structure diagrams

**Files:**
- Modify: `chapters/ch01-system-purpose/02-part-def.ipynb` (insert one cell after cell 9)
- Modify: `chapters/ch01-system-purpose/04-composition.ipynb` (insert one cell after cell 11)

**Interfaces:**
- Consumes: `model_to_dot()` (unchanged, no new params needed for these two).

**Per `decisions/diagram-survey.md`'s Chapter 1 section:**

1. `02-part-def.ipynb`: after cell 9 (the `print(f"PartDefinition: ...")` loop, which currently ends with `conn.close()`), insert a new code cell rendering `HeatingSystem` and `ControlSystem` as two disconnected boxes — **zero edges**, matching the chapter's own point at this stage ("two part definitions can exist side by side with no relationship yet"). This is the first diagram in the whole tutorial. Insert it *before* the existing `conn.close()` line — i.e., between the current cell 9 and cell 10, not appended after `conn.close()` runs.

   The current cell 10 (verified directly, must match before editing):
   ```python
   hs = model.find("ToasterDemo::HeatingSystem")
   assert hs is not None
   print(f"kind : {hs.kind}")
   print(f"id   : {hs.id}")

   print()
   for e in model.query():
       d = e.as_dict()
       if d["@type"] == "PartDefinition":
           print(f"PartDefinition: {d['qualifiedName']}")
   conn.close()
   ```

   Split this into two cells: the existing content minus `conn.close()`, then a new diagram cell, then a final one-line cell with `conn.close()`. New diagram cell:
   ```python
   from toaster.render import model_to_dot, render_dot

   cs = model.find("ToasterDemo::ControlSystem")
   dot = model_to_dot(model, title="Ch1", elements=[hs, cs])
   render_dot(dot, Path("../../figures/ch01-part-defs.svg"))
   from IPython.display import SVG
   SVG(filename="../../figures/ch01-part-defs.svg")
   ```
   New markdown cell immediately before it (the diagram's own one-sentence narration, matching this notebook's existing terse style): "`HeatingSystem` and `ControlSystem` drawn as two boxes with no edge between them: both exist, neither refers to the other yet."

2. `04-composition.ipynb`: after cell 12 (the `parts()`/`attributes()` print loop, which also ends in `conn.close()`), same split pattern — insert a scoped structure diagram showing `Toaster`'s full composition/typing, using `containment_subgraph(model, "ToasterDemo::Toaster", relations=("composition", "typing"), depth=2)`. This is the chapter's **first diagram with any edge** (composition diamond, typing dash).

- [ ] **Step 1: Read both notebooks' real current cell 9/10 (part-def) and 11/12 (composition) and confirm they match the content quoted above**

Run: `uv run python -c "import json; nb = json.load(open('chapters/ch01-system-purpose/02-part-def.ipynb')); print(''.join(nb['cells'][10]['source']))"`
Expected: matches the block quoted above exactly.

- [ ] **Step 2: Edit `02-part-def.ipynb`** per the split described above (use a notebook-editing script, not hand JSON editing, to preserve nbformat structure — follow the exact pattern used for `exercises/ch08/exercise.ipynb`'s own cell edit in `decisions/log.md` DL-085: load with `json.load`, mutate `cells[i]['source']` lists, `json.dump` back with `indent=1`).

- [ ] **Step 3: Re-execute and verify**

Run: `uv run jupyter nbconvert --to notebook --execute --output /tmp/ch01-nb02-check.ipynb chapters/ch01-system-purpose/02-part-def.ipynb`
Expected: exit 0, no cell errors. Inspect the executed output: the new cell's SVG output must contain `HeatingSystem` and `ControlSystem` and must NOT contain any edge-drawing DOT syntax (`->`) between them (confirms zero edges, per the chapter's own point).

- [ ] **Step 4: Edit `04-composition.ipynb`** with the scoped structure diagram described above.

- [ ] **Step 5: Re-execute and verify**

Run: `uv run jupyter nbconvert --to notebook --execute --output /tmp/ch01-nb04-check.ipynb chapters/ch01-system-purpose/04-composition.ipynb`
Expected: exit 0. The new cell's SVG must contain `Toaster`, `heating`, `control`, `HeatingSystem`, `ControlSystem`, and at least one `->` edge (composition) and one dashed-style edge (typing) — confirmed by checking the DOT source (printed or saved alongside) for `arrowhead=diamond` and `style=dashed`.

- [ ] **Step 6: Run the full suite and construction check**

Run: `uv run pytest tests/ glossary/tests/ -q && uv run python scripts/check_construction.py --check`
Expected: both clean.

- [ ] **Step 7: Commit**

```bash
git add chapters/ch01-system-purpose/02-part-def.ipynb chapters/ch01-system-purpose/04-composition.ipynb
git commit -m "Ch1: add the tutorial's first two structure diagrams (edgeless, then composition+typing)"
```

---

## Task 3: Chapter 2 — one structure diagram

**Files:**
- Modify: `chapters/ch02-requirements/03-judgment-context.ipynb` (insert one cell after cell 2)

**Per `decisions/diagram-survey.md`'s Chapter 2 section:** after cell 2 (`print(source)` + load, the chapter's densest output), add a whole-model structure diagram — "add", not replace; the raw source print stays, since it shows requirement/override syntax `model_to_dot()` cannot draw. **Explicit non-goal**, carried forward from the survey: do not attempt to show `TimelyToast`, the `attribute :>>` override, or the judgment-record content in this or any diagram — none has `model_to_dot()` support.

- [ ] **Step 1: Confirm cell 2's real current content matches**

Run: `uv run python -c "import json; nb = json.load(open('chapters/ch02-requirements/03-judgment-context.ipynb')); print(''.join(nb['cells'][2]['source']))"`
Expected:
```python
from pathlib import Path
import opensysml
from toaster.report import format_diagnostics

conn = opensysml.connect(version="v0.9.0")
source = Path("../../models/ch02-cumulative.sysml").read_text()
print(source)
model = conn.load_from_content(source, strict=False)
assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
```

- [ ] **Step 2: Insert one markdown + one code cell after cell 2** (pushing the existing cell 3 markdown down):

Markdown: "The containment skeleton this model carries so far, drawn directly from the model that just loaded."

Code:
```python
from toaster.render import model_to_dot, render_dot
from IPython.display import SVG

dot = model_to_dot(model, title="Ch2")
out_path = Path("../../figures/ch02-structure.svg")
out_path.parent.mkdir(exist_ok=True)
render_dot(dot, out_path)
SVG(filename=str(out_path))
```

- [ ] **Step 3: Re-execute and verify**

Run: `uv run jupyter nbconvert --to notebook --execute --output /tmp/ch02-nb03-check.ipynb chapters/ch02-requirements/03-judgment-context.ipynb`
Expected: exit 0. New cell's SVG contains `Toaster`, `nominal`, `slow`, `HeatingSystem`, `ControlSystem`.

- [ ] **Step 4: Full suite + construction check, commit**

```bash
uv run pytest tests/ glossary/tests/ -q && uv run python scripts/check_construction.py --check
git add chapters/ch02-requirements/03-judgment-context.ipynb
git commit -m "Ch2: add a structure diagram orienting the reader before the judgment-context content"
```

---

## Task 4: Chapter 3 — one structure diagram

**Files:**
- Modify: `chapters/ch03-measures/03-threshold-judgment.ipynb` (insert one cell after cell 2)

**Per `decisions/diagram-survey.md`'s Chapter 3 section:** same pattern as Task 3 — after cell 2's `print(source)` (an 83-line dump, the chapter's densest output), add a whole-model structure diagram. **Explicit non-goal**: cannot show `TimelyToast`, `timely`, the folded `assert not satisfy timely by slow`, or `TimelyToastTest` — no `model_to_dot()` support for any of them; the diagram only orients the reader to the unchanged `Toaster`/`heating`/`control`/`nominal`/`slow` skeleton.

- [ ] **Step 1: Confirm cell 2's content** (same load pattern as Task 3's Step 1, targeting `ch03-cumulative.sysml`).

Run: `uv run python -c "import json; nb = json.load(open('chapters/ch03-measures/03-threshold-judgment.ipynb')); print(''.join(nb['cells'][2]['source']))"`

- [ ] **Step 2: Insert markdown + code cell after cell 2**, identical structure to Task 3's Step 2, writing to `figures/ch03-structure.svg`, with markdown: "The part skeleton underneath the requirement and judgment content below — unchanged since Chapter 2, drawn here to orient before reading the satisfy claim in detail."

- [ ] **Step 3: Re-execute and verify**

Run: `uv run jupyter nbconvert --to notebook --execute --output /tmp/ch03-nb03-check.ipynb chapters/ch03-measures/03-threshold-judgment.ipynb`
Expected: exit 0. SVG contains `Toaster`, `nominal`, `slow`.

- [ ] **Step 4: Full suite + construction check, commit**

```bash
uv run pytest tests/ glossary/tests/ -q && uv run python scripts/check_construction.py --check
git add chapters/ch03-measures/03-threshold-judgment.ipynb
git commit -m "Ch3: add a structure diagram orienting the reader before the threshold-judgment content"
```

---

## Task 5: Chapter 4 — action-flow diagram (new notation) + structure diagram

**Files:**
- Modify: `chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb` (insert one cell after cell 14)
- Modify: `chapters/ch04-functional-decomp/03-completeness-check.ipynb` (insert one cell after cell 2)

**Interfaces:**
- Consumes: `render_action_flow()` (Task 1).

**Per `decisions/diagram-survey.md`'s Chapter 4 section:**

1. `01-action-def-ffbd.ipynb`: after cell 14 (the `print(TOASTER_INCREMENT)` + model load, confirmed real content below), add an action-flow diagram of `ToastBread` — the **tutorial's first action-flow diagram**.

   Real current cell 14 (confirm before editing):
   ```python
   TOASTBREAD_REOPENED = (
       "action def ToastBread {\n"
       "    doc /* Transform bread into toast acceptable to its user. */\n"
       "    in bread : Bread;\n"
       "    out toast : Toast;\n"
       f"{TOASTBREAD_SEQUENCE}\n"
       "}"
   )
   TOASTER_INCREMENT = f"{APPLY_HEAT_DEF}\n{TOASTBREAD_REOPENED}"
   print(TOASTER_INCREMENT)

   source = Path("../../models/ch04-cumulative.sysml").read_text()
   model = conn.load_from_content(source, strict=False)
   assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
   ```

   New code cell inserted after it:
   ```python
   from toaster.render import render_action_flow
   from IPython.display import SVG

   out_path = Path("../../figures/ch04-toastbread-flow.svg")
   out_path.parent.mkdir(exist_ok=True)
   render_action_flow(model, "ToasterDemo::ToastBread", out_path)
   SVG(filename=str(out_path))
   ```
   New markdown cell immediately after the diagram (the chapter's first action-flow notation, name it as such behaviorally, never citing "Tall" or any builder-facing lens, per `AGENTS.md` 1.10): "The `start → applyHeat → done` sequence drawn directly from the loaded model: the same nesting the text above states, shown as a flow."

2. `03-completeness-check.ipynb`: after cell 2 (`print(source)`, a 115+-line dump), add a scoped structure diagram via `containment_subgraph(model, "ToasterDemo::Toaster", depth=2)` — same pattern as Tasks 3/4, reused structure notation, not new.

- [ ] **Step 1: Confirm `01-action-def-ffbd.ipynb` cell 14's real content matches the block above**

Run: `uv run python -c "import json; nb = json.load(open('chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb')); print(''.join(nb['cells'][14]['source']))"`

- [ ] **Step 2: Insert the action-flow diagram cell + narration after cell 14**

- [ ] **Step 3: Re-execute `01-action-def-ffbd.ipynb` and verify**

Run: `uv run jupyter nbconvert --to notebook --execute --output /tmp/ch04-nb01-check.ipynb chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb`
Expected: exit 0. New cell's SVG contains `ApplyHeat` and `ToastBread`.

- [ ] **Step 4: Confirm `03-completeness-check.ipynb` cell 2's real content, insert the structure diagram after it** (same pattern as Task 3 Step 2, writing `figures/ch04-structure.svg`).

- [ ] **Step 5: Re-execute `03-completeness-check.ipynb` and verify**

Run: `uv run jupyter nbconvert --to notebook --execute --output /tmp/ch04-nb03-check.ipynb chapters/ch04-functional-decomp/03-completeness-check.ipynb`
Expected: exit 0. New cell's SVG contains `Toaster`, `heating`, `control`.

- [ ] **Step 6: Full suite + construction check, commit**

```bash
uv run pytest tests/ glossary/tests/ -q && uv run python scripts/check_construction.py --check
git add chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb chapters/ch04-functional-decomp/03-completeness-check.ipynb
git commit -m "Ch4: add the tutorial's first action-flow diagram, and a scoped structure diagram"
```

---

## Task 6: Chapter 5 — remaining structure diagram

**Files:**
- Modify: `chapters/ch05-architecture/01-concept-selection.ipynb` (insert one cell after cell 2)

**Per `decisions/diagram-survey.md`'s Chapter 5 section:** Ch5's interconnection-view upgrade (`03-interfaces.ipynb`) is already done (`CONTRACT CH05-TOOLKIT-VIZ`, merged). The one remaining candidate: after `01-concept-selection.ipynb` cell 2 (`print(source)`, 131 lines), a whole-model structure diagram, unscoped (`elements=None` — the model is still small enough). **Explicit note from the survey**: skip the identical `print(source)` dump that recurs in `02-allocate.ipynb` and `03-interfaces.ipynb` — no second or third copy of this same diagram; it belongs once, here.

- [ ] **Step 1: Confirm cell 2's content**

Run: `uv run python -c "import json; nb = json.load(open('chapters/ch05-architecture/01-concept-selection.ipynb')); print(''.join(nb['cells'][2]['source']))"`

- [ ] **Step 2: Insert markdown + code cell after cell 2**, writing `figures/ch05-structure.svg`, `model_to_dot(model, title="Ch5")` unscoped. Markdown: "The containment skeleton of everything built so far, before the chapter adds a port and an allocation."

- [ ] **Step 3: Re-execute and verify**

Run: `uv run jupyter nbconvert --to notebook --execute --output /tmp/ch05-nb01-check.ipynb chapters/ch05-architecture/01-concept-selection.ipynb`
Expected: exit 0. SVG contains `Toaster`, `heating`, `control`, `nominal`, `slow`.

- [ ] **Step 4: Full suite + construction check, commit**

```bash
uv run pytest tests/ glossary/tests/ -q && uv run python scripts/check_construction.py --check
git add chapters/ch05-architecture/01-concept-selection.ipynb
git commit -m "Ch5: add the chapter's remaining structure diagram (nb01, unscoped)"
```

---

## Task 7: Chapter 6 — four diagrams (action-flow, interconnection x2, structure), all reused notation at a deeper root

**Files:**
- Modify: `chapters/ch06-recursive-decomp/01-subsystem-requirements.ipynb` (insert cells after cell 6 and after cell 17)
- Modify: `chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb` (insert cells after cell 2 and after cell 6)

**Interfaces:**
- Consumes: `render_action_flow()` (Task 1); `containment_subgraph()`, `render_interconnection()`/`build_interconnection_intent()` (already exist).

**Per `decisions/diagram-survey.md`'s Chapter 6 section:** no new notation — everything roots at `HeatingAssembly`, not the familiar `Toaster`, because `Toaster::heating` is typed by the abstract `HeatingSystem` with no edge to the concrete `HeatingAssembly`/`heatGen` (the exact worked example in `containment_subgraph()`'s own test suite, `tests/test_containment_subgraph.py::test_heating_assembly_reaches_heatgen_type_at_depth_two`). **Do not root any of these four diagrams at `Toaster`.**

1. `01-subsystem-requirements.ipynb`, after cell 6 (the `ApplyHeat`/`generateHeat` increment, confirm real content first): action-flow diagram of `ApplyHeat`, reused notation.
2. `01-subsystem-requirements.ipynb`, cell 16 (confirmed real content: `allocations = find_allocations(model); print(f"Allocations: {allocations}"); print(f"Perform relationships: {perform_relationships(model)}")`, with cell 17's markdown explaining it immediately after): **replace** the `Allocations:` print line specifically (keep `Perform relationships:` as text — no supported notation for perform edges) with an interconnection/allocation diagram of `HeatingAssembly`, `depth=1`, inserted as a new cell between cell 16 and cell 17.
3. `03-stopping-judgment.ipynb`, after cell 2 (`print(source)`, 213 lines, confirm real content first): structure diagram, `containment_subgraph(model, "ToasterDemo::HeatingAssembly", relations=("composition","typing"), depth=2)`.
4. `03-stopping-judgment.ipynb`, after cell 6 (the `performs`/`allocations`/`eval` print, confirm real content first): same interconnection/allocation diagram as item 2 (re-rendered; this is `AI-C06`'s own evidence base, grounding the judgment in a picture at the point it's assembled).

- [ ] **Step 1: Confirm all four real insertion-point cells match what's quoted in this task** (cell 6 and cell 16 of nb01; cell 2 and cell 6 of nb03) — run the same `json.load`/print pattern as prior tasks for each, comparing against:

nb01 cell 6 must contain `APPLY_HEAT_INCREMENT` and end with the ApplyHeat/generateHeat declaration printed.
nb01 cell 16 must be the code cell `allocations = find_allocations(model); print(f"Allocations: {allocations}"); print(f"Perform relationships: {perform_relationships(model)}")`, with cell 17's markdown explaining it immediately after.
nb03 cell 2 must match the same `print(source)` + load pattern as every other chapter's nb0N cell 2.
nb03 cell 6 must contain `performs = perform_relationships(model)` / `allocations = find_allocations(model)` / the two `model.eval(...)` calls.

- [ ] **Step 2: Insert the action-flow diagram in nb01 after the ApplyHeat/generateHeat cell** (`render_action_flow(model, "ToasterDemo::ApplyHeat", Path("../../figures/ch06-applyheat-flow.svg"))`), markdown: "`generateHeat`, nested inside `ApplyHeat` one level deeper than Chapter 4's own flow, drawn the same way."

- [ ] **Step 3: In nb01, split cell 16's two print lines and insert an interconnection diagram between them and cell 17** (keep `Perform relationships:` printed as-is, drop the `Allocations:` print line, replacing it with the diagram, so the cell order becomes: perform-relationships print, then a new diagram cell, then the existing cell 17 markdown):
```python
from toaster.render import build_interconnection_intent, render_interconnection
intent = build_interconnection_intent(model, "ToasterDemo::HeatingAssembly", depth=1)
out_path = Path("../../figures/ch06-heatingassembly-interconnect.svg")
render_interconnection(intent, out_path)
from IPython.display import SVG
SVG(filename=str(out_path))
```

- [ ] **Step 4: Re-execute `01-subsystem-requirements.ipynb` and verify**

Run: `uv run jupyter nbconvert --to notebook --execute --output /tmp/ch06-nb01-check.ipynb chapters/ch06-recursive-decomp/01-subsystem-requirements.ipynb`
Expected: exit 0. Action-flow SVG contains `ApplyHeat`, `generateHeat`. Interconnection SVG contains `heatGen` and does NOT contain `Toaster` as a drawn box (confirms the HeatingAssembly root, not the familiar Toaster root).

- [ ] **Step 5: Insert the structure diagram in nb03 after cell 2**, rooted at `HeatingAssembly`, `depth=2`: `model_to_dot(model, title="Ch6", elements=containment_subgraph(model, "ToasterDemo::HeatingAssembly", relations=("composition","typing"), depth=2))`. Markdown: "Rooted at `HeatingAssembly`, not `Toaster` — the only root that reaches `heatGen` and its type, `HeatGenerator`."

- [ ] **Step 6: Insert the same interconnection diagram (Step 3's code) in nb03 after the `performs`/`allocations`/`eval` cell.**

- [ ] **Step 7: Re-execute `03-stopping-judgment.ipynb` and verify**

Run: `uv run jupyter nbconvert --to notebook --execute --output /tmp/ch06-nb03-check.ipynb chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb`
Expected: exit 0. Structure SVG contains `HeatingAssembly`, `heatGen`, `HeatGenerator` and does NOT contain `Toaster`. Interconnection SVG matches Step 4's own content.

- [ ] **Step 8: Full suite + construction check, commit**

```bash
uv run pytest tests/ glossary/tests/ -q && uv run python scripts/check_construction.py --check
git add chapters/ch06-recursive-decomp/01-subsystem-requirements.ipynb chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb
git commit -m "Ch6: add four diagrams (action-flow, interconnection x2, structure), all rooted at HeatingAssembly"
```

---

## Task 8: Chapter 7 — three state diagrams (new notation)

**Files:**
- Modify: `chapters/ch07-execution/02-state-traces.ipynb` (insert cells after cell 12, after cell 21, after cell 24)

**Interfaces:**
- Consumes: `render_state_flow()` (Task 1).

**Per `decisions/diagram-survey.md`'s Chapter 7 section**, with the one previously-unconfirmed item now resolved: rendering the trigger-typo negative control DOES show the mislabeled trigger as an edge label — confirmed directly in this plan's own Task 1 investigation (`"n1" -> "n2" [label="accept Start"]` against the real, untouched `Cycle`). **Keep all three proposed diagrams; none is dropped.**

1. After cell 12 (`CYCLE_DEF` print, confirm real content first): state diagram of `Cycle` — the **tutorial's first state diagram**.
2. After cell 21 (confirm real content: the typo-probe markdown explaining `language_gap_findings` catches `Strat`): state diagram of the **typo'd** model — render `typo_model` (not `model`), confirming the mislabeled trigger `Strat` is visible on the edge.
3. After cell 24 (the two `execute_state` trace prints, confirm real content first): the base `Cycle` diagram again (Step 1's own cell re-run is sufficient conceptually, but per the survey's own "supplement, not replace" framing, this is a narrative callback, not a new render — add one markdown cell pointing back at the first diagram rather than re-rendering identical content a third time in one notebook).

- [ ] **Step 1: Confirm cell 12's real content** (`CYCLE_DEF = (...); print(CYCLE_DEF)`).

- [ ] **Step 2: Insert the first state diagram after cell 12**:
```python
from toaster.render import render_state_flow
from IPython.display import SVG

out_path = Path("../../figures/ch07-cycle-state.svg")
out_path.parent.mkdir(exist_ok=True)
render_state_flow(model, "ToasterDemo::Cycle", out_path)
SVG(filename=str(out_path))
```
Markdown immediately after: "`Cycle`'s own transition table, drawn: the tutorial's first state diagram."

- [ ] **Step 3: Confirm cell 20-21's real content** (the `typo_source`/`typo_model` cell and its markdown, quoted in this task's own header above).

- [ ] **Step 4: Insert the typo-probe state diagram after cell 21**:
```python
typo_out_path = Path("../../figures/ch07-cycle-state-typo.svg")
render_state_flow(typo_model, "ToasterDemo::Cycle", typo_out_path)
SVG(filename=str(typo_out_path))
```
Markdown immediately after: "The same transition drawn with the typo'd trigger: the edge now reads `accept Strat`, visible in the picture the same way it is invisible to OpenSysML's own loader."

- [ ] **Step 5: Confirm cell 24's real content** (the two `execute_state` trace prints).

- [ ] **Step 6: Insert one markdown-only cell after cell 24** (no new render): "Both traces above run against the same transition table the first diagram in this notebook already drew — `idle → heating → ready → idle` and `idle → heating → cancelled → idle` are two paths through that one picture, not two different machines."

- [ ] **Step 7: Re-execute and verify**

Run: `uv run jupyter nbconvert --to notebook --execute --output /tmp/ch07-nb02-check.ipynb chapters/ch07-execution/02-state-traces.ipynb`
Expected: exit 0. First SVG contains `idle`, `heating`, `ready`, `cancelled`, `accept Start`. Second SVG contains `accept Strat` (the typo, confirming the diagram actually shows it) and does NOT contain `accept Start` (confirming the original trigger text is gone, not just supplemented).

- [ ] **Step 8: Full suite + construction check, commit**

```bash
uv run pytest tests/ glossary/tests/ -q && uv run python scripts/check_construction.py --check
git add chapters/ch07-execution/02-state-traces.ipynb
git commit -m "Ch7: add the tutorial's first state diagrams (base Cycle, and the typo'd negative control)"
```

---

## Task 9: Chapter 8 — one structure diagram

**Files:**
- Modify: `chapters/ch08-checking/01-invariant-def.ipynb` (insert one cell after cell 3)

**Per `decisions/diagram-survey.md`'s Chapter 8 section:** Ch8 introduces no new notation. After cell 3 (the markdown explaining `heatGenCheck` is "just another usage" of `HeatGenerator`, alongside `rated`/`weak`), add a whole-model structure diagram grounding that specific prose claim. **Explicit non-goal**: cannot show the lemma, the constraint, or the Z3 proof — no tool support for any of it; this diagram shows only the part-sibling relationship the one sentence asserts.

- [ ] **Step 1: Confirm cell 3's real content**

Run: `uv run python -c "import json; nb = json.load(open('chapters/ch08-checking/01-invariant-def.ipynb')); print(''.join(nb['cells'][3]['source']))"`
Expected: the "`heatGenCheck` adds nothing to the model but an unbound usage of `HeatGenerator`..." markdown quoted in this task's own header.

- [ ] **Step 2: Insert markdown + code cell after cell 3**, `model_to_dot(model, title="Ch8")` unscoped (model still small), writing `figures/ch08-structure.svg`. Markdown: "`heatGenCheck` drawn as a sibling usage of `HeatGenerator`, alongside `rated` and `weak` — the structural claim the previous paragraph makes, shown."

- [ ] **Step 3: Re-execute and verify**

Run: `uv run jupyter nbconvert --to notebook --execute --output /tmp/ch08-nb01-check.ipynb chapters/ch08-checking/01-invariant-def.ipynb`
Expected: exit 0. SVG contains `heatGenCheck`, `rated`, `weak`, `HeatGenerator`.

- [ ] **Step 4: Full suite + construction check, commit**

```bash
uv run pytest tests/ glossary/tests/ -q && uv run python scripts/check_construction.py --check
git add chapters/ch08-checking/01-invariant-def.ipynb
git commit -m "Ch8: add a structure diagram grounding the heatGenCheck sibling-usage claim"
```

---

## Task 10: Chapter 10 — one structure diagram, whole-model (not root-scoped)

**Files:**
- Modify: `chapters/ch10-traceability-signoff/01-traceability-graph.ipynb` (insert one cell after cell 4)

**Per `decisions/diagram-survey.md`'s Chapter 10 section:** before the dense `requirement_coverage`/`traceability_graph` dict dumps, orient the reader with the physical hierarchy underneath both traced chains. **Must use `model_to_dot()` unscoped (`elements=None`), not `containment_subgraph()` with a single root** — the survey's own finding: `nominal`/`slow` are typed by `Toaster` but not owned by it, so a forward-only `containment_subgraph()` traversal from any single root misses one or the other chain (the same "wrong root chosen" pitfall as Ch6, in reverse — here no single root reaches everything, so don't pick one).

- [ ] **Step 1: Confirm cell 4's real content** (the negative control: `bad_source` with the undeclared-feature allocate, confirm it matches this task's header quote) and cell 2 (`model = conn.load_from_content(...)`, confirm it precedes cell 4).

- [ ] **Step 2: Insert markdown + code cell after cell 4** (before cell 5's trace narrative begins):
```python
from toaster.render import model_to_dot, render_dot
from IPython.display import SVG

dot = model_to_dot(model, title="Ch10")
out_path = Path("../../figures/ch10-structure.svg")
out_path.parent.mkdir(exist_ok=True)
render_dot(dot, out_path)
SVG(filename=str(out_path))
```
Markdown: "The full part hierarchy underneath both traced chains, drawn whole rather than rooted at either one — `nominal` and `slow` are typed by, but not owned by, `Toaster`, so no single root reaches both `heatGen`'s own chain and theirs."

- [ ] **Step 3: Re-execute and verify**

Run: `uv run jupyter nbconvert --to notebook --execute --output /tmp/ch10-nb01-check.ipynb chapters/ch10-traceability-signoff/01-traceability-graph.ipynb`
Expected: exit 0. SVG contains `Toaster`, `nominal`, `slow`, `HeatingAssembly`, `heatGen`, `HeatGenerator`.

- [ ] **Step 4: Full suite + construction check, commit**

```bash
uv run pytest tests/ glossary/tests/ -q && uv run python scripts/check_construction.py --check
git add chapters/ch10-traceability-signoff/01-traceability-graph.ipynb
git commit -m "Ch10: add a whole-model structure diagram orienting the reader before the traceability tables"
```

---

## Self-Review Notes

**Spec coverage:** all 16 diagram placements `decisions/diagram-survey.md` lists are covered — Ch1 (2, Task 2), Ch2 (1, Task 3), Ch3 (1, Task 4), Ch4 (2, Task 5), Ch5 (1 remaining, Task 6; the interconnection upgrade is already done), Ch6 (4, Task 7), Ch7 (3, Task 8), Ch8 (1, Task 9), Ch10 (1, Task 10) = 2+1+1+2+1+4+3+1+1 = 16. Ch9's own zero-candidate finding needs no task, per the survey's own explicit null result.

**Placeholder scan:** every task names its exact file, exact cell, exact code, and exact verification string. No "TBD", no "add appropriate", no "similar to Task N" without the actual code repeated in full.

**Type/interface consistency:** `render_action_flow(model, name, out, *, binary=None)` and `render_state_flow(model, name, out, *, binary=None)` (Task 1) are called identically in Tasks 5, 7, and 8 with no `binary=` override (using the default auto-provisioning path) — confirmed consistent across every call site in this plan.

**Known risk not independently mitigated by a task of its own:** Task 1's `ensure_cli_binary()` network test (`test_ensure_cli_binary_downloads_verifies_and_caches`) is the one test in this whole plan that requires network access; if this plan is ever run in a sandboxed CI environment without it, that one test needs a documented skip condition — flagged here for whoever wires this into CI, not solved in this plan (CI wiring is the separate, already-tracked `2026-10-01-ci-cd-deploy-readiness-plan.md`'s own concern).
