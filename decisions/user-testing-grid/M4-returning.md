# Grid cell M4-returning — local clone exercise, Returning Learner persona, Chapter 10

## First-run-unmodified result (required, separate from the fill-in attempt)
Ran `exercises/ch10/exercise.ipynb` exactly as committed via `uv run jupyter nbconvert --to notebook --execute`. Cells 0-1 (markdown) render fine. Cell 2 (first code cell) raises `AssertionError` at `assert model.ok, ...`: `source = """\n# Your solution here\n"""` is not valid SysML, so `conn.load_from_content` returns `model.ok=False` with diagnostics `(line 2) expected '{' or ';' after declaration` / `(line 2) expected a namespace member`. Execution stops there; cells 3-59 never run. This is consistent with a deliberate "fill in the blank" exercise, not a genuine bug: the placeholder is an obvious comment, the assertion message names exactly what's missing ("source is missing CoffeeDemo::deliveredMassBoundedBySupply -- paste your full Chapters 1-8 model"), and every other exercise chapter (checked ch06, ch09) uses the identical `"""\n# Your solution here\n"""` pattern with no committed solution anywhere in the repo.

## Fill-in attempt
As Returning Learner I do not have a real saved Chapters 1-8 coffee-maker source (nothing is committed for any exercise chapter — checked ch01-ch09, all are unfilled placeholders too). I reconstructed a plausible Chapters 1-8-equivalent model from scratch, mirroring `models/ch08-cumulative.sysml`'s structure 1:1 into the coffee domain using the exact construct names the exercise notebook itself discloses (`CoffeeDemo`, `BrewUnit`, `BrewAssembly`, `WaterMover`, `Impeller`, `rated`/`weak`, `brewReq`, `tempCheck`, `deliveredMassBoundedBySupply`, `BrewStart`/`BrewCancel`). It loaded (`model.ok=True`), and Step 1's query helpers worked correctly for `brewReq`: `requirement_subject` found `wm:WaterMover`, `allocations_for`/`supertypes_transitively` traced the allocation and realization chain, and `requirement_coverage` returned the expected bidirectional result (`satisfied_by=['rated']`, `failed_by=['weak']`), matching Chapter 10's real shape exactly. `tied_to_any_requirement` correctly returned `False` for my lemma, matching the gap the real chapter finds. I hit a genuine snag on `tempCheck`: my `assert not satisfy tempCheck by hot.brewUnit;` (targeting a nested feature path) produced `failed_by=[]` instead of `['hot']` — `requirement_coverage()` apparently expects the asserted subject to be a top-level part usage, not a dotted path, which nothing in Chapters 1-9's own material states explicitly. I stopped there rather than fabricate chapters 1-9 state I never actually built.

This does feel like real capstone synthesis in structure — it genuinely requires every prior chapter's constructs (actions, perform, allocation, requirements, verification, state machines) working together — but in practice its biggest cost is not conceptual synthesis, it's that nothing carries forward automatically between exercise notebooks: a returning learner must have manually preserved their own full model text across nine prior sessions, with zero scaffolding or checkpoint file in the repo to recover it from.

## Structured findings
- id: M4-returning-01
  severity: positive
  location: exercises/ch10/exercise.ipynb cell 2
  quote: "assert model.ok, f\"Model failed: {format_diagnostics(model.diagnostics)}\""
  expected: unmodified placeholder fails with a diagnostic pointing at what's missing.
  actual: fails exactly as expected, with a clear message naming the missing construct; not a bug.
- id: M4-returning-02
  severity: friction
  location: exercises/ch10/exercise.ipynb cell 2 / Problem section
  quote: "paste your own full, completed Chapters 1-8 coffee-maker model as source"
  expected: a returning learner can proceed from what Chapters 1-9 taught.
  actual: proceeding requires a full, self-preserved copy of 8 prior chapters' model text that the repo never checkpoints anywhere; nothing here is recoverable if that copy is lost.
- id: M4-returning-03
  severity: confusing
  location: exercises/ch10/exercise.ipynb Step 3 (ch06_source_pre_impeller / ch06_source_final)
  quote: "Step 3 asks for TWO ch06-stage placeholders... do not collapse them into one shared placeholder"
  expected: one accumulated model carried forward, consistent with how chapters build.
  actual: requires separately preserving two distinct intermediate states from chapter 6 alone, on top of the full chapters 1-8 model — a bookkeeping burden with no tooling support.
- id: M4-returning-04
  severity: positive
  location: Step 1 query cells (requirement_subject, allocations_for, requirement_coverage)
  quote: "satisfied_by=['rated'], failed_by=['weak']"
  expected: query helpers work the same way against a freshly-authored coffee-maker model as against the toaster.
  actual: worked correctly on the first attempt for brewReq, confirming the helpers genuinely generalize.

## Overall
NEEDS-FIX (process/scaffolding, not content) — the unmodified notebook fails exactly as a fill-in-the-blank should; the capstone's real difficulty is that no exercise chapter ever checkpoints a learner's accumulated model, forcing a returning learner to reconstruct or preserve nine chapters of state entirely outside the repo's own support.

---
Branch: worktree-agent-a017a9d55e4d4e1eb (worktree off main, contract specified user-testing/browser-pass1; this worktree's actual branch lineage did not include that branch — see note below)
Model run on: Sonnet 5 (matches contract and the user-testing SKILL.md persona table for Returning Learner)
Could not execute: full Steps 2-4 of the fill-in attempt (remediation, judgment ledger, synthesis record) — stopped after Step 1 surfaced a real coverage-query snag on tempCheck, to avoid fabricating chapters 1-9 state never actually built. Also note: `docs/superpowers/specs/2026-10-01-large-scale-user-testing-design.md`, which this contract cites, does not exist in this worktree's branch history (only on `user-testing/browser-pass1`, not an ancestor of this worktree's base); I read its M4 row via `git show 6d404b1:...` instead of a local file read.
