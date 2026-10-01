---
name: user-testing
description: Simulated learner protocol for chapter checkpoint tests — persona definitions, execution checklist, report format, and pass bar for ACE synthesis.
---

# Simulated User Testing

**Loaded by:** `simulated-learner` (all activities), `ace` (synthesis and grounded self-test). Spawned by the orchestrator, per the Pass 2 operating model (`decisions/next-passes.md` §2): the orchestrator launches one `simulated-learner` agent per persona and collects their reports; the ACE receives the compiled reports for synthesis, not the raw spawn.

## Purpose

At each chapter checkpoint, the orchestrator spawns two or three `simulated-learner` agents with different personas. Each agent reads and executes the chapter as a learner, then reports findings using the fixed format below. The ACE runs one brief test of its own (one notebook) before synthesizing, so the decision is grounded rather than purely delegated.

The bar is: **good enough to proceed to the next chapter.** The question is not perfection — it is whether a learner could make meaningful progress through this content as written.

## Personas and model assignment

The orchestrator chooses two or three from this list per checkpoint, ensuring coverage of novice and practitioner perspectives, and launches each with an **explicit model override** — a simulated novice should not have more capability than the learner it stands for (`decisions/next-passes.md` §3):

| Persona | Model | Background | Focus |
|---|---|---|---|
| **Novice** | Haiku 4.5 | Python-literate; no prior SysML or MBSE | Clarity of concept statements, negative-control diagnostics, whether prose assumes unstated context |
| **SE Practitioner** | Sonnet 5 | Systems engineering background; no SysML v2 | Correctness of SE concepts, whether model choices are defensible, whether the Tall seam (below) is addressed |
| **Returning Learner** | Sonnet 5 | Completed prior chapters; starting this one fresh | Whether index.md sets up correctly, whether the cumulative model is self-contained, exercise pointer utility |

One agent per persona. No two agents with identical persona in one checkpoint run.

## Execution checklist (`simulated-learner` must run these in order)

For each sub-notebook in the assigned chapter(s):

1. **Read index.md** — does it orient you? Note any undefined terms or missing prerequisites.
2. **Cell 0** — read the concept statement. Is it exactly one sentence? Does it state what you will learn?
3. **Cell 1** — read the context paragraph. Does it locate this notebook in the arc? Is there a link to the prior notebook where needed?
4. **Cell 2 (execute)** — run the model-loading code. Record: `model.ok`, any diagnostic output.
5. **Cell 3 (execute)** — run the negative control. Record: `bad.ok` (must be False), printed diagnostic message.
6. **Cell 4 (execute)** — run the demonstration. Record: output produced; note if it matches what cell 0 promised.
7. **Cell 5** — read the Tall seam. AGENTS.md 1.10 binds that learner content **never names** Tall or "the three worlds" (the `tall-named` lint rule, `glossary/lint_rules.toml`, DL-028, already enforces the never-name half in CI). Your job is the half a lint rule cannot judge: does the cell **address the seam in behavior** — is it clear, without naming the lens, that the SysML text, the tool that loads and runs it, and the rendered/printed result are three distinct things the reader has just seen connect? Record which of the three you could each point to concretely from what the cell actually showed, and whether a reader who had not been told there were "three worlds" would still notice the seam.
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
- Cell 5 addresses the seam without naming it: [yes/no] — [which of the three you could point to; if no, what's missing]
- Cell 6 one sentence: [yes/no]
- conclusion.md three paragraphs + exercise reference: [yes/no]

OVERALL: [PASS/NEEDS-FIX] — one sentence.
```

Maximum 400 words per report.

## ACE synthesis protocol

After receiving the compiled `simulated-learner` reports from the orchestrator:

1. **Run own test** — pick one notebook from the chapter, run all cells, read the narrative. One fresh observation.
2. **Triage** — for each NEEDS-FIX, classify: blocking (prevents understanding), minor (friction but learner can continue), cosmetic (wording preference).
3. **Rule or return, never edit.** The ACE does not edit repository files (`ace-protocol`, current and binding): for each blocking issue, the ACE either **rules** what the fix should be (if a framework, principle or heuristic determines it) or **escalates** to Z, and returns that to the orchestrator, which dispatches a builder/author-role work contract to make the change and a reviewer to confirm it — the same pipeline as any other fix. Log each ruling or escalation as a DL entry (Path: Handled by ACE, or Escalated to Z — user-test finding). Do not decide minor or cosmetic items without Z's direction.
4. **Decide** — if zero blocking issues remain (after the dispatched fixes are confirmed in): **CHECKPOINT PASS**. Log the DL entry; proceed to the next chapter. If blocking issues remain: escalate to Z.

## What counts as blocking

- A cell that does not execute (Python error, not a deliberate negative control)
- A concept statement longer than one sentence or missing entirely
- A Tall seam that names Tall or "the three worlds" (already caught by the `tall-named` lint rule in CI; a `simulated-learner` finding of this kind is a lint escape and should also be reported as such) — or one that avoids naming them but does not address the seam in behavior either (the judgment this protocol exists to make)
- A negative control where `bad.ok == True` (the assert would fail at runtime)
- Cumulative model from prior chapter omitted or broken

## What does NOT count as blocking (do not fix without Z)

- Wording preferences ("I would have said it differently")
- Wanting more explanation of a concept already covered in the docs/glossary
- Style deviations caught by `tutorial-style-guide` that don't prevent understanding
- Exercise pointer phrasing (unless missing entirely)
