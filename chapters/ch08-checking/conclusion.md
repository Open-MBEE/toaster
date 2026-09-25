# Chapter 8 Conclusion

## What we built

`verify_satisfaction()` evaluates the model's `assert satisfy timely by nominal` and `assert satisfy timely by slow` declarations, returning Verdict objects with `holds` fields. A violation witness ReviewRecord (`AS-C08`) captures the slow variant's failure with a non-empty `counterevidence` field. The stale detection pattern (`check_stale()`) is exercised by changing the requirement threshold and confirming that the stored hash no longer matches.

## What this establishes

The checking results show that the requirement boundary is real and correctly encoded: the nominal design (cycleTime=120) satisfies TimelyToast; the slow design (cycleTime=200) does not. The violation witness is formal engineering evidence, not just a test result — it is attached to the model by `model_ref`, scoped by `scope`, and bounded by `counterevidence` and `residual_uncertainties`.

## What comes next

Chapter 9 broadens the analysis: instead of checking two specific candidates, it queries all requirement declarations and all satisfy relationships to produce a coverage table that shows which requirements have been addressed and which have not.

## Exercise

See `exercises/ch08/exercise.ipynb`: produce a violation witness for the `weak` Heater variant and demonstrate stale detection after changing the HeatingReq threshold.
