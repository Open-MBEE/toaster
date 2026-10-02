---
title: Conclusion
---

# Chapter 5: Conclusion

## What we built

The Chapter 5 model adds three constructs to the cumulative model. `model.find()` and `model.get()` are now the standard navigation layer: notebook 01 confirms they return a `Symbol` for any known qualified name and `None` (rather than an exception) for an unknown name. `HeatingSystem` becomes an abstract logical component: `abstract part def HeatingSystem { perform action applyHeat : ApplyHeat; }`, giving it real content instead of an empty name. `allocation heatAllocation allocate toastBread.applyHeat to heating;`, written as a member of `Toaster` itself, is a named, usage-level `AllocationUsage`, visible directly through `model.query()`. `DurationPort` types a new port on `ControlSystem` and its conjugate `~DurationPort` types a new port on `HeatingSystem`; `interface durationInterface connect control.durationOut to heating.durationIn;` inside `Toaster` is what joins them: a named, port-typed interface, a connection whose ends are both ports. It states where the duration signal `ApplyHeat` declared in Chapter 4 would flow, once something produces it; `ApplyHeat::duration` itself is not yet bound to this port. `render_toolkit_interconnection()` shells out to sysml-toolkit's own `viz` CLI and PlantUML to render that connection as an SVG, displayed directly in notebook 03, with each conjugated port drawn as its own named box rather than collapsed into a single edge label.

## What this establishes

The chapter answers its engineering question: the toaster model now allocates a function to the logical component that performs it, and connects two logical components through a real, port-typed interface. The allocation points at two usages reachable from inside `Toaster` itself, `toastBread.applyHeat` and `heating`; `HeatingSystem`'s own `perform` relationship shows it is the same kind of action, allocated and performed by type, not a claim that the two are the same occurrence. The port connection is new structure, not new behavior: it gives the duration signal a place to enter `HeatingSystem`, but binding it to `ApplyHeat::duration` itself is later work, once a control policy exists to produce a value. The staged conformance check for port-type compatibility (`opensysml-query` recipe 5) has a real, non-vacuous pair to compare for the first time in this model: it checks that `durationIn` and `durationOut` declare related types, which they do. It does not check that the conjugation itself is correct, only that the underlying types are equal or one specializes the other.

## What comes next

Chapter 6 asks what one branch of the recursion shows one level below `HeatingSystem`. It nests a function inside `ApplyHeat`, gives it an abstract logical carrier with its own interface point, records a mechanism selection and a measure framing before specializing it with a concrete realization, checks that realization against a requirement, then records a stopping judgment stating plainly what the branch establishes and what it does not.

**Exercise:** The [Chapter 5 exercise](../../exercises/ch05/exercise.ipynb) asks you to allocate your coffee maker's `applyWater` step to `brewUnit` (both usages, not the `Brew`/`BrewUnit` definitions), add a `CoffeeFlow` assembly with a `pump` and a `filterUnit` joined by a named, port-typed interface, confirm `port_type_mismatches()` returns an empty list, navigate to it with `model.find()` (confirming `None` for a nonexistent element), build the interconnection intent, and confirm the endpoint paths appear correctly in the intent dict.
