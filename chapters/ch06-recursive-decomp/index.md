---
title: Overview
---

# Chapter 6: Recursive Decomposition

## Purpose

This chapter asks: for one branch of `ApplyHeat`'s own decomposition, what does the recursion's stopping rule actually show, and what does it not yet show, one level below where Chapter 5 stopped?

After completing this chapter, the cumulative model has a real second-level function (`GenerateHeat`, nested inside `ApplyHeat`, committed to no energy form), an abstract logical carrier for it (`HeatGenerator`, performing the function and exposing an energy port, also uncommitted), a usage-level allocation between them, a requirement stated on the carrier, a recorded mechanism selection, a concrete physical realization the selection licenses (`ResistanceCoil`), two real candidates checked against the requirement, and a stopping judgment that states plainly what this one branch does and does not establish.

## Ingredients

| Notebook | Concept |
|---|---|
| [01: level-2 function and logical carrier](01-subsystem-requirements.ipynb) | Nest `GenerateHeat` inside `ApplyHeat`, the same way `ApplyHeat` nests inside `ToastBread`, and give it a logical carrier, `HeatGenerator`, one level below `HeatingSystem`; neither commits to an energy form or mechanism. |
| [02: level-2 physical realization](02-second-level.ipynb) | State the requirement `HeatGenerator`'s rating is checked against, record the measure framing and the mechanism selection that requirement raises, then build `ResistanceCoil`, the concrete realization the selection licenses. |
| [03: stopping judgment](03-stopping-judgment.ipynb) | Record `AI-C06`, an `asserted_inference` checked against real analysis on the loaded model, stating plainly what this one branch establishes and what it does not. |

## Equipment

See [Getting Started](../../docs/setup.md) for environment setup. No chapter-specific tools are required.

## Method

The chapter carries one branch of the recursive step through all three layers at the second level, not straight from a level-1 logical grouping to level-2 physical parts, and not by naming a mechanism-specific part before the argument for it exists. Notebook 01 builds the function and the abstract carrier that performs it, allocated at the usage level, both energy-neutral. Notebook 02 states the requirement first, records why the requirement is a measure of performance and why a resistive mechanism is chosen, then builds the concrete realization that selection licenses. Notebook 03 asks what the recursion's own stopping rule shows for this one branch, against real evidence gathered from the loaded model, and states plainly what it does not yet show.

## Expected result

After running all three notebooks, `perform_relationships(model)` includes `HeatGenerator` performing `GenerateHeat`; `find_allocations(model)` includes `HeatingAssembly::heatGenAllocation`, nested in `HeatingAssembly` itself, with source end `['HeatingSystem::applyHeat', 'ApplyHeat::generateHeat']` (the inherited `applyHeat` usage, then its own nested `generateHeat` step) and target end `['HeatingAssembly::heatGen']`; `model.eval("ToasterDemo::heatGenerationReq(ToasterDemo::rated)")` is `True` and the same call on `weak` is `False`; and `validate_record()` returns `[]` for `AC-C06`, `AS-C06` and `AI-C06`.

## Experiment

Try the [Chapter 6 exercise](https://github.com/Open-MBEE/toaster/blob/main/exercises/ch06/exercise.ipynb): nest `MoveWater` inside `ApplyWater`, give it an abstract carrier `WaterMover`, build `BrewAssembly :> BrewUnit` composing it with a usage-level allocation, and state a `BrewReq` requirement on `WaterMover` itself, following the same level-2 function/carrier/allocation/requirement pattern this chapter builds for `GenerateHeat`/`HeatGenerator`; record a measure-framing and a mechanism-selection judgment the requirement raises (`Impeller`, built only after the selection is argued), and write an honestly scoped `asserted_inference` record stating what the decomposition establishes and does not.
