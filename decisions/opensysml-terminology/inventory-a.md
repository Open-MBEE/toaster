# OT-1a inventory: OpenSysML terminology, learner-facing surface

Contract OT-1a (read-only), 2026-10-03, branch `term/inv-a`, base `terminology` 1649785. Authority: DL-116 and the normative convention in `docs/superpowers/plans/2026-10-03-opensysml-terminology-plan.md`. Nothing but this file was written.

## Method

- Surface: `chapters/**` (markdown cells of the 32 chapter notebooks, code cells for KEEP-ID listing, plus every `index.md` and `conclusion.md`), `exercises/**` (10 notebooks), `docs/*.md`, `docs/case-studies/*.md`, `README.md`. Excluded: `docs/superpowers/**` and everything under `decisions/` (protected; read only as evidence).
- Unit: one line of a cell's `source` (notebooks, JSON read, cell `id` plus 1-based line within the cell) or one file line (markdown). Raw JSON file lines are not the unit, because some notebooks store a whole code cell in one JSON string. Stored cell outputs are not in the surface; the one output containing the name is noted at R067-R068.
- Selection: every unit matching `/opensysml/i`, extracted by script (`ot1a/ext.py` in the scratch dir) and then read in full. A second pass searched the surface for sentences that conflate or contrast the runtime and sysml-toolkit without the word (`the tool`, `the library`, `toolchain`, `the pilot`, `OMG pilot`, `sysmlv2`, `toolkit`); those are the adjacent rows A01-A14 and D1-D2 (outside the machine check, listed separately).
- Capability claims were classified against DEFERRED.md bodies (not only headings). Entries read: D-004 (second, line 172), D-014, D-017, D-018, D-019, D-020, D-023, D-024, D-025, D-026, D-028, D-030, D-031, D-032, D-033, D-034, D-035, D-036, D-037, D-038, plus `decisions/log.md:876` for one claim with no DEFERRED entry.
- Every quote is verbatim, was checked to occur exactly once in its cell (notebooks) or file (markdown) for every non-KEEP-ID row and for the adjacent rows, and sits on the stated line. KEEP-ID code rows quote the line truncated to 110 characters; their locator (cell id and line) identifies them.
- Rules cited in replacements: [C1] a claim true of, or probed against, one component names that component; [C2] a version number attaches to a component name; [C3] first mention on a published page uses the full component name (then `the runtime` may follow); [C4] a contrast names both components; [C5] the stack is defined once each on setup, references and reproducibility with the opensysml.org link; [C6] the Pilot is named in full on first mention (`the OMG SysML v2 Pilot Implementation`, then `the pilot`) and is never counted among the two tools. Replacements assume the convention paragraph of the plan, not a Pilot-membership answer (default OUT).
- Replacement format: the quote is replaced by the replacement text exactly (a substring substitution); where a replacement starts with a capital the quote's preceding text ends a sentence.

## Machine check

Lines in the surface matching /opensysml/i: **132**. Primary rows: **132**. Additional rows on a line already having a row (listed duplicates): **1** (R-id marked `+dup` in the locator). Total rows: **133**. Check: lines 132 = rows 133 - listed duplicates 1. Adjacent rows A01-A14, D1-D2 are outside this count because their lines do not match /opensysml/i.

Independent cross-check: markdown files only, `git grep -ci opensysml` over the surface's `.md` files gives 24 matching lines (README 1, docs/index 2, docs/setup 4, docs/references 3, docs/reproducibility 3, docs/contributor 2, case study 2, chapters index/conclusion 7); notebooks by JSON cell-source scan: 96 code lines + 12 markdown lines = 108; 24 + 108 = 132.

## Counts by class (primary rows, one per matching line)

| class | rows |
|---|---|
| KEEP-ID | 100 |
| KEEP-STACK | 3 |
| RUNTIME | 10 |
| TOOLKIT | 0 |
| BOTH | 2 |
| FALSE-UNDER-STACK | 6 |
| SAME | 0 |
| UNPROBED | 10 |
| DEFINE | 1 |
| AMBIGUOUS | 0 |
| **total** | **132** |

Adjacent rows (outside the machine check): AMBIGUOUS 6, DEFINE 2, FALSE-UNDER-STACK 2, RUNTIME 5, UNPROBED 1, total 16.

Notes on the classes: no row is `TOOLKIT` (no learner-facing sentence is about sysml-toolkit alone and wrong) and no row is `SAME` (the toolkit-same entries D-014, D-020, D-032 are not cited anywhere in the surface, which also contains no sentence quoting them). `FALSE-UNDER-STACK` and `UNPROBED` rows are the capability claims; their DEFERRED entry id and the line that shows what sysml-toolkit does (or that nothing was probed) are in the row note.

## Counts by file

Columns: matching lines | classes of the primary rows.

