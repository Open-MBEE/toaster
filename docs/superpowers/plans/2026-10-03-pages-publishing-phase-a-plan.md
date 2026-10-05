# Pages Publishing Implementation Plan (Phase A: discovery; Phase B outline)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. This repo's own harness applies: every task is a CONTRACT per `decisions/work-contract-template.md`, run through `decisions/task-states.md`, author and reviewer on different pinned models, worktree per task created by the orchestrator, plain commits (no trailers), subagents never merge or push.

**Goal:** Find out exactly what stops the book from building and publishing on a clean GitHub Pages pipeline, and fix it, so a green pull-request build on a clean runner yields the published site.

**Architecture:** Two phases, as in the diagram-text-integration and judgment-record-store initiatives. Phase A is read-mostly discovery on a clean machine, a real `ubuntu-latest` runner, and a content scan; its output is `decisions/pages-publishing-survey.md`. Phase B (outlined here, specified as full contracts in a second plan once the survey exists) adds a tool resolver, removes hard-coded paths, provisions the toolkit by pinned download, adds the CI build and Pages deploy, and cleans dangling references.

**Tech Stack:** MyST (`mystmd` 1.11.0), `uv`, Python >= 3.12, `opensysml==0.9.0`, sysml-toolkit `sysmlv2` release binary, GitHub Actions (`actions/upload-pages-artifact`, `actions/deploy-pages`), Graphviz, Java + PlantUML.

**Spec:** `docs/superpowers/specs/2026-10-03-pages-publishing-design.md` (read it first; decisions 1-6 and Q1-Q3 apply to every task).

## Global Constraints

- Notebook edits follow the minimal-diff standard (DL-099): patch only the named cells' `source`; never `jupyter nbconvert --execute --inplace` a tracked notebook; run notebooks only in throwaway copies.
- Commit messages are plain: no `Co-Authored-By` or any trailer. Subagents do not push, merge or open PRs.
- No PDF or secret is ever committed. Downloaded tool binaries stay in scratch directories or caches, never in the repo.
- Phase A changes no learner-facing file. Its only tracked outputs are the findings files named in each contract and one throwaway workflow file on the branch `pub/diagnose`.
- Do not invent URLs, versions or hashes: every one is read from the live source and recorded with how it was obtained.
- Python commands are run with `uv run`; the repo's checks (`uv run pytest tests/ glossary/tests/ -q`, `uv run python -m glossary check`, `uv run python scripts/check_construction.py --check`) must stay clean at every merge.

## Review Focus

1. A clean runner has no `~/Documents/GitHub/...` and no `/opt/homebrew/...`: every notebook cell that names one must be found, not only the ones already known (Ch5-03 cell 16, Ch8-02 cells 11/13/15, Ch10-01 cells 25/46/48, `exercises/ch08`).
2. A figure cell with empty stored output silently produces nothing if the site is built without executing; the site-level figure count is the check, not "build exited 0".
3. The release binary may differ from Z's local build (`0.9.1-1-gaf839f0`), changing verdict strings that chapter prose quotes; equivalence must be measured, not assumed.
4. `BASE_URL=/toaster` changes every asset and internal link; absolute `/...` links and local `../../docs/glossary.md#...` links must be checked on the built site.
5. The first Pages deploy exposes everything in the build to the public: a scan of the built HTML for local paths, usernames and internal-only text is a release check.

---

## Task 1: Clean-checkout dry run on Z's machine (PA-1)

**Files:** Create `decisions/pages-publishing/a1-clean-checkout.md` (findings). Scratch outside the repo.

**Interfaces:** Produces the failure list for tasks that follow; consumes nothing.

