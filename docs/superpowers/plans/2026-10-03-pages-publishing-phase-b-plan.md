# Pages Publishing Implementation Plan (Phase B: contracts)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This repo's own harness applies: every task is a CONTRACT per `decisions/work-contract-template.md`, run through `decisions/task-states.md`, author and reviewer on different pinned models, worktree per task created by the orchestrator, plain commits (no trailers), subagents never merge or push.

**Goal:** A pull request whose green build, on a clean `ubuntu-latest` runner, executes every notebook with zero cell errors, builds the site with `BASE_URL=/toaster`, passes the site checks, and (on `main` only) deploys it to GitHub Pages.

**Architecture:** One integration branch `pages-publishing` (off `main`); every contract is built in its own worktree off that branch and merged back into it after independent review; one pull request at the end. A resolver module (`toaster.tools`) replaces every hard-coded tool path; `scripts/provision-tools.py` downloads pinned tools into a gitignored `.tools/` directory; `scripts/check-site.py` is the machine-checkable release gate; `ci.yml` runs provisioning, tests, the executed build, the gate, and the Pages deploy.

**Tech Stack:** Python >= 3.12 with `uv`; mystmd 1.11.0 (`npx myst`); GitHub Actions (`actions/upload-pages-artifact`, `actions/deploy-pages`); sysml-toolkit v0.9.1 release binary; Z3 5.1.0; PlantUML 1.2026.8 jar; Graphviz and a JRE from apt.

**Spec:** `docs/superpowers/specs/2026-10-03-pages-publishing-design.md`. **Survey (the evidence behind every contract):** `decisions/pages-publishing-survey.md` and `decisions/pages-publishing/a1-clean-checkout.md`, `a2-real-runner.md`, `a3-output-equivalence.md`, `a4-dangling-references.md`.

## Global Constraints

- Notebook edits follow the minimal-diff standard (DL-099): patch only the named cells' `source` (and, only where a contract says so, the matching stored output text); never `jupyter nbconvert --execute --inplace` a tracked notebook; run notebooks only in throwaway copies; every other cell, `execution_count` and output stays byte-identical (compare cell by cell with `json`).
- Commit messages are plain: no `Co-Authored-By` or any trailer. Subagents do not push, merge or open PRs.
- No PDF, secret or downloaded binary is ever committed; tools live in the gitignored `.tools/`.
- Identity (DL-112): "Z" means the contributor `mzargham`. On published pages say "mzargham (Z)" at first mention instead of a bare "Z". Internal files (`decisions/`, `.claude/`) keep "Z".
- Pins, copied from the survey (verify each against the live source before relying on it): sysml-toolkit `v0.9.1` linux x86_64 asset `sysmlv2-0.9.1-x86_64-unknown-linux-gnu.tar.gz` sha256 `76b4a1e4f159bdf72bde8857bf25e60f59b4ffe4c7c48eeb8c419d856f4ff570`; macOS arm64 asset `sysmlv2-0.9.1-aarch64-apple-darwin.tar.gz` sha256 `ad0204041c95ce9817d398420e5057132a1378d53a812172cbd207cc40100c4a`; `sysml.library` from `Systems-Modeling/SysML-v2-Release` commit `de1070ae8e79c21532b8004fc663d47b35d0e9fa`; PlantUML `v1.2026.8` `plantuml-1.2026.8.jar` sha256 `5e1ecfa8ecd32c90b03bbf3b1eb6f020943f98ab0fcf4032be31a0002ee2c462`; Z3 `z3-5.1.0` linux asset `z3-5.1.0-x64-glibc-2.39.zip` sha256 `f47be8d27d3230e823bf1eeede2fe0abaca55bb78d0b59974370e6689a92284a`.
- Environment variable names (already used by `toaster.modelcheck` for the first two): `SYSMLV2_BINARY`, `SYSMLV2_LIB_DIR`, `PLANTUML_JAR`, `JAVA`, `Z3`.
- Repo checks that must stay clean at every merge: `uv run pytest tests/ glossary/tests/ -q`, `uv run python -m glossary check`, `uv run python scripts/check_construction.py --check`.
- Reference-policy rulings (Z, 2026-10-03): harness files named on `docs/contributor.md` are KEEP with a GitHub link at first mention (A1); `AGENTS.md` and `decisions/log.md` cited as the source of substantive text are LINKed to GitHub, while DL-nnn in chapter text is REWORDed (A2, A4); exercises are not published, every `exercises/` reference links to GitHub (A9); `reproducibility.md` links the `decisions/` directory (A10); `models/` paths and D-nnn ids on executable lines or inside SysML doc comments and `ReviewRecord` strings are KEEP (A6, A7), and rows tagged A7 are NOT edited by the PUB-5A..E contracts.

## Review Focus

