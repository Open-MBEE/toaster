# Chapter 8 — Constraint Checking

## Purpose

This chapter asks: do the design candidates formally satisfy the stated requirements, and how do we record what happens when they do not?

After completing this chapter, the model has been evaluated with `verify_satisfaction()`, a violation witness ReviewRecord has been created for the slow variant, and a stale record detection pattern has been demonstrated for the case where the model changes after the record was written.

## Ingredients

| Notebook | Concept |
|---|---|
| [01 — Satisfaction evaluation](01-invariant-def.ipynb) | Call `verify_satisfaction()` to evaluate `assert satisfy` declarations; confirm `nominal` holds and `slow` fails. |
| [02 — Violation witness](02-violation-witness.ipynb) | Extract the failing Verdict for `slow`; record it as a ReviewRecord with `engineering_conclusion='refuted'`. |
| [03 — Stale record detection](03-revision-flow.ipynb) | Change the requirement threshold; show that `check_stale()` fires, marking the existing record for re-review. |

## Equipment

See [docs/setup.md](../../docs/setup.md) for environment setup. No chapter-specific tools are required beyond the base environment.

## Method

Notebook 01 uses `verify_satisfaction()` — the computational evaluation of the model's `assert satisfy` declarations — to determine which candidates pass and which fail. Notebook 02 treats the failing Verdict as engineering evidence and encodes it in a ReviewRecord following the Hawkins §3.3 `asserted_solution` pattern. Notebook 03 shows that records are not static: when the model changes, `check_stale()` detects the mismatch between the stored hash and the current source.

## Expected result

After running all three notebooks, `verify_satisfaction()` returns two Verdict objects: `nominal` holds=True, `slow` holds=False. `validate_record(violation)` returns `[]`. `check_stale(record, revised_source)` returns True after the requirement threshold changes.

## Experiment

Try the [Chapter 8 exercise](../../exercises/ch08/exercise.ipynb): produce a violation witness for the `weak` Heater variant and demonstrate stale detection after changing the HeatingReq power threshold.
