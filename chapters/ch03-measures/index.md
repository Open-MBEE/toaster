---
title: Overview
---

# Chapter 3: Measures of Success

## Purpose

Chapter 3 asks: how do we record and check a satisfaction claim against a requirement? After completing this chapter, the model contains a requirement usage (`timely`), a satisfaction claim folded into the failing usage's own context (`slow`), and a verification case (`TimelyToastTest`) declaring how the requirement will be checked. `nominal`'s satisfaction of `timely` is not yet claimed: `Toaster.cycleTime` has no value until a later chapter derives one.

## Ingredients

| Notebook | Construct | Concept |
|---|---|---|
| [01: requirement usage](01-moe-definition.ipynb) | `requirement` usage | Applying a requirement definition to the model, and recording whether the measure it constrains is effectiveness or performance |
| [02: satisfaction claims](02-mop-candidate-eval.ipynb) | `assert satisfy` / `assert not satisfy` | Recording, inside a usage's own context, whether it meets a requirement, and evaluating the claim |
| [03: threshold judgment](03-threshold-judgment.ipynb) | `asserted_solution` ReviewRecord | A judgment record stating what an evaluated claim supports, and what remains open |
| [04: verification def](04-verification-case.ipynb) | `verification def` + `objective { verify ... }` | A formal verification case specifying how a requirement will be checked |

## Equipment

See [setup](../../docs/setup.md) to provision Python and the OpenSysML runtime binary before running any notebook. Node.js is only needed if you also want to build the rendered book locally, not for running notebooks.

## Method

Notebook 01 applies the `TimelyToast` requirement definition from Chapter 2 to the model as `timely : TimelyToast`, then records the modeling judgment behind it: whether toast time is a [measure of effectiveness](../../docs/glossary.md#measure-of-effectiveness-moe) (the user's acceptance) or a [measure of performance](../../docs/glossary.md#measure-of-performance-mop) (an engineering figure), a case-specific decision this chapter justifies rather than assumes. Notebook 02 folds a satisfaction claim into `slow`'s own body, `assert not satisfy timely by slow`, and evaluates it against the model's own values. Notebook 03 writes the chapter's `asserted_solution` judgment record, stating what the evaluated claim supports and what it does not decide about `nominal`. Notebook 04 closes the three-part requirement anatomy (description, rationale, verification method) by adding `TimelyToastTest`: a `verification def` (§7.24) that declares the subject under test and an objective naming `timely` as the requirement to verify.

## Expected result

The Ch3 cumulative model contains everything from Ch1-2, plus:

- `requirement timely : TimelyToast;`, the requirement usage
- `part slow : Toaster { attribute :>> cycleTime = 200.0 [SI::s]; assert not satisfy timely by slow; }`, the negated satisfaction claim folded into the failing usage's own context
- `verification def TimelyToastTest { doc /* ... */ subject toaster : Toaster; objective { verify timely; } }`, the verification case (§7.24)

The Python side carries an `asserted_context` ReviewRecord (`AC-C03`) recording the MoE/MoP framing judgment, and an `asserted_solution` ReviewRecord (`AS-C03`) recording what the evaluated claim on `slow` supports and what remains open for `nominal`.

## Experiment

The [chapter exercise](https://github.com/Open-MBEE/toaster/blob/main/exercises/ch03/exercise.ipynb) asks you to add a requirement usage, record an `asserted_context` framing judgment (MoE or MoP), evaluate a negated satisfaction claim folded into a deliberately faulty candidate only, write an `asserted_solution` record for that claim, and close the requirement's anatomy with a `verification def`, to your coffee maker model. Work through it after completing all four notebooks.
