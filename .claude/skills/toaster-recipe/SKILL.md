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
| **Model load** | Code | Reads model from file, displays it, then loads it (see pattern below). `assert model.ok`. |
| **Negative control** | Code + Markdown | Short bad_source string. `bad = conn.load_from_content(bad_source, strict=False)`. `assert not bad.ok`. Markdown: one sentence naming the error type and pointing to the diagnostic. |
| **Demonstration** | Code + Markdown | One key operation per code cell. If two things happen, split into two cells each with its own narration markdown. |
| **Tall seam** | Markdown | Exactly one sentence naming all three worlds. |
| **Exercise pointer** | Markdown | One sentence: "Try the chapter exercise in `exercises/ch{N}/exercise.ipynb`: [one-line description]." No embedded code. |

### Cell 2 — model load pattern (required)

```python
from pathlib import Path
conn = opensysml.connect(version="v0.9.0")
source = Path("../../models/ch07-cumulative.sysml").read_text()
print(source)
model = conn.load_from_content(source, strict=False)
assert model.ok
```

- Path is relative from the notebook file to the repo `models/` directory.
- `print(source)` makes the model visible in output without embedding it in the cell.
- No inline SysML strings longer than ~10 lines. The negative-control `bad_source` is exempt — it is deliberately minimal by design.
- The model file is authored by A3 and must exist before A4 can finalize this cell.

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
- [ ] **Model load cell present:** reads from `models/chXX-cumulative.sysml` via `Path(...).read_text()`; no inline SysML string longer than ~10 lines (bad_source exempt); `print(source)` before `load_from_content`; `assert model.ok`
- [ ] **Negative control present:** short bad_source inline; `assert not bad.ok`; markdown names the error type
- [ ] **Demo cell(s) present:** one key operation per code cell; each code cell followed by markdown narration
- [ ] **Tall seam present:** exactly one sentence naming A-F (model file), O-S (API call), and E (rendered output)
- [ ] **Exercise pointer present:** markdown only; one sentence pointing to `exercises/ch{N}/exercise.ipynb`
- [ ] ≤600 words prose; ≤50 lines code
- [ ] One new construct/operation (or DEPTH annotation for Ch6)

## What A4 must never do

- Write prose that explains how Python works
- Embed inline SysML strings longer than ~10 lines in a notebook cell (model source belongs in `models/chXX-cumulative.sysml`)
- Embed exercise content in the exercise pointer cell (pointer only; exercises live in `exercises/`)
- Write conclusion.md without the exercise reference paragraph
- Leave a code cell that does two conceptual things without splitting it and adding narration between the halves
