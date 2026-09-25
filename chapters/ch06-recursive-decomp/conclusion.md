# Chapter 6 — Conclusion

## What we built

The Chapter 6 model adds three things to the cumulative model. `HeatingReq` is a requirement definition that constrains `Heater.power >= 600.0`, with an `efficient` variant and a `weak` variant that overrides power to 400.0. `HeatingElement`, `ResistanceCoil`, `PowerWire`, and `HeatingAssembly` form a second-level structural decomposition: `HeatingAssembly` specializes `HeatingSystem` and composes both subparts. `AI-C06` is an `asserted_inference` record claiming that decomposition is complete, with `premises = ["AS-C03", "AI-C04"]` connecting it to the energy delivery evidence and the functional completeness claim.

## What this establishes

The chapter answers its engineering question: the toaster model is decomposed to a level where each allocated function maps to a structural part, and that claim is formally recorded. `ResistanceCoil` realizes heat application (the function `ApplyHeat` allocates to `HeatingSystem`); `PowerWire` delivers the electrical power input. The stopping judgment does not assert that no further decomposition is possible — it asserts that no further decomposition is *needed* for the claims at this level. The chain of premises makes the basis for that assertion auditable.

## What comes next

Chapter 7 asks how the model behaves at runtime. It binds `DeliveredEnergy` to sympy, evaluates it numerically, and runs `execute_state` to trace normal and cancel scenarios through the toaster's state machine.

**Exercise:** The [Chapter 6 exercise](../../exercises/ch06/exercise.ipynb) asks you to decompose `BrewUnit` into an `Impeller` and a `FilterBasket`, add a `BrewReq` requirement for minimum water throughput, and write an `asserted_inference` record claiming the decomposition is complete with `premises` referencing your Chapter 5 allocation exercise result.
