# Chapter 3 layer audit

Contract PASS2-008-B, 2026-09-26. Role: `.claude/agents/layer-auditor.md`. Model: claude-opus-5-5 (exact id `claude-opus-5-5[1m]`), effort high.
Branch `audit/ch03`, base commit `927f04f`.

Subject: the elements Chapter 3 adds, that is, the difference between `models/ch02-cumulative.sysml` (41 lines) and `models/ch03-cumulative.sysml` (58 lines). Both are generated fixtures and were not edited.
Method: the four-question pass and the per-layer checklist in `.claude/skills/architecture-layers/SKILL.md`, AGENTS.md §1.4 to §1.6, the glossary (`uv run python -m glossary tutorial TERM` for `moe`, `mop`, `tpm`, `requirement`, `verification`, `asserted-solution`, `behavior`, `usage`, `mechanism`, `traceability`), and the ACE rulings DL-018 to DL-023.

How the difference was established. Both fixtures were loaded with OpenSysML v0.9.0 (`load_from_content`, `strict=False`; `model.ok == True` for both, no diagnostics) and their API JSON exports were compared by (metaclass, qualified name) through `toaster.query.ApiIndex`. Nothing in ch02 is missing from ch03. The added named elements are: one `NamespaceImport` (`MeasurementReferences::*`), `RequirementUsage timely`, `PartUsage evidence` with two `SatisfyRequirementUsage`s, `VerificationCaseDefinition TimelyToastTest` (doc, subject, objective requirement, one `verify`), and `CalculationDefinition DeliveredEnergy` (three `in` parameters, one return). The rest of the added export elements are the memberships, typings and expressions those declare. Chapter 3 also moves `nominal` and `slow` above `TimelyToast` in the text; that has no semantic effect and is not audited.

Other facts confirmed by running the model (scratch scripts, not committed):
- There is **no metadata usage** in the ch03 export (no `MeasureOfEffectiveness`, `MeasureOfPerformance` or any other). No attribute, requirement or calc is tagged or named as a MoE, MoP or TPM. The same holds for every fixture ch01 to ch08: the only text match for "metadata" in `models/` is the `#verificationMethod` note in ch03's verification doc.
- `model.eval("ToasterDemo::nominal.cycleTime <= 180.0 [SI::s]")` returns `True`; the same expression for `slow` returns `False`. `nominal.cycleTime` evaluates to the `Toaster` default (120 s) and `slow.cycleTime` to its redefinition (200 s).
- A minimal model that asserts `satisfy` for a candidate whose default violates the requirement loads with `ok == True` and no diagnostics, so OpenSysML v0.9.0 does not diagnose a false satisfaction assertion. `assert not satisfy r by x;` parses and exports `isNegated: true`; both ch03 assertions have no `isNegated`.
- `DeliveredEnergy` is referenced by nothing outside its own body in ch03 (no calc usage, no binding to any candidate or requirement). `model.eval("ToasterDemo::DeliveredEnergy(800.0 [SI::W], 120.0 [SI::s], 0.7)")` returns 67200 J, as notebook 02 cell 10 states. Downstream, ch04 line 46 calls it inside `action def ApplyHeat` (observation, not audited).

Evidence read for intent: `chapters/ch03-measures/index.md`, `conclusion.md`, and every cell of notebooks `01-moe-definition`, `02-mop-candidate-eval`, `03-threshold-judgment` and `04-verification-case`. In all of that text the strings "MoE", "MoP", "TPM", "measure of", "effectiveness" and "performance" appear only in the two notebook file names (in the `index.md` links). The chapter title is "Measures of Success".

## Classification table

