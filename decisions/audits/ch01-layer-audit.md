# Chapter 1 layer audit

Contract PASS2-001, 2026-09-26. Role: `.claude/agents/layer-auditor.md`. Model: claude-opus-5-5 (effort high).
Branch `audit/ch01`, base commit `9136437`.

Subject: `models/ch01-cumulative.sysml` (25 lines, generated fixture, not edited).
Method: the four-question pass and the per-layer checklist in `.claude/skills/architecture-layers/SKILL.md`, AGENTS.md §1.5 and §1.6, and the glossary (`uv run python -m glossary tutorial TERM`). The model was loaded with OpenSysML v0.9.0 (`load_from_content`, `model.ok == True`, no diagnostics) and its API JSON export was read to confirm what the text says: `ToastingSystem` has `isAbstract: true`; there are exactly two `Subclassification`s (`HeatingSystem` and `ControlSystem` to `ToastingSystem`); `power` and `cycleTime` each have a `FeatureValue` with `isDefault: true`; there is no `Subclassification` from `Toaster` and no usage typed by `Heater`.

Evidence read for intent: `chapters/ch01-system-purpose/index.md`, `conclusion.md`, and all cells of notebooks `01` to `04`. Later fixtures (`models/ch02` to `ch08-cumulative.sysml`) were read only to see how Chapter 1 elements are used downstream, not audited.

Chapter 1 is the start of the tutorial, so the status column separates two kinds of "no" on the checklist: **wrong** (the model says something the layer rules say it must not) and **not yet built** (a checklist item that is expected to fail this early). Both are listed; only the first kind is a defect in Chapter 1.

## Classification table

| Element (qualified name) | Layer | Reason | Status |
|---|---|---|---|
| `ToasterDemo` (package) | none (container) | A namespace; carries no intent, prescription or value. | PASS (not classified) |
| `ToasterDemo::ToastingSystem` (`abstract part def`) | Functional by the method; construct is the logical idiom | Q1 (substitution test, §1.5 boundary tests): a pop-up toaster and tongs-with-a-blowtorch are both "toasting systems". It carries no mechanism, no `perform`, no interface, so it is not a logical component (`term-logical-architecture`, §1.5 gloss *logical component*: "the prescribed carrier of a mechanism"). The `abstract part def` form is what §1.5 lists for the logical layer. | OPEN-QUESTION (OQ-1) |
| `ToasterDemo::ToastingSystem` doc "Transform bread into toast acceptable to its user." | Functional | Solution-independent intent with an acceptance clause (`term-functional-architecture`); "acceptable to its user" is the seed of a MoE but is not yet a measurable attribute with a unit and means of collection (`term-moe`). | PASS; MoE not yet built |
| `ToasterDemo::Heater` (`part def`) | Physical | Q3: a concrete part def whose only content is a value that a chosen part has (skill example "the coil is an 800 W nichrome element"; `term-physical-architecture`). | FINDING F-2 (not yet built: no logical def to specialize; unused) |
| `ToasterDemo::Heater::power : ISQ::PowerValue default = 800.0 [SI::W]` | Physical | Q3: a value only a chosen part has; a rated power is a sizing choice (§1.5 *Numbers*: "sizing choices appear only when a physical part is chosen"). It is a prescription, not a TPM, since it is chosen, not assessed (`term-tpm`). | PASS |
| `ToasterDemo::HeatingSystem` (`part def :> ToastingSystem`) | Logical (recommended), undecided | A responsibility grouping (Douglas "who", `def-douglas--logical-architecture`; §1.2 "Douglas's 'who' is this tutorial's 'how'"). Later chapters allocate `ApplyHeat` to it (`ch05-cumulative.sysml` line 53), which treats it as a logical component. But it commits to no mechanism and is concrete, not abstract. | OPEN-QUESTION (OQ-2) |
| `ToasterDemo::ControlSystem` (`part def :> ToastingSystem`) | Logical (recommended), undecided | Same as `HeatingSystem`: a responsibility grouping with no mechanism, no policy (`term-policy` via §1.5 gloss), no interface, concrete. | OPEN-QUESTION (OQ-2) |
| `HeatingSystem :> ToastingSystem` (Subclassification) | Cross-layer relation | Says every heating subsystem is a kind of the whole toasting system, so it inherits the purpose "transform bread into toast". The whole system, `Toaster`, does not specialize `ToastingSystem`. | FINDING F-3 |
| `ControlSystem :> ToastingSystem` (Subclassification) | Cross-layer relation | As above. | FINDING F-3 |
| `ToasterDemo::Toaster` (`part def`) | Logical (recommended), undecided | It prescribes an arrangement (one heating and one control subsystem) and names no specific part and no part value (§1.5 logical-to-physical test). `index.md` calls the chapter "the physical architecture layer". | OPEN-QUESTION (OQ-3); also FINDING F-3 |
| `ToasterDemo::Toaster::cycleTime : ISQ::DurationValue default = 120.0 [SI::s]` | Emergent result | Q4: a cycle time is a result the design is expected to produce (§1.5 prescribed-versus-emergent test; skill Q4 names "a cycle time"; `term-behavior`). It is entered as a default value, that is, as a choice. | FINDING F-1 (see OQ-4 for the one reading under which it is not) |
| `ToasterDemo::Toaster::heating : HeatingSystem` (part usage) | Follows its type (logical, recommended) | Composition of a responsibility grouping into the system arrangement. | OPEN-QUESTION (via OQ-2) |
| `ToasterDemo::Toaster::control : ControlSystem` (part usage) | Follows its type (logical, recommended) | As above. | OPEN-QUESTION (via OQ-2) |
| Imports `ScalarValues::*`, `SI::*`, `ISQ::*` (unnamed `NamespaceImport`s) | none | Library access, no engineering content. | PASS (not classified) |

