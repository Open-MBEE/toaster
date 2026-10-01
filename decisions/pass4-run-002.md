# Pass 4, run 002: Chapter 2 re-derivation (2026-09-27)

Contract PASS4-002. Builder Sonnet 5, reviewer Opus 5.5 (independent, different model each
round), three review rounds. All five open questions the Ch2 audit raised were already ruled
(DL-023, DL-032, DL-034, DL-035) — this contract executed an already-determined target, same
pattern as Chapter 1.

## What shipped

`models/ch02-cumulative.sysml` first needed a **rebase**, not just its own fixes: the fixture was
stale, still carrying Chapter 1's *old* content (bare `doc`, backwards specialization, an unused
`Heater`, a defaulted `cycleTime`) — the exact predecessor-containment gap `pass4-run-001.md`
recorded as expected. The builder correctly rebuilt Chapter 2's base content to match the new
`ch01-cumulative.sysml`, then applied Chapter 2's own fixes on top:

- **F-5 (DL-018 recurring)**: no narration treats `nominal`'s now-valueless `cycleTime` as if it
  holds 120 s, and no verdict is asserted from comparing entered numbers.
- **F-6/OQ-7/OQ-8 (DL-032)**: `nominal` and `slow` are consistently narrated as named usages of
  the subject, never "candidates." `slow` is narrated as a deliberately injected fault for the
  requirement's failing branch — never a "design variant," "operating condition," or "assumption."
- **F-7/OQ-9 (DL-034)**: the judgment record (`context_record`/AC-001) no longer cites the model's
  own declaration as its evidence (circular, and the declaration doesn't even exist anymore).
  Rebuilt as an explicitly-labeled illustrative placeholder, honestly unsourced across every
  field, not a disguised invented citation.
- **F-8**: removed the false "any `Toaster` instance must satisfy this requirement" claim (a
  requirement definition binds a subject only via a usage plus `satisfy`, which Ch3 introduces);
  fixed which notebook actually introduces `nominal`; separated `:>>` (redefinition) from a fixed
  value binding; corrected the toaster#10/#11 "not yet supported" comments to say the gap is the
  Editor API's, not a parsing failure (verified against `DEFERRED.md` D-005/D-006 and a live load).
- **OQ-6/DL-035**: the rationale's "usability envelope for a countertop appliance" reworded to
  stakeholder/usage context, no solution-class commitment; no MoE/MoP tag added (correctly
  deferred to Chapter 3).

## Review rounds

1. **Build**, including the rebase. Self-reported, unrequested fix: a live `tall-named` lint
   violation (the "(A-F)"/"(O-S)"/"(E)" abbreviation pattern DL-050 fixed in Ch1) had leaked into
   all three Ch2 seam cells too — the audit predates that lint rule's widening, so it never caught
   this. Fixed proactively, closing 6 of the repo's 57 remaining hits.
2. **Review round 1: FAIL.** Three spots of forbidden narration survived the first pass ("design
   variants," "a specific candidate meets this constraint," "for any `Toaster`" — the same class
   of overclaim, phrased differently each time) plus a genuinely self-contradicting judgment
   record: AC-001's `criteria` field stated the invented 90-150s range as if reported from
   "manufacturer specification sheets," while its own `assumption_refs` field called the same
   number invented. The reviewer also raised three real judgment calls rather than deciding them:
   whether `slow`'s *content* (not just narration) needed to change; what AC-001 may honestly cite
   as a source; and whether to fix the exercise's own matching contradiction in the same contract.
3. **My rulings**: narration-only is the correct, sufficient scope for `slow` in Chapter 2 — DL-032's
   full "fails for a design reason" requirement can only be satisfied once an actual check runs
   against it, which is Chapter 3's `assert satisfy`/`assert not satisfy`, not Chapter 2's.
   AC-001 must never present invented data as reported fact in any field, even while admitting it
   elsewhere — every field must consistently say it's an illustrative placeholder with no real
   source. The exercise contradiction is real but systemic (`ch03`/`ch06`/`ch07`/`ch08`'s exercises
   all share the same dependency on the pattern this chapter just removed) — routed to its own
   dedicated contract (`decisions/next-passes.md` §7 item 9), not patched piecemeal here.
4. **Push-back and fix, plus a small sweep round**: all four findings fixed; AC-001 rebuilt so
   every field (claim, criteria, assumption_refs, evidence_refs, rationale, counterevidence,
   residual_uncertainties) consistently states the range as invented and unsourced.
5. **Review round 2: PASS**, with two flagged-but-accepted non-blocking observations: one hedged,
   unsourced figure remaining in AC-001's `counterevidence` field ("may require 180-240s"), and a
   forward promise to a later chapter's derivation that doesn't exist yet — both consistent with
   DL-018's own stated plan, not new defects.

## What the run showed

- **A chapter's own fixture can go stale the moment its predecessor is fixed, even before anyone
  touches the later chapter directly** — Ch2's model file was wrong from the moment Ch1's
  re-derivation landed, independent of anything this contract's own audit found. Every subsequent
  chapter contract in this sequence needs the same explicit rebase step, not just its own
  audit-driven fixes.
- **The predecessor-containment gap moves, it doesn't just close.** Closing ch01→ch02 by correctly
  carrying Chapter 1's elements forward immediately reproduced the identical gap one chapter
  later (ch02→ch03), because ch03 hasn't been re-derived yet. Recorded the same way, by the same
  precedent, without being asked to — this is now a established, expected rhythm for the rest of
  the sequence, not a one-off.
- **A systemic problem surfaced by one chapter's fix should not be patched piecemeal inside that
  chapter's own contract.** The exercise track's dependency on a pattern the main chapters no
  longer use spans four still-untouched chapters; fixing only Ch2's copy now would have made it
  inconsistent with its neighbors instead of consistent with the chapter it accompanies. Recorded
  as its own backlog item instead.
- **The same three overclaim patterns (candidate, variant, "for any X") recur chapter to chapter**
  as different phrasings of one underlying defect (DL-032's ruling), and a first pass doesn't
  reliably catch every phrasing — this is worth an explicit grep-based check in a later chapter's
  review, not just careful reading.

## Verification

287 tests passing (unchanged in count — the ch01→ch02/ch02→ch03 test swap is net-zero), touched
files ruff-clean, `glossary lint` shows zero hits from ch01 or ch02 now (57 remain in ch03-ch10,
untouched), `glossary check` clean, 0 co-author trailers across 4 commits, worktree and branch
cleaned up. Also corrected, on main directly (outside this branch): a wrong claim in
`pass4-run-001.md` (it said all 63 pre-Ch2 lint hits were "in chapters ≥3"; 6 were actually in ch02,
now closed by this run).

## Not fixed here, carried forward explicitly

- `exercises/ch02/exercise.ipynb` (and `ch03`/`ch06`/`ch07`/`ch08`'s) — routed to a dedicated
  exercise-track contract, `decisions/next-passes.md` §7 item 9.
- `scripts/check_construction.py`'s Chapter 2 context stubs still show a stale
  `cycleTime default = 120.0 [SI::s]` — a non-literal validation stand-in, doesn't affect
  correctness, left as-is (matches Chapter 1's own stub, which is similarly non-literal).
- `ch03-cumulative.sysml`'s `assert satisfy timely by slow;` (asserting satisfaction by a fixture
  built to fail) — already flagged for Chapter 3's own audit-driven contract, not touched here.
