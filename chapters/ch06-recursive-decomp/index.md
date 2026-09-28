# Chapter 6: Recursive Decomposition

## Purpose

This chapter asks: what does one complete step of the recursion look like, one level below where Chapter 5 stopped?

After completing this chapter, the cumulative model has a real second-level function (`GenerateHeat`, nested inside `ApplyHeat`), an abstract logical carrier for it (`HeatGenerator`, performing the function and exposing an energy port), a usage-level allocation between them, a concrete physical realization (`ResistanceCoil`), a requirement checked against two real candidates, and three judgment records: a selection among alternatives for the mechanism, a measure-framing judgment for the requirement, and a stopping judgment tying the branch back to the recursion's own rule.

## Ingredients

| Notebook | Concept |
|---|---|
| [01: Level-2 Function and Logical Carrier](01-subsystem-requirements.ipynb) | Nest `GenerateHeat` inside `ApplyHeat`, the same way `ApplyHeat` nests inside `ToastBread`, and give it a logical carrier, `HeatGenerator`, one level below `HeatingSystem`. |
| [02: Level-2 Physical Realization](02-second-level.ipynb) | Specialize `HeatGenerator` with `ResistanceCoil`, state the requirement its rating is checked against, and record the mechanism selection and measure framing that decision raises. |
| [03: Stopping Judgment](03-stopping-judgment.ipynb) | Record `AI-C06`, an `asserted_inference` checked against real analysis on the loaded model, honest about what the branch does and does not yet establish. |

## Equipment

See [docs/setup.md](../../docs/setup.md) for environment setup. No chapter-specific tools are required.

## Method

The chapter carries the recursive step through all three layers at the second level, not straight from a level-1 logical grouping to level-2 physical parts. Notebook 01 builds the function and the abstract carrier that performs it, allocated at the usage level. Notebook 02 builds the concrete realization and the requirement it is checked against, recording the two judgments that choice raises. Notebook 03 asks whether this branch meets the recursion's own stopping rule, against real evidence gathered from the loaded model, and states plainly what it does not yet meet.

## Expected result

After running all three notebooks, `perform_relationships(model)` includes `HeatGenerator` performing `GenerateHeat`; `find_allocations(model)` includes `heatGenAllocation`, from `ApplyHeat::generateHeat` to `HeatingAssembly::heatGen`; `model.eval("ToasterDemo::heatGenerationReq(ToasterDemo::rated)")` is `True` and the same call on `weak` is `False`; and `validate_record()` returns `[]` for `AS-C06`, `AC-C06` and `AI-C06`.

## Experiment

Try the [Chapter 6 exercise](../../exercises/ch06/exercise.ipynb): decompose `BrewUnit` into an `Impeller` and a `FilterBasket`, add a `BrewReq` requirement, and write an `asserted_inference` record claiming the decomposition is complete.