```
CONTRACT PA-1 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          ready
Task:           Reproduce, as closely as possible on this Mac, what a contributor or CI sees on a clean
                machine, and record exactly what breaks. Do not fix anything.
Context:        docs/superpowers/specs/2026-10-03-pages-publishing-design.md; docs/setup.md; ci.yml;
                scripts/check-tools.py; src/toaster/bootstrap.py.
Non-goals:      No edits to any tracked file except the findings file. No downloads into the repo.
Blast zone:     decisions/pages-publishing/a1-clean-checkout.md -- on branch pub/a1 in worktree
                .claude/worktrees/pub-a1. All experiments run in a scratch dir from `mktemp -d`.
Acceptance:     The findings file contains, from one real run of this sequence:
                  T=$(mktemp -d); git clone --no-local /Users/z/Documents/GitHub/toaster $T/repo
                  mkdir $T/home; cd $T/repo
                  env HOME=$T/home uv sync --locked
                  env HOME=$T/home uv run python scripts/check-tools.py
                  npm ci
                  env HOME=$T/home BASE_URL=/toaster npx myst build --html --execute 2>&1 | tee $T/build.log
                (verify the flags with `npx myst build --help` first; if `--html --execute` is not valid,
                use the documented equivalent and say so). Report: (a) wall time of each step; (b) every
                notebook that fails and the first error line of each failing cell, with notebook path and
                cell id; (c) the count of warnings by type; (d) from the built `_build/html`: number of
                <img> or inline <svg> figures per page for pages that have figure cells, total figures, and
                any page whose figure cell produced no figure; (e) `grep -rIl` of the built tree for
                "/Users/", "/opt/homebrew", "Documents/GitHub" (list files and counts); (f) a link check of
                internal links under BASE_URL=/toaster (use a small script; list broken ones). Also run
                the same build once more with HOME unset to the real home and PATH containing the toolkit
                (i.e. Z's normal environment) to confirm the baseline builds cleanly, so failures are
                attributable to the clean environment. Commands and outputs quoted, not summarized.
Premises:       The hard-coded paths named in the spec (verify each by grep before the run and list every
                occurrence of Path.home(), "/opt/homebrew" and "Documents/GitHub" in chapters/ and
                exercises/ with notebook, cell id and line).
Questions to:   the orchestrator
Report:         branch and commit, model run on, the findings file path, every flagged-not-fixed item.
```

- [ ] **Step 1:** Orchestrator creates worktree: `git worktree add .claude/worktrees/pub-a1 -b pub/a1 main`; writes the contract above to `CONTRACT.md` in it.
- [ ] **Step 2:** Dispatch builder; wait for report.
- [ ] **Step 3:** Dispatch reviewer (different model): re-run the grep inventory and the step-(d) figure count from the findings' own commands on a fresh scratch checkout, and confirm at least three failing cells reproduce.
- [ ] **Step 4:** Merge on PASS; remove worktree and branch.

## Task 2: Real-runner diagnostic workflow (PA-2)

**Files:** Create `.github/workflows/pages-diagnose.yml` on branch `pub/diagnose` only (never merged to main).

**Interfaces:** Produces the authoritative result for ubuntu-latest; consumes nothing from Task 1 (runs in parallel).

