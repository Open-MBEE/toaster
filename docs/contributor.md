# Contributor Guide

This page is for maintainers working on the tutorial itself, not learners working through it.
It assumes you can read Python and SysML and that you have the environment from
[Getting Started](setup.md) already set up.

(what-we-accept)=
## What we accept

The contributions we want keep this tutorial current to its toolchain (the OpenSysML runtime, sysml-toolkit and the other pinned tools) and to the OMG SysML v2 specifications; we are not adding new content. Existing content may be refined, clarified or otherwise improved against three priorities: (1) conformance with the SysML v2 specifications (the OMG SysML v2 language, API and Services, and KerML specifications); (2) didactic clarity; (3) effective, demonstrative use of tools from the OpenSysML stack (the OpenSysML runtime and sysml-toolkit). An improvement is accepted only if it is strictly dominant: better on at least one of these and worse on none. The binding statement is [`AGENTS.md`](https://github.com/Open-MBEE/toaster/blob/main/AGENTS.md) §1.12.

- **Keep current.** Bump a pin in `pyproject.toml`/`uv.lock`, `package.json`/`package-lock.json` or [`scripts/tool-pins.json`](https://github.com/Open-MBEE/toaster/blob/main/scripts/tool-pins.json) and regenerate the outputs ([below](#keep-current)); retire a workaround whose [`DEFERRED.md`](https://github.com/Open-MBEE/toaster/blob/main/DEFERRED.md) resolution condition a new release meets, adding a dated status line to that entry (or updating the one it has), updating the comment cell at the workaround, and leaving the heading as it is (headings are linked anchors); re-check a clause that a new edition of one of the three OMG specifications changed. Reporting drift is a contribution too: open an issue naming the tool and version (or the specification edition), the chapter and cell, and the spec clause. Upstream issues are filed by the project itself, after mzargham (Z) has reviewed the text (`AGENTS.md` §1.9).
- **Improve what is here.** State in the pull request which priority improves and the evidence, and for each of the other two why it is not worse; the pull-request template asks for exactly this. Adding text or a cell counts as improving only if the learner's task gets harder without it, and the pacing rule and the one-construct-per-notebook rule still apply. An independent reviewer on a different AI model checks the statement; what the reviewer cannot tell goes to the ACE (the project's triage role, described below). A trade-off (better on one priority, worse on another) is not an improvement under this policy: open an issue and Z decides.
- **Not accepted by pull request.** A new chapter, notebook, exercise, construct or analysis operation, model element, judgment record or glossary term, or a new learning outcome. Replacing a recorded workaround with the spec-anchored construct a newer tool release accepts is keeping current, not new content. If you think the tutorial needs something new, open an issue; only Z decides that, and a glossary term is confirmed only by Z.

The reviewer applies this test. A pull request passes when one "better" line (or, for keeping
current, the currency event) and all three "not worse" lines are evidenced; any "worse" means the
change is not accepted; what the reviewer cannot tell goes to the ACE.

| Priority | "Worse" means | Verified by, with what evidence |
|---|---|---|
| (1) Spec conformance | Text or model violating a normative clause of one of the three specifications; a spec-anchored construct replaced by a tool idiom; a conformance check or its negative control dropped or weakened | Reviewer: the clause citation, `uv run python scripts/check_conformance.py`, a strict load under the pinned runtime; the OMG SysML v2 Pilot Implementation is the baseline where a clause is ambiguous |
| (2) Didactic clarity | Longer or denser without the learner's task getting harder without it; a second construct or operation in one sub-notebook; a check presented as proof; the pacing rule broken; a figure whose omissions are no longer stated | Reviewer: the pull request's statement, the pacing check, and a simulated-learner checkpoint when the change alters what a learner does or sees beyond wording |
| (3) Tool use | A construct described as working but not run under the pinned version; a new workaround without a `DEFERRED.md` entry and comment cell; a tool demonstration removed; meaning moved from the model into Python | CI (`TOASTER_REQUIRE_TOOLS=1`, `myst build --strict`, `scripts/check-site.py`) and the reviewer re-running the touched notebook; the executed outputs and the `DEFERRED.md` entries touched |

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
  implement and independently check each change (always on different AI models, never the same
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

If you want to keep a chapter current, clarify a definition, or review didactic content, the harness
tools above are built for exactly that — start at `CLAUDE.md`'s own read order rather than
improvising a workflow from scratch. The sections below cover the maintenance tasks directly; none
of them require running an agent, but all of them follow conventions the harness itself enforces
(the recipe's pacing rule, the layer boundary tests, the review gate), and every change passes the
test in [What we accept](#what-we-accept).

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

(keep-current)=
## Keep current: update a dependency or tool pin and regenerate outputs

1. Change the version in `pyproject.toml` (Python), `package.json` (Node) or
   [`scripts/tool-pins.json`](https://github.com/Open-MBEE/toaster/blob/main/scripts/tool-pins.json)
   (the `sysmlv2` binary, Z3 and the PlantUML jar with their sha256 hashes, and the
   standard-library commit), then `uv lock` / `npm install` to update the lockfile, or
   `uv run python scripts/provision-tools.py` to re-provision `.tools/`. The OpenSysML runtime
   binary is pinned separately from the `opensysml` package: change the `version="v0.9.0"`
   defaults in `src/toaster/bootstrap.py` (and its `_CLI_SUMS` hashes) and
   `src/toaster/connect.py`, and the `opensysml.connect(version=...)` calls in
   `scripts/check_conformance.py` and `scripts/check_construction.py`, together.
2. Run `TOASTER_REQUIRE_TOOLS=1 uv run pytest tests/ glossary/tests/` and
   `uv run python scripts/check-tools.py`
   ([`check-tools.py` on GitHub](https://github.com/Open-MBEE/toaster/blob/main/scripts/check-tools.py)).
3. Rebuild the local preview (`uv run npx mystmd start --execute`) and spot-check a chapter that
   exercises the changed dependency; a version bump in `opensysml` or `sympy` can change
   printed output even when no test fails.
4. Re-read the `DEFERRED.md` entries that name the bumped tool. If the new release meets an
   entry's resolution condition, retire the workaround, add a dated status line to the entry (or
   update the one it has), update the comment cell at the workaround (do not rename the heading),
   and recompute the `content_hash` of any judgment record the model change touches
   ([below](#change-a-model-element)). A release
   that breaks something gets a new entry, not a silently dropped demonstration.
5. Commit the lockfile or the pins alongside the version change; never bump a version without
   regenerating and committing what matches it. Update the version strings in
   `docs/setup.md`, `docs/reproducibility.md` and `AGENTS.md` §1.2 in the same change, and
   re-check chapter prose and `DEFERRED.md` entries that state a version
   (`git grep -n 'v0\.9\.[01]' -- chapters DEFERRED.md`): a statement re-probed under the new
   release takes the new version; one not re-probed keeps the version it was probed against.

## How a change is built and reviewed

New chapters are not accepted ([What we accept](#what-we-accept)); the rules that governed
building the existing ones govern every change to them:

1. `toaster-recipe`'s sub-notebook skeleton and `architecture-layers`' boundary tests bind any
   model element a change touches; both are binding, not stylistic suggestions.
2. Each cumulative fixture (`models/chNN-cumulative.sysml`) must keep containing everything the
   previous chapter's fixture has; see
   [`tests/test_predecessor_containment.py`](https://github.com/Open-MBEE/toaster/blob/main/tests/test_predecessor_containment.py) for how that invariant is checked.
   After changing a notebook's construction cells or a fixture, run
   `uv run python scripts/check_construction.py --check --chapter=N`
   ([`scripts/check_construction.py`](https://github.com/Open-MBEE/toaster/blob/main/scripts/check_construction.py)):
   it executes the registered construction zones and loads each `TOASTER_INCREMENT` and the
   cumulative fixture. Update a notebook's existing `CONSTRUCTION_NOTEBOOKS` entry only if its
   stubs change; new entries are for new notebooks, which are not accepted.
3. Run `uv run python -m glossary lint` before committing prose; run the pacing check in
   `tutorial-style-guide` (consecutive code cells with no markdown between them) on every
   notebook you touched.
4. Get an independent review on a different AI model than whoever authored the change, per
   `decisions/task-states.md`'s merge gate.

(change-a-model-element)=
## Change a model element and review stale judgment records

A `ReviewRecord`'s `content_hash` is computed from the model source it was written against.
Changing that source without updating the record leaves it silently stale.

A model change is accepted only as keeping current (a workaround retired) or as a strictly
dominant improvement ([What we accept](#what-we-accept)); either way:

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
