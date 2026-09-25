# Chapter 3 — Measures of Success

## Purpose

Chapter 3 asks: how do we verify that a candidate design satisfies a requirement? After completing this chapter, the model contains a requirement usage (`timely`) applied to the nominal and slow candidates, a named calculation (`DeliveredEnergy`), and a Python judgment record that claims the nominal design satisfies the requirement.

## Ingredients

| Notebook | Construct | Concept |
|---|---|---|
| [01 — requirement usage](01-moe-definition.ipynb) | `requirement` usage + `assert satisfy ... by ...` | Applying a requirement definition to named design candidates |
| [02 — calc def](02-mop-candidate-eval.ipynb) | `calc def` with `in` / `return : Real = expr` | A named, reusable calculation with typed inputs and a return expression |
| [03 — threshold judgment](03-threshold-judgment.ipynb) | `asserted_solution` ReviewRecord | A judgment record claiming that evidence directly supports a conclusion |

## Equipment

See [setup](../../docs/setup.md) to provision Python, Node, and the OpenSysML binary before running any notebook.

## Method

Notebook 01 applies the `TimelyToast` requirement definition from Chapter 2 to the nominal and slow candidates. The model now carries explicit `assert satisfy` claims for both. Notebook 02 adds `DeliveredEnergy`, a calc def that computes the thermal energy delivered in one cycle — the quantitative basis for evaluating the nominal design. Notebook 03 does not add a new SysML construct; instead it introduces the first `asserted_solution` judgment record, recording the argument that the nominal candidate satisfies the requirement.

## Expected result

The Ch3 cumulative model contains everything from Ch1-2, plus:

- `requirement timely : TimelyToast;` — the requirement usage
- `part evidence { assert satisfy timely by nominal; assert satisfy timely by slow; }` — satisfaction claims for both candidates
- `calc def DeliveredEnergy { in power : Real; in duration : Real; in efficiency : Real; return : Real = power * duration * efficiency; }` — the delivered-energy calculation

The Python side carries an `asserted_solution` ReviewRecord (`AS-C03`) with populated `rationale`, `counterevidence`, and `evidence_refs`.

## Experiment

The [chapter exercise](../../exercises/ch03/exercise.ipynb) asks you to add a requirement usage and an asserted_solution record to your coffee maker model. Work through it after completing all three notebooks.
