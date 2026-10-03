# A1: clean-checkout reproduction of the Pages build

Contract PA-1, 2026-10-03. Builder: claude-sonnet-5-5. Investigation only: nothing was fixed.
Every number below comes from a real run on this Mac (Darwin 25.5.0, arm64) on 2026-10-03; scratch dirs were `mktemp -d`
directories (volatile; paths shown as `$T...`). No tracked file was edited. Downloads went to the scratch dirs only.

## 0. What "clean" can and cannot mean on this machine (fidelity limits)

- macOS, not `ubuntu-latest`. The absolute paths `/opt/homebrew/opt/plantuml/...` and `/opt/homebrew/opt/openjdk/...`
  exist on this Mac, so a clean `HOME` hides them. They would fail on a Linux runner; that is not observable here.
- `HOME=$T/home` was applied to `uv sync`, `check-tools.py` and the MyST build, exactly as the contract says. `npm ci`
  ran with the real `HOME` (the contract's command has no `HOME=` on it), so the npm cache was warm.
- `PATH` was not scrubbed in the literal run (see 2.1): the Mac `PATH` has Homebrew, Anaconda, `dot`, `plantuml`.
- Toolchain seen: uv 0.9.18 (CI pins `0.5.x`), node v23.7.0 (`.nvmrc` says 22), npm 10.9.2, mystmd 1.11.0,
  `uv sync` picked CPython 3.14.7 (`requires-python >= 3.12`), Graphviz 16.0.0.
- The sequence was run on a `git clone --no-local` of `/Users/z/Documents/GitHub/toaster` at `main` = `e6e928b`.

## 1. Premises: hard-coded locations (grep before the run)

Method: JSON-aware scan of every code cell of every `.ipynb` under `chapters/` and `exercises/` for
`Path.home()`, `/opt/homebrew`, `Documents/GitHub` (plus a plain grep of the `.md` files and a check of stored outputs).
Totals: `Path.home()` 9, `/opt/homebrew` 2, `Documents/GitHub` 9 (line-level occurrences). Stored outputs: none.
Markdown files under `chapters/`, `exercises/`: none.

| notebook | cell id (index) | line | text |
|---|---|---|---|
| chapters/ch05-architecture/03-interfaces.ipynb | cell-16 (16) | 8 | `BINARY = Path.home() / "Documents/GitHub/sysml-toolkit/target/release/sysmlv2"` |
| same | cell-16 | 9 | `LIB = Path.home() / "Documents/GitHub/sysml-toolkit/spec-refs/SysML-v2-Release/sysml.library"` |
| same | cell-16 | 10 | `PLANTUML_JAR = Path("/opt/homebrew/opt/plantuml/libexec/plantuml.jar")` |
| same | cell-16 | 11 | `JAVA = Path("/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home/bin/java")` |
| chapters/ch08-checking/02-violation-witness.ipynb | cell-11 (11) | 4 | `BINARY = Path.home() / "Documents/GitHub/sysml-toolkit/target/release/sysmlv2"` |
| same | cell-11 | 5 | `LIB = Path.home() / "Documents/GitHub/sysml-toolkit/spec-refs/SysML-v2-Release/sysml.library"` |
| chapters/ch10-traceability-signoff/01-traceability-graph.ipynb | 4d859570 (25) | 2 | `Path.home() / "Documents/GitHub/sysml-toolkit/spec-refs/SysML-v2-Release/sysml.library"` |
| same | 3850dee3 (46) | 9 | `SYSMLV2_BINARY = Path.home() / "Documents/GitHub/sysml-toolkit/target/release/sysmlv2"` |
| same | 3850dee3 | 10 | `SYSMLV2_LIB = Path.home() / "Documents/GitHub/sysml-toolkit/spec-refs/SysML-v2-Release/sysml.library"` |
| exercises/ch08/exercise.ipynb | cell-09 (9) | 4 | `BINARY = Path.home() / "Documents/GitHub/sysml-toolkit/target/release/sysmlv2"` |
| same | cell-09 | 5 | `LIB = Path.home() / "Documents/GitHub/sysml-toolkit/spec-refs/SysML-v2-Release/sysml.library"` |

(Each `Path.home()` line is also a `Documents/GitHub` line, hence 9 + 2 = 11 rows, 9 distinct `Path.home()` lines.)

Premise discrepancies against the plan/spec text:
- The plan lists "Ch8-02 cells 11/13/15" and "Ch10-01 cells 25/46/48". Those are cells that FAIL on a clean machine.
  Only Ch8-02 `cell-11` and Ch10-01 `4d859570` / `3850dee3` NAME a path. Ch8-02 `cell-13`/`cell-15` and Ch10-01
  `9cc5f8de` (index 48) use the variables `BINARY`/`SYSMLV2_BINARY` set earlier, so a grep for the three strings
  does not find them. A fix keyed on the grep list alone misses nothing today, but the failing set is larger than the naming set.
- Outside `chapters/` and `exercises/` (flagged, not fixed): `tests/test_render_toolkit_interconnection.py`,
  `tests/test_modelcheck.py`, `tests/test_ch08_conservation_property.py` hard-code the same `Path.home()` /
  `/opt/homebrew` locations; `scripts/diagram_study/provision_check.py:53` hard-codes `~/Documents/GitHub/sysml-toolkit`;
  `src/toaster/bootstrap.py:50` uses `Path.home() / ".opensysml" / "bin"` (legitimate cache, but it is why `HOME` matters).
- `scripts/check-tools.py` verifies only Graphviz `dot` and downloads the OpenSysML binaries. It checks nothing about
  `sysmlv2`, its library, Java or PlantUML, so a green `check-tools` says nothing about the notebooks that need them.

## 2. The contract sequence, run once, verbatim

### 2.1 Flag check

```
$ npx myst build --help          (excerpt)
  --execute               Execute Notebooks (default: false)
  --html                  Build static HTML site content (default: false)
  --strict                Summarize build warnings and exit non-zero on any errors. (default: false)
```
`--html --execute` is valid as written. No equivalent substitution was needed.

### 2.2 Commands and per-step wall time (a)

```
T=$(mktemp -d); git clone --no-local /Users/z/Documents/GitHub/toaster $T/repo     # clone        1 s
mkdir $T/home; cd $T/repo
env HOME=$T/home uv sync --locked                                                   # uv-sync      5 s  (rc 0)
env HOME=$T/home uv run python scripts/check-tools.py                               # check-tools  7 s  (rc 0)
npm ci                                                                              # npm-ci       1 s  (rc 0)
env HOME=$T/home BASE_URL=/toaster npx myst build --html --execute 2>&1 | tee $T/build.log   # build  15 s ("Built 59 pages ... in 6.3 s")
```
Outputs (quoted):
```
Using CPython 3.14.7 interpreter at: /opt/homebrew/opt/python@3.14/bin/python3.14
Creating virtual environment at: .venv
Resolved 143 packages in 1ms
Prepared 141 packages in 3.44s
Installed 141 packages in 426ms
---
dot: dot - graphviz version 16.0.0 (20260814.1018)
All tools verified.
---
added 1 package, and audited 2 packages in 625ms
found 0 vulnerabilities
```
The pipeline's exit status is `tee`'s (0), not MyST's. MyST itself, run without `tee` on a build that has errors:
`npx myst build --html --execute` exits 0; with `--strict` it exits 1 ("Site has 3 errors and 39 warnings, stopping build.").
So the contract's command (and any CI step written the same way) cannot fail the job on a notebook error.

### 2.3 RESULT OF THE LITERAL RUN: nothing executes (finding F1, blocking)

The literal sequence never puts the project virtualenv on `PATH`. MyST starts a Jupyter server with whatever
`jupyter` is first on `PATH`, and the notebooks' kernelspec is the generic `python3` (all 42 notebooks:
`"kernelspec": {"name": "python3"}`). Result:
```
🚀 Starting new Jupyter server
🪐 Jupyter server did not start
Unable to instantiate connection to Jupyter Server
⛔️ chapters/ch04-functional-decomp/02-heating-refinement.ipynb Could not load Jupyter session manager to run executable nodes
... (32 such lines, one per executable notebook)
```
On this Mac the first `jupyter` is Anaconda's, which is broken (`jupyter lab --version` ends in
`ImportError: cannot import name 'run_sync_in_worker_thread' from 'anyio'`). A run with every directory that
contains a `jupyter` removed from `PATH` (variant A2) fails the same way, with the clearer text
`Unable to instantiate connection to Jupyter Server Error: not found: python`.
Warning/error counts for this run: 32 errors, 98 warnings (breakdown in 2.5). Figures in the built site: 1 (see 2.6).

