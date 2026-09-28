# Pass 4, run 003: Chapter 3 re-derivation (2026-09-27)

Contract PASS4-003. Builder Sonnet 5, reviewer Opus 5.5 (independent, different model), two review
rounds plus non-blocking polish applied at merge. Executes `decisions/audits/ch03-layer-audit.md`
against the already-ruled decisions (DL-018, DL-022, DL-023, DL-030, DL-032, DL-033, DL-035,
DL-039, DL-048) — same pattern as PASS4-001 (Ch1) and PASS4-002 (Ch2).

## What shipped

`models/ch03-cumulative.sysml` needed the same rebase PASS4-002 predicted would reappear here: the
fixture was stale, still carrying Chapter 1's *pre-rederivation* content (an 800 W `Heater`
default, `HeatingSystem`/`ControlSystem` not specializing `ToastingSystem`, a defaulted
`cycleTime`, no `Bread`/`Toast`/`ToastBread`). The builder rebased onto the current
`ch02-cumulative.sysml`, then applied Chapter 3's own fixes on top:

- **F-1/OQ-1 (DL-035, DL-022)**: `timely` labeled MoE, with a new `asserted_context` ReviewRecord
  (`AC-C03`, notebook 01) stating who cares (the user's kitchen workflow) and the acceptance-versus-
  performance framing, `residual_uncertainties` honestly marking this a contestable judgment.
- **F-2/F-3 (DL-018, DL-032, DL-039)**: the empirical premise that made this chapter's real content
  different from what the audit assumed — post-rebase, `nominal.cycleTime` has no value at all
  (Chapter 1's DL-018 fix), so `assert satisfy timely by nominal` cannot even be evaluated
  (`ExecutionError: no value for feature toaster.cycleTime`), not merely "passes because the
  default happens to hold." The chapter no longer claims anything about `nominal`; it introduces
  the satisfy idiom entirely through `slow`'s deliberately negated claim, narrated honestly as one
  of DL-032's three sanctioned ways to build a failing branch (a deliberately negated claim), not as
  a demonstration of a design-rooted failure (DL-049).
- **F-4/OQ-4 (DL-033)**: `part evidence` (the invented namespace container) removed. Two idioms
  were probed empirically rather than assumed: binding through `TimelyToastTest`'s own
  subject/objective leaves the exported `SatisfyRequirementUsage` with `subject: None`, so the
  conformance check would silently skip it; folding the claim into `slow`'s own body resolves a
  real subject and evaluates. The builder used the second, and the reviewer independently confirmed
  the first genuinely doesn't work as tried (though a different construction of it might; DL-033
  authorized either idiom, so this doesn't reopen anything).
- **F-5/OQ-3 (DL-030)**: `calc def DeliveredEnergy` removed from the chapter entirely, deferred to
  the logical carrier (`HeatingSystem`) that doesn't exist until Chapter 4/5. Notebook 02
  repurposed from calc-def evaluation to teaching the satisfy/not-satisfy idiom itself.
- **F-6**: chapter text errors fixed (notebook count, `TimelyToastTest` mentioned in `conclusion.md`,
  no claim that both candidates satisfy).
- **Standing SOP (`next-passes.md` item 10)**: Chapter 2's `conclusion.md` "What comes next" was
  re-checked and rewritten to match what Chapter 3 actually contains (it had already gone stale on
  `calc def`, per F-5's removal).
- `myst.yml`'s Chapter 3 table of contents was missing `04-verification-case` entirely; added.

## Review rounds

1. **Build**, including the rebase and the two empirical probes above (subject resolution for both
   named F-4 idioms; the `nominal` eval-error premise, confirmed against the real fixture, not a
   synthetic snippet).
2. **Review round 1: FAIL.** Co-author trailers on all four commits (this repo's plain-commit rule).
   "Candidate"/"variant"/"design" narration of `nominal`/`slow` survived in several places — the
   same class of DL-032 violation PASS4-002 already had to fix once in Chapter 2, recurring here in
   new spots (`index.md`, both chapters' `conclusion.md`, notebook 02, and a self-contradicting
   AS-C03 whose `premises` and `rationale` disagreed with each other). One cell stated DL-032/DL-049's
   ruling backwards, claiming the negated claim demonstrated a "design-rooted" failure when the
   ruling says the opposite. Three consecutive code cells in notebook 04 with no narration bridge,
   the exact pacing defect the contract named explicitly. Plus non-blocking notes: decision-log
   numbers leaking into learner-facing prose and ReviewRecord fields, two lines of metanarration, and
   an inaccurate test docstring.
3. **My rulings on the reviewer's open questions**: the `slow` fixture itself is fine as built
   (typed redefinition plus a negated claim is explicitly DL-032's third sanctioned option); only the
   narration was wrong about *why*. Notebook filenames stay unrenamed (already decided in the
   original contract). Exercise pointers stay pointed at the real, unfixed exercise content, per the
   exact precedent PASS4-002 set for the identical situation in Chapter 2 (routed to
   `next-passes.md` §7 item 9, not patched piecemeal). DL numbers do not belong in learner content
   anywhere, including inside ReviewRecord field strings.
4. **Push-back and fix**: co-author trailers stripped via `git filter-branch --msg-filter` (verified
   by tree-hash comparison in round 2 that only commit messages changed, not content); all
   candidate/variant language fixed and re-grepped; the inverted DL-032/DL-049 cell rewritten to
   match AS-C03's own (already-correct) counterevidence field; two narration bridges added to
   notebook 04; DL-number citations and metanarration removed; the test docstring corrected.
5. **Review round 2: PASS.** Every round-1 finding verified fixed independently, including
   re-reading `exercises/ch03/exercise.ipynb` directly to confirm the rewritten conclusion.md text
   ("nominal and hot usages of `BrewUnit`") wasn't fabricated. Four small non-blocking notes
   remained (residual process-history wording in two places, one ambiguous phrase in AS-C03, a test
   assertion that could pin what the docstring only asserted in prose).
6. **Non-blocking polish applied directly at merge** (orchestrator, not a third builder round, per
   the reviewer's own framing that these were mergeable as-is): dropped "recorded here by this
   chapter's re-derivation" and "rebuilds... so it states honestly" (both artifacts of describing
   the tutorial's own authoring process rather than its content); reworded AS-C03's "as designed" to
   "as intended for the injected fault" (removed the reading that could imply design-rootedness);
   added a real `assert "ToasterDemo::timely" not in joined` to
   `test_predecessor_containment.py`'s ch03-to-ch04 test, which previously asserted this only in its
   docstring. Applied as plain string-level substitutions (not JSON re-serialization) to keep the
   diffs to single-line changes; verified the notebook JSON stayed valid and re-ran the full
   acceptance suite before merging.

## What the run showed

- **The predecessor-containment gap moved again, exactly as PASS4-002 said it would.**
  `ch03 -> ch04`'s 8 failures (the same 6 functional constructs Ch2's fix carried forward, plus
  `TimelyToastTest` and its subject — a pre-existing drop from before this contract) are now the
  next chapter's problem, recorded and not fixed here, same non-goal boundary as every prior run in
  this sequence.
- **A ruling can authorize two idioms and still have only one actually work.** DL-033 named two
  acceptable ways to replace `part evidence`; only empirical probing (not re-reading the ruling more
  carefully) revealed that binding through a verification case's subject/objective leaves the claim
  with an unresolved subject in OpenSysML v0.9.0 today. The ruling wasn't wrong to name both; the
  tool just doesn't support one of them yet.
- **A narration defect can recur in a new chapter even after the exact same class of defect was
  fixed once already.** PASS4-002 fixed "candidate"/"variant" language in Chapter 2; it reappeared
  in Chapter 3's own new prose, in new spots, requiring the same fix again. Worth an explicit
  grep-based check in every future chapter's review, not just careful first-pass reading (the same
  lesson PASS4-002 itself already drew about the "candidate/variant/for any X" family).
- **Rewriting a chapter's own settled reasoning is a distinct failure mode from getting a fact
  wrong.** Round 1's most substantial finding wasn't a wrong fact but a *backwards* reading of an
  existing ruling (DL-032/DL-049), stated confidently in a cell right next to a ReviewRecord that
  had the correct framing in its own `counterevidence` field. The fix was to match the two, not to
  invent new reasoning — a sign that the check for this class of error is "does this cell agree with
  the record sitting three cells away," not just "is this cell internally plausible."
- **The standing SOP (checking the previous chapter's "What comes next") caught a real, expected
  staleness immediately**, the first time it ran as a required contract step rather than an
  after-the-fact discovery: Chapter 2's forward claim about `calc def` was already wrong the moment
  F-5 removed it from Chapter 3, and the contract's own structure meant this was fixed in the same
  pass rather than found later by chance.

## Verification

289 tests passing (unchanged from the pre-contract baseline, confirmed independently by both the
author and reviewer against the true parent commit rather than trusting the contract's stale
`287` figure inherited from `pass4-run-002.md`), 0 ch03 lint hits (28 before), `glossary check`
clean, 0 co-author trailers across 5 integrated commits, 0 em-dashes in every touched file including
code-cell comments, `conformance.report(model, stage=(3,1))` reports `satisfaction-claims-evaluated`
`passed` with exactly one evaluated claim (`slow`, negated, holds) and zero findings, local book
build clean (58 pages), all four ch03 notebooks execute fresh with real, non-empty output cells.
Worktree and branch cleaned up after merge (`ffa4dc8`).

## Not fixed here, carried forward explicitly

- **Chapter 4's predecessor-containment gap** against the new Chapter 3 (8 elements: the 6
  functional constructs plus `TimelyToastTest` and its subject) — inherits to whichever contract
  re-derives Chapter 4.
- **`scripts/check_construction.py`'s Chapter 4 context stub** still attributes `calc def
  DeliveredEnergy` to Chapter 3; it no longer originates there. Doesn't break anything today (a
  self-contained, non-literal validation stand-in, same class of harmless staleness PASS4-002 left
  in Chapter 2's own stub) but is now factually wrong about provenance.
- **`exercises/ch03/exercise.ipynb`** — untouched, per the exercise-track contract already logged
  (`decisions/next-passes.md` §7 item 9). Still asks for the deprecated pattern (satisfy claims for
  both a nominal and a hot variant, a `calc def`). The main chapter's exercise pointers were checked
  for factual accuracy against the exercise's real (unfixed) content and left as accurate
  descriptions of it, per the identical precedent PASS4-002 set in Chapter 2.
- **`models/ch04-cumulative.sysml`'s `assert satisfy timely by slow;`** (a positive, now-contradicted
  claim, since Chapter 3's own copy is negated) — already tracked in `decisions/pass4-backlog.md`
  item 1; belongs to Chapter 4's own re-derivation.
- **`src/toaster/conformance.py`'s `satisfaction_claims_evaluated`** silently skips a satisfy
  relationship with no resolvable requirement, rather than reporting it distinguishably (the
  reviewer's own probe constructed this case). Outside this contract's blast zone; noted here for
  whoever next touches that function.
