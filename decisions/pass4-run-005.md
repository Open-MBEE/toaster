# Pass 4, run 005: Chapter 5 re-derivation (2026-09-28)

Contract PASS4-005. Builder Sonnet 5, reviewer Opus 5.5 (independent, different model), four review
rounds. Executes `decisions/audits/ch05-layer-audit.md` against DL-018, DL-019, DL-020, DL-021,
DL-023, DL-030, DL-031, DL-036, DL-037, DL-038, DL-039, DL-048. A real structural redesign, not a
patch: the audit found the chapter's central teaching content invalid, and this run replaced it
with content genuinely new to the model — its first real port-typed interface.

## What shipped

- **F-1 (allocation declared between definitions, invalid per KerML, undiagnosed by OpenSysML).**
  Replaced with a named, usage-level allocation (`allocation heatAllocation allocate
  ToastBread::applyHeat to Toaster::heating;`), now possible because Chapter 4's own nesting fix
  gave `ApplyHeat` a real usage to allocate. Visible to `model.query()`.
- **F-2 (no `perform`, no abstract logical carrier, DL-020).** `HeatingSystem` rebuilt as a genuine
  logical carrier: `abstract part def HeatingSystem { perform action applyHeat : ApplyHeat; port
  durationIn : ~DurationPort; }`.
- **F-3 through F-6 (BreadLoader/BreadEjector/BreadHandling: invalid item-typed part usages, traced
  to no function, never composed into the system of interest).** Removed entirely rather than
  repaired — the underlying functions don't exist in the model, and inventing them would violate
  the same "don't invent functions not asked for" boundary test the original content already broke.
- **New port/interface content.** `ControlSystem` and `HeatingSystem` connected through
  `interface durationInterface connect control.durationOut to heating.durationIn;`, carrying the
  `duration` signal Chapter 4 explicitly left unconnected. The conjugate-port idiom (`~DurationPort`)
  was verified against the actual SysML v2.0 spec text (Annex A.3, Figure 60's `FuelInterface`
  example) before committing to it, not assumed — confirmed the interface's own ends are bare ports,
  matching exactly what was built.
- **Conformance check scheduling (DL-038).** `port-type`'s `applies_from` set to `(5, 3)`, the first
  chapter with a real port-typed connection to test — reports `passed` against a genuine two-port
  comparison, confirmed non-vacuous by a dedicated negative-control test.
- **F-8 (the "Concept Selection" title/filename mismatch, a vocabulary lint hit).** Retitled to
  reflect the notebook's actual content (model navigation via `model.find`/`model.get`), filename
  kept per the Chapter 3 precedent.
- **F-9 (the interconnection figure existed but was never shown).** Unlike Chapters 2 and 4, this
  chapter's own tooling call already existed unused — actually rendered and displayed this time,
  the first chapter in the sequence to do so.

## Review rounds

1. **Build.** F-1 through F-9 implemented; the port/interface construct choice (`flow` vs.
   `interface`) probed empirically; `render.py` widened to recognize the new construct.
2. **Round 1: FAIL**, most seriously a real regression — `HeatingSystem :> ToastingSystem`
   reintroduced, exactly the pattern DL-019 (`ToastingSystem` is the subject all layers describe, not
   a logical component) and DL-020 ruled out, and that Chapter 1's own re-derivation had already
   removed (`decisions/pass4-run-001.md`). Also: the retitle never reached the published book (no
   heading, so MyST fell back to the filename); two claims contradicted by the model itself (duration
   "now has a source" when nothing binds it; the port check "confirms compatibility" when its own
   docstring admits it doesn't handle conjugation); a new test that couldn't distinguish a real port
   comparison from a vacuous one.
3. **My rulings on four open questions**: use `interface` (spec-correct for a connection whose ends
   are all ports) over `flow` (which the reviewer's own citation showed isn't a connection at all),
   widening `render.py`'s blast zone to match; `ControlSystem` stays concrete with no invented policy
   action (no policy exists yet to allocate); the forward claim to Chapter 6 must not presuppose a
   direct logical-to-physical jump (DL-043); the allocation's usage and `HeatingSystem`'s own
   `perform` being distinct, type-matched occurrences is acceptable at this stage.
4. **Push-back and fix**: the regression reverted; the retitle fixed with real headings; both
   overclaims reworded to state precisely what was and wasn't accomplished; the test rewritten to
   assert the connector's actual ends and to include a genuine mismatch negative control; `interface`
   substituted for `flow` throughout, with a real node-identity rendering bug found and fixed as a
   side effect; a new tool gap (reopening a definition poisons `to_api_json()`) found and logged
   (`DEFERRED.md` D-027, held not filed).
5. **Round 2: FAIL** on four items: co-author trailers (mechanical, stripped directly); D-027's own
   repro didn't reproduce as written (missing an import — the same class of error D-026 needed a
   round to fix); three stale forward references still described the removed `flow` construct; one
   notebook claimed the allocation's evidence without printing it, blurring a usage with its
   definition in the one notebook whose point is that allocation is usage-level.