`docs/setup.md` documents `npm install` then `npx mystmd start --execute` with no mention of activating `.venv` or
using `uv run`. A contributor following it on a clean machine meets this failure.
CI has the same gap: the step list in `ci.yml` has no MyST step yet, and a naive `npx myst build --html --execute`
after `uv sync` has no `jupyter` on `PATH`.

## 3. Variant B: the same sequence with `.venv/bin` first on `PATH` (the realistic CI shape)

Same clean `HOME`, same clone method, one change: `PATH=$T/repo/.venv/bin:$PATH` for the MyST step.
Timing: clone 1 s, uv-sync 4 s, check-tools 8 s, npm-ci 0 s, build 46 s ("Built 59 pages for project in 38 s").
The Jupyter server starts (`🪐 Jupyter server started`), 32 notebooks execute, 59 pages are built.

### 3.1 (b) Failing notebooks and the first error line of each failing cell

As built by MyST (it halts a notebook at its first error, so only one cell per notebook is visible):

| notebook | cell id | first error line |
|---|---|---|
| chapters/ch05-architecture/03-interfaces.ipynb | cell-16 | `AssertionError: sysmlv2 binary not found at $T/home/Documents/GitHub/sysml-toolkit/target/release/sysmlv2 (see work contract CH05-TOOLKIT-VIZ)` |
| chapters/ch08-checking/02-violation-witness.ipynb | cell-11 | `AssertionError: sysmlv2 binary not found at $T/home/Documents/GitHub/sysml-toolkit/target/release/sysmlv2 (see work contract PASS4-008)` |
| chapters/ch10-traceability-signoff/01-traceability-graph.ipynb | 4d859570 | `FileNotFoundError: [Errno 2] No such file or directory: '$T/home/Documents/GitHub/sysml-toolkit/spec-refs/SysML-v2-Release/sysml.library/Systems Library/Requirements.sysml'` |

