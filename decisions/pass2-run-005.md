# Pass 2, run 005: vocabulary lint, three review rounds (2026-09-26)

Contract PASS2-007: `uv run python -m glossary lint [--json] [--baseline FILE] [--write-baseline FILE]`, rules in `glossary/lint_rules.toml`, scanning learner-facing markdown (chapter notebook markdown cells, chapters/**/*.md, docs/**/*.md except the generated glossary page). Builder Sonnet 5, reviewer Opus 5.5, ACE Fable 5.1; roles launched by name, models confirmed.

## Rounds

1. **Build.** Delivered with 25 tests; the real-repo run produced the first vocabulary backlog (below). The builder disclosed its own baseline weakness (set-based matching).
2. **Review 1: FAIL.** A rules-file type error exited 1 with a traceback (breaking the contract's exit 2), two tests claimed coverage they lacked (the rule id in the baseline key; string-source notebook cells, 51 in the real content), and two rule-breadth questions came up. The orchestrator resolved the contract-level ones itself (count-based baseline, because the contract's purpose is "exit 1 only on a NEW hit"; fail closed on an empty rule set) and sent the breadth questions to the ACE (DL-028, DL-029).
3. **Push-back 1**, then a small change (hyphenated "three-worlds").
4. **Review 2: FAIL.** A test regression introduced by the count-based change (the file component of the baseline key no longer discriminated) and a non-UTF-8 rules file that still crashed. Both were small; the orchestrator re-ran the reviewer's 64-mutant harness itself after the fix.
5. **Push-back 2**, then integrated: 174 tests, ruff clean, all mutants killed, `check` passes, no co-author trailers.

## What the run showed

- **A change can weaken the tests that guarded the old behavior.** The count-based baseline was correct, and the test that claimed to check the file key stopped checking it. Mutation testing caught it; a re-run of the same tests would not have.
- **"Never a traceback" is a class of cases, not a list.** The contract enumerated the bad rules files; the reviewer found two more (type errors, non-UTF-8). Contracts should state the invariant and ask for it to be tested across input classes.
- **The orchestrator closes contract gaps; the ACE closes judgment gaps.** Count-based baseline and fail-closed were applied by the orchestrator (they follow from stated purposes); the two questions about what counts as a violation went to the ACE with extension flags for Z.
- **Cost:** three builder passes and three reviews for a rule-driven lint. Mutation-driven review is the expensive part and the reason for the low escape rate.

## First vocabulary backlog (real repo, 8 error hits; none edited)

- 6 x `tall-named`: the "Tall seam (stub)" cells (cell 5) in ch09 01-03 and ch10 01-03.
- 1 x `concept-selection`: ch05-architecture/index.md line 13 ("Concept Selection").
- 1 x `stale-physical-layer`: ch01-system-purpose/index.md line 26 ("physical architecture layer").
- Not lint hits, recorded as Pass 4 inputs (DL-028, DL-029): about 64 seam cells in ch01 to ch08 use world labels A-F and O-S; ch01 conclusion.md line 9 ("The structure is implementation-agnostic").

## Known gaps

A rule regex that can match the empty string is not rejected; unknown keys inside a rule are ignored (every field is required, so a misspelled required field fails); a malformed notebook whose cell source is neither string nor list would raise. The lint is not wired into CI (a non-goal; CI wiring is a Pass 3 item, and a baseline file for the 8 known hits should be committed when it is).
