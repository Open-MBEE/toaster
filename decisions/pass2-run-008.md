# Pass 2, run 008: conformance CLI and predecessor-containment check (2026-09-27)

Contract PASS2-010. Builder Sonnet 5, reviewer Opus 5.5 (independent, different model each round), two rounds (one FAIL-free PASS with test-coverage gaps, one push-back to close them).

## What shipped

- `scripts/check_conformance.py`: runs `toaster.conformance.report()` against every `models/chNN-cumulative.sysml` (or named files), default stage `(chapter, 0)`, `--stage CH,SEC` override, `--json`, exit 1 only on a "failed" check. Confirmed against the real repo: ch05-ch08 show the known gap findings and `blocked` statuses; ch01-ch04 are clean and `open` (nothing scheduled).
- `scripts/check_construction.py` gained a predecessor-containment check: every named element in ch(N-1) must appear in chNN with the same qualified name and `@type`. Wired into the existing `--check` flow. It correctly and immediately caught a REAL pre-existing defect: ch04-cumulative.sysml silently drops ch03's `TimelyToastTest` verification def and its subject (decisions/audits/ch04-layer-audit.md F-5). `check_construction.py --check` now exits 1 where it previously reported "6 chapters consistent" — this is the check working, not a regression; DEFERRED.md D-022 records it. All other adjacent chapter pairs (1→2, 2→3, 4→5, 5→6, 6→7, 7→8) confirmed clean.

## Review

Round 1: PASS on substance (no code defects), but the reviewer found real test-coverage gaps — most notably nothing tested the @type-mismatch branch the contract explicitly named, and the CLI's default-stage/--stage/"passed"-exit-0 paths were unasserted. Also caught, before it shipped: the builder's own first implementation used the wrong JSON field (`name` instead of `declaredName`) for element identity, which would have silently reported zero findings everywhere — caught by the builder itself, by actually running the check rather than trusting inspection, before the first hand-back.

Two open questions from the reviewer were resolved by the orchestrator directly (tool-design tradeoffs, not layer/definition judgment, so no ACE involvement): exit-code semantics stay contract-as-written (exit 1 only on "failed"; today vacuous since REGISTRY has nothing scheduled, which is expected and documented); predecessor containment stays named-only (the doc/rationale blind spot is recorded next to D-022, not fixed here).

Push-back closed all four coverage gaps with tests, each verified to kill the specific mutant the reviewer identified (type-check dropped, wiring removed, unnamed-elements-included). No behavior changed, only test coverage and two documentation corrections (a wrong file path reference, an inaccurate claim in D-022 about which chapter pairs run under bare `--check`).

## What the run showed

- **A builder catching its own bug before handoff is the system working as intended** — the `declaredName` fix happened because the builder ran the check against real data instead of trusting a field-name guess.
- **"Do not fix the model" was honored cleanly.** The predecessor check surfacing a real defect (not a bug in the check) was correctly recognized by both builder and reviewer as the intended, desired outcome — nobody tried to paper over it.
- **Two rounds only, both clean** — no crashes, no inverted logic, no false positives this time, unlike PASS2-009's four rounds. The contract was more precisely scoped (explicit non-goals naming exactly what not to touch) and that likely explains the cleaner run.

## Known remaining gaps (recorded, not blocking)

- `check_construction.py --check` (no `--chapter`) still doesn't reach chapters 6 and 8 by default — pre-existing `CONSTRUCTION_NOTEBOOKS` gap, unrelated to this contract, flagged as a follow-up.
- One pre-existing ruff `BLE001` on an untouched line in `check_construction.py` — left alone per the "don't reformat existing lines" non-goal; a lint-cleanup task's job.
- Predecessor containment does not catch unnamed-element drops (the `TimelyToast` doc half of F-5) — by design (named elements only), recorded next to D-022.
