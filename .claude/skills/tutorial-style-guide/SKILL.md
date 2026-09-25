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

## Structural consistency (A4, A6)

- Cell 0 (concept statement): exactly one sentence. No exceptions.
- Cell 5 (Tall seam): exactly one sentence naming all three worlds. No exceptions.
- Cell 6 (exercise pointer): exactly one sentence. Markdown only.
- Chapter `conclusion.md`: exactly four items (three paragraphs + exercise reference). Not three, not five.
- `index.md` six recipe elements appear in stated order. No reordering.

## What every agent loading this skill must never do

- Write a Tall seam that names only two worlds.
- Use Mermaid for any diagram.
- Use em-dashes in prose.
- Write a figure caption longer than two sentences.
- Write a concept statement longer than one sentence.
- Write a conclusion.md without the exercise reference.
