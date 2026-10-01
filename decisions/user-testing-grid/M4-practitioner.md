# Grid cell M4-practitioner — local clone exercise, SE Practitioner persona, Chapter 8

## First-run-unmodified result (required, separate from the fill-in attempt)
Ran `exercises/ch08/exercise.ipynb` top to bottom, unmodified, via `jupyter nbconvert --execute`.
Cell 1 (model load): `Model ok: False`, two diagnostics — `(line 2) expected '{' or ';' after declaration`, `(line 2) expected a namespace member` (the placeholder `# Your solution here` body is not valid SysML, as expected). No assertion here; execution continues.
Cell 2 (narrative, no code).
Cell 3: `sym = model.find("CoffeeDemo::deliveredMassBoundedBySupply"); assert sym is not None, "deliveredMassBoundedBySupply not found in the loaded model"` — raises uncaught `AssertionError: deliveredMassBoundedBySupply not found in the loaded model`. Execution halts here under a normal "Run All"; nothing after this cell runs.

## Did it feel like a bug, or like an obvious "fill this in" state?
Genuinely mixed, and that's the finding. Cell 1's `Model ok: False` with diagnostics reads exactly like Ch1's exercise — an expected, informative "you haven't written anything yet" state. But Cell 3 immediately converts that into a raw Python traceback with no framing, one cell after a println pattern that trained me to expect graceful printed status. Ch1's exercise never asserts past an unfilled placeholder; it only prints `ok` and conditionally inspects with `if cm:`. Hitting an uncaught `AssertionError` two cells later, with no comment preparing me for it, reads as "the exercise itself is broken" on first encounter — I only recognized it as a placeholder consequence because I already knew Ch1's gentler pattern and could infer the asymmetry.

## Fill-in attempt
Mirroring Ch8-01's `HeatGenerator`/`heatGenCheck` pattern (abstract part def with free attributes, a top-level unbound usage, a duration attribute, one `assert constraint` whose antecedent restates the bound and whose consequent restates the calc), I wrote a self-contained `WaterMover` with `throughput`, `transferEfficiency`, `transferEfficiencyBounded`, `deliveredMass`, plus `moverCheck`/`moverCheckDuration`/`deliveredMassBoundedBySupply`. First attempt failed: unqualified `DimensionOneValue` (works inside `ch07-cumulative.sysml`'s own import context, not reproducible standalone) needed `MeasurementReferences::DimensionOneValue`, and an `SI::'kg/s'` unit literal didn't resolve. After removing/qualifying those, `model.ok == True`. The exercise's own hint text ("mirroring efficiency/deliveredEnergy exactly") doesn't flag that the qualified-name requirement differs outside the chapter's own fixture file — Ch8 doesn't teach this, Ch7's own notebooks never show it either. I did not attempt the `verify_holds()` companion cells (needs the local `sysmlv2`/Z3 binaries, which errored in the first-run pass with build/FD-poll noise unrelated to my content).

## Structured findings
- id: M4-practitioner-01
  severity: blocking
  location: exercises/ch08/exercise.ipynb, cell 3 (In[2] in executed output)
  quote: "AssertionError: deliveredMassBoundedBySupply not found in the loaded model"
  expected: An unfilled placeholder fails the same gracefully-printed way Ch1's exercise does (print + conditional check), or cell 3 is commented to say the assert is deliberate and expected to fail until filled in.
  actual: Raw uncaught AssertionError halts the notebook two cells after a printed-status pattern that trained the opposite expectation.
- id: M4-practitioner-02
  severity: confusing
  location: exercises/ch08/exercise.ipynb, `source` placeholder / scalar-type usage
  quote: "mirroring efficiency/deliveredEnergy exactly"
  expected: Mirroring the chapter's dimensionless-attribute declaration works unchanged in a standalone companion.
  actual: Unqualified DimensionOneValue resolves inside ch07/ch08-cumulative.sysml's own import context but not standalone; needed MeasurementReferences::DimensionOneValue, not mentioned by either chapter.
- id: M4-practitioner-03
  severity: positive
  location: exercises/ch08/exercise.ipynb, cell 1
  quote: "Model ok: False"
  expected: Placeholder content fails to parse with informative diagnostics.
  actual: Matches exactly, same as Ch1 and other chapters' exercises.

## Overall
NEEDS-FIX — confirmed: the uncaught AssertionError in cell 3 is real and reproduces on a fresh, completely unmodified run; it is a scaffolding inconsistency against Ch1's own gentler pattern, not a sign the exercise concept is unreachable.
