# Decision log

## DL-009 | 2026-09-25 | Cross-WP | Checkpoint PASS — notebook strategy revision user-test synthesis

Path: Handled by ACE

Decision: CHECKPOINT PASS. Strategy revision (file-based model loading, narration cells) is sound. Proceed to WP-6.

Agents: L13 Novice/Ch1-2, L14 SE Practitioner/Ch4-6, L15 Returning Learner/Ch7-8. ACE grounded self-test on Ch3/nb02.

Fixes applied (corroborated — pre-approved by Z):

- (L13 / blocking): `ch01/04-composition.ipynb` cell 5 called `model_to_dot` without importing it (NameError on every run). Pre-dates the strategy revision. Removed the broken call and its stale comment; `toaster.parts()` + `conn.close()` remain.
- (L14 / blocking): Ch4 narration (all three notebooks) said `item def Start/Finish/Cancel` "represent items flowing between action steps" — factually wrong. Inside `ApplyHeat`, `first start;` and `then done;` are sequence control keywords, not type references. The item defs are standalone declarations used as part types in `BreadHandling` (Ch5). Fixed: "declare typed items for structural use; they appear as part types in `BreadHandling` in Chapter 5, not as references inside `ApplyHeat` itself."

Non-blocking findings (do not fix without Z's direction):

- MF-16 (L15): Ch7/nb01 narration leads with `state Cycle` content even though nb01's demo exercises `DeliveredEnergy` via sympy. The narration is accurate for the ch07-cumulative.sysml file but orients the learner toward the state machine introduced in nb02. Concept statement is correct, model loads, seam is correct. Non-blocking.
- MF-17 (L14): Ch6/03 negative control uses `ReviewRecord(premises=[]) + validate_record()` rather than the `bad_source + assert not bad.ok` SysML parser pattern. Defensible — ch6/03 tests Hawkins schema enforcement, not the parser. A brief inline comment explaining the switch would reduce confusion for learners expecting the parser pattern.

ACE grounded self-test (Ch3/nb02): all 8 cells structurally correct. File-load pattern present. Narration accurately describes satisfy-assertion pattern and calc def. Tall seam labels A-F as the calc def construct (pre-existing phrasing — does not say "model file" explicitly, but names all three worlds). PASS.

## DL-008 | 2026-09-25 | Cross-WP | Notebook construction strategy revision + SA-2 update

Path: Handled by ACE — implementing Z's explicit direction; SA-2 update logged

Decision: Move all SysML model source from inline notebook strings to `models/chXX-cumulative.sysml` files. Notebooks load and display the model via `Path("../../models/chXX-cumulative.sysml").read_text()` + `print(source)` + `conn.load_from_content(source, strict=False)`. The 7-cell template becomes a minimum skeleton; additional markdown+code pairs between cells 2–4 are expected for narration. Five skills updated.

SA-2 update: SA-2 previously read "self-contained notebooks" meaning a standalone .ipynb could execute anywhere. The revised reading is "self-contained given the cloned repo structure" — `models/` is always co-located when a reader follows `docs/setup.md` (clone the repo). The standalone .sysml download benefit is enhanced, not diminished: the model files ARE the downloads. Fresh-kernel execution criterion is met because `models/` is always present in CI and in the cloned repo.

ACE review findings addressed:
- ACE-R1: SA-2 wording updated (this entry)
- ACE-R2: toaster-recipe A6 checklist changed to content-typed (not position-typed)
- ACE-R3: `print(source)` accepted; syntax highlighting is D-003 (deferred)
- ACE-R4: orchestrator-protocol updated with A3-before-A4 dependency note
- ACE-R5: bad_source exemption made explicit in tutorial-style-guide
- ACE-R6: execution order established: skills → generator scripts → notebooks → commit

Skill modifications (all permitted without escalation — tightening, clarifying, adding patterns):
- toaster-recipe: file-load cell 2 pattern; content-typed A6 checklist; ~10-line inline limit; bad_source exemption
- tutorial-style-guide: narration density rule; inline-SysML prohibition with bad_source exemption; A-F definition updated
- sysml-v2-toaster-model: model file structure section added; A3-authors-first rule
- opensysml-api: file-loading pattern added under Connection section
- orchestrator-protocol: A3-before-A4 dependency note added

## DL-007 | 2026-09-25 | WP-5 | Checkpoint PASS — Ch7-8 user-test synthesis

Path: Handled by ACE
Decision: CHECKPOINT PASS. Proceed to WP-6.
Rationale: Three A9 simulated learner agents ran (L10 Novice/Ch7, L11 SE Practitioner/Ch7+Ch8, L12 Returning Learner/Ch8) plus ACE grounded self-test of Ch8/nb03. One blocking issue found and fixed inline. Zero remaining blocking issues. All six notebooks have 7-cell m,m,c,c,c,m,m structure; all negative controls fire correctly; all Tall seams name three worlds; all concept statements are one sentence starting with "This notebook introduces".

Fixes applied (corroborated — pre-approved by Z):

- (L11+L10 / blocking): Ch7/nb03 cell 2 had `conn.close()` before cells 3-4, causing the negative control (cell 3) to fail at runtime on a closed connection. Fixed: `conn.close()` moved to end of cell 4, consistent with all other notebooks.
- (L11/L12): Ch8/nb02 and Ch8/nb03 concept statements used "produces" and "demonstrates" instead of the required "introduces". Fixed: rewrote both cell 0 statements to conform to the template.
- (L11): Ch7/nb03 cell 3 comment hedged about whether `bad.ok` would be False, contradicting the `assert not bad.ok` on the next line. Fixed: replaced with a clean "Expected failure: Real is undefined without ScalarValues::* import" comment.
- (L11+L10): All Ch7-8 notebooks with the cumulative model had `BreadEjector { ... }    state Cycle {` on a single line. Fixed: added newline before `state Cycle {` in all five affected notebooks.

Non-blocking findings (do not fix without Z's direction):

- MF-13 (L10): Ch7/nb01 cell 4 uses `sp.symbols(...)` and `sp.lambdify(...)` without bridging prose. A learner unfamiliar with sympy has no context for why these exist. Non-blocking per skill criteria; cell 5 Tall seam correctly labels the operation.
- MF-14 (L10): Ch7/nb01 cell 4 contains two cross-checks: lambdify evaluation and `model.eval()`. The template says one key operation per demo cell; having two makes the cell longer and potentially confusing for a novice.
- MF-15 (L10): `model.eval()` is called in Ch7/nb01 cell 4 without any prior introduction in cells 0-3. Non-blocking; the probe confirmed the API works and the Tall seam correctly frames it as O-S.

ACE grounded self-test: Ch8/nb03 stale round-trip logic verified: `hash_content(source)` matches current source; `source.replace(...)` changes the constraint threshold; `check_stale(record, revised_source)` returns True. All three assertions present.

## DL-006 | 2026-09-25 | WP-5 | SA-6 adaptation: use verify_satisfaction() in Ch8; verify_constraint(engine="check") unusable

Path: Handled by ACE
Decision: Ch8 uses `model.verify_satisfaction()` instead of `model.verify_constraint(name, subject, engine="check")` as specified in SA-6 and the Chapter plan.
Rationale: WP-5 probe confirmed `verify_constraint(engine="check")` returns "not covered" for any constraint — it does not evaluate attribute overrides and cannot discriminate nominal (holds=True) from slow (holds=False). `verify_satisfaction()` evaluates `assert satisfy` declarations correctly and returns `Verdict(holds=True/False, element=...)` for each. This is the right API for Ch8's learning outcome (SA-6 specifies "bounded model checking: opensysml `check` engine only" — the spirit is "no external model checkers," which `verify_satisfaction()` satisfies). Ch9 previously planned to introduce `verify_satisfaction()`; Ch9 is not yet built, so the introduction point moves to Ch8 with no impact on prior chapters. SA-6 skill entry to be updated to note this probe result. Z pre-approved minor corroborated fixes.

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

## DL-005 | 2026-09-25 | WP-4 | Checkpoint PASS — Ch5-6 user-test synthesis

Path: Handled by ACE
Decision: CHECKPOINT PASS. Proceed to WP-5.
Rationale: Three A9 agents ran (L7 Novice/Ch5, L8 SE Practitioner/Ch5+Ch6, L9 Returning Learner/Ch6) plus ACE grounded self-test of ch06-nb03. One blocking issue found and fixed inline. Zero remaining blocking issues. All six notebooks execute without error; all negative controls fire correctly (bad.ok=False or validate_record fails as expected); all Tall seams name three worlds; all concept statements are one sentence.

Fix applied (corroborated by L8 + L9 — blocking):

- MF-9 (L8/L9/corroborated): `validate_record()` in `evidence.py` had no check for empty `premises` on `asserted_inference` records. Ch6/nb03 cell 3 negative control relied on `assert len(errors) > 0` but the empty-premises record passed validation, causing an `AssertionError` at runtime. Fixed: added `if r.kind == "asserted_inference" and not r.premises: errors.append("asserted_inference requires at least one premise (Hawkins §3.1)")`. ACE self-test confirmed cell 3 now prints the expected error and the assert passes.

Non-blocking findings (do not fix without Z's direction):

- MF-10 (L7): Ch5/nb01 cell 6 exercise pointer forward-references a second-level element "you will add in Chapter 6" — a linear reader cannot complete the exercise until Ch6 is done. Non-blocking; wording could say "you will add later" but doesn't prevent Ch5 progress.
- MF-11 (L7): Ch5/nb03 cell 4 emits ~28 gRPC fork-detection lines ("FD from fork parent still in poll list") to stderr during `render_sysmld()`. Execution completes correctly; a novice may mistake the output for errors. Non-blocking; a comment noting the noise is benign would help.
- MF-12 (L9): Ch6/index.md Expected Result section uses "kind matching a requirement" rather than the exact string `'requirementDef'`. Non-blocking; the index is a navigation aid, not a specification.

ACE grounded self-test: ch06/nb03 cells 2–4 all execute cleanly after the fix. Fresh observation: the two-phase structure of cell 3 (bad record fails, assert passes) followed by cell 4 (good record passes, premises printed) is an unusually clear demonstration of the Hawkins schema enforcement pattern — the negative control and positive case are directly adjacent.

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
