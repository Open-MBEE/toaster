# Diagram/Text Integration Survey

Compiled from 9 parallel chapter-survey agents (2026-10-02), per
`docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md`. Each
chapter section below is a short prose strategy paragraph, then a table
(Notebook | Cells | Pattern | Current content | Proposed content | Rationale).
Literal proposed code/markdown is reproduced from each agent's own report,
not paraphrased. This is Phase A's complete output; Phase B is planned
separately against this document (see "Next step" at the end).

**Orchestrator consistency-check (Task 10, Step 2):** spot-checked 3 of 5
Pattern-2 proposals (Ch2, Ch4, Ch6) by grepping the real committed SVGs'
`<title>` elements directly. All three agents' claims about what their
chapter's diagram does and does not draw are confirmed exactly:
- `figures/ch02-structure.svg`: draws `ToastingSystem`, `HeatingSystem`,
  `ControlSystem`, `Toaster`, `Toaster::heating`, `Toaster::control`,
  `nominal`, `slow`, plus specialization/composition/typing edges. No
  `TimelyToast`, no metadata — matches the Ch2 agent's claim exactly.
- `figures/ch04-structure.svg`: draws exactly 5 nodes — `Toaster`,
  `Toaster::heating`, `Toaster::control`, `HeatingSystem`, `ControlSystem`.
  No `ApplyHeat`, `ToastBread`, item defs, or `ToastingSystem` specialization
  — matches the Ch4 agent's claim of a narrow depth-2 scope exactly.
- `figures/ch06-structure.svg`: draws exactly 3 nodes — `HeatingAssembly`,
  `HeatingAssembly::heatGen`, `HeatGenerator`. Confirms the Ch6 agent's claim
  that this is the narrowest-scoped diagram in the tutorial, and that most
  of the chapter's 213-line dump is structurally invisible to it.

No inconsistency was found in any of the three sampled chapters. The
remaining Pattern-2 proposals (Ch3, Ch5) were not independently re-checked
here, per Task 10's own "spot-check a sample, not all" instruction — each
was independently verified by its own agent against the real files, as
reported below.

---

## Chapter 1: System and Purpose

No Pattern-2 dump exists in this chapter (confirmed by grep). All four
notebooks have the construction-zone reflection-print duplication; two
(`02-part-def`, `04-composition`) already have a diagram occupying the
correct "After" slot, so the fix is pure deletion. The other two
(`01-abstract-def`, `03-specialization`) have no diagram, but each already
has a `model.find()`/`model.query()` confirmation cell sitting in the right
place in the skeleton, so no new cell needs to be added there either — this
chapter is unusual in that every Pattern-1/1b fix in it is a pure deletion.
One existing seam cell (`04-composition.ipynb`) needs a small rewording
because it quotes the now-removed printed block literally.

| Notebook | Cells | Pattern | Current content | Proposed content | Rationale |
|---|---|---|---|---|---|
| `01-abstract-def.ipynb` | cell 8 (`cell-07`) | 1b | `TOASTER_INCREMENT = f"{BREAD_DEF}\n{TOAST_DEF}\n{TOASTBREAD_DEF}\n{TOASTING_SYSTEM_DEF}"`<br>`print(TOASTER_INCREMENT)`<br>`source = Path(...).read_text()`<br>`model = conn.load_from_content(source, strict=False)`<br>`assert model.ok, ...` | Same, with `print(TOASTER_INCREMENT)` line removed. | Each fragment already printed individually at cells 2/4/6. No new confirmation cell needed — cells 12/14 (`model.find()`) already serve as Pattern 1b's required "E" step, and the existing seam cell (16) already points at them, not at the reprint. |
| `02-part-def.ipynb` | cell 6 (`cell-06`) | 1 | `TOASTER_INCREMENT = f"{HEATING_SYS_DEF}\n{CONTROL_SYS_DEF}"`<br>`print(TOASTER_INCREMENT)`<br>...load cell... | Same, print line removed. Bridge cell 11 and diagram cell 12 unchanged — already correctly positioned. | Diagram (`model_to_dot`, two disconnected boxes) already exists at cell 12 and does not need to move. Existing seam cell (16) refers to the still-present individual fragment prints and the cell-10 query, not the removed reprint — no edit needed there. |
| `03-specialization.ipynb` | cell 4 (`cell-04`) | 1b | `TOASTER_INCREMENT = TOASTER_SPEC_DEF`<br>`print(TOASTER_INCREMENT)`<br>...load cell... | Same, print line removed. | Purest duplication in the chapter: identical string printed twice, two cells apart. No diagram exists or is planned (specialization has no `model_to_dot()` representation). Cell 8's `toaster.specializations` query already serves as the confirmation step; seam cell 10 unaffected. |
| `04-composition.ipynb` | cell 8 (`cell-08`); seam cell 18 (`cell-13`) | 1 | Cell 8: `TOASTER_INCREMENT = f"{TOASTER_DEF}\n{CYCLE_TIME_ATTR}\n{HEATING_PART}\n{CONTROL_PART}\n}}"` + print + load. Seam cell 18: "`part def Toaster :> ToastingSystem { ... }` printed above loaded without error, and `toaster.parts()` returns the two part symbols shown below, confirming the composition is now part of the model." | Cell 8: print line removed. Seam cell 18 replaced with: "The assembled `Toaster` declaration loaded without error, and the diagram above confirms `heating` and `control` are part of the model." | Diagram already exists at cell 14 (full composition+typing, depth 2) and does not need to move; bridge cell 13 already correctly positioned. Unlike the other three notebooks, the existing seam cell here quotes the literal closed-brace block only the now-removed print ever showed — it must be reworded to point at the diagram instead, or it becomes a factual error once the print is gone. |

