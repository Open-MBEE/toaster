# Chapter 2: Conclusion

## What we built

The Chapter 2 model adds `TimelyToast`, a requirement definition whose constraint bounds its `Toaster` subject's `cycleTime` to at most 180 seconds. It also adds two named usages of `Toaster`, not design variants: `nominal`, whose `cycleTime` carries no value, and `slow`, a deliberately faulty fixture whose `cycleTime` is fixed at 200 seconds via `attribute :>>`. The Python side adds `context_record`, a `ReviewRecord` of kind `asserted_context` that records an illustrative placeholder estimate of nominal cycle time (about 120 seconds, explicitly labeled as invented for this tutorial, not drawn from any real-world source), used only as context pending the value a later chapter derives.

## What this establishes

The chapter answers its engineering question: we now have a formal requirement and two named usages built to exercise it. `nominal` carries no cycle-time value yet; `slow` is a deliberately faulty fixture whose fixed 200-second cycle time exceeds the 180-second bound, built to exercise the requirement's failing branch, not to represent a competing design. No analysis in this chapter derives a cycle time, so neither usage's relationship to the bound is reported as a settled pass/fail verdict; the context record's estimate for `nominal` is likewise conditional on its stated assumption, not a derived value. The context record makes the assumption explicit before any such comparison is made. That ordering matters: a judgment about satisfaction is only meaningful when the context is stated.

## What comes next

Chapter 3 introduces `requirement` usage (applying `TimelyToast` to the model as `timely`) and the `assert satisfy` / `assert not satisfy` idiom, which folds a satisfaction claim into a candidate's own context and evaluates it against the model's own values. It also introduces `verification def`, which declares how a requirement will be checked.

**Exercise:** The [Chapter 2 exercise](../../exercises/ch02/exercise.ipynb) asks you to add a `TemperatureReq` to your coffee maker model and write an `asserted_context` record for the `brewTemp` assumption. Use the same pattern as `TimelyToast` and `context_record`.
