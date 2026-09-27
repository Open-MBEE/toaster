# Chapter 5 layer audit

Contract PASS2-008-D, 2026-09-26. Role: `.claude/agents/layer-auditor.md`. Model: claude-opus-5-5[1m] (effort high).
Branch `audit/ch05`, base commit `927f04f`.

Subject: the elements Chapter 5 adds, that is, the diff between `models/ch04-cumulative.sysml` (52 lines) and `models/ch05-cumulative.sysml` (60 lines). Both are generated fixtures and were not edited. The diff is lines 53 to 60 of the ch05 fixture, plus the header comment on line 3:

```
allocate ApplyHeat to HeatingSystem;
part def BreadLoader { part bread : Start; }
part def BreadEjector { part bread : Finish; }
part def BreadHandling {
    part loader : BreadLoader;
    part ejector : BreadEjector;
    flow loader.bread to ejector.bread;
}
```

Method: the four-question pass and the per-layer checklist in `.claude/skills/architecture-layers/SKILL.md`, AGENTS.md §1.5 and §1.6, the glossary (`uv run python -m glossary tutorial TERM` for logical component, allocation, mechanism, physical architecture, logical architecture, functional architecture, interface, selection among alternatives, perform action, specialization, abstract definition, part definition), and the ACE rulings DL-018 to DL-023 as settled precedent. I did not re-argue those rulings.

Evidence collected by running things:
- Both fixtures loaded with OpenSysML v0.9.0 (`load_from_content`, `strict=False`): `model.ok == True`, no diagnostics.
- A diff of the API JSON export by qualified name (helpers from `src/toaster/query.py`: `ApiIndex`, `find_allocations`, `find_connectors`, `perform_relationships`, `port_type_mismatches`, `specialization_graph`). The added elements are exactly: one `AllocationUsage` (`ToasterDemo::@19`, unnamed), three `PartDefinition`s, four `PartUsage`s and one `FlowUsage` (`ToasterDemo::BreadHandling::@2`, unnamed). Metaclass count deltas also show the implied `ReferenceUsage`, `FeatureChaining`, `ReferenceSubsetting`, `EndFeatureMembership` and `FeatureTyping` elements that belong to those.
- The allocation's two connector ends reference `ToasterDemo::ApplyHeat` (`ActionDefinition`) and `ToasterDemo::HeatingSystem` (`PartDefinition`): definitions, not usages.
- The flow's ends are `BreadHandling::loader` then `BreadLoader::bread`, and `BreadHandling::ejector` then `BreadEjector::bread`. Both `bread` features are `PartUsage`s typed by `ItemDefinition`s (`Start` and `Finish`), which have no supertypes in common.
- `perform_relationships(...) == []`. There are no `PortDefinition`, `PortUsage` or `InterfaceDefinition` elements. `port_type_mismatches(...) == []`. `HeatingSystem` has no `isAbstract` flag. Nothing specializes `HeatingSystem`, `BreadLoader`, `BreadEjector` or `BreadHandling`, and they specialize nothing new. No usage is typed by `BreadHandling` or by `ApplyHeat`.
- sysml-toolkit v0.9.1 (`~/Documents/GitHub/sysml-toolkit/target/release/sysmlv2 check --lib .../spec-refs/SysML-v2-Release/sysml.library`) was run on both fixtures. For ch04 it reports no errors. For ch05 it reports one error on line 53: `ReferenceSubsetting::referencedFeature must refer to a Feature [relationship-endpoint-metaclass]`. AGENTS.md §1.2 allows the toolchain to be cited only to flag a spec gap, which is the only way it is used here.
- The metamodel files vendored in that checkout (`spec-refs/KerML.xmi` and `spec-refs/SysML.xmi`, OMG metamodel 20250201) were read for two points. `ReferenceSubsetting::referencedFeature` is described as "The `Feature` that is referenced". `PartUsage` carries the constraint `validatePartUsagePartDefinition` ("At least one of the itemDefinitions of a PartUsage must be a PartDefinition"; OCL `partDefinition->notEmpty()`).

