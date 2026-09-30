# Chapter 3: Conclusion

## What we built

The Chapter 3 model applies `TimelyToast` to the model as a `requirement timely : TimelyToast` usage. `slow`, Chapter 2's deliberately injected fault (`cycleTime` fixed at 200 s), now carries `assert not satisfy timely by slow`, folded into its own body and evaluated against the model's own values: it holds, confirming the negated claim. `TimelyToastTest`, a `verification def` with an `objective { verify timely; }`, declares how the requirement would be checked, and is never run in this chapter. On the Python side, `AC-C03` records the judgment that `timely` is framed as a measure of effectiveness, and `AS-C03` records what the evaluated claim on `slow` supports.

## What this establishes

The chapter answers its engineering question: the model now records and evaluates a satisfaction claim against a requirement, using `slow` as the requirement's demonstrated failing branch. It does not yet claim that `nominal` satisfies `TimelyToast`: `Toaster.cycleTime` carries no value absent a mechanism-and-energy-balance derivation, so `nominal`'s status stays genuinely open rather than asserted from an unset default. That restraint, an evaluated claim on `slow`, no claim on `nominal`, and a verification case that states how the requirement will eventually be checked, is what distinguishes an engineering judgment from an assertion.

## What comes next

Chapter 4 asks how the system performs its function step by step. It introduces `action def` for functional decomposition and `item def` for typed flows.

**Exercise:** The [Chapter 3 exercise](../../exercises/ch03/exercise.ipynb) asks you to add a `TemperatureReq` usage to your coffee maker model, fold a negated satisfaction claim into the `hot` usage only (not `nominal`, whose `brewTemp` is unbound), write an `asserted_solution` record for that claim, and close the requirement's anatomy with a `verification def`. Use the same pattern as `timely`/`slow` and `TimelyToastTest`.
