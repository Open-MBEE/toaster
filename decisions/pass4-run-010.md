# Pass 4, run 010: Chapter 10, authored from scratch, the tutorial's final chapter (2026-09-28)

Contract PASS4-010. Builder Sonnet 5, reviewer Opus 5.5 (independent, different model), two review
rounds plus a third, narrow round applied directly by the orchestrator. Like Chapter 9, this was
original authoring, not a re-derivation: Chapter 10 ("Traceability and Sign-off") was a genuine
`[TODO]` stub. This is the tutorial's capstone chapter, and the highest-stakes content in the whole
pass for one specific reason: AGENTS.md's judgment section is unconditional that no tutorial text may
ever record a disposition as "accepted" (SA-7), and this is precisely the chapter titled "sign-off,"
exactly where a careless author would be tempted to write a triumphant, closed ending.

## What shipped

- **A real traceability graph built from real queries, not hand-typed tables.** `heatGenerationReq`
  traces to genuine, bidirectional verification evidence (`rated` satisfies it, `weak` fails it, both
  correctly expressed since Chapter 3/6's own fixes). `timely` traces just as far through intent,
  allocation and realization, but stops one link short: no candidate has ever been positively checked
  against it, only `slow`'s negative claim and an unbound verification-case objective exist.
- **A real, honest, previously-undiscovered finding: the tutorial's single strongest piece of evidence
  is orphaned from any requirement.** `deliveredEnergyBoundedBySupply` (Chapter 8's Z3-proved universal
  property) is tied to no `RequirementUsage` anywhere in the model, confirmed by direct query (every
  `SatisfyRequirementUsage` names only `timely` or `heatGenerationReq`). The chapter states this
  precisely as the inverse of a failure mode Douglas's own traceability concern names (an unjustified
  widget, a design element with no requirement behind it; here, evidence disconnected from any stated
  need instead) rather than treating it as a defect in the proof itself.
