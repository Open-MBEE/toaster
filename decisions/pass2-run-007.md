# Pass 2, run 007: language-gap guard and satisfaction-claims check (2026-09-27)

Contract PASS2-009, implementing DL-039. Builder Sonnet 5, reviewer Opus 5.5 (independent, different model each round), four review rounds.

## What shipped

`src/toaster/conformance.py` gained:
- `language_gap_findings(model)`: always-on (part of `language_conformance`, not staged), two rules — `allocate-between-definitions` (KerML 8.3.3.3.9: a ReferenceSubsetting's referenced element must be a Feature) and `part-typed-only-by-item-def` (SysML `validatePartUsagePartDefinition`) — each with a spec citation and a negative control. `_METACLASS_SUPERTYPES` treats ConnectionDefinition, InterfaceDefinition, AllocationDefinition, ViewDefinition and RenderingDefinition as satisfying "is or specializes PartDefinition" per SysML 7.26.1 and the abstract syntax (8.3), so the part-typed rule doesn't false-positive on legitimate SysML.
- `satisfaction-claims-evaluated`: a staged, unscheduled project check that evaluates every `SatisfyRequirementUsage` via `model.eval`, respecting `isNegated` (a negated claim is a finding when the expression is True, not False). A bare `satisfy` with no explicit subject is recorded distinctly ("not evaluated: no explicit subject") rather than silently dropped or falsely flagged.
- `report()`: per DL-039, any `gap_findings` blocks every non-wont-do project check symmetrically with `model.ok is False` (including unscheduled ones), with a reason naming the specific violated rule(s).

Applied against the real repo: ch05 to ch08 each show 2 allocation-end findings + 2 item-typed-part findings (matching the Ch5 audit); the satisfaction check flags `timely(slow)` (ch05+) and `heating(weak)` (ch06+), confirming the Ch3 audit's finding extends as expected. Nothing in the chapters or models was touched — Pass 4's job.

## Review rounds

1. Build: reported clean, but two commits carried co-author trailers (a first for this session's push-back history) and review found a real crash and two correctness bugs.
2. Round 1 review: FAIL. Trailers; `report()` crashed (KeyError) on models the base handled fine, because the always-on guard queried allocations unconditionally; `assert not satisfy` was evaluated backwards (inverted true/false); the item-typed-part rule flagged valid SysML (connection/interface/allocation defs, deep specializations).
3. Push-back: history rewritten to strip trailers; guard made ok=True-only with per-element fault tolerance; negation logic fixed; rule switched to a specialization-closure check.
4. Round 2 review: FAIL, narrower. Two new false positives (`view def`/`rendering def`, both genuinely part-definition kinds per spec — verified against the spec text before pushing back) and a test gap that let the `model.ok` guard regress invisibly (the existing tests used a not-ok model with no gap constructs in it, so removing the guard entirely still passed).
5. Push-back: table extended, guard pinned with a not-ok model that actually contains gap constructs.
6. Round 3 review: PASS, with one minor, non-blocking survivor (a `break` vs `continue` mutant in a defensively-coded branch that no real SysML can reach). Integrated as is; recorded here rather than spinning a fourth round.

## What the run showed

- **Trailers slipped through once.** All prior runs' commits were clean; this is the first regression. Push-back mechanics (rebase, not just amend) worked to fix history mid-branch.
- **"Always-on" checks need an explicit ok-gate, and that gate needs a test that actually exercises the gated behavior**, not just a model that happens to produce an empty result either way. The reviewer's mutation testing found this precisely because it tests behavior, not code coverage.
- **Verify spec citations yourself before accepting a push-back item as fact.** Before instructing the fix for F7 (view/rendering defs), the orchestrator independently confirmed the spec text (§7.26.1) rather than trusting the reviewer's uncited claim — this matters because a wrong "fix" here would have introduced a false negative in a conformance check.
- **Cost:** four builder passes, four review rounds, roughly 900k subagent tokens total — expensive for a ~90-line production diff, and proportionate given it's conformance-checking infrastructure that Pass 4 will depend on for correctness, not cosmetics.

## Known minor gap (not blocking)

`satisfaction_claims_evaluated`'s `if not requirement: continue` branch: a mutant changing `continue` to `break` survives, because the one test covering it patches in a single-entry list. Fix (cheap, next time this file is touched): extend that test's patched data to include a second, evaluable claim and assert it still produces a finding.
