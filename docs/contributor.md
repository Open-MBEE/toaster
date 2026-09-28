# Contributor Guide

This page is for maintainers working on the tutorial itself, not learners working through it.
It assumes you can read Python and SysML and that you have the environment from
[Getting Started](setup.md) already set up.

## Deployment status

Deployment to GitHub Pages is deliberately disabled (`.github/workflows/ci.yml`, the `deploy`
job's `if: false`), not merely unfinished. It stays off until the tutorial has complete,
end-to-end content ready to publish. Enabling it is a decision the maintainer makes explicitly
when that bar is met, by removing the `if: false` guard, not something a passing build should
trigger on its own.

Once enabled, the pipeline runs in seven steps, all defined in `.github/workflows/ci.yml`:

1. Provision the environment (`uv sync --locked`, `npm ci`, `scripts/check-tools.py`) and
   verify tool versions.
2. Execute every chapter notebook in a fresh kernel, with a timeout, excluding `exercises/`.
3. Assert expected outputs, diagnostics, negative controls, and review-record integrity.
4. Stage the executed notebooks, generated models, figures, and a provenance manifest.
5. Build the MyST site (`npx mystmd build`).
6. Check navigation, code, outputs, figures, and downloads render correctly under the
   `/toaster` base path.
7. Deploy to Pages. This step alone carries the `pages: write` permission; the `build` job
   does not.

**Before enabling deployment, add a branch guard the current YAML does not have.** The
workflow triggers on both push-to-`main` and `pull_request` (`on:` at the top of the file),
and the `deploy` job's only gate today is `needs: build` plus the disabled `if: false`. Simply
removing `if: false` would let `deploy` run on a successful pull-request build too, not only on
`main`, which is very unlikely to be intended. Add `if: github.ref == 'refs/heads/main'` (or
equivalent) to the `deploy` job at the same time you remove `if: false`, not as a separate,
later fix.

Enabling deployment, once that guard is in place: confirm the current `main` branch builds and
executes cleanly end to end (steps 1 through 6 above, run locally or via a scratch branch's CI
run), then push to `main`.

## Update a dependency and regenerate outputs

1. Change the version in `pyproject.toml` (Python) or `package.json` (Node), then
   `uv lock` / `npm install` to update the lockfile.
2. Run `uv run pytest tests/ glossary/tests/` and `uv run python scripts/check-tools.py`.
3. Rebuild the local preview (`npx mystmd start --execute`) and spot-check a chapter that
   exercises the changed dependency; a version bump in `opensysml` or `sympy` can change
   printed output even when no test fails.
4. Commit the lockfile alongside the version change; never bump a version without
   regenerating and committing the matching lockfile.

## Add a new chapter

1. Follow `toaster-recipe`'s sub-notebook skeleton and `architecture-layers`' boundary tests
   for every new model element; both are binding, not stylistic suggestions.
2. Add the chapter's cumulative fixture (`models/chNN-cumulative.sysml`), authored to contain
   everything the previous chapter's fixture has plus the new chapter's own additions; see
   `tests/test_predecessor_containment.py` for how that invariant is checked.
3. Register the new notebooks in `scripts/check_construction.py`'s `CONSTRUCTION_NOTEBOOKS`
   and in `myst.yml`'s table of contents.
4. Run `uv run python -m glossary lint` before committing prose; run the pacing check in
   `tutorial-style-guide` (consecutive code cells with no markdown between them) on every new
   notebook.
5. Get an independent review on a different model than whoever authored the chapter, per
   `decisions/task-states.md`'s merge gate.

## Change a model element and review stale judgment records

A `ReviewRecord`'s `content_hash` is computed from the model source it was written against.
Changing that source without updating the record leaves it silently stale.

1. Find every `ReviewRecord` whose `model_ref` touches the element you are changing
   (`grep -rl model_ref= chapters/`).
2. After changing the model, recompute each record's `content_hash` and re-run
   `validate_record` on it.
3. Re-read the record's `claim`, `rationale`, and `counterevidence` fields against the new
   model state. A hash mismatch tells you the record is stale; it does not tell you whether
   the claim is still true. Rewrite what no longer holds; do not just refresh the hash.

## Run the full CI pipeline locally

```sh
uv sync --locked
npm ci
uv run python scripts/check-tools.py
uv run pytest tests/ glossary/tests/ -v
npx mystmd start --execute
```

This mirrors the `build` job's steps 1 through 6. It does not run step 7 (deploy); there is no
local equivalent, and there should not be, since publishing is a decision, not a build artifact.
