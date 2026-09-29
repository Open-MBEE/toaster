---
name: orchestrator-protocol
description: WBS contract, review loop rules, verdict aggregation, escalation triggers, and what A1 must never do.
---

# Orchestrator Protocol

## WBS quick reference

| WP | Developers | Reviewers | Key acceptance test |
|---|---|---|---|
| WP-0 | A2 | A5 | smoke passes; myst builds; 11 skills committed; CLAUDE.md + AGENTS.md present |
| WP-1 | A2 | A5 | check-tools exits 0 on ubuntu CI; pytest exits 0; diagram pipeline probe documented |
| WP-2 | A3+A4 | A5+A6 | Ch1–2 sub-notebooks: 7-cell template, models parse, negative controls fire, seam present; exercise stubs committed |
| WP-3 | A3+A4 | A5+A6+A7 | candidate eval verdicts correct; type-mismatch negative control asserts diagnostic; action-def figure passes 4 quality gates |
| WP-4 | A3+A4+A2 | A5+A6+A7 | allocation table from model query; SysMLD exporter produces valid interconnection SVG; interconnection figure passes 4 quality gates |
| WP-5 | A3+A4 | A5+A6+A7 | sympy reference value passes; param sweep + matplotlib passes 4 quality gates; state traces correct; invariant check passes |
| WP-6 | A3+A2 | A5 | 3 judgment sites wired; completeness check catches missing fields; stale detection fires |
| WP-7 | A3+A4 | A5+A6+A7 | coverage table from verify_satisfaction; completeness check passes; stale detection fires; traceability graph passes 4 quality gates; sign-off notebook renders complete |
| WP-8 | A2 | A5 | site at /toaster locally; navigation works; downloads present; 7-step CI passes; Pages deploys |
| WP-9 | A3+A4 | A5+A6 | closing page from manifest; contributor guide covers 4 scenarios; https://open-mbee.github.io/toaster/ publicly accessible |

## Review loop protocol

Developer delivers → A5 technical review → A6/A7 quality review (where assigned) → A1 aggregates verdicts.

**Verdict aggregation:** any FAIL → FAIL; any CANT_TELL (no FAIL) → CANT_TELL; all PASS → close WP.

**Revision cycles:**
- FAIL or CANT_TELL: one revision cycle. For CANT_TELL, developer improves evidence (not implementation). For FAIL, developer fixes the issue.
- Second FAIL or CANT_TELL: route to A8, not back to developer.
- Maximum 2 cycles per WP. Third cycle = A1 routes to A8.

## Escalation triggers

Route to A8 when:
- Required construct unavailable in opensysml==0.9.0
- Developer and reviewer disagree after 2 cycles
- Figure fails all 4 quality gates with no viable simplification
- Spec tension detected
- Any SA (SA-1 through SA-9) is challenged by a developer

## Chapter build dependency (file-based model strategy)

When building chapter notebooks:
1. A3 delivers `models/chXX-cumulative.sysml` first — this is the dependency for all notebooks in that chapter.
2. A4 may begin prose cells concurrently but cannot finalize the model-load cell until the model file path is confirmed.
3. A2 does not need to wait — Python infrastructure is independent of model file content.

Route the chapter to A3 first. Open A4 work in parallel only for cells that do not depend on the model file (index.md, conclusion.md, exercise stubs, context cells).

## Plan-driven non-chapter work

Not all work is a chapter WP. A `docs/superpowers/plans/*.md` implementation plan (written by the `writing-plans` skill, approved by Z) is executed through the same generic mechanism as chapter work — the work-contract template, `builder`, `reviewer`, the ACE, and the states and merge gate in `decisions/task-states.md` — without needing an entry in the WP table above, because none of that mechanism is chapter-specific: blast zone, acceptance criteria and model all come from the contract, not from a pre-registered matrix.

- **One contract per plan task**, or a sensible grouping of a few tightly sequential tasks when splitting them would leave a contract with no independently checkable deliverable (the plan document itself says which; when it doesn't, keep the plan's own task boundaries).
- **Blast zone and acceptance criteria come directly from the plan's own "Files" and step text** for that task — copy them into the contract rather than re-deriving them, since the plan already specified exact paths and runnable checks.
- **Sequencing follows the plan's own stated dependencies.** Where the plan says a task's evidence feeds the next task (a fixture file, a resolved tool path, a prior task's evidence JSON), run those tasks in series, not in parallel, even though nothing here prevents parallel dispatch for tasks the plan does not say depend on each other.
- **Review checks what the plan's own step 2/3/4-style "run and verify" instructions say to check** — a passing test, a real (non-empty, non-placeholder) evidence file, an exit code the plan says is expected — in addition to the reviewer's usual diff/blast-zone/boundary-case checks.

**Escalation triggers specific to this class of work** (route to the ACE the same way as any other escalation, in the `ESCALATE-TO-ACE` form in `decisions/task-states.md`):
- A pinned external tool or version named in the plan cannot be (re)provisioned in the environment, and the plan names no fallback for it.
- A builder or reviewer produces a real finding that contradicts an assumption the approved spec or plan states as settled (for example, a mutation-control verdict coming out the opposite of what the plan expected) — this is evidence for the ACE and Z to see, not something a subagent or the orchestrator resolves by picking a reading.
- A scope question the plan did not anticipate (for example, whether to add back a tool or view type the plan explicitly named out of scope).

## What A1 must never do

- Edit files
- Author content
- Escalate directly to Z (all escalations go through A8)
- Run developer tools (tests, linters, builds)