```
CONTRACT PA-2 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          ready
Task:           Write a throwaway GitHub Actions workflow that builds the UNMODIFIED book on a clean
                ubuntu-latest runner, so the real failures are measured before any fix. To let unmodified
                notebooks find their hard-coded paths, the workflow creates those exact paths as symlinks
                to freshly provisioned tools (this is deliberate and only for diagnosis).
Context:        Spec "Context" items 3 and 4; Ch5-03 cell 16, Ch8-02 cells 11/13/15, Ch10-01 cells
                25/46/48 for the exact paths. sysml-toolkit release v0.9.1 asset
                sysmlv2-0.9.1-x86_64-unknown-linux-gnu.tar.gz and its SHA256SUMS
                (https://github.com/Open-MBEE/sysml-toolkit/releases/tag/v0.9.1). Library:
                https://github.com/Systems-Modeling/SysML-v2-Release at commit
                de1070ae8e79c21532b8004fc663d47b35d0e9fa, directory sysml.library. Existing steps to copy:
                .github/workflows/ci.yml (uv 0.5.x, setup-node with .nvmrc, npm ci, graphviz).
Non-goals:      Do not edit ci.yml or any other file. Do not add deploy steps. Do not put secrets or tokens
                in the file.
Blast zone:     .github/workflows/pages-diagnose.yml -- on branch pub/diagnose in worktree
                .claude/worktrees/pub-diagnose.
Acceptance:     The workflow has triggers `workflow_dispatch` and `push` limited to branch pub/diagnose.
                Steps, in order: checkout; astral-sh/setup-uv; actions/setup-node (node-version-file
                .nvmrc); `uv sync --locked`; `npm ci`; `sudo apt-get update && sudo apt-get install -y
                graphviz openjdk-17-jre-headless plantuml`; download the v0.9.1 linux toolkit asset and
                SHA256SUMS with curl, verify with `sha256sum -c` (fail the step on mismatch), extract the
                `sysmlv2` executable; sparse-clone SysML-v2-Release and `git checkout` the pinned commit;
                create these paths with `sudo mkdir -p` and `ln -sf` so unmodified notebooks work:
                $HOME/Documents/GitHub/sysml-toolkit/target/release/sysmlv2,
                $HOME/Documents/GitHub/sysml-toolkit/spec-refs/SysML-v2-Release/sysml.library,
                /opt/homebrew/opt/plantuml/libexec/plantuml.jar (point at the apt plantuml jar: find it
                with `dpkg -L plantuml | grep '\.jar$'`), and
                /opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home/bin/java (point at the real
                java); `uv run python scripts/check-tools.py`; `BASE_URL=/toaster npx myst build --html
                --execute 2>&1 | tee build.log` with `continue-on-error: true`; a final step that writes
                to $GITHUB_STEP_SUMMARY the failing notebook/cell lines (grep the log) and the built
                figure count (count <img and inline <svg in _build/html pages), and uploads build.log and
                `_build/html` with actions/upload-artifact (retention 7 days). The file passes
                `uvx actionlint` (or `pip install actionlint-py` equivalent) with no errors; paste the
                output. No action is referenced without a pinned major version tag.
Premises:       The dpkg jar path and the asset names above exist (check with `gh release view v0.9.1
                --repo Open-MBEE/sysml-toolkit --json assets` and record the sha256 line you rely on).
Questions to:   the orchestrator
Report:         branch and commit, model run on, actionlint output, the sha256 of the linux asset taken
                from SHA256SUMS, anything flagged and not fixed.
```

