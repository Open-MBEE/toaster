# Pass 4, run 008: Chapter 8 re-derivation (2026-09-28)

Contract PASS4-008. Builder Sonnet 5, reviewer Opus 5.5 (independent, different model), three review
rounds plus a fourth, narrow round applied directly by the orchestrator. Executes
`decisions/audits/ch08-layer-audit.md` against DL-018, DL-023, DL-030 through DL-039, and especially
DL-046 through DL-049, the four late entries that resolved every open question the audit raised. The
chapter that delivers real formal model checking for the first time in this tutorial, using a toolchain
capability (sysml-toolkit's `verify --solve`, via Z3) this pass had already built a wrapper for
(`src/toaster/modelcheck.py`, DEFERRED.md D-025) but never actually used in a chapter until now.

## What shipped

- **Mandatory rebase, and a much bigger ripple than any prior chapter's.** `models/ch08-cumulative.sysml`
  at HEAD was a byte-copy of the *stale* ch07 fixture with only the provenance comment edited (the
  audit's F-1). Rebuilt on the real, current `ch07-cumulative.sysml`. This exposed the audit's own F-7
  warning as accurate: ch08 was "the repository's most-referenced fixture," and two test files
  (`tests/test_query.py`, `tests/test_conformance.py`) hardcoded assumptions about its stale schema.
  Fixing this required widening the contract's blast zone mid-round to those two files (approved by the
  orchestrator after independently reproducing the 11 broken tests), while a third file
  (`tests/test_skill_snippets.py`, which executes the `opensysml-query` skill's own documented snippets)
  was ruled to stay explicitly failing and tracked (`decisions/next-passes.md` item 17), since fixing it
  requires the skill-editor protocol, outside builder or orchestrator authority to invoke unilaterally.
- **F-3/F-4 (already fixed upstream, confirmed not re-broken).** The false-satisfy pattern the audit
  found (`assert satisfy timely by slow`, `assert satisfy heating by weak`) was already corrected by
  Chapter 3 and Chapter 6's own re-derivations (`assert not satisfy`, folded into each usage's own
  context, no `evidence`/`heatingEvidence` container). Verified directly against the real model rather
  than assumed from the audit, which read a stale fixture.
- **DL-046/DL-047 (the core substantive addition): a real, genuinely non-trivial formal property, proved
  by Z3.** `assert constraint deliveredEnergyBoundedBySupply`, stating that a bounded efficiency
  together with the delivered-energy relation entails conservation for *every* value in the bound, not
  just the one instance (`rated`, 0.7) Chapter 7 happened to check. Confirmed non-trivial by the reviewer
  in every round: the property flips to `undecided` when its own stated hypothesis is dropped, and a
  deliberately false entailment (`e<=0.5 implies e<=0.4`) correctly comes back `undecided`, not a false
  `satisfied`.
- **The most consequential finding of the whole run, discovered in round 1 review and confirmed
  irreducible in round 2: the proved property could not actually be tied to the model's real
  `efficiencyBounded`/`deliveredEnergy` elements.** See below.
- **A real negative control and a real "undecided" demonstration.** A full negation of the property
  (`A and not B`) is correctly reported `violated`; a realistically weakened variant (the bound loosened
  from 1.0 to 1.2, the same edit Chapter 8's own staleness demo already used) is correctly reported
  `undecided` with a genuine Z3 witness, and `holds()` correctly raises `ModelCheckInconclusiveError`
  rather than answering a false `True` or `False`.
- **`verify_satisfaction()` and `verify_holds()` kept sharply, honestly distinguished throughout**, per
  DL-046(1)'s framing: the former stays "observed," point-evaluation of the model's three real
  `assert satisfy`/`assert not satisfy` claims (unchanged in substance from earlier chapters); the latter
  is a genuine universal proof, and only it earns words like "proves" anywhere in the chapter.
- **F-5 (the judgment record rebuilt on real, non-circular evidence).** The old `AS-C08`/`AS-C08-REV`
  records assumed `assert satisfy timely by nominal`, which does not exist in the real model at all.
  Dropped both; built one new record grounded entirely in the new formal property's Z3 proof.
- **Two new toolchain gaps found and logged: D-029, D-030, D-031.** D-029: `modelcheck.py`'s line parser
  cannot read a verdict for any constraint that's also the subject of an `assert satisfy`/`assert not
  satisfy` declaration (forcing a companion-file restatement rather than running `verify_holds` directly
  against the real committed model). D-030 and D-031, found during the fight to fix F-1 (below): two
  independently-declared `assert constraint`s (sibling or inherited) are never composed by `verify
  --solve`, and a chained calc/function invocation is not in Z3's solvable fragment.

## The proved-property linkage problem: what it took to find, and what it took to accept

1. **Round 1 review found the defect that mattered.** The reviewer didn't just read the property; it
   adversarially probed whether the "proof" actually depended on the real model elements it claimed to.
   Loosening the real `efficiencyBounded`'s bound to 1.5, or doubling the real `deliveredEnergy`'s own
   definition, left the new construct's verdict unchanged (`satisfied`) in both cases; it should have
   flipped if the link were real. The chapter's own claim, doc comment, and judgment record all said
   otherwise.
2. **The push-back required one more genuine attempt before conceding, not an immediate retreat to
   honest reframing.** A same-scope sibling `assert constraint` (declared directly inside `HeatGenerator`
   itself, alongside `efficiencyBounded`, using bare, non-dotted feature references) was the one
   plausible mechanism the round 1 diagnosis hadn't yet ruled out. It failed the same way: `undecided`,
   with a Z3 witness showing the solver treats each `assert constraint` as checked entirely on its own,
   never as an assumed-true premise for a different one, whether the second constraint is a sibling, an
   inherited member, or reached through a calc invocation.
3. **Once genuinely ruled out, the fix was honest reframing, not a workaround.** The claim, the model's
   own doc comment, and every chapter file were reworded to say precisely what's proved: a hand-restated
   real-arithmetic lemma "of the same shape as" the real elements, not a solver-checked reference to them,
   with the record's own `content_hash` staleness noted as a partial (not complete) mitigation. Two new
   `DEFERRED.md` entries record the actual solver-fragment limits found, each citing a real reproduction.
4. **Round 3 confirmed the fix, and the reviewer re-ran every one of the round 1 probes against the
   final model independently**, including the sibling-constraint attempt, before passing.

## Review rounds, in brief

1. **Build**, plus a mid-contract escalation: rebasing onto the real model broke 11 tests in 3 files
   outside the declared blast zone. The orchestrator independently reproduced all 11, then ruled a
   middle path rather than either extreme: widen the blast zone now for the 2 ordinary test files (9
   failures, genuinely fixable, several testing behavior that's "still correct, just against different
   qualified names"), and rule the 2 skill-snippet failures a deliberate, logged, tracked exception
   rather than something to fix without the skill-editor protocol.
2. **Test-suite fix round**: 9/9 fixed, each rewritten assertion checked against real behavior rather
   than weakened to pass (one genuinely required moving a code path's coverage to a standalone fixture,
   with the reasoning for why checked empirically, not assumed); `decisions/next-passes.md` item 17
   records the 2 tracked exceptions at real, checkable detail.
3. **Round 1 review: FAIL.** F1 (the linkage defect, described above) plus seven mechanical items: a
   mis-described negative control (claimed as the entailment's conclusion negated; actually the whole
   property's negation, a materially different and weaker-sounding but actually stronger check); a false
   claim about which verdict `satisfaction_claims_evaluated()` skips; D-029's own observed-behavior text
   being wrong in a way that would misfire if naively fixed; two test fixtures accidentally reintroducing
   known-bad language-conformance patterns; lost multi-hop test coverage; an unrecorded propagation-only
   "satisfied" false-confidence risk; and several stale/imprecise learner-facing details.
4. **Push-back and fix**: the sibling-constraint probe, the honest reframing, D-030/D-031, and all seven
   mechanical items, plus the two ruled open questions (a genuine "undecided" demonstration added; a
   one-paragraph contrast with Chapter 7's own sampled sweep, to actually deliver the model-checking/
   simulation complementarity AGENTS.md 1.1 item 5 promises).
5. **A small follow-up, ruled separately**: a nondeterministic tempfile path was breaking the standing
   fresh-execution-vs-committed-output diff. Fixed before dispatching round 3, independently.
6. **Round 3 review: PASS**, with four cosmetic notes.
7. **Applied directly by the orchestrator**: a machine-specific `/var/folders/...` scratch path in
   published notebook output (fixed to a repo-relative, portable path, re-executed, confirmed byte-for-
   byte reproducible both run-to-run and cell-by-cell against a second independent fresh run); an
   ambiguous "passes for the first time" claim that could be misread as this check's first pass anywhere
   in the tutorial rather than on ch08's own fixture specifically; two `language_gap_findings` assertions
   that existed only in docstrings, not as real test assertions; and two small factual slips (a
   "product of two" that is really three unbound features; a "both lines" introducing three examples).

## What the run showed

- **Adversarial probing of a "proof" is not optional, and a reviewer who only reads the claim will miss
  exactly the defect that matters most.** The chapter's own text, doc comment, and judgment record all
  consistently and confidently described the property as tied to the real model elements. Only actively
  trying to break the claimed link (loosen the bound, double the formula, and check whether the verdict
  moves) surfaced that it didn't. This is the same discipline Chapter 6's `GasBurner` counter-example and
  Chapter 7's do-action-removal probe already established, applied here to a genuinely new kind of claim.
- **A real toolchain limitation, once found, deserves one more good-faith attempt at a fix before
  conceding, but only one.** The sibling-constraint probe wasn't a stalling tactic; it was the one
  mechanism the diagnosis hadn't yet ruled out, and trying it (cheaply) either would have fixed the
  chapter's central claim or would confirm the limitation is real, not an artifact of one particular
  scoping choice. It confirmed the latter, and having tried made the honest-reframing fallback
  trustworthy rather than a shrug.
- **A test-suite ripple from a fixture rebase is not automatically the current contract's problem to
  fully absorb, and treating "fix everything" and "fix nothing, defer everything" as the only two options
  is a false choice.** Splitting the 11 broken tests by what kind of fix each actually needs (ordinary
  test-fixture staleness, fixable by an ordinary test file edit, versus a skill's own documented content,
  requiring a different protocol and a different sign-off) let 9 of them get fixed in the same round
  without either blocking the chapter's merge on a slower process or quietly overstepping into
  skill-maintenance authority the contract never granted.
- **A cosmetic finding can still be worth fixing directly rather than waved through as "good enough,"
  especially when the underlying property (reproducibility) is one this project has an explicit standing
  document about** (`docs/reproducibility.md`). A machine-specific absolute path in committed,
  published notebook output is a small thing on its own, but it's exactly the kind of small thing that
  compounds into "this reproduces on my machine" being quietly, silently false for anyone else's.

## Verification

299 tests passing, 2 known and explicitly tracked failures (`tests/test_skill_snippets.py`, DEFERRED to
the `opensysml-query` skill's own re-derivation, `decisions/next-passes.md` item 17), unchanged and
independently reconfirmed after every round including the orchestrator's own final direct-fix commit.
0 ch08-specific lint hits (24 before the rebuild, all closed as a byproduct of the rewrite; the remaining
64 repository-wide are pre-existing, in Chapters 9-10 and docs). `glossary check` clean. 0 co-author
trailers across 12 integrated commits (none needed stripping this run; every builder commit landed
clean). 0 em-dashes in every touched learner-facing and test file, including this run's own direct fixes
(one self-introduced em-dash in a new `.gitignore` comment was caught and fixed before commit).
`conformance.report` shows `satisfaction-claims-evaluated` reporting `passed` on ch08's own fixture for
the first time (already passing on ch03 through ch07; the wording was corrected mid-review to avoid
implying otherwise). Local book build clean; all three notebooks execute cleanly with real, non-empty
output. A byte-for-byte fresh-execution-versus-committed-output diff (per-cell concatenated text, the
correct comparison once a subprocess call's stdout/stderr interleaving with adjacent prints is accounted
for) confirmed zero content differences across all three notebooks before merge, including after the
final portability fix. Worktree and branch cleaned up after merge (`e1a3de6`).

## Not fixed here, carried forward explicitly

- **`tests/test_skill_snippets.py`'s 2 known failures.** The `opensysml-query` skill's own documented
  snippets are stale against the real, current model (a `Heater` part def that no longer exists;
  `HeatingSystem` no longer specializing `ToastingSystem`; an empty `FlowUsage` list where the recipe
  expects a non-empty one). Fixing this requires the skill-editor protocol and Z's sign-off, not builder
  or orchestrator authority. `decisions/next-passes.md` item 17 records the exact stale constructs and
  line numbers.
- **D-029 (the `modelcheck.py` parser gap), D-030 (assert constraints don't compose), D-031 (chained
  calc invocation unsolvable).** All three logged, none fixed; `src/toaster/modelcheck.py` and the
  underlying sysml-toolkit binary are both outside this contract's blast zone regardless.
- **`Toaster::cycleTime` staying a settable, underived attribute.** Unchanged since Chapter 5. The
  chapter's own `verify_satisfaction()` demonstration is explicitly captioned as illustrating evaluation
  mechanics on a not-yet-derived value, not a finding about the toaster's actual timing.
- **`.claude/skills/opensysml-api/SKILL.md`'s stale engine listing and `sysml-v2-toaster-model`'s stale
  A2/A4 chapter placement**, and `toaster-review-protocol`'s "two evidence paths" table still describing
  the old `verify_constraint(engine="check")` path rather than what this chapter now actually
  demonstrates. Confirmed still stale, reported, not fixed (skill edits outside every builder's ordinary
  authority, matching every prior chapter's own non-goal on this point).
- **`chapters/ch07-execution/conclusion.md`'s "What comes next" paragraph**, now stale in the other
  direction (it undersells Chapter 8 as only doing `verify_satisfaction()`). Outside this contract's
  blast zone; flagged for whoever next touches Chapter 7's own files.
- **Whether Chapter 9's realizer/coverage queries will pick up `heatGenCheck` (proof scaffolding, not a
  design candidate) as a `HeatGenerator` realizer.** A real forward-looking question, not this contract's
  to answer; `decisions/next-passes.md` item 19.
- **Whether `query.allocations_for`'s `inherit=True` code path has any conformant trigger anywhere in the
  tutorial's own real chapter models.** Checked directly: it does not, as of ch08. Recorded as an
  observation (`decisions/next-passes.md` item 18), not a defect.
