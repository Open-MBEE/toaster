# Pass 4, run 007: Chapter 7 re-derivation (2026-09-28)

Contract PASS4-007. Builder Sonnet 5, reviewer Opus 5.5 (independent, different model), three review
rounds plus a fourth, narrow round applied directly by the orchestrator. Executes
`decisions/audits/ch07-layer-audit.md` against DL-018, DL-019, DL-020, DL-022, DL-030, DL-031,
DL-034, DL-036, DL-039, DL-044, DL-045. The chapter that finally builds the energy relation Chapter 3
removed and no chapter since has rebuilt, and gives `Cycle` a real owner and real behavioral content
for the first time.

## What shipped

- **Mandatory rebase.** `models/ch07-cumulative.sysml` at HEAD predated Chapters 4 through 6 entirely
  (old `ApplyHeat`, undifferentiated `HeatingSystem`, `Heater`/`HeatingElement`/`PowerWire`,
  `BreadLoader`/`BreadEjector`/`BreadHandling`, none of which exist in the current model). Rebuilt on
  the current, merged `models/ch06-cumulative.sysml`.
- **F-1/OQ-1/DL-019/DL-044 (Cycle finally gets a real owner, and the right one).** `exhibit state
  cycle : Cycle;` sits on `ToastingSystem`, the abstract subject DL-019 already named, not on
  `Toaster`, one concrete realization of it (round 2's own fix, after round 1 first put it on
  `Toaster`, following the pattern `perform action toastBread : ToastBread;` already established:
  `Toaster::cycle` does not resolve by that name, the same way `Toaster::toastBread` already does not,
  since both are inherited members of `ToastingSystem`).
- **F-2 (heating gets real behavioral content, honestly described).** `heating`'s `do action` invokes
  `GenerateHeat` (Chapter 6's typed signature), confirmed to be real execution (an unbound-parameter
  probe raises from inside the state, not silently) rather than a claim taken on faith. `GenerateHeat`
  itself still has no body, so the chapter says plainly that what changes is which mode the machine is
  in, not any computed quantity, not "the state actually generates heat."
- **F-3 (Cycle actually cycles).** `ready` and `cancelled` get untriggered completion transitions back
  to `idle`; a two-cycle run (`Start, Finish, Start, Finish`) genuinely revisits `heating` and returns
  to `idle` twice.
- **F-4/DL-039 (the real, previously untracked language-tier gap).** Confirmed `DEFERRED.md` D-023
  already covers this exact gap (added between the audit and this contract, in PASS4-000-B); no
  duplicate entry needed. `chapters/ch07-execution/02-state-traces.ipynb` is the first chapter
  notebook to demonstrate D-023's guard directly (a `Strat`/`Start` typo, undetected by OpenSysML,
  caught by `language_gap_findings`).
- **F-5/F-6/DL-030 (the core substantive addition: `calc def DeliveredEnergy` finally rebuilt, and
  genuinely bounded this time).** Landed as a **calc usage** `deliveredEnergy`, nested directly in
  `HeatGenerator`, with `power`/`duration` as free `in` parameters but no separate `efficiency`
  parameter at all: it resolves through whichever usage's own bound `efficiency` the calc is invoked
  through, so the same `efficiencyBounded` constraint (`0 <= efficiency <= 1`) that already governs
  the attribute governs every value the calc can ever use. This was not the first form tried: an
  initial version kept a separate `in efficiency` parameter alongside the bounded attribute, silently
  decoupled from it, and a round-1 reviewer probe (`deliveredEnergy(800W, 120s, 1.5)` returning
  144000 J, more than P times t) proved the bound was cosmetic. The fix (below) required an actual
  design change, not a wording patch.
- **F-7 (the figure finally renders inline).** The parameter sweep's matplotlib figure is a real
  `display_data` PNG in the notebook's own output and a real asset in the built book, not written to a
  file and closed (the pattern deferred in Ch2/Ch4/Ch6 stays deferred there; this data figure, unlike
  those structural diagrams, was judged cheap enough to fix outright).
