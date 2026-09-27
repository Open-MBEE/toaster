Model: claude-opus-5-5[1m] (role pin claude-opus-5-5, effort high)

# Chapter 4 layer audit

Contract PASS2-008-C, 2026-09-26. Role: `.claude/agents/layer-auditor.md`.
Branch `audit/ch04`, base commit `927f04f`.

Subject: the elements Chapter 4 adds, that is the difference between `models/ch03-cumulative.sysml` (58 lines) and `models/ch04-cumulative.sysml` (52 lines), both generated fixtures, not edited.
Method: the four-question pass and the per-layer checklist in `.claude/skills/architecture-layers/SKILL.md`, AGENTS.md §1.5, §1.6 and §1.8, the ACE rulings DL-017 to DL-023, and the glossary (`uv run python -m glossary tutorial TERM` for `function`, `functional-architecture`, `mechanism`, `mop`, `moe`, `behavior`, `policy`, `logical-component`, `decomposition`, `asserted-inference`, `interface`, `control-law`).

Model evidence. Both fixtures were loaded with OpenSysML v0.9.0 (`load_from_content`, `strict=False`): `model.ok == True` for both, no diagnostics for Chapter 4. Their API JSON exports were compared by (`@type`, `qualifiedName`) counts (213 elements for Chapter 3, 270 for Chapter 4). What the export confirms:
- Added, named: `ActionDefinition ApplyHeat`; four `ReferenceUsage` parameters `power`, `duration`, `efficiency` (direction `in`) and `energy` (direction `out`), each with one `FeatureTyping`; `ActionUsage calculate` owning one `AssignmentActionUsage` whose value is an `InvocationExpression` of `ToasterDemo::DeliveredEnergy` with three `FeatureReferenceExpression` arguments referring to `ApplyHeat::power`, `::duration` and `::efficiency`; two `SuccessionAsUsage` (`@6`, `@8`); two `Membership`s (`@4`, `@7`) to library features (the `start` and `done` nodes); three `ItemDefinition`s `Start`, `Finish`, `Cancel`.
- `Start`, `Finish` and `Cancel` are referenced by no element in the Chapter 4 export (no typing, subsetting, flow or succession targets them).
- Removed relative to Chapter 3: `Documentation TimelyToast::@0` and `VerificationCaseDefinition TimelyToastTest` with its `doc`, subject and objective (see F-5). The `ConstraintUsage` renumbering `TimelyToast::@2` to `@1` is a consequence of the removed `doc`; the constraint text is identical.
- Succession ends: in the export, the target end of `@6` reference-subsets `calculate` and the target end of `@8` reference-subsets `@7` (`done`); the source end of neither carries a `ReferenceSubsetting`. I did not establish whether that is how v0.9.0 records a `first`/`then` source or a gap, so the start-calculate-done order is read from the text, not confirmed from the export.

Evidence read for intent: `chapters/ch04-functional-decomp/index.md`, `conclusion.md`, all cells of notebooks `01` to `03`; AGENTS.md Part 2 §1 (Douglas Part 3 story, legacy section, used only as story evidence). "cell-N" below is the 0-based position of a cell in its notebook, not the cell's `id` field. `models/ch05-cumulative.sysml` and `ch08-cumulative.sysml` were read only for how Chapter 4 elements are used downstream, not audited. `scripts/check_construction.py --check --chapter=4` was run (read-only by its docstring): "All 1 chapter(s) consistent." Notebook 03 was executed to a scratch directory outside the worktree (see F-6). `uv run python -m glossary lint --json` reports 0 hits for Chapter 4, confirming the contract's "lint hits: none".

Status legend as in the Chapter 1 audit: a **finding** is something the model or chapter says that the layer rules say it must not, or a checklist "no"; "not yet built" marks a checklist item that is expected to be absent at this chapter.

## Classification table

