# Chapter 6 layer audit

Contract PASS2-011-A, 2026-09-27. Role: `.claude/agents/layer-auditor.md`. Model: claude-opus-5-5[1m] (effort high).
Branch `audit/ch06`, base commit `a84dceb`.

Subject: the elements Chapter 6 adds, that is, the diff between `models/ch05-cumulative.sysml` (60 lines) and `models/ch06-cumulative.sysml` (82 lines). Both are generated fixtures and were not edited. The diff is lines 54 to 75 of the ch06 fixture, plus the header comment on line 3:

```
requirement def HeatingReq {
    subject heater : Heater;
    require constraint { heater.power >= 600.0 [SI::W] }
}
requirement heating : HeatingReq;
part efficient : Heater;
part weak : Heater { attribute :>> power = 400.0 [SI::W]; }
abstract part def HeatingElement;
part def ResistanceCoil :> HeatingElement {
    attribute resistance : Real default = 12.0;
}
part def PowerWire :> HeatingElement {
    attribute gauge : Real default = 14.0;
}
part def HeatingAssembly :> HeatingSystem {
    part coil : ResistanceCoil;
    part wire : PowerWire;
}
part heatingEvidence {
    assert satisfy heating by efficient;
    assert satisfy heating by weak;
}
```

Method: the four-question pass and the per-layer checklist in `.claude/skills/architecture-layers/SKILL.md`, AGENTS.md §1.5 to §1.9, `z-principles.md` (F1 to F7, P1 to P6, and the confirmed extensions), the glossary (`uv run python -m glossary tutorial TERM` for specialization, physical architecture, logical component, mop, tpm, traceability, decomposition, requirement, usage, asserted inference, abstract definition, part definition, emergence), and the ACE rulings DL-018 to DL-039 as settled precedent. I cite DL numbers by the headings in `decisions/log.md` (see premise 6 on a numbering mismatch). I did not re-argue those rulings.

