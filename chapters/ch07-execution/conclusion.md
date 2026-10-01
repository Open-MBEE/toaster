---
title: Conclusion
---

# Chapter 7 Conclusion

## What we built

The cumulative model now has `deliveredEnergy`, a calc on `HeatGenerator` with a real, bounded `efficiency` slot (`0 <= efficiency <= 1`), and `rated`'s own concrete efficiency value. `efficiency` is not a free parameter of the calc: it is always the invoking carrier's own bound value, so the relation can never be evaluated against an efficiency `efficiencyBounded` does not also cover; `power` and `duration` stay free, queryable inputs, since exploring the power design space against `HeatGenerationReq` is this chapter's own point. `Cycle` is a real `state def`, exhibited by `ToastingSystem`, the abstract subject, as `cycle`, inherited and executable through `Toaster` and any usage of it; its `heating` state has a `do action` that invokes `GenerateHeat`, the level-2 function Chapter 6 built (`GenerateHeat` itself has no body yet, so nothing is computed; what changes is which mode the machine is in); and `ready` and `cancelled` both transition back to `idle`, so a run completes and the machine is ready for another. A parameter sweep evaluates `deliveredEnergy` across a range of its own `power` input, at every point through the model rather than a formula rebuilt in Python, and marks `HeatGenerationReq`'s own 600 W threshold on `HeatGenerator::power`, read from the model.

## What this establishes

The efficiency bound is a real constraint, not a comment: it holds for `rated`'s own value and fails, witnessed by evaluation, for a value outside it, and there is no way to reach the relation with an efficiency that bypasses this check. `ToastingSystem` now exhibits a real mode machine: `Cycle`'s traces are derived from its own transition table, not entered as a choice. Running `[Start, Finish]` and `[Start, Cancel]` shows the machine actually cycling, including a repeated run that returns to `idle` twice. These traces are specification analysis: they confirm the transition table says what it was meant to say and would catch a mistake in it, not evidence about the toaster's behavior in use. OpenSysML v0.9.0 does not resolve a transition's trigger against the item def it names; the tutorial's own guard, demonstrated directly in notebook 02, catches a typo'd trigger the tool lets through silently (`DEFERRED.md` D-023).

## What comes next

Chapter 8 checks the model's own claims against its own values: `verify_satisfaction()` on the `assert satisfy` declarations this chapter and its predecessors have built, recorded as judgment records rather than asserted as proofs.

## Exercise

See `exercises/ch07/exercise.ipynb`: add a bounded `transferEfficiency` slot and `deliveredMass` calc to the coffee maker's `WaterMover`, add a `BrewCycle` state machine, and sweep `deliveredMass`'s `throughput` argument against `BrewReq`'s own threshold, read from the model.
