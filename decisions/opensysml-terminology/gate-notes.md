# OT-8 gate notes (2026-10-03): non-blocking items carried forward

Gate verdict: PASS, no blockers (Opus reviewer; executed `--strict` builds of both trees, output equality 59 content files /
255 outputs, 0 orphan page-text differences, protected zones and judgment records byte-identical, AS-C08 hash intact,
lint equal to base outside `docs/superpowers/`, 1882 passed with 0 skipped under `TOASTER_REQUIRE_TOOLS=1`).

Open items for the ACE (to be rulings in the next ACE round; none block publication):
- **N1.** `glossary/README.md` (lint documentation) was edited by OT-7 outside its stated blast zone (`lint.py` is implied by DL-118 D). The edit is accurate; record retroactively.
- **N2.** The Pilot's exclusion ("not one of the two tools the chapters run") is explicit on `docs/setup.md` only; `docs/references.md` and `docs/reproducibility.md` follow `final-texts.md` verbatim and omit it, though DL-117 (6) says every definition sentence carries it. Decide whether to add the clause there.
- **N3.** Plan Task 8 says to log the merge as DL-117; that number is taken (this entry is DL-121).
- **N4.** `docs/setup.md`: "sysml-toolkit does what the OpenSysML runtime cannot yet: prove ..." is broader than D-024/D-025, which record that the runtime's *Python binding* is evaluate-only while the runtime has its own `check`/`smt` engines. Decide whether to say "the runtime's Python binding".
- **N5.** ch07 nb02 cell-23: "The tutorial's own guard does:" now follows the inserted sysml-toolkit clause, so "does" refers back past it. Cosmetic.
- **N6.** The ch03 threshold-judgment page shows the doc comment "not yet supported in OpenSysML v0.9.0" from `models/ch03-cumulative.sysml` (protected). Nothing on that page clarifies it (verification-case does, via R032). Consider an adjacent markdown clarification.
- **N7.** Residual phrasing left on purpose: the ch07 stored-output label `OpenSysML itself`; "the pilot itself stays toolchain" (ch10 nb01 310279c7); "this toolchain's Z3 backend" in code cells/outputs and "nothing in this toolchain checks" in markdown/outputs; "The tool rejects `perform ToastBread;`" (D-019 body); the sysml-diagrams overstatement of D-037 ("real action-flow notation", "100% success"); the KEEP-BODY Resolution line "upstream fix in OpenSysML alone" (D-034). Unknown rule fields in `lint_rules.toml` are silently ignored (follow-up).
- **N8.** Two benign "Kernel: dead" lines appear in the head executed build log (base has none); all outputs identical, treated as shutdown noise.
