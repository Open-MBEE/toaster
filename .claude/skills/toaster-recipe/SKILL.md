---
name: toaster-recipe
description: Sub-notebook 7-cell template, chapter index/conclusion structure, Tall three worlds requirement, and A6 review checklist.
---

# Toaster Recipe

## Sub-notebook template (7 cells, fixed order)

| Cell | Type | Constraint |
|---|---|---|
| 0 | Markdown | **Concept statement** — exactly one sentence: "This notebook introduces X; after running it you can Y." |
| 1 | Markdown | **Context** — one paragraph locating this notebook in the chapter arc. One link to prior notebook if model state carries over. |
| 2 | Code | **Model increment** — full cumulative SysML (SA-2). `conn = opensysml.connect(version="v0.9.0")`. `model = conn.load_from_content(source, strict=False)`. `assert model.ok`. |
| 3 | Code + Markdown | **Negative control** — bad SysML string. `bad = conn.load_from_content(bad_source, strict=False)`. `assert not bad.ok`. Markdown: one sentence naming the error type and pointing to the diagnostic. |
| 4 | Code + Markdown | **Demonstration** — one key operation + output. Brief markdown interpreting the output. |
| 5 | Markdown | **Tall seam** — exactly one sentence naming all three worlds: "[A-F construct] is executed by OpenSysML [O-S]; the result is [E]." |
| 6 | Markdown | **Exercise pointer** — one sentence: "Try the chapter exercise in `exercises/ch{N}/exercise.ipynb`: [one-line description]." Does not contain the exercise. |

## Tall's three worlds

- **A-F (axiomatic formalism):** the visible SysML source string in cell 2
- **O-S (operational symbolism):** `conn.load_from_content(...)` or the downstream API call in cell 4
- **E (conceptual embodiment):** the output rendered below cell 4 (figure, table, or diagnostic)
- **Seam cell (5):** names all three worlds explicitly in one sentence

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

- [ ] All 7 cells present in stated order
- [ ] Cell 0: exactly one sentence
- [ ] Cell 2: `conn.load_from_content(...)` + `assert model.ok`
- [ ] Cell 3: `assert not bad.ok` + markdown naming the error type
- [ ] Cell 5: exactly one sentence, names all three worlds
- [ ] Cell 6: markdown only — pointer to exercise, no embedded code
- [ ] ≤600 words prose; ≤50 lines code
- [ ] One new construct/operation (or DEPTH annotation for Ch6)

## What A4 must never do

- Write prose that explains how Python works
- Touch Python code cells or SysML source strings
- Embed exercise content in Cell 6 (pointer only; exercises live in `exercises/`)
- Write conclusion.md without the exercise reference paragraph