- [ ] **Step 1:** Orchestrator creates worktree `git worktree add .claude/worktrees/pub-diagnose -b pub/diagnose main`; writes contract; dispatches builder; dispatches reviewer to run actionlint and re-verify the sha256 line against the release.
- [ ] **Step 2 (orchestrator, needs Z's go-ahead because it pushes a branch and consumes Actions minutes):** push `pub/diagnose`; `gh workflow run pages-diagnose.yml --ref pub/diagnose`; wait with `gh run watch`; download the artifact and `gh run view --log` into `decisions/pages-publishing/a2-real-runner.md` with the step summary pasted verbatim.
- [ ] **Step 3:** Delete the remote branch `pub/diagnose` after the findings are committed to main; the workflow file is not merged.

## Task 3: Release-binary output equivalence (PA-3)

**Files:** Create `decisions/pages-publishing/a3-output-equivalence.md`. Scratch outside the repo.

**Interfaces:** Produces the pin decision input (which toolkit version CI downloads) for Phase B.

```
CONTRACT PA-3 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          ready
Task:           Measure whether the toolkit's published v0.9.1 release binary reproduces the stored
                outputs of the toolkit-dependent notebooks that Z's locally built `sysmlv2 0.9.1`
                produced, so the book's quoted verdicts stay true when CI uses the release binary.
Context:        Notebooks and cells: chapters/ch05-architecture/03-interfaces.ipynb (cell 16, the
                interconnection figure), chapters/ch08-checking/01-assert-constraint-def.ipynb,
                02-violation-witness.ipynb, 03-revision-flow.ipynb, chapters/ch10-traceability-signoff/
                01-traceability-graph.ipynb (cells 25, 46, 48). src/toaster/modelcheck.py;
                src/toaster/render.py (render_toolkit_interconnection). Release assets:
                https://github.com/Open-MBEE/sysml-toolkit/releases/tag/v0.9.1.
Non-goals:      Do not edit any tracked notebook or source file; run throwaway copies only. Do not
                replace Z's ~/Documents/GitHub/sysml-toolkit build.
Blast zone:     decisions/pages-publishing/a3-output-equivalence.md -- on branch pub/a3 in worktree
                .claude/worktrees/pub-a3. Scratch dir via mktemp -d.
Acceptance:     In scratch: download the macOS asset matching this machine (`uname -m`: arm64 means
                aarch64-apple-darwin) plus SHA256SUMS; verify with shasum -a 256 -c; extract. Check out
                SysML-v2-Release at de1070ae8e79c21532b8004fc663d47b35d0e9fa (sparse or shallow fetch of
                that commit). Make a scratch HOME in which the notebooks' hard-coded toolkit paths
                resolve to the release binary and that library (symlinks), and run copies of the five
                notebooks above with nbclient (or `jupyter nbconvert --execute --output-dir <scratch>`)
                under that HOME. Then, cell by cell, compare each executed copy's code-cell outputs with
                the tracked notebook's stored outputs. Report: per notebook, the number of cells whose
                outputs differ, and for each differing cell the stored versus fresh text (quoted). Classify
                each difference: cosmetic (whitespace, ordering, timing), verdict-changing (a verdict
                string, count, status or proof result differs), or figure (compare the two SVGs by parsing
                their node and edge labels, not bytes). State plainly whether v0.9.1 release is
                equivalent for every claim chapter prose makes about these outputs (cite the prose
                sentence when a difference touches one). Also run `sysmlv2 --version` for both binaries.
Premises:       The five notebooks execute successfully with Z's local build first (run one baseline copy
                and confirm zero error cells before comparing), so differences are attributable to the
                binary.
Questions to:   the orchestrator
Report:         branch and commit, model run on, findings path, the asset name and sha256 used, every
                verdict-changing difference, anything flagged and not fixed.
```

- [ ] **Step 1:** Create worktree `pub-a3` (branch `pub/a3`), write contract, dispatch builder, dispatch reviewer (re-run one notebook's comparison independently and re-verify the sha256), merge on PASS.

## Task 4: Dangling-reference inventory (PA-4)

**Files:** Create `decisions/pages-publishing/a4-dangling-references.md`.

**Interfaces:** Produces the table that Phase B's reference-cleanup contract edits from.

```
CONTRACT PA-4 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort low
Reviewer:       reviewer, model claude-opus-5-5
State:          ready
Task:           List every place the published site shows a reference to something that will not exist
                on the site, and propose the fix for each. Read-only survey.
Context:        The published page set is myst.yml's toc: docs/index, setup, reproducibility, glossary,
                references, contributor, docs/case-studies/2026-09-30-energy-conservation-requirement-tie,
                and every chapter index/notebook/conclusion. Internal artifacts that will not exist on
                the site: DEFERRED.md entries (D-001..D-0nn), decisions/log.md entries (DL-nnn),
                decisions/*.md, AGENTS.md, CLAUDE.md, .claude/ (skills, agents), standing-assumption
                tags (SA-n), work-contract ids, toaster#n / OpenSysML#n issue numbers (these resolve on
                GitHub and are acceptable if written as links), repo-relative paths.
Non-goals:      Edit nothing but the findings file. Do not judge whether the content is correct.
Blast zone:     decisions/pages-publishing/a4-dangling-references.md -- on branch pub/a4 in worktree
                .claude/worktrees/pub-a4.
Acceptance:     Scan, with a script committed into the findings file as a code block, ALL text a reader
                sees: markdown cells, index.md and conclusion.md, docs pages in the toc, code comments and
                string literals in code cells (readers see source), and stored output text. A table with
                one row per occurrence: file | cell id or line | exact quoted sentence | internal artifact
                | class | proposed fix. Classes: LINK (the reader benefits from the full text; propose the
                exact github.com/Open-MBEE/toaster/blob/main/<path> URL and verify the path exists at
                main), REWORD (process jargon; propose replacement wording that keeps the sentence's
                meaning and stands alone), KEEP (intentional, e.g. docs/contributor.md describing how the
                project works; say why). A count by class and by artifact type. Verify each LINK path
                exists with `test -e` and each issue number resolves with `gh issue view`. List the
                items where the class is ambiguous for Z (Spec Q2).
Premises:       The earlier scan found these artifact types in learner content: SA-7, DL-070/071/072,
                D-001/023/025/026/028/029/030/031/033, DEFERRED.md, AGENTS.md, decisions/ paths, "skill",
                ".claude/", "orchestrator"; confirm and extend, do not assume the list is complete.
Questions to:   the orchestrator
Report:         branch and commit, model run on, findings path, counts, ambiguous items.
```

- [ ] **Step 1:** Create worktree `pub-a4` (branch `pub/a4`), write contract, dispatch builder, dispatch reviewer (independently re-scan one chapter and one docs page and compare to the table), merge on PASS.

## Task 5: Survey compilation and Phase B specification (orchestrator)

**Files:** Create `decisions/pages-publishing-survey.md`; later `docs/superpowers/plans/2026-10-03-pages-publishing-phase-b-plan.md`.

- [ ] **Step 1:** Compile A1-A4 into the survey: per question, evidence and file reference; the failure list from the real runner; the pin recommendation (toolkit version and asset sha256, library commit); equivalence verdict; reference table with counts; list of decisions for Z/ACE.
- [ ] **Step 2:** Route judgment items to the ACE (reference policy, whether any verdict-changing difference changes chapter prose); ask Z the spec's open questions that Phase A did not settle.
- [ ] **Step 3:** Write the Phase B plan as full contracts (no placeholders), using the survey's exact paths, hashes and cell ids; log a DL entry; ask Z to review before Phase B starts.

---

## Phase B outline (to be written as full contracts after the survey; the shape is fixed now so the dependencies are visible)

| Contract | Deliverable | Depends on | Blast zone (intended) |
|---|---|---|---|
| PUB-1 | `src/toaster/tools.py`: `resolve_sysmlv2()`, `resolve_library()`, `resolve_plantuml_jar()`, `resolve_java()` from env (`SYSMLV2_BINARY`, `SYSMLV2_LIB_DIR`, `PLANTUML_JAR`, `JAVA`), then PATH and platform locations, raising an error that names the variable and the provisioning command; unit tests with tmp paths | survey (A1, A2) | `src/toaster/tools.py`, `tests/test_tools.py` |
| PUB-2 | Replace every hard-coded path in the notebooks with PUB-1 calls (cells from A1's list); a test that fails if any notebook contains `Path.home()`, `/opt/homebrew` or `Documents/GitHub`; stored outputs unchanged | PUB-1 | the listed notebook cells, `tests/test_no_local_paths.py` |
| PUB-3 | Provisioning: `scripts/provision-toolkit.py` (or extension of `toaster.bootstrap`) downloads the pinned toolkit release asset for the platform, verifies the pinned sha256, fetches the pinned `sysml.library` commit, and prints the env exports; `check-tools.py` calls it; pins recorded in one file | PUB-1, A3 | `scripts/`, `src/toaster/bootstrap.py`, a pins file, tests |
| PUB-4 | CI: `ci.yml` build job executes the book (`BASE_URL=/toaster myst build --html --execute`), installs graphviz/java/plantuml, runs PUB-3; deploy job on `main` only with `upload-pages-artifact` and `deploy-pages`, `pages: write`, `id-token: write`, concurrency group; PRs build without deploying; built-site checks (figure count, no local paths, internal links) as a script run in CI | PUB-2, PUB-3, A2 | `.github/workflows/ci.yml`, `scripts/check-site.py` |
| PUB-5 | Dangling-reference edits from A4's table (LINK and REWORD rows), minimal diffs, outputs untouched | A4, Z/ACE policy | listed pages and notebook cells |
| PUB-6 | Docs: `docs/setup.md` and `README.md` publishing section (how the site builds, the env vars, how to preview with `BASE_URL`), `DEFERRED.md` entry recording the toolkit dependency of Ch5/8/10, DL entries | PUB-4 | `docs/setup.md`, `README.md`, `DEFERRED.md`, `decisions/log.md` |
| PUB-7 | First deploy: Z enables Pages (Settings, Pages, Source: GitHub Actions); orchestrator merges the PR, watches the deploy run, then runs the built-site checks against the live URL | PUB-4..6, Z | none (verification) |

Merge order: PUB-1, then PUB-2 and PUB-3 in parallel, then PUB-4, PUB-5 in parallel with PUB-4, then PUB-6, then PUB-7.
