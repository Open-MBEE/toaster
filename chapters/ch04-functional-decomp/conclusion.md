# Chapter 4 — Conclusion

## What we built

The Chapter 4 model adds three constructs to the cumulative model. `ApplyHeat` is an action definition that sequences three inputs (power, duration, efficiency) through a `calculate` sub-action that assigns the output (`energy`) via `DeliveredEnergy`. `Start`, `Finish`, and `Cancel` are item definitions naming the typed flows that move through the cycle. The Python side adds `AI-C04`, an `asserted_inference` ReviewRecord that claims the decomposition is complete, with `AS-C03` in its `premises` list.

## What this establishes

The chapter answers its engineering question: the toaster now has a formal functional layer. `ApplyHeat` states what the system *does* — sequence inputs through a calculation to produce an output — without committing to how the hardware achieves it. The inference record makes the completeness argument visible: every input reaches at least one sub-action, and the output is assigned. That argument rests on a prior solution claim, which is why `premises` references `AS-C03`.

## What comes next

Chapter 5 asks how functions are allocated to parts and how interfaces between parts are defined. It introduces `allocate` for assignment relationships and `flow` for item flows between parts.

**Exercise:** The [Chapter 4 exercise](../../exercises/ch04/exercise.ipynb) asks you to define an `EjectToast` action for the bread-removal path and write an `asserted_inference` record claiming the eject sequence is complete. Use the same pattern as `ApplyHeat` and `AI-C04`.