**Open questions from this chapter:** Figure captions in `02-part-def.ipynb`
(cell 13) and `04-composition.ipynb` (cell 15) are each a single sentence,
not the two `tutorial-style-guide/SKILL.md` requires. Pre-existing, not
touched by either target pattern, not named in the four enumerated cleanup
items — flagged for Z, not fixed here.

**Index.md check:** No drift. All four rows match their notebooks' live
headings exactly; already uses the `"01:"` separator convention.

---

## Chapter 2: Requirements and Assumptions

One Pattern-2 notebook (`03-judgment-context.ipynb`) and two Pattern-1b
notebooks. The chapter's diagram (whole-model, unscoped) covers all
structural content but cannot show the requirement's constraint body, the
attribute override value, or any judgment-record metadata — those stay as a
small residual excerpt. Both Pattern-1b fixes also require small rewordings
of downstream seam sentences that currently quote the exact closed-brace
block only the removed print produced.

| Notebook | Cells | Pattern | Current content | Proposed content | Rationale |
|---|---|---|---|---|---|
| `03-judgment-context.ipynb` | cell 2 | 2 | `print(source)` — full 55-line `models/ch02-cumulative.sysml` dump (spec's "~45 lines" estimate is stale; confirmed 55 as of 2026-10-02). | ```python\nrequirement_block = source[source.index("requirement def"):source.index("part nominal")].strip()\noverride_line = next(l.strip() for l in source.splitlines() if "attribute :>> cycleTime" in l)\nprint(requirement_block)\nprint(override_line)\n``` (verified by direct execution against the real file) | Diagram (whole-model `model_to_dot`) shows every structural fact already. Only the `TimelyToast` requirement's `require constraint` body (lines 36-45) and the `cycleTime` override value (line 53) are in the dump, outside the diagram's reach, and not reprinted elsewhere in the notebook. The metadata tag text is excluded from the residual because it's already reprinted verbatim later (cells 8/10) — keeping it in cell 2 too would just move the double-print earlier. |
| `01-requirement-def.ipynb` | cell 8; seam cell 13 | 1b | Cell 8: `TOASTER_INCREMENT = f"{TIMELY_TOAST_REQ}{CONSTRAINT_BODY}\n}}\n{NOMINAL_PART}"` + print + load. Seam cell 13 quotes the full assembled, closed-brace requirement block as "printed above." | Cell 8: print removed. Seam cell 13: "The `TimelyToast` fragments printed above loaded without error, and `model.find()`/`model.query()` confirm it's now part of the model." (17 words) | `TIMELY_TOAST_REQ`/`CONSTRAINT_BODY`/`NOMINAL_PART` each already printed individually (cells 2/4/6); existing cell 12 `model.find()`+`model.query()` already serves as the Pattern 1b confirmation. Seam cell needs rewording because it quotes a single closed-brace block only the removed print ever assembled — neither underlying fragment has the closing brace on its own. |
| `02-assumptions.ipynb` | cell 6; seam cell 11 | 1b | Cell 6: `TOASTER_INCREMENT = f"{SLOW_PART}\n{CYCLE_OVERRIDE}\n}}"` + print + load. Seam cell 11 quotes the full closed-brace `slow` block as "printed above." | Cell 6: print removed. Seam cell 11: "The `slow` fragments printed above loaded without error, and `slow.attributes()` confirms the override is now part of the model." (19 words) | Same shape as `01-requirement-def.ipynb`: existing cell 10 `model.find()` + `slow.attributes()` already serves as confirmation; seam cell needs the same kind of reword for the same reason (quotes a block only the removed print produced). |

**Open questions from this chapter:** A genuine conflict between two skills
— `toaster-recipe/SKILL.md` says judgment/analysis notebooks have no
construction zone and never assign `TOASTER_INCREMENT`, while
`toaster-review-protocol/SKILL.md`'s own "judgment record construction zone"
section explicitly prescribes building and printing a `TOASTER_INCREMENT`
fragment for a judgment record's model-side anchor tag.
`03-judgment-context.ipynb`'s cells 8-12 do exactly this, and that reflection
print is structurally identical to the Pattern 1/1b duplication this
redesign targets — but was *not* flagged as a fix target by this task's own
scope, since it is a judgment-record notebook under the second skill's
sanctioned pattern. Whether this double-print is a deliberate, sanctioned
exception or itself a defect requiring a Pattern-1b fix is a question this
survey surfaces but does not resolve — it requires a `skill-editor`-gated
decision about which skill's rule governs, before Phase B can touch it.

**Index.md check:** No drift. All three rows match; already uses `"01:"`.

---

## Chapter 3: Measures of Success

One Pattern-2 notebook (`03-threshold-judgment.ipynb`) and three Pattern-1b
notebooks, all four fixes being pure deletions since every notebook already
has its own confirmation query in place. A second, independent double-print
was found inside the Pattern-2 notebook itself, not originally named in this
chapter's task scope.

| Notebook | Cells | Pattern | Current content | Proposed content | Rationale |
|---|---|---|---|---|---|
| `03-threshold-judgment.ipynb` | cell 2 | 2 | `print(source)` — full 81-line `models/ch03-cumulative.sysml` dump (spec's "83 lines" is stale; confirmed 81 as of 2026-10-02). | ```python\nlines = source.splitlines()\nexcerpt = "\n".join(lines[35:47] + ["    ..."] + lines[61:65] + ["    ..."] + lines[66:80])\nprint(excerpt)\n``` — 30 real lines instead of 81. | Diagram (parts-only) draws only the Toaster/HeatingSystem/ControlSystem/nominal/slow skeleton. Residual: the `TimelyToast` requirement definition + usage (lines 36-47), the `slow` override + folded satisfy claim (lines 62-65), and `TimelyToastTest` (lines 67-80) — none diagrammable, confirmed against both the real SVG and `model_to_dot()`'s own node-kind logic. |
| `03-threshold-judgment.ipynb` (second finding, same notebook) | cell 13 | 1b | `TOASTER_INCREMENT = AS_C03_TAG`<br>`print(TOASTER_INCREMENT)` | Print line removed. | `AS_C03_TAG` already printed in full two cells earlier (cell 11) — a second, independent double-print inside the same whole-dump notebook, not named in the original task scope. `AS_C03_TAG` is a `MetadataUsage`, invisible to `model.find`/`model.query`; the real confirmation already exists at cell 23 (`get_review_record_refs`), narrated by cell 24. |
| `01-moe-definition.ipynb` | cell 11 | 1b | `TOASTER_INCREMENT = f"{TIMELY_USAGE}\n{AC_C03_TAG}"`<br>`print(TOASTER_INCREMENT)` | Print line removed. | `TIMELY_USAGE` confirmed at cell 6 (`model.find`+`model.query`); `AC_C03_TAG` is metadata, confirmed instead at cell 23 via `get_review_record_refs` — this tutorial's established idiom for metadata tags. No new cell needed. |
| `02-mop-candidate-eval.ipynb` | cell 4 | 1b | `TOASTER_INCREMENT = SLOW_WITH_CLAIM`<br>`print(TOASTER_INCREMENT)` + load | Print line removed. | `assert ... satisfy` is invisible to both `model.find`/`model.query` and `model_to_dot()`. Real confirmation already exists at cell 8 (`satisfy_relationships` + `model.eval()`), narrated by seam cell 10. |
| `04-verification-case.ipynb` | cell 10 | 1b | `TOASTER_INCREMENT = f"{VERIF_DEF_OPEN}\n{DOC_COMMENT}\n{SUBJECT_DECL}\n{OBJECTIVE_BODY}\n}}"` + print + load | Print line removed. | `VerificationCaseDefinition` is queryable; cell 14 already does `model.find()`+`model.query()`, narrated by seam cell 15 — the cleanest instance in the chapter, no API limitation involved. |

**Open questions from this chapter:** None beyond the second double-print
finding folded into the table above (flagged there so it isn't lost between
survey and Phase B planning — recommend the Ch3 Phase B contract name both
`01-moe-definition.ipynb` cell 11 and `03-threshold-judgment.ipynb` cell 13
explicitly). The design spec's own stated line count for this notebook's
dump (83) is off by two against the real file (81); use 81 in Phase B.

**Index.md check:** No drift. All four rows match; already uses `"01:"`.

---

## Chapter 4: Functional Decomposition

One Pattern-2 notebook (`03-completeness-check.ipynb`) and two Pattern-1
notebooks (both chapter diagrams already correctly positioned). A second,
unnamed construction-zone double-print was found in the Pattern-2
notebook's own judgment-tag cells, raising a classification question for
Phase B.

| Notebook | Cells | Pattern | Current content | Proposed content | Rationale |
|---|---|---|---|---|---|
| `01-action-def-ffbd.ipynb` | cell 14 | 1 | `TOASTER_INCREMENT = f"{APPLY_HEAT_DEF}\n{TOASTBREAD_REOPENED}"` + print + load. Cells 15/16 (bridge + diagram) already present, unchanged. | Print line removed; cells 15/16 untouched. | Diagram renders `ToastBread` (not `ApplyHeat` — confirmed against the real cell and SVG; an earlier spec draft mis-stated this). Bridge+diagram pair already in the correct "After" position. Downstream cell 23's "printed above" claims resolve to cells 10/12, unaffected. |
| `02-heating-refinement.ipynb` | cell 8 | 1b | `TOASTER_INCREMENT = f"{START_DEF}\n{FINISH_DEF}\n{CANCEL_DEF}"` + print + load | Print line removed. | No diagram exists or is planned. Existing cell 12 (`model.find()` loop over `Start`/`Finish`/`Cancel`) already serves as the Pattern 1b confirmation. Cell 13's "printed above" claim resolves to cells 2/4/6, unaffected. |
| `03-completeness-check.ipynb` | cell 2 | 2 | `print(source)` — full 117-line `models/ch04-cumulative.sysml` dump. | ```python\nlines = source.splitlines()\nnew_this_chapter = "\n".join(lines[16:32] + lines[37:47] + lines[107:116])\nprint(new_this_chapter)\n``` — 35 lines. | Scoped diagram (depth-2, rooted at `Toaster`) draws only `{Toaster, heating, control, HeatingSystem, ControlSystem}` — confirmed against the real SVG. Residual: `ApplyHeat` (17-32), `ToastBread`'s reopened body (38-47), the three item defs (108-116) — none drawn by `model_to_dot()`. The `aiC04Tag` metadata is excluded from the residual because the same notebook's own cells 9-11 reprint it moments later (see open question below). |
| `03-completeness-check.ipynb` (additional finding, same notebook) | cells 9-11 | — (flagged, not fixed; see open question) | Cell 9 declares+prints `AI_C04_TAG`; cell 11 sets `TOASTER_INCREMENT = AI_C04_TAG` and reprints it verbatim. | Not proposed — classification question, see below. | Structurally identical to the Pattern 1/1b duplication elsewhere, but prior planning docs (`decisions/declarative-construction-plan.md`) list this notebook as having no construction cells at all, since it's a judgment notebook. Whether it counts as in-scope under this redesign is a call for Z/the orchestrator, not this survey. |

**Open questions from this chapter:** (1) The cells 9-11 classification
question above. (2) `01-action-def-ffbd.ipynb` cell 17's existing caption is
one sentence, not two — pre-existing, outside this task's scope, flagged
only. (3) `03-completeness-check.ipynb` cell 3's bridge sentence has the same
single-sentence-with-colon style issue — remains factually accurate after
the trim, no edit required for correctness.

**Index.md check:** No drift. Both diagrams already named explicitly in the
table (per DL-089's earlier fix); confirmed still accurate.

---

## Chapter 5: Architecture and Allocation

One Pattern-2 notebook (`01-model-navigation.ipynb`, whose diagram is
unscoped and covers the dump's structural content completely — the only
chapter where the residual is genuinely empty) and two Pattern-1/1b
construction-zone fixes. **This chapter's survey also corrects a factual
error in `decisions/diagram-survey.md` itself**: that document's claim that
`02-allocate.ipynb` and `03-interfaces.ipynb` each separately re-print the
full 131-line dump does not match the real files, confirmed both by direct
read and by checking the historical commit that produced that document.

| Notebook | Cells | Pattern | Current content | Proposed content | Rationale |
|---|---|---|---|---|---|
| `01-model-navigation.ipynb` | cell 2 | 2 | `print(source)` — full 131-line `models/ch05-cumulative.sysml` dump. | Delete the `print(source)` line entirely. **Residual: none.** | Diagram is unscoped (whole-model `model_to_dot`), confirmed by direct comparison to draw every structural fact the dump contains. The notebook's own narrow teaching purpose (`model.find()`/`model.get()` navigation) doesn't need any of the non-structural content (action bodies, port/interface/allocation/requirement text) the diagram omits — that content belongs to the chapters that already taught it. Cell 1's own prose already summarizes what's new in prose form. |
| `02-allocate.ipynb` | cell 6 | 1b | `TOASTER_INCREMENT = f"{HEATING_SYSTEM_DEF}\n{TOASTER_WITH_ALLOCATION}"` + print + load | Print line removed (`# assembled, not printed` comment optional). | No diagram exists for allocation views. Existing cell 10 (`find_allocations`/`perform_relationships`) already serves as the Pattern 1b confirmation, narrated by seam cell 12 — which needs its "definitions printed above" phrase updated once the print is gone (left to Phase B, since exact wording depends on final cell numbering). |
| `03-interfaces.ipynb` | cell 10 | 1 | `TOASTER_INCREMENT = (f"{DURATION_PORT_DEF}\n{HEATING_SYSTEM_PORT}\n{CONTROL_SYSTEM_PORT}\n{TOASTER_WITH_INTERFACE}")` + print + load | Print line removed. | Diagram (`render_toolkit_interconnection`, the conjugated-port figure) already exists at cell 16, confirmed unaffected. Existing cell 14 (`port_type_mismatches`) already serves as confirmation, narrated by seam cell 18 — same "printed above" wording issue as `02-allocate.ipynb`, left to Phase B. |

**Open questions from this chapter (major):** `decisions/diagram-survey.md`'s
own row claiming `02-allocate.ipynb` cell 6 and `03-interfaces.ipynb` cell 10
each re-print the same 131-line dump as `01-model-navigation.ipynb` does not
match the real files — both cells only ever print their own small
`TOASTER_INCREMENT` fragment (9 and ~15 lines respectively), never the full
131-line `source`. Confirmed both against the live notebooks and against
`git show` of the commit that produced `diagram-survey.md`, so this is a
factual error in that prior document, not later drift. There is no
"triple-dump" to remove — the real, present issue in these two cells is the
ordinary construction-zone double-print already captured in the table above.
Flagging for Z/the orchestrator; no action needed beyond what's already
proposed.

**Index.md check:** Confirmed mismatch — `index.md` line 17 says
`[01: Model Navigation]` (title case) against the notebook's live heading
`# model navigation` (lowercase). Proposed corrected row:
```
| [01: model navigation](01-model-navigation.ipynb) | Navigate model elements by qualified name using `model.find()` and `model.get(fqn)`. |
```
Separator convention (`"01:"`) already correct, no change needed.

---

## Chapter 6: Recursive Decomposition

One Pattern-2 notebook (`03-stopping-judgment.ipynb`, the single largest cut
in the whole tutorial — 213 lines down to 66) and one Pattern-1 fix. A
second, smaller Pattern-1b instance was found inside the same Pattern-2
notebook. This chapter's survey also surfaces the clearest version of a
cross-chapter skill conflict already touched on by Chapter 2 and Chapter 5's
findings: `tutorial-style-guide/SKILL.md` has a hard rule requiring
`TOASTER_INCREMENT` to be printed as the reflection, which every Pattern 1/1b
fix in this entire survey directly contradicts.

| Notebook | Cells | Pattern | Current content | Proposed content | Rationale |
|---|---|---|---|---|---|
| `03-stopping-judgment.ipynb` | cell 2; markdown wrap-up cell 3 | 2 | Cell 2: `print(source)` — full 213-line `models/ch06-cumulative.sysml` dump (the densest block in the tutorial). Cell 3 (markdown) names 5 facts as "printed above." | Cell 2: ```python\nlines = source.splitlines()\nprint("\n".join(lines[137:164] + lines[173:212]))\n``` — 66 lines (down from 213). Cell 3 reworded to: "HeatGenerator, EnergyPort, HeatGenerationReq, ResistanceCoil, rated and weak loaded without error, and the diagram confirms HeatingAssembly composing heatGen, typed by HeatGenerator. The next cell checks what happens when an inference record's own required field is left empty." | Scoped diagram reaches only `{HeatingAssembly, heatGen, HeatGenerator}` (confirmed against the real SVG and `containment_subgraph`'s own test suite). ~137 of 213 lines are an exact, byte-identical repeat of Chapter 5's own already-printed cumulative model — the largest single redundancy found in this survey, independent of what the diagram can or can't show. Residual: `EnergyPort`, `GenerateHeat`, `HeatGenerator`'s doc/attributes, `HeatGenerationReq`, `ResistanceCoil`'s doc/attributes, and `rated`/`weak` with their overrides — none diagrammable. Cell 3 must be reworded because it names facts (e.g. the allocation) the trimmed print no longer shows. |
| `01-subsystem-requirements.ipynb` | cell 14 | 1 | `TOASTER_INCREMENT = (f"{GENERATE_HEAT_DEF}\n{ENERGY_PORT_DEF}\n{APPLY_HEAT_INCREMENT}\n{HEAT_GENERATOR_DEF}\n{HEATING_ASSEMBLY_DEF}")` + print + load | Print line removed. | Two diagrams (action-flow + interconnection) already sit immediately after in the correct position. Fragments already individually printed at cells 2/4/6/8/10. Cell 20's "printed above" claim resolves to those fragment prints, unaffected. |
| `03-stopping-judgment.ipynb` (second finding, same notebook) | cell 11 | 1b (flagged, not pre-decided) | `TOASTER_INCREMENT = AI_C06_TAG`<br>`print(TOASTER_INCREMENT)` | Proposed, if adopted: print line removed (assignment kept — required by `scripts/check_construction.py`). | Reprints text already shown two cells earlier (cell 9); cell 10's markdown already calls this duplication "deliberate." Not named in the spec's five-notebook Pattern-2 list — flagged as a genuine but previously-unnamed finding, not fixed unilaterally. Confirmation already exists at cell 22 (`get_review_record_refs`). |

**Open questions from this chapter (major, cross-chapter):**
`tutorial-style-guide/SKILL.md`'s own "Construction cells" section states as
a hard rule: *"`TOASTER_INCREMENT` is assembled... Print it as the
reflection."* This is the exact line every Pattern 1/1b fix in this entire
survey (all 9 chapters) contradicts. This is not a Ch6-specific issue — it
needs one centralized `skill-editor`-gated update to that skill line, done
once before or alongside Phase B, rather than left to drift notebook by
notebook. Also: whether to trim the `assumption_refs` text in cell 16, which
already supports the Pattern-2 trim rather than conflicting with it — a
reviewer should confirm it reads naturally post-trim.

**Index.md check:** Confirmed mismatch, all three rows (not just the one
named in the task prompt) — title case vs. lowercase live headings:
```
| [01: level-2 function and logical carrier](01-subsystem-requirements.ipynb) | ... |
| [02: level-2 physical realization](02-second-level.ipynb) | ... |
| [03: stopping judgment](03-stopping-judgment.ipynb) | ... |
```
Separator convention already correct (`"01:"`), no change needed.

---

## Chapter 7: Execution and Experiments

No Pattern-2 dump (confirmed by grep). One Pattern-1 fix (diagram already
correctly positioned) and one Pattern-1b fix requiring one new confirmation
line, since this chapter has no existing query to reuse for one of its two
fragments. The third notebook has no construction zone at all.

| Notebook | Cells | Pattern | Current content | Proposed content | Rationale |
|---|---|---|---|---|---|
| `02-state-traces.ipynb` | cell 16 | 1 | `TOASTER_INCREMENT = f"{CYCLE_DEF}\n{TOASTING_SYSTEM_INCREMENT}"` + print + load | Print line removed; cells 17/18 (bridge + diagram) unchanged. | `CYCLE_DEF`/`TOASTING_SYSTEM_INCREMENT` already printed individually (cells 12/14). Bridge+diagram pair (state-flow render) already correctly positioned. Cell 31's "definitions printed above" phrase resolves to the individual fragment prints, unaffected. |
| `01-calc-energy.ipynb` | cell 9; markdown cell 10 | 1b | `TOASTER_INCREMENT = f"{HEAT_GENERATOR_INCREMENT}\n{RATED_INCREMENT}"` + print + load. Cell 10: two sentences about the negative control. | Cell 9: print removed; one line added: `delivered_energy = model.find("ToasterDemo::HeatGenerator::deliveredEnergy")`<br>`print(f"HeatGenerator::deliveredEnergy: kind={delivered_energy.kind!r}, id={delivered_energy.id!r}")`. Cell 10: one sentence prepended: "`HeatGenerator::deliveredEnergy` is now part of the loaded model, confirmed by `model.find`." (11 words) | Unlike every other Pattern-1b fix in this survey, this notebook has no existing confirmation query to reuse — a new `model.find()` cell (reusing `02-state-traces.ipynb`'s own established idiom) must be added, plus one markdown sentence interpreting it, per the style guide's narration-density rule. |
| `03-param-sweep.ipynb` | — | none | No construction zone at all — confirmed by direct read; cell 2 loads the cumulative model directly, no fragment-declaration cells precede it. | No change. | Matches `toaster-recipe`'s own rule that param-sweep notebooks have no construction zone. |

**Open questions from this chapter:** (1) Two intermediate sub-assembly
reprints exist (`02-state-traces.ipynb` cell 12, `01-calc-energy.ipynb` cell
7) that are not the *final* `TOASTER_INCREMENT` reflection either target
pattern defines — flagged, not proposed, since they're outside the spec's
named scope. (2) Three real em-dash violations found in
`02-state-traces.ipynb` (cells 29, 32) — outside this task's scope, flagged
for Z. (3) The rolling-cleanup item 1 premise (a curly-vs-straight apostrophe
drift in this chapter's `index.md`) does not hold on direct byte-level
inspection — 0 curly apostrophes found anywhere in the file; recommend
confirming with Z whether this was already fixed or conflated with Ch5/Ch6's
actual (different) title-case defect.

**Index.md check:** No correction needed — confirmed byte-for-byte match
between all three table rows and their notebooks' live headings (apostrophe
form included). Separator convention already correct.

---

## Chapter 8: Checking and Revision

No Pattern-2 dump (confirmed directly; an earlier spec draft wrongly claimed
one existed here). The chapter's one diagram (grounding a specific
sibling-usage/specialization claim) is already correct and untouched. Two
Pattern-1b fixes, both pure deletions. This chapter is also named in two of
the four enumerated rolling-cleanup items: the index.md separator convention
and the `01-invariant-def.ipynb` filename rename.

| Notebook | Cells | Pattern | Current content | Proposed content | Rationale |
|---|---|---|---|---|---|
| `01-invariant-def.ipynb` | cell-08 | 1b | `TOASTER_INCREMENT = f"{HEAT_GEN_CHECK_USAGE}\n{CHECK_DURATION_ATTR}\n\n{DELIVERED_ENERGY_BOUND}\n"` + print + load | Print line removed. | Diagram cells (cell-03a/03b/03d) ground an earlier, separate claim and are already correct — no change needed there. This reflection print is independent of them. Existing cell-09/cell-10 (`model.find()`+`model.query()`) already serves as the Pattern 1b confirmation. |
| `02-violation-witness.ipynb` | cell-20 | 1b | `TOASTER_INCREMENT = AS_C08_TAG`<br>`print(TOASTER_INCREMENT)` | Print line removed (bare deletion; no new confirmation inserted — see open question). | `AS_C08_TAG` already printed at cell-18. Confirmation exists later at cell-32/33 (`get_review_record_refs`); inserting a nearer one would be premature (the record it anchors isn't built yet) and would itself be a third printing. |
| `03-revision-flow.ipynb` | — | none | No construction zone — confirmed by grep (`TOASTER_INCREMENT` appears zero times). | No change. | Matches `toaster-recipe`'s own rule for analysis notebooks (rebuilds a Python `ReviewRecord`, no new model element). |

**Open questions from this chapter:** Whether `02-violation-witness.ipynb`
should get a nearer confirmation query right after the trimmed cell-20,
matching `01-invariant-def.ipynb`'s immediate-confirmation idiom more
literally, instead of relying on the later cell-32/33 confirmation — the
agent recommends relying on the existing later one (parsimony), but flags it
as a reviewer judgment call.

**Index.md check (rolling-cleanup item 2):** Proposed, dash → colon
separator for all three rows, with row 1's link target updated for the
proposed rename:
```
| [01: assert constraint](01-assert-constraint-def.ipynb) | State `deliveredEnergyBoundedBySupply` as a real SysML constraint; confirm it is really in the loaded model. |
| [02: proof versus point evaluation](02-violation-witness.ipynb) | Contrast `verify_holds()`'s universal proof with `verify_satisfaction()`'s point evaluation; show the loop catching a fully broken variant as `violated` and a merely weakened variant as `undecided`; record the proof as engineering evidence with its own real limits stated. |
| [03: stale record detection](03-revision-flow.ipynb) | Loosen the lemma's own bound; show `check_stale()` marking the existing record for re-review. |
```

---

## Chapter 10: Traceability and Sign-off

No Pattern-2 dump (confirmed directly; an earlier spec draft wrongly claimed
one existed here, same as Ch8). One narrow, non-canonical instance of the
underlying duplication concern was found, not matching either pattern's
literal shape. The chapter's own unscoped structure diagram is unaffected.
This chapter is named in rolling-cleanup item 2 (separator convention).

| Notebook | Cells | Pattern | Current content | Proposed content | Rationale |
|---|---|---|---|---|---|
| `01-traceability-graph.ipynb` | cell 33 (delete); cell 32 (one-word edit) | "1b-style" (does not match either pattern's literal before/after shape — flagged for Phase B scoping, see open question) | Cell 32 (markdown), last sentence: "The subsetting construct below is how that is stated." Cell 33 (code): `print(ENERGY_CONSERVATION_REQ_DEF)` — a verbatim reprint of cell 27's own fragment, with the real confirmation query (cells 35-36) already in place immediately after. | Cell 32 last sentence: "The subsetting construct shown above is how that is stated." Cell 33: deleted outright. | This notebook doesn't follow the canonical construction-zone shape at all (model loaded once at the top, before any construction narrative; `TOASTER_INCREMENT`, assigned at cell 39, is never printed) — so Pattern 1/1b's literal shape doesn't apply. But cell 33 is a real instance of the same underlying concern: a pure narrative recap of text already shown five cells earlier, immediately before a real confirmation query (cells 35-36) that already does the job. Fix is pure deletion, stricter than Pattern 1b's add-a-query default, since a query already exists. |
| `02-judgment-synthesis.ipynb` | — | none | No construction zone — confirmed by grep. | No change. | Judgment/reconstruction notebook, reconstructs Python `ReviewRecord` objects from earlier chapters; no new model content. |
| `03-engineering-signoff.ipynb` | — | none | No construction zone — confirmed by grep. | No change. | Synthesizes one new `ReviewRecord` from citations; judgment-record-only construction (name fields, narrate, print once each), not a model-construction zone with a reflection-print problem. |

**Open questions from this chapter:** Whether the cell-33 finding (above)
counts as in-scope for a Phase B task under the spec's Decision 2 wording,
given it doesn't match Pattern 1/1b's literal shape, or whether it should be
folded into Phase B's acceptance criteria as an explicitly-named extra item
(the same mechanism already used for the four enumerated cleanup items).

**Index.md check (rolling-cleanup item 2):** Proposed, dash → colon
separator for all three rows (concept-column prose untouched):
```
| [01: traceability graph](01-traceability-graph.ipynb) | ... |
| [02: judgment ledger](02-judgment-synthesis.ipynb) | ... |
| [03: engineering synthesis](03-engineering-signoff.ipynb) | ... |
```

---

## Cross-chapter open questions

For Z/the orchestrator to triage before Phase B's own plan is written:

1. **A skill contradiction that blocks every proposed fix in this survey.**
   `tutorial-style-guide/SKILL.md`'s "Construction cells" section states a
   hard rule: *"`TOASTER_INCREMENT` is assembled from the fragment
   variables... Print it as the reflection."* Every single Pattern-1/1b fix
   proposed across all 9 chapters above removes that print. This needs one
   centralized `skill-editor`-gated update, decided once, before or
   alongside Phase B — not left implicit or discovered independently by
   each chapter's Phase B contract. (Surfaced independently by the Ch2, Ch5,
   and Ch6 agents.)

2. **A second, related skill contradiction, narrower in scope.**
   `toaster-recipe/SKILL.md` says judgment/analysis notebooks have no
   construction zone and never assign `TOASTER_INCREMENT`, while
   `toaster-review-protocol/SKILL.md` explicitly prescribes building and
   printing a `TOASTER_INCREMENT` fragment for a judgment record's
   model-side anchor tag — and several real notebooks
   (`ch02/03-judgment-context`, `ch03/01-moe-definition` and
   `03-threshold-judgment`'s own tag cells, `ch04/03-completeness-check`
   cells 9-11, `ch06/03-stopping-judgment` cell 11, `ch08/02-violation-witness`,
   `ch10/01-traceability-graph`) do exactly this. Whether these
   judgment-tag reflection prints are a deliberate, sanctioned exception or
   themselves a Pattern-1b-style defect is a single, cross-cutting
   classification question — not something to resolve chapter by chapter.
   (Surfaced by Ch2's agent; related instances independently found by Ch3,
   Ch4, Ch6, Ch8, and Ch10's agents without being asked to look for this
   specific pattern.)

3. **`decisions/diagram-survey.md` contains a factual error.** Its own row
   for `ch05/02-allocate.ipynb` and `03-interfaces.ipynb` claims both
   notebooks re-print the full 131-line cumulative-model dump, "no candidate
   ... diagram fatigue, not a real reduction." This does not match the real
   files (confirmed both by direct read and by checking the historical
   commit that produced that document) — both cells only ever print their
   own small `TOASTER_INCREMENT` fragment. There is no triple-dump to
   remove. Recommend correcting this row in `decisions/diagram-survey.md`
   itself as a small, separate administrative fix (not a chapter-content
   edit), distinct from anything Phase B needs to do.

4. **Three line-count figures in the governing spec are stale**, confirmed
   against the real files as of 2026-10-02: Ch3's dump is 81 lines (spec
   says 83); Ch2's dump is 55 lines (spec says "~45"). Use the real counts
   in Phase B, not the spec's.

5. **A classification question for `ch04/03-completeness-check.ipynb` cells
   9-11.** This notebook's judgment-tag reflection print (`AI_C04_TAG`) is
   structurally identical to the duplication this redesign targets, but
   prior planning documents (`decisions/declarative-construction-plan.md`)
   explicitly list this notebook as having no construction cells at all.
   Overlaps with cross-chapter item 2 above but is called out separately
   since it also bears on whether this notebook is a "construction
   notebook" under the original declarative-construction plan's own
   classification.

6. **`ch06/03-stopping-judgment.ipynb` cell 11** has a second, smaller
   Pattern-1b-shaped duplication (`AI_C06_TAG` reprinted two cells after its
   own fragment print) that was not named in the spec's five-notebook
   Pattern-2 list. Proposed fix is included in the Ch6 table above but
   flagged, not pre-decided, consistent with cross-chapter item 2.

7. **`ch10/01-traceability-graph.ipynb` cell 33** (see Ch10 table) is a real
   instance of the underlying duplication concern that matches neither
   pattern's literal before/after shape. Recommend folding it into Phase B's
   Ch10 task as an explicitly-named extra item, the same mechanism already
   used for the four enumerated cleanup items.

8. **Minor, out-of-scope items flagged by individual agents, not acted on:**
   single-sentence figure captions in `ch01/02-part-def.ipynb` (cell 13),
   `ch01/04-composition.ipynb` (cell 15), and `ch04/01-action-def-ffbd.ipynb`
   (cell 17) — `tutorial-style-guide/SKILL.md` requires exactly two
   sentences; three real em-dash violations in `ch07/02-state-traces.ipynb`
   (cells 29, 32); and the premise of rolling-cleanup item 1 (a curly vs.
   straight apostrophe drift in Ch7's own `index.md`) does not hold on
   direct inspection — recommend confirming with Z whether this was already
   fixed or conflated with Ch5/Ch6's actual (different) title-case defect.

---

## Index.md corrections

Separator-convention fix (`"01 -"` → `"01:"`), rolling-cleanup item 2 — Ch8
and Ch10 (full rows given in their own chapter sections above). Heading-case
sync fix, rolling-cleanup item 1 — Ch5 (one row) and Ch6 (all three rows,
given in their own chapter sections above). Ch1, Ch2, Ch3, Ch4, and Ch7 need
no index.md correction — confirmed already accurate by direct read.

---

## Proposed rename (Ch8)

**Proposed new filename:** `chapters/ch08-checking/01-assert-constraint-def.ipynb`
(renamed from `01-invariant-def.ipynb`), following the exact precedent of
the Ch5 rename (`01-concept-selection.ipynb` → `01-model-navigation.ipynb`,
commit `0b3151b`). The notebook's own H1 heading already reads "assert
constraint"; this matches the repo's own `-def`-suffix convention for
notebooks that declare a specific SysML construct type
(`01-abstract-def.ipynb`, `01-requirement-def.ipynb`,
`01-action-def-ffbd.ipynb`).

**Files needing their reference updated if the rename proceeds** (confirmed
by direct repo-wide grep for `invariant-def`/`invariant_def`; the latter had
zero hits anywhere):

1. `myst.yml` line 67 — TOC entry.
2. `chapters/ch08-checking/index.md` line 17 — Ingredients-table link (shown
   fixed in the Ch8 section above).
3. `chapters/ch08-checking/02-violation-witness.ipynb`, cell-01 — cross-reference
   link target only (`[Ch8-01](01-invariant-def.ipynb)` →
   `[Ch8-01](01-assert-constraint-def.ipynb)`); surrounding sentence
   untouched.
4. `exercises/ch08/exercise.ipynb` line 28 — prose referencing the notebook
   by path.
5. `scripts/check_construction.py` line 280 — active code registry entry;
   would silently stop checking the renamed file if not updated.
6. `DEFERRED.md` lines 693 and 798 — live, currently-accurate D-029/D-030/D-031
   workaround notes that point at this file by path.

**Historical-record files found but NOT recommended for update** (per the
same convention the Ch5 rename precedent established): `decisions/diagram-survey.md`
line 219; `decisions/log.md` lines 892, 903, 1093, 1225, 1239;
`decisions/audits/ch08-layer-audit.md` lines 140, 240 (the record that
recommended this very rename — correctly worded in the past tense already);
`decisions/user-testing-grid/M2-practitioner.md` line 17;
`docs/superpowers/plans/2026-10-01-diagram-survey-phase2-plan.md` lines 819,
825, 832, 839.

**Ambiguous, flagged for the orchestrator's own call, not pre-decided:**
`docs/superpowers/plans/2026-10-02-diagram-text-integration-phase-a-plan.md`
(this very Phase A plan, which names the old filename throughout) and
`docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md` (the
governing spec, which also names it). The surveying agent recommends leaving
both as-is — they are records of what Phase A was asked to find under the
old name, not live links requiring resolution — but flags the call as the
orchestrator's to make, not its own.

**Total:** 6 live files need updating, plus the file itself (7 touched).
5 files are historical and should be left alone. 2 files are ambiguous.

---

## Next step

Phase A is now complete. Per this survey's own governing plan
(`docs/superpowers/plans/2026-10-02-diagram-text-integration-phase-a-plan.md`,
Task 10 Step 4), the next step is to invoke `superpowers:writing-plans`
again, for **Phase B** (implementation), using this document and
`docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md` as
its two inputs. Phase B's own plan will have one task per chapter (or per
notebook, where warranted), each a `CONTRACT.md` executed through this
repo's own builder/reviewer harness exactly as every Phase 2 chapter task
was — builder `claude-sonnet-5`, reviewer `claude-opus-5-5`, a
`simulated-learner` spot-check for any notebook whose prose shrank
materially, per spec Decision 3 and the Verification section. Phase B's own
plan must also resolve, or explicitly route to the ACE/Z, the 8 cross-chapter
open questions above before any chapter's own contract is dispatched —
especially open questions 1 and 2, since they affect the exact wording of
nearly every proposed fix in this document.
