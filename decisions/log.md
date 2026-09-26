# Decision log

## DL-017 | 2026-09-26 | Pass 1 (M2) | Z walk-through: mechanisms as laws, MoE/MoP as judgment, two-tier conformance

Status: COMPLETE

Path: Escalated to Z. The ACE dry run (DL-101..114 in `decisions/ace-dry-run.md`) ruled three scenarios from Z-statements that were recorded too rigidly; Z corrected them by popup on 2026-09-26.

Decision:
- **Mechanisms (Z):** physical laws such as Joule heating (I^2 R) are mechanisms: modeling decisions grounded in established engineering practice, the laws we use to reason about behavior. "Sub-behavior" is dropped from prompts, keys and skills. A law that holds for any solution (energy balance) stays functional; the same kind of law as applied to a chosen component is logical. The confirmed tutorial definition of *mechanism* was extended with the modeling-decision framing (Z chose "add the modeling-decision framing").
- **MoE versus MoP (Z):** contextual modeling judgment, justified for each case; how long toast takes could be either. Tutorial edges for *MoE* and *MoP* now say so and no longer fix examples. The earlier ACE ruling that swapped the two was wrong.
- **Conformance (Z):** two tiers. Language conformance is always on; project conformance is staged (applied from a declared chapter and section, negative control, open until applied). G4 is reframed accordingly; recipe 5 in `opensysml-query` is the port-type check, tested against a mismatch and a specialization.
- Wording changes: AGENTS.md 1.5 and 1.9, `architecture-layers`, `opensysml-query`, `ace-protocol`, `z-model.md` (Z-5, Z-6 revised; Z-25 to Z-27 added).

Rationale: Z's corrections; nothing else changed. Confirmed glossary definitions (mechanism, MoE, MoP) were edited at Z's direction in this walk-through and are shown to Z for review; `glossary check` passes.

Z's decision: as above.

## DL-016 | 2026-09-26 | Pass 1 (M1) | Glossary confirmation triage: 11 tutorial edges, 35 tutorialDefinition proposals

Status: COMPLETE (Z confirmed the batch, 2026-09-26)

