# Chapter 6 — Recursive Decomposition

## Purpose

This chapter asks: how deep should the decomposition go, and how do you know when to stop?

After completing this chapter, the cumulative model has a second-level structural decomposition of `HeatingSystem` into `ResistanceCoil` and `PowerWire`, a subsystem-level requirement (`HeatingReq`), and an `asserted_inference` record (`AI-C06`) that chains the stopping judgment back to the Chapter 3 and Chapter 4 evidence.

## Ingredients

| Notebook | Concept |
|---|---|
| [01 — Subsystem Requirements](01-subsystem-requirements.ipynb) | Apply `requirement def` and `attribute :>>` override to the heating subsystem — the same two constructs from Chapter 2, one level down. |
| [02 — Second Level](02-second-level.ipynb) | Decompose `HeatingSystem` using the four structural constructs from Chapter 1: abstract def, part def, specialization, and composition. |
| [03 — Stopping Judgment](03-stopping-judgment.ipynb) | Record `AI-C06`, an `asserted_inference` that the decomposition is complete, with `premises` referencing `AS-C03` and `AI-C04`. |

## Equipment

See [docs/setup.md](../../docs/setup.md) for environment setup. No chapter-specific tools are required.

## Method

The chapter demonstrates self-similarity: the same three-notebook structure (requirement, structure, judgment) that appeared in Chapters 2–4 recurs at the second decomposition level. Notebook 01 applies the requirement and attribute override pattern to `Heater`. Notebook 02 applies the abstract-def, part-def, specialization, and composition pattern to `HeatingSystem`. Notebook 03 records the stopping judgment, which requires a non-empty `premises` list to satisfy the Hawkins §3.1 schema.

## Expected result

After running all three notebooks, `model.query()` returns `HeatingElement`, `ResistanceCoil`, `PowerWire`, and `HeatingAssembly` as `PartDefinition` elements. `model.find("ToasterDemo::HeatingReq")` returns a symbol with `kind` matching a requirement. `validate_record(stopping_judgment)` returns `[]`, and `stopping_judgment.premises` is `["AS-C03", "AI-C04"]`.

## Experiment

Try the [Chapter 6 exercise](../../exercises/ch06/exercise.ipynb): decompose `BrewUnit` into an `Impeller` and a `FilterBasket`, add a `BrewReq` requirement, and write an `asserted_inference` record claiming the decomposition is complete.
