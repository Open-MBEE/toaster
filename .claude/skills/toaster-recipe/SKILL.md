---
name: toaster-recipe
description: Sub-notebook 7-cell template, chapter index/conclusion structure, Tall three worlds requirement, and A6 review checklist.
---

# Toaster Recipe

## Sub-notebook template — minimum skeleton

The 7 cells below are the **required skeleton**. Additional markdown+code pairs may be inserted between cells 2–4 whenever a new operation needs narration or a code cell would otherwise do two conceptual things. A6 reviews for skeleton completeness by content type, not by cell index.

| Skeleton slot | Type | Constraint |
|---|---|---|
| **Concept** | Markdown | Exactly one sentence: "This notebook introduces X; after running it you can Y." |
| **Context** | Markdown | One paragraph locating this notebook in the chapter arc. One link to prior notebook if model state carries over. |
| **Model increment** | Code | Two-phase. (1) Declare the increment: Pattern A (Editor API, returns full model) or Pattern B (SysML string fragment for gap constructs). Assign to `TOASTER_INCREMENT`; print immediately as reflection. Only in construct-introducing notebooks — see scope table in `decisions/declarative-construction-plan.md`. (2) Load full chapter cumulative from `models/chXX-cumulative.sysml`; `assert model.ok`. |
| **Negative control** | Code + Markdown | Short bad_source string. `bad = conn.load_from_content(bad_source, strict=False)`. `assert not bad.ok`. Markdown: one sentence naming the error type and pointing to the diagnostic. |
| **Demonstration** | Code + Markdown | One key operation per code cell. If two things happen, split into two cells each with its own narration markdown. |
| **Tall seam** | Markdown | Exactly one sentence naming all three worlds. |
| **Exercise pointer** | Markdown | One sentence: "Try the chapter exercise in `exercises/ch{N}/exercise.ipynb`: [one-line description]." No embedded code. |

### Construction zone — model increment pattern (construct-introducing notebooks only)

All 13 construction notebooks use SysML string fragments (Editor API gaps — see DEFERRED.md
D-004 through D-010 and skill `sysml-v2-toaster-model` for the full gap list).

**Structural rule: code factored as if we had the API calls.**
One named fragment variable per element = one future `editor.add_*()` call.
When the Editor API matures, replace each string with the corresponding call.

The construction zone replaces the single cell-02 with a sequence of code+markdown pairs:

```
[code]     fragment variable declared + printed    ← mirrors one editor.add_*() call
[markdown] narration for that element
[code]     next fragment variable + printed         ← mirrors next editor.add_*() call
[markdown] narration
...
[code]     TOASTER_INCREMENT assembled + printed    ← reflection
           cumulative model loaded; assert model.ok ← for subsequent cells
```

**Fragment size rule:** ≤5 lines per fragment variable (ideally 1–3). If longer, split further.

**Single-element example (Ch1/nb01 — abstract part def):**

```python
from pathlib import Path
import opensysml
from toaster.report import format_diagnostics

conn = opensysml.connect(version="v0.9.0")

# abstract modifier not yet supported — toaster#9 / OpenSysML#595
# spec: SysML v2 formal/2026-03-02 §7.3.3 (PartDefinition — AbstractClassifier)
TOASTING_SYSTEM_DEF = """\
abstract part def ToastingSystem {
    doc /* Any system that converts electrical energy into thermal energy
         for food preparation. */
}
"""
print(TOASTING_SYSTEM_DEF)

TOASTER_INCREMENT = TOASTING_SYSTEM_DEF
source = Path("../../models/ch01-cumulative.sysml").read_text()
model = conn.load_from_content(source, strict=False)
assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
```

**Multi-element example (Ch1/nb02 — part def + attributes, spread across cells):**

```python
# Cell: part def shell
# editor.add_part_def(owner='ToasterDemo', name='Heater') when API ships
HEATER_DEF = "part def Heater {"
print(HEATER_DEF)
```
```python
# Cell: power attribute
# editor.add_attribute(..., name='power', ..., default='800.0 [SI::W]') when API ships
# default = modifier not yet supported — toaster#16 / OpenSysML#603
POWER_ATTR = "    attribute power : ISQ::PowerValue default = 800.0 [SI::W];"
print(POWER_ATTR)
```
```python
# Cell: assembly + reflection + cumulative load
TOASTER_INCREMENT = f"{HEATER_DEF}\n{POWER_ATTR}\n    ...\n}}"
print(TOASTER_INCREMENT)

source = Path("../../models/ch01-cumulative.sysml").read_text()
model = conn.load_from_content(source, strict=False)
assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
```

