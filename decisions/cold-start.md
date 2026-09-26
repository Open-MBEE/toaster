# Cold-start test, Pass 1 (2026-09-26)

Purpose: a fresh session, given only `CLAUDE.md`, must reach working alignment from AGENTS.md Part 1, the skills and the glossary CLI, on every model tier the eventual roles may use. Each agent had a private git worktree of this branch (HEAD `ede5dae`, so the glossary and new skills were present, the gitignored PDFs absent), a pinned model, and read-only instructions. Tiers stand in for the role range (roles do not exist yet): **Haiku 4.5** (the novice), **Sonnet 5** (a routine builder), **Opus 5.5** (a judgment-heavy reviewer). The ACE itself is tested separately on Fable 5.1 (`decisions/ace-dry-run.md`).

A first attempt used the harness's built-in worktree isolation. Those worktrees were created from an older commit (`ef4744d`) with no glossary, so the Sonnet run there could not reach the glossary and the other two were stopped. Lesson recorded: create the worktree yourself with `git worktree add <path> HEAD` and pass its path; do not rely on default isolation to start from the current branch.

## Task and key

A. `glossary check` passes in a worktree without the PDFs. B. Classify seven statements. C. Does OpenSysML diagnose a power-to-fuel port connection (no, G4). D. Which source defines logical as "how" (none: Douglas says "who", SEBoK's logical includes the functional view; the tutorial's bridge edge is the "how" reading, a Z-approved differsFrom). E. Can a MoP be "a requirement" (no: it characterizes a requirement; a threshold and a means of checking complete it). F. Steps before a workaround (gap-tracking rule). G. May you hand-edit glossed text; who changes a confirmed definition (no, generated; only Z). H. What was confusing.

Key for B: 1 functional (MoE); 2 logical (mechanism plus interface); 3 physical; 4 physical TPM and emergent result (either label accepted, with the reason); 5 functional (solution-independent balance); 6 invalid (a prescription tested against a threshold); 7 logical (MoP threshold).

## Results

| Tier | A | B (7 items) | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| Haiku 4.5 | ok, exit 0 | 7 of 7 | correct | correct | correct | correct | correct |
| Sonnet 5 | ok, exit 0 | 7 of 7 | correct | correct | correct | correct | correct |
| Opus 5.5 | ok, exit 0 | 7 of 7 | correct | correct | correct | correct | correct |

`glossary check` reported `ok (0 errors, 7 warnings)` in every worktree: the seven warnings are "source file absent" for the gitignored PDFs, as designed. All three tiers cited AGENTS.md sections, skills and glossary term ids for their reasons. No tier failed, so the Foundations do not depend on more capability or context than a cold Haiku session has, for this task.

## What the agents found confusing, and what was done

- **Item 4 fits two labels** (physical TPM and emergent result). The `architecture-layers` skill now says a TPM is both: physical when asked for a layer, an emergent result when asked whether it was prescribed. Fixed.
- **Cannot find "measure of performance" by name.** `lookup` and `tutorial` matched only the full label with its parenthetical. Terms now resolve by the label without the parenthetical or by the abbreviation (`MoP`). Fixed, with a test.
- **How to reach the ACE** was unclear to a contributor outside the legacy roster. AGENTS.md 1.11 now says: through the orchestrator, or, with none, state the question and a recommended default in your report. Fixed.
- **Part 2's authority matrix versus Part 1** (who may edit AGENTS.md or glossary files; A8's skill authority): known, Part 1 governs, roster rebuild is Pass 2. Recorded as an input in `decisions/next-passes.md` (step 12).
- **Tutorial edge locators** still read "Foundations (AGENTS.md Part 1, to be written at gate M2)". To fix now that Part 1 exists (next commit).
- **The tongs-and-flamethrower Douglas timestamp** is unverified. Re-verify in Chrome before a skill cites a time.
- **Skills not yet updated** (`toaster-recipe` still names Tall; and others) are listed in CLAUDE.md as stale where Part 1 governs. Pass 2 and 4 inputs.
- **Gap status is spread over several files.** `DEFERRED.md` entries and the issue drafts (step 11a) become the single register.
- One agent reported an "older CLAUDE.md" in its session context that differed from its worktree copy. That is the harness loading the original checkout's project instructions, not a repo defect; the worktree copy was the one it followed.