| file | lines | classes |
|---|---|---|
| README.md | 1 | KEEP-STACK 1 |
| chapters/ch01-system-purpose/01-abstract-def.ipynb | 3 | KEEP-ID 3 |
| chapters/ch01-system-purpose/02-part-def.ipynb | 2 | KEEP-ID 2 |
| chapters/ch01-system-purpose/03-specialization.ipynb | 2 | KEEP-ID 2 |
| chapters/ch01-system-purpose/04-composition.ipynb | 2 | KEEP-ID 2 |
| chapters/ch01-system-purpose/index.md | 1 | RUNTIME 1 |
| chapters/ch02-requirements/01-requirement-def.ipynb | 3 | KEEP-ID 3 |
| chapters/ch02-requirements/02-assumptions.ipynb | 3 | KEEP-ID 3 |
| chapters/ch02-requirements/03-judgment-context.ipynb | 2 | KEEP-ID 2 |
| chapters/ch03-measures/01-moe-definition.ipynb | 2 | KEEP-ID 2 |
| chapters/ch03-measures/02-mop-candidate-eval.ipynb | 3 | KEEP-ID 3 |
| chapters/ch03-measures/03-threshold-judgment.ipynb | 2 | KEEP-ID 2 |
| chapters/ch03-measures/04-verification-case.ipynb | 6 | KEEP-ID 5, UNPROBED 1 |
| chapters/ch03-measures/index.md | 1 | RUNTIME 1 |
| chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb | 4 | KEEP-ID 3, UNPROBED 1 |
| chapters/ch04-functional-decomp/02-heating-refinement.ipynb | 2 | KEEP-ID 2 |
| chapters/ch04-functional-decomp/03-completeness-check.ipynb | 2 | KEEP-ID 2 |
| chapters/ch04-functional-decomp/conclusion.md | 1 | UNPROBED 1 |
| chapters/ch04-functional-decomp/index.md | 2 | RUNTIME 1, UNPROBED 1 |
| chapters/ch05-architecture/01-model-navigation.ipynb | 2 | KEEP-ID 2 |
| chapters/ch05-architecture/02-allocate.ipynb | 3 | KEEP-ID 3 |
| chapters/ch05-architecture/03-interfaces.ipynb | 2 | KEEP-ID 2 |
| chapters/ch06-recursive-decomp/01-subsystem-requirements.ipynb | 2 | KEEP-ID 2 |
| chapters/ch06-recursive-decomp/02-second-level.ipynb | 2 | KEEP-ID 2 |
| chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb | 2 | KEEP-ID 2 |
| chapters/ch07-execution/01-calc-energy.ipynb | 5 | KEEP-ID 4, UNPROBED 1 |
| chapters/ch07-execution/02-state-traces.ipynb | 9 | FALSE-UNDER-STACK 3, KEEP-ID 4, RUNTIME 1, UNPROBED 1 |
| chapters/ch07-execution/03-param-sweep.ipynb | 2 | KEEP-ID 2 |
| chapters/ch07-execution/conclusion.md | 1 | FALSE-UNDER-STACK 1 |
| chapters/ch07-execution/index.md | 1 | UNPROBED 1 |
| chapters/ch08-checking/01-assert-constraint-def.ipynb | 2 | KEEP-ID 2 |
| chapters/ch08-checking/02-violation-witness.ipynb | 2 | KEEP-ID 2 |
| chapters/ch08-checking/03-revision-flow.ipynb | 2 | KEEP-ID 2 |
| chapters/ch09-coverage-sufficiency/01-requirement-coverage.ipynb | 2 | KEEP-ID 2 |
| chapters/ch09-coverage-sufficiency/02-evidence-completeness.ipynb | 2 | KEEP-ID 2 |
| chapters/ch09-coverage-sufficiency/03-stale-detection.ipynb | 2 | KEEP-ID 2 |
| chapters/ch10-traceability-signoff/01-traceability-graph.ipynb | 4 | KEEP-ID 3, UNPROBED 1 |
| chapters/ch10-traceability-signoff/02-judgment-synthesis.ipynb | 2 | KEEP-ID 2 |
| chapters/ch10-traceability-signoff/03-engineering-signoff.ipynb | 2 | KEEP-ID 2 |
| docs/case-studies/2026-09-30-energy-conservation-requirement-tie.md | 2 | UNPROBED 2 |
| docs/contributor.md | 2 | BOTH 1, KEEP-ID 1 |
| docs/index.md | 2 | KEEP-STACK 2 |
| docs/references.md | 3 | DEFINE 1, KEEP-ID 1, RUNTIME 1 |
| docs/reproducibility.md | 3 | BOTH 1, RUNTIME 2 |
| docs/setup.md | 4 | FALSE-UNDER-STACK 1, RUNTIME 3 |
| exercises/ch01/exercise.ipynb | 2 | KEEP-ID 2 |
| exercises/ch02/exercise.ipynb | 2 | KEEP-ID 2 |
| exercises/ch03/exercise.ipynb | 2 | KEEP-ID 2 |
| exercises/ch04/exercise.ipynb | 2 | KEEP-ID 2 |
| exercises/ch05/exercise.ipynb | 2 | KEEP-ID 2 |
| exercises/ch06/exercise.ipynb | 2 | KEEP-ID 2 |
| exercises/ch07/exercise.ipynb | 3 | FALSE-UNDER-STACK 1, KEEP-ID 2 |
| exercises/ch08/exercise.ipynb | 2 | KEEP-ID 2 |
| exercises/ch09/exercise.ipynb | 2 | KEEP-ID 2 |
| exercises/ch10/exercise.ipynb | 2 | KEEP-ID 2 |

## Truth-class summary (capability claims)

FALSE-UNDER-STACK (false once OpenSysML includes sysml-toolkit; DEFERRED entry shows the toolkit differs): R066, R069, R070, R074, R112, R125 (6 primary rows: D-023 for the ch07 notebook 02 and ch07 conclusion rows, D-024/D-025 for docs/setup.md, decisions/log.md:876 for the exercises/ch07 row). Adjacent rows A02 and A05 (D-023) are also FALSE-UNDER-STACK.

UNPROBED (the entry names only the runtime; sysml-toolkit not run): R032, R037, R042, R044, R060, R065, R075, R091, R096, R097 (10 rows; D-004 second entry, D-026, D-033, and the two case-study lines / ch10 cell 02281b44 with no DEFERRED entry). Adjacent row A03 (D-038) is also UNPROBED.

SAME: none in this surface. (D-014, D-020, D-032 are the toolkit-same entries; none is cited by a learner-facing OpenSysML sentence.)

## Row table

