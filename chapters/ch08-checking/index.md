---
title: Overview
---

# Chapter 8: Checking and Revision

## Purpose

This chapter asks a different question from Chapter 3's and Chapter 6's own: not "does the model's own entered value satisfy a threshold" (point evaluation, which those chapters already do), but "does a real-arithmetic lemma hold for every value its unbound features could take" (a genuinely formal, model-checked property).

After completing this chapter, the model has grown by one new construct, `deliveredEnergyBoundedBySupply`, a real SysML `assert constraint` stating a real-arithmetic lemma of the same shape as the conservation entailment that Chapter 7's `efficiencyBounded` and `deliveredEnergy` already imply. It is proved, for every value of efficiency, power and duration a hand-restated companion admits, by a real Z3-backed solver (`sysml-toolkit`'s `verify --solve`, wrapped by `toaster.modelcheck`), not evaluated at one point. It is a hand-restated copy, not a solver-checked reference to `HeatGenerator`'s own `efficiencyBounded` or `deliveredEnergy`: this toolchain does not compose separately declared constraints, and cannot reason through a chained calc invocation (`DEFERRED.md` D-030, D-031).

## Ingredients

| Notebook | Concept |
|---|---|
| [01: assert constraint](01-assert-constraint-def.ipynb) | State `deliveredEnergyBoundedBySupply` as a real SysML constraint; confirm it is really in the loaded model. |
| [02: proof versus point evaluation](02-violation-witness.ipynb) | Contrast `verify_holds()`'s universal proof with `verify_satisfaction()`'s point evaluation; show the loop catching a fully broken variant as `violated` and a merely weakened variant as `undecided`; record the proof as engineering evidence with its own real limits stated. |
| [03: stale record detection](03-revision-flow.ipynb) | Loosen the lemma's own bound; show `check_stale()` marking the existing record for re-review. |

## Equipment

See [docs/setup.md](../../docs/setup.md) for environment setup. This chapter additionally needs a local build of `sysml-toolkit`'s `sysmlv2` CLI and the `z3` binary (see `tests/test_modelcheck.py` for the exact paths this repository's own tests use); without them, `verify_holds()` cannot run.

## Method

Notebook 01 states the new lemma directly in `models/ch08-cumulative.sysml`. Notebook 02 evaluates the model's existing `assert satisfy` claims with `verify_satisfaction()` (point evaluation, unchanged since Chapter 3 and Chapter 6), proves the lemma with `verify_holds()` (universal, over every value a small companion restatement's unbound features can take), shows a fully broken variant of the same shape reported `violated`, and shows a merely weakened variant reported `undecided`, with `holds()` correctly refusing to collapse that into a clean pass or fail. Notebook 03 shows the resulting judgment record is not static: loosening the lemma's own bound makes the record's stored hash stop matching the model.

Chapter 7's parameter sweep samples 50 specific power values and shows where a threshold is crossed among those samples; it says nothing about values it did not sample. `deliveredEnergyBoundedBySupply`, when genuinely proved, holds for every value in its stated domain at once, not just the ones anyone thought to try. That is the real difference between checking scenarios and model checking a property (AGENTS.md 1.1 item 5): simulation explores; a proof, when it succeeds, covers the whole space it is stated over.

## Expected result

After running all three notebooks: `deliveredEnergyBoundedBySupply` is confirmed present in the loaded model by `model.find()` and `model.query()`; `verify_holds()` reports it `satisfied`, with the reason text naming `z3`, proved for all values a companion restatement admits, not evaluated at one; a fully broken variant of the same shape is reported `violated`; a merely weakened variant is reported `undecided`, with `holds()` raising an inconclusive error rather than answering `True` or `False`; `verify_satisfaction()` still reports the model's three existing claims exactly as it always has; `conformance.report()` shows `satisfaction-claims-evaluated` reporting `passed`, not `blocked`, on ch08's own fixture for the first time (it was already passing on ch03 through ch07); `check_stale()` returns `True` once the lemma's bound is loosened.

## Experiment

Try the [Chapter 8 exercise](../../exercises/ch08/exercise.ipynb): it works through the same `verify_satisfaction()` and stale-detection pattern on its own, separate coffee-maker exercise model.
