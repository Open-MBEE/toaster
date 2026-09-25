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

## Model files — one per chapter

Each chapter has a corresponding cumulative model file in `models/`:

| File | Contents |
|---|---|
| `models/ch01-cumulative.sysml` | Constructs 1–4 (abstract part def, part def, specialization, composition) |
| `models/ch02-cumulative.sysml` | + constructs 5–6 (attribute override, requirement def) |
| `models/ch03-cumulative.sysml` | + constructs 7–8 (requirement usage + assert satisfy, calc def) |
| `models/ch04-cumulative.sysml` | + constructs 9–10 (action def, item def) |
| `models/ch05-cumulative.sysml` | + constructs 11–12 (allocate, flow) |
| `models/ch06-cumulative.sysml` | Same constructs as Ch5, second-level decomposition added |
| `models/ch07-cumulative.sysml` | + construct 13 (state machine) |
| `models/ch08-cumulative.sysml` | Same constructs as Ch7 (Ch8 introduces analysis operations, not new constructs) |

**File authority:** A3 is the sole author of `models/*.sysml` files. A4 references these files in notebooks but does not edit them.

**Authoring rule:** A3 must deliver `models/chXX-cumulative.sysml` before A4 finalizes the model-load cell of any notebook in that chapter. The file is the dependency.

**Naming convention:** `ch{NN}-cumulative.sysml` — zero-padded two-digit chapter number. No other naming variants.

**Content rule:** Each file is the full cumulative model at the end of that chapter (SA-2). It is not a diff. It is not a partial model. A notebook reading `ch07-cumulative.sysml` gets all constructs 1–13.

**Build relationship:** `ch{N}-cumulative.sysml` = `ch{N-1}-cumulative.sysml` + constructs introduced in Ch(N). When revising a model element, update the file for the chapter where it is introduced AND all subsequent chapter files that include it.

## Rules

- **SA-8:** One new construct OR one new analysis operation per sub-notebook. Ch6 depth notebooks introduce neither — pedagogical value is recursive application.
- **SA-2:** Every sub-notebook loads the full cumulative model from `models/chXX-cumulative.sysml` (not a diff; not an inline string).
- **Name consistency:** Element names are stable across all 10 chapters. A name change in Ch4 propagates backward and forward through all model files.
- **Negative control:** Every sub-notebook has exactly one intentionally broken SysML string (`bad_source`). It is short, inline (exempt from the ~10-line rule), and deliberately minimal. `assert not bad.ok`. Markdown names the error type and points to the diagnostic.
- **Fallback rule:** If a construct fails to parse, try the simplest legal alternative first. If none exists, escalate to the orchestrator — do not add complexity.

**Ground truth:** `tests/fixtures/probe.sysml` — all confirmed constructs present and verified.
