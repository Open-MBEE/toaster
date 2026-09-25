# Decision log

## DL-000 | 2026-09-25 | WP-0 | Plan approved; build begins

Path: Escalated to Z (plan approval)
Decision: Proceed with full WP-0 initialization per approved plan.
Rationale: Plan passed three ACE review passes (B-7 through B-12 all resolved). Z approved.

## DL-001 | 2026-09-25 | WP-1 | Remove java from required tools in bootstrap.py

Path: Handled by ACE
Decision: Remove `java` from `check_tool_versions()`. Only `dot` (Graphviz) is required.
Rationale: `sysml-grpc` is a native Go binary (confirmed via `--help` output); it has no Java dependency. Java was on ubuntu-latest CI but absent on some macOS installs. Checking for it is noise and a false gate on systems where opensysml works correctly.

## DL-002 | 2026-09-25 | WP-1 | Diagram pipeline: Python-generated DOT selected

Path: Handled by ACE
Decision: opensysml v0.9.0 provides no native DOT rendering. Use `model.query()` → `model_to_dot()` → Graphviz `dot -Tsvg` for all relationship/hierarchy diagrams.
Rationale: WP-1 probe confirmed: `sysml-grpc` is a gRPC server with no render flags; Python API has only `model.render_document()` (document queries, not diagrams). Python-generated DOT gives full control, is traceable to the model, and is testable. Probe test `tests/test_diagram_probe.py` passes: DOT generated, SVG rendered. Documented in `sysml-diagrams` skill.

## DL-003 | 2026-09-25 | WP-2 | Checkpoint PASS — Ch1-2 user-test synthesis

Path: Handled by ACE
Decision: CHECKPOINT PASS. Proceed to WP-3.
Rationale: Three A9 simulated learner agents ran (L1 Novice/Ch1, L2 SE Practitioner/Ch1+Ch2, L3 Returning Learner/Ch2) plus ACE grounded self-test of ch02-nb01. Zero blocking issues found. All 7 notebooks execute without error; all negative controls fire correctly (bad.ok=False); all Tall seams name three worlds; all concept statements are one sentence. Four minor findings logged below — none prevents a learner from making meaningful progress.

Minor findings (do not fix without Z's direction):

- MF-1 (L1): A-F/O-S/E abbreviations in cell-5 Tall seams are undefined for a first-time reader; three worlds are named (structural criterion met) but abbreviations are not introduced until docs/glossary.md (WP-9 work). Non-blocking per skill criteria.
- MF-2 (L1): `conclusion.md` ch01 line 5 says "five part definitions and one composed system" — Toaster appears in both the five and as the composed system, making the count ambiguous. index.md correctly says "four part definitions and one composed system." Minor factual inconsistency; A4 fix.
- MF-3 (L2): ch01-nb02 `index.md` Ingredients table lists only Heater for nb02, but the cumulative model (SA-2) also introduces `HeatingSystem;` and `ControlSystem;` as stubs in that notebook. Minor table inaccuracy; A4 fix.
- MF-4 (L2): ch02-nb03 negative control reuses the `nonExistentAttr` pattern from nb01. Expected limitation — opensysml's permissive parser makes reliable failures hard to vary. Non-blocking.

ACE grounded self-test: ch02-nb01 all cells execute clean. Fresh observation: Tall seam abbreviations (A-F/O-S/E) read naturally once you know them but the template uses them without a first-definition footnote — supports MF-1 as an A4/docs-glossary item, not a structural defect.

## DL-004 | 2026-09-25 | WP-3 | Checkpoint PASS — Ch3-4 user-test synthesis

Path: Handled by ACE
Decision: CHECKPOINT PASS. Proceed to WP-4.
Rationale: Three A9 agents ran (L4 Novice/Ch3, L5 SE Practitioner/Ch3+Ch4, L6 Returning Learner/Ch4) plus ACE grounded self-test of ch03-nb02. Zero blocking issues. All six notebooks execute without error; all negative controls fire correctly; all Tall seams name three worlds; all concept statements are one sentence. Three corroborated minor findings fixed inline; two non-blocking findings logged below.

Fixes applied (corroborated minor findings):

- MF-3a (L4/corroborated): A-F label in judgment notebook Tall seams was ambiguous — A-F labeled the Python ReviewRecord object, inconsistent with A-F = SysML source text in non-judgment notebooks. Fixed: Tall seams in ch02-nb03, ch03-nb03, and ch04-nb03 now read "The Hawkins §N.N schema specifies what the record must contain (A-F); filling and validating in Python enacts that schema (O-S); validate_record() returning [] confirms all fields present (E)." — A-F now consistently refers to the formal argument specification (Hawkins schema), not the Python object.
- MF-5b (L5): ch04-nb01 cell 0 promised "an assignment that wires a calculation into the flow" but cell 4 only verified action.kind and action.id. Fixed: trimmed cell 0 to what the demo actually establishes.
- MF-6b (L6): ch04-nb01 cell 6 exercise pointer said "EjectToast" (toaster domain) while the actual exercise and other cell 6 pointers used the coffee maker domain. Fixed: updated to reference the Brew action for coffee maker.

Non-blocking findings (do not fix without Z's direction):

- MF-7 (L4/L6): Hawkins §N.N citations in concept statements have no link or glossary pointer. Non-blocking; docs/glossary.md (WP-9) is the right location.
- MF-8 (L5): ch03-nb03 negative control exercises the model side (undefined requirement type ref) rather than the Python record side. Defensible — the model is the precondition for the record. Non-blocking.

ACE grounded self-test: ch03-nb02 executes clean. Fresh observation: the η=0.7 reference value check (67200 J) in cell 4 is well-chosen — it validates the calc def against the probe fixture value and makes the demonstration self-verifying.
