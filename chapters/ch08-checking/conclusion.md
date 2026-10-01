# Chapter 8 Conclusion

## What we built

`models/ch08-cumulative.sysml` adds one new construct to Chapter 7's content: `deliveredEnergyBoundedBySupply`, an `assert constraint` stating a real-arithmetic lemma of the same shape as `HeatGenerator`'s conservation entailment (`efficiencyBounded` together with `deliveredEnergy`'s own definition would guarantee delivered energy never exceeds supplied energy). `toaster.modelcheck.verify_holds()` proves this lemma `satisfied` for every value of efficiency, power and duration a companion restatement admits, using `sysml-toolkit`'s real `verify --solve` (Z3), reports a fully broken variant of the same shape as `violated`, and reports a merely weakened variant as `undecided`, with a genuine Z3-found witness. A ReviewRecord (`AS-C08`) cites the proof as its evidence and states plainly what it does not establish.

## What this establishes

This is the first chapter that genuinely delivers a model-checked property, not a point evaluation, though the property proved is a hand-restated lemma, not a solver-checked reference to the model's own original elements: this toolchain does not compose two separately declared `assert constraint`s (whether sibling or inherited) and cannot reason through a chained calc invocation, confirmed directly by loosening `efficiencyBounded`'s own bound and by doubling `deliveredEnergy`'s own definition, neither of which moves the lemma's verdict at all (`DEFERRED.md` D-030, D-031). `verify_satisfaction()` (Chapter 3 onward) tells you whether one candidate's own fixed values satisfy a requirement, and stays exactly that kind of check; `verify_holds()` tells you whether a stated lemma holds for every value its unbound features could take, proved or refuted, or genuinely left undecided when it does neither. All three are real, distinguishable outcomes, and this chapter keeps them distinguished throughout: the model's existing `not satisfy timely by slow`, `satisfy heatGenerationReq by rated` and `not satisfy heatGenerationReq by weak` claims are still observed at one point each (`cycleTime` is not yet derived from anything, so the `timely` claims show evaluation mechanics, not a finding about the toaster's actual timing; `HeatGenerator::power` is a chosen physical rating, so the `heatGenerationReq` claims are legitimate feasibility checks of a design choice); `deliveredEnergyBoundedBySupply` is proved for every value its unbound features admit, within the limits stated above. `conformance.report()`'s `satisfaction-claims-evaluated` check, already scheduled from Chapter 3 onward and already passing on ch03 through ch07, now demonstrably passes on ch08's own fixture for the first time too, because the model is language conformant here and carries no false claims.

## What comes next

Chapter 9 broadens the analysis again: instead of one proved lemma and a handful of point-evaluated claims, it queries every requirement declaration and every satisfy relationship in the model to produce a coverage table showing which requirements have been addressed and which have not.

## Exercise

See `exercises/ch08/exercise.ipynb`: it works through the same `verify_satisfaction()` and stale-detection pattern on its own, separate coffee-maker exercise model.
