# Pages publishing: Phase A survey

**Date:** 2026-10-03
**Inputs:** `decisions/pages-publishing/a1-clean-checkout.md` (PA-1), `a3-output-equivalence.md` (PA-3),
`a4-dangling-references.md` (PA-4); PA-2 (real `ubuntu-latest` run) is **pending**: the workflow is final on
branch `pub/diagnose` (local commit `7498a97`; the remote has an older version) and has not been run.
Every finding below was reproduced by an independent reviewer on a different model, except where noted.

## 1. What breaks on a clean machine (PA-1)

| # | Finding | Evidence |
|---|---|---|
| F1 | **No notebook executes unless the project venv is first on PATH.** MyST starts the first `jupyter` on PATH (here Anaconda's, broken). `docs/setup.md` says only `npx mystmd start --execute`. With the literal sequence: 32 errors, 1 figure. | PA-1 literal run; reviewer reproduced (rc=0 despite 32 errors). |
| F2 | **`myst build` exits 0 with notebook errors;** only `--strict` exits 1. A CI job without `--strict` cannot fail. | rc=0 / rc=1 measured by builder and reviewer. |
| F3 | With venv on PATH and a clean HOME, **exactly 3 notebooks fail**, all on missing toolkit paths: Ch5-03 cell-16 (`sysmlv2 binary not found`), Ch8-02 cell-11 (same), Ch10-01 cell `4d859570` (`FileNotFoundError ... sysml.library/Systems Library/Requirements.sysml`). Allowing errors to continue shows 11 failing cells (cascading NameErrors in Ch8-02 and Ch10-01). | Both reproduced exactly. |
| F4 | **Figures are not in the page DOM.** SVG figures live in the page JSON and are drawn client-side. Count `image/*` outputs in `_build/site/content/*.json`: 17 in the clean build (Ch5-03 missing), 18 in a fully working build. | Reviewer re-derived 17 and 18. |
| F5 | **The built site leaks local paths:** `Documents/GitHub` in 12 files (68 occurrences), `/opt/homebrew` in 6 files, plus the build host's home directory in failed-cell tracebacks (reviewer: 6 files). `/Users/` appears nowhere. The paths come from notebook source, so they publish even when execution succeeds. | Both reproduced counts. |
| F6 | **Files are published that should not be:** MyST copies any linked non-page file into `/build/`. Exercises ch01-ch08 (8 of 10 notebooks) and `DEFERRED.md` are published as raw downloads because chapter pages link to them; ch08's exercise and `DEFERRED.md` carry the author's `Documents/GitHub` path. `project.exclude: exercises/**` only stops them being parsed as pages. | Reviewer md5-matched the 8 exercises. |
| F7 | Internal links under `BASE_URL=/toaster`: 2305 checked, 0 broken (a wrong-base control reports thousands broken, so the check can fail). | Both. |
| F8 | Tooling drift and unpinned inputs: MyST downloads the book theme from `refs/heads/main.zip` (unpinned) at build time; `ci.yml` pins uv `0.5.x` but this machine ran 0.9.18 and Python 3.14.7; node here is 23.7 vs `.nvmrc` 22; `scripts/check-tools.py` checks only Graphviz and downloads OpenSysML (nothing about `sysmlv2`, Java, PlantUML). | PA-1 observations. |
| F9 | Hard-coded local paths also exist in `tests/` (`test_render_toolkit_interconnection.py`, `test_modelcheck.py`, `test_ch08_conservation_property.py`), `scripts/diagram_study/provision_check.py`, `exercises/ch08` cell-09, and `src/toaster/bootstrap.py` (cache dir, benign). | Reviewer re-grepped. |

Notebook cells that name a local path (the full list for the fix): Ch5-03 cell-16 (`Path.home()` x2, `/opt/homebrew` plantuml jar and java), Ch8-02 cell-11, Ch10-01 `4d859570` (index 25) and `3850dee3` (index 46), `exercises/ch08` cell-09. The plan's "Ch8-02 cells 11/13/15, Ch10-01 cells 25/46/48" is the list of *failing* cells; cells 13, 15 and 48 use variables set earlier.

## 2. Toolchain provisioning facts (PA-2 prep, PA-3)

- sysml-toolkit v0.9.1 release assets: `sysmlv2-0.9.1-x86_64-unknown-linux-gnu.tar.gz` sha256
  `76b4a1e4f159bdf72bde8857bf25e60f59b4ffe4c7c48eeb8c419d856f4ff570` (from the release `SHA256SUMS`);
  `sysmlv2-0.9.1-aarch64-apple-darwin.tar.gz` sha256 `ad0204041c95ce9817d398420e5057132a1378d53a812172cbd207cc40100c4a`.
  Tarball layout `sysmlv2-0.9.1-<target>/{sysmlv2,README.md,LICENSE}`. The Linux binary links only libc, libm, libgcc_s (no Z3 library needed).
- `sysml.library`: `Systems-Modeling/SysML-v2-Release` commit `de1070ae8e79c21532b8004fc663d47b35d0e9fa`, top-level `sysml.library`; the sparse-clone commands in the workflow were run by a reviewer and fetch it (117 files, 1.4 MB `.git`).
- PlantUML: Ubuntu's apt `plantuml` (1.2020.2) **rejects** the committed `figures/ch05-interconnection.puml` (a `port` inside a `rectangle`); the upstream jar `plantuml-1.2026.8.jar` (sha256 `5e1ecfa8ecd32c90b03bbf3b1eb6f020943f98ab0fcf4032be31a0002ee2c462`, matching GitHub's published digest) renders it. apt `plantuml` pulls Java 21, not 17.
- **Output equivalence (PA-3, macOS arm64 only):** the release v0.9.1 binary reproduces every output of Ch5-03, Ch8-01/02/03 and Ch10-01 (cells 25, 46, 48) versus both Z's local build (`0.9.1-1-gaf839f0`) and the stored outputs: zero verdict-changing differences, Ch5 figure byte-identical, same Z3 witness. Cosmetic only: stdout stream chunk boundaries vary run to run, so any CI comparison of raw outputs must join adjacent same-stream chunks first. **Not measured: Linux** (Z3 witness values and PlantUML/Graphviz versions could differ); that is PA-2's job.

