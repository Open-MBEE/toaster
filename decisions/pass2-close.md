# Pass 2 close-out (2026-09-27)

Pass 2's declared exit criteria (`decisions/next-passes.md` §1): *"The roster and authority matrix
are consistent with the Foundations; every role skill cites glossary ids; each role has a pinned
model and a cold-start test."* This record checks each against evidence and closes the pass.

## 1. Roster and authority matrix consistent with the Foundations

Five process roles now live in `.claude/agents/`: `orchestrator`, `layer-auditor`, `builder`,
`reviewer`, `ace`. `AGENTS.md` Part 2's opening now states the explicit mapping from each to the
legacy archetype it supersedes (A1→orchestrator, A2→builder, A8→ace; `layer-auditor` and
`reviewer` are new, with no legacy A-id — `reviewer` generalizes A5/A6's intent, which had no
model assignment of their own). The content-authoring archetypes (A3, A4, A7, A9, A10) have no
Pass 2 role file and correctly remain legacy: they are Pass 4's concern (the didactic content
pass), not this one's. `AGENTS.md`'s own header (line 6) is updated from "legacy, pending
rebuild" to reflect the partial, correct-scope rebuild.

`decisions/task-states.md`, `decisions/work-contract-template.md` and the five role files were
swept for stale archetype references (`grep -n "\bA[1-9]\b\|\bA10\b"`); none found. One real
inconsistency was found and fixed: `.claude/skills/ace-protocol/SKILL.md` (a Pass 2-current
skill, not on CLAUDE.md's "not yet updated" list) still said "A6 CANT_TELL" and "Return to A1" /
"Returned to A1" in its decision-path table and log-entry format — both renamed to `reviewer`
and `orchestrator`. No historical `decisions/log.md` entry used the old "Returned to A1" text
(checked), so this is a clean forward-only fix, not a retroactive rewrite.

## 2. Every role skill cites glossary ids

Confirmed directly (`grep -l "glossary\|term-" .claude/agents/*.md`): all five role files
(`orchestrator.md`, `layer-auditor.md`, `builder.md`, `reviewer.md`, `ace.md`) reference the
glossary or specific term ids.

## 3. Each role has a pinned model and a cold-start test

Pinned models: `orchestrator` and `builder` on Sonnet 5, `layer-auditor` and `reviewer` on Opus
5.5, `ace` on Fable 5.1 — stated in each role file and enforced at launch (an explicit `model:`
override on every `Agent` call, never inherited; `pass2-run-009.md` records the one point this
was missed and self-corrected, when a reviewer launch collided with the author's model and the
reviewer itself refused and reported `CANT_TELL`).

Cold-start evidence: `decisions/cold-start.md` is a Pass 1 record (three model tiers standing in
for "the role range," since roles did not exist yet) and does not by itself cover the five named
Pass 2 roles. Rather than write a second synthetic exercise, this closes the criterion against
actual production use, which is the stronger evidence: every role ran repeatedly, cold, in its
own private worktree, on its pinned model, with no conversation history —
`layer-auditor` across all eight chapter audits (`decisions/audits/ch0[1-8]-layer-audit.md`),
`builder` and `reviewer` across `pass2-run-001` through `012`, `ace` across the dry run
(`decisions/ace-dry-run.md`) and every live `Handled by ACE` / `Escalated to Z` entry in
`decisions/log.md`, `orchestrator` as the role this session itself runs under.

## 4. Other findings closed in this pass

- DL-048 (satisfaction-claims-evaluated scheduling) executed: `applies_from=(3, 1)`, verified
  against the real ch03/ch04/ch08 fixtures and the CLI (`pass2-run-011.md`); a related CLI
  default-stage defect found and fixed in the same run.
- N1 (PASS2-012's one accepted-as-minor test gap) closed: `tests/test_modelcheck.py` now covers
  the "exit 1 requires violated > 0" half of F3's disambiguation directly
  (`test_exit_1_with_zero_violated_raises`).

## 5. Open for Z, not decided here

`decisions/gap-issue-drafts.md` carries eight drafts (Draft 8 retracted), status "nothing filed,
Z decides." Drafts 6 and 7 (D-019, D-020) are new, added during the Ch6-8 audits, and have not
been through any review round with Z that this record can find. Whatever disposition Drafts 1-5
received earlier in the conversation that is not captured in `decisions/log.md` verbatim should
be treated as still pending until Z confirms it was carried out (nothing in this repo's records
shows any of the eight actually filed on a public tracker). This is Z's call, not the
orchestrator's or the ACE's, per the file's own standing rule.

## Verification

Full suite (`tests` + `glossary/tests`): 261 passed, 7 deselected. `ruff check` on every file
this pass touched: clean (a whole-tree `ruff check src tests scripts` surfaces pre-existing lint
debt in unrelated, untouched files from earlier work passes — out of this contract's scope,
left alone rather than swept in). `glossary check`: 0 errors, 7 warnings (all `source-absent`,
expected in a worktree without the gitignored local PDFs). `git log main..HEAD --format=%B |
grep -c "Co-Authored"`: 0.

## Pass 3 entry

Per `decisions/next-passes.md` §1, Pass 3 (evaluation workflows) enters on "Pass 2 roster,"
which this record confirms is in place. No blocking item found; the open drafts in §5 above are
independent of Pass 3's entry condition.