6. **Push-back and fix**: all three substantive items corrected and independently re-verified; trailers
   stripped a second time.
7. **Round 3: FAIL** on three small, precisely-specified text items (a stale "connects" claim missed
   in one file when fixed in another; a false cross-reference; a stale print label on an unchanged,
   correct dict key) — each narrower in scope than the round before it.
8. **Applied directly by the orchestrator** rather than a fourth builder round, given the pattern of
   narrowing, purely-textual findings (the same judgment applied to PASS4-004's D-026/Draft 10 late
   rounds); bundled two related non-blocking notes (a value-vs-type-of-value tension; an internal
   process document cited in learner prose) into the same fix.
9. **Round 4: PASS.** Confirmed clean, including re-executing both touched notebooks fresh and
   verifying the fix's word-diff was exactly the three targeted lines, nothing broader.

## What the run showed

- **A rebuild can regress an already-settled ruling from an earlier chapter, and the audit that
  targets the current chapter won't catch it** — the Ch5 audit never mentions `ToastingSystem`
  specialization because the stale fixture it read predates Chapter 4's fix; only independent review
  against the actual current DL rulings caught the reintroduction. This is a sharper version of the
  "predecessor-containment gap moves" lesson: a regression can reintroduce something a *different*
  chapter's audit already flagged and a *different* chapter's contract already fixed, invisible to
  both the current chapter's own audit and its own predecessor-containment check (which only verifies
  elements aren't *missing*, not that removed problems don't quietly come back under a new name).
- **Genuinely new model territory (this chapter's first port/interface content) is exactly where
  spec verification earns its keep.** The builder's own uncertainty about the correct idiom (bare
  port ends vs. the directed-feature form) was resolved not by guessing or by the reviewer's citation
  alone, but by the orchestrator reading the actual spec figure — confirming the builder's instinct
  was right for a subtly different reason than either party had fully articulated (the directed flow
  is a nested annotation *inside* an interface definition, not an alternative to the interface's own
  end declarations).
- **A tool's own rendering/tooling limitations should not dictate model content.** The initial choice
  of `flow` over `interface` was made to fit `render.py`'s narrower element recognition — exactly
  the inversion the diagrams skill warns against ("keep model content and presentation settings
  distinct"). The fix was to widen the tool, not to let its gap shape what the model says.
- **A test that only checks a count or a status can still be vacuous.** The original port-type test
  passed before this chapter had any real port-typed connection to test at all; even after one
  existed, an early version could not distinguish a real end-to-end port comparison from an
  accidental comparison of inner features. Only an explicit end-identity assertion, plus a genuine
  mismatch negative control, closes this — matching exactly the "tests assert real behavior, not
  just that code runs" standard the reviewer role already carries.

## Verification

294 tests passing (289 at Chapter 4's baseline, +5 net across this chapter: two new port-type tests,
two interconnection regression tests, one predecessor-containment rename), 0 ch05 lint hits
(`concept-selection` rule: 1 before, 0 after), `glossary check` clean, 0 co-author trailers across
15 integrated commits (stripped three separate times across the build/review cycle, tree-hash
verified each time), 0 em-dashes in every touched learner-facing file. `conformance.report`'s
`port-type` check reports `passed` on a genuine two-port comparison at `(5, 3)`. Local book build
clean (58 pages); the interconnection figure renders and displays correctly, node-identity bug fixed.
Worktree and branch cleaned up after merge (`5b532e3`).

## Not fixed here, carried forward explicitly

- **Chapter 6's predecessor-containment gap** against the new Chapter 5 — inherits to Chapter 6's
  own contract, along with `HeatingSystem`'s corrected shape (abstract, no `ToastingSystem`
  supertype, performs `ApplyHeat`) and the new interface idiom this chapter established.
- **D-027, held, not filed.** The "reopening a definition poisons `to_api_json()`" gap
  (`DEFERRED.md`, `decisions/gap-issue-drafts.md` Draft 11) — a candidate language-tier hole, framed
  honestly with two unresolved readings rather than a settled bug claim, awaiting Z's review before
  any upstream report.
- **`exercises/ch05/exercise.ipynb`** — untouched (`decisions/next-passes.md` §7 item 9's dedicated
  exercise-track contract); still asks for the removed `flow`/definition-level `allocate` pattern.
  Every pointer in the main chapter checked for accuracy against its real, unfixed content.
  Flagged for whoever eventually re-derives that contract, not enumerated by chapter number in the
  existing generic tracking item.
- **`ControlSystem` staying concrete with no `perform`** — acceptable at this stage per DL-020's own
  "logical, not yet built" framing; a policy action for it to perform doesn't exist anywhere in the
  model yet (DL-022/DL-044's territory, once state machines are modeled).
