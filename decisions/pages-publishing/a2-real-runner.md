# PA-2: real-runner diagnosis (ubuntu-latest)

**Date:** 2026-10-03. **Workflow:** `.github/workflows/pages-diagnose.yml` on branch `pub/diagnose` (never merged to main; remote branch kept at Z's request). It builds the UNMODIFIED book on a clean runner; to let unmodified notebooks run it creates the hard-coded paths as symlinks to freshly provisioned tools (diagnosis only).

## Runs

| Run | Commit | Tools | Result |
|---|---|---|---|
| 37146440620 | 7498a97 | toolkit v0.9.1 (linux x86_64, sha256 verified), PlantUML 1.2026.8 jar (sha256 verified), SysML-v2-Release `de1070ae...` | 85 s job, 59 pages built in 24 s. **2 notebooks fail:** Ch8-02 cell 5 `ModelCheckError ... error: Z3 is not available: cannot run \`z3\`: No such file or directory`; Ch10-01 cell 19 `StopIteration` (cascade: the solver output it parses is absent). 18 figures. Leaks: `/home/runner` 2 files (failed-cell tracebacks), `/opt/homebrew` 4, `Documents/GitHub` 12, `/Users/` 0. |
| 37146757647 | 48b8bb7 | the above + Z3 5.1.0 (`z3-5.1.0-x64-glibc-2.39.zip`, sha256 `f47be8d27d3230e823bf1eeede2fe0abaca55bb78d0b59974370e6689a92284a`, matches the published digest; `z3` on PATH) | 95 s job, 59 pages built in 27 s. **0 cell errors.** 18 figures. Leaks: `/home/runner` 0, `/opt/homebrew` 4, `Documents/GitHub` 12, `/Users/` 0. |

## Findings

1. **`sysmlv2 verify --solve` shells out to a separate `z3` executable** (the binary links no libz3). A runner without `z3` on PATH fails Ch8-02 and Ch10-01. Provision Z3 5.1.0 (same version as Z's machine) by pinned download; do not rely on Ubuntu's apt `z3` (older).
2. **Linux reproduces the macOS outputs exactly.** With the v0.9.1 release binary, Z3 5.1.0 and PlantUML 1.2026.8 on `ubuntu-latest`, the executed outputs of Ch8-01, Ch8-02, Ch8-03 and Ch10-01 equal the stored (macOS) outputs after whitespace normalisation, apart from the `<IPython.core.display.SVG object>` repr that figure cells print when executed (their stored copies are empty by convention). Ch8-02 prints `[satisfied] deliveredEnergyBoundedBySupply (z3: holds for all values of unbound features)`, `[violated] deliveredEnergyExceedsSupply (z3: unsatisfiable -- no assignment can make this hold)` and `[undecided] ... z3: satisfiable, e.g. heatGenCheck.efficiency = 0, heatGenCheck.power = 0 [W], heatGenCheckDuration = 1 [s]`. This closes PA-3's open Linux question for these notebooks.
3. **Ch5-03 passes on Linux only with a current PlantUML.** Ubuntu's apt PlantUML 1.2020.2 rejects the committed `figures/ch05-interconnection.puml`; the upstream jar renders it (the Ch5 figure is produced; 18 figures total). Ubuntu's `openjdk-17-jre-headless` is enough as the Java runtime.
4. **Figure count = 18 is necessary but not sufficient.** In run 1, 18 figures were present even though two notebooks failed, because the failures come after their figure cells. CI must also require zero cell errors (`--strict`, or the exception count).
5. **Cost.** The whole job (checkout, uv sync, npm ci, apt, four downloads, execute every notebook, build 59 pages) takes about 95 s on a cold runner; the MyST build itself 24-27 s. Spec Q1 (CI time) is answered: well under two minutes with no caching.
6. **Residual leaks come from notebook source, not execution.** `Documents/GitHub` (12 files) and `/opt/homebrew` (4 files) appear because the cells name those paths; `/home/runner` vanished once nothing failed. Removing the hard-coded paths (Phase B) clears them.
7. Warnings unchanged from the Mac: 59 "Extension inferred", 39 "Duplicate identifier".

## Not covered

The runs used symlinks at the hard-coded paths, so they do not test the future tool resolver; `check-tools.py` was run on the runner and passed. Python on the runner was whatever `uv sync --locked` selected; Node followed `.nvmrc`. No deploy or Pages-artifact step was exercised.
