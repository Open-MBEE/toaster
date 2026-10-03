---
title: Conclusion
---

# Chapter 4: Conclusion

## What we built

The Chapter 4 model adds `ApplyHeat`, an action definition with typed flows: bread and energy in, toast, delivered energy and loss out. `energy` and `duration` each carry an explicit `[0..*]` multiplicity, the same multiplicity a bare, unstated declaration already defaults to (SysML v2.0 formal/2026-03-02 7.6.3, 7.6.4) but which OpenSysML v0.9.0 only honors when it is written out. An asserted constraint requires `delivered` and `loss` to each be non-negative and their sum bounded by `energy`, without assuming any particular efficiency. `ApplyHeat` is nested inside `ToastBread`, the whole-system function Chapter 1 declared with no body, as its first step: `first start; then action applyHeat : ApplyHeat { in bread = ToastBread::bread; } then done;`. `energy` and `duration` stay unbound; no energy source or control function exists anywhere in the model yet. `Start`, `Finish`, and `Cancel` are item definitions naming the cycle's signals, each carrying a `doc` stating that it names a signal, not the bread or toast material flow. The Python side adds `AI-C04`, an `asserted_inference` ReviewRecord claiming the flows this worked example names are accounted for, with `AS-C03` in its `premises` list.

## What this establishes

The chapter answers its engineering question: the toaster now has one functional step, correctly typed and correctly placed. `ApplyHeat` states what the system *does*, bread and energy in, toast and accounted-for energy out, without committing to how the hardware achieves it. The balance constraint is a real, evaluable, asserted relation, not a conversion formula: it holds or fails against concrete values, catching both an overdrawn energy split and a negative-loss split, and no specific efficiency is assumed. `ApplyHeat` is reachable as `ToastBread`'s own step, which is what makes this a decomposition rather than an isolated action, and the model stays fully evaluable: `slow.cycleTime`, unrelated to `ApplyHeat`, evaluates the same 200 seconds Chapter 2 gave it. The inference record states the scope honestly: this is a flow accounting for the one function modeled, not for the toaster's full functional architecture of roughly fifteen verb-noun functions.

## What comes next

Chapter 5 asks which logical component performs this function, and how logical components connect. It introduces a named, usage-level `allocate` connecting `ApplyHeat` to the component that performs it, and a named `interface` giving `duration` a connection point between components, without yet binding it to a value.

**Exercise:** The [Chapter 4 exercise](https://github.com/Open-MBEE/toaster/blob/main/exercises/ch04/exercise.ipynb) asks you to define a new action def for your coffee maker's `BrewUnit` (not `action def Brew` — Chapter 1 already declares that at package level), whose usage nests inside `Brew`'s reopened body; name three signal item defs; probe the balance constraint's own three usages; and write an `asserted_inference` record honestly scoped to that one action's own flows, not to whether brewing as a whole is decomposed. Use the same pattern as `ApplyHeat` and `AI-C04`.