Evidence read for intent: `chapters/ch05-architecture/index.md`, `conclusion.md`, and every cell of notebooks `01-concept-selection`, `02-allocate` and `03-interfaces`. Chapter 4 notebook `02-heating-refinement` (cells 1, 5 and 6) was read only for what `Start` and `Finish` mean. `models/ch06` to `ch08-cumulative.sysml` were read only to see how the Chapter 5 additions are used downstream; they were not audited.

## Classification table

Elements from earlier chapters that the additions reference are shown in *italics* for context. They are not audited here.

| Element (qualified name) | Layer | Reason | Status |
|---|---|---|---|
| `allocate ApplyHeat to HeatingSystem` (`AllocationUsage` `ToasterDemo::@19`, unnamed) | Cross-layer relation: a function (functional) assigned to a logical component (logical) | Allocation assigns functions to logical components (`term-allocation`, AGENTS.md §1.5 gloss). DL-020 already classifies the target `HeatingSystem` as a logical component, not yet built. The source `ApplyHeat` reads as functional (OQ-4). So the relation goes to a logical component, not to a physical part. It is declared between definitions, though, which does not conform to the language. It has no name, so `model.query()` cannot see it. And no `perform` expresses the responsibility. | FINDING F-1, F-2 |
| *`ToasterDemo::ApplyHeat` (ch04 `action def`)* | *Functional, as read here* | *Depends on the Chapter 4 audit (OQ-4).* | *context* |
| *`ToasterDemo::HeatingSystem` (ch01 `part def :> ToastingSystem`)* | *Logical, not yet built* | *DL-020.* | *context* |
| `ToasterDemo::BreadLoader` (`part def`) | Logical, not yet built (DL-020 precedent) | Q3 does not apply: no specific part is named and no value is chosen (§1.5 logical-to-physical test). Like `HeatingSystem`, it is a responsibility grouping with no value and no modeled mechanism, and DL-020 classes that as logical, not yet built. It does not follow the logical idiom: it is concrete, has no `perform`, no port, and no function allocated to it (`term-logical-component`). | FINDING F-4 |
| `ToasterDemo::BreadLoader::bread : Start` (`PartUsage` typed by an `ItemDefinition`) | Logical by role: a flow endpoint standing in for an interface | Its only job is to be an end of the flow. §1.5 connectivity rule: logical connectivity is interface compatibility. It is a part usage typed by an item def, which violates `validatePartUsagePartDefinition`, so the construct itself is not valid SysML v2. | FINDING F-3, F-5 |
| `ToasterDemo::BreadEjector` (`part def`) | Logical, not yet built (DL-020 precedent) | Same as `BreadLoader`. The name "ejector" may commit to a pop-up mechanism (OQ-1). | FINDING F-4; OPEN-QUESTION OQ-1 |
| `ToasterDemo::BreadEjector::bread : Finish` (`PartUsage` typed by an `ItemDefinition`) | Logical by role (flow endpoint) | Same as `BreadLoader::bread`. | FINDING F-3, F-5 |
| `ToasterDemo::BreadHandling` (`part def`) | Logical arrangement (DL-021 precedent) | It composes two slots and a flow, with no specific part and no value (§1.5 logical-to-physical test; heuristic "arrangement before sizing" in DL-021). It is not part of the system of interest: no usage is typed by it. | FINDING F-4, F-6 |
| `ToasterDemo::BreadHandling::loader : BreadLoader` (`PartUsage`) | Logical (follows its type) | A slot in the arrangement. | PASS |
| `ToasterDemo::BreadHandling::ejector : BreadEjector` (`PartUsage`) | Logical (follows its type) | A slot in the arrangement. | PASS |
| `flow loader.bread to ejector.bread` (`FlowUsage` `ToasterDemo::BreadHandling::@2`, unnamed) | Logical: interconnection between components | §1.5 "Connectivity differs by layer": connectivity between structural components is interface compatibility, which is logical. The skill's logical idiom is `port def`, `interface def`, `connection`, `flow`. There are no ports. The end types (`Start`, `Finish`) are unrelated. No payload is declared, and the flow has no name. | FINDING F-5; OPEN-QUESTION OQ-2, OQ-3 |

No MoE, MoP, TPM, requirement, constraint, attribute, metadata or specialization is added in Chapter 5.

## Per-layer checklist results

