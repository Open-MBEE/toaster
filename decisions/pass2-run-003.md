# Pass 2, run 003: blocked and wont-do, independent review (2026-09-26)

Purpose: apply Z's minor revisions (a `blocked` status with a checkable unblock criterion, a `wont-do` status, a coordination state machine, and segregated models with independent review) and use the revised chain on the code change.

## Revisions made

- `decisions/task-states.md`: states (`ready`, `in-progress`, `in-review`, `escalated`, `blocked`, `done`, `wont-do`), transitions, required fields (a blocked task records `blocked_on`, `unblock_when`, `owner`; a `wont-do` task records the reason and the change that removed the need, proposed by the orchestrator and ruled by the ACE), an `ESCALATE-TO-ACE` form with typed questions, and the three segregation boundaries: workspace (local git worktrees), context (role instructions plus contract, no history), capability (pinned model; author and reviewer differ).
- `.claude/agents/reviewer.md` (Opus 5.5, read-only); orchestrator, contract template, CLAUDE.md, AGENTS.md and `next-passes.md` updated.
- `src/toaster/conformance.py`: five statuses with `reason` and `unblock_when`; a check on a model that fails language conformance is `blocked` (DL-025, superseding DL-024).

## What ran

Builder (Sonnet 5) implemented contract PASS2-004. An independent reviewer (Opus 5.5, a different model) reviewed the diff: PASS, 10 of 12 mutants killed, two surviving mutants (the schedule dropped from `blocked` and `wont-do` results), a formatting-noise flag, and one open question (an unscheduled check on a failed model). The question is answered by DL-025's wording, so no ACE call was needed. A second builder contract (PASS2-005, tests only) closed the gaps; the orchestrator re-ran the reviewer's mutation harness: 12 of 12 killed. Integrated after the blast zone, suite (102 tests) and ruff checks.

## Findings about the chain

- **Independent review earned its place.** The reviewer used mutation testing on the builder's tests and found real gaps that the builder's own report and my re-run of the tests missed.
- **Route only real judgments to the ACE.** The reviewer's open question was already decided by Z's ruling, so the orchestrator applied it rather than escalating.
- **Formatting noise.** The builder ran `ruff format` over unrelated lines in both files. It stayed inside the blast zone, so it was accepted, and the follow-up contract forbade reformatting. Future contracts should say "do not reformat existing lines".
- **Repo-wide `ruff check .` reports 79 errors** in notebooks and other files that predate this work; acceptance criteria are scoped to the changed files.
