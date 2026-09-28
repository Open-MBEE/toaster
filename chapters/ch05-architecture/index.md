# Chapter 5: Architecture and Allocation

## Purpose

This chapter asks: which logical component performs which function, and how are components connected?

After completing this chapter, the cumulative model has a named, usage-level `allocate` connecting `ApplyHeat` to the logical component that performs it, and a real port-typed interface between `ControlSystem` and `HeatingSystem`. You can also inspect any model element by qualified name using `model.find()` and `model.get()`.

## Ingredients

| Notebook | Concept |
|---|---|
| [01: Model Navigation](01-concept-selection.ipynb) | Navigate model elements by qualified name using `model.find()` and `model.get(fqn)`. |
| [02: Allocate](02-allocate.ipynb) | Make `HeatingSystem` an abstract logical component that performs `ApplyHeat`, and assign it a named, usage-level allocation. |
| [03: Interfaces](03-interfaces.ipynb) | Declare a port-typed interface between `ControlSystem` and `HeatingSystem` and render the interconnection diagram. |

## Equipment

See [docs/setup.md](../../docs/setup.md) for environment setup. No chapter-specific tools are required beyond the base installation.

## Method

The chapter begins with navigation: before adding new relationships, you need to locate elements reliably. Notebook 01 shows how qualified names anchor every subsequent operation in this chapter and in Chapter 6.

Notebook 02 introduces `allocate`, which answers the question "which component is responsible for which function?" `HeatingSystem` becomes an abstract logical component that performs `ApplyHeat` (Chapter 4's function, nested inside `ToastBread`), and a named allocation usage connects the two directly.

Notebook 03 introduces `port def` and `interface`, which answer "what connection point does each component expose, and how are they joined?" `HeatingSystem` and `ControlSystem` each get a port, joined by a named interface showing where the `duration` signal `ApplyHeat` has declared since Chapter 4 would flow, once something produces it. It closes with `build_interconnection_intent()` and `render_sysmld()`, which extract the connection from the model and render it as a displayed SVG diagram.

## Expected result

After running all three notebooks, the cumulative model contains the complete Ch1-Ch5 model including `abstract part def HeatingSystem` (performing `ApplyHeat` through a `perform` relationship, no supertype), `allocation heatAllocation allocate ToastBread::applyHeat to Toaster::heating;`, a `DurationPort` typing a new port on each of `ControlSystem` and `HeatingSystem`, and `interface durationInterface connect control.durationOut to heating.durationIn;` inside `Toaster`, joining those two ports. `build_interconnection_intent(model, "ToasterDemo::Toaster")` returns a dict with two parts and one connection, and the rendered interconnection diagram is visible in notebook 03's own output.

## Experiment

Try the [Chapter 5 exercise](../../exercises/ch05/exercise.ipynb): allocate your coffee maker's `Brew` action to its `BrewUnit`, then add a `CoffeeFlow` assembly with `pump` and `filter` parts connected by a flow, and render the interconnection diagram.
