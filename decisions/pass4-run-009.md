# Pass 4, run 009: Chapter 9, authored from scratch (2026-09-28)

Contract PASS4-009. Builder Sonnet 5, reviewer Opus 5.5 (independent, different model), three review
rounds plus a fourth, narrow round applied directly by the orchestrator. Unlike every prior Pass 4
chapter, this was not a re-derivation against an existing layer audit: Chapter 9 ("Coverage and
Sufficiency") was a genuine `[TODO]` stub with no model file and no prior content at all. This contract
authored it from scratch, grounded directly in AGENTS.md Part 1 (item 7: "coverage and traceability in
service of the accountable engineer's sign-off") and the glossary's `sufficiency`/`traceability` terms,
anchored on a real finding verified against the current model before the contract was even written:
`nominal` (the usage meant to represent the toaster actually meeting `TimelyToast`) has no `assert
satisfy timely by nominal` anywhere in the model.

## What shipped

- **A real, not manufactured, coverage gap as the chapter's own negative control.** `heatGenerationReq`
  is fully covered (`assert satisfy ... by rated`, `assert not satisfy ... by weak`); `timely` has never
  had a positive claim, only `slow`'s negative one and `TimelyToastTest`'s bare `verify timely;`
  objective (no subject bound). The chapter states precisely what this means (an absence of a claim, not
  evidence that `nominal` fails `timely`, since `cycleTime` is still undecided from anything) and what it
  doesn't.
- **A real, previously-flagged, never-fixed tool bug found and fixed as part of this contract:
  `src/toaster/query.py`'s `requirement_coverage()` was polarity-blind.** It counted `slow`'s FAILING
  claim as coverage (`timely: covered=True, satisfied_by=['slow']`), a defect `decisions/audits/
  ch06-layer-audit.md` had already named (F-1: "counts the false claim as coverage") and that had sat
  unfixed and untracked since. The chapter's own hand-rolled join reached the correct, opposite answer
  without ever mentioning the helper disagreed with it, until review caught this. Fixed for real (split
  into `satisfied_by`/`failed_by`, verification-case objectives with no bound subject excluded), with
  nb01 redesigned around a naive-vs-fixed contrast: rather than silently working around a real bug, the
  chapter now teaches from it directly.
- **Verbatim record reconstruction, verified programmatically.** Notebook 02 (sufficiency) and notebook
  03 (staleness at scale) both reconstruct two real records, `AS-C06` (Chapter 6) and `AS-C08` (Chapter
  8), as a small, honestly-scoped representative sample (this tutorial has no central ReviewRecord
  registry, confirmed by search, so "every record ever written" cannot be scanned). Round 1 review found
  real drift between the reconstructions and the originals (a dropped sentence, a miscounted "two"
  toolchain limits where the original names three). Round 2's fix was verified not just by inspection but
  programmatically: a script executed the real original notebooks in memory and compared every
  `ReviewRecord` field against the reconstruction; round 3 independently re-ran the same kind of check
  and confirmed zero differing fields (except `content_hash`, which correctly differs by design, computed
  against different files).
- **A genuine sufficiency negative control.** `AS-PLACEHOLDER`, a record with `counterevidence="None
  known."` and `residual_uncertainties="None."`: structurally valid (`validate_record()` accepts it
  outright) but substantively empty, contrasted against `AS-C06`/`AS-C08`'s real, specific fields.
- **A genuinely stronger staleness story than the first draft told.** `AS-C06`'s own record is not just
  formally stale (a whole-file hash mismatch); Chapter 7 added exactly the `HeatGenerator`
  `efficiency`/`efficiencyBounded`/`deliveredEnergy` machinery its own counterevidence had named as
  missing, squarely inside its declared scope. Round 3 review caught that the fix's own language had
  overclaimed this as the gap being "exactly closed" (it's genuinely only partly overtaken: the Joule-
  heating relation and any response-time comparison the same counterevidence names are still unmodeled)
  and misattributed the growth to "Chapters 7 and 8" when the `HeatGenerator` block is byte-identical
  between those two files (Chapter 7 alone did it). Both corrected in the final direct-fix round.
- **Tests that check what their names claim.** The two new predecessor-containment tests were
  initially tautological (asserting something already true before the diff, or indistinguishable from a
  genuine clean pass); fixed to check the real filesystem state and to prove the early-return guard fires
  via a monkeypatch, sanity-verified by the builder deliberately breaking each check and confirming it
  fails, then reverting.
- **An honest design choice: no `models/ch09-cumulative.sysml`.** This is an analysis-only chapter over
  the real, current `ch08-cumulative.sysml`; adding a fixture wasn't needed for the anchor finding and
  wasn't added by default. Made explicit rather than silently indistinguishable from every other
  chapter's own fixture-adding pattern, with two dedicated tests and a `decisions/next-passes.md` entry
  flagging the consequence for Chapter 10's own predecessor-containment check.

## Review rounds, in brief

1. **Build.** The anchor coverage gap discovered and demonstrated for real; the three notebooks
   (requirement coverage, evidence sufficiency, staleness at scale) built against real, current model
   data throughout.
2. **Round 1 review: FAIL**, on six real defects. F1 (above, the standout: a real, previously-flagged
   tool bug the chapter silently disagreed with rather than fixed or even mentioned). F2: a second
   "independent corroboration" claim in nb01 was vacuous, since `conformance.satisfaction_claims_
   evaluated()` only ever reports a finding for a failed claim or an error, never for a claim's mere
   absence, proven by the reviewer adding a real satisfying claim and getting an identical empty result.
   F3: the "exactly" reconstructed records had real drift. F4: the sufficiency check had no negative
   control of its own, only `validate_record()`'s structural floor. F5: the staleness narration was
   inaccurate in two ways (calling in-scope growth "unrelated"; misattributing which edit caused which
   record's staleness). F6: the two new tests didn't verify what their names claimed.
3. **Push-back and fix, including a real blast-zone widening** (to `src/toaster/query.py` and
   `tests/test_query.py`, ruled by the orchestrator after independently reproducing the bug): the helper
   fixed for real, not routed around; nb01 redesigned around the naive-vs-fixed contrast rather than
   inventing a weaker replacement corroboration; records reconstructed genuinely verbatim, verified
   programmatically; a real sufficiency negative control added; the staleness story rewritten around the
   truer, stronger finding (a record's own stated uncertainty substantively overtaken by real growth, not
   just a coincidental hash mismatch); the two tests fixed and sanity-checked by deliberately breaking
   them first.
4. **Round 3 review: FAIL, narrow.** All nine priority checks and every standing check passed on the
   code, tests and records; the fail was two learner-facing prose defects. The round 2 fix's own
   staleness story had overclaimed "exactly closed" where the model showed only a partial overtaking (the
   Joule-heating relation and response-time comparisons the same record names are still unmodeled), and
   misattributed two chapters' worth of growth to what was, checked directly, one chapter's own addition.
   A separate, smaller slip: index.md's "Expected result" section contradicted nb01's own finding,
   describing `timely` as "covered by neither" a positive nor negative claim when a real negative claim
   (`slow`'s) does exist; "covered by a negative claim" is exactly the polarity-blind framing the chapter
   argues against.
5. **Applied directly by the orchestrator**: both prose fixes, plus three small cosmetic items the
   reviewer also found (a placeholder finding-id citation left as literal "F-..." in `query.py`'s own
   docstring; a "(1 words)" pluralization bug requiring a small code fix and re-execution; an overstated
   claim about what "checking a batch" of records specifically reveals, versus what reading each record's
   real fields against the real model diff actually does). Independently re-verified (full test suite,
   construction check, glossary check, zero em-dashes, fresh-execution confirmation on the two re-executed
   notebooks) before merge.

## What the run showed

- **Original authoring needs the same adversarial rigor as re-derivation, arguably more, because there
  is no prior audit to check the result against.** Every "this is real, not manufactured" claim in this
  chapter was independently reproduced by the reviewer against the actual committed model at every round,
  not read and accepted from the notebook's own narration, exactly the discipline that caught F1 (a real
  bug the chapter would otherwise have silently shipped alongside) and the round 3 overclaim (a true
  finding stated with more certainty than the evidence actually supported).
- **A real, previously-known tool bug is sometimes worth fixing inside a content contract, not just
  flagging.** `requirement_coverage()`'s polarity-blindness had been named in an audit three chapters
  earlier and never touched. Routing around it (as the chapter's first draft did, silently) would have
  left two disagreeing coverage computations in the repository, one of them the skill-documented "correct"
  way to do this query. Fixing it, and then teaching directly from the fix, produced a better chapter than
  either silently working around the bug or deferring it yet again.
- **A genuinely careful reconstruction is worth verifying programmatically, not just by inspection.**
  "I copied it exactly" and "I actually did" turned out to be different claims in round 1 (a dropped
  sentence, a miscounted "two" instead of three) despite confident phrasing; the fix that actually closed
  this was a script that executed the real source notebooks and diffed every dataclass field, independently
  re-run by the round 3 reviewer with the same result.
- **The truer version of a finding is often more interesting than the first, tidier draft**, and can
  still be overclaimed on the way to being told. AS-C06's staleness being substantively tied to real,
  in-scope model growth (not "unrelated" bookkeeping) was itself a correction found in round 1; round 3
  then caught that same corrected finding had drifted into overclaiming completeness ("exactly closed")
  in the retelling. Precision has to be checked at every rewrite, not just once.

## Verification

303 tests passing, 2 known and explicitly tracked failures (unchanged, unrelated: `tests/
test_skill_snippets.py`, `decisions/next-passes.md` item 17). 0 ch09-specific lint hits. `glossary check`
clean. 0 co-author trailers across 8 integrated commits. 0 em-dashes in every touched learner-facing and
code file. `check_construction.py --check` reports all 9 chapters consistent, with Chapter 9's own lack
of a cumulative fixture made explicit via two dedicated tests rather than silently indistinguishable from
a real clean predecessor-containment pass. Local book build clean; all three notebooks execute cleanly
with real, non-empty output. A per-cell fresh-execution-versus-committed-output comparison (the correct
methodology once a subprocess call's own stdout/stderr interleaving with adjacent prints is accounted
for, per Chapter 8's established precedent) confirmed zero content differences across all three
notebooks before merge, including after the final round's re-execution. Worktree and branch cleaned up
after merge (`32de302`).

## Not fixed here, carried forward explicitly

- **`.claude/skills/opensysml-query/SKILL.md`'s own recommendation of `requirement_coverage()`
  now needs a skill-editor-protocol review**, since the function's return shape and behavior changed
  underneath it (the skill's own line only names the helper in a list with no documented return shape, so
  nothing it currently says is contradicted, but the change is worth a maintainer's look). `decisions/
  next-passes.md` item 20.
- **Chapter 10's own predecessor-containment check will silently no-op against Chapter 9**, since
  Chapter 9 has no cumulative fixture for it to compare against. A precondition for Chapter 10's own
  contract (fall back to the nearest earlier real fixture, or add an explicit separate assertion),
  recorded in `decisions/next-passes.md` item 21, not fixed here.
- **`exercises/ch09/exercise.ipynb`'s own drift**: it asks for a coverage table over "bread-handling
  requirements" against a `models/ch09-snapshot.sysml` file that doesn't exist and doesn't match this
  repo's naming convention, breaking from every other chapter's own self-contained "coffee maker" exercise
  pattern. Confirmed genuinely stale by the reviewer; the chapter's own pointer text describes the
  exercise faithfully as written rather than fabricating a fit that doesn't exist. Not fixed (outside
  every builder's established non-goal for this file); the same systemic exercise-track drift `decisions/
  next-passes.md` item 9 already tracks.
- **`docs/contributor.md`'s "Add a new chapter" guidance** (step 2: "Add the chapter's cumulative
  fixture...") is now slightly stale for an analysis-only chapter like this one. Flagged, not fixed
  (outside this contract's blast zone).
- **A requirement introduced by redefinition** (`requirement :>> r1` in a subtype) exports with no
  `declaredName` and would be silently excluded by `requirement_coverage()`'s new filter. No real chapter
  model uses this pattern today; found as a boundary probe during round 3 review, worth one line of
  awareness in Chapter 10's own contract if its traceability graph ever redefines a requirement in a
  subtype.
- **Whether the style guide's "no em-dash" rule's intent extends to the ASCII " -- " stand-in** this
  chapter (and Chapter 8 before it) uses in its place. The written rule is literally about the em-dash
  character, which this chapter satisfies; whether the intent behind the rule (a specific prose register)
  extends further is a style-guide question for the ACE or Z, not decided in this contract.
