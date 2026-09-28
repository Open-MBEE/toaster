# Chapter 8 Conclusion

## What we built

`models/ch08-cumulative.sysml` adds one new construct to Chapter 7's content: `deliveredEnergyBoundedBySupply`, an `assert constraint` on `HeatGenerator`'s own conservation entailment (`efficiencyBounded` together with `deliveredEnergy`'s own definition guarantee delivered energy never exceeds supplied energy). `toaster.modelcheck.verify_holds()` proves it `satisfied` for every value of efficiency, power and duration a companion restatement of the construct admits, using `sysml-toolkit`'s real `verify --solve` (Z3), and reports a deliberately broken variant of the same shape as `violated`. A ReviewRecord (`AS-C08`) cites that proof as its evidence.

## What this establishes

This is the first chapter that genuinely delivers a model-checked property, not a point evaluation. `verify_satisfaction()` (Chapter 3 onward) tells you whether one candidate's own fixed values satisfy a requirement, and stays exactly that kind of check; `verify_holds()` tells you whether a relation holds for every value its unbound features could take. The two are not the same kind of evidence, and this chapter keeps them distinguished throughout: the model's existing `not satisfy timely by slow`, `satisfy heatGenerationReq by rated` and `not satisfy heatGenerationReq by weak` claims are still observed at one point each (`cycleTime` is not yet derived from anything, so the `timely` claims show evaluation mechanics, not a finding about the toaster's actual timing; `HeatGenerator::power` is a chosen physical rating, so the `heatGenerationReq` claims are legitimate feasibility checks of a design choice); `deliveredEnergyBoundedBySupply` is proved for every value its unbound features admit. `conformance.report()`'s `satisfaction-claims-evaluated` check, unscheduled no longer, now reports `passed` on a model that is both language conformant and free of the false claims earlier chapters once carried.

## What comes next

Chapter 9 broadens the analysis again: instead of one proved property and a handful of point-evaluated claims, it queries every requirement declaration and every satisfy relationship in the model to produce a coverage table showing which requirements have been addressed and which have not.

## Exercise

See `exercises/ch08/exercise.ipynb`: produce a violation witness for the `weak` Heater variant and demonstrate stale detection after changing the HeatingReq threshold.