**Functional**
- Chapter 5 adds no functional element.
- The only function involved, `ApplyHeat`, is the allocation source. No action exists for loading or ejecting bread, so `BreadLoader` and `BreadEjector` have no function to be responsible for (F-4).
- No MoE is added. Not applicable.

**Logical**
- *Does each mechanism have a carrier and an interface?* No. No mechanism is carried by any component: there is no `perform`, and no constraint or calc is owned by a component. `HeatingSystem` gains an allocation and nothing else (F-2).
- *Do the interfaces actually match?* This is **open**, not passed. No port or interface def exists. Recipe 5 (`port_type_mismatches`) returns `[]` only because it considers `PortUsage` ends and there are none, so the empty result is vacuous. The ends that do exist are typed by the unrelated item defs `Start` and `Finish` (F-5, OQ-3).
- *Are MoP thresholds derived?* None are added. Not applicable.
- *Are there no solution values and no results entered as choices?* PASS for the additions: none carry a value.
- *Does it read as a design space?* Partly. `BreadHandling` is a slot structure, but its slots are not typed by abstract logical defs and it carries no constraints.

**Physical**
- Chapter 5 adds no physical element: no concrete part def specializes an abstract logical def, and no value is conferred. The contract premise on this point does not hold (see below).
- The abstract-to-concrete chain does not exist in the ch05 model. The only abstract part def is `ToastingSystem`, which DL-019 makes the subject, not a layer. `HeatingSystem` is concrete and nothing specializes it. `Heater` (ch01) specializes nothing (ch01 F-2 still stands). `BreadLoader`, `BreadEjector` and `BreadHandling` are concrete and specialize nothing.

**Across layers**
- *Stopping rule* (every leaf concrete, interfaced and verified, §1.8): no leaf meets it. Not yet built.
- *Emergent result set as a default and then "verified"*: none added in Chapter 5 (the ch01 `cycleTime` defect, DL-018, is inherited unchanged).
- *Judgment recorded*: none is recorded. The one design choice Chapter 5 makes is which component is responsible for heating, and it is not presented as a judgment. Notebook 01 is titled "Concept Selection" but does no selection among alternatives (F-8).
- *Figures*: notebook 03 cell 10 renders the interconnection SVG to a temporary directory and prints its byte size. It is not shown, has no caption, and covers only `BreadHandling`, not the assembled model (F-9).

## Findings

**F-1. The allocation is declared between definitions. That does not conform to the language, and OpenSysML does not diagnose it.**
Element: `allocate ApplyHeat to HeatingSystem` (`ToasterDemo::@19`).
Check: the SysML v2 idiom table in the skill (allocation "between usages", or an `allocation def` with typed ends), and AGENTS.md §1.9 (language conformance breaks the load).
What is wrong:
- The export shows each connector end's `ReferenceSubsetting` pointing at an `ActionDefinition` and a `PartDefinition`. The KerML metamodel types `referencedFeature` as a `Feature`, and a definition is not a feature. sysml-toolkit v0.9.1 reports exactly this as an error on line 53. OpenSysML v0.9.0 loads it with `ok=True`.
- Compare G2 in `decisions/probes.md`: OpenSysML correctly rejects `perform ToastBread;` because a def is not a usage. It applies no such rule to `allocate` ends. That looks like a tool gap in the G4 family.
- The allocation has no name, so `model.query()` cannot see it, against the convention "Name allocations so `model.query()` sees them" (skill; `opensysml-query`). Notebook 02 reads it back from the JSON export instead.
- No usage of `ApplyHeat` exists anywhere in the model, so a usage-level allocation, the form the skill lists as tested, could not be written against the current model.
- The line appears unchanged in `ch06`, `ch07` and `ch08` (line 53 in each).

What I did not do: I did not change the model or file an upstream issue, and I did not add a probe row to `decisions/probes.md`.

**F-2. There is allocation without responsibility: no `perform`, and no abstract logical def to carry it.**
Element: the allocation and its target `HeatingSystem`.
Check: the logical idiom in the AGENTS.md §1.5 table (`abstract part def` with `perform action x : ActionDef`); `term-logical-component` ("modeled here as an abstract part definition that performs an action"); the skill's logical checklist, first item.
What is wrong:
- `perform_relationships` returns nothing for the whole ch05 model.
- `HeatingSystem` is concrete.
- The allocation states that heating is assigned to `HeatingSystem`, but nothing in `HeatingSystem` performs `ApplyHeat`, carries a mechanism or exposes an interface.

