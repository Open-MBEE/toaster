# Pass 4, run 006: Chapter 6 re-derivation (2026-09-28)

Contract PASS4-006. Builder Sonnet 5, reviewer Opus 5.5 (independent, different model), six review
rounds — the most of any chapter in this sequence. Executes `decisions/audits/ch06-layer-audit.md`
against DL-018 through DL-021, DL-030 through DL-033, DL-036 through DL-043, DL-048, DL-049. The
chapter that must show a genuinely complete recursive decomposition step, not a jump straight from a
logical component to physical parts — and the one where getting the selection-among-alternatives
judgment right took real, repeated scrutiny to actually achieve, not just claim.

## What shipped

- **Mandatory rebase**, resolving F-3 for free: `Heater` no longer exists anywhere in the current
  model (Chapter 1's own re-derivation already removed it), so the audit's finding about
  `HeatingReq`'s subject sitting outside the decomposition didn't need fixing — it needed rebuilding
  fresh.
- **F-1/F-2 (DL-039(4), DL-033, DL-049).** The false `assert satisfy heating by weak` replaced with
  `assert not satisfy` folded into the candidate's own context, the same idiom Chapter 3 and Chapter
  5 established. Per DL-049, this is now legitimately a design-choice failure (a chosen power rating
  genuinely failing a threshold), not DL-018's defect.
- **F-5/F-6/F-8 (DL-043 — the core structural requirement).** A complete level-2 chain: `GenerateHeat`
  (a real, energy-neutral function nested inside `ApplyHeat`, mirroring how `ApplyHeat` nests inside
  `ToastBread`), `HeatGenerator` (an abstract logical carrier, performs `GenerateHeat`, exposes an
  energy-in port honestly noted as unconnected to any producer), a named usage-level allocation, and
  `ResistanceCoil` (the concrete physical realization, properly ISQ-typed).
- **F-7 (DL-042 — naming and the selection among alternatives).** `HeatGenerator` stays neutral
  (named for the function, not a mechanism); `ResistanceCoil`'s mechanism-specific name and
  Joule-heating doc become admissible only after `AS-C06`, a real judgment record, is written.
  `PowerWire` — ungrounded, no function drives it — removed entirely rather than repaired, the same
  discipline applied to Chapter 1's `Heater` and Chapter 5's bread-handling content.
- **Honest scope, not overclaimed completeness.** The chapter states plainly that it builds one
  complete-in-argument, honestly-scoped branch of `ApplyHeat`'s own decomposition (the energy-to-heat
  path), not a full accounting of every flow `ApplyHeat` declares — matching the precedent Chapter 4
  already set for `ApplyHeat` itself.

## The selection-among-alternatives record: what six rounds actually bought

This chapter's hardest problem wasn't the model structure — it was making `AS-C06` (the DL-042
selection judgment) genuinely non-circular and internally honest, and it took real, repeated
scrutiny to get there, not a single pass.

1. **Round 1 found the deepest problem, and it was mine, not the builder's.** My own original
   contract told the builder to make `GenerateHeat` convert "an electrical energy input into a
   thermal energy output" — smuggling in exactly the mechanism commitment DL-042 says must wait for
   a recorded selection. The reviewer proved this directly: a combustion alternative genuinely
   couldn't satisfy an already-electrical signature, so `GenerateHeat`'s own claim to pass the same
   substitution test `ApplyHeat` passes was false, and `AS-C06`'s trade argument (resistive vs.
   gas-burner) was circular — the real choice had already been made, silently, in the function's own
   signature. I corrected my own contract wording in the push-back rather than asking the builder to
   guess what I actually meant.
2. **The fix (making `GenerateHeat`/`EnergyPort` genuinely energy-neutral, and having `AS-C06` argue
   from something that predates this chapter — `ControlSystem`'s existing discrete `durationOut`
   signal) was correct in substance, but each subsequent round found a corner of the record that
   still carried the withdrawn argument.** A reviewer-constructed `GasBurner :> HeatGenerator`
   counter-example — satisfying the requirement and both conformance checks exactly as cleanly as the
   resistive realization — became the standing test every round's fix was checked against, and it
   kept finding something: round 2's rationale still claimed a model-demonstrated "fit" the
   counter-example refuted; round 3's fix corrected the rationale and premises but left
   counterevidence and residual_uncertainties still asserting the same withdrawn claim, so the record
   contradicted itself field to field; round 5 found the same pattern a third time, in four markdown
   cells surrounding the record that hadn't been checked yet, plus one premise field.
