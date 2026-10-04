# Contributor Guide

This page is for maintainers working on the tutorial itself, not learners working through it.
It assumes you can read Python and SysML and that you have the environment from
[Getting Started](setup.md) already set up.

## Who is Z

"Z" is the contributor identity `mzargham` (Michael Zargham, GitHub user
[`mzargham`](https://github.com/mzargham)), the project's author and chief engineer. Project files
such as [`AGENTS.md`](https://github.com/Open-MBEE/toaster/blob/main/AGENTS.md) and the decision log in
[`decisions/`](https://github.com/Open-MBEE/toaster/tree/main/decisions) say "Z" for that person. Published pages that mention
"Z" name the handle at first mention, as "mzargham (Z)". Other contributors are named by their
own handles, and "Z" is never reused for anyone else.

## How this repo is built, tested, and reviewed

The tutorial's content — every chapter notebook, exercise, and model file — is built and
reviewed through a small multi-agent harness that lives alongside the content itself. Three
root files and two directories carry that harness, and they're worth knowing about before you
touch anything, even if you never run an agent yourself:

- **[`AGENTS.md`](https://github.com/Open-MBEE/toaster/blob/main/AGENTS.md)** states what the tutorial teaches (the functional/logical/physical layering,
  where its terms come from, how models are built and queried) and the legacy role roster that
  used to own each file. It's the harness's own foundational reference, read first by every
  agent role before it does anything else.
- **[`CLAUDE.md`](https://github.com/Open-MBEE/toaster/blob/main/CLAUDE.md)** is the entry point: read order, the glossary CLI, and the skill index below.
- **[`DEFERRED.md`](https://github.com/Open-MBEE/toaster/blob/main/DEFERRED.md)** tracks known gaps in the toolchain (the OpenSysML runtime, sysml-toolkit) that the
  tutorial works around — what the workaround is, why it's needed, and the condition under
  which it comes out once the upstream gap closes.
- **[`.claude/agents/`](https://github.com/Open-MBEE/toaster/tree/main/.claude/agents)** defines the roles that do the work: an `orchestrator` that turns a
  request into scoped contracts and integrates results; `builder`/`reviewer` pairs that
  implement and independently check each change (always on different models, never the same
  one reviewing its own work); a `layer-auditor` that classifies model elements against the
  functional/logical/physical boundaries; a `simulated-learner` that executes a chapter as a
  persona-assigned reader and reports what it found; and the `ace`, which triages questions
  between the team and the tutorial's author, ruling where it can and escalating what it can't.
- **[`.claude/skills/`](https://github.com/Open-MBEE/toaster/tree/main/.claude/skills)** holds the how-to for each kind of work — the sub-notebook template and
  pacing rules (`toaster-recipe`), the boundary tests for classifying a model element
  (`architecture-layers`), the glossary's own usage rules (`tutorial-glossary`), the simulated
  learner protocol (`user-testing`), and more — each one a reference an agent (or a human
  contributor) reads before doing that kind of work, not after.
- **[`decisions/`](https://github.com/Open-MBEE/toaster/tree/main/decisions)** is the record of what was decided and why: `log.md` (the running decision
  log, one entry per substantive ruling or escalation), `work-contract-template.md` (the shape
  of a task handed to a builder or reviewer), and `task-states.md` (what state a task is in and
  what moves it to the next one).

If you want to extend a chapter, clarify a definition, or review didactic content, the harness
tools above are built for exactly that — start at `CLAUDE.md`'s own read order rather than
improvising a workflow from scratch. The sections below cover specific maintenance tasks
directly; none of them require running an agent, but all of them follow conventions the harness
itself enforces (the recipe's pacing rule, the layer boundary tests, the review gate).

(deployment-status)=
## Deployment status

CI builds the book on every pull request and deploys it from `main` to
<https://open-mbee.github.io/toaster/>. Pull-request builds do not deploy: the `deploy` job runs
only for a push to `main`, and only after the `build` job passes. The workflow is
[`.github/workflows/ci.yml`](https://github.com/Open-MBEE/toaster/blob/main/.github/workflows/ci.yml).

The `build` job provisions the tools with
[`scripts/provision-tools.py`](https://github.com/Open-MBEE/toaster/blob/main/scripts/provision-tools.py)
(see [Getting Started](#tools-for-chapters)), runs the test suite, builds the
book with every notebook executed, and then runs the release gate,
[`scripts/check-site.py`](https://github.com/Open-MBEE/toaster/blob/main/scripts/check-site.py).
The gate fails the build unless all five checks pass:

1. the build log has no code-execution or Jupyter-session failure (MyST exits 0 even when a cell
   raised unless it is run with `--strict`, which CI does; the log check backs that up, so a
   failed cell is caught even if the flag is ever dropped);
2. the built content has the expected number of figures, recorded in
   [`scripts/site-baseline.json`](https://github.com/Open-MBEE/toaster/blob/main/scripts/site-baseline.json);
3. no built text file contains a host path (a home directory, a Homebrew prefix or a CI runner path);
4. MyST has not published `exercises/` files or `DEFERRED.md` as raw downloads under `build/`;
5. every root-relative link and asset in the HTML carries the `/toaster` base path and points at
   a file that exists in the built site.

To reproduce the build and the gate locally, from a clone with the tools provisioned:

```sh
set -o pipefail
BASE_URL=/toaster uv run --frozen npx myst build --html --execute --strict 2>&1 | tee build.log
uv run python scripts/check-site.py --site _build/html --content _build/site/content \
    --log build.log --base-url /toaster
```

## Update a dependency and regenerate outputs

1. Change the version in `pyproject.toml` (Python) or `package.json` (Node), then
   `uv lock` / `npm install` to update the lockfile.
2. Run `uv run pytest tests/ glossary/tests/` and `uv run python scripts/check-tools.py`
   ([`check-tools.py` on GitHub](https://github.com/Open-MBEE/toaster/blob/main/scripts/check-tools.py)).
3. Rebuild the local preview (`uv run npx mystmd start --execute`) and spot-check a chapter that
   exercises the changed dependency; a version bump in `opensysml` or `sympy` can change
   printed output even when no test fails.
4. Commit the lockfile alongside the version change; never bump a version without
   regenerating and committing the matching lockfile.

## Add a new chapter

1. Follow `toaster-recipe`'s sub-notebook skeleton and `architecture-layers`' boundary tests
   for every new model element; both are binding, not stylistic suggestions.
2. Add the chapter's cumulative fixture (`models/chNN-cumulative.sysml`), authored to contain
   everything the previous chapter's fixture has plus the new chapter's own additions; see
   [`tests/test_predecessor_containment.py`](https://github.com/Open-MBEE/toaster/blob/main/tests/test_predecessor_containment.py) for how that invariant is checked.
3. Register the new notebooks in [`scripts/check_construction.py`](https://github.com/Open-MBEE/toaster/blob/main/scripts/check_construction.py)'s `CONSTRUCTION_NOTEBOOKS`
   and in `myst.yml`'s table of contents.
4. Run `uv run python -m glossary lint` before committing prose; run the pacing check in
   `tutorial-style-guide` (consecutive code cells with no markdown between them) on every new
   notebook.
5. Get an independent review on a different model than whoever authored the chapter, per
   `decisions/task-states.md`'s merge gate.

(change-a-model-element)=
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
uv run python scripts/provision-tools.py
uv run python scripts/check-tools.py
uv run pytest tests/ glossary/tests/ -v
uv run npx mystmd start --execute
```

The first five commands mirror the `build` job's provisioning and tests (the job also installs
Graphviz and a Java runtime from apt); the last serves the book for preview rather than building
it. CI runs pytest with `TOASTER_REQUIRE_TOOLS=1`, so a missing external tool fails the tests
instead of skipping them; prefix the pytest line with it to get the same behavior locally. To run the build itself and
the release gate, use the two commands under [Deployment status](#deployment-status). There is no
local equivalent of the `deploy` job, and there should not be, since publishing is a decision, not
a build artifact.