| Element (qualified name) | Layer | Reason | Status |
|---|---|---|---|
| Import `MeasurementReferences::*` (`ToasterDemo::@3`, `NamespaceImport`) | none | Library access for `DimensionOneValue` (D-003 workaround, noted in the model comment and notebook 02 cell 5). No engineering content. | PASS (not classified) |
| `ToasterDemo::timely` (`requirement timely : TimelyToast`) | Follows `TimelyToast` (ch02): a MoE at the functional layer or a derived MoP threshold at the logical layer, by recorded judgment | §1.5: "whether a measure is a MoE or a MoP is a modeling judgment for the case at hand"; skill example row "Toast is ready within 150 s": MoE or MoP by judgment; `term-moe`, `term-mop`. The justification is **missing** from Chapter 3. The constraint it carries compares `cycleTime`, a result entered as a choice (DL-018). | OPEN-QUESTION (OQ-1); FINDING F-1, F-2 |
| `ToasterDemo::evidence` (untyped `part` usage) | none; could not classify | It is a part usage (an occurrence in the package, beside `nominal` and `slow`) used only as a namespace for claims (notebook 01 cell 5: "a named scope that collects satisfaction claims"). It is not a system part, and it holds assertions, not analysis results (§1.4: simulations produce the evidence base). | FINDING F-4; OPEN-QUESTION (OQ-4) |
| `ToasterDemo::evidence::@0` (`assert satisfy timely by nominal`) | Cross-layer claim (requirement to candidate) | Traceability relation (`term-traceability`) whose truth rests on `nominal.cycleTime`, the `Toaster` default of 120 s. Skill across-layers check: "Is any emergent result set as an attribute default and then 'verified'?" Yes. | FINDING F-2; OPEN-QUESTION (OQ-4) |
| `ToasterDemo::evidence::@1` (`assert satisfy timely by slow`) | Cross-layer claim (requirement to candidate) | As above, and the claim is false by the model's own values (`slow.cycleTime` = 200 s; the constraint evaluates `False`). The chapter says the slow variant violates the requirement. | FINDING F-2, F-3; OPEN-QUESTION (OQ-4) |
| `ToasterDemo::TimelyToastTest` (`verification def`) | Not a layer element | DL-023 and §1.5: classify by what it tests and by tier. It tests `timely` (layer per OQ-1). Tier: language conformance only (it parses and resolves); it is never run and yields no verdict, so it is not yet evidence. The value it would measure (cycle time on a built candidate) is a TPM and an emergent result (skill example row "Measured browning time ... 118 s"). | PASS (classification); see F-4 for the missing link to the claims |
| `ToasterDemo::TimelyToastTest::@0` (doc: "timed test of three consecutive toasting cycles at nominal input power; all must complete within 180 seconds") | Part of the verification case | The means of checking that `term-mop` and §1.5 require of a MoP requirement ("the requirement needs a threshold and a means of checking it"), stated in prose. The formal `#verificationMethod` metadata is a tracked gap (toaster#19 / OpenSysML#608, cited in the model and notebook 04 cells 4 and 5). | PASS; evidence for OQ-1 |
| `ToasterDemo::TimelyToastTest::toaster` (`subject toaster : Toaster`) | none (the subject) | §1.5 and DL-019 (F7): the system of interest is the subject all layers describe, not a layer. | PASS (not classified) |
| `ToasterDemo::TimelyToastTest::@2` (objective) and `::@2::@0` (`verify timely`) | Part of the verification case | DL-023. The `verify` exports as a `SatisfyRequirementUsage` subsetting `timely` (opensysml-query recipe 4). | PASS (not classified); subject binding not checked (see below) |
| `ToasterDemo::DeliveredEnergy` (`calc def`, return `power * duration * efficiency`) | Functional by the method (recommended); contested with logical | Q1: a pop-up toaster and tongs-with-a-blowtorch both have a supplied power, a duration and a fraction of energy reaching the bread, so the relation holds for both (skill Q1: "a relation among phenomena (energy, temperature, time)"). It is not stated for a chosen component (§1.5 *Constraints, split by solution-independence*). Against: the constant-power product form is a modeling decision (`term-mechanism`), and ch04/ch05 attach it to `ApplyHeat` and `HeatingSystem`. | OPEN-QUESTION (OQ-3); FINDING F-5 |
| `ToasterDemo::DeliveredEnergy::power : ISQ::PowerValue` (`in`) | Follows the calc def | A typed, unit-bearing parameter with no value. | PASS |
| `ToasterDemo::DeliveredEnergy::duration : ISQ::DurationValue` (`in`) | Follows the calc def | As above. Notebook 02 feeds it 120 s, the `cycleTime` default (F-2, OQ-2). | PASS |
| `ToasterDemo::DeliveredEnergy::efficiency : DimensionOneValue` (`in`) | Follows the calc def | Power efficiency is the glossary's own MoP example (`term-mop`), but here it is an unbounded dimensionless input: not tagged as a measure, no threshold, no means of collection, and no `0..1` bound. | FINDING F-1, F-5; OPEN-QUESTION (OQ-2) |
| `ToasterDemo::DeliveredEnergy::@3` (return `: ISQ::EnergyValue`) | Follows the calc def; any value it yields on a candidate is an emergent result | `term-behavior`, §1.6: derived, not chosen. The one evaluated value (67 200 J, notebook 02 cell 10) is not stored in the model and is compared with nothing. | PASS (as a relation); OPEN-QUESTION (OQ-2) on whether its evaluation is a TPM |
| `AS-C03` (Python `ReviewRecord`, notebook 03 cell 5; not in the model diff) | Judgment record (not a layer element) | Skill across-layers check on judgment: `counterevidence` and `residual_uncertainties` are populated and `disposition` is "pending", not "accepted" (§1.6). Its `evidence_refs` cites the assertion `assert satisfy timely by nominal`, and its `rationale` compares the default with the limit. | PASS on the §1.6 fields; FINDING F-2, F-4 on what it cites |

## Per-layer checklist results

**Functional**
- Typed inputs and outputs on each action: no action is added in Chapter 3 (actions arrive in Chapter 4). Not yet built.
- Solution-independent statements: `DeliveredEnergy` passes the substitution test (OQ-3 records the contest). PASS by the method.
- Phenomena relations as relations (balance inequality): `DeliveredEnergy` is an equality with an unbounded efficiency, not a balance; no energy balance exists in the model. FINDING F-5.
- At least one MoE about acceptance, with any MoE-versus-MoP split justified and recorded: none. No MoE is declared or tagged, and no split is justified. FINDING F-1; OQ-1.
- Reads as an objective: the only objective content is `TimelyToast` (ch02), a threshold with no stated MoE above it.

**Logical**
- Mechanism carriers and interfaces: none added. Not yet built. Port-type conformance (§1.9, recipe 5) stays **open**: no connection exists.
- MoP thresholds derived from a MoE, with a means of checking: no MoP exists. If `timely` is read as a MoP (OQ-1), its 180 s threshold is not derived from any MoE in the model (the ch02 rationale argues it in prose) and its means of checking exists only as the `TimelyToastTest` doc. FINDING F-1 (as absent), OQ-1.
- No solution values and no results entered as choices: Chapter 3 adds no values, but every check it adds compares `cycleTime`, a result entered as a choice. FINDING F-2.
- Reads as a design space: `DeliveredEnergy`'s parameters are typed, unit-bearing slots. PASS.

**Physical**
- Concrete defs specializing abstract logical defs: none added. Not applicable.
- Values meet derived thresholds, TPM assessed not asserted: no TPM exists. The satisfaction of `timely` is **asserted** (`assert satisfy`) against default values, not assessed. FINDING F-2, F-3.
- Reads as a candidate: `nominal` and `slow` (ch02) are the candidates; Chapter 3 claims both satisfy, and one does not (F-3).

**Across layers**
- Stopping rule: not reached at Chapter 3. Not yet built.
- An emergent result set as an attribute default and then "verified": yes, this is the chapter's central check. FINDING F-2.
- Judgment recorded, with counterevidence and residual uncertainties, no "accepted" disposition: `AS-C03` has all three. PASS on form; F-4 on its evidence.
- Figures: Chapter 3 has no figure cells; not checked beyond that (see below).

## Findings

**F-1. Chapter 3 declares no MoE, MoP or TPM, although its title and two notebook names say it does, and it records no MoE-versus-MoP justification.**
Checks: functional checklist ("at least one MoE ... if a timing or efficiency figure is filed as a MoE or a MoP, is the split justified for this case and recorded?"); logical checklist (MoP thresholds derived from a MoE); `term-moe`, `term-mop`, `term-tpm`; §1.5 (the split is a judgment "recorded with its justification"); DL-022 ("Chapter 3's re-derivation carries a recorded justification").
Evidence: no metadata usage in the export; no attribute named or documented as a measure; the notebook named `01-moe-definition` adds `requirement timely` and two `assert satisfy`, and its text never mentions a measure of effectiveness; the notebook named `02-mop-candidate-eval` adds `calc def DeliveredEnergy` with no threshold, attribute or means of collection, and its text never mentions a measure of performance. The only threshold in play (180 s) comes from ch02. So the chapter's labeling is not matched by the model, and neither label is justified anywhere in the chapter. `index.md` states the chapter's question as "how do we verify that a candidate design satisfies a requirement?", which is about satisfaction claims rather than measures.
Not done: I did not propose which measures the chapter should declare, and I did not decide the split (OQ-1, OQ-2).

**F-2. Every threshold check Chapter 3 adds compares an attribute default with the limit (the pattern §1.5 says is not a valid check).**
Checks: across-layers ("Is any emergent result set as an attribute default and then 'verified'?"); §1.5 *Prescribed versus emergent*; skill example row "Cycle time = 120 s set as an attribute default, then checked against a 150 s limit: not a valid check"; DL-018.
Evidence: `assert satisfy timely by nominal` holds only because `Toaster::cycleTime` defaults to 120 s; `AS-C03`'s rationale is "120 s < 180 s", its criteria are `toaster.cycleTime <= 180.0`, and its own counterevidence says "The nominal holds only for the default cycleTime." `DeliveredEnergy` could have been part of a derivation, but it is not connected to `cycleTime`, `timely` or any candidate, and it takes duration as an input, so as declared it cannot derive a cycle time (DL-018: cycle time is derived "from the mechanism and the energy balance"). This is ch01 F-1 carried into Chapter 3's new elements: the check "can never fail for a reason about the design" (DL-018 reasoning).
Not done: no edit to the model, notebooks or record.

**F-3. The model asserts that `slow` satisfies `timely`, which its own values falsify and its own text denies, and the tool does not diagnose it.**
Checks: physical checklist (TPM assessed, not asserted); §1.6 ("behavior is derived and checked, never asserted"); §1.9 (tools may not diagnose a fault; the tutorial supplies the check).
Evidence: `ToasterDemo::evidence::@1` is `assert satisfy timely by slow`; `slow.cycleTime` is 200 s; `model.eval("ToasterDemo::slow.cycleTime <= 180.0 [SI::s]")` is `False`. `conclusion.md` line 5 says "the slow variant at 200 s violates it"; `AS-C03` counterevidence says the same. `conclusion.md` line 9 says the model "now records *which* candidate satisfies the requirement", but it records both as satisfying. `index.md` calls them "satisfaction claims for both candidates". OpenSysML v0.9.0 loads a minimal equivalent with no diagnostic. The negated form `assert not satisfy` parses in v0.9.0 (`isNegated: true`) and was not used. The same two assertions persist unchanged in ch04 to ch08 (observation only; not audited).
Not done: I did not decide whether `slow` is meant as a negative control (and so should be a negated claim or a computed check), and I did not file a gap entry (§1.9 asks for one only once it is established that the spec requires the diagnosis, which I did not check).

**F-4. Claims are labeled and cited as evidence, and the verification case is not linked to them.**
Checks: §1.4 ("Simulations produce the evidence base; judgments ... rest on that evidence and point at it. They do not replace it."); across-layers judgment check; DL-023 (a verification case's verdict is evidence).
Evidence: the claims live in a part usage named `evidence`; `AS-C03.evidence_refs` is `["assert satisfy timely by nominal"]`, so the judgment cites a model assertion, which itself rests on a default (F-2), rather than an analysis result. `TimelyToastTest` declares how `timely` would be verified but yields no verdict, and nothing connects it to the `assert satisfy` claims or to `AS-C03`. The chain from requirement to verification to evidence to judgment is not closed at any link.
Not done: no restructuring proposed; whether `evidence` is a legitimate construct is OQ-4.

**F-5. `DeliveredEnergy` is a free-standing equality with an unbounded efficiency, not a balance, and it is unused in Chapter 3.**
Checks: functional checklist ("phenomena relations stated as relations (balance inequality)"); §1.5 (the functional idiom is an energy balance "which respects conservation without assuming perfect efficiency").
Evidence: `return : ISQ::EnergyValue = power * duration * efficiency` with `efficiency : DimensionOneValue` and no constraint `0 <= efficiency <= 1`, so as declared it admits delivered energy greater than supplied energy. There is no loss term and no balance anywhere in the ch03 model. Nothing in ch03 uses the calc (ch04 does). Notebook 02 cell 1 calls it "the quantitative basis for evaluating the nominal design", but the model does not bind it to `nominal`, and the one evaluation (notebook 02 cell 10) uses Python literals, including an efficiency of 0.7 that exists nowhere in the model (§1.4: a number without a model-defined relation and inputs is not evidence).
Not done: no bound or balance added. The "unused" half is "not yet built" (ch04 uses it); the unbounded efficiency is a defect in the relation as declared.

**F-6. Chapter text disagrees with the fixture and with itself (documentation consistency, not a layer defect in the model).**
- `index.md` Ingredients row for notebook 02 says `return : Real = expr`; the fixture and notebook 02 use `ISQ::EnergyValue` and ISQ-typed inputs.
- `index.md` Experiment says "after completing all three notebooks"; the chapter has four.
- `conclusion.md` does not mention `TimelyToastTest`, which the chapter adds.
- `conclusion.md` line 9 versus the model (F-3).
- The notebook names say MoE and MoP; the notebook titles and text say requirement usage and calc def (F-1).
Reported only; no edits.

## Open questions (for the orchestrator to route)

**OQ-1. Is the toast-time measure behind `timely` (`TimelyToast`, `cycleTime <= 180 s`) a MoE or a MoP? Justification: missing.**
- MoE reading: `TimelyToast`'s rationale argues from the user ("kitchen workflows", "usability envelope for a countertop appliance"), which answers "who cares" with the user and frames time as part of acceptance. The skill's example row names toast time as a case where MoE is defensible. The notebook that adds `timely` is named `01-moe-definition`.
- MoP reading: `TimelyToastTest`'s doc checks it as engineering performance under a test condition ("at nominal input power"). The glossary's MoE example is evenness of toasting, not time. `term-mop` asks for a unit, a threshold and a means of checking, and all three exist (s, 180 s, the timed test in prose).
- Against both, as declared: the measured quantity is `cycleTime`, which is a result entered as a choice (DL-018), so whichever label is chosen the check is not yet valid (F-2). If MoP, its threshold is not derived from any MoE in the model.
- Justification present in Chapter 3: none. No text in `index.md`, `conclusion.md` or the notebooks says which it is or why; the only signal is a file name. DL-022 expects the re-derivation to carry the recorded justification.
- Recommended default: leave it unlabeled (neither MoE nor MoP) and keep `timely`'s layer open until the Chapter 3 re-derivation records the judgment (who cares; acceptance or engineering performance), per §1.5 and DL-022. Do not infer the label from the file name.

**OQ-2. What measure does notebook 02 (`02-mop-candidate-eval`) intend, and is its evaluation a TPM?**
- MoP is efficiency: `term-mop`'s own toaster example is power efficiency, and `efficiency` is an input of `DeliveredEnergy`. Against: no threshold, no attribute, no means of collection, not tagged.
- MoP is delivered energy: the notebook calls it "the quantitative basis for evaluating the nominal design". Against: no threshold, and nothing relates delivered energy to `timely` or to acceptable toast.
- The evaluation (67 200 J) is a TPM: it is a value computed by analysis from the heater's 800 W. Against: `term-tpm` is "the evidence against a MoP threshold", and there is no threshold; the inputs are Python literals not bound to a candidate; the 120 s input is a result entered as a choice; the 0.7 has no source in the model; the result is not stored in the model.
- Recommended default: record that the model has **no MoP and no TPM** in Chapter 3 (F-1), and route the intent question to the chapter's re-derivation author.

**OQ-3. Is `DeliveredEnergy` a functional phenomena relation or a logical mechanism?**
- Functional: Q1 is yes (a blowtorch also has a supplied power, a duration and a fraction reaching the bread); it is stated for no chosen component; §1.5 says a relation that holds for any solution stays functional.
- Logical: the constant-power product is a modeling decision grounded in practice (`term-mechanism`), and from ch04 it is the body of `ApplyHeat`, which ch05 allocates to `HeatingSystem`; notebook 02 evaluates it with the heater's 800 W.
- Recommended default: **functional as declared in Chapter 3** (the method stops at Q1), with F-5 open against it because it is not a balance. Whether its use inside `ApplyHeat` from ch04 is logical belongs to the Chapter 4 and 5 audits.

**OQ-4. What are `part evidence` and its `assert satisfy` claims in layer terms?**
- Analysis side, not a layer element: they record the outcome of a check, like a verification case (DL-023 by analogy). Against: DL-023 rules on `verification def`, not on `satisfy`, and an `assert satisfy` is a claim, not an analysis.
- Cross-layer traceability relation: a satisfy links a requirement to the design element that meets it (`term-traceability`, Douglas: "the design traces back to the requirements it implements"), so it takes no layer of its own. Against: that does not settle what the container `part evidence` is; as a part usage it is an occurrence in the package, not a namespace.
- Recommended default: classify each `assert satisfy` as a cross-layer traceability claim (no layer of its own), treat `part evidence` as unclassifiable, and ask the ACE whether DL-023 extends to satisfaction claims and whether a part usage is an acceptable container for them.

## Contract premises that did not hold

1. **"Chapter 3 introduces measures of effectiveness and performance."** Not at HEAD. The model has no MoE or MoP (no metadata, no measure attribute, no new threshold), and the chapter text never uses either term except in two notebook file names. See F-1.
2. **"Its threshold checks compare a derived value rather than an attribute default."** Does not hold. The only threshold check (`timely` via `assert satisfy ... by nominal` and `by slow`, and `AS-C03`'s rationale) compares `cycleTime`, which is a `Toaster` default (120 s) or a redefinition (200 s). The one derived value in the chapter (67 200 J) is compared with nothing. See F-2.
3. **"TPM values come from analysis."** Does not hold, because there is no TPM. Nothing in the model is an assessed value; the values the checks use are prescribed defaults, and the one analysis output is not in the model and not against a threshold. See OQ-2.

The contract's context statement "Lint hits for this chapter: none" holds: `uv run python -m glossary lint --json` reports hits only in ch01, ch05, ch09 and ch10 files.

## Constructs that could not be classified cleanly

- `ToasterDemo::evidence`: an untyped part usage used as a namespace for claims (OQ-4).
- The two `assert satisfy` usages: relations whose layer is that of the requirement they cite, which is itself open (OQ-1, OQ-4).
- `ToasterDemo::timely`: its layer depends on a MoE-versus-MoP judgment that has not been recorded (OQ-1).
- `DeliveredEnergy`: classified by the method (functional), but contested (OQ-3).

## Cross-chapter dependencies

- `TimelyToast` is a Chapter 2 element. Its layer decides `timely`'s (OQ-1). There is no `ch02-layer-audit.md` in this checkout, so I do not know whether it has been classified.
- F-2 is ch01 F-1 (DL-018) carried forward: it closes only when `cycleTime` is derived rather than defaulted.
- `DeliveredEnergy` is used from ch04 (`ApplyHeat`, line 46) and, through ch05, sits under `HeatingSystem`'s allocation (OQ-3).
- `assert satisfy timely by slow` persists unchanged through ch08 (F-3). ch06 adds a similar block, carried through ch08, (`heatingEvidence { assert satisfy heating by efficient; assert satisfy heating by weak; }`) that may repeat the pattern; I did not evaluate it.
- No fixture ch01 to ch08 carries MoE or MoP metadata, so if F-1 is resolved in Chapter 3, later chapters are affected.

## Not checked, and why

- **Subject binding of `verify timely`**: the export shows the objective's `SatisfyRequirementUsage` with no `subject`. I did not check against §7.24 whether the objective's requirement binds to the case's `toaster` subject by default, so I make no claim either way.
- **Whether SysML v2 requires a tool to diagnose a false `assert satisfy`**: not checked against the spec; F-3 reports only the observed behavior of OpenSysML v0.9.0.
- **Library type names of the calc parameters**: the export gives library types as bare UUIDs that the index cannot resolve to names. I relied on the source text (`ISQ::PowerValue`, `ISQ::DurationValue`, `DimensionOneValue`, `ISQ::EnergyValue`) and on the model loading with `ok == True`.
- **`AS-C03`**: read in notebook 03 cell 5 only; I did not run `validate_record` or check assumption `AC-001`.
- **`exercises/ch03/exercise.ipynb`**: not in scope.
- **Figures**: Chapter 3 has no figure cells; the across-layers figures check does not apply.
- **Seam-cell labels**: notebooks 01, 02, 03 and 04 end with cells using the A-F, O-S and E labels. DL-028 parks those as a Pass 4 input; I did not assess them.
- **Later chapters**: read only to trace Chapter 3 elements downstream; not audited.
- **Glossary sources**: `uv run python -m glossary check` passes (0 errors, 7 warnings: local source PDFs absent, hashes not verified). I relied on the glossary's recorded definitions, not on the source texts.