MyST also printed `Kernel "python3" did not become ready (attempt 1/3); restarting it` once during this run.
Of the 32 chapter notebooks, 29 execute with no error; 3 fail. (The other 10 `.ipynb` files are exercises, excluded from the book.)

Complete failing-cell list, found by executing every notebook with `nbclient` (`allow_errors=True`, clean `HOME`,
`.venv/bin` first) in the same clone, because MyST's halt hides later cells. Cells marked (root) fail for the environment
reason; cells marked (cascade) fail only because an earlier cell in the notebook did not define a name:

```
chapters/ch05-architecture/03-interfaces.ipynb
  cell-16  (root)    AssertionError: sysmlv2 binary not found at .../home/Documents/GitHub/sysml-toolkit/target/release/sysmlv2 (see work contract CH05-TOOLKIT-VIZ)
chapters/ch08-checking/02-violation-witness.ipynb
  cell-11  (root)    AssertionError: sysmlv2 binary not found at ... (see work contract PASS4-008)
  cell-13  (cascade) NameError: name '_write_companion' is not defined
  cell-15  (cascade) NameError: name '_write_companion' is not defined
  cell-28  (cascade) NameError: name 'pos_verdict' is not defined
  cell-32  (cascade) NameError: name 'evidence_refs' is not defined
chapters/ch10-traceability-signoff/01-traceability-graph.ipynb
  4d859570 (root)    FileNotFoundError: [Errno 2] No such file or directory: '.../home/Documents/GitHub/sysml-toolkit/spec-refs/SysML-v2-Release/sysml.library/Systems Library/Requirements.sysml'
  3850dee3 (root)    AssertionError: sysmlv2 binary not found at .../target/release/sysmlv2
  9cc5f8de (root)    FileNotFoundError: [Errno 2] No such file or directory: '.../target/release/sysmlv2'
  cc09043c (cascade) NameError: name 'energy_conservation_lines' is not defined
  e14ede2b (cascade) NameError: name 'ac_c10_evidence_refs' is not defined
```
Compare with the plan's "Ch8-02 cells 11/13/15" and "Ch10-01 cells 25/46/48": 13 and 15 are cascade NameErrors, not path failures.

`exercises/` (excluded from the book, so not built by MyST): every exercise notebook except ch01, ch02, ch04 raises errors both
in the clean environment and in Z's environment (they are fill-in-the-blank exercises, e.g. `exercises/ch03` cell-2
`ExecutionError: evaluation failed: unresolved reference: CoffeeDemo::hot`). Total failing cells across chapters + exercises:
63 clean vs 52 baseline (`nbrun_B.log` vs `nbrun_C2.log`). The only clean-attributable differences are the three chapter
notebooks above (11 cells) and `exercises/ch08` `cell-09`, whose error text changes from `ModelCheckError: ... sysmlv2 verify ...`
(baseline: the binary exists, the check itself errors) to `AssertionError: sysmlv2 binary not found ...` (clean).