Path: Handled by ACE (Fable 5.1, cold session, from Z's recorded statements) for 43 items / Escalated to Z for 4 (physical architecture, allocation, dynamical system, specialization). Z ruled all four; ACE rulings are recommendations Z skims, since only Z sets `gl:confirmed`.

Decision:
- Tutorial edges: functional architecture, policy, selection among alternatives, MoE, TPM unchanged. Edited: logical architecture (Douglas says "who"; "how" is our sharpening), mechanism (word and determinism emphasis marked ours; also refines Astrom Sec. 3.2), logical component (abstract-part-def/perform stated as the tutorial's modeling convention), behavior (not prescribed; derived by analysis or simulation and judged against intent, never "never asserted").
- MoP (Z): a MoP characterizes a requirement but does not make one; the requirement also needs a threshold and a means of checking. Refines SEBoK MoP, and now cites SysML (MoP is metadata identifying an attribute, 9.3.4.2.2; a requirement is a constraint a valid solution must satisfy, 8.3.21.8; a verification case's pass criteria are modeled explicitly, 7.24.1).
- Physical architecture (Z, E-1): lens vocabulary is not barred but may not be load-bearing; kept only if it makes the term easier to learn. The "feasibility/utility" sentence was replaced by plain wording (each part fits the logical interfaces and meets the derived thresholds).
- Allocation (Z, E-2): SysML v2 sense governs because the model is the executable source of truth; new tutorial refinement edge acknowledges the SEBoK and Douglas senses and says why SysML is used. Rule recorded: our terms position themselves as refinements or interpretations of INCOSE/SEBoK wherever possible, never contradict SysML v2 semantics, and where they strictly disagree SysML v2 governs.
- Ties (Z, E-3): Astrom over Sutton for `dynamical system` (statements must stay consistent with both; reassess on hard contradiction); SysML over KerML for `specialization` (closer to our abstraction level; the two must not contradict).
- Tutorial definition is a derived view, not a stored pointer (Z), and the sources are kinds of definition, not rivals (Z): SEBoK, Hawkins, Astrom and Sutton supply the idea (gl:conceptual); the OMG specs supply formal, checkable semantics (gl:formal); Douglas supplies analogy and story (gl:didactic); this tutorial's own edges are the bridge (gl:bridge). `queries/tutorial_definitions.rq` returns the best confirmed edge of each kind per term; `gl:rank` orders sources of the same kind only and `gl:preferred` breaks ties within one source (behavior-2, emergence-2, function def. 3, Sutton policy 1.3, Astrom dynamical-system). `gl:tutorialDefinition` removed. The one-line gloss comes from the bridge edge, else the idea, else the formal semantics, else the story. CLI `tutorial [--proposed]` previews the view; `check` errors on ambiguity within a kind and warns on terms with nothing confirmed. The earlier allocation ruling (SysML governs) is superseded by this framing; the definitions are treated as non-contradicting.
- Data fixes: replaced weak or mismatched quotes (Hawkins appropriateness and assumption, Astrom control law, SEBoK selection, SysML verification and view), each machine-verified on its page; added term `concept` with a SEBoK edge to ground the "concept selection" claim.

Rationale: Z-recorded positions (canonical first, refinements only, no invention, judgment never eliminated, lens vocabulary allowed only when it earns its place). `glossary check` and `verify-sources` pass; 0 confirmed, 82 proposed.

Remaining: tutorial-edge locators still say "Foundations (AGENTS.md Part 1...)" and are fixed at M2.

Z's decision: confirm the batch as Z's own after the Douglas quotes were verified ("confirm the batch as mine but verify the Douglas quotes first"). Applied by Claude on Z's instruction: all 82 edges set `gl:confirmed`, `gl:confirmedBy "Z"`.
Douglas verification: all 9 quotes re-checked against fresh YouTube transcripts (Part 3 `UTm1ORuZ1dg`, Part 4 `Iblo2Il-pOA`, read in Z's Chrome, 2026-09-26). Seven matched their locators exactly; two locators were corrected (requirement 1:41 -> 1:43, traceability 9:45 -> 9:43). No quote failed. Every other quote was already machine-verified on its PDF page (`verify-sources` ok).

## DL-015 | 2026-09-26 | Pass 1 | Z-directed alignment pass: Foundations, glossary, layer and query skills, ACE definition, handoff

Status: PENDING

Path: Escalated to Z — this pass was specified interactively by Z (plan approved 2026-09-26, `/Users/z/.claude/plans/now-we-re-starting-to-merry-music.md`). Because Z directed it, the skill-editor escalate-to-Z gates (multi-archetype change, >20% of a skill, new capability, learning-outcome effect) are satisfied by this entry; this is a one-off Z override, not a change to file authority.

Decision (intended change, one sentence): align AGENTS.md (new Part 1 Foundations, existing roster kept as legacy Part 2), CLAUDE.md, `ace-protocol`, `skill-editor`, and three new skills (`architecture-layers`, `opensysml-query`, `tutorial-glossary`) with Z's what/how/where intent, backed by a new local glossary knowledge graph (`glossary/`), a query-helper fix in `src/toaster/query.py`, gap records G1-G7, and a handoff file `decisions/next-passes.md`.

Skill edit pre-entry (skill-editor step 1; Z-directed pass): existing skills `ace-protocol`, `skill-editor` and `opensysml-api` are edited in this pass. Revert record: their text at commit `21c26e5` (`git show 21c26e5:.claude/skills/<skill>/SKILL.md`), which precedes the first edit. No work package is mid-loop; this is a Z-directed alignment pass.

Progress and corrections (2026-09-26): gate M1 closed (DL-016); AGENTS.md Part 1 and CLAUDE.md committed (step 5); re-probes recorded in `decisions/probes.md`. Gap status changes from the re-probes: G3 resolved (spec form works, nothing to file), G2 not a bug, G1 partial (name allocations, connections and flows), G4 open, G7 OpenSysML-only (sysml-toolkit resolves cross-file imports). Correction to the plan: sysml-toolkit v0.9.1 summary mode is a Rust and WebAssembly option only, not in the CLI or Python.

M2 status (2026-09-26): steps 6 to 10 done. New skills `architecture-layers`, `opensysml-query`, `tutorial-glossary` (snippets executed by `tests/test_skill_snippets.py`); `ace-protocol` (triage role, Fable 5.1, Z-model, audits), `skill-editor` (Z-directed clause, generated-region exemption, no-contradiction check) and `opensysml-api` corrections. ACE dry run recorded in `decisions/ace-dry-run.md` (13 of 14 matched the key; 1 defensible divergence changed the skill wording). Cold-start test at three model tiers recorded in `decisions/cold-start.md` (all passed; findings fixed). Awaiting Z's skim of the expected-outcome key.

Overrides recorded (Z): (1) one-logical-change-per-session (AGENTS.md section 3, rule 1) is suspended for this pass; commits remain one logical change each. (2) A2-owned files (`pyproject.toml`, `uv.lock`, `.gitignore`, `.github/workflows/ci.yml`, `src/toaster/query.py`, `tests/`, AGENTS.md, CLAUDE.md) and A8-owned files are edited in this pass by Z direction. Gates: M1 (glossary confirmed by Z), M2 (documents and skills, dry runs), M3 (query fix, gap records, handoff).

Revert record: the verbatim pre-edit text of every file this pass changes is the tree at commit `8b52280` (branch point of `pass1/harness-alignment`). To revert any edit: `git show 8b52280:<path>`. The one paragraph replaced in AGENTS.md section 3b (the "Functional-first framing rule") is preserved here verbatim:

> **Functional-first framing rule:** A10 ensures that the three-layer architecture is narrated explicitly in order: functional (what the system does, via verb-noun `action def` and abstract functional role definitions) -> logical (how functions are partitioned into implementation-agnostic components with defined interfaces, via `abstract part def` + `flow`/ports) -> physical (concrete part selections that fulfill logical roles, via `part def` with physical attributes). `abstract part def ToastingSystem` and its specializations are the **logical** layer — they define component boundaries and interfaces without committing to a physical solution. Narrative cells must use verb-noun convention (e.g., "transform bread into toast," "apply thermal energy") when describing functions, and must distinguish logical structure (with interfaces) from physical implementation (concrete part selection).

Recorded here for the pass (each is detailed in the plan and in `decisions/next-passes.md` once written):
- Approved departure (Z): the tutorial's "logical" `differsFrom` SEBoK's "logical architecture" (which contains the functional view). Z's approval was given in planning 2026-09-26 and is quoted when the glossary edge is written.
- Tall's three worlds is a builder-facing lens: learner content never names it. `toaster-recipe` still requires a named per-notebook "Tall seam" cell, which contradicts this rule; the recipe rewrite is a later pass.
- SA-2 (full stage model per chapter): Z ruled that the assembled model, made legible through diagrams, satisfies it (recorded for read-back at M2).
- SA-3 (energy model Q = eta P t) and SA-8 (one construct per notebook) will collide with the content pass; SA-7 stays.
- What comes next: see `decisions/next-passes.md` (to be written at M3).

## DL-014 | 2026-09-25 | Ch2+Ch3 | User-test checkpoint: A10 reframe + verification def

Path: Handled by ACE — four A9 agents (L19 Novice, L20 SE Practitioner, L21 Returning Learner, L22 Systems Architect) + one ACE self-test. Two fixes applied inline; three open questions logged.

Decision: Two blocking/NEEDS-FIX issues resolved; CHECKPOINT PASS for Ch2-03 and Ch3-04 after fixes. Three open questions escalated to Z.

**Fixes applied (ACE inline):**
1. **ch03/nb03 missing import** — `from toaster.evidence import ReviewRecord, validate_record, hash_content` was absent from the model-load cell; cell-05 raised NameError at runtime. Added import to cell-02. Fix verified: `validate_record()` returns `[]`. (L20 NEEDS-FIX, confirmed blocking.)
2. **ch02/nb01 API-comment explanation** — cell-01 context now ends with: "Each code cell contains a commented-out `editor.add_*()` call showing the future Editor API equivalent; these are informational — run the cell as written." Addresses L19 NEEDS-FIX: novice saw the comment and didn't know whether to act on it.

**Passing verdicts:**
- L21 Returning Learner Ch1+Ch4: PASS — physical-layer label in ch01 present, verb-noun scope note in ch04 present, WHAT-not-HOW in nb01 cell-01 correct.
- L22 Systems Architect Ch2+Ch3: PASS — six execution cells green, three-part anatomy correctly stated and demonstrated, def/usage distinction present in ch03-nb04, gap note cites both toaster#19 and OpenSysML#608.

**Open questions for Z (do not fix without direction):**

OQ-1 — **req def/usage template distinction absent from ch02-nb01 for novice readers.** L19: cell-03 says "TimelyToast is a requirement definition" without clarifying that "definition" means a reusable template (classifier), not just "a defined requirement." The def/usage distinction is not explained until Ch3-nb01 where `timely : TimelyToast` appears. Question: add a one-sentence forward-reference in cell-03? ("A requirement _definition_ is a template — Chapter 3 shows how to apply it to a named design candidate.") Or keep the scoped-reveal pattern as-is?

OQ-2 — **Logical architecture layer unnamed in ch01/ch04 index.md.** L21: ch01 correctly labels the structural model as "physical architecture layer" (forward ref from the A10 framing). But the logical layer (abstract part def specializations + interface contracts) is never named by name in either index. The tutorial implies functional→physical but the middle layer appears unnamed. Question: add one sentence to ch01/index.md and ch04/index.md naming the logical layer explicitly and saying Ch5 is where it gets its interfaces? Or is the silence correct because logical architecture is Ch5's business?

OQ-3 — **"Inspired by" hedge on the three-part anatomy.** L22 (Systems Architect): cell-01 of ch02-nb01 says "(inspired by Brian Douglas, Part 4)" around the three-part anatomy. An architect reads this as a hedge around what Part 4 presents as a firm convention. The "inspired by" framing was Z's explicit directive (to relieve perfect-match pressure with the video), but L22 flags it. No change proposed — logging for awareness.

## DL-013 | 2026-09-25 | Phase 4 | User-test checkpoint: Phase 4 construction zones pass

Path: Handled by ACE — three A9 reports + ACE self-test; zero blocking issues; checkpoint passed

Decision: CHECKPOINT PASS for Phase 4 (all 13 construction zones). Content proceeds to next WP.

Rationale: Three A9 simulated learner agents (Novice/Ch1, SE Practitioner/Ch3-Ch4, Returning Learner/Ch5+Ch7) and one ACE self-test (Ch3/nb02) returned zero blocking issues across all tested notebooks. All model-loading assertions pass, all negative controls return bad.ok=False with legible diagnostics, and all structural template slots (cell-0 concept statement, Tall seam, cell-6 exercise pointer, conclusion.md three paragraphs) are populated correctly.

Seven minor findings logged (do not fix without Z's direction):
1. Ch1/nb01: "specializations" used before the term is defined (arrives in nb03) — Novice forward-reference friction
2. Ch1/nb02: `:>>` operator mentioned without definition or cross-reference — Novice forward-reference friction
3. Ch1/nb02: "ownership relationship" without a plain-English anchor phrase — minor clarity gap
4. Ch3/nb01 context cell: mentions `calc def DeliveredEnergy` before nb02 introduces it — SE Practitioner forward-reference in narration
5. Ch4/nb01 context cell: forward-references nb02 constructs and Chapter 5 before learner has reached either — minor cognitive load
6. Ch3/nb02 narration: cites D-003 without a pointer to DEFERRED.md — minor documentation gap
7. Ch7/nb02 cell-0: contains an H2 header before the concept sentence, violating one-sentence cell-0 template — structural deviation; understanding not prevented

## DL-012 | 2026-09-25 | Cross-WP | Phase 2 pilot: all 13 notebooks use Pattern B; multi-fragment convention adopted

Path: Handled by ACE — implementing Z's explicit design directives; architecture revision logged

Decision: All 13 construct-introducing notebooks use Pattern B (SysML string fragments) for
their construction zones. Pattern A (Editor API) is fully deferred. The multi-fragment convention
is adopted: one named fragment variable per element = one future `editor.add_*()` call. Each
fragment is in its own code cell, printed immediately, with a narration markdown cell after it.
`TOASTER_INCREMENT` is assembled from the fragment variables at the end of the construction zone
and equals new declarations for that notebook only (not the full cumulative model).

Rationale: Phase 2 pilot (Ch3/nb02) probed `add_calc_def` with `inputs` kwarg → TypeError.
Further probing confirmed: `add_attribute` produces fixed binding (not `default =`), and
`add_action_def` / `add_member(kind='action def')` produce bare declarations only. Together
with D-004–D-010 (already confirmed), the API cannot produce any of the 13 notebook constructs
in their correct form. Z's directions (verbatim):

1. "we can do this but then we need to make sure all the gaps are well documented as issues.
   each location we encounter this issue needs its own comment markdown, linking to issue in this
   repo, linking to issue in opensysml and these much carry exact citation to the spec so its
   clear we're only asking for the spec to be implemented not extraneous feature requests."
2. "be careful to avoid mega strings. don't do the whole increment in one call or even one cell.
   you need to do increments do them in smaller chunks. always needs to be inspectable & intuitive."
3. "code should be factored the same way it would be if we had the api calls we wanted."

New gaps confirmed and filed (Phase 2 pilot 2026-09-25):

- D-011: `attribute default =` modifier — toaster#16 / OpenSysML#603 (KerML §8.4.1)
- D-012: `calc def` body (inputs + return expression) — toaster#17 / OpenSysML#604 (SysML v2 §7.16)
- D-013: `action def` body (params, sequencing, nested actions) — toaster#18 / OpenSysML#605 (SysML v2 §7.15, §7.20)

All 5 upstream OpenSysML issues filed: OpenSysML#601 (flow/D-009), #602 (state/D-010), #603 (attr
default/D-011), #604 (calc def body/D-012), #605 (action def body/D-013). DEFERRED.md updated.
All 4 skills updated with confirmed issue numbers and multi-fragment convention. Plan updated.

## DL-011 | 2026-09-25 | Cross-WP | Declarative construction architecture: notebooks ARE the build

Path: Handled by ACE

Decision: Adopt declarative construction architecture. Cell-02 in each of 13 construct-introducing notebooks declares the SysML increment (via Editor API or SysML string); the cumulative `.sysml` files become generated checkpoints. The `scripts/check_construction.py --check` script verifies consistency. Full plan in `decisions/declarative-construction-plan.md`.

Rationale: Z's verbatim direction — "ideally someone who pulls this repo constructs the sysml v2 model, they are not pulling an existing one. we're teaching engineering here." The hybrid architecture (Pattern A = Editor API for ~8 construct kinds; Pattern B = SysML string for 5 gap constructs pending OpenSysML#595–599) is the only viable path given current implementation gaps. The scope is 13 notebooks, not all 31.

Key findings from ACE review of the plan (B-ACE-3 critical):
- `editor.apply()` returns the FULL model (all existing + new members), not just the new member.
  Probed: base = `package P { part def X; }`, after `add_part_def('Y')` → `"package P { part def X; \n    part def Y;\n}"`.
  This invalidated the "reconstruct from TOASTER_INCREMENT concatenation" design for the verification script.
  Fix: `check_construction.py` verifies consistency only (run construction cells, check they parse, compare
  last Pattern A TOASTER_INCREMENT per chapter to committed fixture). Does NOT reconstruct from scratch.
- Pattern A TOASTER_INCREMENT = full cumulative model. Pattern B TOASTER_INCREMENT = new SysML fragment only.
  The two patterns are not interchangeable. The verification script must handle both separately.
- Ch1 has no ch00-cumulative; Pattern A cells within Ch1 chain on the prior notebook's TOASTER_INCREMENT.

ACE review findings table: 4 blocking + 5 minor, all corrected in `decisions/declarative-construction-plan.md`.
Gap construct notes already added to 5 affected notebooks; upstream issues filed (OpenSysML#595–599);
DEFERRED.md entries D-004–D-008 present with cross-references.

## DL-010 | 2026-09-25 | Cross-WP | ISQ/SI unit typing + B+ hybrid-systems interface contract

Path: Handled by ACE

Decision: (1) All 8 model files updated to use `ISQ::PowerValue`, `ISQ::DurationValue`, and `ISQ::EnergyValue` (Option A — ISQ for all physical attributes from ch01). `resistance` and `gauge` in ch06 stay `Real` (structural placeholders, not simulation quantities). (2) Ch7/nb01 updated with `BINDING` dict (B+ option): explicit sympy↔SysML attribute mapping driving `lambdify` argument order, with narration framing the dict as the data dictionary for the continuous dynamics.

Rationale: Z identified the toaster as a hybrid system (discrete state machine + continuous dynamics) and directed an explicit interface contract between SysML continuous-valued fields and their sympy symbol definitions. Z chose Option A (ISQ everywhere) over Option B (calc def only) and Option C (defer), framing the unit-typing decision itself as substantive engineering judgment. Z's framing: the BINDING dict is "essentially a data dictionary that also determines the basis for how the SysML model tells an engineer to interpret data generated by simulations."

Probe findings (2026-09-25):
- `attribute x : ISQ::DurationValue default = 120.0 [SI::s]` parses + allows override: ok=True
- `= VALUE [SI::UNIT]` without `default` creates a fixed binding (cannot override): avoided
- Mixed ISQ+Real in `calc def` (efficiency stays Real): ok=True
- `model.eval()` with ISQ-typed params requires unit-annotated literals (`[SI::W]`, `[SI::s]`)
- Return type is `opensysml.values.Quantity`; `.magnitude` extracts numeric value; `float()` fails
- `model.eval("ToasterDemo::DeliveredEnergy(800.0 [SI::W], 120.0 [SI::s], 0.7)").magnitude = 67200.0`
- IDE language server reports conformance errors on ISQ literals; opensysml v0.9.0 runtime accepts them

Files changed:
- `models/ch01-ch08-cumulative.sysml` (all 8): ISQ imports + typed attributes + unit-annotated values
- `chapters/ch07-execution/01-calc-energy.ipynb`: BINDING dict + narration + updated model.eval call
- `.claude/skills/sysml-v2-toaster-model/SKILL.md`: ISQ unit typing section added

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

## DL-005 | 2026-09-25 | Ch2-Ch3 | Requirement anatomy + verification def

Path: Handled by ACE (Z directed during context compaction)
Decision: Add (1) `doc` rationale to `TimelyToast` in Ch2; (2) new Ch3-nb04 notebook introducing `verification def TimelyToastTest` (§7.24); log `VerificationMethodKind` metadata gap as D-004 / toaster#19 / OpenSysML#608; add A10 Systems Architect archetype to AGENTS.md.
Rationale: Brian Douglas Part 4 specifies the 3-part requirement anatomy (description, rationale, verification method). The `doc` comment (§7.21.2) carries informal text in the requirement def; `verification def` (§7.24) is the spec construct for verification cases. `verify` must target a requirement *usage* (not a definition) — confirmed by probe (`ok=False`, error: "satisfy target must be a requirement usage, found requirementDef") — so the verification def is placed in Ch3 where `timely : TimelyToast` is already defined, not Ch2. The `VerificationMethodKind` metadata construct is a gap in OpenSysML v0.9.0.
