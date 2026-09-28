# Chapter 7: Execution and Experiments

## Purpose

This chapter asks: what does the model actually do when it is executed, and what does the design space `HeatGenerationReq` opens actually deliver?

After completing this chapter, the cumulative model has `deliveredEnergy`, a calc on `HeatGenerator` bounded by a real efficiency constraint, and `Cycle`, a state def `Toaster` exhibits, with a `heating` state whose `do action` invokes the heat-generation step and transitions that return `ready` and `cancelled` to `idle`.

## Ingredients

| Notebook | Concept |
|---|---|
| [01: Delivered energy on the heat generator](01-calc-energy.ipynb) | Add a bounded `efficiency` and `calc deliveredEnergy` to `HeatGenerator`; query the relation and the bound through `model.eval` and `verify_constraint`. |
| [02: The toaster's own operating cycle](02-state-traces.ipynb) | Build `Cycle` as a real `state def`; have `Toaster` exhibit it; give `heating` a `do action`; add transitions that return `ready` and `cancelled` to `idle`; trace the result with `execute_state`. |
| [03: Sweeping the design space HeatGenerationReq opens](03-param-sweep.ipynb) | Sweep `HeatGenerator::power`, evaluating `deliveredEnergy` at each point through the model, and mark `HeatGenerationReq`'s own 600 W threshold, read from the model. |

## Equipment

See [docs/setup.md](../../docs/setup.md) for environment setup. Chapter 7 requires `numpy` and `matplotlib` (both in `pyproject.toml`).

## Method

Notebook 01 builds `HeatGenerator` a bounded `efficiency` slot and a `calc deliveredEnergy` that characterizes what the carrier actually delivers, with `efficiency` resolved from the carrier's own bound value rather than passed as a free argument. Notebook 02 gives `Cycle` an owner, a `heating` state whose `do action` invokes a real function, and transitions that complete what the chapter's own name promises. Notebook 03 connects the two: it sweeps the design space `HeatGenerationReq` opens and checks it against the relation notebook 01 built.

## Expected result

After running all three notebooks, `model.eval("ToasterDemo::rated.deliveredEnergy(800.0 [SI::W], 120.0 [SI::s])")` returns 67200 J; `model.find("ToasterDemo::Toaster::cycle")` returns a `stateUsage`, the usage `Toaster` exhibits; `model.execute_state("ToasterDemo::Cycle", events=["Start", "Finish"])` returns `states_visited=['idle', 'heating', 'ready', 'idle']`; and the parameter sweep's figure marks `HeatGenerationReq`'s own 600 W threshold, read from the model rather than invented in Python.

## Experiment

Try the [Chapter 7 exercise](../../exercises/ch07/exercise.ipynb): adapt the symbolic binding and sweep for the coffee maker's brew energy formula.