3. **Two of these rounds also caught a distinct, mechanical failure mode**: a fix verified as correct
   against a scratch `/tmp` execution copy, but never actually written back into the committed
   notebook, so the stored, published output still showed the old, wrong text. This surfaced twice
   (round 3 for notebook 02, round 4 for notebook 03, which prints the whole model and had gone stale
   after a model-doc edit two rounds earlier). From round 3 onward, a byte-for-byte fresh-execution-
   versus-committed-output diff across all three notebooks became a standing check, specifically
   because "I re-executed it and it worked" and "I saved the version I re-executed" turned out to be
   two different claims.
4. **Round 6 passed clean** after an exhaustive, full re-read of every touched file (not a targeted
   check of previously-flagged cells), confirming via the same standing `GasBurner` counter-example
   that nothing remaining could be falsified by it, and confirming the fresh-vs-stored diff was
   genuinely zero everywhere, not just where the last fix landed.

## Review rounds, in brief

1. **Build.** F-1 through F-13 addressed; the level-2 chain built; `AS-C06` written (with the
   circularity described above, not yet caught).
2. **Round 1: FAIL.** The circularity (B3, mine); overclaimed completeness against DL-043 (B1/B2,
   contradicting the record's own counterevidence); `ResistanceCoil` named before the selection that
   licenses it (B4); two records citing evidence never gathered (B5); inaccurate exercise pointers
   (B6).
3. **Push-back and fix**: `GenerateHeat`/`EnergyPort` made energy-neutral; `AS-C06` rewritten to argue
   from `ControlSystem`'s pre-existing signal; completeness language removed, `engineering_conclusion`
   downgraded to `undetermined`; ordering fixed; evidence citations corrected; exercise pointers fixed.
4. **Round 2: FAIL.** A `print(source)` call reintroduced the ordering problem in a new cell; the
   rewritten rationale still claimed a discriminating "fit" the reviewer's own `GasBurner` probe
   disproved; residual "complete-in-itself" language; one more exercise-pointer inaccuracy.
5. **Applied directly by the orchestrator**: all four were narrow, precisely specified, no further
   design exploration needed.
6. **Round 3: FAIL.** The engineering_conclusion downgrade and rationale rewrite were correct, but
   `counterevidence`/`residual_uncertainties` — the same record's other two fields — still asserted
   the withdrawn "fitting what this model already builds" claim, contradicting the just-fixed
   rationale.
7. **Applied directly**: rewrote both fields consistently with the domain-premise framing; verified
   via the standing `GasBurner` counter-example.
8. **Round 4: FAIL.** The fix was verified via a scratch execution but never actually saved to the
   committed notebook (`--inplace` was needed, not used).
9. **Applied directly**: re-executed `--inplace`, confirmed the committed file's stored output matches.
10. **Round 5: FAIL.** Four markdown cells around `AS-C06` (not yet checked in any prior round) still
    described the selection as "argued from what the model already has"; one premise field still said
    a switched mechanism "fits this control interface directly"; and notebook 03 — untouched since an
    earlier round — had gone stale after the model doc changed two rounds earlier, publishing the
    withdrawn text in the built book.
11. **Applied directly**, plus an orchestrator-initiated exhaustive keyword sweep across every touched
    file before the next round, to try to catch anything remaining proactively.
12. **Round 6: PASS**, after an exhaustive full read (not a targeted check), confirmed via the
    standing counter-example and a repeated fresh-vs-stored diff across all three notebooks. One
    trivial grammar fix (a round-5 edit that read awkwardly) applied directly and merged without a
    further round.

## What the run showed

- **A contract's own wording can smuggle in exactly the defect the contract is trying to prevent.**
  DL-042 exists specifically to stop a mechanism name pre-empting an unrecorded selection; my own
  instruction to the builder did exactly that at one level down (a function signature, not a part
  name), and the review caught it precisely because it checked the substitution test rather than
  trusting the contract's framing. The fix belonged to whoever wrote the contract, not whoever
  executed it — and correcting it openly, rather than routing it back to the builder as if it were
  their mistake, kept the record of what actually happened honest.
- **A single false claim rarely lives in only one place once a chapter has been through several
  narrative passes.** The withdrawn "resistive heating fits the model" argument had been restated,
  paraphrased, and cross-referenced across a rationale, a counterevidence field, a residual-
  uncertainty note, four markdown framing cells, one premise, a model doc comment, and a chapter
  conclusion — eight distinct locations found across four separate rounds. A fix that only touches the
  cell a reviewer explicitly names will reliably miss the others; a standing, reusable counter-example
  (construct the disfavored alternative, confirm it satisfies everything equally) is what actually
  catches every one of them, because it doesn't depend on remembering where the claim was last seen.
- **"I verified this and it worked" and "I saved the version I verified" are different claims, and
  conflating them is a real, recurring failure mode**, not a one-off slip — it happened twice in this
  same chapter. A fresh-execution-versus-committed-output diff, not just a successful nbconvert run,
  is the check that actually closes this gap, and it's cheap enough to run every round once the risk
  is known.
- **`engineering_conclusion="undetermined"` is not a downgrade to avoid — it's the correct outcome for
  an honestly-scoped judgment, and the taxonomy label around it (`asserted_solution`) still holds.**
  The final open question the reviewer raised — does labeling this an `asserted_solution` still imply
  more certainty than the record actually has — resolves once you notice that `engineering_conclusion`
  is exactly the field Hawkins' framework provides for recording "this evidence does not yet establish
  sufficiency." A record can honestly assert a solution and honestly say its own evidence falls short
  of settling it; that's not a contradiction, it's the framework working as intended.

## Verification

294 tests passing (unchanged from Chapter 5's baseline), 0 ch06 lint hits (20 before: `tall-named`
and em-dash violations, closed as a byproduct of the rewrite), `glossary check` clean, 0 co-author
trailers across 10 integrated commits (stripped from every round's commits, tree-hash verified each
time), 0 em-dashes in every touched learner-facing file. `conformance.report` shows both `port-type`
and `satisfaction-claims-evaluated` reporting `passed` non-vacuously — the first time this chapter's
own fixture has been clean enough for either check to actually run. Local book build clean; a
byte-for-byte fresh-execution-versus-committed-output diff across all three notebooks confirmed zero
differences before merge. Worktree and branch cleaned up after merge (`35d1d60`).

## Not fixed here, carried forward explicitly

- **Chapter 7's predecessor-containment gap** against the new Chapter 6 (every new element this
  chapter added) — inherits to Chapter 7's own contract.
- **`calc def DeliveredEnergy`'s placement** — still not built anywhere. DL-030 places it with
  `HeatingSystem`, and this chapter's own `GenerateHeat`/`HeatGenerator` pairing is a plausible home,
  but building it was outside this contract's scope; flagged for whichever contract eventually
  connects the energy relation to a real realization.
- **The exercise's own "claim completeness" prompt** now sits in tension with this chapter's
  corrected lesson that completeness shouldn't be claimed prematurely — a real, specific instance of
  the exercise-track's systemic drift (`decisions/next-passes.md` §7 item 9), noted here for whoever
  eventually re-derives that contract, not fixed in this one.
- **`src/toaster/query.py`'s `port_type_mismatches`** has no applicability gate — it reports `passed`
  even with zero port-typed connections to compare, contrary to DL-038(3)'s own stated design. Found
  during this chapter's review; real, pre-existing, outside this chapter's blast zone.
- **`tests/test_predecessor_containment.py`'s same-name-same-`@type` blind spot** (a changed typing
  target between two fixtures isn't caught the same way an added/removed element is) — found during
  this chapter's review; needs its own `DEFERRED.md` entry from whoever next touches that file.
