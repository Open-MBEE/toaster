# Pass 4, Phase 0 close-out (2026-09-27)

Infrastructure that had to be right before any chapter is re-derived. Four items, per the
proposed contract; all four done. No chapter or model content was touched.

## 1. `toaster-recipe` rewritten

Fixed the Tall-seam-naming contradiction DL-050 confirmed live: the recipe required the seam
cell to *name* "(A-F)", "(O-S)", "(E)" — exactly what AGENTS.md 1.10 forbids. Rewrote the
seam-cell template, the A6 checklist item, and the construction-cell-update section to describe
Tall's three worlds as the *author's own design lens*, never learner-facing, with the seam
addressed behaviorally instead. Same fix applied to the two other skills DL-050 named as
mandating the same pattern (`sysml-v2-toaster-model`, `tutorial-style-guide`).

## 2. `tall-named` lint widened

Extended the regex to also catch `A-F` and `O-S` (exact case), per DL-050's own recommendation.
`(E)` is correctly left unmatched (a bare letter would be unusable — false-positive prone).
Confirmed against the real repo: 72 hits now surface (up from 8 under the old, narrower rule),
matching the ACE's own estimate almost exactly. `glossary lint` isn't wired into CI as a gating
step (confirmed — only its unit tests run there), so this doesn't break CI; the hits are
correctly deferred to each chapter's own Pass 4 rewrite, not fixed here.

## 3. DL-051: SA-8 relaxed for structural increments

Escalated to Z directly (reopening a binding Standing Assumption is reserved to Z, not the ACE
or the orchestrator, per `ace-protocol`). Z's ruling: a notebook whose job is separating what one
element conflates across layers (DL-030's fix) may introduce the small set of constructs one
layer boundary genuinely requires together, rather than being forced across artificially split
notebooks or blocked by SA-8's letter. Logged as DL-051.

## 4. Docs fixes

`docs/references.md`: added SEBoK, Åström and Murray, and Sutton and Barto (all previously
missing); corrected the Douglas series from a stale "6-part" to the already-verified five parts.
`docs/glossary.md`'s "wrong H1, render support not built" note in `next-passes.md` was itself
stale — `render` support exists and the page is current, passing `glossary check`'s own
`_docs_page` check. Corrected the record rather than redoing work already done.

## 5. Ch7 trigger-resolution guard (D-023) — the long pole

Built `unresolved-transition-trigger`, a new `GapRule` in `src/toaster/conformance.py`, guarding
the gap the Ch7 audit found (OpenSysML never resolves a transition's `accept` trigger name
against a declared type). This took **four review rounds**, each catching a real defect, not
process noise:

- **Round 1**: my own citation "fix" (applied directly, no review) was itself wrong — I mis-cited
  `AcceptActionUsage` as §8.3.16 (Flow Abstract Syntax) rather than §8.3.17.2, having jumped into
  the PDF mid-section without reading its actual heading. The reviewer caught it, along with real
  functional bugs: the rule flagged several forms of valid SysML as violations (qualified names,
  named payloads, time/change triggers, non-`ItemDefinition` payload kinds).
- **Round 2**: my own design ruling (narrow scope to same-package-or-qualified-match) was also
  wrong — real chapter models universally import standard libraries (`ScalarValues`, `SI`, `ISQ`,
  `MeasurementReferences`), which the narrowed scope couldn't distinguish from a genuine
  cross-package error, producing new false positives on legitimate imports the round-1 fix had
  just resolved.
- **Round 3**: accepting a documented limitation (skip whenever *any* unresolvable import is
  present) turned out to defeat the guard's entire purpose — verified directly, injecting a
  `Start`→`Strat` typo into the real `ch07`/`ch08` fixtures gave **zero findings**, because every
  real chapter has a library import. This is the headline case D-023 exists for; a "correctly
  documented but useless" guard was not an acceptable final state.
- **Round 4**: replaced the import-based leniency with a similarity heuristic
  (`difflib.get_close_matches`, cutoff 0.8, empirically fitted against the real ch07 vocabulary
  and justified in a code comment) — a name close to something declared locally is flagged
  regardless of imports present; only a name resembling nothing local falls back to the
  import-aware leniency. Verified: the real `Start`→`Strat` injection now gives exactly one
  finding on both `ch07` and `ch08`; the legitimate library-import case (`Boolean` via
  `private import ScalarValues::*`) still correctly resolves to no finding.

Final state: 23 tests for this rule alone (up from an initial 9), all passing against the real
toolchain, not synthetic assumptions. `DEFERRED.md` D-023 updated to record the guard precisely.
Draft 9 (`decisions/gap-issue-drafts.md`) drafted for the upstream issue, its own citation
corrected to match (8.3.17.2), held for Z's review — not filed.

**Lesson, worth stating plainly:** every round's failure was a design or citation call *I* made
that turned out wrong under empirical pressure, not a builder or reviewer error — the pipeline
did exactly what it's for. The cost (four builder rounds, four review rounds) was real, and
proportionate here because this guard runs in the always-on language-conformance tier every
future chapter depends on; getting its scope wrong would have meant either silently missing the
regression it exists to catch, or silently blocking legitimate future content. Both failure modes
are worse than the cost of getting it right.

## Verification

287 tests passing (up from 261 at Pass 3's close), touched files ruff-clean, glossary check
clean, 0 co-author trailers across every commit this phase produced, worktree and branch cleaned
up.

## Next

Phase 0 is closed. Ch1's re-derivation is the next proposed contract, following the sequence in
`decisions/pass4-backlog.md`.