- **A judgment ledger built from three verbatim-reconstructed real records** (`AS-C06`, `AS-C08` reused
  from Chapter 9 and independently re-verified rather than assumed correct; `AI-C06`, a new
  reconstruction of Chapter 6's own stopping judgment), each checked programmatically against its real
  original by executing the source notebook and diffing every `ReviewRecord` field, not eyeballed.
- **A capstone synthesis record, `AI-C10`**, built as a real `ReviewRecord` (`kind="asserted_inference"`,
  its own `premises` drawn directly from what notebooks 01 and 02 actually establish), with
  `disposition="pending"` and `engineering_conclusion="undetermined"`, the only honest characterization
  of a case with one requirement fully covered, one uncovered, and the tutorial's strongest proof tied to
  neither.
- **An explicit, load-bearing distinction stated to the learner**: this record is not sign-off. Sign-off
  is a human, accountable act the tutorial can show the inputs to, not perform on the learner's behalf.
  A closing paragraph ties this directly to AGENTS.md's own line that strong emergence "is what sign-off
  judges," framing the chapter's synthesis as an input to that judgment, never a substitute for it.
- **A real fix to Chapter 9's own carried-forward precondition** (`decisions/next-passes.md` item 21):
  Chapter 9 added no cumulative fixture, so a naive predecessor-containment check would silently no-op
  against it. Chapter 10 generalized the check itself (`_nearest_predecessor_fixture`, walking backward
  to the nearest chapter with a real file on disk) rather than special-casing chapter 9, verified as
  genuinely non-vacuous by constructing a scratch removal and confirming the check catches it.

## The one defect that mattered, and how it was caught and removed

1. **Round 1 review found a real, maximum-severity SA-7 violation.** Notebook 03's own negative-control
   cell constructed a genuine `ReviewRecord` with `disposition="accepted"` (named `AI-BAD-ACCEPTED`, with
   a forbidding comment, never added to the ledger or to `AI-C10`'s premises). The reviewer classified
   this precisely: it is a real object construction with that literal disposition value, in committed,
   executable, learner-facing code, regardless of the surrounding framing.
2. **The orchestrator ruled it a zero-tolerance violation, no exception.** AGENTS.md's rule has no
   negative-control carve-out anywhere, and every prior chapter in this pass had kept the literal string
   "accepted" out of every constructed `ReviewRecord`, full stop, across nine chapters. The fix directed:
   remove the construction entirely, replace with a genuinely better negative control (a draft `AI-C10`
   with empty `counterevidence`, which `validate_record()` actually and correctly rejects), and if the
   point about the validator's own blind spot is still worth making, state it in prose only, never by
   executing the forbidden construction.
3. **The fix was verified two ways before round 2 review, and a third time independently by the
   reviewer.** The builder's own report reproduced the reviewer's exact grep and found zero remaining
   hits attached to any `ReviewRecord` construction. Round 2's reviewer, working independently, re-ran the
   same grep across every notebook's cell sources AND stored outputs (not just source, in case a stale
   execution had left the old output behind), checked every `disposition=` in every code cell individually
   (confirming all were `"pending"`), and even searched for obfuscated forms (string concatenation, `chr()`
   calls) that might smuggle the value past a literal grep. None were found.
4. **A genuinely new question surfaced only at the very end: does the zero-tolerance rule reach git
   history, not just the current committed state?** The forbidden construction still exists in an earlier
   commit on the branch (the version before it was deleted). The orchestrator ruled: no, merge normally
   (`--no-ff`, preserving full history), matching this entire pass's own consistent, established practice
   of keeping every chapter's real mistakes and fixes visible in its git history and its own run log
   (Chapter 6's circularity, Chapter 7 and 9's own caught overclaims, and now this). SA-7 governs what the
   tutorial currently teaches a reader, not an erasure of the transparent record of how a real mistake was
   caught and corrected, which this project has valued consistently throughout.

## Review rounds, in brief

1. **Build.** The traceability graph, judgment ledger and sign-off synthesis built against real,
   current model data; the predecessor-containment precondition resolved generally, not special-cased.
2. **Round 1 review: FAIL**, on the SA-7 violation above (maximum severity) plus eight mechanical items:
   two unrecorded real gaps this chapter's own work exposed (`validate_record()` doesn't itself enforce
   SA-7's disposition rule; the lint's `accepted-disposition` check only scans markdown cells, never
   code); an overclaimed "honestly and completely" contradicting the chapter's own honest-scope framing
   elsewhere; a Purpose section that briefly implied the chapter performs sign-off, contradicting its own
   explicit "it is not sign-off" statement; a factual slip mirroring one Chapter 9's own round 3 already
   had to fix ("timely covered by neither" when a real negative claim exists); a Douglas-attribution
   overclaim and a judgment record wrongly conflating two separate facts (why the proof is orphaned versus
   what its own scope limitation is); plus several smaller wording and test-docstring inaccuracies.
3. **Push-back and fix**: the SA-7 violation removed and replaced with a genuinely stronger negative
   control; both real gaps recorded in `decisions/next-passes.md`; every overclaim and misattribution
   corrected; a new paragraph added tying the chapter's synthesis explicitly to AGENTS.md's own strong-
   emergence framing.
4. **Round 2 review: PASS**, with three optional, non-blocking wording nits (an ambiguous sentence that
   could be misread as restating the original Douglas overclaim; a residual "or no evidence" phrase where
   no traced element actually has zero evidence; a test docstring crediting the wrong test function with a
   proof). One additional judgment call surfaced: whether SA-7's zero tolerance extends to git history
   (see above).
5. **Applied directly by the orchestrator**: the three nits, plus the merge-strategy ruling. Independently
   re-verified (full test suite, construction check, glossary check, zero em-dashes, a repo-wide grep
   confirming zero instances of `disposition="accepted"` anywhere in the merged, integrated tutorial)
   before merge.

## What the run showed

- **The highest-stakes rule in the whole tutorial needed the most adversarial verification, and got it.**
  Both reviewers treated the SA-7 check as the load-bearing priority it was framed as, going well beyond a
  literal-string grep on source code alone: checking stored notebook outputs (not just source, in case a
  stale execution masked a fix), checking every `disposition=` value individually rather than trusting a
  single grep to catch everything, and explicitly probing for obfuscated forms. This is the discipline
  this whole pass has built toward: a rule this important does not get a cursory pass.