| Element (qualified name) | Layer | Reason | Status |
|---|---|---|---|
| `ToasterDemo::ApplyHeat` (`action def`) | Mixed: functional signature and name; body carries a mechanism-shaped relation with a performance parameter | Q1 (substitution test, §1.5) holds for "apply heat: energy in, energy delivered out"; a verb-noun function (`def-douglas--function`, `term-functional-architecture`). But its only content beyond the signature is an equality `energy := DeliveredEnergy(power, duration, efficiency)` that takes the conversion efficiency as a given input: a "prescribed, comparatively deterministic input-to-output relation" (`term-mechanism`) parameterized by the glossary's example MoP, power efficiency (`term-mop`). §1.5 states the functional phenomena relation as a balance inequality "without assuming perfect efficiency". | FINDING F-1, F-2, F-4; OPEN-QUESTION OQ-1 |
| `ToasterDemo::ApplyHeat::power` (`in`, `ISQ::PowerValue`) | Functional | Q1: a pop-up toaster (mains power) and tongs with a blowtorch (fuel power) both take in a rate of energy; an energy input flow (`def-douglas--function`: inputs are material, energy or signals). Typed and unit-bearing, no value. | PASS |
| `ToasterDemo::ApplyHeat::duration` (`in`, `ISQ::DurationValue`) | Functional slot by Q1, kind undecided | Q1 holds ("apply heat for a given time" fits both). It is not material or energy; it could be a signal from a control function, a timer setpoint (`term-policy`, DL-022: a setpoint is a policy parameter on the control component) or the heating time, which DL-018 says is a result. Typed, no value. | OPEN-QUESTION OQ-2 |
| `ToasterDemo::ApplyHeat::efficiency` (`in`, `DimensionOneValue`) | Logical by the glossary (a MoP of a conversion); Q1 alone does not exclude it | Not a flow of material, energy or signal (`def-douglas--function`); SEBoK's function is a transformation of flows "with defined performance" (`def-sebok--function`), and efficiency is that performance. `term-mop` names power efficiency as the toaster MoP, "typically logical". Entered as an input, it makes the function's output depend on a characteristic of whatever mechanism is chosen. Unbounded type (no 0 to 1 constraint). | FINDING F-1; OPEN-QUESTION OQ-1 |
| `ToasterDemo::ApplyHeat::energy` (`out`, `ISQ::EnergyValue`) | Functional | Q1: an energy output delivered by any heat source. Typed, no value. Its recipient (the bread) is not modeled, and it is the only output (no loss output). | PASS as an element; flow accounting fails (F-2) |
| `ToasterDemo::ApplyHeat::@4` (`first start`, membership to the library `start` node) | Functional (control flow) | The sequencing of a functional behavior (FFBD ordering, index.md); commits to no mechanism. | PASS |
| `ToasterDemo::ApplyHeat::@7` (membership to the library `done` node) | Functional (control flow) | As above. | PASS |
| `ToasterDemo::ApplyHeat::@6` (`SuccessionAsUsage`, start then `calculate`) | Functional (control flow) | Ordering only. Source end not resolved in the export (see Model evidence). | PASS (source end not confirmed) |
| `ToasterDemo::ApplyHeat::@8` (`SuccessionAsUsage`, `calculate` then done) | Functional (control flow) | As above. | PASS (source end not confirmed) |
| `ToasterDemo::ApplyHeat::calculate` (`ActionUsage`) | Follows the relation it evaluates (OQ-1); not a sub-function | It has no flows of its own and no verb-noun name; its only content is an assignment that evaluates a `calc def`. It is the executable-specification body of `ApplyHeat` (§1.1 item 3), not a finer function (Douglas "decomposing functions into finer functions", skill story anchors 4:02; `def-sebok--decomposition`). | FINDING F-4; layer via OQ-1 |
| `ToasterDemo::ApplyHeat::calculate::@0` (`AssignmentActionUsage` `energy := DeliveredEnergy(power, duration, efficiency)`, with its `InvocationExpression` and three argument references) | Undecided: phenomenon (functional) or characterized conversion (logical) | The equality E = P t η. Holds for any constant-power heat source if η is defined as delivered over supplied energy (functional reading), but it assumes a known efficiency and states no loss (logical reading; `term-mechanism`, `term-mop`, §1.5 constraints split by solution-independence). Its layer is also the layer of `DeliveredEnergy`, a Chapter 3 element (cross-chapter dependency). | OPEN-QUESTION OQ-1; FINDING F-2 |
| `ToasterDemo::Start` (`item def`) | Functional (flow type), denotation undecided | Q1: bread entering (nb02 cell-05) is a material input of any toasting solution. The name denotes an event, not bread. Used by no action in Chapter 4. | FINDING F-3; OPEN-QUESTION OQ-3 |
| `ToasterDemo::Finish` (`item def`) | Functional (flow type), denotation undecided | As `Start`, for toast exiting. | FINDING F-3; OPEN-QUESTION OQ-3 |
| `ToasterDemo::Cancel` (`item def`) | Functional (signal flow type) | Q1: a request to stop heating fits both solutions (a lever, or the user turning off the torch); a signal input (`def-douglas--function`). Conceptual-to-functional test (§1.5): a stop-on-demand need is plausible but not traced to a stakeholder statement in the chapter. Used by no action in Chapter 4. | FINDING F-3 |
| Unnamed supporting elements (`FeatureMembership`, `ParameterMembership`, `ReturnParameterMembership`, `EndFeatureMembership`, `FeatureValue`, `FeatureTyping`, `ReferenceSubsetting`, `Feature`) | Classified with their owners | Structural plumbing of the elements above; no content of their own. | PASS (not separately classified) |
| Removed: `TimelyToast` `doc`; `TimelyToastTest` (`verification def`) | Not classified (Chapter 3 elements) | Present in Chapter 3, absent from the Chapter 4 cumulative fixture. `TimelyToastTest` would not be a layer element anyway (DL-023). | FINDING F-5 |
| Python side: `AI-C04` (`asserted_inference` ReviewRecord, nb03 cell-05) | Not a layer element (argument about the model) | A judgment record is analysis and argument, not a prescription or intent (by analogy with DL-023; `term-asserted-inference`). Checked against the cross-layer judgment item: counterevidence and residual uncertainties are filled; disposition `pending`, not "accepted" (SA-7). | PASS on the judgment fields; FINDING F-2 (criterion) and F-6 (does not execute) |

