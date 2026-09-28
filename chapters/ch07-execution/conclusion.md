# Chapter 7 Conclusion

## What we built

The cumulative model now has `deliveredEnergy`, a calc on `HeatGenerator` with a real, bounded `efficiency` slot (`0 <= efficiency <= 1`), and `rated`'s own concrete efficiency value. `efficiency` is not a free parameter of the calc: it is always the invoking carrier's own bound value, so the relation can never be evaluated against an efficiency `efficiencyBounded` does not also cover. `Cycle` is a real `state def`, exhibited by `Toaster` as `cycle`; its `heating` state has a `do action` that invokes `GenerateHeat`, the level-2 function Chapter 6 built (`GenerateHeat` itself has no body yet, so nothing is computed; what changes is which mode the machine is in); and `ready` and `cancelled` both transition back to `idle`, so a run completes and the machine is ready for another. A parameter sweep evaluates `deliveredEnergy` across `HeatGenerator::power`, at every point through the model rather than a formula rebuilt in Python, and marks `HeatGenerationReq`'s own 600 W threshold, read from the model.

## What this establishes

The efficiency bound is a real constraint, not a comment: it holds for `rated`'s own value and fails, witnessed by evaluation, for a value outside it, and there is no way to reach the relation with an efficiency that bypasses this check. `Toaster` now exhibits a real mode machine: `Cycle`'s traces are derived from its own transition table, not entered as a choice. Running `[Start, Finish]` and `[Start, Cancel]` shows the machine actually cycling, including a repeated run that returns to `idle` twice. These traces are specification analysis: they confirm the transition table says what it was meant to say and would catch a mistake in it, not evidence about the toaster's behavior in use. OpenSysML v0.9.0 does not resolve a transition's trigger against the item def it names; the tutorial's own guard, demonstrated directly in notebook 02, catches a typo'd trigger the tool lets through silently (`DEFERRED.md` D-023).

## What comes next

Chapter 8 checks the model's own claims against its own values: `verify_satisfaction()` on the `assert satisfy` declarations this chapter and its predecessors have built, recorded as judgment records rather than asserted as proofs.

## Exercise

See `exercises/ch07/exercise.ipynb`: bind the coffee maker's brew energy formula to sympy, add a `BrewCycle` state machine, sweep duration, and find the minimum duration that meets a 40000 J threshold.
