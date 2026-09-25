# Chapter 7 — Execution and Experiments

## Purpose

This chapter asks: does the toaster model behave correctly when we execute it, and does the HeatingSystem deliver enough energy across the operating range?

After completing this chapter, the cumulative model has a `state Cycle` that captures the toaster's discrete operating modes, a sympy-bound energy expression checked against the 67200 J reference value, and a matplotlib figure showing energy vs. heater power with the design threshold marked.

## Ingredients

| Notebook | Concept |
|---|---|
| [01 — Symbolic energy binding](01-calc-energy.ipynb) | Bind `DeliveredEnergy` to a sympy expression; verify the 67200 J reference value with lambdify and `model.eval()`. |
| [02 — State machine traces](02-state-traces.ipynb) | Introduce `state Cycle` with transitions (construct 13); simulate normal and cancel scenarios with `execute_state`. |
| [03 — Parameter sweep](03-param-sweep.ipynb) | Sweep heater power with `sweep_1d`; plot energy vs. power and mark the design threshold. |

## Equipment

See [docs/setup.md](../../docs/setup.md) for environment setup. Chapter 7 requires `sympy`, `numpy`, and `matplotlib` (all in `pyproject.toml`).

## Method

Notebook 01 establishes the sympy binding and reference value — the anchor for all downstream numerical claims. Notebook 02 introduces the state machine and shows that `execute_state` correctly routes two distinct event sequences. Notebook 03 uses the established binding with `sweep_1d` to produce simulation evidence for the energy requirement.

## Expected result

After running all three notebooks, `model.find("ToasterDemo::Cycle")` returns a symbol with `kind='stateDef'` or equivalent. `execute_state(cycle.id, events=['Start', 'Finish'])` returns `states_visited=['idle', 'heating', 'ready']`. `Q_fn(800.0, 120.0, 0.7)` returns 67200.0. The parameter sweep figure shows the energy curve crossing the threshold between 590 W and 600 W.

## Experiment

Try the [Chapter 7 exercise](../../exercises/ch07/exercise.ipynb): adapt the symbolic binding and sweep for the coffee maker's brew energy formula.