## Per-layer checklist results

**Functional**
- Each action states typed inputs and outputs: `ApplyHeat` does; all four parameters are ISQ or dimension-one typed. PASS. `calculate` states none (F-4).
- All flows accounted for at this level: no. Supplied energy (power times duration) and delivered energy differ by (1 - efficiency) times supplied energy, which leaves as no output; the bread that receives the energy is not an input or output; `Start`, `Finish` and `Cancel` are consumed or produced by no action (F-2, F-3).
- Solution-independent (substitution test): the signature and name pass; the efficiency input and the equality body are contested (F-1, OQ-1).
- Phenomena relations stated as relations (balance inequality), not as a specific part's behavior: no inequality is stated. The relation is an equality with an efficiency parameter. It names no specific part (ApplyHeat is unallocated in Chapter 4), so it is not a part's behavior, but it is not the balance form §1.5 prescribes (F-2, OQ-1).
- At least one MoE about acceptance: none added by Chapter 4. `ApplyHeat` carries no measure; the one measure-like term it carries (efficiency) is the glossary's MoP example. Not yet built for this chapter.
- Reads as an objective: partly. "Deliver energy" says what is good, not what is good enough; there is no threshold or acceptance measure on the function.

**Logical**
- Chapter 4 adds no logical components, ports or interfaces. Port-type conformance (§1.9, `opensysml-query` recipe 5) remains **open**, not passed: no connection is declared.
- No solution values and no results entered as choices: Chapter 4 adds no attribute values at all. PASS. Whether `efficiency` and `duration` smuggle a logical commitment into a functional action is F-1, OQ-1 and OQ-2.
- MoP thresholds derived from a MoE: none added. Not yet built.

