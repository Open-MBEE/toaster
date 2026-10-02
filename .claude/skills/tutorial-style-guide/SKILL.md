---
name: tutorial-style-guide
description: Prose style, diagram aesthetics, and code style rules that all agents must follow to prevent style thrashing.
---

# Tutorial Style Guide

Load this skill alongside domain skills. It does not replace them.

## Prose style (A3, A4)

- Active voice. Never "it can be seen that" or "it is worth noting." Say the thing.
- Sentences ≤20 words as the default ceiling. Split longer ones.
- **No em-dashes, anywhere, in any learner-facing file — including code-cell comments.** Not for asides, not for emphasis, not for a dramatic pause. Use a period, a comma, a colon for an elaboration, or parentheses for a short aside. **In a YAML file (`myst.yml`), quote any title that uses a colon this way** (`title: "Chapter 1: System and Purpose"`); an unquoted colon inside a YAML scalar is a parse error, not a style choice. Mechanically enforced, with a real gap: `tall-named`'s neighbor rule `no-em-dash` in `glossary/lint_rules.toml` flags every hit (`uv run python -m glossary lint`), but the lint only scans markdown cells and `.md` files (`glossary/lint.py`'s own documented scope) — it does not see code-cell comments at all. Found by direct human review 2026-09-27: 35 em-dashes in Chapters 1-2's markdown alone, in a rule already written down here and never checked, plus 3 more hiding in code-cell spec-citation comments that the lint cannot see regardless. Until the lint's scope is widened to cover code cells, grep for the literal character (`grep -rn $'—' <path>`) across an entire notebook, not just its markdown, before calling prose done.
- **No metanarration: text about the act of teaching or writing, instead of the subject matter itself.** Textbook register states facts about the model and the method directly; it does not comment on itself. Banned patterns, all found in this tutorial's own output before this pass: "Let's explore/dive into/unpack X," "Now we'll turn to X," "This is where it gets interesting," "As you can see above," "It's worth noting that," "Here's the key insight," any sentence whose subject is "this notebook/section/tutorial" doing something to the reader rather than the subject matter doing something in the model. Write "The requirement constrains cycle time" not "In this section, we'll look at how the requirement constrains cycle time."
- No hedging when the claim is established: "the model shows" not "the model seems to suggest."
- Present tense for model facts: "the toaster has three parts." Past tense for actions already taken: "we added a requirement."
- Oxford comma.
- Glossary terms introduced once; used without definition thereafter.

**What A4 must never do:** Restate what the code just did. If `model.ok` is True and printed, don't write "as we can see, the model loaded successfully" (also metanarration, doubly banned).

**What A6 must check, mechanically, not by impression:** run `uv run python -m glossary lint` and read every `no-em-dash` hit before approving prose; grep the diff for the metanarration patterns above. A reviewer who read the prose and "didn't notice" an em-dash is not evidence there are none.

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

**A6 test, mechanical, not "scan and see if anything jumps out":** for every notebook in the diff, list the cell types in order (`code`/`markdown`) and check for two `code` cells in a row with no `markdown` between them. Found by direct human review 2026-09-27, not by any prior automated or human check: every one of Chapter 1 and Chapter 2's seven construction-introducing notebooks had at least one such run (`toaster-recipe`'s own pacing rule, and Chapter 1/2's retrofit). A quick check, worth running every time:

```python
import json
nb = json.load(open("path/to/notebook.ipynb"))
seq = [c["cell_type"] for c in nb["cells"]]
print("".join("C" if t == "code" else "M" for t in seq))
```

Any run of two or more consecutive `C`s is a finding, unless the contract explicitly names that pair as one inseparable operation.

## Structural consistency (A4, A6)

- Cell 0 (concept statement): exactly one sentence. No exceptions.
- Cell 5 (seam): exactly one sentence addressing the seam (definition, loading tool, rendered result) in behavior. No exceptions, and no naming Tall, "the three worlds", A-F, O-S or E (AGENTS.md 1.10; corrected DL-050) — see `toaster-recipe`'s "Tall's three worlds" section.
- Cell 6 (exercise pointer): exactly one sentence. Markdown only.
- Chapter `conclusion.md`: exactly four items (three paragraphs + exercise reference). Not three, not five.
- `index.md` six recipe elements appear in stated order. No reordering.

## Construction cells (construct-introducing notebooks only)

**Rule: code factored as if we had the API calls we wanted.**
One fragment variable per element = one future `editor.add_*()` call. When the Editor API
gains full spec coverage, each string fragment is replaced by the corresponding call; the
structure stays the same.

- One code cell per fragment variable. Each is printed immediately after assignment.
- Fragment variable names mirror the element: `HEATER_DEF`, `POWER_ATTR`, `TIMELY_REQ`, etc.
- Fragment size: ≤5 lines of SysML per variable (ideally 1–3). Split if longer.
- Every gap construct: add a comment citing the toaster issue + OpenSysML issue + spec section
  directly above the string, e.g.:
  ```python
  # abstract modifier not yet supported — toaster#9 / OpenSysML#595
  # spec: SysML v2 formal/2026-03-02 §7.3.3
  TOASTING_SYSTEM_DEF = "abstract part def ToastingSystem;"
  ```
- `TOASTER_INCREMENT` is assembled from the fragment variables in the final construction cell
  and equals the **new declarations for this notebook only** (not the full cumulative model).
  It is assigned, not printed: each fragment was already printed when declared, and
  `scripts/check_construction.py` reads the assignment, never the print. The reflection -- the
  result the seam cell points at -- is the chapter's diagram where one exists; otherwise a short
  confirmation query against the construct just declared (`model.find()`/`model.query()`/
  `model.eval()`, or the `src/toaster/query.py` helper for constructs those surfaces do not see:
  `get_review_record_refs` for metadata usages, `satisfy_relationships` for `assert satisfy`,
  `find_allocations`/`perform_relationships` for allocations and performs), added if none exists.
- The cumulative load (`conn.load_from_content(ch0X-cumulative.sysml)`) happens in the same
  final cell as the assignment.
- `conn.close()` belongs at the end of the last code cell in the notebook (cell-04 or later),
  never in the construction zone.
- Judgment notebooks that introduce a new `ReviewRecordRef` tag assign (not print)
  `TOASTER_INCREMENT` as the tag fragment(s), per DL-084. Python-only reconstruction, depth,
  navigation, analysis and param-sweep notebooks do not assign it at all.

## What every agent loading this skill must never do

- Write a seam sentence that names Tall, "the three worlds", or their abbreviations (A-F, O-S, E) — those are the author's own design lens, never learner-facing (AGENTS.md 1.10).
- Write a seam sentence vague enough that a reader could not point to which printed thing is the definition, which is the loading step, and which is the result — e.g. "the source string in cell 2" is not specific enough; name the actual model file or fragment, `models/chXX-cumulative.sysml`, not the inline string.
- Use Mermaid for any diagram.
- Use em-dashes in prose.
- Write a figure caption longer than two sentences.
- Write a concept statement longer than one sentence.
- Write a conclusion.md without the exercise reference.
- Embed a SysML model string longer than ~10 lines in a notebook cell.
- Leave a code cell with no adjacent markdown narration (before or after, as appropriate).
