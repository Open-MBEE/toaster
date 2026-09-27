# Chapter 1 — Conclusion

## What we built

The Chapter 1 model states the toaster's purpose and its logical composition. `ToastingSystem`, the abstract subject, performs `ToastBread`: an action with typed `Bread` in and `Toast` out flows, carrying the acceptance language ("acceptable to its user") as its `doc`. `HeatingSystem` and `ControlSystem` are concrete placeholders with no content of their own. `Toaster`, the actual whole, specializes `ToastingSystem` — inheriting the performed purpose — and composes those two subsystems as its `heating` and `control` parts; it also carries a `cycleTime` slot, typed but with no value. After notebook 04, `model.find("ToasterDemo::Toaster").parts()` returns two symbols: `heating` and `control`.

## What this establishes

The model answers Chapter 1's engineering question: a toaster is the subject that performs the purpose of transforming bread into toast, composed of a heating subsystem and a control subsystem, neither of which yet commits to a mechanism, an interface, or a value. `cycleTime` stays an empty, unit-bearing slot rather than a chosen number, because how long a cycle actually takes is a result the design will produce, not a choice made here. That separation — purpose and arrangement now, mechanisms and values later — is what makes the model a useful engineering artifact rather than a design sketch.

## What comes next

Chapter 2 asks what the toaster must do. It introduces requirements, attribute overrides for design variants, and the first engineering judgment record. The model from Chapter 1 is the starting point.

**Exercise:** The [Chapter 1 exercise](../../exercises/ch01/exercise.ipynb) asks you to model a coffee maker using the same constructs. The problem is structurally similar to the toaster but uses a different domain: declare the abstract concept, add two component types with no content yet, specialize the whole (not the parts) from the concept, and compose it into the top-level system.
