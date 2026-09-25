# Chapter 5 — Architecture

## Purpose

This chapter asks: which structural parts perform which functions, and what flows between them?

After completing this chapter, the cumulative model has two new relationship types — `allocate` for function-to-structure assignment and `flow` for item interfaces — and you can inspect any model element by qualified name using `model.find()` and `model.get()`.

## Ingredients

| Notebook | Concept |
|---|---|
| [01 — Concept Selection](01-concept-selection.ipynb) | Navigate model elements by qualified name using `model.find()` and `model.get(fqn)`. |
| [02 — Allocate](02-allocate.ipynb) | Assign a behavioral element to a structural part using `allocate X to Y`. |
| [03 — Interfaces](03-interfaces.ipynb) | Declare item flows between parts using `flow X.port to Y.port`; render an interconnection SVG. |

## Equipment

See [docs/setup.md](../../docs/setup.md) for environment setup. No chapter-specific tools are required beyond the base installation.

## Method

The chapter begins with navigation: before adding new relationships, you need to locate elements reliably. Notebook 01 shows how qualified names anchor every subsequent operation in this chapter and in Chapter 6.

Notebook 02 introduces `allocate`, which answers the question "which part is responsible for which function?" by creating a formal assignment between `ApplyHeat` and `HeatingSystem`.

Notebook 03 introduces `flow`, which answers "what passes between parts?" by declaring a bread item flow between `BreadLoader` and `BreadEjector` in a new `BreadHandling` assembly. It closes with `build_interconnection_intent()` and `render_sysmld()`, which extract the flow endpoints from the model's JSON export and render an SVG interconnection diagram.

## Expected result

After running all three notebooks, the cumulative model contains the complete Ch1–Ch5 model including `allocate ApplyHeat to HeatingSystem`, three new part definitions (`BreadLoader`, `BreadEjector`, `BreadHandling`), and a `flow loader.bread to ejector.bread` declaration. `build_interconnection_intent(model, "ToasterDemo::BreadHandling")` returns a dict with two parts and one flow, and `render_sysmld()` produces a valid SVG.

## Experiment

Try the [Chapter 5 exercise](../../exercises/ch05/exercise.ipynb): add a `CoffeeFlow` assembly with `pump` and `filter` parts, declare a flow between them, and render the interconnection diagram.
