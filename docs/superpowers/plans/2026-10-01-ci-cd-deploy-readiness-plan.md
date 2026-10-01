# CI/CD Deploy-Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `.github/workflows/ci.yml`'s `deploy` job from a placeholder (`echo "Pages deployment placeholder"`) into the real, working seven-step pipeline `docs/contributor.md` already documents — so that flipping `if: false` is the *last* step, not the first, and actually produces a correct, live GitHub Pages site at `https://open-mbee.github.io/toaster/`.

**Architecture:** No new service, no new language, no new dependency beyond what's already pinned (`mystmd`, `opensysml`, standard `actions/*` GitHub Actions for Pages). Seven CI steps, each independently testable locally before it's trusted in CI, matching `docs/contributor.md`'s own numbered list exactly. The `build` job (push + PR, read-only) gets steps 1–4 and 6 added to what it already does (`pytest`, tool checks); a separate `deploy` job (main-only, `pages: write`) gets steps 5 and 7, gated behind `build` passing and, once enabled, behind a branch guard `docs/contributor.md` already calls out as a prerequisite it doesn't yet have.

**Tech Stack:** GitHub Actions (`actions/checkout`, `astral-sh/setup-uv`, `actions/setup-node`, `actions/configure-pages`, `actions/upload-pages-artifact`, `actions/deploy-pages`), `mystmd` (already pinned at 1.11.0), `opensysml` v0.9.0, Python 3.12+, Node 22 (`.nvmrc`).

**Spec:** [`docs/contributor.md`](../../contributor.md)'s "Deployment status" section is the existing, authoritative spec for what the seven steps are and what order they run in — this plan does not redesign that pipeline, it implements it. Also read `.claude/skills/orchestrator-protocol/SKILL.md`'s WP-8 row (`site at /toaster locally; navigation works; downloads present; 7-step CI passes; Pages deploys`) for the acceptance bar this whole plan is scoped against.

## Global Constraints