- **A negative control that requires constructing the forbidden thing itself is a design smell, not just
  a rule violation.** The fix wasn't merely "delete the offending cell": it replaced a negative control
  that demonstrated a real problem (a validator gap) by executing something categorically forbidden with
  one that demonstrates the same kind of point (a validator catching something) using a construction the
  rule has no objection to at all (empty `counterevidence`, which is genuinely, separately wrong and which
  the validator is actually designed to catch). The better fix and the compliant fix turned out to be the
  same fix.
- **Finding a real, previously-undiscovered gap in the tutorial's own tooling is worth surfacing even in
  the very last chapter.** `validate_record()` never checking `disposition`, and the lint's blind spot for
  code cells, are real, load-bearing findings about the tutorial's own mechanized safety net that only
  surfaced because this chapter's own draft happened to test the boundary. Recording them, rather than
  letting the fix that removed the symptom also erase the discovery, keeps the gap-tracking discipline this
  entire pass has maintained intact through its very last content contract.
- **A completed tutorial does not mean every judgment is now closed**, and the tutorial's own closing
  chapter had to model that honestly about itself, not just about the toaster. `AI-C10`'s own
  `engineering_conclusion="undetermined"` and the explicit "this is not sign-off" framing are the chapter
  practicing exactly the discipline the whole pass has enforced on every prior chapter's own claims.

## Verification

308 tests passing, 2 known and explicitly tracked failures (unchanged, unrelated: `tests/
test_skill_snippets.py`, `decisions/next-passes.md` item 17). 0 ch10-specific lint hits at `error`
severity (2 `warn`-severity `accepted-disposition` hits remain, both confirmed prose-only, discussing the
rule and the tool gap, never attached to executed code). `glossary check` clean. 0 co-author trailers
across 6 integrated commits (stripped twice across the review cycle after the harness's own automated
attribution pass re-added one mid-round; tree-hash verified unchanged both times). 0 em-dashes in every
touched learner-facing and test file. A repo-wide grep after merge confirms zero instances of
`disposition="accepted"` anywhere in the fully integrated, ten-chapter tutorial. `check_construction.py
--check` reports all 10 chapters consistent; the ch08-to-ch10 predecessor-containment fallback confirmed
genuinely non-vacuous (a constructed scratch removal is caught). A per-cell fresh-execution-versus-
committed-output comparison confirmed zero content differences across every touched notebook before
merge. Local book build clean; all three notebooks execute cleanly with real, non-empty output. Worktree
and branch cleaned up after merge (`8ad8270`).

## Not fixed here, carried forward explicitly

- **`validate_record()` never inspects `disposition`, and `glossary/lint.py`'s `accepted-disposition`
  rule only scans markdown cells, never code cells** (found and recorded this chapter, `decisions/
  next-passes.md` item 22). A real gap in the tutorial's own mechanized SA-7 safety net; the code fix for
  either is outside this contract's blast zone.
- **The predecessor-containment fallback's own trade-off**: it cannot distinguish a deliberately-missing
  intermediate fixture (Chapter 9's own design choice) from an accidentally-missing one, and silently
  walks past either. Recorded in the same next-passes item; not a defect in the current sequence (every
  chapter 1 through 8's fixture is real and present), but worth a maintainer's awareness before a future
  chapter follows Chapter 9's own precedent.
- **`exercises/ch10/exercise.ipynb`'s own drift**: it names a nonexistent `models/ch10-snapshot.sysml`
  and asks for "bread-handling allocation links" the real model has never had. Confirmed genuinely stale;
  the chapter's own pointer text describes the exercise faithfully without repeating either false premise.
  The same systemic exercise-track drift `decisions/next-passes.md` item 9 already tracks.
- **`.claude/skills/opensysml-query/SKILL.md`'s stale citation of `requirement_coverage()`** (Chapter 9's
  own carried-forward item 20) remains untouched; nothing in this chapter's own work changed that
  assessment.

## Closing note: this completes the ten-chapter re-derivation

Chapters 1 through 10 have now all been re-derived or, for Chapters 9 and 10, authored from scratch
against the aligned Foundations (AGENTS.md Part 1), producing a complete, internally consistent draft of
the tutorial for Z's end-to-end review. `decisions/next-passes.md` carries forward every item flagged
along the way (22 numbered items as of this run) for whoever picks up the next pass. `docs/
reproducibility.md` and the other backmatter pages were completed earlier in this same session, alongside
this chapter sequence.
