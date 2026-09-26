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

### Cell 2 — model increment pattern (construct-introducing notebooks only)

Two patterns. See `decisions/declarative-construction-plan.md` and `sysml-v2-toaster-model` skill for which notebook uses which.

**Pattern A (Editor API) — TOASTER_INCREMENT = full cumulative model after apply():**

```python
from pathlib import Path
import opensysml
from toaster.report import format_diagnostics

conn = opensysml.connect(version="v0.9.0")
base = conn.load_from_content(
    Path("../../models/ch02-cumulative.sysml").read_text(), strict=False
)
assert base.ok
editor = base.edit()
editor.add_calc_def(
    owner="ToasterDemo", name="DeliveredEnergy",
    inputs=[("power", "ISQ::PowerValue"), ("duration", "ISQ::DurationValue"),
            ("efficiency", "MeasurementReferences::DimensionOneValue")],
    return_type="ISQ::EnergyValue",
    expression="power * duration * efficiency",
)
increment = editor.apply()
TOASTER_INCREMENT = str(increment)   # full model up to this point
print(TOASTER_INCREMENT)             # reflection

source = Path("../../models/ch03-cumulative.sysml").read_text()
model = conn.load_from_content(source, strict=False)
assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
```

**Pattern B (gap construct) — TOASTER_INCREMENT = new SysML fragment only:**

```python
from pathlib import Path
import opensysml
from toaster.report import format_diagnostics

conn = opensysml.connect(version="v0.9.0")

# abstract modifier not yet supported by Editor API — toaster#9 / OpenSysML#595
TOASTER_INCREMENT = """\
abstract part def ToastingSystem {
    doc /* ... */
}
"""
print(TOASTER_INCREMENT)   # reflection: the declaration itself

source = Path("../../models/ch01-cumulative.sysml").read_text()
model = conn.load_from_content(source, strict=False)
assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
```

**Notes:**
- `TOASTER_INCREMENT` must be assigned and printed in cell-02 of every construct-introducing notebook.
- Pattern A: TOASTER_INCREMENT is the full model. Pattern B: TOASTER_INCREMENT is the fragment only.
- 13 notebooks have construction cells; judgment, depth, navigation, analysis, and param-sweep notebooks do not.
- The model file (loaded at end of cell) is authored by A3 and must exist before A4 can finalize this cell.

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