- **The `deploy` job stays gated behind `if: false` until Task 7's branch guard is in place AND a human (Z) decides content is ready** (`docs/contributor.md`: "Enabling it is a decision the maintainer makes explicitly... not something a passing build should trigger on its own"). This plan builds and verifies every step *up to* that flip; flipping it is Task 8, done deliberately, separately, never bundled into the same PR/commit as a content change.
- **Single-platform CI only** (SA-4: `ubuntu-latest`). Do not add a matrix.
- **No custom CSS, no theme changes** (SA-5: default book-theme).
- **`exercises/` is excluded from notebook execution** in CI, same as the MyST build itself already excludes it (`myst.yml`'s `exclude: - exercises/**`) — exercises are blank learner workspaces, not CI-verified content.
- **Every new CI step must be runnable and verifiable locally first**, with the exact command recorded in this plan's own task text, before it's trusted inside a GitHub Actions YAML change — this project's own "probe before asserting" discipline (`ace-protocol`) applies to infrastructure the same as it applies to SysML constructs.
- **No `|| true` anywhere** (ace-protocol: "Gate verdicts only. `|| true` is banned everywhere"). A step that can fail must be allowed to fail the job.

## Review Focus

- **A notebook that raises mid-execution in CI must fail the build, not get silently skipped or reported as a warning.** `nbconvert`/`myst build --execute` have an `--allow-errors` style flag that does the opposite of what CI needs; Task 1's own acceptance test deliberately breaks a cell and confirms the build goes red, not green.
- **The `deploy` job's `pages: write` / `id-token: write` permissions must never be inherited by the `build` job.** `docs/contributor.md` already states this ("This step alone carries the `pages: write` permission; the `build` job does not") — Task 6's own review step confirms the permissions block is job-scoped, not workflow-scoped.
- **A PR build must never trigger a real deploy**, even after `if: false` is removed. This is `docs/contributor.md`'s own explicitly flagged gap (the workflow triggers on `pull_request` too, and today only `needs: build` gates `deploy`) — Task 7 is not complete until this is independently verified by opening a scratch PR and confirming `deploy` does not run.
- **The built site must resolve correctly under the `/toaster` subpath**, not just at a bare `localhost:3000` root the way local dev preview serves it — a relative-link or asset-path bug that's invisible in local dev can 404 everything once deployed under `https://open-mbee.github.io/toaster/`. Task 2's own acceptance test builds a static export and serves it from a `/toaster` subpath locally, not just the dev server's own root-path preview.
- **A broken internal link or a 404'd asset must fail the build**, not just get noticed by a human reading the deployed site later (which is exactly how last night's "Case studies" 404 and this session's earlier title-mismatch bugs were found — manually, after the fact). Task 5 exists specifically so this class of bug is caught by CI before it ships, not after.

---

## Task 1: Wire real notebook execution into the `build` job (steps 1–2 of the spec)

**Files:**
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: the existing `uv sync --locked` / `npm ci` / `scripts/check-tools.py` steps already in `build` (unchanged).
- Produces: a CI step that fails the whole job if any chapter notebook raises during execution. Task 3 and Task 5 both run *after* this step and depend on it having actually executed every notebook (not just loaded them).

**Design decision this task makes, stated explicitly so it can be reviewed:** execute notebooks via `npx mystmd build --execute` itself (which re-executes every notebook as part of building the site), rather than a separate `jupyter nbconvert --execute` pass per notebook followed by a *second*, redundant execution inside the MyST build. `docs/contributor.md`'s step 2 ("execute every chapter notebook") and step 5 ("build the MyST site") read as two numbered steps but do not have to be two separate *mechanical* CI steps — collapsing them avoids executing every notebook twice (once via nbconvert, once via MyST) for no benefit. If local verification (Step 2 below) finds that `mystmd build --execute` does *not* fail loudly on a broken cell the way CI needs, fall back to a separate `nbconvert --execute` pass before the MyST build and say so in this task's own report — do not silently assume either behavior.

- [ ] **Step 1: Probe `mystmd build --execute`'s failure behavior locally, before writing any CI YAML**

```bash
# Deliberately break one cell to confirm the build actually fails loudly
cp chapters/ch01-system-purpose/01-abstract-def.ipynb /tmp/01-abstract-def.ipynb.bak
python3 - <<'EOF'
import json
nb = json.load(open("chapters/ch01-system-purpose/01-abstract-def.ipynb"))
nb["cells"][2]["source"] = ["raise RuntimeError('deliberate CI probe failure')"]
json.dump(nb, open("chapters/ch01-system-purpose/01-abstract-def.ipynb", "w"))
EOF
npx mystmd build --execute; echo "exit code: $?"
# Restore immediately, do not commit the broken state
cp /tmp/01-abstract-def.ipynb.bak chapters/ch01-system-purpose/01-abstract-def.ipynb
```

Expected and required: non-zero exit code. If `mystmd build --execute` exits 0 despite the raised error, this is a real, load-bearing finding — do not proceed to Step 2 with that command; use a prior `jupyter nbconvert --to notebook --execute` pass (which this session already confirmed, repeatedly, fails loudly and is already the pattern every judgment-record retrofit task this session verified against) as the CI execution step instead, and build the static site in a separate step afterward without `--execute` (consuming the already-executed notebook outputs on disk, or re-running `mystmd build --execute` a second time and accepting the double-execution cost — record which fallback was chosen and why).

- [ ] **Step 2: Add the execution step to `.github/workflows/ci.yml`'s `build` job**, after the existing `Check tool versions` step and before any new staging/check step:

```yaml
      # Step 2: Execute every chapter notebook and build the MyST site
      - name: Execute notebooks and build site
        run: npx mystmd build --execute
```

(Or the nbconvert-first fallback from Step 1, if that's what the probe required — write the actual, verified-working YAML here, not this plan's own default guess.)

- [ ] **Step 3: Confirm the full `build` job still passes on an unmodified checkout.** Run the equivalent sequence locally end to end (`uv sync --locked && npm ci && uv run python scripts/check-tools.py && npx mystmd build --execute`) and confirm it exits 0.

- [ ] **Step 4: Commit.**
```bash
git add .github/workflows/ci.yml
git commit -m "CI: execute every chapter notebook and build the MyST site (step 2/5 of the documented pipeline)"
```

---

## Task 2: Add the `/toaster` base-path config and verify the built site resolves under it

**Files:**
- Modify: `myst.yml`

**Interfaces:**
- Consumes: nothing new.
- Produces: a `project.github`-adjacent base-URL config that makes every internal link, asset path and downloaded-figure reference resolve correctly when the site is served from `https://open-mbee.github.io/toaster/` instead of a bare domain root. Task 5's own link-checker runs against a site built with this config, not the bare-root dev-server config Task 1 and all of last night's/this session's manual testing used.

- [ ] **Step 1: Confirm the config key.** MyST's base-path option for GitHub Pages project sites is documented at `https://mystmd.org/guide/deployment#deploy-base-url` (the same page `myst.yml`'s own "Site not loading correctly?" fallback banner, found during this session's browser testing, already links to) — read it directly and confirm the exact key name and YAML shape for the current pinned `mystmd` version (1.11.0) before writing it, rather than guessing from memory.

- [ ] **Step 2: Add the config to `myst.yml`.**

- [ ] **Step 3: Build a static export and serve it from a `/toaster` subpath locally, not the dev server's bare root:**

```bash
npx mystmd build --execute --html
cd /tmp && python3 -m http.server 8080 --directory - <<'EOF'
# serve _build/html (or wherever this mystmd version emits static output) at /toaster/,
# e.g. by symlinking it into a parent dir named "toaster" and serving the parent
EOF
```

(Write the actual working local-verification commands here once Step 1's exact output directory and serving approach are confirmed — `mystmd`'s own docs or `--help` output names the real build output path; don't assume `_build/html` without checking.)

- [ ] **Step 4: Visually/programmatically confirm** at least one chapter page, one figure, and one cross-chapter link resolve correctly under the `/toaster/...` prefix, not just at the bare root.

- [ ] **Step 5: Commit.**
```bash
git add myst.yml
git commit -m "Configure the /toaster base path for GitHub Pages project-site deployment"
```

---

## Task 3: Wire the two existing, already-working conformance scripts into CI (step 3 of the spec)

**Files:**
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: `scripts/check_construction.py` and `scripts/check_conformance.py`, both already working, already used throughout this session's own manual verification (`uv run python scripts/check_construction.py --check` was run as an acceptance gate on every one of last night's 15 implementation tasks), but **not currently called anywhere in CI** (confirmed by grep — this is a real gap, not a restatement of existing coverage).

**Context on why this task is small:** `docs/contributor.md`'s step 3 ("assert expected outputs, diagnostics, negative controls, and review-record integrity") sounds like it might need new tooling, but it mostly doesn't — every chapter notebook already asserts its own expected output inline (`assert model.ok`, `assert not bad.ok`, `assert errors == [...]`, confirmed throughout this session's own retrofit work), so Task 1's own notebook execution already enforces most of step 3 as a side effect of failing loudly on any `assert`. What's missing is the two *cross-notebook, cross-chapter* checks that no single notebook's own assertions can cover: construction-zone-to-committed-fixture consistency (`check_construction.py`) and the staged project-conformance tiers (`check_conformance.py`).

- [ ] **Step 1: Run both scripts locally against the current `main`/working branch to confirm they pass clean today** (a prerequisite for adding them to CI — if either currently fails, that's a separate, pre-existing bug to fix first, not something to paper over with `|| true`):
```bash
uv run python scripts/check_construction.py --check
uv run python scripts/check_conformance.py
```

- [ ] **Step 2: Add both as CI steps**, after the notebook-execution step from Task 1:
```yaml
      # Step 3: Construction-zone and conformance checks
      - name: Check construction zone consistency
        run: uv run python scripts/check_construction.py --check
      - name: Check project conformance
        run: uv run python scripts/check_conformance.py
```

- [ ] **Step 3: Confirm the full `build` job still passes locally** with both new steps added (re-run the full local sequence from Task 1 Step 3, now including these two commands).

- [ ] **Step 4: Commit.**
```bash
git add .github/workflows/ci.yml
git commit -m "CI: wire check_construction.py and check_conformance.py into the build job (step 3/5)"
```

---

## Task 4: Stage build artifacts (step 4 of the spec) — scope this down, don't invent a manifest format unasked

**Files:**
- Modify: `.github/workflows/ci.yml`

**Context — a genuine open question, not resolved by this plan:** `docs/contributor.md`'s step 4 names "executed notebooks, generated models, figures, and a provenance manifest." The first three already exist as ordinary build output once Task 1's execution step runs (executed notebooks are on disk; `models/*.sysml` are already committed, not generated fresh; `figures/*.svg` are already committed too, confirmed during this session's own browser testing of the Chapter 5 interconnection figure). **No provenance-manifest format or generator exists anywhere in this repo today** (confirmed by grep for "provenance" and "manifest" across `scripts/` and `src/toaster/`) — this is new, not wiring-up-the-existing the way Task 3 was.

- [ ] **Step 1: Decide, with Z, whether a provenance manifest is actually required for the first real deploy, or a `next-passes.md`-tracked follow-up.** A minimal version (commit SHA, build timestamp, `mystmd`/`opensysml` versions, written as one JSON file into the build output) is cheap and low-risk if wanted now; a richer one (per-chapter execution hashes, content-addressed figure provenance) is a larger, separate design question this plan does not scope. **Do not build either without that decision** — this step is a checkpoint, not optional busywork to skip.

- [ ] **Step 2 (only if Step 1 says "yes, minimal version now"):** add a small script (`scripts/write_provenance_manifest.py`) that writes `{commit, built_at, mystmd_version, opensysml_version}` as JSON into the build output directory, and one CI step that calls it between the build (Task 1) and the upload-artifact step (Task 6).

- [ ] **Step 3: Commit**, if Step 2 was done.

---

## Task 5: Automated post-build link and asset check (step 6 of the spec)

**Files:**
- Create: `scripts/check_site_links.py`
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: the static site built by Task 1 + Task 2 (served locally under the `/toaster` prefix, same as Task 2's own verification).
- Produces: a CI step that fails the build if any internal link resolves to a 404, any image/figure fails to load, or any page is missing its expected title — the same class of check this session performed *manually* last night (a scripted `fetch()` loop over all 58 known page URLs, checking for `Document Not Found`, tracebacks, and non-200 statuses) and found one real bug with (the "Case studies" 404, already fixed). This task turns that manual, one-off script into a permanent, repeatable CI gate.

- [ ] **Step 1: Write `scripts/check_site_links.py`**, adapting the exact approach this session used manually: start a local HTTP server against the built static output (served under `/toaster`, matching Task 2), enumerate every page MyST's own build manifest or `myst.yml`'s project TOC lists (don't hand-maintain a separate URL list that can drift from the real TOC the way this plan's own earlier browser-testing session found stale titles drifting from `myst.yml`), fetch each one, and fail (non-zero exit, printing every failing URL) if any: HTTP status is not 200, the response body contains `Document Not Found`, or any `<img>`/figure fails to resolve (a HEAD request against every `src` found in the fetched HTML). This must also catch every `exercises/ch{N}/exercise.ipynb` link each chapter's `index.md`/`conclusion.md` carries: `myst.yml` excludes `exercises/**` from the build (`myst-publication` skill), so on the dev server these links resolve by falling through to a locally running Jupyter server, a fallback that does not exist on the static build — the user-testing grid's M2-novice cell found this ambiguity (`decisions/log.md` DL-085(5)) and it was unverified against a real static build until this task runs. If the static build cannot serve an excluded path, this is a real content bug (the link must be rewritten to the file's GitHub URL instead), not a checker gap to special-case around.

- [ ] **Step 2: Run it locally against a `/toaster`-served build** (Task 2's own local serving setup) and confirm it exits 0 on the current, already-fixed site, then confirm it correctly fails (non-zero, with a clear message) when pointed at a deliberately-reintroduced broken link (e.g., temporarily re-break the "Case studies" link this session already fixed, confirm the script catches it, then revert).

- [ ] **Step 3: Add it as a CI step**, after the build and staging steps:
```yaml
      # Step 6: Check navigation, links, and assets under the /toaster base path
      - name: Check site links and assets
        run: uv run python scripts/check_site_links.py
```

- [ ] **Step 4: Commit.**
```bash
git add scripts/check_site_links.py .github/workflows/ci.yml
git commit -m "CI: add an automated link/asset checker for the built site (step 6/7)"
```

---

## Task 6: Replace the `deploy` job's placeholder with the real Pages deploy (step 7 of the spec)

**Files:**
- Modify: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: Task 1 through Task 5's build output.
- Produces: a real, working `deploy` job using the standard GitHub Actions Pages flow. **`if: false` stays in place through this entire task** — this task makes the job *correct*, not *enabled*; Task 8 is the separate, deliberate act of enabling it.

- [ ] **Step 1: Replace the placeholder `deploy` job** with the standard three-action Pages sequence, keeping `if: false` and `needs: build` exactly as they are today, and keeping the existing `pages: write` / `id-token: write` permissions block scoped to this job only (confirmed in Review Focus above — do not move it to the workflow-level `permissions:` key):

```yaml
  deploy:
    if: false  # still disabled -- Task 8 flips this, deliberately, separately
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
        with:
          version: "0.5.x"
      - run: uv sync --locked
      - uses: actions/setup-node@v4
        with:
          node-version-file: .nvmrc
      - run: npm ci
      - run: npx mystmd build --execute --html
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: <the real build output directory, confirmed in Task 2 Step 1 — do not guess>
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

(The `deploy` job rebuilds rather than reusing `build`'s own artifact, matching this repo's existing single-job-per-concern CI style and avoiding a cross-job artifact-passing mechanism this plan doesn't otherwise need — note this as a deliberate simplicity choice, not an oversight, when reviewing.)

- [ ] **Step 2: Add the branch guard `docs/contributor.md` explicitly requires before enabling deployment** (quoted in that file: "Simply removing `if: false` would let `deploy` run on a successful pull-request build too... Add `if: github.ref == 'refs/heads/main'`"). Combine it with the existing `if: false` for now (`if: false && github.ref == 'refs/heads/main'`), so the guard is in place and reviewable before Task 8 ever needs to touch this line again — Task 8 then only has to delete the `false &&` prefix, nothing else.

- [ ] **Step 3: Verify the guard independently, per this plan's own Review Focus.** Open a scratch PR against a throwaway branch (not `main`) with a trivial, reversible change, and confirm in the Actions tab that `build` runs but `deploy` is skipped — both because of `if: false` (expected either way right now) and, separately, trace through the YAML logic by hand to confirm that even with `false &&` removed, a PR-triggered run's `github.ref` would not equal `refs/heads/main` and `deploy` would still correctly skip.

- [ ] **Step 4: Commit.**
```bash
git add .github/workflows/ci.yml
git commit -m "CI: replace deploy placeholder with the real Pages pipeline, still gated off (step 7/7, deploy stays disabled)"
```

---

## Task 7: Dry-run the complete pipeline before asking Z to flip anything

**Files:** none (verification only).

- [ ] **Step 1: Push this plan's branch and open a real PR**, so the full `build` job (Tasks 1–5) runs for real in GitHub's own CI environment, not just locally — confirm every step this plan added is green there, not only on a local machine that may have tool versions or caches the CI runner doesn't.
- [ ] **Step 2: Temporarily flip `if: false && github.ref == 'refs/heads/main'` to `if: true && github.ref == 'refs/heads/main'` on a throwaway branch only** (never on this plan's real PR branch, never on `main`), push it as its own disposable branch, and confirm the `deploy` job runs and either succeeds or fails informatively. Delete the throwaway branch afterward regardless of outcome; this step exists to prove the deploy job itself works, not to actually publish anything yet.
- [ ] **Step 3: Report results to Z**: every step's real CI run output, the dry-run deploy's outcome, and an explicit recommendation on whether Task 8 is ready.

---

## Task 8: Enable deployment (Z's own action, not a subagent task)

This is deliberately **not** broken into sub-steps here, per `docs/contributor.md`'s own stated philosophy: enabling deployment is a decision Z makes explicitly, once, when content is ready — not a task a builder executes as part of a normal contract. When Z decides to do it: remove `false && ` from the `deploy` job's `if:` condition (leaving only the branch guard), on its own commit, on `main`, separately from any content change.

---

## Sequencing

Tasks 1–6 have real dependencies on each other's outputs (Task 3/5/6 all need Task 1's execution step; Task 5 needs Task 2's base-path config) but touch the *same single file* (`.github/workflows/ci.yml`) in five of six cases — **run them strictly in series**, same reasoning as this session's own Hawkins-plan execution: a shared-blast-zone file forces serial dispatch regardless of logical independence. Task 4 is a genuine checkpoint-then-maybe-branch, not a hard dependency of 5 or 6. Task 7 depends on 1–6 all being merged. Task 8 depends on 7's dry run actually succeeding and is Z's own action.