**Notes:**
- `TOASTER_INCREMENT` = new declarations introduced by this notebook only (not the full model).
- It is assembled from the named fragment variables and printed as the reflection.
- 13 notebooks have construction cells; judgment, depth, navigation, analysis, param-sweep do not.
- The cumulative model file is authored by A3 and must exist before A4 finalizes the assembly cell.

## Tall's three worlds

- **A-F (axiomatic formalism):** the SysML model file at `models/chXX-cumulative.sysml`
- **O-S (operational symbolism):** `conn.load_from_content(...)` loads and indexes it; downstream API calls in demo cells execute operations on it
- **E (conceptual embodiment):** the output rendered below the demo cell (figure, table, or diagnostic)
- **Seam cell:** names all three worlds explicitly in one sentence; identified by content type, not cell index

## Chapter index.md — 6-element recipe

1. Purpose — engineering question and model state after completing the chapter
2. Ingredients — links to each sub-notebook with its one-sentence concept statement
3. Equipment — link to `docs/setup.md`; any chapter-specific requirement
4. Method — one-paragraph narrative of how sub-notebooks connect
5. Expected result — the full cumulative model; what it can demonstrate
6. Experiment — pointer to `exercises/ch{N}/exercise.ipynb`

No executable cells. Pure navigation and framing.

## Chapter conclusion.md — 3 paragraphs + exercise reference

1. **What we built** — model state after this chapter
2. **What this establishes** — the engineering conclusion
3. **What comes next** — one sentence bridging to the next chapter's question
4. **Exercise** — one sentence pointing to the chapter exercise notebook with a one-line description of what it asks

No executable cells.

## Size limits (A6 review criteria)

- Prose: ≤600 words across markdown cells
- Code: ≤50 lines across code cells combined
- Exactly one new construct or one new analysis operation (SA-8)

## A6 checklist per sub-notebook

Identify required cells by content type, not by cell index — additional narration cells may be interspersed.

- [ ] **Concept statement present:** exactly one sentence starting "This notebook introduces"
- [ ] **Context cell present:** one paragraph with link to prior notebook (where applicable)
- [ ] **Model increment cell present (construct-introducing notebooks only):** two-phase — (1) `TOASTER_INCREMENT` assigned and printed as reflection (Pattern A: `str(editor.apply())`; Pattern B: SysML fragment string); (2) full cumulative loaded from `models/chXX-cumulative.sysml`; `assert model.ok`. Judgment/depth/navigation/analysis notebooks: cell-02 loads cumulative only, no TOASTER_INCREMENT.
- [ ] **Negative control present:** short bad_source inline; `assert not bad.ok`; markdown names the error type
- [ ] **Demo cell(s) present:** one key operation per code cell; each code cell followed by markdown narration
- [ ] **Tall seam present:** exactly one sentence naming A-F (model file), O-S (API call), and E (rendered output)
- [ ] **Exercise pointer present:** markdown only; one sentence pointing to `exercises/ch{N}/exercise.ipynb`
- [ ] ≤600 words prose; ≤50 lines code
- [ ] One new construct/operation (or DEPTH annotation for Ch6)

## Tall's three worlds — construction cell update

The A-F → O-S seam is now visible in cell-02 of construct-introducing notebooks:

- **A-F:** the SysML declaration produced by the construction call or written as a string
- **O-S:** `editor.apply()` (Pattern A) or `conn.load_from_content()` (Pattern B) executes it
- **E:** `TOASTER_INCREMENT` printed as the reflection — the engineer sees the validated canonical SysML

The Tall seam cell (slot 5) must still name all three worlds. For Pattern A notebooks, the A-F reference is the `editor.add_*()` call in cell-02, not the printed TOASTER_INCREMENT (which is the full model). For Pattern B notebooks, the A-F reference is the TOASTER_INCREMENT string itself.

## What A4 must never do

- Write prose that explains how Python works
- Embed inline SysML strings longer than ~10 lines in a notebook cell (model source belongs in `models/chXX-cumulative.sysml`)
- Embed exercise content in the exercise pointer cell (pointer only; exercises live in `exercises/`)
- Write conclusion.md without the exercise reference paragraph
- Leave a code cell that does two conceptual things without splitting it and adding narration between the halves
