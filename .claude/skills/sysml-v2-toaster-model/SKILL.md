---
name: sysml-v2-toaster-model
description: SysML v2 construct subset for the toaster tutorial — confirmed constructs, chapter mapping, negative control rules, and name consistency.
---

# SysML v2 Toaster Model

## Confirmed construct subset (opensysml v0.9.0)

| # | Construct | Introduced in | Verified |
|---|---|---|---|
| 1 | `abstract part def` + `doc /* */` | Ch1 | probe.sysml line 4 |
| 2 | `part def` + `attribute : Real default = X` | Ch1 | probe.sysml line 7 |
| 3 | `:>` specialization | Ch1 | probe.sysml line 9 |
| 4 | `part` usage (composition) | Ch1 | probe.sysml lines 8, 11, 13 |
| 5 | `attribute :>>` override | Ch2 | probe.sysml line 14 |
| 6 | `requirement def` + `subject` + `require constraint { ... }` | Ch2 | probe.sysml lines 15–18 |
| 7 | `requirement` usage + `assert satisfy ... by ...` | Ch3 | probe.sysml lines 19–23 |
| 8 | `calc def` with `in` / `return : Real = expr` | Ch3 | probe.sysml lines 24–29 |
| 9 | `action def` with `in`/`out`, `first`/`then`, nested `action` | Ch4 | probe.sysml lines 30–38 |
| 10 | `item def` | Ch4 | probe.sysml lines 39–41 |
| 11 | `allocate X to Y` | Ch5 | probed 2026-09-25 |
| 12 | `flow X.port to Y.port` | Ch5 | probed 2026-09-25 |
| 13 | `state` + entry/then/sub-states + `transition ... accept ... then ...` | Ch7 | probe.sysml lines 42–51 |

No other constructs. `port def`, `interface def`, `connection def`, parametric diagrams, and `metadata` are out of scope for v0.1.

## Ch9–10: analysis operations (not new constructs)

| # | Operation | Introduced | API |
|---|---|---|---|
| A1 | Requirement coverage query | Ch9 nb1 | `model.query()` + `get_satisfy_relationships()` |
| A2 | Satisfaction evaluation | Ch9 nb1 | `model.verify_satisfaction()` |
| A3 | ReviewRecord completeness check | Ch9 nb2 | Python validation |
| A4 | Stale-dependency detection | Ch9 nb3 | `check_stale()` |
| A5 | Multi-relationship traceability graph | Ch10 nb1 | `model.query()` + DOT |
| A6 | Inference dependency traversal | Ch10 nb2 | Python topological sort |
| A7 | Assembled sign-off document | Ch10 nb3 | `format_signoff_document()` |

## Rules

- **SA-8:** One new construct OR one new analysis operation per sub-notebook. Ch6 depth notebooks introduce neither — pedagogical value is recursive application.
- **SA-2:** Every sub-notebook loads the full cumulative model (not a diff).
- **Name consistency:** Element names are stable across all 10 chapters. A name change in Ch4 propagates backward.
- **Negative control:** Every sub-notebook has exactly one intentionally broken SysML string. `assert not bad.ok`. Markdown names the error type and points to the diagnostic.
- **Fallback rule:** If a construct fails to parse, try the simplest legal alternative first. If none exists, escalate to the orchestrator — do not add complexity.

**Ground truth:** `tests/fixtures/probe.sysml` — all confirmed constructs present and verified.