DL-020 already records `HeatingSystem` as "logical, not yet built". This finding records that Chapter 5, the chapter that introduces allocation, does not build it either.

What I did not do: I did not propose where `perform` or `abstract` should be introduced.

**F-3. `part bread : Start` and `part bread : Finish` type part usages by item definitions, which the language does not allow.**
Elements: `BreadLoader::bread` and `BreadEjector::bread`.
Check: language conformance (AGENTS.md §1.9).
What is wrong:
- `SysML.xmi` constraint `validatePartUsagePartDefinition` requires that at least one definition of a `PartUsage` be a `PartDefinition`. `Start` and `Finish` are `ItemDefinition`s, and the export confirms the usages are `PartUsage`s typed only by them.
- Neither OpenSysML v0.9.0 nor `sysmlv2 check` v0.9.1 reports it. That is a second undiagnosed language rule, and it should be recorded as a gap.
- The model also contradicts the tutorial's own text. Chapter 4 notebook 02 cell 1 says "Items are not parts", and cell 6 says the items "appear as part types in `BreadHandling` in Chapter 5".

What I did not do: I did not rewrite the declarations, for example as `item` or port usages.

**F-4. `BreadLoader`, `BreadEjector` and `BreadHandling` are components with no function.**
Check:
- Cross-layer traceability.
- Allocation (`term-allocation`: functions are assigned to logical components; Douglas: components group functions).
- The §1.5 boundary test *Conceptual to functional* ("Do not invent functions they have not asked for").
- The logical checklist, first item.

What is wrong:
- The functional layer has no action for loading or ejecting bread.
- Nothing is allocated to or performed by these three defs.
- They are concrete, specialize nothing, and nothing specializes them.

So the chapter adds logical structure that traces to no function, and it introduces the responsibilities "load" and "eject" without a functional statement behind them.

What I did not do: I did not propose functions or allocations for them.

**F-5. The flow is not an interface in the tutorial's sense, and its two ends carry unrelated item types.**
Element: `flow loader.bread to ejector.bread` (`BreadHandling::@2`).
Check: the logical checklist ("Do the interfaces actually match?"), the skill idiom (`port def`, `interface def`, `connection`, `flow`), and DL-023 (interface compatibility is logical and is checked as staged project conformance).
What is wrong:
- (a) No port def, port usage or interface def exists. The ends are part usages typed by item defs (F-3).
- (b) One end is typed `Start` and the other `Finish`, and neither specializes the other. Chapter 4 notebook 02 cell 5 says `Start` and `Finish` "mark the bread entering and toast exiting". Read that way, the flow says entering bread arrives at the ejector as exiting toast, and the path never passes the heating component.
- (c) The flow declares no payload item.
- (d) The flow has no name, so `model.query()` cannot see it.
- (e) Recipe 5 returns `[]` here only because there are no `PortUsage` ends. Reading that as a pass would be wrong, so this audit reports the check as **open**.

What I did not do: I did not extend `port_type_mismatches` to item-typed ends, and I did not retype the ends.

**F-6. `BreadHandling` is not part of the system of interest.**
Check: cross-layer; DL-019 and DL-021 (the whole is the subject, and its composition is the logical arrangement).
What is wrong: no usage anywhere is typed by `BreadHandling`, and `Toaster` composes only `heating` and `control`. The bread flow therefore sits outside the system whose arrangement the layers describe. Read as text, `ch06` to `ch08` still do not compose it into `Toaster`.
What I did not do: I did not add a usage.

