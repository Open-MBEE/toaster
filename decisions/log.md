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
