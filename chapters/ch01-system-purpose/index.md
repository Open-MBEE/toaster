---
title: Overview
---

# Chapter 1: System and Purpose

## Purpose

Chapter 1 asks: how do we describe a system in SysML v2 before we know how it is built? After completing this chapter, the model states the toaster's purpose as a performed, flow-typed function, and composes the toaster's logical arrangement from two subsystem placeholders.

## Ingredients

| Notebook | Construct | Concept |
|---|---|---|
| [01: abstract part def](01-abstract-def.ipynb) | `abstract part def` + `perform` + `action def` + `item def` | The system's purpose stated as a performed, flow-typed function, not a comment |
| [02: part def](02-part-def.ipynb) | `part def` | Two concrete subsystem placeholders, no attributes or hierarchy yet |
| [03: specialization](03-specialization.ipynb) | `:>` specialization | Declaring that the whole is a kind of the concept that names it |
| [04: composition](04-composition.ipynb) | `part` usage | A system that owns named instances of its subsystem types, plus an unvalued cycle-time slot |

## Equipment

See [setup](../../docs/setup.md) to provision Python and the OpenSysML binary before running any notebook.

## Method

The four notebooks build the model of the toaster, the subject the tutorial's layers describe. Notebook 01 states the toaster's purpose functionally: `ToastingSystem`, the [abstract](../../docs/glossary.md#abstract-definition) subject, performs `ToastBread`, an action with typed `Bread` in and `Toast` out flows and the acceptance language as its `doc`. Notebooks 02 through 04 build the logical composition: two concrete subsystem placeholders (`HeatingSystem`, `ControlSystem`) with no content yet, the specialization that makes the concrete whole (`Toaster`) a kind of the subject it names, and the composition that gives `Toaster` a `heating` part and a `control` part.

By the end of notebook 04, `Toaster :> ToastingSystem` performs the toasting purpose and owns both subsystems. Neither subsystem carries a [mechanism](../../docs/glossary.md#mechanism), an interface, or a value yet. That is later chapters' work, once a mechanism has been selected for each.

## Expected result

The Ch1 cumulative model contains:

- `Bread`, `Toast` (`item def`, typed flows)
- `ToastBread` (`action def`, `in bread : Bread`, `out toast : Toast`, with the acceptance `doc`)
- `ToastingSystem` (abstract, performs `ToastBread`)
- `HeatingSystem`, `ControlSystem` (concrete, bare placeholders)
- `Toaster :> ToastingSystem` (with `cycleTime : ISQ::DurationValue`, no value yet; composed of `heating` and `control`)

`model.find("ToasterDemo::Toaster").parts()` returns two part symbols after notebook 04.

## Experiment

The [chapter exercise](../../exercises/ch01/exercise.ipynb) asks you to model a coffee maker using the same constructs. Work through it after completing all four notebooks.