**Physical**
- Chapter 4 adds no physical elements. Not applicable.

**Across layers**
- Stopping rule (§1.8): `ApplyHeat` is a leaf that is not concrete, not interfaced and not verified. Expected at Chapter 4; not yet built. (Downstream, `ch05` line 53 allocates it to `HeatingSystem`.)
- An emergent result set as an attribute default and then "verified": Chapter 4 adds none. PASS. OQ-2 notes that `duration` must not become the quantity checked as time to toast (DL-018).
- Judgment recorded with counterevidence and residual uncertainties, no "accepted" disposition: `AI-C04` satisfies the field checks (disposition `pending`, `engineering_conclusion` `undetermined`). Its criterion is weaker than §1.8 completeness (F-2), and it does not execute (F-6).
- Figures show the assembled model: Chapter 4 has no figure. No notebook renders or mentions a diagram, and the notebooks carry no image outputs, although notebook 01 is named `01-action-def-ffbd`. AGENTS.md §1.7 says every chapter shows the assembled model (F-7).

## Findings

**F-1. `ApplyHeat` mixes a performance characteristic of the heating mechanism into the flows of a functional action (the contract's flagged check).**
Check: functional checklist items 1 to 3; AGENTS.md §1.5 functional row ("typed flows and the relations among phenomena (an energy balance inequality, which respects conservation without assuming perfect efficiency)") and the constraint split; `term-function`, `term-mop`, `term-mechanism`.
Evidence:
- `in efficiency : DimensionOneValue;` (fixture line 42) is declared as an input alongside `power` and `duration`. It is not a material, energy or signal flow (`def-douglas--function`); in SEBoK's terms it is the "defined performance" of the transformation (`def-sebok--function`), not one of its input flows.
- The glossary's tutorial MoP definition gives "for the toaster, power efficiency" as its example and says "Typically logical" (`def-tutorial--mop`); the architecture-layers example table files "Heating efficiency is at least 0.6" as a logical MoP threshold.
- The body `assign energy := DeliveredEnergy(power, duration, efficiency)` (line 46) makes the output a deterministic function of the inputs, the shape of `term-mechanism` ("a prescribed, comparatively deterministic input-to-output relation").
- The chapter says the opposite: nb01 cell-01 "each described as *what* it does rather than how it does it"; `conclusion.md` "without committing to how the hardware achieves it". nb01 cell-05 gives the reason the parameters exist: "Three `in` parameters mirror the `DeliveredEnergy` inputs", so the signature was derived from the Chapter 3 calculation, not from the flows of the function.
- What is not contested: `efficiency` is not a flow, and a functional action whose output requires a known efficiency as an input assumes a conversion characteristic that §1.5 says the functional relation must not assume. What is contested (whether the equality itself is a phenomenon or a mechanism) is OQ-1.
Not done: I did not change the model, the notebooks or the chapter text, and did not propose a replacement signature.

**F-2. Inputs and outputs are not accounted for at the one level Chapter 4 models, and the completeness record checks a weaker criterion.**
Check: functional checklist ("are all flows accounted for at this level?"); AGENTS.md §1.8 ("at every level, account for every input and output"); Douglas Part 3 as recorded in AGENTS.md Part 2 §1 ("Any unaccounted flow is a gap"; entry model bread, `toast bread`, toast).
Evidence:
- Energy: supplied energy is `power * duration`; the only output is `energy = power * duration * efficiency`. The remainder, `(1 - efficiency) * power * duration`, is neither an output nor a stated loss. The skill's functional example is "bread and energy in, toast and lost energy out; energy to the bread plus loss cannot exceed energy supplied".
- Conservation is not enforced: `efficiency` is `DimensionOneValue` with no bound, so the model admits delivered energy greater than supplied energy. No constraint in Chapter 4 or Chapter 3 bounds it.
- Material: `ApplyHeat` does not take bread in or give anything to bread. "Apply thermal energy" in Douglas's first decomposition acts on the bread between "load/position bread" and "remove toast".
- `AI-C04` (nb03 cell-05) claims "The ApplyHeat action decomposition is functionally complete" on the criterion "Every in parameter feeds at least one sub-action; the out parameter is assigned before done". That checks parameter use, not flow accounting. Its own `counterevidence` says "The model does not capture heat loss or warm-up transients — those flows are absent from this decomposition", which is an unaccounted flow by §1.8. `conclusion.md` repeats the weaker criterion ("every input reaches at least one sub-action, and the output is assigned").
Not done: no edit to the record, the model or the conclusion.

**F-3. `Start`, `Finish` and `Cancel` are declared as flow types but are no action's input or output, and their names do not say what they denote.**
Check: functional checklist items 1 and 2; §1.8 accounting.
Evidence: the export shows nothing references the three item defs. nb02 cell-01 says `item def` "names the typed flows: the bread entering, the toast exiting, and the signal that cancels the cycle"; nb02 cell-05 says "`Start` and `Finish` mark the bread entering and toast exiting"; nb02 cell-06 and nb03 cell-03 say they "declare typed items for structural use; they appear as part types in `BreadHandling` in Chapter 5, not as references inside `ApplyHeat` itself". The names are events (start, finish), the text says material (bread, toast). Downstream, `ch05` line 54 declares `part def BreadLoader { part bread : Start; }` (a part usage typed by an item def) and `ch08` lines 84 to 86 use the same defs as accepted triggers (`accept Start`, `accept Finish`, `accept Cancel`), so the same definition serves as material and as a signal. The downstream use is observed, not audited. Denotation is OQ-3.
Not done: no rename, no flow added.

**F-4. Chapter 4 does not decompose a function into finer functions.**
Check: the contract premise and the functional layer's idiom (§1.5: "`action def` with typed in and out flows"); `def-sebok--decomposition` ("decompose a function until implementable system elements can be identified"); `def-douglas--decomposition`.
Evidence: there is no parent function. `ApplyHeat` is owned by the package and composed into no action; the whole's purpose "Transform bread into toast acceptable to its user" is still a `doc` on `ToastingSystem`, whereas DL-019's re-derivation guidance puts it in "a functional construct (an action def with typed flows, or a behavioral requirement def) that the whole performs". The only child of `ApplyHeat` is `calculate`, which is not a verb-noun function and has no flows of its own; it evaluates a calculation. `index.md` acknowledges that Douglas's architecture has about 15 verb-noun functions and that Chapter 4 models one as a worked example; that is a stated scope choice, so the defect recorded here is narrower: what Chapter 4 calls "the functional decomposition of the heating operation" (nb01 cell-07, nb02 cell-06, nb03 cell-03) is one function plus the executable evaluation of a relation, not a decomposition.
Not done: no parent function or sub-functions proposed.

**F-5. The Chapter 4 cumulative fixture drops two Chapter 3 elements, so it is not cumulative.**
Check: not a layer check; contract premise (the diff is "what Chapter 4 adds") and `index.md` ("The Ch4 cumulative model contains everything from Ch1-3, plus ...").
Evidence: the diff removes the `doc` rationale of `TimelyToast` and the whole `verification def TimelyToastTest` (Chapter 3 fixture lines 25 to 30 and 35 to 48). Commit `c237300` ("feat(ch2-ch3): add requirement rationale and verification case") changed only the Chapter 2 and 3 fixtures, and the Chapter 5 fixture also lacks the `doc` (first 30 lines read). `scripts/check_construction.py --check --chapter=4` passes because it checks that fixtures load and increments parse, not that each fixture contains its predecessor. This bears on the requirement anatomy (description, rationale, method) taught in Chapters 2 and 3, which is lost from Chapter 4 onward.
Not done: I did not regenerate or edit any fixture, and did not audit Chapters 5 to 8 for the same loss.

**F-6. Notebook 03 fails at the cell that builds `AI-C04` (not a layer defect; reported because the chapter's completeness claim rests on it).**
Evidence: nb03 cell-02 imports only `Path`, `opensysml` and `format_diagnostics`; cell-05 calls `ReviewRecord`, `hash_content` and `validate_record`. Executed with `jupyter nbconvert --execute` (output written outside the worktree): `NameError: name 'ReviewRecord' is not defined`. DL-014 fix 1 records the same missing import in Chapter 3 notebook 03. `check_construction.py` does not execute this cell.
Not done: no import added.

**F-7. Chapter 4 shows no view of the model it builds.**
Check: cross-layer checklist, last item; AGENTS.md §1.7 ("every chapter shows the assembled model so that explicit and implicit parts are distinguishable without reading the Python").
Evidence: no cell in notebooks 01 to 03 renders a diagram, and the notebooks have no image outputs; notebook 01 is named `01-action-def-ffbd` but draws no FFBD.
Not done: no figure made.

Documentation consistency (reported only, as in the Chapter 1 audit's F-4): `index.md` "Expected result" gives `in power : Real; in duration : Real; in efficiency : Real; out energy : Real`, while the fixture and nb01 cell-04 use `ISQ::PowerValue`, `ISQ::DurationValue`, `DimensionOneValue` and `ISQ::EnergyValue`. `index.md` and `conclusion.md` describe the exercise as an `EjectToast` action; nb01 cell-12 describes a `Brew` action for a coffee maker (nb03 cell-07 a `BrewUnit` action). The exercise itself was not read.

## Open questions (for the orchestrator to route)

**OQ-1. Is `ApplyHeat`'s relation `energy = power * duration * efficiency` a phenomena relation (functional) or a characterized conversion carrying a MoP (logical)? (mechanism versus phenomenon)**
- Functional reading: the relation holds for any heat source of constant power, electric or fuel, if efficiency is defined as delivered over supplied energy; a pop-up toaster and tongs with a blowtorch both satisfy it, and the method stops at Q1. No component is chosen in Chapter 4 (`ApplyHeat` is unallocated until `ch05`), and DL-017 makes a law logical when it is "applied to a chosen component".
- Logical reading: the relation takes a known efficiency as an input and states no loss, so it is not the §1.5 balance inequality "without assuming perfect efficiency"; its shape is the glossary's mechanism (`term-mechanism`); its parameter is the glossary's MoP example, "typically logical" (`term-mop`); the architecture-layers table files efficiency thresholds as logical MoPs. A functional statement that needs an efficiency value only makes sense once a conversion has been characterized.
- Cross-chapter dependency: the same question applies to `calc def DeliveredEnergy` (Chapter 3). The Chapter 3 audit and this one should agree, so the ruling belongs to whichever is routed first.
- Recommended default: classify the `ApplyHeat` signature (energy in, energy delivered out) as functional, and the efficiency-parameterized equality as a logical commitment (a characterized conversion whose efficiency is a MoP) placed in a functional action. F-1 and F-2 stand under either reading.

**OQ-2. What is `ApplyHeat::duration`: a signal flow, a policy setpoint, or a result?**
- Signal flow (functional): Q1 holds; a control function telling the heater how long to heat is a behavioral dependency (§1.5 connectivity), and any solution has one (a timer or a user).
- Policy setpoint (logical): a chosen heating time is an open-loop timer, a policy parameter (`term-policy`); DL-022 puts a setpoint on the control component, named as a setpoint. A closed-loop solution that stops on browning has no such input, so the parameter commits to a policy.
- Result (emergent): the time to acceptable toast follows from power, bread and control (DL-018, `term-behavior`); if this parameter is identified with it, entering it as an input repeats the Chapter 1 F-1 pattern.
- Evidence in the chapter: nb01 cell-05 says the parameters "mirror the `DeliveredEnergy` inputs"; nothing links `duration` to `Toaster::cycleTime` or to `ControlSystem`.
- Recommended default: a functional input slot (typed, no value) whose source function is not yet modeled, with the constraint that it is never the quantity a requirement checks as time to toast (DL-018, DL-022).

**OQ-3. What do `Start` and `Finish` denote: material (bread in, toast out), events (cycle start and finish), or both?**
- Material: nb02 cell-01 and cell-05 say so; `ch05` types `part bread : Start` and `part bread : Finish`.
- Events or signals: the names are events; `ch08` uses them as accepted triggers of a state machine; nb02 groups them with `Cancel`, which the text calls a signal.
- Both: the fixtures use one definition in both roles, which a flow-accounting check (F-2, F-3) cannot audit until one denotation is chosen.
- Recommended default: classify all three as functional flow types (Q1 holds under any denotation) and record the denotation as undecided for the re-derivation. This is also a cross-chapter dependency for the Chapter 5 and Chapter 8 audits.

## Contract premises that did not hold

1. **"Chapter 4 is the functional decomposition with verb-noun functions and typed flows."** Partly. There is one verb-noun function (`ApplyHeat`) with typed attribute parameters and three typed item defs. There is no parent function and no finer function (F-4): the only sub-action, `calculate`, evaluates a calculation and has no flows. The item defs are typed but unattached (F-3). One parameter, `efficiency`, is not a flow (F-1).
2. **"Every input and output is accounted for at each level."** Does not hold. Lost energy, bread and toast are unaccounted, and the three item defs are no action's input or output (F-2, F-3). `AI-C04` asserts completeness on a parameter-use criterion, and its own counterevidence names the missing flows.
3. **"No mechanism appears in a functional action."** Does not hold on the uncontested part and is contested on the rest. A performance characteristic of the conversion (`efficiency`, the glossary's MoP example) is an input of the functional action (F-1). Whether the equality it feeds is itself a mechanism is OQ-1.
4. **Implicit premise: the Chapter 3 to Chapter 4 diff is only what Chapter 4 adds.** Does not hold: the diff also removes the `TimelyToast` rationale and `TimelyToastTest` (F-5). They are reported, not classified as additions.
5. **"Lint hits for this chapter: none."** Holds (`glossary lint --json`, 0 hits under `chapters/ch04-functional-decomp`).

## Constructs that could not be classified cleanly

- `ApplyHeat` as a whole: signature functional, body undecided (OQ-1). Reported as mixed, not given a single layer.
- `ApplyHeat::calculate` and its assignment: their layer is the layer of the relation they evaluate, which is OQ-1, and depends on the Chapter 3 `DeliveredEnergy`.
- `ApplyHeat::duration`: functional by Q1, but three readings of what it is (OQ-2).
- `Start` and `Finish`: layer clear (functional flow types), denotation not (OQ-3).
- `AI-C04`: a Python judgment record, not a model element; classified as not a layer element by analogy with DL-023, which rules on verification cases, not judgment records. The analogy is mine, not a ruling.

## Not checked, and why

- **Succession source ends:** the export does not show a `ReferenceSubsetting` on the source end of `@6` or `@8`. I did not probe whether this is v0.9.0's normal representation of `first start; then ...` or a gap, so the ordering is taken from the text.
- **Library targets of `@4` and `@7`:** the member elements are library ids not present in the export by qualified name; I took them to be `start` and `done` from the text.
- **Notebooks 01 and 02 end to end:** not executed; their increments pass `check_construction.py`. Notebook 03 was executed (F-6).
- **Exercise `exercises/ch04/exercise.ipynb`:** not in scope.
- **Chapters 3, 5 and 8:** read only for dependencies. The loss in F-5 was checked only for the Chapter 5 fixture's first 30 lines, not for Chapters 6 to 8.
- **Douglas Part 3 content** is taken from AGENTS.md Part 2 §1 (legacy) and the skill's anchors; timestamps not re-verified and the video not re-watched.
- **Glossary sources:** `uv run python -m glossary check` passes (0 errors, 7 warnings); the warnings say the source PDFs are not in `glossary/sources/local/`, so I relied on the recorded definitions, not the source texts.
- **Tall seam labels** (A-F, O-S) in nb01 cell-11, nb02 cell-10 and nb03 cell-06: out of scope; parked for Pass 4 by DL-028.

Model: claude-opus-5-5[1m]
