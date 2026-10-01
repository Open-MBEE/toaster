# Contributor Guide

This page is for maintainers working on the tutorial itself, not learners working through it.
It assumes you can read Python and SysML and that you have the environment from
[Getting Started](setup.md) already set up.

## How this repo is built, tested, and reviewed

The tutorial's content — every chapter notebook, exercise, and model file — is built and
reviewed through a small multi-agent harness that lives alongside the content itself. Three
root files and two directories carry that harness, and they're worth knowing about before you
touch anything, even if you never run an agent yourself:

- **`AGENTS.md`** states what the tutorial teaches (the functional/logical/physical layering,
  where its terms come from, how models are built and queried) and the legacy role roster that
  used to own each file. It's the harness's own foundational reference, read first by every
  agent role before it does anything else.
- **`CLAUDE.md`** is the entry point: read order, the glossary CLI, and the skill index below.
- **`DEFERRED.md`** tracks known gaps in the toolchain (OpenSysML, sysml-toolkit) that the
  tutorial works around — what the workaround is, why it's needed, and the condition under
  which it comes out once the upstream gap closes.
- **`.claude/agents/`** defines the roles that do the work: an `orchestrator` that turns a
  request into scoped contracts and integrates results; `builder`/`reviewer` pairs that
  implement and independently check each change (always on different models, never the same
  one reviewing its own work); a `layer-auditor` that classifies model elements against the
  functional/logical/physical boundaries; a `simulated-learner` that executes a chapter as a
  persona-assigned reader and reports what it found; and the `ace`, which triages questions
  between the team and the tutorial's author, ruling where it can and escalating what it can't.
- **`.claude/skills/`** holds the how-to for each kind of work — the sub-notebook template and
  pacing rules (`toaster-recipe`), the boundary tests for classifying a model element
  (`architecture-layers`), the glossary's own usage rules (`tutorial-glossary`), the simulated
  learner protocol (`user-testing`), and more — each one a reference an agent (or a human
  contributor) reads before doing that kind of work, not after.
- **`decisions/`** is the record of what was decided and why: `log.md` (the running decision
  log, one entry per substantive ruling or escalation), `work-contract-template.md` (the shape
  of a task handed to a builder or reviewer), and `task-states.md` (what state a task is in and
  what moves it to the next one).

If you want to extend a chapter, clarify a definition, or review didactic content, the harness
tools above are built for exactly that — start at `CLAUDE.md`'s own read order rather than
improvising a workflow from scratch. The sections below cover specific maintenance tasks
directly; none of them require running an agent, but all of them follow conventions the harness
itself enforces (the recipe's pacing rule, the layer boundary tests, the review gate).

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
