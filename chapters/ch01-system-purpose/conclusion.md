# Chapter 1 — Conclusion

## What we built

The Chapter 1 model contains four component type definitions and one composed system. `ToastingSystem` is abstract and documents the system purpose. `Heater` carries a `power` attribute. `HeatingSystem` and `ControlSystem` specialize `ToastingSystem`, establishing them as kinds of toasting-system components. `Toaster` composes those two subsystems and carries a `cycleTime` attribute. After notebook 04, `model.find("ToasterDemo::Toaster").parts()` returns two symbols: `heating` and `control`.

## What this establishes

The model answers Chapter 1's engineering question: a toaster is a system with two subsystems, both traceable to a common abstract concept. The structure is implementation-agnostic. It states what the system is made of, not how each part works. That separation — structure now, behavior later — is what makes the model a useful engineering artifact rather than a design sketch.

## What comes next

Chapter 2 asks what the toaster must do. It introduces requirements, attribute overrides for design variants, and the first engineering judgment record. The model from Chapter 1 is the starting point.

**Exercise:** The [Chapter 1 exercise](../../exercises/ch01/exercise.ipynb) asks you to model a coffee maker using the same four constructs. The problem is structurally similar to the toaster but uses a different domain: declare the abstract concept, add a component type with an attribute, specialize it, and compose it into a top-level system.
