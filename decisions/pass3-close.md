# Pass 3 close-out (2026-09-27)

Pass 3's declared exit criterion (`decisions/next-passes.md` §1): *"Evaluations run on the pinned
models and produce reports the ACE can triage."* Pass 3's declared scope names five items; this
record checks each.

## What was already done, ahead of schedule

Three of the five scope items were built during Pass 2 and confirmed still in force, not rebuilt
here:

- **Glossary `check` in CI** — `run_check()` has 26 tests in `glossary/tests/test_check.py`,
  running via CI's `pytest tests/ glossary/tests/`.
- **Skill-snippet tests in CI** — `tests/test_skill_snippets.py` executes the `opensysml-query`
  recipes and `architecture-layers`' example model against real fixtures, in CI.
- **Prose lint against confirmed definitions** — `glossary/lint.py` (contract PASS2-007, DL-028,
  DL-029): rule table in `lint_rules.toml`, count-based baseline, CLI text/JSON output, 20 tests,
  in CI.
- **Layer audit** is proven, not just designed — the `layer-auditor` role ran for real across all
  eight chapters in Pass 2. `decisions/next-passes.md` now records it as the standing tool Pass 4
  reuses; no new construction was needed.

## What Pass 3 actually built

**`user-testing` had three real contradictions with the system Pass 2 built**, found while
reading it in full rather than assuming it was current:

1. Its execution checklist asked the learner to check whether a cell "names all three worlds" —
   exactly backwards from AGENTS.md 1.10's binding rule (never name Tall or the three worlds),
   which the Pass 2-built `tall-named` lint rule (DL-028) already enforces.
2. Its "what counts as blocking" list repeated the same inversion.
3. Its ACE synthesis protocol had the ACE "fix blocking issues... inline" — directly contradicting
   `ace-protocol`'s current, binding rule that the ACE never edits repository files and the
   orchestrator dispatches fixes.

All three fixed in `.claude/skills/user-testing/SKILL.md`. The Tall-seam checklist item now asks
the question a lint rule cannot answer: is the seam (model text, tool, rendered output)
*addressed in behavior*, without ever naming the lens. Legacy `A9`/`ACE-spawns`/`WP` references
replaced with the current roster and vocabulary (chapters, not work packages).

**New role: `.claude/agents/simulated-learner.md`.** Pinned per persona per the skill's table
(Haiku 4.5 Novice, Sonnet 5 SE Practitioner and Returning Learner — a simulated novice should not
out-capability the learner it stands for). `AGENTS.md` Part 2's supersession mapping updated to
include it (A9 Simulated Learner → `simulated-learner`).

## The dry run

Two `simulated-learner` agents (Novice/Haiku, SE Practitioner/Sonnet) ran
`chapters/ch01-system-purpose/01-abstract-def.ipynb` (plus its index.md/conclusion.md) for real —
actually executing cells, not describing expected output. **First attempt used the Agent tool's
built-in `isolation: "worktree"`, which checked out a stale commit (`ef4744d`) predating the
entire Foundations rewrite — no AGENTS.md Part 1, no glossary CLI.** This is the exact failure
mode Pass 1's `decisions/cold-start.md` already documented and warned against ("create the
worktree yourself... do not rely on default isolation"); it was reintroduced here by not
following that recorded lesson. The SE Practitioner (Sonnet) noticed and flagged the broken
environment explicitly, unprompted, and refused to treat its own report as representative; the
Novice (Haiku) did not notice at all and reported a clean PASS regardless — a real finding about
model-tier diligence under a broken environment, not just a process hiccup.

Redone correctly: worktrees created manually (`git worktree add <path> HEAD`), no `isolation`
parameter, both agents told to `cd` into the given path and stay there. Both reports landed
clean, PASS overall, reports at `decisions/dryrun/pass3-learner-novice-ch01.md` and
`decisions/dryrun/pass3-learner-practitioner-ch01.md`.

**ACE synthesis (Fable 5.1)** reproduced every execution result independently, ran its own fresh
notebook (nb02) per the protocol, probed two of the practitioner's claims against the real
toolchain rather than taking them on faith, and triaged five items to zero blocking. The most
substantive: both personas independently flagged the same thing — a seam cell tagging its three
elements "(A-F)", "(O-S)", "(E)". These are Tall's own three-worlds vocabulary under abbreviated
names, required by three skills (`toaster-recipe`, `sysml-v2-toaster-model`,
`tutorial-style-guide`) as a mandatory per-notebook pattern, and **invisible to the `tall-named`
lint rule** (its regex, `\b(?-i:Tall)\b|\bthree[\s-]+worlds\b`, cannot match any of the three
abbreviations — verified against `glossary/lint_rules.toml` directly). This is not a new gap: it
is exactly the recipe-versus-rule contradiction Pass 1's DL-015 already flagged and parked for
Pass 4's recipe rewrite, and DL-028 already recorded as a not-decided Pass 4 input. The ACE
declined to widen the lint or rule on it now, reasoning that doing either would decide the parked
question by regex ahead of the recipe rewrite that is supposed to decide it — and logged the
learner evidence for that rewrite instead (DL-050). Full reasoning and provenance, independently
spot-verified by the orchestrator (DL-003, D-004, the lint regex) before commit: DL-050,
`decisions/log.md`.

**What the dry run demonstrated**, which is the actual point of Pass 3, not a chapter verdict
(Pass 3 does not gate content; Pass 4 does):

- The mechanism produces format-conformant, evidence-backed, sub-400-word reports on the models
  it says it will, and the ACE can reproduce and triage them without taking anything on faith.
- The Novice/Practitioner split surfaces different kinds of findings at appropriate depth for
  each persona's pinned model (the Novice flagged confusion; the Practitioner traced two claims
  to their actual root cause in the toolchain).
- The behavioral Tall-seam judgment catches what the literal-naming lint rule is designed not to
  see — the two evaluation mechanisms are complementary, not redundant, confirmed by neither
  learner flagging the already-tracked layer-vocabulary defects that are `layer-auditor`'s job
  instead.
- A known, previously-documented environment failure mode recurred and was caught, corrected, and
  is now doubly on record.

## Verification

Full suite (`tests` + `glossary/tests`): 261 passed, 7 deselected (unchanged — this pass touched
no chapter, model or conformance code). `ruff check` on every file this pass touched: clean.
`glossary check`: 0 errors, 7 warnings (all `source-absent`, expected without the gitignored
local PDFs). `git log main..HEAD --format=%B | grep -c "Co-Authored"`: 0. All dry-run worktrees
and branches removed.

## Pass 4 entry

Per `decisions/next-passes.md` §1, Pass 4 (didactic content) enters on "Pass 3," which this
record confirms is in place: the evaluation machinery is built, proven on real content, and its
one substantive finding (the seam-label contradiction) is already correctly filed as a Pass 4
input rather than decided out of turn.