| row | file | locator | quoted sentence | class | proposed replacement wording |
|---|---|---|---|---|---|
| R001 | README.md | L3 | using SysML v2 and OpenSysML. | KEEP-STACK | (no change)  **NOTE:** The tutorial uses SysML v2 with two components of the OpenSysML tool stack; the sentence is about the stack. Optional: link https://opensysml.org/ (not required by the convention). |
| R002 | chapters/ch01-system-purpose/01-abstract-def.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R003 | chapters/ch01-system-purpose/01-abstract-def.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R004 | chapters/ch01-system-purpose/01-abstract-def.ipynb | `cell-06` line 3 | # abstract modifier: the Editor API does not yet author it (https://github.com/Open-MBEE/toaster/issues/9 / ht | KEEP-ID | (no change) Code comment carrying a repo/issue reference (`Open-MBEE/OpenSysML#NNN`, protected token and code-cell string). |
| R005 | chapters/ch01-system-purpose/02-part-def.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R006 | chapters/ch01-system-purpose/02-part-def.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R007 | chapters/ch01-system-purpose/03-specialization.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R008 | chapters/ch01-system-purpose/03-specialization.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R009 | chapters/ch01-system-purpose/04-composition.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R010 | chapters/ch01-system-purpose/04-composition.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R011 | chapters/ch01-system-purpose/index.md | L22 | provision Python and the OpenSysML binary | RUNTIME | provision Python and the OpenSysML runtime binary  **NOTE:** setup.md L27 states the downloaded binary is the one the `opensysml` Python package connects to, i.e. the runtime. [C1][C3] - first mention on the page. |
| R012 | chapters/ch02-requirements/01-requirement-def.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R013 | chapters/ch02-requirements/01-requirement-def.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R014 | chapters/ch02-requirements/01-requirement-def.ipynb | `976fc6bc` line 2 | # require constraint: the Editor API does not yet author it (https://github.com/Open-MBEE/toaster/issues/11 /  | KEEP-ID | (no change) Code comment carrying a repo/issue reference (`Open-MBEE/OpenSysML#NNN`, protected token and code-cell string). |
| R015 | chapters/ch02-requirements/02-assumptions.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R016 | chapters/ch02-requirements/02-assumptions.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R017 | chapters/ch02-requirements/02-assumptions.ipynb | `fa97b3a7` line 2 | # attribute :>> redefinition: the Editor API does not yet author it (https://github.com/Open-MBEE/toaster/issu | KEEP-ID | (no change) Code comment carrying a repo/issue reference (`Open-MBEE/OpenSysML#NNN`, protected token and code-cell string). |
| R018 | chapters/ch02-requirements/03-judgment-context.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R019 | chapters/ch02-requirements/03-judgment-context.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R020 | chapters/ch03-measures/01-moe-definition.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R021 | chapters/ch03-measures/01-moe-definition.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R022 | chapters/ch03-measures/02-mop-candidate-eval.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R023 | chapters/ch03-measures/02-mop-candidate-eval.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R024 | chapters/ch03-measures/02-mop-candidate-eval.ipynb | `cell-02` line 8 | # assert satisfy not yet supported by the Editor API - https://github.com/Open-MBEE/toaster/issues/12 / https: | KEEP-ID | (no change) Code comment carrying a repo/issue reference (`Open-MBEE/OpenSysML#NNN`, protected token and code-cell string). |
| R025 | chapters/ch03-measures/03-threshold-judgment.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R026 | chapters/ch03-measures/03-threshold-judgment.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R027 | chapters/ch03-measures/04-verification-case.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R028 | chapters/ch03-measures/04-verification-case.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R029 | chapters/ch03-measures/04-verification-case.ipynb | `a1b2c3d4` line 3 | # Note: #verificationMethod = VerificationMethodKind::test metadata not yet supported (https://github.com/Open | KEEP-ID | (no change) Code comment carrying a repo/issue reference (`Open-MBEE/OpenSysML#NNN`, protected token and code-cell string). |
| R030 | chapters/ch03-measures/04-verification-case.ipynb | `a1b2c3d4` line 10 | * Note: formal #verificationMethod metadata not yet supported in OpenSysML v0.9.0; | KEEP-ID | (no change) Code-cell string (protected, DL-115). |
| R031 | chapters/ch03-measures/04-verification-case.ipynb | `a1b2c3d4` line 11 | * tracked at toaster#19 / OpenSysML#608. | KEEP-ID | (no change) Code comment carrying a repo/issue reference (`Open-MBEE/OpenSysML#NNN`, protected token and code-cell string). |
| R032 | chapters/ch03-measures/04-verification-case.ipynb | `e5f6g7h8` line 1 | it is not yet supported in OpenSysML v0.9.0 ( | UNPROBED | it is not yet supported in the OpenSysML runtime v0.9.0 (  **NOTE:** D-004 second entry (DEFERRED.md:172-189) records only the runtime ('In OpenSysML v0.9.0 this raises "expected a body member"'); no sysml-toolkit probe. [C1][C2][C3]. The same cell's `OpenSysML#608` link text is KEEP-ID. This cell also carries the clarification for code cell `a1b2c3d4` lines 3, 10, 11 (comment/`doc` text 'not yet supported in OpenSysML v0.9.0', KEEP-ID). |
| R033 | chapters/ch03-measures/index.md | L22 | provision Python and the OpenSysML binary | RUNTIME | provision Python and the OpenSysML runtime binary  **NOTE:** setup.md L27 states the downloaded binary is the one the `opensysml` Python package connects to, i.e. the runtime. [C1][C3] - first mention on the page. |
| R034 | chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R035 | chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R036 | chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb | `cell-04` line 1 | # params argument of add_action_def not yet supported, https://github.com/Open-MBEE/toaster/issues/18 / https: | KEEP-ID | (no change) Code comment carrying a repo/issue reference (`Open-MBEE/OpenSysML#NNN`, protected token and code-cell string). |
| R037 | chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb | `cell-15` line 1 | but OpenSysML v0.9.0 treats them differently: | UNPROBED | but the OpenSysML runtime v0.9.0 treats them differently:  **NOTE:** D-026 (DEFERRED.md:342-546) has no sysml-toolkit probe ('the tool accepts both (`model.ok == True`)' is `model.ok`, the runtime API). [C1][C2][C3]. URL anchor `d-026-opensysml-treats...` on the same line is KEEP-ID. |
| R038 | chapters/ch04-functional-decomp/02-heating-refinement.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R039 | chapters/ch04-functional-decomp/02-heating-refinement.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R040 | chapters/ch04-functional-decomp/03-completeness-check.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R041 | chapters/ch04-functional-decomp/03-completeness-check.ipynb | `cell-02` line 7 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R042 | chapters/ch04-functional-decomp/conclusion.md | L9 | but which OpenSysML v0.9.0 only honors when it is written out | UNPROBED | but which the OpenSysML runtime v0.9.0 only honors when it is written out  **NOTE:** D-026 (no toolkit probe). [C1][C2][C3]. First mention on this page. |
| R043 | chapters/ch04-functional-decomp/index.md | L21 | provision Python and the OpenSysML binary | RUNTIME | provision Python and the OpenSysML runtime binary  **NOTE:** setup.md L27 states the downloaded binary is the one the `opensysml` Python package connects to, i.e. the runtime. [C1][C3] - first mention on the page. |
| R044 | chapters/ch04-functional-decomp/index.md | L25 | so that OpenSysML v0.9.0 keeps the whole model evaluable | UNPROBED | so that the OpenSysML runtime v0.9.0 keeps the whole model evaluable  **NOTE:** D-026 (no toolkit probe). [C1][C2]. Full component name kept (line 21 of the same page already introduced it; 'the runtime v0.9.0' would also satisfy the convention). |
| R045 | chapters/ch05-architecture/01-model-navigation.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R046 | chapters/ch05-architecture/01-model-navigation.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R047 | chapters/ch05-architecture/02-allocate.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R048 | chapters/ch05-architecture/02-allocate.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R049 | chapters/ch05-architecture/02-allocate.ipynb | `cell-04` line 1 | # allocate not yet supported by the Editor API: toaster#13 (https://github.com/Open-MBEE/toaster/issues/13) /  | KEEP-ID | (no change) Code comment carrying a repo/issue reference (`Open-MBEE/OpenSysML#NNN`, protected token and code-cell string). |
| R050 | chapters/ch05-architecture/03-interfaces.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R051 | chapters/ch05-architecture/03-interfaces.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R052 | chapters/ch06-recursive-decomp/01-subsystem-requirements.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R053 | chapters/ch06-recursive-decomp/01-subsystem-requirements.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R054 | chapters/ch06-recursive-decomp/02-second-level.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R055 | chapters/ch06-recursive-decomp/02-second-level.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R056 | chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R057 | chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb | `cell-02` line 7 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R058 | chapters/ch07-execution/01-calc-energy.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R059 | chapters/ch07-execution/01-calc-energy.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R060 | chapters/ch07-execution/01-calc-energy.ipynb | `cell-14` line 1 | (OpenSysML prints this as the unsimplified | UNPROBED | (the OpenSysML runtime prints this as the unsimplified  **NOTE:** D-033 (DEFERRED.md:856-864): found by ad hoc `model.eval()` calls; sysml-toolkit has no probe. [C1][C3]. URL anchor `d-033-opensysmls-eval...` on the line is KEEP-ID. |
| R061 | chapters/ch07-execution/01-calc-energy.ipynb | `cell-15` line 6 | # opensysml's own verdict string uses an em-dash; the printed form here uses a | KEEP-ID | (no change) Code-cell string (protected, DL-115). |
| R062 | chapters/ch07-execution/01-calc-energy.ipynb | `cell-18` line 1 | d-033-opensysmls-eval-does-not-simplify | KEEP-ID | (no change)  **NOTE:** Only occurrence on the line is the DEFERRED.md anchor inside a URL. The sentence's 'printed as the same unsimplified compound unit' needs no edit (the page's first mention is cell-14). |
| R063 | chapters/ch07-execution/02-state-traces.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R064 | chapters/ch07-execution/02-state-traces.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R065 | chapters/ch07-execution/02-state-traces.ipynb | `cell-05` line 1 | stay executable when left unbound in OpenSysML v0.9.0 ( | UNPROBED | stay executable when left unbound in the OpenSysML runtime v0.9.0 (  **NOTE:** D-026 (no toolkit probe). [C1][C2][C3] - this is the page's first prose mention, so the full component name. URL anchor on the line is KEEP-ID. |
| R066 | chapters/ch07-execution/02-state-traces.ipynb | `cell-09` line 1 | OpenSysML v0.9.0 keeps a transition's trigger only as a string and never resolves it against `Start`, `Finish` or `Cancel`: a typo, or a reference to a name the model never declares, loads without error and simply never fires | FALSE-UNDER-STACK | The OpenSysML runtime keeps a transition's trigger only as a string and never resolves it against `Start`, `Finish` or `Cancel`: in the runtime v0.9.0 a typo, or a reference to a name the model never declares, loads without error and simply never fires, where sysml-toolkit v0.9.1 resolves these names and warns on a broken reference  **NOTE:** D-023 (DEFERRED.md:298 'sysml-toolkit v0.9.1 does resolve these names and warns on broken references'). Under the stack reading 'OpenSysML ... never resolves' is false. [C1][C2][C4]. Quote begins mid-sentence: the preceding text is 'modes. ' so the replacement starts with a capital 'The'. URL anchor on the line is KEEP-ID. (Builders: if a shorter fix is preferred, 'the OpenSysML runtime v0.9.0 keeps ... never fires, where sysml-toolkit v0.9.1 warns' is equivalent.) |
| R067 | chapters/ch07-execution/02-state-traces.ipynb | `cell-22` line 3 | OpenSysML itself accepts the typo'd trigger with no diagnostic | KEEP-ID | (no change in the code cell)  **NOTE:** Code-cell assertion message (DL-115 protected). Wrong under the stack reading (the string says the whole stack accepts the typo; sysml-toolkit v0.9.1 warns, D-023). Clarification lives in markdown cell-23 (row for cell-23). |
| R068 | chapters/ch07-execution/02-state-traces.ipynb | `cell-22` line 4 | OpenSysML itself: typo_model.ok= | KEEP-ID | (no change in the code cell)  **NOTE:** Code-cell print; the string is also stored in the cell's stdout output ('OpenSysML itself: typo_model.ok=True', the only stored output in the surface containing the name). Protected; clarified in markdown cell-23. |
| R069 | chapters/ch07-execution/02-state-traces.ipynb | `cell-23` line 1 | OpenSysML loads the typo cleanly: `Strat` never fires, and nothing in the tool says so. | FALSE-UNDER-STACK | The OpenSysML runtime loads the typo cleanly (the `OpenSysML itself` line printed above is the runtime's verdict): `Strat` never fires, and nothing in the runtime says so, where sysml-toolkit v0.9.1 warns on the broken reference.  **NOTE:** D-023 (DEFERRED.md:298 'sysml-toolkit v0.9.1 does resolve these names and warns on broken references'). [C1][C2][C4]. This sentence is the markdown clarification for the code-cell strings in cell-22 (rows above). The same cell's 'The tool has a real hole here' is adjacent row A2. |
| R070 | chapters/ch07-execution/02-state-traces.ipynb | `cell-25` line 1 | invisible to OpenSysML's own loader. | FALSE-UNDER-STACK | invisible to the OpenSysML runtime's own loader (sysml-toolkit v0.9.1 would warn on it).  **NOTE:** D-023 (DEFERRED.md:298 'sysml-toolkit v0.9.1 does resolve these names and warns on broken references'). [C1][C4]. Cell 25 is the figure caption cell for the typo'd trigger. If the ACE prefers a shorter edit, drop the parenthesis: 'invisible to the OpenSysML runtime's own loader.' |
| R071 | chapters/ch07-execution/02-state-traces.ipynb | `cell-27` line 1 | in OpenSysML v0.9.0, `execute_state`'s `performer` argument has no effect on the result | RUNTIME | in the OpenSysML runtime v0.9.0, `execute_state`'s `performer` argument has no effect on the result  **NOTE:** D-028 (DEFERRED.md:600-637): an argument of the runtime's Python `Model.execute_state`; the entry has no sysml-toolkit probe, and sysml-toolkit's Python `Session` is a different API, so this is an API-surface claim, not a language-capability claim. [C1][C2]. |
| R072 | chapters/ch07-execution/03-param-sweep.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R073 | chapters/ch07-execution/03-param-sweep.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R074 | chapters/ch07-execution/conclusion.md | L13 | OpenSysML v0.9.0 does not resolve a transition's trigger against the item def it names; | FALSE-UNDER-STACK | The OpenSysML runtime v0.9.0 does not resolve a transition's trigger against the item def it names, where sysml-toolkit v0.9.1 does;  **NOTE:** D-023 (DEFERRED.md:298 'sysml-toolkit v0.9.1 does resolve these names and warns on broken references'). [C1][C2][C4]. Quote starts after 'in use. '. URL anchor on the line is KEEP-ID. The same sentence's 'the tool lets through silently' is adjacent row A5. |
| R075 | chapters/ch07-execution/index.md | L31 | (printed by OpenSysML as | UNPROBED | (printed by the OpenSysML runtime as  **NOTE:** D-033 (no toolkit probe; `model.eval` is the runtime's API). [C1][C3]. URL anchor on the line is KEEP-ID. |
| R076 | chapters/ch08-checking/01-assert-constraint-def.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R077 | chapters/ch08-checking/01-assert-constraint-def.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R078 | chapters/ch08-checking/02-violation-witness.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R079 | chapters/ch08-checking/02-violation-witness.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R080 | chapters/ch08-checking/03-revision-flow.ipynb | `cell-02` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R081 | chapters/ch08-checking/03-revision-flow.ipynb | `cell-02` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R082 | chapters/ch09-coverage-sufficiency/01-requirement-coverage.ipynb | `5de63c72` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R083 | chapters/ch09-coverage-sufficiency/01-requirement-coverage.ipynb | `5de63c72` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R084 | chapters/ch09-coverage-sufficiency/02-evidence-completeness.ipynb | `419ecbee` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R085 | chapters/ch09-coverage-sufficiency/02-evidence-completeness.ipynb | `419ecbee` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R086 | chapters/ch09-coverage-sufficiency/03-stale-detection.ipynb | `dc06bb34` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R087 | chapters/ch09-coverage-sufficiency/03-stale-detection.ipynb | `dc06bb34` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R088 | chapters/ch10-traceability-signoff/01-traceability-graph.ipynb | `b8bb18ce` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R089 | chapters/ch10-traceability-signoff/01-traceability-graph.ipynb | `b8bb18ce` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R090 | chapters/ch10-traceability-signoff/01-traceability-graph.ipynb | `ed18ec1d` line 3 | d-038-opensysmls-api-json-export | KEEP-ID | (no change)  **NOTE:** Only occurrence on the line is the DEFERRED.md anchor inside a URL. The surrounding sentence 'a gap in the API-JSON export' is adjacent row A3 (D-038, UNPROBED). |
| R091 | chapters/ch10-traceability-signoff/01-traceability-graph.ipynb | `02281b44` line 1 | and OpenSysML raises no diagnostic against any of them | UNPROBED | and the OpenSysML runtime raises no diagnostic against any of them  **NOTE:** No DEFERRED entry; DL-116 item 7 and the case study (rows below) list this as toolkit-unprobed (no sysml-toolkit run on the subject-less `assert satisfy` fixtures is recorded). [C1][C3]. This is the page's first prose mention of the component (the code cells' `import opensysml` are KEEP-ID). |
| R092 | chapters/ch10-traceability-signoff/02-judgment-synthesis.ipynb | `407bfd17` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R093 | chapters/ch10-traceability-signoff/02-judgment-synthesis.ipynb | `407bfd17` line 6 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R094 | chapters/ch10-traceability-signoff/03-engineering-signoff.ipynb | `bc09af84` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R095 | chapters/ch10-traceability-signoff/03-engineering-signoff.ipynb | `bc09af84` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R096 | docs/case-studies/2026-09-30-energy-conservation-requirement-tie.md | L104 | and loads cleanly under OpenSysML. | UNPROBED | and loads cleanly under the OpenSysML runtime.  **NOTE:** DL-116 item 7: toolkit-unprobed (no sysml-toolkit run on this line recorded; the file mentions sysml-toolkit only for `verify --solve`, line 24). [C1][C3]. This is the file's first mention of OpenSysML. |
| R097 | docs/case-studies/2026-09-30-energy-conservation-requirement-tie.md | L124 | **Tool support.** Neither OpenSysML nor the OMG pilot flags | UNPROBED | **Tool support.** Neither the OpenSysML runtime nor the pilot flags  **NOTE:** DL-116 item 7: toolkit-unprobed. [C1][C6]. Wording assumes the Pilot is first named in full at line 60 (adjacent row A6); the sentence does not claim anything about sysml-toolkit. Alternative if the ACE wants the claim to cover the stack: add '(sysml-toolkit was not probed on this line)' after 'pilot'. |
| R098 | docs/contributor.md | L28 | in the toolchain (OpenSysML, sysml-toolkit) | BOTH | in the toolchain (the OpenSysML runtime, sysml-toolkit)  **NOTE:** Lists the runtime and sysml-toolkit as parallel items, which only works if the first names the runtime; under the stack reading 'OpenSysML, sysml-toolkit' lists the whole and a part. [C1][C4]. |
| R099 | docs/contributor.md | L95 | a version bump in `opensysml` or `sympy` | KEEP-ID | (no change)  **NOTE:** Package name `opensysml` (protected token). |
| R100 | docs/index.md | L3 | using SysML v2 and OpenSysML. | KEEP-STACK | (no change)  **NOTE:** As README.md L3. |
| R101 | docs/index.md | L11 | Execute model analyses using OpenSysML and interpret the results | KEEP-STACK | (no change)  **NOTE:** The analyses run on the runtime (chapters 1-10) and, for Chapter 8, sysml-toolkit, so a statement about the stack is true. Setup page defines the stack and components. |
| R102 | docs/references.md | L63 | ## OpenSysML | DEFINE | ## OpenSysML<br><br>OpenSysML ([opensysml.org](https://opensysml.org/)) is the open-source SysML v2 tool stack. This tutorial uses two of its components and names them by role: the OpenSysML runtime (Go; repository `Open-MBEE/OpenSysML`; Python package `opensysml`; pinned v0.9.0) and sysml-toolkit (Rust; `sysmlv2` binary; pinned v0.9.1). The OMG SysML v2 Pilot Implementation (EPL-2.0) is the conformance baseline and is always named as such.  **NOTE:** Heading text stays 'OpenSysML' (the anchor #opensysml stays valid). Definition site per plan: stack defined once each on setup.md, references.md, reproducibility.md. Wording applies the convention paragraph verbatim in substance and holds whichever way the Pilot-membership question is answered. [C5]. Rows below give the two component entries. |
| R103 | docs/references.md | L65 | Open-MBEE/OpenSysML. <https://github.com/Open-MBEE/OpenSysML> | KEEP-ID | (no change to the repo name or URL; prefix a label, see replacement)  **NOTE:** Repo name and URL are protected. Proposed: put 'The OpenSysML runtime: ' in front of the unchanged repo line, and add a parallel line after the runtime paragraph: 'sysml-toolkit: Open-MBEE/sysml-toolkit. <https://github.com/Open-MBEE/sysml-toolkit>' followed by 'The Rust toolkit (`sysmlv2` binary, pinned v0.9.1) used for `sysmlv2 verify --solve` in Chapter 8 and for the cross-checks recorded in DEFERRED.md (D-014, D-017, D-019, D-023).' |
| R104 | docs/references.md | L67 | The Python library (`opensysml==0.9.0`) used to load, validate, evaluate, and query SysML v2 models in this tutorial. | RUNTIME | The OpenSysML runtime's Python package (`opensysml==0.9.0`), used to load, validate, evaluate, and query SysML v2 models in this tutorial.  **NOTE:** Line matches /opensysml/ only through the package token (kept). The sentence is the runtime's description. [C1][C2]. |
| R105 | docs/references.md | L67 +dup | Gaps between the library's current API and the SysML v2 specification | RUNTIME | Gaps between the runtime's current API and the SysML v2 specification  **NOTE:** Second sentence on the same line (row suffix b: not counted as a separate line in the machine check). Also covers sysml-toolkit gaps in DEFERRED.md, so the sentence 'are tracked in DEFERRED.md' is still true of both; optional extension: 'Gaps in either component and the SysML v2 specification'. [C1][C4]. |
| R106 | docs/reproducibility.md | L11 | the OpenSysML binary, | RUNTIME | the OpenSysML runtime binary,  **NOTE:** Pinned runtime binary (line 17 says `v0.9.0`). [C1][C3] - first mention on the page. DEFINE row D2 (adjacent table) adds the stack definition on this page. |
| R107 | docs/reproducibility.md | L17 | **The OpenSysML binary** is pinned by version string (`v0.9.0` as of this tutorial) | RUNTIME | **The OpenSysML runtime binary** is pinned by version string (`v0.9.0` as of this tutorial)  **NOTE:** Version attaches to the component named in the same bold phrase. [C1][C2]. |
| R108 | docs/reproducibility.md | L90 | Where OpenSysML or sysml-toolkit | BOTH | Where the OpenSysML runtime or sysml-toolkit  **NOTE:** Both-tools contrast; the banned bare form 'OpenSysML or sysml-toolkit' is exactly what this row removes. [C1][C4]. |
| R109 | docs/setup.md | L27 | the OpenSysML binary this tutorial's Python package connects to | RUNTIME | the OpenSysML runtime binary this tutorial's Python package connects to  **NOTE:** [C1][C3] - first mention on the page; the `opensysml` package connects to the runtime. DEFINE row D1 (adjacent table) adds the stack definition on this page. |
| R110 | docs/setup.md | L140 | **OpenSysML** (`opensysml`, installed automatically by | RUNTIME | **The OpenSysML runtime** (`opensysml`, installed automatically by  **NOTE:** 'is the primary tool: it loads, validates, queries, and evaluates every model' is a runtime statement (D-024/D-025: toolkit's Python Session has no such role in chapters 1-7). [C1]. |
| R111 | docs/setup.md | L142 | also provisions a second OpenSysML binary, the | RUNTIME | also provisions a second OpenSysML runtime binary, the  **NOTE:** The render-capable CLI is the runtime's `-render` CLI (D-037: 'OpenSysML's own `-render` CLI'). [C1]. |
| R112 | docs/setup.md | L147 | **sysml-toolkit** does one thing OpenSysML cannot yet: | FALSE-UNDER-STACK | **sysml-toolkit** does one thing the OpenSysML runtime cannot yet:  **NOTE:** Self-contradictory under the stack reading (sysml-toolkit IS part of OpenSysML). Evidence: D-024 (DEFERRED.md:325 '(sysml-toolkit can)', retracted claim that no tool could; runtime's Python binding is evaluate-only) and D-025 (DEFERRED.md:333 'only the Rust CLI (`sysmlv2 verify --solve`) proves a constraint holds for all values'). [C1][C4]. |
| R113 | exercises/ch01/exercise.ipynb | `cell-01` line 1 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R114 | exercises/ch01/exercise.ipynb | `cell-01` line 3 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R115 | exercises/ch02/exercise.ipynb | `cell-1` line 1 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R116 | exercises/ch02/exercise.ipynb | `cell-1` line 4 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R117 | exercises/ch03/exercise.ipynb | `cell-1` line 1 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R118 | exercises/ch03/exercise.ipynb | `cell-1` line 4 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R119 | exercises/ch04/exercise.ipynb | `cell-1` line 1 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R120 | exercises/ch04/exercise.ipynb | `cell-1` line 4 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R121 | exercises/ch05/exercise.ipynb | `cell-1` line 1 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R122 | exercises/ch05/exercise.ipynb | `cell-1` line 4 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R123 | exercises/ch06/exercise.ipynb | `62d48965` line 1 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R124 | exercises/ch06/exercise.ipynb | `62d48965` line 4 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R125 | exercises/ch07/exercise.ipynb | `cell-0` line 48 | which OpenSysML loads silently but | FALSE-UNDER-STACK | which the OpenSysML runtime loads silently but  **NOTE:** The next line says 'sysml-toolkit and the pilot both flag' it, so the sentence is a contrast whose first term is false under the stack reading. Evidence: decisions/log.md:876 ('not by OpenSysML (which loads it silently) but by sysml-toolkit ... `validateNamespaceDistinguishibility`'); no DEFERRED entry. [C1][C4][C3]. The Pilot naming on line 49 is adjacent row A4. |
| R126 | exercises/ch07/exercise.ipynb | `cell-1` line 1 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R127 | exercises/ch07/exercise.ipynb | `cell-1` line 4 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R128 | exercises/ch08/exercise.ipynb | `cell-01` line 1 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R129 | exercises/ch08/exercise.ipynb | `cell-01` line 4 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R130 | exercises/ch09/exercise.ipynb | `cell-03` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R131 | exercises/ch09/exercise.ipynb | `cell-03` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |
| R132 | exercises/ch10/exercise.ipynb | `cell-03` line 2 | import opensysml | KEEP-ID | (no change) `import opensysml` (protected token). |
| R133 | exercises/ch10/exercise.ipynb | `cell-03` line 5 | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) `opensysml.connect(version="v0.9.0")` (protected: API call and version literal; the page's markdown names the runtime). |

## Adjacent rows (no `opensysml` on the line; outside the machine check)

A = conflating or naming fixes found by the second pass; D = stack definition insertions (class DEFINE). Same columns; the last column carries replacement and note.

| row | file | locator | quoted sentence | class | proposed replacement wording and note |
|---|---|---|---|---|---|
| A01 | chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb | `cell-15` line 1 | working around a real tool inconsistency | RUNTIME | working around a real inconsistency in the OpenSysML runtime  **NOTE:** 'the tool' here is the runtime (D-026). Same cell as row for L1 (cell-15), so 'the OpenSysML runtime' is used again rather than 'the runtime' only if the ACE wants each sentence self-contained; 'the runtime' is also acceptable. |
| A02 | chapters/ch07-execution/02-state-traces.ipynb | `cell-23` line 1 | The tool has a real hole here | FALSE-UNDER-STACK | The runtime has a real hole here  **NOTE:** D-023: false for sysml-toolkit v0.9.1, which warns. Same cell as the cell-23 row. |
| A03 | chapters/ch10-traceability-signoff/01-traceability-graph.ipynb | `ed18ec1d` line 3 | a gap in the API-JSON export, which has no structural | UNPROBED | a gap in the OpenSysML runtime's API-JSON export, which has no structural  **NOTE:** D-038 (DEFERRED.md:908-915): 'The API-JSON export OpenSysML v0.9.0 produces' - runtime only, no toolkit probe. Page's first prose mention is this cell (ed18ec1d precedes 02281b44), so the FULL name is used here and the 02281b44 row can then use 'the OpenSysML runtime' (still fine) or 'the runtime'. |
| A04 | exercises/ch07/exercise.ipynb | `cell-0` line 49 | and the pilot both flag | RUNTIME | and the OMG SysML v2 Pilot Implementation both flag  **NOTE:** Pilot named in full on first mention (convention: 'the OMG SysML v2 Pilot Implementation (then "the pilot")'); first mention on this page. Not a runtime/toolkit claim; class is naming only. Counted with the L48 row's contrast. |
| A05 | chapters/ch07-execution/conclusion.md | L13 | the tool lets through silently | FALSE-UNDER-STACK | the runtime lets through silently  **NOTE:** D-023: sysml-toolkit v0.9.1 does not let it through silently. Same sentence as the L13 row. |
| A06 | docs/case-studies/2026-09-30-energy-conservation-requirement-tie.md | L60 | so the OMG pilot had no live binding | RUNTIME | so the OMG SysML v2 Pilot Implementation (the pilot) had no live binding  **NOTE:** First mention of the Pilot in this file (convention: full name, then 'the pilot'). Naming only. |
| A07 | docs/case-studies/2026-09-30-energy-conservation-requirement-tie.md | L277 | The OMG pilot *does* catch | RUNTIME | The pilot *does* catch  **NOTE:** After first mention, 'the pilot'. Naming only. (Lines 61, 65, 69, 125, 278, 283 already say 'the pilot' or 'pilot'.) |
| A08 | exercises/ch10/exercise.ipynb | `a2487aff` line 19 | real OMG pilot did flag directly | RUNTIME | real OMG SysML v2 Pilot Implementation did flag directly  **NOTE:** First mention of the Pilot on this page. Naming only. |
| A09 | docs/case-studies/2026-09-30-energy-conservation-requirement-tie.md | L129 | That is a semantic | AMBIGUOUS | (line 129-130: 'no diagnostic in this toolchain computes')  **NOTE:** Claim 'no diagnostic in this toolchain computes' covers the runtime, the pilot and sysml-toolkit, but sysml-toolkit was not probed on this line (DL-116 item 7). Options: (a) keep 'this toolchain' (no bare OpenSysML; true as a statement about what was probed); (b) 'no diagnostic of the OpenSysML runtime or the pilot computes'; (c) (a) plus '(sysml-toolkit was not probed on this line)'. Recommend (c). |
| A10 | chapters/ch08-checking/01-assert-constraint-def.ipynb | `cell-07` line 1 | because this toolchain's solver never reaches through to either one | AMBIGUOUS | because sysml-toolkit's solver never reaches through to either one  **NOTE:** D-030/D-031 are probes of sysml-toolkit's `verify --solve` (Z3), so a component-naming reader would write sysml-toolkit. 'toolchain' is not the bare OpenSysML name, so the convention does not force a change. Options: (a) leave 'this toolchain' (b) 'sysml-toolkit' as shown. Recommend (b) where the sentence cites D-030/D-031, to keep the claim attached to the probed component. Not a lint-rule hit. |
| A11 | chapters/ch08-checking/conclusion.md | L13 | this toolchain does not compose two separately declared `assert constraint`s | AMBIGUOUS | sysml-toolkit does not compose two separately declared `assert constraint`s  **NOTE:** D-030/D-031 are probes of sysml-toolkit's `verify --solve` (Z3), so a component-naming reader would write sysml-toolkit. 'toolchain' is not the bare OpenSysML name, so the convention does not force a change. Options: (a) leave 'this toolchain' (b) 'sysml-toolkit' as shown. Recommend (b) where the sentence cites D-030/D-031, to keep the claim attached to the probed component. Not a lint-rule hit. |
| A12 | chapters/ch08-checking/index.md | L11 | this toolchain does not compose separately declared constraints | AMBIGUOUS | sysml-toolkit does not compose separately declared constraints  **NOTE:** D-030/D-031 are probes of sysml-toolkit's `verify --solve` (Z3), so a component-naming reader would write sysml-toolkit. 'toolchain' is not the bare OpenSysML name, so the convention does not force a change. Options: (a) leave 'this toolchain' (b) 'sysml-toolkit' as shown. Recommend (b) where the sentence cites D-030/D-031, to keep the claim attached to the probed component. Not a lint-rule hit. |
| A13 | exercises/ch08/exercise.ipynb | `cell-14` line 1 | D-030 says this toolchain's Z3 backend does not compose two separately | AMBIGUOUS | D-030 says sysml-toolkit's Z3 backend does not compose two separately  **NOTE:** D-030/D-031 are probes of sysml-toolkit's `verify --solve` (Z3), so a component-naming reader would write sysml-toolkit. 'toolchain' is not the bare OpenSysML name, so the convention does not force a change. Options: (a) leave 'this toolchain' (b) 'sysml-toolkit' as shown. Recommend (b) where the sentence cites D-030/D-031, to keep the claim attached to the probed component. Not a lint-rule hit. |
| A14 | exercises/ch08/exercise.ipynb | `cell-16` line 5 | toolchain's Z3 backend never composes two separately declared `assert | AMBIGUOUS | sysml-toolkit's Z3 backend never composes two separately declared `assert  **NOTE:** D-030/D-031 are probes of sysml-toolkit's `verify --solve` (Z3), so a component-naming reader would write sysml-toolkit. 'toolchain' is not the bare OpenSysML name, so the convention does not force a change. Options: (a) leave 'this toolchain' (b) 'sysml-toolkit' as shown. Recommend (b) where the sentence cites D-030/D-031, to keep the claim attached to the probed component. Not a lint-rule hit. |
| D1 | docs/setup.md | L136 | This tutorial models a system in SysML v2 and runs that model with Python. Two tools do that | DEFINE | OpenSysML ([opensysml.org](https://opensysml.org/)) is the open-source SysML v2 tool stack. This tutorial uses two of its components and names them by role: the OpenSysML runtime (Go; repository `Open-MBEE/OpenSysML`; Python package `opensysml`; pinned v0.9.0) and sysml-toolkit (Rust; `sysmlv2` binary; pinned v0.9.1). The OMG SysML v2 Pilot Implementation (EPL-2.0) is the conformance baseline and is always named as such. It is not one of the two tools the tutorial runs.<br><br>Then the existing text continues unchanged ('This tutorial models a system ... Two tools do that work ...'). Insert as a new paragraph immediately before line 136.  **NOTE:** Definition site (setup page). The last sentence ('not one of the two tools the tutorial runs') is true whichever way the ACE/Z rules on Pilot membership in 'OpenSysML' (the Pilot is not run by the tutorial), and keeps the Pilot out of 'both tools'. [C5][C6] |
| D2 | docs/reproducibility.md | L12 | building the rendered book) the Node toolchain. | DEFINE | Insert after the sentence ending on line 12 a new short paragraph: 'OpenSysML ([opensysml.org](https://opensysml.org/)) is the open-source SysML v2 tool stack. This tutorial pins two of its components: the OpenSysML runtime (Go; `Open-MBEE/OpenSysML`; Python package `opensysml`; v0.9.0) and sysml-toolkit (Rust; `sysmlv2` binary; v0.9.1). The OMG SysML v2 Pilot Implementation (EPL-2.0) is the conformance baseline.'   **NOTE:** Definition site (reproducibility page): the page pins versions, so each version attaches to a component here. Line 8-12 says 'four things exactly: ... the OpenSysML binary' (row for L11 renames it). [C2][C5][C6] |

## AMBIGUOUS list (for the ACE)

- A09 (docs/case-studies/2026-09-30-energy-conservation-requirement-tie.md L129): options in the row note.
- A10 (chapters/ch08-checking/01-assert-constraint-def.ipynb `cell-07` line 1): options in the row note.
- A11 (chapters/ch08-checking/conclusion.md L13): options in the row note.
- A12 (chapters/ch08-checking/index.md L11): options in the row note.
- A13 (exercises/ch08/exercise.ipynb `cell-14` line 1): options in the row note.
- A14 (exercises/ch08/exercise.ipynb `cell-16` line 5): options in the row note.

No row among the 132 matching lines is AMBIGUOUS.

## Reviewed, no change proposed

- `exercises/ch05/exercise.ipynb` `cell-0` line 10: 'filter ... some tools silently tolerate' (D-034: one tool, the runtime) names no tool; leave. D-034 body reads 'OpenSysML alone', which is DEFERRED text, protected.
- `chapters/ch09-coverage-sufficiency/02-evidence-completeness.ipynb` `0c378f59` and `exercises/ch09/exercise.ipynb` `cell-23`, `cell-27` say 'toolchain limits' (D-029 is the tutorial's wrapper parser; D-030/D-031 are sysml-toolkit): generic, not a bare OpenSysML use; leave.
- `chapters/ch08-checking/02-violation-witness.ipynb` `cell-16` 'nothing in this toolchain checks that the restated copy stays in sync' and `cell-10`, `3a3d9d15` (ch10) already name `sysml-toolkit`/`sysmlv2` correctly; leave.
- `docs/setup.md` lines 81-165 and `docs/reproducibility.md` lines 21-24 already name sysml-toolkit by its own name; leave.
- Other index/conclusion pages that say 'the tools' (ch05, ch08 index) without the name: no row.
