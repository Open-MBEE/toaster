# Chapter 5: Conclusion

## What we built

The Chapter 5 model adds three constructs to the cumulative model. `model.find()` and `model.get()` are now the standard navigation layer: notebook 01 confirms they return a `Symbol` for any known qualified name and `None` (rather than an exception) for an unknown name. `HeatingSystem` becomes an abstract logical component: `abstract part def HeatingSystem :> ToastingSystem { perform action applyHeat : ApplyHeat; }`, giving it real content instead of an empty name. `allocation heatAllocation allocate ToastBread::applyHeat to Toaster::heating;` is a named, usage-level `AllocationUsage`, visible directly through `model.query()`. `DurationPort` and its conjugate connect a new port on `ControlSystem` to a new port on `HeatingSystem`, and `flow control.durationOut to heating.durationIn;` inside `Toaster` states that the duration signal `ApplyHeat` has declared since Chapter 4 now has a source. The `build_interconnection_intent()` and `render_sysmld()` functions extract that connection and render it as an SVG, displayed directly in notebook 03.

## What this establishes

The chapter answers its engineering question: the toaster model now allocates a function to the logical component that performs it, and connects two logical components through a real, port-typed interface. The allocation points at two usages, `ToastBread::applyHeat` and `Toaster::heating`, and `HeatingSystem`'s own `perform` relationship confirms it genuinely carries the function it is allocated: allocation and performance agree. The port connection gives `ApplyHeat::duration` a modeled source for the first time, closing a gap Chapter 4 left open on purpose. The staged conformance check for port-type compatibility (`opensysml-query` recipe 5) has something to test for the first time in this model, and reports the two ports as compatible.

## What comes next

Chapter 6 asks how deep the decomposition should go. It applies the same structural constructs one level down, decomposing `HeatingSystem` into its physical parts, and records a stopping judgment that ties the child-level evidence back to the parent claims.

**Exercise:** The [Chapter 5 exercise](../../exercises/ch05/exercise.ipynb) asks you to allocate your coffee maker's `Brew` action to its `BrewUnit`, add a `CoffeeFlow` assembly with a `pump` and a `filter`, declare a flow between them, build the interconnection intent, and confirm the endpoint paths appear correctly in the intent dict.
