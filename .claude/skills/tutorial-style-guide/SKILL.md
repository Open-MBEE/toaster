---
name: tutorial-style-guide
description: Prose style, diagram aesthetics, and code style rules that all agents must follow to prevent style thrashing.
---

# Tutorial Style Guide

Load this skill alongside domain skills. It does not replace them.

## Prose style (A3, A4)

- Active voice. Never "it can be seen that" or "it is worth noting." Say the thing.
- Sentences ≤20 words as the default ceiling. Split longer ones.
- No em-dashes. Use parentheses (short aside) or a colon: for an elaboration, or a new sentence.
- No hedging when the claim is established: "the model shows" not "the model seems to suggest."
- Present tense for model facts: "the toaster has three parts." Past tense for actions already taken: "we added a requirement."
- Oxford comma.
- Glossary terms introduced once; used without definition thereafter.

**What A4 must never do:** Restate what the code just did. If `model.ok` is True and printed, don't write "as we can see, the model loaded successfully."

## Diagram aesthetics (A7)

- White backgrounds on all figures. No grey.
- DOT/Graphviz is the default for sequence and relationship diagrams. Never Mermaid.
- SysMLD is first-class for port-level interconnection.
- PlantUML for action flow.
- Matplotlib for quantitative figures: axis labels include units; reference values marked with a dashed line; legend when more than one series; no chart junk.
- Every figure caption: one sentence stating what the figure shows + one sentence stating what conclusion it supports. Exactly two sentences.

**What A7 must never do:**
- Accept a figure with a caption that says "the figure above shows X" — the caption is the label, not a pointer to itself.
- Accept a grey background.
- Accept a Mermaid diagram.

## Code style (all agents writing notebook cells or src/toaster/)

- ruff-formatted. 88-char line length.
- Variable names mirror model element names: `nominal_model`, `slow_model`, not `m1`, `m2`.
- No inline comments that explain what the code obviously does. A comment is warranted only when the code is non-obvious or deliberately contra-idiomatic.
- `print()` for notebook output: one line per concept, short. No multi-line formatted output in tutorial notebooks.
- **Never embed a SysML model string longer than ~10 lines in a notebook cell.** The full cumulative model belongs in `models/chXX-cumulative.sysml`. The negative-control `bad_source` is exempt — it is deliberately short and self-contained by design.
- One code cell = one conceptual action. If a cell defines something AND checks it, split into two cells.

## Narration density (A4, A6)

Every major operation gets its own dedicated markdown cell. This is not optional — it is the primary teaching mechanism.

- A code cell that loads the model is followed or preceded by a markdown cell explaining what the model contains at this chapter stage.
- A code cell that calls an API operation (`model.eval()`, `model.execute_state()`, `model.verify_satisfaction()`) is preceded by a markdown cell explaining what the call does and why it is meaningful at this point in the tutorial.
- A code cell whose output needs interpretation is followed by a markdown cell interpreting it. Do not leave output to speak for itself.
- If a demo involves two distinct steps (e.g., define a sympy expression, then lambdify it), those are two code cells each with its own narration — not one cell with a comment.

**A6 test:** scan each code cell. If it does more than one conceptual thing OR if its output has no adjacent markdown explanation, flag it.

## Structural consistency (A4, A6)

- Cell 0 (concept statement): exactly one sentence. No exceptions.
- Cell 5 (Tall seam): exactly one sentence naming all three worlds. No exceptions.
- Cell 6 (exercise pointer): exactly one sentence. Markdown only.
- Chapter `conclusion.md`: exactly four items (three paragraphs + exercise reference). Not three, not five.
- `index.md` six recipe elements appear in stated order. No reordering.

## What every agent loading this skill must never do

- Write a Tall seam that names only two worlds.
- Write a Tall seam that says "the source string in cell 2" — A-F is the model file `models/chXX-cumulative.sysml`, not the inline string.
- Use Mermaid for any diagram.
- Use em-dashes in prose.
- Write a figure caption longer than two sentences.
- Write a concept statement longer than one sentence.
- Write a conclusion.md without the exercise reference.
- Embed a SysML model string longer than ~10 lines in a notebook cell.
- Leave a code cell with no adjacent markdown narration (before or after, as appropriate).
