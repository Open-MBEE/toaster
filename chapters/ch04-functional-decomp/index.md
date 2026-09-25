# Chapter 4 — Functional Decomposition

## Purpose

Chapter 4 asks: how do we describe the sequence of functional steps that transforms inputs into outputs? After completing this chapter, the model contains an `action def` with typed `in`/`out` parameters and an ordered sequence of sub-actions, item definitions naming the flows between actions, and a Python judgment record claiming the decomposition is functionally complete.

## Ingredients

| Notebook | Construct | Concept |
|---|---|---|
| [01 — action def](01-action-def-ffbd.ipynb) | `action def` with `in`/`out`, `first`/`then`, nested `action` | A named behavior with ordered sub-actions and typed parameter assignments |
| [02 — item def](02-heating-refinement.ipynb) | `item def` | Typed goods that flow between actions |
| [03 — completeness check](03-completeness-check.ipynb) | `asserted_inference` ReviewRecord | A judgment record claiming child claims support a parent claim |

## Equipment

See [setup](../../docs/setup.md) to provision Python, Node, and the OpenSysML binary before running any notebook.

## Method

Notebook 01 adds `ApplyHeat`, an action definition that sequences power input through `DeliveredEnergy` to an energy output using `first`/`then` and a nested assign step. Notebook 02 adds `Start`, `Finish`, and `Cancel` — three item definitions that name the typed flows entering and leaving the cycle. Notebook 03 introduces the first `asserted_inference` record: a parent claim (the decomposition is complete) supported by a child claim (the calculate sub-action accounts for all parameters).

## Expected result

The Ch4 cumulative model contains everything from Ch1-3, plus:

- `action def ApplyHeat { in power : Real; in duration : Real; in efficiency : Real; out energy : Real; first start; then action calculate { assign energy := DeliveredEnergy(power, duration, efficiency); } then done; }`
- `item def Start; item def Finish; item def Cancel;`

The Python side carries an `asserted_inference` ReviewRecord (`AI-C04`) with a non-empty `premises` list referencing `AS-C03`.

## Experiment

The [chapter exercise](../../exercises/ch04/exercise.ipynb) asks you to define an `EjectToast` action and write an `asserted_inference` record for your coffee maker. Work through it after completing all three notebooks.
