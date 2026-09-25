# Chapter 1 — System and Purpose

## Purpose

Chapter 1 asks: how do we describe a system in SysML v2 before we know how to build it? After completing this chapter, the model contains four part definitions and one composed system definition.

## Ingredients

| Notebook | Construct | Concept |
|---|---|---|
| [01 — abstract part def](01-abstract-def.ipynb) | `abstract part def` + `doc` | A system concept no part may directly instantiate |
| [02 — part def and attributes](02-part-def.ipynb) | `part def` + `attribute : Real default` | Named component types with numeric parameters |
| [03 — specialization](03-specialization.ipynb) | `:>` specialization | Declaring that one type is a kind of another |
| [04 — composition](04-composition.ipynb) | `part` usage | A system that owns named instances of its subsystem types |

## Equipment

See [setup](../../docs/setup.md) to provision Python, Node, and the OpenSysML binary before running any notebook.

## Method

The four notebooks build the model in one direction: from the most abstract (the system concept) toward the most concrete (the assembled system). Each notebook adds exactly one SysML construct. The model in each notebook is the full cumulative model up to that point.

By the end of notebook 04, `Toaster` owns a `HeatingSystem` part and a `ControlSystem` part, both of which specialize `ToastingSystem`. That structure is the starting point for Chapter 2.

## Expected result

The Ch1 cumulative model contains:

- `ToastingSystem` (abstract, with `doc`)
- `Heater` (with `power : Real default = 800.0`)
- `HeatingSystem :> ToastingSystem`
- `ControlSystem :> ToastingSystem`
- `Toaster` (with `cycleTime : Real default = 120.0`, composed of `heating` and `control`)

`model.find("ToasterDemo::Toaster").parts()` returns two part symbols after notebook 04.

## Experiment

The [chapter exercise](../../exercises/ch01/exercise.ipynb) asks you to model a coffee maker using the same four constructs. Work through it after completing all four notebooks.