### 3.2 (c) Warnings by type (identical across all variants except the error line)

```
  59  WARN  myst.yml Extension inferred for table of contents entry   (every toc entry lacks its extension)
  39  WARN  Duplicate identifier in project                           (cell ids "cell-00".."cell-NN", "cell-06b", ... reused across notebooks)
total WARN: 98   total ERROR: 3
```
(`--strict` counts "3 errors and 39 warnings"; the 59 toc warnings are printed earlier and are not in that count.)
Literal run: 98 warnings, 32 errors, all `Could not load Jupyter session manager to run executable nodes`.
Errors in variant B: 3, all `An exception occurred during code execution, halting further execution`.

### 3.3 (d) Figures in the built `_build/html`

Figure cells in the source (code cells that end in `SVG(...)` or `plt`, counted from the notebooks): 18, on 15 pages.
Static facts about the built HTML: SVG figures are NOT in the page DOM. They live in the page's embedded
`window.__remixContext` JSON (`"image/svg+xml":{"content":"<svg ..."`) and the site renders them with JavaScript. A DOM
count of `<img>`/inline `<svg>` in `<main>` therefore finds only the one PNG. Counts below are therefore given three ways.

Per page with a figure, variant B (clean HOME, venv on PATH), `figs.py` output:
```
page                    dom_img dom_svg page_json_image_outputs html_embedded_image_outputs
action-def-ffbd            0       0        1        1
assert-constraint-def      0       0        1        1
completeness-check         0       0        1        1
composition                0       0        1        1
judgment-context           0       0        1        1
judgment-synthesis         0       0        1        1
model-navigation           0       0        1        1
param-sweep                1       0        1        1     (matplotlib PNG, stored output)
part-def                   0       0        1        1
state-traces               0       0        2        2
stopping-judgment          0       0        2        2
subsystem-requirements     0       0        2        2
threshold-judgment         0       0        1        1
traceability-graph         0       0        1        1
TOTAL                      1       0       17       17     (pages=59)
```
Page with a figure cell that produced no figure: `interfaces` (Ch5-03, `cell-16`, fails on the missing `sysmlv2` binary).
So the clean build has 17 figures; the baseline (variant C2) has 18, the same list plus `interfaces`.
`ch10 traceability-graph` shows its figure (cell `47344a8b`) because that cell runs before the failing cell `4d859570`;
cells after the failure never execute, so a notebook can show a partial page without any visible gap.
Literal run (no Jupyter): 1 figure total, the `param-sweep` PNG, which is the only stored output in the repo's chapters.

### 3.4 (e) Published local paths: `grep -rIl` of the built tree

Variant B, `$T/repo/_build/html` (22 + 68 occurrences):
```
== grep -rIl '/Users/' .            (0 files)
== grep -rIl '/opt/homebrew' .      (6 files, 22 occurrences)
build/03-interfaces-<hash>.ipynb
interfaces.json
interfaces/index.html
myst.search.json
traceability-graph.json            (a stored traceback line: /opt/homebrew/Cellar/python@3.14/3.14.7/.../pathlib/__init__.py)
traceability-graph/index.html      (same traceback)
== grep -rIl 'Documents/GitHub' .   (12 files, 68 occurrences)
build/01-traceability-grap-<hash>.ipynb
build/02-violation-witness-<hash>.ipynb
build/03-interfaces-<hash>.ipynb
build/DEFERRED-<hash>.md
build/exercise-<hash>.ipynb          (exercises/ch08/exercise.ipynb, copied into the site because a chapter page links to it)
interfaces.json
interfaces/index.html
myst.search.json
traceability-graph.json
traceability-graph/index.html
violation-witness.json
violation-witness/index.html
```
(In B the "occurrences" are `grep -o` match counts; `grep -c` counts matching lines, which is lower because JSON and HTML
put many matches on one line.) Baseline C2 (Z's environment, no errors): `/Users/` 0 files; `/opt/homebrew` 4 files
(10 occurrences; matching lines per file: `build/03-interfaces.ipynb` 1, `interfaces.json` 1, `interfaces/index.html` 3,
`myst.search.json` 1); `Documents/GitHub` 12 files (38 occurrences; matching lines per file: `build/01-traceability-grap.ipynb` 3,
`build/02-violation-witness.ipynb` 2, `build/03-interfaces.ipynb` 1, `build/DEFERRED.md` 1, `build/exercise.ipynb` 2,
`interfaces.json` 1, `interfaces/index.html` 3, `myst.search.json` 1, `traceability-graph.json` 1,
`traceability-graph/index.html` 4, `violation-witness.json` 1, `violation-witness/index.html` 3).
The literal run (A) shows the same 4 + 12 files.
Takeaways: (1) the paths are published from the notebook SOURCE, whether or not execution succeeds, so replacing them is needed
for the spec's "no built page contains ..." check; (2) the site also publishes `DEFERRED.md` (line 340 names
`~/Documents/GitHub/sysml-toolkit/target/release/sysmlv2`) and `exercises/ch08/exercise.ipynb` as downloadable files
under `/toaster/build/`; (3) failed runs additionally leak interpreter paths (`/opt/homebrew/Cellar/...`) in stored tracebacks;
(4) no `/Users/` string appears anywhere in any variant.