Evidence collected by running things:
- `uv run python scripts/check_conformance.py models/ch06-cumulative.sysml --stage 6,0`: `ok=True`, no diagnostics, four gap findings (`allocate-between-definitions` twice on `ToasterDemo::@19`; `part-typed-only-by-item-def` on `BreadLoader::bread` and `BreadEjector::bread`). All four are on Chapter 5 lines (53, 76, 77); none is on a Chapter 6 addition. Both project checks (`port-type`, `satisfaction-claims-evaluated`) are `blocked` with the unblock criterion "no language-tier violation, per the spec, is present". Exit code 0.
- Both fixtures loaded with OpenSysML v0.9.0 (`load_from_content`, `strict=False`): both `ok == True`. A diff of the API JSON export by qualified name (helpers in `src/toaster/query.py`) gives exactly these added named elements: `RequirementDefinition HeatingReq` with `ReferenceUsage HeatingReq::heater` (subject) and `ConstraintUsage HeatingReq::@1`; `RequirementUsage heating`; `PartUsage efficient`, `weak` (with `AttributeUsage weak::@0`, a redefinition of `power`); `PartDefinition HeatingElement` (`isAbstract` true), `ResistanceCoil` (with `resistance`), `PowerWire` (with `gauge`), `HeatingAssembly` (with `PartUsage coil`, `wire`); `PartUsage heatingEvidence` with two `SatisfyRequirementUsage`s (`@0`, `@1`). Metaclass deltas include 3 `Subclassification`s and 1 `Redefinition`, and no `AllocationUsage`, `PerformActionUsage`, `PortDefinition`, `PortUsage`, `InterfaceDefinition`, `ConnectionUsage` or `FlowUsage`.
- `perform_relationships(m6) == []`. `find_allocations(m6)` returns only the Chapter 5 `@19`. `allocations_for(m6, "ToasterDemo::HeatingAssembly")` returns `@19` by inheritance through `HeatingAssembly :> HeatingSystem`. `port_type_mismatches(m6) == []` (vacuous: no port ends).
- Specialization closure: `HeatingAssembly` has supertypes `{HeatingSystem, ToastingSystem}` and nothing specializes it or types a usage by it. `HeatingElement` has no supertypes; its subtypes are `ResistanceCoil`, `PowerWire` and the two `HeatingAssembly` slots. `Heater` has no supertypes; the only usages typed by it are `HeatingReq::heater`, `efficient` and `weak`. `HeatingSystem`'s only usage is still `Toaster::heating`.
- Satisfaction claims: the registered check is blocked, so I called `toaster.conformance.satisfaction_claims_evaluated(m6)` directly, as a diagnostic and not as a check verdict. It returns two findings: `evidence::@1` (`timely(slow)` is False, Chapter 3) and `heatingEvidence::@1` (`heating(weak)` is False, Chapter 6). Direct `model.eval`: `HeatingReq(efficient)` True, `HeatingReq(weak)` False, `heating(efficient)` True, `heating(weak)` False.
- Probe: `attribute r : ISQ::ResistanceValue default = 12.0 [SI::ohm];` loads with `ok=True` in OpenSysML v0.9.0 (a unit-bearing type for the coil's resistance is expressible). `[SI::Ω]` does not parse.
- The code cells of the three notebooks were executed in order from their directory (source only, outputs not written): notebooks 01 and 02 run; notebook 03 stops at cell-04 with `NameError: name 'ReviewRecord' is not defined`.
- `uv run python -m glossary lint`: 8 hits, none in `chapters/ch06-recursive-decomp/`. `uv run python -m glossary check` passes in this worktree (see Not checked).

Evidence read for intent: `chapters/ch06-recursive-decomp/index.md`, `conclusion.md`, and every cell of notebooks `01-subsystem-requirements`, `02-second-level` and `03-stopping-judgment`. `exercises/ch02/exercise.ipynb` and `exercises/ch03/exercise.ipynb` were read only to locate the identifier `AC-C01`. `src/toaster/conformance.py` was read for the check's behaviour.

## Classification table

Elements from earlier chapters that the additions reference are shown in *italics* for context. They are not audited here.

| Element (qualified name) | Layer | Reason | Status |
|---|---|---|---|
| `ToasterDemo::HeatingReq` (`requirement def`) | Logical: the form of a derived MoP threshold; the MoE or MoP label is unrecorded | Skill Q2 and example row "Heating efficiency is at least 0.6" (logical, MoP threshold); AGENTS.md §1.5 "Constraints, split" (a derived MoP threshold is logical) and "Numbers"; `term-mop`. A minimum heating power is an engineering performance measure. No label or justification is recorded (P2; DL-035 pattern). | FINDING F-3, F-4; OPEN-QUESTION OQ-2 |
| `ToasterDemo::HeatingReq::heater : Heater` (subject, `ReferenceUsage`) | Binds the requirement to a physical part def | *`Heater`* confers 800 W, a physical sizing choice (DL-021; ch01 F-2). It specializes nothing and is not composed anywhere in the system of interest. | FINDING F-3 |
| `ToasterDemo::HeatingReq::@1` (`require constraint { heater.power >= 600.0 [SI::W] }`) | Logical (a MoP threshold) | §1.5: a derived MoP threshold is logical. The skill's logical checklist asks that it be derived from a MoE, with a means of checking. It is a free-standing number. | FINDING F-4 |
| `ToasterDemo::heating : HeatingReq` (`RequirementUsage`) | Logical (follows its definition) | Same as `HeatingReq`. Its name repeats `Toaster::heating` (a `HeatingSystem` part usage). | FINDING F-11 |
| `ToasterDemo::efficient : Heater` (`PartUsage`) | Physical by its type (a usage of a part def that confers a value); adds nothing | DL-021 (Heater's 800 W is physical). Z-confirmed extension of F7 to usages (DL-032 in the log): "candidate" requires a concrete part that realizes a logical slot. `Heater` realizes none, and `efficient` is not in `Toaster`. | FINDING F-5, F-11 |
| `ToasterDemo::weak : Heater` (`PartUsage`) with `weak::@0` (`:>> power = 400.0 [SI::W]`) | Physical if `power` is a prescribed part value (the default reading); an entered result if not | Q3 (a value only a chosen part has) versus Q4 (a result), depending on what `power` denotes. It is the failing-branch fixture for `HeatingReq`. | FINDING F-1, F-5; OPEN-QUESTION OQ-1 |
| `ToasterDemo::HeatingElement` (`abstract part def`) | Logical, not yet built (DL-020 pattern) | It uses the logical idiom's form (§1.5 table; `term-abstract`) but carries no `perform`, mechanism, attribute or interface (`term-logical-component`). It is related to nothing on the logical side: `HeatingSystem` has no slot typed by it. | FINDING F-6, F-7; OPEN-QUESTION OQ-3 |
| `ToasterDemo::ResistanceCoil` (`part def :> HeatingElement`) | Physical | Q3: it names a specific kind of part (a resistive coil) and gives it a value. A concrete def specializes an abstract def (§1.5 physical idiom). | FINDING F-6, F-9 |
| `ToasterDemo::ResistanceCoil::resistance : Real default = 12.0` | Physical (a part value) | §1.5 "Numbers": a value a chosen part has. It has no unit, and nothing assesses it against a threshold. | FINDING F-9 |
| `ResistanceCoil :> HeatingElement` (`Subclassification`) | Realization by specialization (§1.5 "Allocation is not realization") | The shape is right. `HeatingElement` declares no feature, interface or `perform`, so there is nothing to conform to and nothing is realized. | PASS (shape); see F-6 |
| `ToasterDemo::PowerWire` (`part def :> HeatingElement`) | Physical | Q3: a specific kind of part with a value. | FINDING F-7, F-8, F-9 |
| `ToasterDemo::PowerWire::gauge : Real default = 14.0` | Physical (a part value) | §1.5 "Numbers". The model does not state what it denotes (AWG number, cross-section) or its unit. | FINDING F-9 |
| `PowerWire :> HeatingElement` (`Subclassification`) | Realization by specialization, as declared | `term-specialization`: the specialized def is a kind of the general one. A power wire is not a heating element, and the chapter's own text says it "delivers the electrical power input". | FINDING F-7 |
| `ToasterDemo::HeatingAssembly` (`part def :> HeatingSystem`) | Physical (it composes named concrete parts), with a logical arrangement in its composition | Q3: it names specific part defs. F2: it mixes an arrangement (two slots, logical per heuristic 3) with physical slot types, and I report the mix. It is not part of the system of interest: nothing is typed by it. | FINDING F-5, F-8 |
| `HeatingAssembly :> HeatingSystem` (`Subclassification`) | Realization of a logical component by specialization (§1.5) | This is the first place in Ch1 to Ch6 where a concrete def specializes a logical component. `HeatingSystem` is concrete, though (DL-020), and `Toaster::heating` is still typed `HeatingSystem`. | FINDING F-5 |
| `ToasterDemo::HeatingAssembly::coil : ResistanceCoil` (`PartUsage`) | Physical (follows its type) | A slot filled by a concrete part. | PASS (layer); see F-8 |
| `ToasterDemo::HeatingAssembly::wire : PowerWire` (`PartUsage`) | Physical (follows its type) | Same. | PASS (layer); see F-8 |
| `ToasterDemo::heatingEvidence` (untyped `PartUsage`) | Not a layer element; a container defect | DL-033(3): a part usage with no part, used as a namespace for claims and named "evidence". Same pattern as Chapter 2's `part evidence`. | FINDING F-2 |
| `ToasterDemo::heatingEvidence::@0` (`assert satisfy heating by efficient`) | No layer: a cross-layer traceability claim | DL-033(2); `term-traceability`. It evaluates True on the model's own values. Its staged check is blocked, so this is not a passed check. The subject is outside the system (F-3). | FINDING F-3 |
| `ToasterDemo::heatingEvidence::@1` (`assert satisfy heating by weak`) | No layer: a cross-layer traceability claim | DL-033(2). It evaluates False (400 W < 600 W). DL-039(4): a false positive assertion; a deliberate failing branch is `assert not satisfy` or a computed check. | FINDING F-1 |
| `AI-C06` (Python `ReviewRecord`, notebook 03 cell-05; not in the model) | Not a layer element | DL-033(1): a judgment record is analysis-side, audited on its P1 fields. | FINDING F-12 |
| *`ToasterDemo::Heater` (ch01)* | *Physical (DL-021; ch01 F-2 stands)* | *Context.* | *context* |
| *`ToasterDemo::HeatingSystem` (ch01)* | *Logical, not yet built (DL-020)* | *Context.* | *context* |
| *`allocate ApplyHeat to HeatingSystem` (ch05, `@19`)* | *Cross-layer relation; language non-conformant (DL-039; ch05 F-1)* | *Context: `HeatingAssembly` inherits it.* | *context* |

The header comment change on line 3 ("chapter 6") is not a model element. Chapter 6 adds no MoE, no MoP or TPM metadata, no action, no port, no interface, no connection, no flow, no allocation and no `perform`.

## Per-layer checklist results

**Functional**
- Chapter 6 adds no functional element. The function it claims to realize at the second level (`ApplyHeat`) is not decomposed, and no sub-function exists for "deliver power" (which the text gives to `PowerWire`) or "convert power to heat" (which it gives to `ResistanceCoil`) (F-6, OQ-4).
- No MoE is added. Not applicable.

**Logical**
- *Does each mechanism have a carrier and an interface?* No. `HeatingElement` is abstract but performs nothing and carries no mechanism or interface. Joule heating, the mechanism `ResistanceCoil`'s name implies, is not stated as a relation (F-6).
- *Do the interfaces actually match?* **Open**, and `blocked` in the tool. No port-typed connection is declared in Chapter 6, so by DL-038's applicability criterion the check does not yet apply. The CLI reports it `blocked` because of the inherited Chapter 5 gap findings. The empty `port_type_mismatches` result is vacuous and is not a pass.
- *Are MoP thresholds derived from a MoE, with a means of checking?* No. The 600 W bound is a free-standing number with no link to `timely` (180 s), to the energy relation or to any MoE. Its only means of checking is the model's own assertion (F-4).
- *Are there no solution values and no results entered as choices?* The logical additions (`HeatingReq`, `HeatingElement`) carry no solution values: PASS. Whether `Heater::power`, which `HeatingReq` checks, is a result entered as a choice is OQ-1.
- *Does it read as a design space?* Barely. `HeatingElement` is an empty slot type, and `HeatingSystem` gains no slots of its own.

**Physical**
- *Is each part a concrete def that specializes an abstract logical def, and does it fit that def's interfaces?* Partly. `ResistanceCoil` and `PowerWire` specialize the abstract `HeatingElement`, which has no interfaces, so "fits" holds only vacuously (F-6). `PowerWire`'s specialization is a false kind-of claim (F-7). `HeatingAssembly` specializes the logical component `HeatingSystem`, which is concrete (F-5).
- *Do the values meet the derived thresholds, and is the TPM assessed, not asserted?* No. `resistance` and `gauge` are unit-less and are checked against no threshold. The one threshold (`HeatingReq`) is checked on `Heater`, not on any of the new physical parts, and its "check" is an assertion (F-1, F-3, F-9).
- *Does it read as a candidate?* No. No usage of `Toaster` or of `HeatingSystem` contains `HeatingAssembly`, so there is no candidate toaster to check for feasibility or utility (F-5).

**Across layers**
- *Stopping rule* (§1.8: every leaf concrete, performs, connects, verified): the leaves `coil` and `wire` are concrete. They perform nothing, connect through nothing, and have no verification evidence. The rule is not met, yet `AI-C06` claims the decomposition is complete (F-8, F-12).
- *Emergent result set as a default and then "verified"*: the Chapter 1 `cycleTime` defect (DL-018) is inherited unchanged. Chapter 6 repeats its syntactic shape with `Heater::power` (default 800 W, `weak` binds 400 W, checked against 600 W). Whether that is the same defect depends on OQ-1.
- *Judgment recorded*: `AI-C06` is recorded with counterevidence and residual uncertainties, `disposition="pending"` and `engineering_conclusion="undetermined"` (no "accepted" disposition: PASS on SA-7). Its evidence and premises do not support its claim (F-12).
- *Figures*: Chapter 6 renders no view of the model at all (F-13).

## Findings

**F-1. The false `assert satisfy` pattern recurs: `assert satisfy heating by weak` is false, and nothing in the chapter or the tool reports it.**
Element: `heatingEvidence::@1`.
Check: DL-039(4) ("satisfaction claims evaluated", a staged project check; a deliberately failing branch is `assert not satisfy` or a computed check); the cross-layer checklist.
What is wrong:
- `model.eval("ToasterDemo::heating(ToasterDemo::weak)")` returns False (400 W against `>= 600 W`). OpenSysML loads the model with `ok=True`.
- The conformance CLI does not report it. `satisfaction-claims-evaluated` is `blocked` by the inherited Chapter 5 gap findings. It is also registered with `applies_from=None`, so on a gap-free model it would still report `open` ("unscheduled"). The finding comes only from calling `satisfaction_claims_evaluated` directly, which I did as a diagnostic and not as a verdict.
- The chapter presents the pattern as the thing to learn. Notebook 01 cell-01: "Each level has a formal specification, candidate variants, and satisfaction claims". Cell-03 of all three notebooks: two candidate heaters "exercise the new requirement using the same satisfy-assertion pattern from Chapter 3".
- `requirement_coverage` reports `heating` as covered by both `efficient` and `weak`, so a coverage view built from assertions counts the false claim as coverage.

What I did not do: I did not negate the assertion, schedule the check, or change the check's blocking rule.

**F-2. `part heatingEvidence` repeats the `part evidence` container defect.**
Element: `heatingEvidence`.
Check: DL-033(3).
What is wrong: it is an untyped part usage, composed by nothing, that holds only two satisfy claims and is named "evidence" for things that are claims. DL-033 reserves "evidence" for analysis results.
What I did not do: I did not choose a replacement idiom.

**F-3. `HeatingReq` constrains `Heater`, which is not part of the system being decomposed, so the "subsystem requirement" traces to nothing in the decomposition.**
Elements: `HeatingReq::heater`, `efficient`, `weak`, and the two satisfy claims.
Check: cross-layer traceability (`term-traceability`, Douglas: "the design traces back to the requirements it implements"); F7 (classify the pieces of the subject); the logical checklist.
What is wrong:
- `Heater` specializes nothing, and the only usages typed by it are the subject and the two variants. `Toaster` composes `heating : HeatingSystem`, and `HeatingAssembly` composes `ResistanceCoil` and `PowerWire`. None of these is, or contains, a `Heater`.
- So the requirement Chapter 6 adds "one level down" constrains a part def that sits outside the hierarchy it claims to be one level down in. No requirement applies to `HeatingSystem`, `HeatingAssembly`, `coil` or `wire`.
- The chapter text says the opposite: notebook 01 cell-01 ("the `Heater` part definition now has its own requirement"), cell-03 of all three notebooks ("on the `Heater` sub-component"), and `index.md` Method ("applies the requirement and attribute override pattern to `Heater`").

What I did not do: I did not re-target the subject or relate `Heater` to `ResistanceCoil`.

**F-4. The 600 W threshold is not derived, carries no label, and has no means of checking other than the assertion.**
Element: `HeatingReq::@1`.
Check: the skill's logical checklist ("Are MoP thresholds derived from a MoE, with a means of checking, not free-standing numbers?"); `term-mop` (SEBoK: a MoP "yields design requirements necessary to satisfy a MoE"); P2 and the DL-035 pattern (the MoE or MoP label is recorded with a justification).
What is wrong:
- Nothing in the model or the notebooks derives 600 W from `timely` (180 s), from the energy relation (`DeliveredEnergy`) or from any MoE. The number appears only in the constraint.
- No MoE or MoP label, and no justification for one, is recorded. No `verification def` or analysis checks it; only `heatingEvidence` asserts it.

What I did not do: I did not derive a threshold or propose a label.

**F-5. The logical-to-physical chain still does not complete: the new physical parts never reach the system of interest.**
Elements: `HeatingAssembly`, `HeatingAssembly :> HeatingSystem`, `efficient`, `weak`.
Check: the physical checklist ("Reads as a candidate"); the Z-confirmed extension of F7 to usages (DL-032 in the log: "candidate" requires a concrete part that realizes a logical slot); pass4-backlog §3.
What is wrong:
- `HeatingAssembly :> HeatingSystem` is the first concrete specialization of a logical component in Ch1 to Ch6. That is progress on the chain.
- Nothing is typed by `HeatingAssembly`. `Toaster::heating` is still typed `HeatingSystem`, which has no parts, and `nominal` and `slow` are unchanged. So no usage anywhere contains the coil or the wire, and there is no candidate toaster.
- `HeatingSystem` is still concrete (DL-020), so the realization is from a concrete logical grouping, not from the abstract carrier the §1.5 idiom names.
- The two branches Chapter 6 adds are disjoint: the requirement branch (`Heater`, `efficient`, `weak`) and the structure branch (`HeatingElement`, `ResistanceCoil`, `PowerWire`, `HeatingAssembly`) share no element.
- The notebooks call `efficient` and `weak` "candidate heaters". Under DL-032 that label is unsupported: `Heater` realizes no logical slot.

What I did not do: I did not add a candidate usage or retype `Toaster::heating`.

**F-6. Missing realization recurs: no `perform`, no allocation to the new parts, and no mechanism. Yet the chapter says the coil "realizes" the allocated function.**
Elements: `HeatingElement`, `ResistanceCoil`, `HeatingAssembly`.
Check: `term-logical-component` ("an abstract part definition that performs an action"); AGENTS.md §1.5 ("Allocation is not realization"; Joule heating stated for a chosen component is logical); §1.8 (a leaf performs its specified behavior); the logical checklist, first item; pass4-backlog §3.
What is wrong:
- `perform_relationships` is empty for the whole model. `HeatingElement` is abstract but performs nothing.
- No allocation was added. The only link from `ApplyHeat` to the new structure is inherited through `HeatingAssembly :> HeatingSystem` from the Chapter 5 allocation, which is between definitions and language non-conformant (DL-039).
- No constraint relates `resistance` to power or heat (Joule heating, `P = V^2 / R` or `I^2 R`). The mechanism the name `ResistanceCoil` implies is not in the model.
- `conclusion.md`: "`ResistanceCoil` realizes heat application (the function `ApplyHeat` allocates to `HeatingSystem`)". `AI-C06`'s claim: "every function allocated to HeatingSystem is realized by at least one subpart". Neither has model support.

What I did not do: I did not add `perform`, an allocation or a mechanism constraint.

**F-7. `PowerWire :> HeatingElement` declares a power wire to be a kind of heating element.**
Elements: `PowerWire`, its `Subclassification`, and `HeatingElement`.
Check: `term-specialization` (the specialized definition is a kind of the general one and inherits its features); the physical checklist ("specializes an abstract logical def"); F4 (the model is the authority on meaning).
What is wrong:
- The chapter's own text gives the two parts different jobs: the coil "applies thermal energy", while the wire "delivers electrical power to the coil" (`conclusion.md`; `AI-C06` rationale). A conductor that delivers power is not a heating element.
- The specialization makes the abstract type a grab-bag of "parts inside the heating assembly" rather than the carrier of one mechanism.
- Because `HeatingElement` declares nothing, the error changes no inherited feature today. It is still a false modeling claim, and it is what the learner reads as the abstract-to-concrete pattern.

What I did not do: I did not introduce a separate abstract def for power delivery.

**F-8. The coil and the wire are not connected, and no interface exists, so the leaves do not "connect through the specified interfaces".**
Elements: `HeatingAssembly`, `coil`, `wire`, `PowerWire`.
Check: §1.8 stopping rule; §1.5 "Connectivity differs by layer"; the logical checklist, first two items; DL-038.
What is wrong:
- The text's central claim for the wire (it delivers power to the coil) has no connection, flow, port or interface behind it.
- Neither the assembly nor `HeatingSystem` has a boundary interface for the electrical supply. A mains outlet is the skill's own example of a logical interface.
- The interface check is `open` under DL-038 (no port-typed connection declared) and `blocked` in the tool. An open check cannot support a completeness claim.

What I did not do: I did not add ports or a connection.

**F-9. The physical values have no units, and nothing assesses them.**
Elements: `ResistanceCoil::resistance`, `PowerWire::gauge`.
Check: AGENTS.md §1.4 ("A number produced in Python without a model-defined unit and relation is not evidence"); F4; the physical checklist ("is the TPM assessed ... not asserted"); DL-036's rule that the model states what an element denotes.
What is wrong:
- Both are `Real`. Every other quantity in the model uses ISQ types (DL-010). `ISQ::ResistanceValue` with `[SI::ohm]` loads in OpenSysML v0.9.0 (probed here), so the unit-less form is not forced by the tool.
- `gauge = 14.0` does not say whether it is an AWG number (dimensionless) or a cross-section. The model does not state it.
- Neither value is related to `Heater::power`, to a supply voltage or to any threshold. For example, the model cannot tell whether a 12 ohm coil is consistent with 800 W, since no supply is modeled.

What I did not do: I did not retype the attributes or add a supply.

**F-10. The settable-result shape recurs on `Heater::power`. Whether it is a defect is OQ-1.**
Elements: `weak::@0`, and `HeatingReq`'s check of `Heater::power` (the default of 800 W is ch01).
Check: the prescribed-versus-emergent boundary test (§1.5); the cross-layer checklist ("Is any emergent result set as an attribute default and then verified?"); DL-018; DL-032.
What is recorded: a default value, a variant that binds a different value, and a requirement that checks the entered value. That is the same shape as `cycleTime`, `slow` and `timely`. It is a defect only if `power` denotes a result (OQ-1). I record the shape as a finding so that it is not lost if OQ-1 goes the other way.

**F-11. Naming: `heating` is used twice, and `efficient` names a measure that the element does not carry.**
Elements: `ToasterDemo::heating` (requirement usage), `efficient`.
Check: P4 (learner-facing content earns its place and does not mislead); DL-037 (names convey commitments to the learner).
What is wrong:
- `ToasterDemo::heating` (a `RequirementUsage`) and `ToasterDemo::Toaster::heating` (a `HeatingSystem` part usage) share a name. Resolution is correct (the satisfy claims resolve to the requirement, as confirmed by evaluation). A learner reading `assert satisfy heating by weak` next to `part heating : HeatingSystem` still has two meanings for one word.
- `efficient` differs from `weak` only in power. Efficiency, which the glossary gives as the toaster's example MoP, is not modeled on `Heater`.

What I did not do: I did not rename anything.

**F-12. `AI-C06` does not run, and its evidence, premises and criterion do not support its claim.**
Element: the `AI-C06` `ReviewRecord` (notebook 03 cell-05). It is not a layer element (DL-033(1)) and is audited on its P1 fields.
Check: P1; DL-033(2) (a record citing the model's own assertion or declaration cites nothing); the DL-034 reasoning (evidence comes from analysis); §1.8 (account for every input and output).
What is wrong:
- (a) Notebook 03 fails at cell-04 with `NameError: name 'ReviewRecord' is not defined`. No cell imports `ReviewRecord`, `validate_record` or `hash_content`. This is the same defect as ch04 F-6 (pass4-backlog §8), and the chapter's expected result (`validate_record(stopping_judgment)` returns `[]`) is never reached.
- (b) `evidence_refs=["ToasterDemo::HeatingAssembly"]` cites the declaration whose sufficiency is being claimed. That is not evidence.
- (c) The rationale says the coil and the wire "account for both inputs to ApplyHeat (power and duration)". `ApplyHeat` has three inputs (`power`, `duration`, `efficiency`) and one output (`energy`). No part accounts for `duration`, which DL-031 places on a control function or setpoint. The criterion is weaker than §1.8's input and output accounting, the same weakness as ch04 F-2.
- (d) The criterion names "power delivery" as a realized function. No such function exists in the model (compare ch05 F-4).
- (e) `assumption_refs=["AC-C01"]`. That identifier is defined only in the learner template `exercises/ch02/exercise.ipynb`; the chapter's assumption record is `AC-001` (Chapter 2 notebook 03).
- (f) The premises are `AS-C03` (whose evidence is the Chapter 3 assertion; ch03 F-4) and `AI-C04` (ch04 F-2). Notebook 03 cell-01 says the chain "connects the stopping judgment back to the measured evidence". Nothing in the chain is measured.
- (g) Notebook 03 cell-06 says `validate_record()` returning `[]` "confirm[s] the chain is complete". It confirms only that the schema's fields are filled (P1: a check is not proof).
- The record's counterevidence ("a more detailed decomposition would add thermal interface parts and a control signal path") and its pending disposition are appropriate.

What I did not do: I did not fix the import or edit the record.

**F-13. Chapter text disagrees with the model and the layer rules, and no figure is shown.** This is documentation consistency, not a model defect.
- `index.md` Purpose: "a second-level structural decomposition of `HeatingSystem` into `ResistanceCoil` and `PowerWire`". `HeatingSystem` has no parts. The parts belong to a subtype that the system does not use (F-5).
- `conclusion.md`: "decomposed to a level where each allocated function maps to a structural part". "Structural" is not a tutorial layer (§1.5, as in ch05 F-7), and no function maps to a part (F-6).
- `conclusion.md`: "`ResistanceCoil` realizes heat application". This contradicts §1.5 ("Allocation is not realization"), and nothing performs the function (F-6).
- Notebooks 01, 02 and 03 cell-03 (the same paragraph three times): "Two candidate heaters" (unsupported, DL-032) and "the `Heater` sub-component" (F-3).
- `index.md` Method: "the same three-notebook structure (requirement, structure, judgment) that appeared in Chapters 2–4 recurs". The recursion §1.8 asks for is the three layers at each level. Chapter 6 adds no functional or logical content at the second level (OQ-4).
- Cell-06 of each notebook uses the world labels A-F, O-S and E. This is noted only; DL-028 parks the labels for the recipe rewrite.
- No notebook renders a view of the assembled model or of the second level (§1.7; the cross-layer checklist's last item).

Reported only; no edits.

## Open questions (for the orchestrator to route)

**OQ-1. Is `Heater::power` a prescribed part value (a rating) or a performance result? This decides whether `weak` is a valid failing branch and whether DL-018's defect recurs.**
- Reading A, a prescribed value. DL-021 already calls Heater's 800 W "a physical sizing choice", and §1.5 "Numbers" puts what a specific part has in the physical layer. On this reading, `HeatingReq` is a feasibility check of a chosen value against a threshold (F2: a candidate is checked for feasibility against the logical layer). `weak` then fails for a reason about the design: someone chose a 400 W part. That makes it the valid failing-branch content that DL-032 found `slow` lacked, and only its expression is wrong (F-1, DL-039).
- Reading B, a result. In the heating context, power is what `ApplyHeat` and `DeliveredEnergy` take in. The power a resistive element draws follows from supply voltage and resistance, and Chapter 6 adds exactly such a resistance (12, unit-less). On this reading 800 W and 400 W are results entered as choices (DL-018 in the `slow` form of DL-032), and the check cannot fail for a reason about the design.
- Recommended default: Reading A for `Heater` as declared. The model has no relation that derives `power`, and DL-021 has ruled the value a choice. Record with it that once a coil and a supply exist in the same candidate, its power must be derived from them and not entered a second time. That is a constraint on the re-derivation, not on this audit.

**OQ-2. What layer is a requirement whose constraint has the form of a MoP threshold but whose subject is typed by a physical part def?**
- Reading A, the constraint's layer: logical. The skill example row "Heating efficiency is at least 0.6" makes a performance threshold logical. The subject binding to `Heater` is then a traceability defect (F-3), not a layer.
- Reading B, a component specification at the physical layer. A requirement bound to a specific part def is a part spec, and its layer follows its subject.
- Reading C, the layer follows the MoE or MoP label, which DL-035's pattern leaves to the re-derivation's recorded justification. Heating power is an engineering measure (it is hard to argue a user accepts toast by its wattage), but the label is still unrecorded.
- Recommended default: Reading A, with the label left unruled as in DL-035. The table uses Reading A.

**OQ-3. Does the name `HeatingElement` commit to a mechanism before any selection among alternatives (the naming extension, DL-037 in the log)?**
- Reading A, generic. "An element that heats" covers a blowtorch's flame as well as a coil, so the abstract def names a responsibility.
- Reading B, mechanism-suggestive. In appliance usage a heating element is an electric resistive element, which only the pop-up branch has. Chapter 6 records no selection among alternatives before introducing it and `ResistanceCoil`.
- Recommended default: Reading B, so it is renamed by function (for example "heat source") in the re-derivation under DL-037, and the choice of a resistive mechanism is recorded as a selection. The layer is logical, not yet built, either way.

**OQ-4. Is a decomposition placed on a physical subtype (`HeatingAssembly :> HeatingSystem` composing concrete parts) an acceptable form of the recursion, or must each level pass through the functional and logical layers first?**
- Reading A, acceptable. §1.5 realizes a logical component by specialization, and a specialized def may add features (`term-specialization`). So realizing and then composing concrete parts is legal SysML and matches "concrete part defs realize logical components".
- Reading B, the recursion is incomplete. §1.8 says that "at each level the three boundaries in §1.5 apply again". Douglas decomposes until there is enough detail to allocate functions to components (`term-decomposition`). Chapter 6 goes straight from a level-1 logical grouping to level-2 physical parts, with no sub-functions of `ApplyHeat`, no abstract level-2 logical slots and no allocation at level 2.
- Recommended default: Reading B. It bears on whether AI-C06's "complete" can be true at all, and on how the Chapter 6 re-derivation is structured.

**OQ-5 (records). Which DL numbering is authoritative for DL-032 to DL-038?**
- The headings in `decisions/log.md` number the rulings one lower than `decisions/pass4-backlog.md` and the "Confirmed extensions" list in `.claude/skills/ace-protocol/z-principles.md`. For example, "F7 to usages" is DL-032 in the log and DL-033 in z-principles, and the naming ruling is DL-037 in the log and DL-038 in z-principles and the backlog.
- Recommended default: the log headings are authoritative, since the log is the record, and the other two files get corrected by whoever owns them (the z-principles file is a Z-confirmed skill file, so the correction goes through the skill-editor path). This report cites log headings throughout.

## Contract premises verified

1. **"The ch06 model repeats the false-satisfy pattern (heating vs weak)."** Holds. `heating(weak)` evaluates False, and OpenSysML loads the model with `ok=True` (F-1). The `slow` claim from Chapter 3 is also still false.
2. **"Whether the settable-result pattern recurs."** Its shape recurs on `Heater::power` (F-10). Whether it is DL-018's defect depends on OQ-1; my default reading says it does not. No new emergent-result attribute is added: `resistance` and `gauge` are part values. `cycleTime` is inherited unchanged.
3. **"Whether the missing-realization pattern recurs."** It recurs. There is no `perform` and no allocation is added, and realization is claimed only in prose and in `AI-C06` (F-6).
4. **The logical-to-physical chain never completing (backlog pattern).** It recurs, with partial progress. `HeatingAssembly :> HeatingSystem` and `ResistanceCoil :> HeatingElement` are the first concrete-to-logical and concrete-to-abstract specializations. The chain still does not reach the system of interest, and the two new branches are disjoint (F-5).
5. **"Use the new conformance tooling to get gap findings and false-satisfy findings."** Holds only in part. The CLI gives the four gap findings, all inherited from Chapter 5. It does not give false-satisfy findings: `satisfaction-claims-evaluated` is `blocked` by those gaps, and it is also unscheduled (`applies_from=None`), so it would report `open` on a gap-free model. I got the false-satisfy findings by calling the check function directly, as a diagnostic and not as a verdict. The CLI's exit code is 0 in this state, by design.
6. **"decisions/log.md DL-018 through DL-039 are the settled patterns"** holds. The cross-references to them in the backlog and in z-principles are off by one for DL-032 to DL-038 (OQ-5).
7. **"Lint hits: none for ch06."** Holds. `glossary lint` gives 8 hits, none in Chapter 6.

## Constructs that could not be classified cleanly

- `weak` (and its power binding): physical or an entered result, depending on OQ-1.
- `HeatingReq`: its layer depends on whether it follows the constraint, the subject or the unrecorded label (OQ-2).
- `HeatingAssembly`: physical by Q3, but it mixes a logical arrangement with physical slot types (F2). I report the mix.
- The satisfy claims, `heatingEvidence` and `AI-C06`: not layer elements (DL-033). They are classified by role.

## Not checked, and why

- **The Chapter 6 exercise** (`exercises/ch06/exercise.ipynb`): out of scope. I read the ch02 and ch03 exercises only to locate `AC-C01`.
- **Whether `AS-C03`'s own `assumption_refs` also cite `AC-C01`**: not checked. It is a Chapter 3 record.
- **Notebook execution under the real kernel**: I executed the code cells' source in order with `exec`, not with Jupyter or nbconvert. The `NameError` does not depend on the kernel. Execution under the chapter's actual runner was not done.
- **Chapters 7 and 8**: not read. The backlog says the `weak` pattern persists there. I did not verify that.
- **Spec text** for `SatisfyRequirementUsage` evaluation semantics, and whether a satisfy claim on a subject outside the system is admissible: not checked against formal/2026-03-02.
- **Glossary sources:** `uv run python -m glossary check` passes in this worktree (0 errors, 7 warnings). The warnings say the local source PDFs are absent, so source hashes were not verified. I relied on the glossary's recorded definitions.
