# Pass 2, run 011: DL-048 executed — satisfaction-claims-evaluated scheduled (2026-09-27)

## What this was

DL-048 (Q-S, PASS2-011-C) had already determined the applicability criterion and its
current-sequence value: `satisfaction-claims-evaluated` applies from the chapter and section
that first declares an `assert satisfy` — Chapter 3, `01-moe-definition.ipynb`, where
`assert satisfy timely by nominal/slow` first appears — and explicitly assigned setting the
registry value to the orchestrator. This was mechanical execution of an already-made ruling,
not a new judgment call, so it was done directly rather than through a builder contract.

`src/toaster/conformance.py` `REGISTRY`: `satisfaction-claims-evaluated.applies_from` set from
`None` to `(3, 1)`, citing DL-048 inline. `tests/test_conformance.py`: the registration test
updated; three new tests added against the real fixtures, matching DL-048's own stated
expectation exactly: `ch03`/`ch04` (which predate the DL-039 language-tier violations) now run
for real and report the `slow` claim `failed`; `ch08` (which carries them) stays `blocked`
regardless of stage reached, because a language failure blocks every non-wont-do project check
unconditionally.

## A defect found while verifying, and fixed directly

Verifying against the real CLI (`scripts/check_conformance.py`, not just `report()` called
directly in tests) surfaced a real bug: its default per-file stage was `(N, 0)`, derived only
from the `chNN` filename prefix. A `chNN-cumulative.sysml` fixture already carries every
section of chapter N — that is what "cumulative" means — but `(N, 0)` is *before* any section
of chapter N, so it understated the fixture's own content. With the new schedule, this meant
the CLI's default invocation would report `satisfaction-claims-evaluated` as
`open: stage not reached` on `ch03-cumulative.sysml`, even though the fixture already contains
the `slow` claim the check exists to catch — the same kind of silent-gap-hiding P5 and F6
forbid for an unscheduled check, now reproduced through a stage-derivation convention instead.

Fixed directly (mechanical correctness against the CLI's own documented purpose, the same
class of fix as PASS2-012's F1–F5, not a modeling judgment call): `_stage_from_filename`'s
default section changed from `0` to a stated `END_OF_CHAPTER = 99` sentinel. Confirmed against
every real fixture: ch01/ch02 stay `open` (the check's subject doesn't exist there yet),
ch03/ch04 now report `failed` with the `slow` claim, ch05–ch08 stay `blocked` — unchanged,
since a language failure overrides stage entirely. The CLI's exit code is now 1 on the
committed models, correctly: a real, previously-hidden defect (Chapter 3's `slow` fixture
failing its own requirement) is now visible in default output, exactly as scheduling the check
was meant to achieve.

`tests/test_check_conformance.py`'s module docstring (written when both checks were
unscheduled, claiming the real REGISTRY "can never itself produce a 'failed' status") and its
default-stage test were both stale against this change and updated.

## Verification

260 tests passing (3 net new), ruff clean, `glossary check` clean, no co-author trailers.
`scripts/check_conformance.py` run against all eight committed fixtures with no arguments,
output matching DL-048's description exactly.

## Lesson

Verifying a ruling against the real CLI, not just the library function `report()` in isolation,
is what surfaced this — the same pattern as PASS2-012's `--ranges` bug: a contract or ruling
stated at the library level can still be silently defeated by an untouched adjacent layer (a
CLI's own default-argument convention) that nothing in the ruling's text mentioned checking.
