# Chapter 3 — Conclusion

## What we built

The Chapter 3 model applies the `TimelyToast` requirement to the nominal and slow candidates via a `requirement timely : TimelyToast` usage and explicit `assert satisfy` claims. It also adds `DeliveredEnergy`, a calc def that computes thermal energy as `power * duration * efficiency`. The Python side adds `AS-C03`, an `asserted_solution` ReviewRecord that records the argument: 120 s is within the 180 s bound by a 60 s margin, and the slow variant at 200 s violates it.

## What this establishes

The chapter answers its engineering question: the model now records *which* candidate satisfies the requirement and *why* that judgment holds. The assert-satisfy claims are formal; the ReviewRecord makes the reasoning visible and auditable. That pairing — formal claim plus recorded argument — is what distinguishes an engineering judgment from an assertion.

## What comes next

Chapter 4 asks how the system performs its function step by step. It introduces `action def` for functional decomposition, `item def` for typed flows, and the first `asserted_inference` record — the judgment that a chain of child claims supports a parent claim.

**Exercise:** The [Chapter 3 exercise](../../exercises/ch03/exercise.ipynb) asks you to add a `TemperatureReq` usage to your coffee maker model, assert satisfaction for the nominal and hot candidates, and write an `asserted_solution` record for the nominal claim. Use the same pattern as `timely` and `AS-C03`.