**F-7. The chapter text contradicts the layer rules and the model.** This is documentation consistency, not a model defect.
- Notebook 01 cell 3, notebook 02 cell 3 and notebook 03 cell 7 (the same paragraph three times) call the allocation "the functional-to-physical assignment". The target is logical under DL-020, and nothing physical is involved.
- The same paragraph says the constructs "connect the functional layer (actions) to the structural layer (parts)". "Structural layer" is not a tutorial layer (§1.5).
- It also says the flow "expresses the item flow at the port level". There are no ports.
- Notebook 02 cell 0: "express which hardware component is responsible for which function". "Hardware" is physical.
- Notebook 03 cell 1: "connecting two `PartUsage` members by their item ports". There are no ports.
- `conclusion.md`: "The `allocate` statement makes explicit ... that `HeatingSystem` realizes `ApplyHeat`." AGENTS.md §1.5: "Allocation is not realization ... A concrete part def *specializes* the abstract logical part def to realize it."
- `conclusion.md`: "The interconnection SVG confirms that the structural connectivity is readable and matches the model." Under §1.7 a diagram is a view generated from the model, so it cannot confirm that it matches the model, and it is not evidence.
- Notebook 02 cell 2 cites "§7.22 (AllocationUsage)" and notebook 03 cell 6 cites "§7.23 (FlowConnectionUsage)". The skill cites 7.15.2 for allocation and 7.12 to 7.14 for flows, and the exported metaclass is `FlowUsage`. I did not verify which section numbers are right.

Reported only; no edits.

**F-8. Vocabulary lint hit, and a title that names a concept the notebook does not teach.**
- `chapters/ch05-architecture/index.md` line 13 contains "Concept Selection". `uv run python -m glossary lint` reports it as rule `concept-selection` (error; the tutorial says "selection among alternatives"). It is the only lint hit in `chapters/ch05-architecture/`.
- The notebook file is named `01-concept-selection.ipynb`. The rule's regex `\bconcept\s+selection\b` does not match the hyphenated form, so the filename, and the link target on line 13, pass the lint unnoticed.
- The notebook's content is navigation by qualified name (`model.find`, `model.get`). It contains no alternatives, no trade study and no derived measures, so it does not teach selection among alternatives (`term-selection-among-alternatives`: "choosing among alternative mechanisms by trade study against the derived measures"). Renaming the title alone would leave a title that does not match the content.

What I did not do: I did not edit the title or the filename, and I did not edit the lint rules.

**F-9. The interconnection figure is not shown and has no caption.**
Check: the cross-layer checklist's last item and AGENTS.md §1.7.
What is wrong: notebook 03 cell 10 writes `bread_handling.svg` to a `tempfile.mkdtemp()` directory and prints only its path and size. The learner never sees it, no caption states what it includes or omits, and it covers `BreadHandling` only, not the assembled model.
What I did not do: I did not render or inspect the SVG.

## Open questions (for the orchestrator to route)

**OQ-1. Does the name `BreadEjector` commit to a pop-up mechanism before any selection among alternatives?**
- Reading A, a responsibility grouping (DL-020 pattern), logical and not yet built. Loading and removing bread happen for tongs-with-a-blowtorch too: the user places and removes it. The def carries no mechanism, constraint or value.
- Reading B, a named mechanism. "Eject" is what a spring-loaded pop-up toaster does, and tongs do not eject. Under Q2 that commits to a mechanism, so the logical layer would already have chosen the pop-up branch without a recorded selection among alternatives.
- Both readings give the layer "logical". They differ on whether an unrecorded selection has been made.
- Recommended default: Reading A. Note that the name leans towards the pop-up solution, which is worth fixing when the chapter is re-derived.

**OQ-2. What does the flow from `loader.bread` to `ejector.bread` denote?**
- Reading A, a material flow of bread. Chapter 4 notebook 02 cell 5 says `Start` and `Finish` mark the bread entering and the toast exiting. On this reading the two ends should carry one item type, or related ones (for example bread, with toast as a state or a specialization), so the `Start`/`Finish` mismatch is a defect (F-5(b)). And a material path from loader to ejector that bypasses heating is incomplete.
- Reading B, event or control signals. `Start`, `Finish` and `Cancel` read like events, and Chapter 4 calls `Cancel` a signal. On this reading the flow is a control dependency and is placed on the wrong elements.
- Recommended default: Reading A. Route the naming of the items to the Chapter 4 audit (cross-chapter dependency).