### 3.5 (f) Internal link check under `BASE_URL=/toaster`

Script: `links.py` (HTML parser over all 59 pages; every `<a href>`, `<img src>`, `<script src>`, `<link href>` that is not
external is resolved against `$T/repo/_build/html` after stripping `/toaster`; fragments checked against element ids) and
`jlinks.py` (the 78 content links stored in the page JSON, e.g. `/abstract-def`, `/toaster/build/exercise-<hash>.ipynb`).
```
pages scanned: 59; internal refs checked: 2305; external refs skipped: 481
broken: 0
content links (page JSON) checked: 78 broken: 0
```
Same result for the literal run and for baseline C2. Negative control: running the same script with the base set to `/wrongbase`
reports 2088 broken refs, so the check can fail. Scope note: external links (481) were not fetched.

## 4. Baseline: Z's normal environment (real `HOME`, toolkit on `PATH`)

Run in a fresh clone (never in the main checkout) with `HOME=/Users/z` and `/Users/z/Documents/GitHub/sysml-toolkit/target/release`
appended to `PATH`, same commands and `BASE_URL=/toaster`.
- C1 (PATH literally as in the contract, plus toolkit): clone 1 s, uv-sync 1 s, check-tools 1 s, npm-ci 1 s, build 8 s.
  32 errors, 98 warnings: the same `Could not load Jupyter session manager` failure, 1 figure. So the literal sequence fails in
  Z's own `PATH`, not only in the clean one. Z's normal flow must therefore already have `.venv/bin` first on `PATH` (or use
  `uv run npx ...`); that is not documented anywhere I read.
- C2 (`.venv/bin` first on `PATH`, plus toolkit): clone 2 s, uv-sync 1 s, check-tools 1 s, npm-ci 1 s, build 23 s ("Built 59 pages
  for project in 15 s"). Result: 0 errors, 98 warnings (59 toc + 39 duplicate identifiers), 18 figures, 0 broken links,
  `/Users/` 0 files. This confirms the baseline builds cleanly, so the clean-environment failures in section 3 are attributable to
  `HOME` (Path.home() lookups) and not to the repository state.

## 5. Summary of findings (all unfixed)

1. F1 (blocking): nothing executes unless `jupyter` from the project venv is on `PATH`; `docs/setup.md` and the literal
   sequence do not arrange it. Failure mode on a clean runner: `Could not load Jupyter session manager` x32 (or `not found: python`).
2. F2: `myst build` exits 0 with errors; only `--strict` makes it non-zero. A `| tee` pipe masks even that.
3. F3: three chapter notebooks fail on a machine without `~/Documents/GitHub/sysml-toolkit` (11 cells including cascades):
   Ch5-03 (also needs PlantUML jar + Java at `/opt/homebrew` paths, unobservable here), Ch8-02, Ch10-01. One of 18 figures is lost.
4. F4: 11 literal lines in 4 notebooks (incl. `exercises/ch08`) name the author's directories; they are published in page JSON,
   HTML, the search index, the downloadable `build/*.ipynb`, and `DEFERRED.md`.
5. F5: warnings: 59 toc "Extension inferred" and 39 "Duplicate identifier" (reused `cell-NN` ids across notebooks).
6. F6: MyST fetches `https://github.com/myst-templates/book-theme/archive/refs/heads/main.zip` at build time (unpinned `main`) and
   queries `api.mystmd.org`; the build needs network and is not reproducible against theme changes.
7. F7: SVG figures render only client-side (embedded in `__remixContext`); a DOM-level figure check finds only the PNG.
8. F8: tooling drift to note for CI: uv 0.9.18 vs `0.5.x` in `ci.yml`, node 23.7.0 vs `.nvmrc` 22, `uv` chose Python 3.14.7.
9. F9: no broken internal links under `/toaster` (2305 refs + 78 content links).
