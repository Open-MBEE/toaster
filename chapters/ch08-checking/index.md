# Chapter 8 - Constraint Checking

## Purpose

This chapter asks a different question from Chapter 3's and Chapter 6's own: not "does the model's own entered value satisfy a threshold" (point evaluation, which those chapters already do), but "does a relation between two of `HeatGenerator`'s own features hold for every value its unbound feature could take" (a genuinely formal, model-checked property).

After completing this chapter, the model has grown by one new construct, `deliveredEnergyBoundedBySupply`, a real SysML `assert constraint` stating the conservation entailment that Chapter 7's `efficiencyBounded` and `deliveredEnergy` already imply, and proved for every value of efficiency, power and duration a companion restatement admits by a real Z3-backed solver (`sysml-toolkit`'s `verify --solve`, wrapped by `toaster.modelcheck`), not evaluated at one point.

## Ingredients

| Notebook | Concept |
|---|---|
| [01 - A formal property, proved not evaluated](01-invariant-def.ipynb) | State `deliveredEnergyBoundedBySupply` as a real SysML constraint on `HeatGenerator`'s own conservation entailment; confirm it is really in the loaded model. |
| [02 - Proof, point evaluation, and a genuine violation](02-violation-witness.ipynb) | Contrast `verify_holds()`'s universal proof with `verify_satisfaction()`'s point evaluation of the model's existing claims; show the loop catching a deliberately broken variant of the entailment as `violated`; record the proof as engineering evidence. |
| [03 - Stale record detection](03-revision-flow.ipynb) | Loosen the efficiency bound the proof protects; show `check_stale()` marking the existing record for re-review. |

## Equipment

See [docs/setup.md](../../docs/setup.md) for environment setup. This chapter additionally needs a local build of `sysml-toolkit`'s `sysmlv2` CLI and the `z3` binary (see `tests/test_modelcheck.py` for the exact paths this repository's own tests use); without them, `verify_holds()` cannot run.

## Method

Notebook 01 states the new formal property directly in `models/ch08-cumulative.sysml`. Notebook 02 evaluates the model's existing `assert satisfy` claims with `verify_satisfaction()` (point evaluation, unchanged since Chapter 3 and Chapter 6), proves the new property with `verify_holds()` (universal, over every value the unbound features of a small companion restatement can take), and shows a deliberately broken variant of the same shape reported `violated`, not merely undecided. Notebook 03 shows the resulting judgment record is not static: loosening the bound the proof protects makes the record's stored hash stop matching the model.

## Expected result

After running all three notebooks: `deliveredEnergyBoundedBySupply` is confirmed present in the loaded model by `model.find()` and `model.query()`; `verify_holds()` reports it `satisfied` against a companion file, proved for all values, not evaluated at one; a genuinely broken variant of the same shape is reported `violated`; `verify_satisfaction()` still reports the model's three existing claims exactly as it always has; `conformance.report()` shows `satisfaction-claims-evaluated` reporting `passed`, not `blocked`, for the first time; `check_stale()` returns `True` once the bound is loosened.

## Experiment

Try the [Chapter 8 exercise](../../exercises/ch08/exercise.ipynb): produce a violation witness for the `weak` Heater variant using `verify_satisfaction()` and demonstrate stale detection after changing the HeatingReq power threshold.