**OQ-3. From which chapter does the interface-compatibility check apply, and does it cover item-typed flow ends?**
- Reading A: Chapter 5 is the first chapter that declares a connection, so under DL-023 the staged check applies from here. It should then be widened beyond `PortUsage` ends, or the chapter should use ports.
- Reading B: the connection is not declared complete, because there are no ports or interface defs, so the check stays open until a chapter introduces ports.
- Recommended default: Reading B. Report the check as open. Ask whether `port_type_mismatches` should also compare item-typed flow ends; that is a scope change to a tested helper, and it is not mine to make.

**OQ-4 (cross-chapter). Is `ApplyHeat` a functional element?**
- My classification of the allocation as "function to logical component" assumes it is.
- Functional reading: its inputs (power, duration, efficiency) and its relation (`DeliveredEnergy = power * duration * efficiency`) hold for a coil and for a blowtorch alike, so it passes the substitution test.
- Against: "efficiency" as an input, and the lack of any bread or toast flow, may make it a mechanism statement rather than a function with typed flows (`term-functional-architecture`).
- Recommended default: functional. Route to the Chapter 4 audit. If it is ruled logical, the allocation becomes logical-to-logical and F-4 and F-7 need re-reading.

## Contract premises that did not hold

1. **"Chapter 5 introduces the logical-to-physical architecture and allocation."** Holds only for allocation. Chapter 5 adds one allocation, from a function to a logical component (DL-020), declared between definitions (F-1). It adds no physical element, no realization by specialization and no logical-to-physical allocation. The chapter text calls the allocation "functional-to-physical" (F-7), which contradicts both the model and DL-020. What Chapter 5 actually introduces is function-to-component allocation and one flow between structural parts.
2. **"Logical components carry mechanisms and interfaces."** It holds as a rule (AGENTS.md §1.5, `term-logical-component`), not in the ch05 model. No component carries a mechanism, a `perform` or a port. The only interconnection is a flow between item-typed part usages (F-2, F-3, F-5).

The contract's specific checks:
- **Does `allocate ApplyHeat to HeatingSystem` go to a logical component or to a physical one?** To a logical component, by DL-020 and the absence of any value or specialization on `HeatingSystem`. It does so at definition level, which does not conform to the language (F-1).
- **Does the abstract/concrete chain exist?** No. See the physical checklist above.
- **Is `perform` used?** No, nowhere in the model (F-2).
- **Vocabulary lint:** confirmed, `index.md` line 13, rule `concept-selection` (F-8).

## Constructs that could not be classified cleanly

- `BreadLoader::bread` and `BreadEjector::bread`: they are not valid constructs (F-3), so they are classified only by role, as flow endpoints (logical).
- The allocation and the flow are relations. I classified them by the layers of their ends (cross-layer, and logical connectivity) rather than giving them a layer of their own. For the allocation, the result depends on OQ-4.
- `BreadEjector`: logical either way, but whether its name commits to a mechanism is open (OQ-1).

## Not checked, and why

- **The rendered SVG and the Chapter 5 exercise** (`exercises/ch05/exercise.ipynb`): out of scope. F-9 rests on reading the cell source.
- **Chapter 4 elements** (`ApplyHeat`, `Start`, `Finish`, `DeliveredEnergy`) and the Chapter 1 elements the additions reference: not audited; they appear only as context and in OQ-2 and OQ-4.
- **Spec version.** The metamodel facts come from the OMG 20250201 XMI vendored in the sysml-toolkit checkout, not from formal/2026-03-02, whose PDF is not in `glossary/sources/local/`. I did not confirm that the two constraints (`ReferenceSubsetting::referencedFeature` typed `Feature`, and `validatePartUsagePartDefinition`) read the same in the formal release.
- **Spec section numbers** in the notebooks (F-7, last bullet): not verified.
- **Whether OpenSysML or sysml-toolkit have issues open** for F-1 or F-3: not checked. Nothing was filed.
- **Glossary sources:** `uv run python -m glossary check` passes in this worktree (0 errors, 7 warnings). The warnings say the local source PDFs are absent, so source hashes were not verified. I relied on the glossary's recorded definitions.
- **Downstream chapters:** `ch06` to `ch08` were read as text only (the allocation, `BreadHandling` and `HeatingAssembly :> HeatingSystem` from `ch06` on). Nothing about them is a finding on those chapters.
