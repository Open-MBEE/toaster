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
