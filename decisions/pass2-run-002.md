# Pass 2, run 002: a builder that edits files (2026-09-26)

Purpose: exercise the second subagent kind, one that changes code and tests, and the integration path with independent verification. Role file: `.claude/agents/builder.md` (Sonnet 5, effort high, pinned).

## What ran

1. **Contract PASS2-002** (orchestrator): implement the two-tier conformance model (AGENTS.md 1.9) as `src/toaster/conformance.py` with tests, blast zone two files, no design decisions (which chapter a check first applies from stays unscheduled). The builder ran cold in its own worktree on Sonnet 5.
2. **Builder** verified its three premises, wrote tests first, and reported the full output of every check. It stayed inside the blast zone and raised no questions.
3. **Orchestrator verification** (not trusting the report): diff limited to the two contracted files; no co-author trailers; full suite 90 passed and ruff clean on integration; then a probe the contract had not covered.
4. **Defect found by the orchestrator, not the builder:** with a model that fails language conformance (`part def A :> Missing;`, `ok False`), a scheduled project check returned `passed`. The contract had not specified this case, so the builder implemented it faithfully.
5. **ACE** (Fable 5.1, launched by name) ruled: project checks report `open` with a recorded reason, no fourth status, extension flagged (DL-024).
6. **Contract PASS2-003** (builder, Sonnet 5): implement DL-024. Orchestrator re-verified (blast zone, 92 tests, ruff) and integrated.

## Findings about the chain

- **The edit-and-integrate path works.** Blast zone held twice, tests were written with the code, reports carried real command output, and independent verification caught a gap the report could not have (an unspecified case).
- **A contract gap is the orchestrator's to close.** The defect was in what the contract did not say. The orchestrator should probe boundary cases (failed language conformance, empty input, unscheduled) before accepting, and add them to the next contract.
- **Launch by name.** `layer-auditor` and `ace` launched by name reported `claude-opus-5-5` and `claude-fable-5-1`: the role file's `model` field is honored. A role file created during a session (`builder`) was not launchable by name until the harness reloads, so it was launched through a general-purpose agent with the model pinned explicitly. Restart the session to pick up new role files.
- **Same-model review is weak.** Both builder runs and the orchestrator ran on Sonnet 5. The independent verification above was the orchestrator running the code, not re-reading it; a later pass could route builder output to a reviewer on another model.
- **One judgment came up and was routed correctly**: the builder did not decide the status semantics; the orchestrator did not decide them either; the ACE did, with an extension flag for Z.

## Open for Z

DL-024 extends "open until applied" from staging to a precondition failure. If you would rather the status field itself say why (a `blocked` status), only the status vocabulary changes.