## Per-layer checklist results

**Functional**
- Typed inputs and outputs on each action: no actions exist. Not yet built (actions arrive in Chapter 4, `chapters/ch04-functional-decomp`).
- Solution-independent statements: the only functional statement (the `doc`) passes the substitution test. PASS.
- Phenomena relations as relations: none stated. Not yet built.
- At least one MoE about acceptance: none. The doc names acceptance in prose only. Not yet built (Chapter 3 is "measures").
- Reads as an objective: partly; the doc says what is good but not what is good enough.

**Logical**
- Each mechanism has a carrier and matching interfaces: there are no mechanisms, no `perform`, no ports. Not yet built. Port-type conformance (§1.9, `opensysml-query` recipe 5) is **open**, not passed, since no connection is declared.
- MoP thresholds derived from a MoE: none. Not yet built.
- No solution values and no results entered as choices: fails if `Toaster` is logical, because `Toaster::cycleTime` carries a value (F-1). `HeatingSystem` and `ControlSystem` carry no values: PASS.
- Reads as a design space: the arrangement is a typed slot structure, but with no constraints yet.

**Physical**
- Each part is a concrete def specializing an abstract logical def: `Heater` specializes nothing (F-2).
- Values meet derived thresholds, TPM assessed: no thresholds exist to meet in Chapter 1. Not yet built. (Downstream, `ch06-cumulative.sysml` checks `heater.power >= 600.0 [SI::W]`; not audited here.)
- Reads as a candidate: `Heater` is a point value with nothing to be feasible against.

**Across layers**
- Stopping rule (every leaf concrete, interfaced, verified, §1.8): no leaf meets it. Expected at Chapter 1; not yet built.
- An emergent result set as an attribute default and then "verified": in Chapter 1, `cycleTime` is set as a default (F-1). The "verified" half happens downstream: `ch02-cumulative.sysml` line 35 has `require constraint { toaster.cycleTime <= 180.0 [SI::s] }`, and notebook 04 cell 5 says "Requirements in later chapters will constrain this value." That is the pattern §1.5 and the skill's last example row name as not a valid check.
- Judgment recorded: no judgment is exercised in the Chapter 1 model. Not applicable.
- Figures: not checked (see below).

## Findings

**F-1. `Toaster::cycleTime` is an emergent result entered as a choice (wrong, not merely early).**
Check: prescribed versus emergent (AGENTS.md §1.5 boundary tests and §1.6; skill Q4 and the "Cycle time = 120 s ... Not a valid check" example; `term-behavior`). `attribute cycleTime : ISQ::DurationValue default = 120.0 [SI::s]` gives a cycle time a value by declaration. The export confirms a `FeatureValue` with `isDefault: true`. An unvalued `cycleTime` slot would be "not yet built"; the value is what makes it a defect. Notebook 04 cell 5 and `ch02-cumulative.sysml` line 35 show the value is then tested against a threshold. One alternative reading (a timer setpoint) is recorded as OQ-4. I did not change the model or the notebook.

