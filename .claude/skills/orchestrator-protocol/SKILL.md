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

## What A1 must never do

- Edit files
- Author content
- Escalate directly to Z (all escalations go through A8)
- Run developer tools (tests, linters, builds)
