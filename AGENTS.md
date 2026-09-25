# AGENTS.md — Toaster Multi-Agent Build Contract

This file is the binding contract for all agents operating on the Open-MBEE/toaster repository. Every agent must read it before taking any action.

---

## 1. Shared domain context

Every agent on this project knows Brian Douglas's *Systems Engineering Part 3: The Benefits of Functional Architectures* (MathWorks, 2020) cold.

**Entry model.** Bread (input) → `toast bread` (function) → toast (output).

**First decomposition.** Three child functions: load/position bread, apply thermal energy, remove toast.

**Full decomposition.** Approximately 15 verb-noun functions covering: heat conversion, heat transfer, heat regulation, energy conversion, control signals, crumb management, bread handling, sensory feedback, and the interfaces connecting them.

**Function anatomy.** A function has three parts: inputs (material, energy, or signals), the process, and outputs. Functions describe WHAT, not HOW. They are implementation-agnostic.

**Auditing completeness.** Functional completeness is auditable: at every decomposition level you must be able to account for every input and every output. Any unaccounted flow is a gap.

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

---

## 3. Editing discipline rules

1. One logical change per session. Commit immediately after the change.
2. A2: targeted tests pass before the session ends.
3. A3: `model.ok = True` for all chapter models before the session ends.
4. A4: never touch Python code cells or SysML source strings.
5. A5/A6: produce a structured review object; never edit source.
6. All agents: if a required change touches a file outside your remit, flag to the orchestrator.

---

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
