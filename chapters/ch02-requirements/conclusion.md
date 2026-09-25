# Chapter 2 — Conclusion

## What we built

The Chapter 2 model adds `TimelyToast`, a requirement definition that constrains `cycleTime` to at most 180 seconds for any `Toaster`. It also adds two named design variants: `nominal` (default 120 seconds) and `slow` (overridden to 200 seconds via `attribute :>>`). The Python side adds `context_record`, a `ReviewRecord` of kind `asserted_context` that declares the 120-second nominal condition as an assumption appropriate for evaluating the requirement.

## What this establishes

The chapter answers its engineering question: we now have a formal requirement and two competing conditions to evaluate against it. One passes (120 seconds is within the 180-second bound), one fails (200 seconds is not). The context record makes the assumption explicit before any evaluation takes place. That ordering matters: a judgment about satisfaction is only meaningful when the context is stated.

## What comes next

Chapter 3 introduces `requirement` usage (applying a requirement to a specific part) and `calc def` (defining a reusable calculation). It also introduces `assert satisfy ... by ...`, which connects a design variant to a requirement claim.

**Exercise:** The [Chapter 2 exercise](../../exercises/ch02/exercise.ipynb) asks you to add a `TemperatureReq` to your coffee maker model and write an `asserted_context` record for the `brewTemp` assumption. Use the same pattern as `TimelyToast` and `context_record`.
