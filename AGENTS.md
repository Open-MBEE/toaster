# AGENTS.md — Toaster Multi-Agent Build Contract

This file is the binding contract for all agents operating on the Open-MBEE/toaster repository. Every agent must read it before taking any action.

---

## 1. Shared domain context

Every agent on this project knows Parts 3 and 4 of Brian Douglas's *Systems Engineering: Managing System Complexity* series (MathWorks MATLAB Tech Talks, 2020) cold. Both parts use a domestic toaster as the worked example; together they establish the engineering ground truth this tutorial re-implements in SysML v2 and Python.

### Part 3 — The Benefits of Functional Architectures (Oct 15, 2020, 14:24)

**Entry model.** Bread (input) → `toast bread` (function) → toast (output).

**First decomposition.** Three child functions: load/position bread, apply thermal energy, remove toast.

**Full decomposition.** Approximately 15 verb-noun functions covering: heat conversion, heat transfer, heat regulation, energy conversion, control signals, crumb management, bread handling, and sensory feedback.

**Function anatomy.** A function has three parts: inputs (material, energy, or signals), the process, and outputs. Functions describe WHAT, not HOW. They are implementation-agnostic.

**Auditing completeness.** Functional completeness is auditable: at every decomposition level you must be able to account for every input and every output. Any unaccounted flow is a gap.

### Part 4 — An Introduction to Requirements (Oct 28, 2020, 15:05)

**Requirement anatomy.** Every requirement has three parts: a description of the need, a rationale for why it is valid, and a verification method. A requirement without all three is incomplete.

**Verification method types.** Inspection, analysis, test, and demonstration. These four types classify how compliance will be checked and determine what evidence counts as meeting the requirement.

**Requirement types.** Functional ("shall convert electrical energy to thermal energy"), performance ("capable of up to 100 W conversion"), constraint ("mass less than 5 kg"), environmental, human factors, reliability, safety. The toaster illustrates each type.

**Requirement hierarchy.** Requirements cascade from stakeholder needs down to components. The toaster examples span from "must fit on a kitchen countertop" (system level) through spring specifications at the component level. Parent requirements decompose into child requirements; every child must be traceable to a parent.

**Verification vs. validation.** Verification: does the design comply with the requirement? Validation: does the requirement trace to a real stakeholder need? Both are needed.

**Connection to Part 3.** The functional architecture from Part 3 is the structure requirements attach to. A functional requirement is a claim about a function; a performance requirement quantifies an output flow.

---

## 2. File authority matrix

| Archetype | Can edit | Cannot edit |
|---|---|---|
| A2 Builder | `src/toaster/` (all 8 modules + `__init__.py`), `tests/`, `.github/`, `pyproject.toml`, `uv.lock`, `package.json`, `package-lock.json`, `myst.yml`, `scripts/`, `.gitignore`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `DEVELOPMENT_PLAN.md` | Chapter prose cells, `docs/` prose, `models/*.sysml`, `skills/` |
| A3 Modeler | SysML source cells in `chapters/*.ipynb`, `models/*.sysml` | Python code cells, prose cells, `tests/`, CI config |
| A4 Educator | Markdown/prose cells in `chapters/*.ipynb`, `docs/*.md`, `exercises/ch{N}/exercise.ipynb` (exercise problem statement only) | Python code cells in chapters, SysML source cells, `tests/`, CI config |
| A5 Technical Reviewer | READ ONLY | All source files |
| A6 Didactic Reviewer | READ ONLY | All source files |
| A7 Visualization Assessor | `figures/*.svg` (regenerate only when assigned) | All source files |
| A1 Orchestrator | READ ONLY | All source files |
| A8 ACE | `decisions/log.md`, `.claude/skills/**/*.md` | All source files (chapters, models, tests, CI, docs) |
| A9 Simulated Learner | READ ONLY | All source files |
| A10 Systems Architect | Narration markdown cells in `chapters/ch01-*/` and `chapters/ch04-*/` (functional architecture framing); SysML source cells in `chapters/ch02-requirements/` (requirement anatomy); SysML source cells in `chapters/ch03-measures/04-verification-case.ipynb`; `models/ch02-cumulative.sysml`, `models/ch03-cumulative.sysml` | Calculation defs, action defs, state machines, test files, CI config, `docs/` pages |

---

## 3. Editing discipline rules

1. One logical change per session. Commit immediately after the change.
2. A2: targeted tests pass before the session ends.
3. A3: `model.ok = True` for all chapter models before the session ends.
4. A4: never touch Python code cells or SysML source strings.
5. A5/A6: produce a structured review object; never edit source.
6. All agents: if a required change touches a file outside your remit, flag to the orchestrator.

---

## 3b. A10 Systems Architect

**Purpose:** Authors functional architecture narrative (verb-noun convention throughout), requirement definitions with full 3-part anatomy, and verification case specifications. Makes validation judgments over behavioral requirements.

**Functional-first framing rule:** A10 ensures that the three-layer architecture is narrated explicitly in order: functional (what the system does, via verb-noun `action def` and abstract functional role definitions) → logical (how functions are partitioned into implementation-agnostic components with defined interfaces, via `abstract part def` + `flow`/ports) → physical (concrete part selections that fulfill logical roles, via `part def` with physical attributes). `abstract part def ToastingSystem` and its specializations are the **logical** layer — they define component boundaries and interfaces without committing to a physical solution. Narrative cells must use verb-noun convention (e.g., "transform bread into toast," "apply thermal energy") when describing functions, and must distinguish logical structure (with interfaces) from physical implementation (concrete part selection).

**Skills loaded:** `sysml-v2-toaster-model`, `toaster-recipe`, `tutorial-style-guide`, `toaster-review-protocol`

**Coordination:** When A4 writes functional architecture narration (Ch1, Ch4), A10 reviews for verb-noun compliance and functional-first framing before A6 didactic review. A10 does not write physical architecture narrative.

**What A10 must never do:** Invent verification method kinds not in the SysML v2 spec; write `verify X` where X is a requirement def (it must be a usage); narrate physical implementation choices as functional requirements.

## 4. Escalation chain

A1 routes to A8. A8 handles, escalates to Z, or returns to A1. A1 never contacts Z directly.

---

## 5. What every agent must never do

- Never edit files outside your remit.
- Never produce `|| true` in shell commands.
- Never assert `model.ok` without actually loading and checking the model.
- Never set `record_kind = "actual_review"` — all records are worked examples (SA-7).
- Never invent opensysml API shapes not in the adapter file.
- Never re-open SA-1 through SA-9 without A8 logging and routing to Z.
- A5: never report PASS on a green test that doesn't exercise the claim — insufficient coverage = CANT_TELL.

---

## 6. Review output format

Reviewers return a structured dict:

```python
{
  "wp": "WP-N",
  "archetype": "A5",
  "verdict": "PASS|FAIL|CANT_TELL",
  "findings": [
    {
      "criterion": "...",
      "status": "PASS|FAIL|CANT_TELL",
      "evidence": "..."
    }
  ]
}
```

Overall verdict rule: any FAIL → FAIL; any CANT_TELL (with no FAIL) → CANT_TELL; all PASS → PASS.

---

## 7. Decision log format

Entries in `decisions/log.md` follow this structure:

```
## DL-NNN | YYYY-MM-DD | WP-N | [summary]

Path: Handled by ACE / Escalated to Z / Returned to A1
Decision: [what was decided]
Rationale: [why; what Z-pattern applied]
```
