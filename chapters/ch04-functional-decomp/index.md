# Chapter 4: Functional Decomposition

## Purpose

Chapter 4 asks: how do we describe one functional step and make it an actual step of a larger function's decomposition? A step needs typed flows in and out and a phenomena relation among them. After completing this chapter, the model contains an `action def` (`ApplyHeat`) with typed `in`/`out` parameters for bread, energy and duration, a balance-inequality constraint bounding delivered energy and loss by the energy supplied, and `ApplyHeat` nested as a step of `ToastBread` from Chapter 1. It also contains three item definitions naming the cycle's signals, and a Python judgment record claiming the flows this worked example names are accounted for.

## Ingredients

| Notebook | Construct | Concept |
|---|---|---|
| [01: action def](01-action-def-ffbd.ipynb) | `action def` with `in`/`out`, a balance constraint, nested as a step of another action | A named behavior with typed flows, a phenomena relation, and its place in a decomposition |
| [02: item def](02-heating-refinement.ipynb) | `item def` | Named signals, each stating its own denotation |
| [03: completeness check](03-completeness-check.ipynb) | `asserted_inference` ReviewRecord | A judgment record claiming child claims support a parent claim |

## Equipment

See [setup](../../docs/setup.md) to provision Python and the OpenSysML binary before running any notebook. Node.js is only needed if you also want to build the rendered book locally, not for running notebooks.

## Method

Notebook 01 adds `ApplyHeat`: bread and energy in, toast, delivered energy and loss out. A constraint states that delivered energy and loss together cannot exceed the energy supplied, without assuming any particular efficiency. `ApplyHeat` corresponds to "apply thermal energy" in the video's decomposition; the full toaster functional architecture from Part 3 covers approximately 15 verb-noun functions. This tutorial models `ApplyHeat` as one worked example to teach the `action def` construct. The same notebook nests it as an actual step of `ToastBread`, the whole-system function Chapter 1 declared with no body; the same approach applies to the remaining functions. Notebook 02 adds `Start`, `Finish`, and `Cancel`: three item definitions, each carrying a `doc` stating that it names a signal (cycle start, cycle finish, cancel request), not the bread or toast material flow. Notebook 03 introduces the first `asserted_inference` record: a parent claim (the flows this worked example names are accounted for) supported by a child claim (the balance constraint evaluates against constructed values, and `ApplyHeat` is reachable as `ToastBread`'s own step).

## Expected result

The Ch4 cumulative model contains everything from Ch1-3, plus:

- `action def ApplyHeat { in bread : Bread; in energy : ISQ::EnergyValue; in duration : ISQ::DurationValue; out toast : Toast; out delivered : ISQ::EnergyValue; out loss : ISQ::EnergyValue; constraint balance { delivered + loss <= energy } }`
- `ToastBread`'s body (Chapter 1 declared none): `first start; then action applyHeat : ApplyHeat; then done;`
- `item def Start { doc ... } item def Finish { doc ... } item def Cancel { doc ... }`, each `doc` stating the signal it names

The Python side carries an `asserted_inference` ReviewRecord (`AI-C04`) with a non-empty `premises` list referencing `AS-C03`.

## Experiment

The [chapter exercise](../../exercises/ch04/exercise.ipynb) asks you to define a `Brew` action def for your coffee maker, name its flows with `item def`, and write an `asserted_inference` record. Work through it after completing all three notebooks.