## 3. Dangling references (PA-4)

365 rows across 58 of 59 pages: LINK 164, REWORD 58, KEEP 143. By cause:
- 55 `exercises/` references (excluded from the site; the markdown-linked ones currently publish as raw downloads). Fix: link to GitHub, which also stops publishing `exercises/ch08` and `DEFERRED.md`.
- 43 `models/` and 34 `DEFERRED.md` entry references, 9 issue numbers, 23 bare repo file names: mostly LINK to `https://github.com/Open-MBEE/toaster/blob/main/<path>` (42 distinct paths, all verified to exist on `main`; DEFERRED anchors verified against GitHub's slug rule).
- Process jargon, `AGENTS.md`/`.claude/`/`decisions/`/`SA-n`/`DL-nnn`/work-contract ids/commit hashes: REWORD (58) or KEEP where the page is about the project (contributor guide).
- Reclassification rules the orchestrator set: `models/` paths on executable lines and D-nnn ids inside SysML doc comments and `ReviewRecord` strings are KEEP (editing them would change `models/*.sysml`, AS-C08's `content_hash`, and persisted records; AS-C08.json would go stale until ch08 nb02 is re-run); add links in adjacent markdown instead.

## 4. Decisions needed (Z, or the ACE where it is judgment)

1. **A1** `docs/contributor.md` names harness files (`AGENTS.md`, `CLAUDE.md`, `.claude/`, `decisions/`): default KEEP with links on first mention.
2. **A2/A4** pages that cite `AGENTS.md` and `decisions/log.md` DL entries as sources of substantive text (references.md, the case study, one Ch10 quoted sentence): default LINK to GitHub; DL-nnn in chapter text REWORD.
3. **A3** the handle "Z" and process narration ("this session", "unmerged worktree") in the case study: **ruled by mzargham (DL-112)**: keep "Z", but make the identity explicit. "Z" means the contributor identity `mzargham` (Michael Zargham, GitHub `mzargham`); public pages name `mzargham` ("mzargham (Z)") at first mention instead of a bare "Z", the identity is recorded in `AGENTS.md` Part 1 and `docs/contributor.md`, and any later contributor is named by their own handle ("Z" never changes meaning). The case study stays a record of the episode; "approved by Z" in references.md becomes "approved by mzargham (Z)".
4. **A7** whether the D-nnn-in-record-strings default (leave unchanged, link adjacent) also covers the other record strings that name internal files (`AGENTS.md SS1`, the ch04 `index.md` string, case-study path strings): ACE to rule.
5. **A10** `reproducibility.md` cites `decisions/pass4-run-*.md` (a glob): default link the `decisions/` directory; alternative drop the pointer.
6. The published `docs/setup.md`, `docs/contributor.md` and `docs/reproducibility.md` currently say deployment is off; they must change when the site is published.
7. Which exercises, if any, should be published (default: none; link to GitHub).
8. Spec Q1 (CI time): measured build time 46 s with all notebooks executed on this Mac; the full runner time is the PA-2 result.

## 5. Consequences for Phase B

- PUB-1/PUB-2/PUB-3 stand as outlined (tool resolver reading `SYSMLV2_BINARY`, `SYSMLV2_LIB_DIR`, `PLANTUML_JAR`, `JAVA`; remove the hard-coded paths in the cells above and `exercises/ch08`; provision the pinned toolkit, library and PlantUML jar). Add `tests/` and `scripts/diagram_study/` to the path-removal scope (F9).
- PUB-4 (CI) changes: build with `uv run --frozen npx myst build --html --execute --strict` (F1, F2); the figure check counts `image/*` outputs in `_build/site/content/*.json` against a recorded baseline (not DOM images), plus a zero-error check (a notebook that halts after a figure still shows its figure); the leak scan must cover `$HOME`/`/home/runner`/`/opt/homebrew`/`Documents/GitHub`/`/Users/`; pin uv, Python and the Node version in CI; decide whether to pin the MyST book theme (F8).
- New contract: retarget links to `exercises/` and `DEFERRED.md` to GitHub (F6) and document `uv run` for local preview in `docs/setup.md` (F1).
- PUB-5 edits are driven by the 365-row table, minimal diffs, no model or persisted-record changes (section 3).
- Phase B waits for: the PA-2 Linux run (confirms Linux Z3 witness and PlantUML results, runner time), and the decisions above.