- **F-8/DL-045 (overclaim removal).** "proves", "behaviourally consistent", "formal engineering
  evidence", and a wrong `model.find("Cycle").kind` claim (now correctly `stateUsage`) are gone. The
  chapter states precisely what a state trace is: derived from `Cycle`'s own transition table, useful
  for catching a modeling mistake in that table, not evidence about behavior in use.

## What three-and-a-fraction review rounds actually found

1. **Round 1: FAIL, one real defect plus a restated-false-claim pattern already familiar from
   Chapter 6.** The efficiency-loophole above (A1) was the substantive defect. Alongside it: five
   learner-facing claims describing an "earlier chapters" history that the current, re-derived
   Chapters 1-6 do not actually contain (`DeliveredEnergy` "removed... from `ApplyHeat`" in Chapter 3;
   a "reference value earlier chapters used" that appears nowhere in ch01-06; `Cycle` "left... a
   package-level label" by "previous chapters" when it appears in no ch01-06 fixture at all); an
   overclaim that `heating` "actually generates heat" (disproven by removing the `do action` entirely
   and getting an identical trace); and an unlabeled or falsely-cited 120 s duration assumption.
2. **Push-back and fix.** The efficiency loophole was closed by changing the model's own structure
   (calc def to calc usage, dropping the free parameter), not by adding a second, redundant
   constraint. The false-history claims were rewritten and grep-swept for other restatements (a
   discipline this project has needed since Chapter 6, applied proactively here instead of being
   caught piecemeal across several more rounds).
3. **Round 2: FAIL, narrow.** Five small wording items (a hardcoded literal that should have read from
   the model; a sweep wrongly described as varying `HeatGenerator::power` the attribute, when it
   varies the calc's own free `power` argument; a stale comment; a subject misattribution; an internal
   doc citation in learner-facing text) plus one real design question: should `Cycle` sit on `Toaster`
   or `ToastingSystem`. Ruled from already-established DL-019/DL-044 rather than as a new judgment
   call: the abstract subject, not one of its concrete realizations.
4. **Push-back and fix**, including the subject-placement move, probed first against a scratch copy
   and checked against the already-working `perform action toastBread` precedent before touching the
   committed model.
5. **Round 3: FAIL, one real but narrow finding.** The reviewer proved that `execute_state`'s
   `performer` argument has no effect on the result in OpenSysML v0.9.0 (confirmed independently by
   the orchestrator against the real committed model before ruling): a trace naming `nominal` as
   performer is identical to one naming `rated` (which exhibits nothing) or omitting `performer`
   entirely. So the chapter's own claim that naming `nominal` "runs the inherited machine through a
   real `Toaster` usage" oversold what the trace itself shows; the inheritance is a fact about the
   model's structure (`model.find`), not something the execution trace demonstrates.
6. **Applied directly by the orchestrator**, matching the pattern established at this point in Chapters
   5 and 6: a new `DEFERRED.md` entry (D-028) for the newly-found tool gap, a fix to the one
   overclaiming notebook cell, and a stale cross-reference in D-023's own PASS4-007 addendum
   (`Toaster` to `ToastingSystem`, left behind by the round-2 fix). Independently re-verified (JSON
   validity, em-dash grep, full test suite, construction check) before merge; no re-execution needed
   since only markdown cells changed.

## What the run showed

- **A bounded-attribute pattern is not automatically bounded everywhere it's used.** Attaching
  `efficiencyBounded` to `HeatGenerator::efficiency` looked, on a first read, like it satisfied DL-030;
  it took an adversarial probe (feed an out-of-range value through the *calc's own parameter*, not
  through the attribute) to show the calc's separate `in efficiency` was an unguarded side door. The
  fix that actually closes this kind of loophole is structural (tie the value to the same feature the
  constraint governs), not an additional assertion layered on top.
- **A trace that looks like it demonstrates something can be silently insensitive to the thing it's
  supposed to demonstrate.** `execute_state`'s `performer` argument doing nothing is exactly this: the
  notebook's own narration sounded reasonable, the trace ran without error, and nothing in the
  API surface hinted the argument was ignored. This was only caught because the round-3 reviewer
  removed the claimed cause (a specific performer) and got an unchanged effect, the same falsification
  discipline that caught Chapter 6's `GasBurner` counter-example and Chapter 7's own "remove the do
  action and see if the trace changes" check for F-2.
- **Confirming a premise before treating it as stale saved real work.** The audit's F-4 said no
  `DEFERRED.md` entry covered the transition-trigger gap; by the time this contract ran, one already
  did (added in a separate pass after the audit was written). The contract's own instruction to probe
  before asserting caught this directly: rather than filing a duplicate D-028-shaped entry for a gap
  that already had one, the builder verified D-023 covered the same construct and mechanism, and added
  a one-line addendum instead.
- **A design call that looks novel is sometimes just two already-ruled decisions composed.** Whether
  `Cycle` belongs on `Toaster` or `ToastingSystem` was not a new judgment call: DL-019 ("the subject")
  and DL-044 ("exhibited by the subject") already answered it once put together, the same way OQ-1's
  `HeatGenerator`-vs-`HeatingSystem` placement question in this same chapter was already settled by
  DL-030's own reasoning applied to Chapter 6's more concrete carrier.

## Verification

294 tests passing (unchanged from Chapter 6's baseline), 0 ch07 lint hits (22 before the rebuild, all
closed as a byproduct of the rewrite; the remaining 88 repository-wide are pre-existing, in Chapters
8-10 and docs), `glossary check` clean, 0 co-author trailers across 6 integrated commits (stripped
from every round, tree-hash verified each time), 0 em-dashes in every touched learner-facing file.
`conformance.report` shows both `port-type` and `satisfaction-claims-evaluated` reporting `passed`
non-vacuously, inherited clean from Chapter 6. A byte-for-byte fresh-execution-versus-committed-output
diff across all three notebooks confirmed zero differences before each of the first three rounds'
merges (the fourth round touched only markdown, no re-execution needed). Local book build clean; the
parameter-sweep figure renders as a real asset in the built HTML. Predecessor containment: ch06 to ch07
clean; ch07 to ch08 shows the expected new gap (49 elements missing from ch08's still-stale fixture,
including the renamed `deliveredEnergy` calc usage and `ToastingSystem::cycle`'s new qualified-name
owner), exactly the pattern every prior chapter's own re-derivation has closed one link at a time.
Worktree and branch cleaned up after merge (`42c603b`).

## Not fixed here, carried forward explicitly

- **`power` and `duration` stay unbounded on `deliveredEnergy`.** A negative value for either yields a
  negative energy, which is physically nonsensical and technically in tension with `ApplyHeat::balance`
  (`delivered >= 0`), but DL-030 requires only the efficiency bound, and this chapter's whole
  parameter sweep depends on `power` staying a free, independently-sweepable input. Noted as a possible
  future refinement, not fixed here to avoid scope creep beyond what was actually asked.
- **D-028 (`execute_state`'s `performer` argument has no effect), found and logged this round.** Not
  blocking, not filed upstream; the chapter's own text now states the distinction precisely instead of
  working around the gap.
- **`exercises/ch07/exercise.ipynb`'s own drift from this chapter's real content**, the same systemic
  pattern already tracked for Chapter 6 (`decisions/next-passes.md` item 15): the exercise still asks
  for a sympy symbolic binding and a `BrewCycle` skeleton with no `do action`/completion-transition
  fix analogous to this chapter's own. Logged as `decisions/next-passes.md` item 16, chapter-7-specific
  rather than folded into the generic tracking item.
- **`.claude/skills/opensysml-api/SKILL.md`'s stale engine listing** (`"check", "ir"` where the real
  v0.9.0 engine list is `check, explore, run, smt, solve, sweep, auto, all`, with no `ir` engine at
  all). Found during this chapter's review; outside builder authority, flagged for whoever next edits
  that skill.