1. `--strict` may fail on the 98 pre-existing warnings (59 "Extension inferred", 39 "Duplicate identifier") even with zero cell errors; PUB-6 must measure this and choose the gate (`--strict` or `check-site.py`'s log check) from evidence, not assume.
2. A figure count equal to the baseline (18) hides failed notebooks (run 1 had 18 figures and 2 failures); the gate needs the zero-error check and the figure check together.
3. Removing a hard-coded path must not change any stored output or `ReviewRecord` text: Ch8-02 cell-11 feeds `AS-C08.json`, and `content_hash` depends on the model files, which no contract here edits.
4. `BASE_URL=/toaster` changes every absolute link and asset; links added by PUB-5 are absolute GitHub URLs or relative in-site links and must be checked on the built site.
5. The first deploy publishes the build to the public: the leak scan (`/home/runner`, `/opt/homebrew`, `Documents/GitHub`, `/Users/`, `/var/folders`, the build host's `$HOME`) and the "no exercises or DEFERRED.md under `build/`" check are release blockers, not warnings.

---
## Task 0: Integration branch and ordering (orchestrator)

- [ ] **Step 1:** `git switch main && git switch -c pages-publishing`. Every worktree below is created with `git worktree add .claude/worktrees/<name> -b pub/<name> pages-publishing`; every merge goes back into `pages-publishing` with `--no-ff`; `main` is untouched until the final PR.
- [ ] **Step 2:** Merge order (dependencies in each contract's `State` line): PUB-1; then PUB-2; then PUB-3, PUB-4 and PUB-5 in parallel; then PUB-6A..D and PUB-7 in parallel; then PUB-8; then PUB-9. The A7 gate (Task 10) can run any time before PUB-6E.
- [ ] **Step 3:** After each merge run the three repo checks on `pages-publishing`; stop and diagnose if any fails.

## Task 1: Tool resolver `toaster.tools` (PUB-1)

**Files:** Create `src/toaster/tools.py`, `tests/test_tools.py`. Modify `.gitignore` (add `.tools/`).

**Interfaces:**
- Produces (later tasks import these exact names): `class ToolNotFoundError(RuntimeError)`; `REPO_ROOT: Path` (module attribute, `Path(__file__).resolve().parents[2]`, patchable in tests); `resolve_sysmlv2(explicit: str | Path | None = None) -> Path`; `resolve_library(explicit=None) -> Path` (the `sysml.library` directory); `resolve_plantuml_jar(explicit=None) -> Path`; `resolve_java(explicit=None) -> Path`; `resolve_z3(explicit=None) -> Path`; `tool_env(base: Mapping[str, str] | None = None) -> dict[str, str]` (a copy of `os.environ`, or of `base`, with the directory of the resolved `z3` prepended to `PATH`, used for subprocesses because `sysmlv2 verify --solve` finds `z3` on `PATH`; raises `ToolNotFoundError` if `z3` is unresolvable).
- Resolution order for every `resolve_*`: (1) the `explicit` argument; (2) its environment variable: `SYSMLV2_BINARY`, `SYSMLV2_LIB_DIR`, `PLANTUML_JAR`, `JAVA`, `Z3`; (3) the provisioned location under `REPO_ROOT / ".tools"`: `bin/sysmlv2`, `sysml.library/`, `plantuml.jar`, `bin/z3` (java is not provisioned); (4) `shutil.which` for `sysmlv2`, `java` and `z3` only (never for the library or jar).
- Validation: the executables must be files with `os.access(path, os.X_OK)`; the library must be a directory containing a `Systems Library` subdirectory; the jar must be a file ending `.jar`. A candidate that is set but invalid is an error that names where it came from (do not silently fall through to the next source).

```
CONTRACT PUB-1 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          ready (branch pages-publishing exists)
Task:           Implement the resolver above with tests. No tool path, home directory or Homebrew location
                appears in this module.
Context:        Spec decision 2; src/toaster/modelcheck.py (existing SYSMLV2_BINARY / SYSMLV2_LIB_DIR handling
                and its `verify_holds(lib, solve, ranges, binary, z3, timeout, *sysml_files)` signature);
                src/toaster/render.py `render_toolkit_interconnection` (takes explicit lib/binary/
                plantuml_jar/java and validates with is_dir/is_file/os.access).
Non-goals:      Do not change modelcheck.py or render.py. Do not provision or download anything. Do not touch
                notebooks.
Blast zone:     src/toaster/tools.py, tests/test_tools.py, .gitignore -- on branch pub/tools in worktree
                .claude/worktrees/tools.
Acceptance:     Tests (all using tmp_path fixtures and monkeypatch for env and REPO_ROOT, no network, no real
                tools) cover for each of the five resolvers: explicit wins over env; env wins over .tools; .tools
                wins over PATH; PATH is used for sysmlv2/java/z3 and NOT for library/jar; a set-but-invalid env
                value raises ToolNotFoundError naming the variable; a missing tool raises ToolNotFoundError whose
                message names the variable and `uv run python scripts/provision-tools.py`; a non-executable file is
                rejected; tool_env prepends the z3 directory to PATH and does not mutate os.environ. Run
                `uv run pytest tests/test_tools.py -q` (all pass), `uv run pytest tests/ glossary/tests/ -q`,
                `uv run python -m glossary check`, `uv run python scripts/check_construction.py --check` (clean;
                the last may rewrite tracked decisions/judgment-records/*.json byte-identically, and git status
                afterwards must show only your files). grep shows no "Path.home" or "/opt/homebrew" or
                "Documents/GitHub" in src/toaster/tools.py.
Premises:       `.tools/` is not already in .gitignore; modelcheck.verify_holds has a `z3` parameter (read it
                and describe how it is used, so PUB-2 can pass the resolved path correctly).
Questions to:   the orchestrator
Report:         branch and commit, model run on, test list, every check's output, what verify_holds does with its
                z3 argument (quote the lines), anything flagged and not fixed.
```

- [ ] **Step 1:** Create worktree `tools` (branch `pub/tools`) off `pages-publishing`; write the contract to `CONTRACT.md`; dispatch builder.
- [ ] **Step 2:** Dispatch reviewer (different model) to re-run the tests, read the resolution-order logic against this contract, and try the three failure modes by hand.
- [ ] **Step 3:** Merge on PASS; remove worktree and branch.

## Task 2: Notebooks use the resolver (PUB-2)

**Files:** Modify the source of exactly these code cells: `chapters/ch05-architecture/03-interfaces.ipynb` cell-16 (index 16); `chapters/ch08-checking/02-violation-witness.ipynb` cell-11 (index 11); `chapters/ch10-traceability-signoff/01-traceability-graph.ipynb` cells `4d859570` (index 25) and `3850dee3` (index 46); `exercises/ch08/exercise.ipynb` cell-09 (index 9).

**Interfaces:** Consumes `toaster.tools` from PUB-1 (names above). Produces notebooks with no `Path.home()`, `/opt/homebrew` or `Documents/GitHub` anywhere.

```
CONTRACT PUB-2 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          blocked_on PUB-1 merged; unblock_when `from toaster.tools import resolve_sysmlv2` works on pages-publishing; owner orchestrator
Task:           Replace every hard-coded tool location in the six cells above with calls to toaster.tools, keeping
                every printed output and every ReviewRecord field byte-identical.
Context:        Survey section 1 (cells that name a path); a1-clean-checkout.md "Premise check" lists each line.
                Today: ch05-03 cell-16 sets BINARY, LIB, PLANTUML_JAR, JAVA (the last two under
                /opt/homebrew) and calls render_toolkit_interconnection(lib=, binary=, plantuml_jar=, java=);
                ch08-02 cell-11 sets BINARY, LIB and calls mc.verify_holds(path, lib=str(LIB), binary=str(BINARY),
                solve=True); cells 13 and 15 reuse BINARY and LIB; ch10-01 cell 4d859570 reads a file under
                Path.home()/.../sysml.library/"Systems Library"/Requirements.sysml; cell 3850dee3 sets
                SYSMLV2_BINARY and SYSMLV2_LIB, asserts the binary exists (message cites a work contract), and
                shells out `[binary, "verify", model, "--lib", lib, "--solve"]` (cell 9cc5f8de reuses the names);
                exercises/ch08 cell-09 mirrors ch08-02 cell-11. `sysmlv2 verify --solve` finds `z3` on PATH, so
                subprocess calls must use `env=tool_env()`; for mc.verify_holds pass the resolved z3 the way
                PUB-1's report says verify_holds uses its `z3` argument.
Non-goals:      Do not change any other cell, output, execution_count, id, metadata. Do not change
                modelcheck.py/render.py. Keep variable names (BINARY, LIB, SYSMLV2_BINARY, SYSMLV2_LIB, ...) so
                downstream cells keep working; only their right-hand sides change. Keep prose, comments and
                narration unchanged except: drop the clause "(see work contract CH05-TOOLKIT-VIZ)" and
                "(see work contract PASS4-008)" that sit in assert messages you are removing anyway.
Blast zone:     the six cells' `source` in the four notebooks above -- on branch pub/nbtools in worktree
                .claude/worktrees/nbtools. Edit by direct JSON text substitution asserting exactly one match
                per substitution; NO nbconvert --inplace.
Acceptance:     (1) Cell-by-cell json comparison against the parent: only the six cells' `source` differ; their
                outputs/execution_count unchanged. (2) `grep -rnE "Path\.home\(\)|/opt/homebrew|Documents/GitHub"
                chapters exercises` returns nothing. (3) With the tools available via environment variables
                (`SYSMLV2_BINARY=/Users/z/Documents/GitHub/sysml-toolkit/target/release/sysmlv2`,
                `SYSMLV2_LIB_DIR=/Users/z/Documents/GitHub/sysml-toolkit/spec-refs/SysML-v2-Release/sysml.library`,
                `PLANTUML_JAR=/opt/homebrew/opt/plantuml/libexec/plantuml.jar`,
                `JAVA=/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home/bin/java`,
                `Z3=$(command -v z3)`) execute throwaway COPIES of ch05-03, ch08-01/02/03 and ch10-01 with
                nbclient and compare each code cell's outputs to the tracked notebook's stored outputs (join
                adjacent same-stream chunks first; ignore the `<IPython.core.display.SVG object>` repr of figure
                cells whose stored output is empty): zero differences, zero error cells; the regenerated
                figures/ch05-interconnection.svg is byte-identical to the tracked file; decisions/judgment-records
                are byte-identical afterwards (git status clean except your cells). (4) With those variables unset
                and no .tools, the same ch08-02 copy fails with ToolNotFoundError whose message names
                SYSMLV2_BINARY and the provisioning command (show it). (5) repo checks clean.
Premises:       The six cells match the description above at HEAD (verify; report any divergence); PUB-1 merged.
Questions to:   the orchestrator
Report:         branch and commit, model, the six cells' before/after source, comparison results, the
                no-tools failure message, every check's output.
```

- [ ] **Step 1:** After PUB-1 merges: worktree `nbtools` (branch `pub/nbtools`) off `pages-publishing`; write contract; dispatch builder; dispatch reviewer (re-run comparison for ch08-02 and ch10-01 independently and the no-tools failure); merge on PASS.

## Task 3: Tests and scripts without local paths, plus a guard test (PUB-3)

**Files:** Modify `tests/test_render_toolkit_interconnection.py`, `tests/test_modelcheck.py`, `tests/test_ch08_conservation_property.py`, `scripts/diagram_study/provision_check.py`. Create `tests/test_no_local_paths.py`.

```
CONTRACT PUB-3 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          blocked_on PUB-2 merged (the guard test scans notebooks); owner orchestrator
Task:           Remove hard-coded home and Homebrew paths from tests/ and scripts/ using toaster.tools, so the
                suite runs the toolkit-dependent tests on any provisioned machine and SKIPS them with an
                actionable reason elsewhere; add a test that fails if a local path reappears anywhere shippable.
Context:        a1-clean-checkout.md flag 2: tests/test_render_toolkit_interconnection.py:14-21,
                tests/test_modelcheck.py:17-20, tests/test_ch08_conservation_property.py:18-21 and
                scripts/diagram_study/provision_check.py:53 name ~/Documents/GitHub/sysml-toolkit and
                /opt/homebrew paths. src/toaster/bootstrap.py:50 uses Path.home()/".opensysml"/"bin" as a cache
                directory (benign, allowed).
Non-goals:      No change to the behaviour under test. Do not weaken an assertion; a test that cannot find a tool
                skips via pytest.skip with a message naming the variable and `uv run python scripts/provision-tools.py`
                (use ToolNotFoundError from toaster.tools to decide). Do not edit src/.
Blast zone:     the four files above and tests/test_no_local_paths.py -- on branch pub/testpaths in worktree
                .claude/worktrees/testpaths.
Acceptance:     tests/test_no_local_paths.py parametrizes over (a) every code cell source in chapters/**.ipynb
                and exercises/**.ipynb, and (b) every .py under src/, tests/, scripts/, and fails on any of
                `Path.home()`, `/opt/homebrew`, `Documents/GitHub`, `/Users/`, `/home/`; the allowlist is exactly:
                this test file itself, and the single line in src/toaster/bootstrap.py containing
                `".opensysml"`. It fails (demonstrate on a temp copy, not the tracked file) when a forbidden
                string is added to a notebook cell and to a .py file. With SYSMLV2_BINARY, SYSMLV2_LIB_DIR,
                PLANTUML_JAR, JAVA and Z3 set as in PUB-2 acceptance (3), `uv run pytest tests/ glossary/tests/ -q`
                passes AND the previously path-dependent tests actually run (report the count of skipped tests
                before and after; show `-rs` output); with them unset they skip with the actionable message and
                the suite still passes. Repo checks clean.
Premises:       The four files contain the paths described (grep and report line numbers); PUB-2 merged.
Questions to:   the orchestrator
Report:         branch and commit, model, diff, skipped-test counts with and without the variables, demonstration
                of the guard test failing, every check's output.
```

- [ ] **Step 1:** After PUB-2: worktree `testpaths`; contract; builder; reviewer (re-run with and without the variables); merge on PASS.

## Task 4: Pinned tool provisioning (PUB-4)

**Files:** Create `scripts/provision-tools.py`, `scripts/tool-pins.json`, `tests/test_provision_tools.py`. Modify `scripts/check-tools.py`.

**Interfaces:**
- Produces: `scripts/provision-tools.py [--dest DIR] [--check]`: downloads the pinned tools for the current platform into `DIR` (default `<repo>/.tools`) using the layout PUB-1 resolves (`bin/sysmlv2`, `bin/z3`, `sysml.library/`, `plantuml.jar`); verifies every download against the pinned sha256 before use; idempotent (an existing file whose sha256 matches is kept); `--check` verifies existing files' hashes and exits non-zero on any mismatch or absence; prints the resolved paths and the equivalent `export` lines. Importable functions with these exact names for tests: `verify_sha256(path: Path, expected: str) -> None` (raises `ValueError` on mismatch), `extract_member(archive: Path, member_suffix: str, dest: Path) -> Path`, `current_platform() -> tuple[str, str]` returning `("linux"|"darwin", "x86_64"|"arm64")`, `load_pins(path: Path) -> dict`.
- `tool-pins.json` schema: `{"sysmlv2": {"version": "v0.9.1", "assets": {"linux-x86_64": {"url", "sha256", "member"}, "darwin-arm64": {...}, "darwin-x86_64": {...}}}, "z3": {"version": "z3-5.1.0", "assets": {...same keys...}}, "plantuml": {"version", "url", "sha256"}, "library": {"repo": "https://github.com/Systems-Modeling/SysML-v2-Release", "commit": "de1070ae8e79c21532b8004fc663d47b35d0e9fa"}}`.

```
CONTRACT PUB-4 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          blocked_on PUB-1 merged; owner orchestrator
Task:           Implement the provisioning script, pins file, tests, and extend check-tools.py to report the
                resolved tools.
Context:        The exact steps already proven on a real runner are in the diagnostic workflow:
                `git show origin/pub/diagnose:.github/workflows/pages-diagnose.yml` (toolkit tarball download and
                sha256 -c, Z3 zip layout `z3-5.1.0-x64-glibc-2.39/bin/z3`, PlantUML jar download, sparse clone of
                SysML-v2-Release at the pinned commit). Pins are in this plan's Global Constraints. Read the real
                values for platforms not listed there from the release pages and record how: toolkit
                `SHA256SUMS` for darwin-x86_64 and (if you add it) linux-aarch64; the Z3 release assets for
                macOS (`gh release view z3-5.1.0 --repo Z3Prover/z3 --json assets`; GitHub publishes a digest per
                asset); if Z3 publishes no macOS asset for a platform, leave that key absent so the script says
                "install z3 via your package manager (brew install z3) and set Z3" rather than guessing.
                scripts/check-tools.py currently calls toaster.bootstrap.provision() (checks `dot`, downloads the
                OpenSysML binaries); keep that behaviour.
Non-goals:      Do not run the real downloads in tests (tests use tiny fake tar/zip archives built in tmp_path and a
                fake pins file). Do not commit any downloaded file. Do not install Java (check-tools reports it).
                Do not edit notebooks, src/toaster/tools.py or docs (PUB-7 documents it).
Blast zone:     scripts/provision-tools.py, scripts/tool-pins.json, scripts/check-tools.py,
                tests/test_provision_tools.py -- on branch pub/provision in worktree .claude/worktrees/provision.
Acceptance:     Offline tests: verify_sha256 passes and fails correctly; extract_member finds a member by suffix
                in a .tar.gz and a .zip and preserves the executable bit; a pins entry with a wrong sha256 makes
                provision fail BEFORE anything is installed (nothing left in dest); idempotence (second run
                downloads nothing: inject a fake downloader and assert it was not called); --check exit codes;
                unsupported platform gives a message listing the supported keys and the environment variables.
                Real run on this machine (macOS arm64): `uv run python scripts/provision-tools.py --dest
                <scratch>/.tools` completes, `--check` exits 0, `<scratch>/.tools/bin/sysmlv2 --version` prints
                `sysmlv2 0.9.1`, `sysml.library/"Systems Library"/Requirements.sysml` exists, the jar renders
                figures/ch05-interconnection.puml (copy it to scratch) with exit 0; then with
                REPO_ROOT patched or `.tools` created by a scratch copy of the repo, `uv run python
                scripts/check-tools.py` prints each resolved tool and its version and exits 0; with the dest
                removed it exits non-zero with the provisioning command in the message. The Linux key is
                verified by hash only: download the linux asset into scratch and check its sha256 equals the pin
                (do not execute it). Repo checks clean; `.tools/` is ignored by git (git status shows nothing).
Premises:       PUB-1 merged (.gitignore has `.tools/`); the pins in Global Constraints still match the live
                release digests (re-verify each with `gh release view` and report).
Questions to:   the orchestrator
Report:         branch and commit, model, pins file content, real-run output, hash re-verification table,
                every check's output, anything flagged and not fixed.
```

- [ ] **Step 1:** After PUB-1: worktree `provision` (branch `pub/provision`); contract; builder; reviewer (re-verify every pin from the live releases and re-run the real provisioning in scratch); merge on PASS.

## Task 5: Site gate `scripts/check-site.py` (PUB-5)

**Files:** Create `scripts/check-site.py`, `scripts/site-baseline.json`, `tests/test_check_site.py`.

**Interfaces:** CLI `uv run python scripts/check-site.py --site _build/html --content _build/site/content --log build.log --base-url /toaster [--baseline scripts/site-baseline.json]`; exit 0 only if every check passes; prints one `PASS`/`FAIL` line per check and the offending items. `scripts/site-baseline.json` is `{"figures": 18}`. Importable check functions, each returning `list[str]` of failures (empty = pass): `check_log(log_text: str) -> list[str]`, `check_figures(content_dir: Path, expected: int) -> list[str]`, `check_leaks(site_dir: Path, extra: Sequence[str] = ()) -> list[str]`, `check_published_files(site_dir: Path) -> list[str]`, `check_links(site_dir: Path, base_url: str) -> list[str]`.

```
CONTRACT PUB-5 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          ready (independent of PUB-2..4; blocked_on PUB-1 only for the shared branch)
Task:           Implement the release gate from the survey's measured facts.
Checks:         (1) check_log: FAIL on any line containing `An exception occurred during code execution`,
                `Could not load Jupyter session manager`, `Jupyter server did not start` (strip ANSI first).
                (2) check_figures: count output nodes with a `jupyter_data.data` key starting `image/` across
                `<content>/*.json` (recursively through dict/list); FAIL unless the count equals the baseline
                (18) -- report the per-page counts. (3) check_leaks: FAIL if any text file under the site
                (grep -I semantics, skip binary) contains `/home/runner`, `/opt/homebrew`, `Documents/GitHub`,
                `/Users/`, `/var/folders`, or any extra string passed (the CLI adds `str(Path.home())` and
                the current working directory path). (4) check_published_files: FAIL if `<site>/build/` contains
                any file named `exercise*` or `DEFERRED*` (MyST publishes linked non-page files there; PA-1
                measured exercises ch01-ch08 and DEFERRED.md). (5) check_links: parse every .html under the
                site with html.parser; for each href/src beginning with `/`: it must begin with the base URL,
                and after stripping the base must resolve to an existing file or a directory with index.html in
                the site; skip `http(s)://`, `mailto:`, `#`-only; report broken ones with the page. (A prior
                checker found 2305 internal refs, 0 broken, and a wrong-base negative control found thousands.)
Context:        a1-clean-checkout.md (F2, F4, F5, F6, F7) and a2-real-runner.md; the figure-count snippet in
                `git show origin/pub/diagnose:.github/workflows/pages-diagnose.yml`.
Non-goals:      No CI workflow, no docs, no notebook changes. No network. Do not make a check pass by loosening
                it; thresholds come from the baseline file only.
Blast zone:     scripts/check-site.py, scripts/site-baseline.json, tests/test_check_site.py -- on branch
                pub/checksite in worktree .claude/worktrees/checksite.
Acceptance:     Offline tests build tiny fixture site trees, content JSON and logs in tmp_path and assert each
                check passes on a good fixture and fails on: an exception line in the log; 17 figures vs
                baseline 18; a leaked `/opt/homebrew` string; a `build/exercise-xyz.ipynb` file; a broken link; a
                link with the wrong base. Run on a real build: in a scratch clone with the tools provisioned
                (use environment variables as in PUB-2 acceptance (3)), `BASE_URL=/toaster uv run --frozen npx
                myst build --html --execute 2>&1 | tee build.log`, then run the script: report each check's
                result. EXPECTED at this commit: check_log passes, check_figures passes (18), check_links passes;
                check_leaks and check_published_files FAIL on the not-yet-fixed content (Documents/GitHub in
                notebook source before PUB-2 lands, exercises and DEFERRED.md under build/) -- show those
                failures and say which later contract clears each. Repo checks clean.
Premises:       MyST writes page JSON to `_build/site/content/<slug>.json` and HTML to `_build/html/` (verify on
                the real build); the figure baseline is 18 on a fully working build (a2-real-runner.md).
Questions to:   the orchestrator
Report:         branch and commit, model, test list, real-build output of every check, anything flagged.
```

- [ ] **Step 1:** Worktree `checksite`; contract; builder; reviewer (re-run the real build and the script; try two deliberate regressions on a scratch copy of the built tree); merge on PASS.

## Task 6: Reference cleanup, Chapters 1-4 (PUB-6A)

**Files:** Modify files under `chapters/ch01-system-purpose/**`, `chapters/ch02-requirements/**`, `chapters/ch03-measures/**`, `chapters/ch04-functional-decomp/**` (markdown pages and notebook cells named by the rows).

```
CONTRACT PUB-6A | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          blocked_on PUB-2 merged; owner orchestrator
Task:           Make the published pages of Chapters 1-4 stand alone: apply the PA-4 LINK and REWORD rows for these
                files (41 actionable rows) so no learner-visible sentence points at a file, id or process that
                will not exist on the site.
Context:        decisions/pages-publishing/a4-dangling-references.md (table rows and rulings A1-A10);
                decisions/pages-publishing-survey.md section 4; DL-112 (identity). Chapter 3's index and notebooks are where `models/` and exercise references concentrate.
Rules (identical in every PUB-6 contract; the findings file is the source of truth):
                1. Work from decisions/pages-publishing/a4-dangling-references.md. Apply every row whose file is in
                   the blast zone and whose class is LINK or REWORD, using the row's proposed URL or replacement
                   wording exactly. Rows classed KEEP: no change. Rows tagged A5, A6: no change. Rows tagged A7
                   (edits inside ReviewRecord strings, SysML doc comments, or their stored outputs): NO change in
                   this contract (Task 10 gates them). Rows for cells that PUB-2 already rewrote (the work-contract
                   assert messages in ch05-03 cell-16, ch08-02 cell-11, ch10-01 cells 4d859570/3850dee3): already
                   handled, skip and list them.
                2. LINK means a clickable link: in markdown, `[text](https://github.com/Open-MBEE/toaster/blob/main/<path>)`
                   (directories use `/tree/main/`); a link to another published page uses its in-site relative link.
                   References to exercises/chNN/exercise.ipynb link to
                   https://github.com/Open-MBEE/toaster/blob/main/exercises/chNN/exercise.ipynb; this also stops MyST
                   publishing the exercise notebooks as raw downloads (a1 F6). Never put a URL in an executable
                   line; LINK rows in code are comments only and the table says so.
                3. REWORD means replace the quoted text with the row's replacement wording; if applying a
                   replacement would change a number, a verdict, or a claim the chapter makes, STOP and report that
                   row instead of applying it.
                4. Identity (DL-112): a bare "Z" or "approved by Z" in these files becomes "mzargham (Z)" at the first
                   mention on that page.
                5. Notebooks: patch only the `source` of the cell named in the row by direct JSON text substitution
                   asserting exactly one match; if the row says an output line quotes the same text, patch that
                   stored output text identically; no nbconvert; every other cell/key byte-identical (compare with
                   json). index.md and conclusion.md are plain text edits.
Non-goals:      No prose rewrites beyond the rows. No change to any model file, persisted record
                (decisions/judgment-records/), figure, code logic or output (except identical output-text patches
                where a row says so). Do not touch files outside the blast zone.
Blast zone:     chapters/ch01-system-purpose/**
                chapters/ch02-requirements/**
                chapters/ch03-measures/**
                chapters/ch04-functional-decomp/**
                -- on branch pub/refs-a in worktree .claude/worktrees/refs-a.
Acceptance:     (1) Count of rows applied by class and rows skipped with reason (KEEP, A5/A6/A7, PUB-2, STOP);
                the sum equals the number of rows for the blast-zone files in the findings table. (2) Every
                GitHub URL you added: the path exists (`git cat-file -e origin/main:<path>`; fetch first) and the
                anchor, if any, matches GitHub's slug of the DEFERRED.md heading. (3) Cell-by-cell json comparison:
                only the cells named in applied rows differ, and only in `source` (plus the output text where the
                row says so). (4) Build the site from your worktree (`npx myst build --html`, execution not
                required, BASE_URL=/toaster) with no new warnings relative to the parent build; click-check 5 of
                your added links (a mix of GitHub URLs and in-site links) and report landing URLs; run
                `grep -rE "exercises/ch[0-9]+/exercise" _build/html | grep -v github.com` and report what remains.
                (5) Repo checks clean; git status shows only blast-zone files.
Premises:       Each row's quoted sentence still exists verbatim at HEAD of pages-publishing (verify; report any
                that moved); PUB-2 is merged.
Questions to:   the orchestrator
Report:         branch and commit, model, the counts in Acceptance (1), the list of skipped rows by reason,
                link-click results, every check's output, anything flagged and not fixed.
```

- [ ] **Step 1:** After PUB-2 merges: worktree `refs-a` (branch `pub/refs-a`) off `pages-publishing`; contract to `CONTRACT.md`; dispatch builder.
- [ ] **Step 2:** Dispatch reviewer (different model): sample 25 rows (fixed seed, report it) and confirm each edit against the table; independently grep the blast-zone files for remaining `DEFERRED.md`, `AGENTS.md`, `decisions/`, `exercises/`, `SA-`, `DL-` mentions and reconcile each against the table (KEEP/A7/skipped); click 8 links on a local build.
- [ ] **Step 3:** Merge on PASS; remove worktree and branch.

## Task 6 (cont.): Reference cleanup, Chapters 5-8 (PUB-6B)

**Files:** Modify files under `chapters/ch05-architecture/**`, `chapters/ch06-recursive-decomp/**`, `chapters/ch07-execution/**`, `chapters/ch08-checking/**` (markdown pages and notebook cells named by the rows).

```
CONTRACT PUB-6B | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          blocked_on PUB-2 merged; owner orchestrator
Task:           Make the published pages of Chapters 5-8 stand alone: apply the PA-4 LINK and REWORD rows for these
                files (56 actionable rows) so no learner-visible sentence points at a file, id or process that
                will not exist on the site.
Context:        decisions/pages-publishing/a4-dangling-references.md (table rows and rulings A1-A10);
                decisions/pages-publishing-survey.md section 4; DL-112 (identity). Ch8-02 cell-11 and Ch5-03 cell-16 were rewritten by PUB-2; Ch8 has the most DEFERRED.md entries (D-029, D-030, D-031) and several of them sit in SysML doc comments or record strings (A7: skip).
Rules (identical in every PUB-6 contract; the findings file is the source of truth):
                1. Work from decisions/pages-publishing/a4-dangling-references.md. Apply every row whose file is in
                   the blast zone and whose class is LINK or REWORD, using the row's proposed URL or replacement
                   wording exactly. Rows classed KEEP: no change. Rows tagged A5, A6: no change. Rows tagged A7
                   (edits inside ReviewRecord strings, SysML doc comments, or their stored outputs): NO change in
                   this contract (Task 10 gates them). Rows for cells that PUB-2 already rewrote (the work-contract
                   assert messages in ch05-03 cell-16, ch08-02 cell-11, ch10-01 cells 4d859570/3850dee3): already
                   handled, skip and list them.
                2. LINK means a clickable link: in markdown, `[text](https://github.com/Open-MBEE/toaster/blob/main/<path>)`
                   (directories use `/tree/main/`); a link to another published page uses its in-site relative link.
                   References to exercises/chNN/exercise.ipynb link to
                   https://github.com/Open-MBEE/toaster/blob/main/exercises/chNN/exercise.ipynb; this also stops MyST
                   publishing the exercise notebooks as raw downloads (a1 F6). Never put a URL in an executable
                   line; LINK rows in code are comments only and the table says so.
                3. REWORD means replace the quoted text with the row's replacement wording; if applying a
                   replacement would change a number, a verdict, or a claim the chapter makes, STOP and report that
                   row instead of applying it.
                4. Identity (DL-112): a bare "Z" or "approved by Z" in these files becomes "mzargham (Z)" at the first
                   mention on that page.
                5. Notebooks: patch only the `source` of the cell named in the row by direct JSON text substitution
                   asserting exactly one match; if the row says an output line quotes the same text, patch that
                   stored output text identically; no nbconvert; every other cell/key byte-identical (compare with
                   json). index.md and conclusion.md are plain text edits.
Non-goals:      No prose rewrites beyond the rows. No change to any model file, persisted record
                (decisions/judgment-records/), figure, code logic or output (except identical output-text patches
                where a row says so). Do not touch files outside the blast zone.
Blast zone:     chapters/ch05-architecture/**
                chapters/ch06-recursive-decomp/**
                chapters/ch07-execution/**
                chapters/ch08-checking/**
                -- on branch pub/refs-b in worktree .claude/worktrees/refs-b.
Acceptance:     (1) Count of rows applied by class and rows skipped with reason (KEEP, A5/A6/A7, PUB-2, STOP);
                the sum equals the number of rows for the blast-zone files in the findings table. (2) Every
                GitHub URL you added: the path exists (`git cat-file -e origin/main:<path>`; fetch first) and the
                anchor, if any, matches GitHub's slug of the DEFERRED.md heading. (3) Cell-by-cell json comparison:
                only the cells named in applied rows differ, and only in `source` (plus the output text where the
                row says so). (4) Build the site from your worktree (`npx myst build --html`, execution not
                required, BASE_URL=/toaster) with no new warnings relative to the parent build; click-check 5 of
                your added links (a mix of GitHub URLs and in-site links) and report landing URLs; run
                `grep -rE "exercises/ch[0-9]+/exercise" _build/html | grep -v github.com` and report what remains.
                (5) Repo checks clean; git status shows only blast-zone files.
Premises:       Each row's quoted sentence still exists verbatim at HEAD of pages-publishing (verify; report any
                that moved); PUB-2 is merged.
Questions to:   the orchestrator
Report:         branch and commit, model, the counts in Acceptance (1), the list of skipped rows by reason,
                link-click results, every check's output, anything flagged and not fixed.
```

- [ ] **Step 1:** After PUB-2 merges: worktree `refs-b` (branch `pub/refs-b`) off `pages-publishing`; contract to `CONTRACT.md`; dispatch builder.
- [ ] **Step 2:** Dispatch reviewer (different model): sample 25 rows (fixed seed, report it) and confirm each edit against the table; independently grep the blast-zone files for remaining `DEFERRED.md`, `AGENTS.md`, `decisions/`, `exercises/`, `SA-`, `DL-` mentions and reconcile each against the table (KEEP/A7/skipped); click 8 links on a local build.
- [ ] **Step 3:** Merge on PASS; remove worktree and branch.

## Task 6 (cont.): Reference cleanup, Chapter 9 (PUB-6C)

**Files:** Modify files under `chapters/ch09-coverage-sufficiency/**` (markdown pages and notebook cells named by the rows).

```
CONTRACT PUB-6C | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          blocked_on PUB-2 merged; owner orchestrator
Task:           Make the published pages of Chapter 9 stand alone: apply the PA-4 LINK and REWORD rows for these
                files (30 actionable rows) so no learner-visible sentence points at a file, id or process that
                will not exist on the site.
Context:        decisions/pages-publishing/a4-dangling-references.md (table rows and rulings A1-A10);
                decisions/pages-publishing-survey.md section 4; DL-112 (identity). Includes the `chapters/...ipynb` paths in code font in 02-evidence-completeness cell 9b78b2f5 (REWORD to in-site links) and the `[index.md](index.md)` link labels in 01-requirement-coverage (REWORD to `[Overview](index.md)`).
Rules (identical in every PUB-6 contract; the findings file is the source of truth):
                1. Work from decisions/pages-publishing/a4-dangling-references.md. Apply every row whose file is in
                   the blast zone and whose class is LINK or REWORD, using the row's proposed URL or replacement
                   wording exactly. Rows classed KEEP: no change. Rows tagged A5, A6: no change. Rows tagged A7
                   (edits inside ReviewRecord strings, SysML doc comments, or their stored outputs): NO change in
                   this contract (Task 10 gates them). Rows for cells that PUB-2 already rewrote (the work-contract
                   assert messages in ch05-03 cell-16, ch08-02 cell-11, ch10-01 cells 4d859570/3850dee3): already
                   handled, skip and list them.
                2. LINK means a clickable link: in markdown, `[text](https://github.com/Open-MBEE/toaster/blob/main/<path>)`
                   (directories use `/tree/main/`); a link to another published page uses its in-site relative link.
                   References to exercises/chNN/exercise.ipynb link to
                   https://github.com/Open-MBEE/toaster/blob/main/exercises/chNN/exercise.ipynb; this also stops MyST
                   publishing the exercise notebooks as raw downloads (a1 F6). Never put a URL in an executable
                   line; LINK rows in code are comments only and the table says so.
                3. REWORD means replace the quoted text with the row's replacement wording; if applying a
                   replacement would change a number, a verdict, or a claim the chapter makes, STOP and report that
                   row instead of applying it.
                4. Identity (DL-112): a bare "Z" or "approved by Z" in these files becomes "mzargham (Z)" at the first
                   mention on that page.
                5. Notebooks: patch only the `source` of the cell named in the row by direct JSON text substitution
                   asserting exactly one match; if the row says an output line quotes the same text, patch that
                   stored output text identically; no nbconvert; every other cell/key byte-identical (compare with
                   json). index.md and conclusion.md are plain text edits.
Non-goals:      No prose rewrites beyond the rows. No change to any model file, persisted record
                (decisions/judgment-records/), figure, code logic or output (except identical output-text patches
                where a row says so). Do not touch files outside the blast zone.
Blast zone:     chapters/ch09-coverage-sufficiency/**
                -- on branch pub/refs-c in worktree .claude/worktrees/refs-c.
Acceptance:     (1) Count of rows applied by class and rows skipped with reason (KEEP, A5/A6/A7, PUB-2, STOP);
                the sum equals the number of rows for the blast-zone files in the findings table. (2) Every
                GitHub URL you added: the path exists (`git cat-file -e origin/main:<path>`; fetch first) and the
                anchor, if any, matches GitHub's slug of the DEFERRED.md heading. (3) Cell-by-cell json comparison:
                only the cells named in applied rows differ, and only in `source` (plus the output text where the
                row says so). (4) Build the site from your worktree (`npx myst build --html`, execution not
                required, BASE_URL=/toaster) with no new warnings relative to the parent build; click-check 5 of
                your added links (a mix of GitHub URLs and in-site links) and report landing URLs; run
                `grep -rE "exercises/ch[0-9]+/exercise" _build/html | grep -v github.com` and report what remains.
                (5) Repo checks clean; git status shows only blast-zone files.
Premises:       Each row's quoted sentence still exists verbatim at HEAD of pages-publishing (verify; report any
                that moved); PUB-2 is merged.
Questions to:   the orchestrator
Report:         branch and commit, model, the counts in Acceptance (1), the list of skipped rows by reason,
                link-click results, every check's output, anything flagged and not fixed.
```

- [ ] **Step 1:** After PUB-2 merges: worktree `refs-c` (branch `pub/refs-c`) off `pages-publishing`; contract to `CONTRACT.md`; dispatch builder.
- [ ] **Step 2:** Dispatch reviewer (different model): sample 25 rows (fixed seed, report it) and confirm each edit against the table; independently grep the blast-zone files for remaining `DEFERRED.md`, `AGENTS.md`, `decisions/`, `exercises/`, `SA-`, `DL-` mentions and reconcile each against the table (KEEP/A7/skipped); click 8 links on a local build.
- [ ] **Step 3:** Merge on PASS; remove worktree and branch.

## Task 6 (cont.): Reference cleanup, Chapter 10 (PUB-6D)

**Files:** Modify files under `chapters/ch10-traceability-signoff/**` (markdown pages and notebook cells named by the rows).

```
CONTRACT PUB-6D | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          blocked_on PUB-2 merged; owner orchestrator
Task:           Make the published pages of Chapter 10 stand alone: apply the PA-4 LINK and REWORD rows for these
                files (58 actionable rows) so no learner-visible sentence points at a file, id or process that
                will not exist on the site.
Context:        decisions/pages-publishing/a4-dangling-references.md (table rows and rulings A1-A10);
                decisions/pages-publishing-survey.md section 4; DL-112 (identity). Chapter 10 has the most REWORD rows (31): many sit in ReviewRecord string literals and are tagged A7 (skip, Task 10); apply the rest. Ch10-01 cells 4d859570 and 3850dee3 were rewritten by PUB-2.
Rules (identical in every PUB-6 contract; the findings file is the source of truth):
                1. Work from decisions/pages-publishing/a4-dangling-references.md. Apply every row whose file is in
                   the blast zone and whose class is LINK or REWORD, using the row's proposed URL or replacement
                   wording exactly. Rows classed KEEP: no change. Rows tagged A5, A6: no change. Rows tagged A7
                   (edits inside ReviewRecord strings, SysML doc comments, or their stored outputs): NO change in
                   this contract (Task 10 gates them). Rows for cells that PUB-2 already rewrote (the work-contract
                   assert messages in ch05-03 cell-16, ch08-02 cell-11, ch10-01 cells 4d859570/3850dee3): already
                   handled, skip and list them.
                2. LINK means a clickable link: in markdown, `[text](https://github.com/Open-MBEE/toaster/blob/main/<path>)`
                   (directories use `/tree/main/`); a link to another published page uses its in-site relative link.
                   References to exercises/chNN/exercise.ipynb link to
                   https://github.com/Open-MBEE/toaster/blob/main/exercises/chNN/exercise.ipynb; this also stops MyST
                   publishing the exercise notebooks as raw downloads (a1 F6). Never put a URL in an executable
                   line; LINK rows in code are comments only and the table says so.
                3. REWORD means replace the quoted text with the row's replacement wording; if applying a
                   replacement would change a number, a verdict, or a claim the chapter makes, STOP and report that
                   row instead of applying it.
                4. Identity (DL-112): a bare "Z" or "approved by Z" in these files becomes "mzargham (Z)" at the first
                   mention on that page.
                5. Notebooks: patch only the `source` of the cell named in the row by direct JSON text substitution
                   asserting exactly one match; if the row says an output line quotes the same text, patch that
                   stored output text identically; no nbconvert; every other cell/key byte-identical (compare with
                   json). index.md and conclusion.md are plain text edits.
Non-goals:      No prose rewrites beyond the rows. No change to any model file, persisted record
                (decisions/judgment-records/), figure, code logic or output (except identical output-text patches
                where a row says so). Do not touch files outside the blast zone.
Blast zone:     chapters/ch10-traceability-signoff/**
                -- on branch pub/refs-d in worktree .claude/worktrees/refs-d.
Acceptance:     (1) Count of rows applied by class and rows skipped with reason (KEEP, A5/A6/A7, PUB-2, STOP);
                the sum equals the number of rows for the blast-zone files in the findings table. (2) Every
                GitHub URL you added: the path exists (`git cat-file -e origin/main:<path>`; fetch first) and the
                anchor, if any, matches GitHub's slug of the DEFERRED.md heading. (3) Cell-by-cell json comparison:
                only the cells named in applied rows differ, and only in `source` (plus the output text where the
                row says so). (4) Build the site from your worktree (`npx myst build --html`, execution not
                required, BASE_URL=/toaster) with no new warnings relative to the parent build; click-check 5 of
                your added links (a mix of GitHub URLs and in-site links) and report landing URLs; run
                `grep -rE "exercises/ch[0-9]+/exercise" _build/html | grep -v github.com` and report what remains.
                (5) Repo checks clean; git status shows only blast-zone files.
Premises:       Each row's quoted sentence still exists verbatim at HEAD of pages-publishing (verify; report any
                that moved); PUB-2 is merged.
Questions to:   the orchestrator
Report:         branch and commit, model, the counts in Acceptance (1), the list of skipped rows by reason,
                link-click results, every check's output, anything flagged and not fixed.
```

- [ ] **Step 1:** After PUB-2 merges: worktree `refs-d` (branch `pub/refs-d`) off `pages-publishing`; contract to `CONTRACT.md`; dispatch builder.
- [ ] **Step 2:** Dispatch reviewer (different model): sample 25 rows (fixed seed, report it) and confirm each edit against the table; independently grep the blast-zone files for remaining `DEFERRED.md`, `AGENTS.md`, `decisions/`, `exercises/`, `SA-`, `DL-` mentions and reconcile each against the table (KEEP/A7/skipped); click 8 links on a local build.
- [ ] **Step 3:** Merge on PASS; remove worktree and branch.

## Task 7: Docs, README and identity (PUB-7)

**Files:** Modify `README.md`, `docs/setup.md`, `docs/contributor.md`, `docs/reproducibility.md`, `docs/references.md`, `docs/case-studies/2026-09-30-energy-conservation-requirement-tie.md`, `AGENTS.md` (one paragraph in Part 1 only).

```
CONTRACT PUB-7 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          blocked_on PUB-4 merged (documents scripts/provision-tools.py) and PUB-2 merged; owner orchestrator
Task:           Make the published and contributor-facing documents true for a repo that builds and deploys to
                GitHub Pages, apply the PA-4 rows for docs pages, and record who "Z" is.
Context:        a4-dangling-references.md (docs rows: setup.md, reproducibility.md, references.md, the case study,
                contributor.md); a1-clean-checkout.md F1 (docs/setup.md and README document `npx mystmd start
                --execute` with no venv, which starts the wrong Jupyter); DL-112 (identity); the A1-A10 rulings in
                this plan's Global Constraints; scripts/provision-tools.py (PUB-4) for the exact command and flags;
                src/toaster/tools.py (PUB-1) for the five environment variable names.
Required edits: (a) README.md quick start and docs/setup.md "Preview the rendered book locally": use
                `uv run npx mystmd start --execute` (and the build form `BASE_URL=/toaster uv run --frozen npx
                myst build --html --execute`), with one sentence saying why `uv run` is needed (MyST must find the
                project's Jupyter). (b) docs/setup.md: a short "Tools for chapters 5, 8 and 10" section:
                `uv run python scripts/provision-tools.py` (downloads pinned sysml-toolkit, Z3, PlantUML jar and the
                SysML library into the gitignored .tools/), a table of the five environment variables and what each
                overrides, that Java 17+ and Graphviz come from the system, and `uv run python scripts/check-tools.py`
                to verify; remove the statements that deployment is off (setup.md L42 and L58 at the time of the
                survey). (c) docs/contributor.md "Deployment status" and docs/reproducibility.md L43: replace with
                the truth: CI builds the book on every pull request and deploys it from main to
                https://open-mbee.github.io/toaster/; pull-request builds do not deploy; the release gate is
                scripts/check-site.py. (d) Apply every LINK and REWORD row of the findings table for the docs pages and
                the case study, per the rules in Task 6 (A1: contributor.md KEEP with a GitHub link at the first mention
                of each harness file; A2/A4: AGENTS.md and decisions/log.md cited as the source of text are links,
                the case study's `Related:` line links decisions/next-passes.md and the log; A3/DL-112: "mzargham (Z)"
                at first mention, "approved by Z" in references.md becomes "approved by mzargham (Z)"; A10:
                reproducibility.md links the `decisions/` directory). (e) docs/reproducibility.md: one sentence and
                link noting that D-nnn ids quoted inside record text refer to DEFERRED.md on GitHub
                (https://github.com/Open-MBEE/toaster/blob/main/DEFERRED.md). (f) docs/contributor.md: a short
                "Who is Z" paragraph: "Z" is the contributor identity `mzargham` (Michael Zargham, GitHub
                `mzargham`), the project's author and chief engineer; other contributors are named by their own
                handles and "Z" is never reused. (g) AGENTS.md Part 1: the same fact as one short paragraph near the
                top of Part 1 (identity of "Z"), and nothing else in AGENTS.md changes.
Non-goals:      No chapter pages, notebooks or code. No change to the glossary. Do not claim the site is live at a
                URL beyond stating where CI deploys it.
Blast zone:     the seven files above -- on branch pub/docs in worktree .claude/worktrees/docs.
Acceptance:     (1) every command in the docs is run verbatim in a scratch clone (or its non-destructive form) and
                works: provision, check-tools, `uv run npx mystmd start --execute` starts Jupyter and serves (run it
                briefly, fetch /, stop it). (2) The env var names in the table equal the names in src/toaster/tools.py
                (grep both). (3) Rows applied/skipped counts as in Task 6 acceptance (1), for the docs and case study
                pages. (4) AGENTS.md diff is exactly one added paragraph (show `git diff --stat` and the hunk).
                (5) `uv run python -m glossary check` clean (the docs pages are rendered by the glossary lint: no
                new findings); local build with no new warnings; pytest and check_construction clean.
Premises:       The survey's quoted statements (setup.md L42/L58, contributor.md "Deployment status",
                reproducibility.md L43) exist at HEAD; quote and replace the actual text.
Questions to:   the orchestrator
Report:         branch and commit, model, diff, command-verification outputs, counts, flags.
```

- [ ] **Step 1:** After PUB-4 (and PUB-2) merge: worktree `docs` (branch `pub/docs`); contract; builder; reviewer (run the documented commands from a fresh clone as a newcomer would; check the AGENTS.md hunk); merge on PASS.

## Task 8: CI build, gate and Pages deploy (PUB-8)

**Files:** Modify `.github/workflows/ci.yml`.

```
CONTRACT PUB-8 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          blocked_on PUB-3, PUB-4, PUB-5 merged (and PUB-6A..D merged before the first full green run); owner orchestrator
Task:           Replace the placeholder pipeline with the real one: provision tools, test, build the book with
                execution, run the release gate, upload artifacts, and deploy only from main.
Context:        decisions/pages-publishing/a2-real-runner.md (the proven runner steps and 95 s timing);
                `git show origin/pub/diagnose:.github/workflows/pages-diagnose.yml`; the current ci.yml (uv 0.5.x,
                setup-node with .nvmrc, `npm ci`, apt graphviz, check-tools, pytest; `deploy` job is `if: false`).
                a1 F2: `myst build` exits 0 despite cell errors, `--strict` exits 1 on them.
Pipeline:       Triggers: `pull_request`; `push` to `main` and to `pages-publishing` (the integration branch trigger
                is for validation runs and is removed by the orchestrator before the pull request). Job `build`
                (ubuntu-latest, permissions contents: read): checkout; setup-uv (keep the existing version pin unless
                it fails; print `uv --version`, `python --version`, `node --version` into the job summary); setup-node
                from .nvmrc; `uv sync --locked`; `npm ci`; apt `graphviz openjdk-17-jre-headless`; cache `.tools/` with
                actions/cache@v4 keyed on `hashFiles('scripts/tool-pins.json')`; `uv run python
                scripts/provision-tools.py`; `uv run python scripts/check-tools.py`; `uv run pytest tests/
                glossary/tests/ -v --tb=short` (the toolkit-dependent tests now run for real); then the book build
                with `set -o pipefail`: `BASE_URL=/toaster uv run --frozen npx myst build --html --execute 2>&1 | tee
                build.log` (add `--strict` ONLY if your local measurement below shows it exits 0 on a clean,
                fully provisioned build despite the 98 existing warnings; otherwise omit it and rely on
                check-site.py check 1, and say so in the report); then `uv run python scripts/check-site.py --site
                _build/html --content _build/site/content --log build.log --base-url /toaster`. Always upload
                build.log (upload-artifact@v4). On `push` to `main` only: upload `_build/html` with
                actions/upload-pages-artifact@v3. Job `deploy` (needs: build; `if: github.event_name == 'push' &&
                github.ref == 'refs/heads/main'`; permissions pages: write, id-token: write; environment
                name: github-pages with url from the deploy step's page_url; concurrency group `pages`,
                cancel-in-progress false; step actions/deploy-pages@v4). No secrets; every action pinned to a
                major version tag.
Non-goals:      No other workflow files. Do not enable Pages (a repository setting; Z does it in Task 9). Do not push.
Blast zone:     .github/workflows/ci.yml -- on branch pub/ci in worktree .claude/worktrees/ci.
Acceptance:     (1) `uvx --from actionlint-py --with shellcheck-py actionlint .github/workflows/ci.yml` clean (paste
                output). (2) Local measurement: in a scratch clone with tools provisioned via
                scripts/provision-tools.py, run the exact build command with and without `--strict`: report exit
                codes and the final line each prints, and state the decision. (3) The workflow's job-level `if` on
                deploy is exactly the main-push condition above, and a pull_request or pages-publishing push cannot
                reach the deploy job or the Pages artifact upload (explain by quoting both conditions). (4) Every
                step name and command in the YAML exists as written in the repo (scripts, flags): `uv run python
                scripts/provision-tools.py --help` etc. (5) The workflow still runs the pytest and glossary
                checks the old one did. The orchestrator then pushes pages-publishing and the first validation run
                must be green; the builder is re-engaged to fix anything the runner shows.
Premises:       PUB-3, PUB-4, PUB-5 merged; scripts exist with the interfaces in Tasks 3-5.
Questions to:   the orchestrator
Report:         branch and commit, model, actionlint output, the --strict measurement and decision, the two deploy
                conditions quoted, flags.
```

- [ ] **Step 1:** After PUB-3, PUB-4, PUB-5 merge: worktree `ci` (branch `pub/ci`); contract; builder; reviewer (actionlint with shellcheck, trace every step against the repo, reason through the trigger/permission matrix for pull_request, branch push and main push).
- [ ] **Step 2 (orchestrator, with Z's go-ahead because it pushes a branch and uses Actions minutes):** merge into `pages-publishing`; `git push -u origin pages-publishing`; watch the run with `gh run view` in a wait loop (`until [ "$(gh run view <id> --json status --jq .status)" = completed ]`; macOS has no `timeout`); download `build-log`; run `scripts/check-site.py` yourself on the downloaded Pages-equivalent tree if the job failed; send failures back to the builder.
- [ ] **Step 3:** Repeat until one run is green with `check-site.py` passing all five checks and the deploy job skipped (branch push).

## Task 9: First deploy (PUB-9)

No builder; this is the orchestrator's release procedure with Z.

- [ ] **Step 1:** All contracts merged into `pages-publishing`; the three repo checks and a green CI run on the branch. Remove the `pages-publishing` push trigger from `ci.yml` (one commit: "CI: remove integration-branch trigger"); push.
- [ ] **Step 2 (Z's go-ahead):** open the pull request `pages-publishing` into `main` (body: the survey's findings and the contract list; test plan lists the CI jobs). Auto-fix on. The PR build must be green and its `deploy` job skipped.
- [ ] **Step 3 (Z only, repository admin):** Settings, Pages, Source: "GitHub Actions". The orchestrator cannot do this and does not try.
- [ ] **Step 4 (Z's merge):** after Z merges, watch the `main` run: build green, `deploy` runs, the Pages URL is reported by the deploy step.
- [ ] **Step 5 (smoke test, orchestrator):** `curl -sS -o /dev/null -w '%{http_code}'` returns 200 for `https://open-mbee.github.io/toaster/`, `/toaster/setup`, `/toaster/glossary`, `/toaster/part-def`, `/toaster/interfaces`, `/toaster/judgment-synthesis`; `https://open-mbee.github.io/toaster/interfaces.json` contains `image/svg+xml`; `https://open-mbee.github.io/toaster/judgment-synthesis.json` contains `image/svg+xml`; no page body contains `Documents/GitHub` or `/opt/homebrew` (grep the fetched HTML of those six pages).
- [ ] **Step 6:** Log the deploy in `decisions/log.md` (DL entry: date, merge commit, run id, URL, gate results); update the survey status; save a memory reference with the live URL.

## Task 10: ACE gate for the A7 rows (decision, no builder)

PA-4 tagged 19 rows A7: reword or link text that sits inside `ReviewRecord` string literals, their stored outputs, or SysML doc comments mirrored in `models/*.sysml`. The survey default (and this plan's Global Constraints) is: leave them unchanged. Editing them would change `models/ch08-cumulative.sysml` and `models/ch10-cumulative.sysml`, make `AS-C08.json`'s `content_hash` (`35b4bff8...`) stale until ch08 nb02 is re-run and re-persisted, and change the stored staleness outputs in ch08 nb03 and ch09 nb03.

- [ ] **Step 1:** Dispatch the ACE with: the A7 rows (list them from the findings file), the blast radius above, and the question "may these remain unchanged on the public site, or does any row need a change?" Outcome A (default, expected): unchanged; record the ruling in `decisions/log.md`; no contract is needed, and PUB-7's DEFERRED.md pointer on the reproducibility page is the mitigation. Outcome B: the ACE names specific rows to change; the orchestrator then writes PUB-6E from the Task 6 template restricted to those rows, adding the required ordering (edit both model files and the fragment together; re-run ch08 nb02 to re-persist `AS-C08.json`; re-run downstream notebooks' stored outputs only as the persisted staleness results require) and runs it before PUB-8's final validation. This plan is complete under Outcome A; Outcome B adds one contract.

---

## Self-review

- **Spec coverage:** decision 1 (execute in CI) PUB-8; 2 (one resolver) PUB-1/2/3; 3 (pinned provisioning) PUB-4; 4 (deploy from main only) PUB-8/9; 5 (dangling references) PUB-6A..D, PUB-7, Task 10; 6 (Z-only Pages step) PUB-9 step 3. Spec verification paragraph: zero cell errors, figure baseline, leak scan, link check are `check-site.py` checks 1-5 and run in CI. Open questions: Q1 answered (95 s), Q2/Q3 rulings in Global Constraints.
- **Survey coverage:** F1 (uv run) PUB-7, PUB-8; F2 (exit 0 on errors) PUB-5 check 1, PUB-8 `--strict` measurement; F3/F9 PUB-2, PUB-3; F4 (figures in page JSON) PUB-5 check 2; F5 leaks PUB-2, PUB-5 check 3; F6 published exercises/DEFERRED.md PUB-6, PUB-5 check 4; F7 links PUB-5 check 5; F8 unpinned inputs: tool versions are recorded in the job summary (PUB-8) and the book theme pin is left as a documented open item below. Z3 on Linux PUB-4/PUB-8.
- **Known open items, not in scope:** MyST downloads the book theme from `refs/heads/main.zip` at build time (survey F8); a theme change could break a future build. Pinning it needs a MyST option not yet investigated; record as a `DEFERRED.md` item when PUB-7 lands. The 59 "Extension inferred" and 39 "Duplicate identifier" warnings are left as they are.
- **Types and names:** `resolve_sysmlv2/resolve_library/resolve_plantuml_jar/resolve_java/resolve_z3/tool_env/ToolNotFoundError/REPO_ROOT` (PUB-1) are the names used in PUB-2, PUB-3, PUB-7; env variable names identical across PUB-1, PUB-2, PUB-3, PUB-7; `check_log/check_figures/check_leaks/check_published_files/check_links` (PUB-5) match PUB-8's use; `.tools/` layout identical in PUB-1 and PUB-4; pins identical in Global Constraints and PUB-4.