**F-2. `Heater` specializes no logical def and is not used anywhere in the Chapter 1 model (not yet built, but flagged).**
Check: physical checklist, first item; AGENTS.md §1.5 *Allocation is not realization* (a concrete part def specializes the abstract logical def to realize it). `Heater` has no supertype, and no usage is typed by it (confirmed in the export: no `Subclassification` or `FeatureTyping` targets `ToasterDemo__Heater`). `Toaster::heating` is typed by `HeatingSystem`, and the model does not say how `Heater` relates to `HeatingSystem`. Downstream, `Heater` is used as a requirement subject and in `part efficient : Heater` (`ch06`, `ch08`), while realization of `HeatingSystem` goes through a separate `HeatingAssembly :> HeatingSystem` (`ch08-cumulative.sysml` line 68), so `Heater` never joins the hierarchy through Chapter 8. That is outside this audit but suggests the gap does not close by itself. I did not fix it.

**F-3. Specialization is used where the text describes decomposition, and the whole system does not specialize its purpose.**
Check: logical checklist (a logical component carries a mechanism; §1.5 gloss *logical component*) and cross-layer traceability. `HeatingSystem :> ToastingSystem` and `ControlSystem :> ToastingSystem` say each subsystem *is a* toasting system, so each inherits the doc "Transform bread into toast acceptable to its user", which neither does alone. `Toaster`, the element that composes them and that the text calls "the top-level system definition" (notebook 04 cell 3), has no `Subclassification` to `ToastingSystem`. The purpose is attached to the parts and not to the whole. Whether this is wrong depends on what `ToastingSystem` denotes (OQ-1). The chapter says both: "the system concept" (notebook 01 cell 1) and "kinds of toasting-system components" (`conclusion.md`). I did not propose a rewrite.

**F-4. Chapter text disagrees with the fixture and with itself about layer and types (documentation consistency; not a layer defect in the model).**
- `index.md` "Expected result" lists `power : Real default = 800.0` and `cycleTime : Real default = 120.0`. The fixture uses `ISQ::PowerValue ... [SI::W]` and `ISQ::DurationValue ... [SI::s]`, and notebook 02 cell 5 teaches the ISQ types. The index Ingredients row also says `attribute : Real default`.
- `index.md` Method says Chapter 1 is "the physical architecture layer". `conclusion.md` says "The structure is implementation-agnostic. It states what the system is made of, not how each part works." A model that contains an 800 W part value is not implementation-agnostic, and "implementation-agnostic" contradicts "physical".
- Notebook 01 cell 2 says "abstract modifier not yet supported — toaster#9 / OpenSysML#595". The v0.9.0 export reports `isAbstract: true` for `ToastingSystem`, so the comment may be stale. I did not check the issue, or whether "not supported" refers to an editor API rather than parsing.
Reported only; no edits.

## Open questions (for the orchestrator to route)

**OQ-1. Which layer is `ToastingSystem`, and what does it denote?**
- Functional reading: it passes the substitution test (Q1 is "yes", so the method stops there); its only content is a solution-independent purpose (`term-functional-architecture`); notebook 01 calls it "the system concept".
- Logical reading: `abstract part def` is the §1.5 logical idiom, and the contract premise calls it logical. Against this: it carries no mechanism, `perform` or interface, so it does not meet the glossary's *logical component* (a carrier of a mechanism).
- A third reading, from `conclusion.md`: a supertype of "toasting-system components", which would make it a category of logical components rather than the system.
- Recommended default: classify it as **functional** (a purpose holder), note that the construct matches the logical idiom, and treat F-3 as live until the denotation is decided.

**OQ-2. Are `HeatingSystem` and `ControlSystem` logical components that are not built yet, or a layer the tutorial does not name?**
- Logical: they are responsibility groupings (Douglas "who" = tutorial "how", §1.2 and DL-015); `ch05` allocates `ApplyHeat` to `HeatingSystem`, which is what §1.5 says allocation does for logical components.
- Not logical yet: they commit to no mechanism or policy and are concrete (`part def`, not `abstract part def`), so they fail Q2's "commits to a mechanism". Under Q1 a pop-up toaster and tongs-with-a-blowtorch both have "something that heats" and "something that controls" (for the tongs, the user), but a part def is not a function, so Q1 does not apply cleanly.
- Recommended default: **logical, not yet built** (mechanism, `perform` and interfaces to come). Also flag that the logical idiom is `abstract part def` and they are concrete.

