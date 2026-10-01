# Grid cell M4-novice — local clone exercise, Novice persona, Chapter 1

## First-run-unmodified result (required, separate from the fill-in attempt)

The exercise notebook runs cleanly without errors. Each of the four cells executes successfully and produces output. However, all four cells report `model.ok: False` because the placeholder comments (`# Your solution here`) contain no SysML code. The notebook does not crash; it simply demonstrates the incomplete state:

```
Step 1 ok: False
Step 2 ok: False
Step 3 ok: False
Step 4 ok: False
```

The verification code on step 4 produces no output for CoffeeMaker parts because the model is incomplete.

## Fill-in attempt

A Novice learner reading Chapter 1 can successfully apply all four constructs to a coffee maker domain without getting stuck.

Following the exact pattern from notebook 01 (item defs + action def with doc + abstract part def performing an action), I declared `Beans` and `Coffee` item defs, a `BrewCoffee` action def with a doc, and an abstract `BrewingSystem` part def that performs it. Step 1 loaded cleanly.

Step 2 followed notebook 02's pattern exactly: two bare `part def` declarations for `BrewUnit` and `HeatExchanger` terminated with semicolons, no attributes yet. Step 2 loaded.

Step 3 applied notebook 03's specialization: `part def CoffeeMaker :> BrewingSystem;` — the concrete whole specializing the abstract concept. Step 3 loaded.

Step 4 followed notebook 04's composition pattern: opening `CoffeeMaker` with a body, adding named parts (`part brew : BrewUnit;` and `part heat : HeatExchanger;`). The model loaded, and `model.find("CoffeeDemo::CoffeeMaker").parts()` returned both parts correctly.

All four steps reported `model.ok: True`. The exercise's own verification code confirmed both parts present: `['CoffeeDemo::CoffeeMaker::brew', 'CoffeeDemo::CoffeeMaker::heat']`.

## Structured findings

- id: M4-novice-01
  severity: positive
  location: cell-01 (Step 1: item defs + action def)
  quote: "item def Beans; item def Coffee; action def BrewCoffee { doc /* ... */ in beans : Beans; out coffee : Coffee; } abstract part def BrewingSystem { perform action brewCoffee : BrewCoffee; }"
  expected: "Following Chapter 1 notebook 01's pattern, this bundle of declarations should load without error"
  actual: "All four declarations loaded without error; model.ok: True"

- id: M4-novice-02
  severity: positive
  location: cell-02 (Step 2: two part defs)
  quote: "part def BrewUnit; part def HeatExchanger;"
  expected: "Two bare part definitions following Chapter 1 notebook 02's pattern should load without error"
  actual: "Both declarations loaded without error; model.ok: True"

- id: M4-novice-03
  severity: positive
  location: cell-03 (Step 3: specialization)
  quote: "part def CoffeeMaker :> BrewingSystem;"
  expected: "Specialization syntax from Chapter 1 notebook 03 should transfer to a new domain without modification"
  actual: "Specialization loaded without error; model.ok: True"

- id: M4-novice-04
  severity: positive
  location: cell-04 (Step 4: composition)
  quote: "part def CoffeeMaker :> BrewingSystem { part brew : BrewUnit; part heat : HeatExchanger; }"
  expected: "Following Chapter 1 notebook 04's composition pattern should load, and model.find().parts() should return both parts"
  actual: "Model loaded without error; model.ok: True; parts() returned ['CoffeeDemo::CoffeeMaker::brew', 'CoffeeDemo::CoffeeMaker::heat']"

- id: M4-novice-05
  severity: positive
  location: exercise.ipynb (problem statement)
  quote: "Work through these steps in the cells below: 1. Declare item defs... 2. Add `part def`... 3. Declare... 4. Complete..."
  expected: "Exercise instructions should map clearly to Chapter 1 constructs and allow a learner to transfer knowledge from chapter to exercise"
  actual: "Novice learner successfully applied Chapter 1 patterns without modification, completing all four steps as written"

## Overall

**PASS** — A Novice learner who read Chapter 1 can successfully model a coffee maker's structure using the same four constructs (item def, action def, abstract part def, specialization, composition) applied to a new domain, completing the exercise without getting stuck.
