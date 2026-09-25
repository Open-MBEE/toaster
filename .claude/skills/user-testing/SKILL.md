---
name: user-testing
description: Simulated learner protocol for chapter checkpoint tests — persona definitions, execution checklist, report format, and pass bar for ACE synthesis.
---

# Simulated User Testing

**Loaded by:** A9 Simulated Learner (all activities), A8 ACE (synthesis and grounded self-test)

## Purpose

At each chapter checkpoint, ACE spawns two or three A9 agents with different personas. Each agent reads and executes the chapter as a learner, then reports findings using the fixed format below. ACE runs one brief test of its own (one notebook) before synthesizing, so the decision is grounded rather than purely delegated.

The bar is: **good enough to proceed to the next WP.** The question is not perfection — it is whether a learner could make meaningful progress through this content as written.

## Personas

ACE chooses two or three from this list per checkpoint, ensuring coverage of novice and practitioner perspectives:

| Persona | Background | Focus |
|---|---|---|
| **Novice** | Python-literate; no prior SysML or MBSE | Clarity of concept statements, negative-control diagnostics, whether prose assumes unstated context |
| **SE Practitioner** | Systems engineering background; no SysML v2 | Correctness of SE concepts, whether model choices are defensible, Tall seam clarity |
| **Returning Learner** | Completed prior chapters; starting this one fresh | Whether index.md sets up correctly, whether the cumulative model is self-contained, exercise pointer utility |

One agent per persona. No two agents with identical persona in one checkpoint run.

## Execution checklist (A9 must run these in order)

For each sub-notebook in the assigned chapter(s):

1. **Read index.md** — does it orient you? Note any undefined terms or missing prerequisites.
2. **Cell 0** — read the concept statement. Is it exactly one sentence? Does it state what you will learn?
3. **Cell 1** — read the context paragraph. Does it locate this notebook in the arc? Is there a link to the prior notebook where needed?
4. **Cell 2 (execute)** — run the model-loading code. Record: `model.ok`, any diagnostic output.
5. **Cell 3 (execute)** — run the negative control. Record: `bad.ok` (must be False), printed diagnostic message.
6. **Cell 4 (execute)** — run the demonstration. Record: output produced; note if it matches what cell 0 promised.
7. **Cell 5** — read the Tall seam. Does it name all three worlds (SysML text, OpenSysML execution, visible output)?
8. **Cell 6** — read the exercise pointer. Is it one sentence? Does it describe what the exercise asks?
9. **Read conclusion.md** — three paragraphs (what was built / what this establishes / what comes next) plus exercise reference?

Execution command:

```sh
cd /Users/z/Documents/GitHub/toaster
uv run python - <<'EOF'
[paste cell code here]
EOF
```

## Report format

```
LEARNER [ID] — [Persona] — Ch[N]

EXECUTION RESULTS:
- nb[N] cell2: ok=[True/False] | [diagnostic if any]
- nb[N] cell3: neg_ok=[True/False] | diagnostic: [message]
- nb[N] cell4: output=[one-line summary]
[repeat for each notebook]

NARRATIVE OBSERVATIONS (top 3, each quoting exact text):
1. "[exact quote]" — [learner reaction in one sentence]
2. "[exact quote]" — [learner reaction in one sentence]
3. "[exact quote]" — [learner reaction in one sentence]

STRUCTURAL CHECKS:
- Cell 0 one sentence: [yes/no]
- Cell 5 names three worlds: [yes/no]
- Cell 6 one sentence: [yes/no]
- conclusion.md three paragraphs + exercise reference: [yes/no]

OVERALL: [PASS/NEEDS-FIX] — one sentence.
```

Maximum 400 words per report.

## ACE synthesis protocol

After receiving all A9 reports:

1. **Run own test** — pick one notebook from the chapter, run all cells, read the narrative. One fresh observation.
2. **Triage** — for each NEEDS-FIX, classify: blocking (prevents understanding), minor (friction but learner can continue), cosmetic (wording preference).
3. **Fix blocking issues** — fix them inline; log each as a DL entry (Path: Handled by ACE — user-test fix). Do not fix minor or cosmetic without Z's direction.
4. **Decide** — if zero blocking issues remain: **CHECKPOINT PASS**. Log DL entry; proceed to next WP. If blocking issues remain after fix: escalate to Z.

## What counts as blocking

- A cell that does not execute (Python error, not a deliberate negative control)
- A concept statement longer than one sentence or missing entirely
- A Tall seam that does not name all three worlds
- A negative control where `bad.ok == True` (the assert would fail at runtime)
- Cumulative model from prior chapter omitted or broken

## What does NOT count as blocking (do not fix without Z)

- Wording preferences ("I would have said it differently")
- Wanting more explanation of a concept already covered in the docs/glossary
- Style deviations caught by `tutorial-style-guide` that don't prevent understanding
- Exercise pointer phrasing (unless missing entirely)