**OQ-3. Which layer is `Toaster`?**
- Logical: it prescribes an arrangement (heating plus control) and names no specific part or value except `cycleTime`, which is not a part value (F-1). §1.5 logical-to-physical test: any part built to the arrangement would satisfy it.
- Physical: `index.md` says Chapter 1 builds "the physical architecture layer ... the structural types that implement the functions"; `Toaster` is a concrete part def, and the name suggests a pop-up appliance rather than tongs.
- Recommended default: **logical** (the system-level arrangement). Record the conflict with `index.md` (F-4).

**OQ-4. Is `cycleTime` a timer setpoint (a prescribed policy parameter) rather than an emergent result?**
- Setpoint reading: many pop-up toasters end the cycle on a timer, so a duration can be a control-policy parameter (`term-policy`), a legitimate prescription; `ControlSystem` exists to carry one.
- Emergent reading: it sits on `Toaster` (the whole), not on `ControlSystem`; nothing names it a setpoint; notebook 04 cell 5 calls it "the toaster-level duration attribute" that requirements will constrain; `ch02` checks it against 180 s, which treats it as a result; the skill's example table names this exact construct as not a valid check.
- Recommended default: **emergent result** (keep F-1). If a timer is intended, it could be modeled as a separately named setpoint on the control component, distinct from the time to acceptable toast. That modeling choice is the orchestrator's to route, not mine.

**OQ-5. MoE or MoP for a toasting time (flagged, not raised by Chapter 1 itself).**
Chapter 1 does not tag `cycleTime` as either. §1.5 says toasting time may be either, by recorded judgment. Once F-1 and OQ-4 are settled, the chapter that introduces measures (Chapter 3) will need that judgment recorded. Recommended default: no action for Chapter 1.

## Contract premises that did not hold

1. **"Chapter 1 is meant to teach the functional layer only."** Not supported at HEAD. `index.md` (Method) says: "In the video's terms, this is the physical architecture layer ... the functional layer (what those parts do) comes in Chapter 4." `conclusion.md` says "structure now, behavior later". The model contains elements that classify as physical (`Heater`, `power`), emergent (`cycleTime`) and probably logical (OQ-2, OQ-3). Only the `doc` and possibly `ToastingSystem` (OQ-1) are functional.
2. **"`Heater.power` and `Toaster.cycleTime` are intended as prescriptions."** Holds for `Heater.power`: notebook 02 presents it as a numeric parameter with an overridable default, and it is a legitimate physical prescription. For `Toaster.cycleTime` it holds for the form but not for the kind: the repository enters it as a prescription (a default, which later chapters constrain), but under AGENTS.md §1.5 and §1.6 a cycle time is an emergent result that must not be entered as a choice. That conflict is F-1, and the one reading in which it is a prescription is OQ-4.
3. **"`ToastingSystem` is a logical-layer element."** Not supported at HEAD. The construct (`abstract part def`) matches the logical idiom, but the element carries no mechanism, `perform` or interface, and the chapter describes it as "the system concept" with a purpose `doc`. The method classifies it as functional (OQ-1).

## Constructs that could not be classified cleanly

- `HeatingSystem`, `ControlSystem` and the usages typed by them: components with no mechanism. The four questions do not settle their layer (OQ-2).
- The two `Subclassification`s: relations between elements whose own layers are open, so they are reported as cross-layer (F-3) rather than given a layer.
- The package and the imports: containers and library access, with no layer.

## Not checked, and why

- **Diagrams and figures** (cross-layer checklist, last item): the contract scope is the model file; I did not render or inspect Chapter 1 figures.
- **`exercises/ch01/exercise.ipynb`**: not in scope.
- **Later chapters**: read only to see how Chapter 1 elements are used; they were not audited. Statements about `ch02` to `ch08` above are observations, not findings on those chapters.
- **toaster#9 / OpenSysML#595 and toaster#16 / OpenSysML#603** (cited in notebook comments): not checked; F-4 notes only that the export shows `isAbstract: true`.
- **Glossary sources**: `uv run python -m glossary check` passes (0 errors, 7 warnings). The warnings say the local source PDFs (SEBoK, SysML, KerML, Sutton and Barto, and others) are not in `glossary/sources/local/`, so source hashes were not verified. I relied on the glossary's recorded definitions, not on the source texts.
- **Douglas timestamps**: not re-verified (the skill already notes this).
