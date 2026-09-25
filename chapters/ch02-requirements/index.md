# Chapter 2 — Requirements and Assumptions

## Purpose

Chapter 2 asks: what must the toaster do, and what do we assume about the conditions under which it operates? After completing this chapter, the model has a requirement definition, two named design variants, and the first engineering judgment record.

## Ingredients

| Notebook | Construct / operation | Concept |
|---|---|---|
| [01 — requirement def](01-requirement-def.ipynb) | `requirement def` + `subject` + `require constraint` | A formal statement of what the system must satisfy |
| [02 — attribute override](02-assumptions.ipynb) | `attribute :>>` override | Named variants that redeclare an inherited attribute value |
| [03 — asserted context](03-judgment-context.ipynb) | `asserted_context` record | An assumption that frames the requirement evaluation |

## Equipment

See [setup](../../docs/setup.md). Chapter 2 also uses `toaster.evidence.ReviewRecord`; run `uv sync --locked` to ensure the package is installed.

## Method

Notebook 01 adds the requirement to the cumulative model from Chapter 1. Notebook 02 adds the `nominal` and `slow` variants by overriding `cycleTime`. Notebook 03 introduces the first judgment record: an `asserted_context` that declares the 120-second cycle assumption before we evaluate whether any variant satisfies the requirement.

The judgment record is the first example of Hawkins et al. (2011) §3.2 in the tutorial. It does not assert that the design is correct — it asserts that the assumption is appropriate for the context.

## Expected result

After notebook 03:

- `TimelyToast` is a `RequirementDefinition` in the model
- `nominal` and `slow` are `PartUsage` instances of `Toaster`
- `slow` has `cycleTime = 200.0` via `attribute :>>`
- `context_record` is a Python `ReviewRecord` with `kind="asserted_context"` and `disposition="pending"`

## Experiment

The [chapter exercise](../../exercises/ch02/exercise.ipynb) asks you to add a temperature requirement to your coffee maker model and write the first context record for the brew-temperature assumption.
