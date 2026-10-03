---
title: Overview
---

# Chapter 2: Requirements and Assumptions

## Purpose

Chapter 2 asks: what must the toaster do, and what do we assume about the conditions under which it operates? After completing this chapter, the model has a requirement definition, two named usages of `Toaster`, and the first engineering judgment record.

A judgment record is a written, checkable record of an engineering judgment call, and following Hawkins et al. (2011) there are three kinds. An `asserted_context` records a context or assumption that is asserted to be appropriate for the argument elements it applies to. An `asserted_solution` records evidence cited as a solution that is asserted to be sufficient to support a claim. An `asserted_inference` records a claim said to be supported by other claims, with the inference asserted to be appropriate and sufficient. Notebook 03 builds the first of these, an `asserted_context`; a record states what is being asserted and does not settle the question, so its disposition stays `pending`.

## Ingredients

| Notebook | Construct / operation | Concept |
|---|---|---|
| [01: requirement def](01-requirement-def.ipynb) | `requirement def` + `subject` + `require constraint` | A formal statement of what the system must satisfy |
| [02: attribute override](02-assumptions.ipynb) | `attribute :>>` override | A named usage that redeclares an inherited attribute with a deliberately faulty value |
| [03: asserted context](03-judgment-context.ipynb) | `asserted_context` record | An assumption underlying a cycle-time estimate, not an evaluation of the requirement |

## Equipment

See [setup](../../docs/setup.md). Chapter 2 also uses `toaster.evidence.ReviewRecord`; run `uv sync --locked` to ensure the package is installed.

## Method

Notebook 01 adds the requirement definition to the cumulative model from Chapter 1, along with `nominal`, a bare usage of `Toaster` with no attribute values set. Notebook 02 adds `slow`, overriding `cycleTime` with a deliberately injected fault value that exceeds the requirement's bound: a fixture for the requirement's failing branch, not a design variant or an operating condition. Notebook 03 introduces the first judgment record: an `asserted_context` that records an assumed estimate of nominal cycle time before any comparison against the requirement is reported.

The judgment record is the first example of Hawkins et al. (2011) §3.2 in the tutorial. It does not assert that the design is correct. It asserts that the assumption is appropriate for the context.

## Expected result

After notebook 03:

- `TimelyToast` is a `RequirementDefinition` in the model
- `nominal` and `slow` are `PartUsage` instances of `Toaster`
- `nominal`'s `cycleTime` carries no value (Chapter 1 removed the default)
- `slow` has `cycleTime = 200.0` via `attribute :>>`, a fixed, deliberately injected fault value
- `context_record` is a Python `ReviewRecord` with `kind="asserted_context"` and `disposition="pending"`

## Experiment

The [chapter exercise](../../exercises/ch02/exercise.ipynb) asks you to add a temperature requirement to your coffee maker model and write the first context record for the brew-temperature assumption.
