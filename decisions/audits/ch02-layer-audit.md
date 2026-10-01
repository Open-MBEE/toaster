# Chapter 2 layer audit

Contract PASS2-008-A, 2026-09-26. Role: `.claude/agents/layer-auditor.md`. Model: claude-opus-5-5 (effort high).
Branch `audit/ch02`, base commit `927f04f`.

Subject: the elements Chapter 2 adds, that is, the diff from `models/ch01-cumulative.sysml` (25 lines) to `models/ch02-cumulative.sysml` (41 lines). Both are generated fixtures and were not edited. The diff is `requirement def TimelyToast` (lines 27 to 36), `part nominal : Toaster` (line 38) and `part slow : Toaster { attribute :>> cycleTime = 200.0 [SI::s]; }` (lines 39 to 41), plus a changed header comment. The chapter also adds one Python judgment record, `context_record` (AC-001, notebook 03 cell 5). It is not a model element, but it is audited below because it makes claims about a model element's value.

Method: the four-question pass and the per-layer checklist in `.claude/skills/architecture-layers/SKILL.md`, AGENTS.md §1.5 and §1.6, and the glossary (`uv run python -m glossary tutorial TERM`). The established calls are DL-018 (cycle time default is a result entered as a choice), DL-019 and DL-021 (the system of interest is the subject, not a layer), DL-020 (`HeatingSystem`, `ControlSystem` logical, not yet built), DL-022 (no timer setpoint; MoE versus MoP for toast timing deferred to Chapter 3 with a recorded justification), DL-023 (a verification case is not a layer element) and DL-017 (MoE versus MoP is a justified judgment). They are applied and not reopened.

Model evidence: both fixtures load with OpenSysML v0.9.0 (`load_from_content`, `strict=False`, `model.ok == True`, no diagnostics). From the API JSON export (`toaster.query.api_elements`):
- `TimelyToast` is a `RequirementDefinition` with one `Documentation`, a `SubjectMembership` owning `TimelyToast::toaster` (a `ReferenceUsage`, `direction: in`, typed by `Toaster`), and a `RequirementConstraintMembership` owning a `ConstraintUsage` whose result is an `OperatorExpression` `<=` with a `LiteralRational` 180.0.
- `nominal` and `slow` are `PartUsage`s typed by `Toaster`. `nominal` has no owned members; its only attribute (`Symbol.attributes()`) is the inherited `Toaster::cycleTime`.
- `slow::@0` is an anonymous `AttributeUsage` with a `Redefinition` of `Toaster::cycleTime` and a `FeatureValue` with no `isDefault` flag (a fixed binding, where `Toaster::cycleTime` and `Heater::power` have `isDefault: true`), bound to a `LiteralRational` 200.0.
- There are still exactly two `Subclassification`s (`HeatingSystem` and `ControlSystem` to `ToastingSystem`), and no `FeatureTyping` or `Subclassification` targets `Heater`.

Evidence read for intent: `chapters/ch02-requirements/index.md`, `conclusion.md`, and every cell of notebooks `01` to `03`. `models/ch03` to `ch08-cumulative.sysml` were read only to see how Chapter 2 elements are used downstream, not audited. The vocabulary lint (`uv run python -m glossary lint`) reports 8 hits in the repository and none in `chapters/ch02-requirements/`.

As in the Chapter 1 audit, the status column separates two kinds of "no" on the checklist: **wrong** (the model says something the layer rules forbid) and **not yet built** (expected to fail at this point). Identifiers continue from the Chapter 1 audit (F-1 to F-4, OQ-1 to OQ-5) so that they do not collide in the decision log.

## Classification table

| Element (qualified name) | Layer | Reason | Status |
|---|---|---|---|
| `ToasterDemo::TimelyToast` (`requirement def`) | Functional (recommended), MoE or MoP by judgment | Q1: "complete a toasting cycle in at most 180 seconds" is met or missed by a pop-up toaster and by tongs-with-a-blowtorch alike (§1.5 substitution test). A requirement definition defines a constraint that a valid solution must satisfy (`term-requirement`, SysML). The skill's example row "Toast is ready within 150 s" says MoE or MoP by judgment (DL-017). The element carries no MoE or MoP tag, and no justification for either is recorded. | OPEN-QUESTION (OQ-6) |
| `TimelyToast` doc, description ("The toaster shall complete a toasting cycle in at most 180 seconds.") | Functional | Solution-independent statement of need, anatomy part 1 (`def-douglas--requirement`). "Toaster" names the subject, not a mechanism. | PASS |
| `TimelyToast` doc, rationale ("kitchen workflows ... usability envelope for a countertop appliance") | Functional (justification of an acceptance threshold) | Anatomy part 2 (`def-douglas--requirement`). It argues from the user's kitchen workflow, which points to acceptance (who cares: the user). "Countertop appliance" names a class of solution; see OQ-6. It is a judgment about a threshold, recorded without counterevidence or residual uncertainties. | FINDING F-7 (judgment not recorded as one) |
| `TimelyToast::toaster` (`subject`, `ReferenceUsage`, `in`, typed by `Toaster`) | None (the subject) | The system of interest is the subject the layers describe, not a layer (§1.5; DL-019, DL-021). A requirement's subject parameter typed by it is that subject. | PASS (not classified) |
| `TimelyToast::@2` (`require constraint { toaster.cycleTime <= 180.0 [SI::s] }`) | Follows the requirement (functional by default, logical if OQ-6 reads it as a MoP threshold) | A unit-bearing threshold on a quantity is a requirement at the layer that states it (§1.5 *Numbers*). Constraining an emergent result (Q4: a cycle time) against a threshold is the right direction. What is wrong sits on the other side of the inequality: every `Toaster` the chapter supplies gets its `cycleTime` as an entered value (F-1, DL-018), so the comparison is between chosen numbers. | PASS for the constraint form; FINDING F-5 for the check it takes part in |
| Third part of the anatomy, a verification method | Not present | The anatomy has three parts (`def-douglas--requirement`; AGENTS.md Part 2 §1, Part 4: "A requirement without all three is incomplete"). Chapter 2 defers it to Chapter 3 (notebook 01 cell 1; `TimelyToastTest` in `ch03-cumulative.sysml`). A verification case is not a layer element (DL-023). | Not yet built (see premise 1) |
| `ToasterDemo::nominal : Toaster` (`part` usage) | Not settled by the four questions. Recommended: a named usage of the subject, not a layer element | Q1: a part, not a statement of intent. Q2: it commits to nothing beyond `Toaster`'s arrangement. Q3: it names no concrete part def and gives no value. Its only attribute value is the inherited 120 s `cycleTime` default, an emergent result (Q4, DL-018). The chapter calls it "the baseline design candidate" (notebook 01 cell 7). | OPEN-QUESTION (OQ-7); FINDING F-6 |
| `ToasterDemo::slow : Toaster` (`part` usage) | As `nominal` | As `nominal`, except that it redefines one attribute (next row). The chapter calls it a design variant, a design candidate, an operating condition and an assumption (F-8). | OPEN-QUESTION (OQ-7, OQ-8); FINDING F-6 |
| `ToasterDemo::slow::cycleTime` (anonymous `attribute :>> cycleTime = 200.0 [SI::s]`; `Redefinition` of `Toaster::cycleTime`; non-default `FeatureValue`) | Emergent result | Q4: a cycle time is a result the design is expected to produce (§1.5 prescribed-versus-emergent test; `term-behavior`). Here it is bound to a fixed value, a stronger form of entering a result as a choice than Chapter 1's default. | FINDING F-5 |
| `context_record` (AC-001, Python `ReviewRecord`, `kind="asserted_context"`; not in the model) | None recommended (analysis and evidence side) | It is a judgment record, not a prescription or an intent. DL-023 rules only on verification cases, so extending it to judgment records is my analogy (OQ-10). Its claim is about an emergent result (the 120 s cycle time), and its evidence is the declared default (F-7). `counterevidence` and `residual_uncertainties` are filled in, and `disposition="pending"` (§1.6 and SA-7 satisfied). `validate_record` returns `[]`. | OPEN-QUESTION (OQ-9, OQ-10); FINDING F-7 |
| Header comment (line 3, "chapter 2's construct-introducing notebooks") | None | Provenance comment, no engineering content. | PASS (not classified) |

## Per-layer checklist results (Chapter 2 additions only)

**Functional**
- Typed inputs and outputs on each action: Chapter 2 adds no actions. Not yet built (Chapter 4).
- Solution-independent statements: the `TimelyToast` description passes the substitution test. PASS. The rationale's "countertop appliance" names a solution class (OQ-6).
- Phenomena relations stated as relations: none added. Not yet built.
- At least one MoE about acceptance, and a recorded MoE or MoP split for a timing figure: `TimelyToast` is the first acceptance-like threshold, but it is not tagged and no MoE or MoP justification is recorded. The glossary requires a MoE to have "a unit and a means of collecting data" (`term-moe`). The unit is present; the means of collection is not (it arrives with `TimelyToastTest` in Chapter 3). DL-022 already assigns the recorded justification to Chapter 3's re-derivation, so this is **not yet built**, not wrong (OQ-6).
- Reads as an objective: yes, "good enough" is stated as a bound (at most 180 s).

**Logical**
- Mechanism carriers and matching interfaces: nothing added. Port-type conformance (§1.9, `opensysml-query` recipe 5) stays **open**, since no connection is declared.
- MoP thresholds derived from a MoE with a means of checking: if OQ-6 reads `TimelyToast` as a MoP threshold, it fails this item. 180 s is justified by a workflow argument and not derived from a stated MoE, and there is no means of checking in Chapter 2. Under the recommended functional reading the item does not apply.
- No solution values and no results entered as choices: `slow` binds a cycle time (F-5). `nominal` carries the 120 s default from `Toaster` (F-1, unchanged).
- Reads as a design space: Chapter 2 adds no slots, only a constraint and two usages.

**Physical**
- Each part is a concrete def specializing an abstract logical def and fitting its interfaces: `nominal` and `slow` are the only new parts. Both are typed by `Toaster`, the subject (DL-021), and contain only the logical slots `heating : HeatingSystem` and `control : ControlSystem` (DL-020). Neither contains or redefines a concrete part. `Heater` is still unused (F-2 unchanged). FINDING F-6.
- Values meet derived thresholds and TPMs are assessed, not asserted: the only candidate values are cycle times, which are asserted (a default and a binding), not assessed. `conclusion.md` line 9 reports that one passes and one fails. FINDING F-5.
- Reads as a candidate: no. A candidate is a concrete point checked for feasibility against the logical layer (§1.10 lens), and these have no physical content (F-6).

**Across layers**
- Stopping rule (§1.8): no leaf meets it. Expected; not yet built.
- An emergent result set as an attribute value and then "verified": yes. This is the Chapter 1 F-1 pattern completed. Chapter 1 set the default. Chapter 2 adds the threshold (`TimelyToast`), a second entered value (`slow`, 200 s, fixed), and a pass/fail verdict in prose (`conclusion.md` line 9). Chapter 3 formalizes it as `assert satisfy timely by nominal; assert satisfy timely by slow;` (`ch03-cumulative.sysml`, observed only). FINDING F-5.
- Judgment recorded where exercised, with counterevidence and residual uncertainties, and no "accepted" disposition: judgment is exercised twice. AC-001 records the 120 s assumption with counterevidence, residual uncertainties and a `pending` disposition (PASS on the fields), but its evidence is the default it justifies (F-7). The 180 s threshold has a rationale only (F-7).
- Figures show the assembled model: Chapter 2 has no figure. Notebook 03 cell 2 prints the whole model text instead. FINDING F-9 (content, not a layer defect).
- Traceability (observed, no finding): `TimelyToast`'s subject is `Toaster`. The purpose statement it serves ("toast acceptable to its user") sits on `ToastingSystem`, which `Toaster` does not specialize (F-3), so nothing in the model links the timing requirement to the purpose. Its parent would be a stakeholder need, and the conceptual layer is out of scope (§1.1), so this is reported and not raised.

## Findings

**F-5. Chapter 1's F-1 recurs and is extended: Chapter 2 checks entered cycle times against a threshold and reports verdicts (wrong).**
Check: prescribed versus emergent (AGENTS.md §1.5 boundary tests; §1.6 "behavior is derived and checked, never asserted"); the skill's example row "Cycle time = 120 s set as an attribute default, then checked against a 150 s limit: Not a valid check"; DL-018.
- `slow` adds `attribute :>> cycleTime = 200.0 [SI::s]`. The export shows a `FeatureValue` with no `isDefault` flag, so this is a fixed binding. Notebook 02 cell 5 says so: "`:>>` sets a fixed value".
- `nominal` takes its cycle time from `Toaster`'s 120 s default (F-1).
- `TimelyToast` constrains `toaster.cycleTime <= 180.0 [SI::s]`.
- `conclusion.md` line 9: "One passes (120 seconds is within the 180-second bound), one fails (200 seconds is not)." No analysis produced either number, and no computation of the verdict appears in the notebooks. The verdicts compare chosen numbers with a limit, so they would hold whatever the design is (DL-018's reasoning).
- Notebook 01 cell 5 says the constraint is "evaluated against concrete `Toaster` instances".
DL-018 already rules on the pattern, so this is not a new call. What is new in Chapter 2 is the fixed binding and a verdict stated in prose. I changed nothing.

**F-6. The design candidates have no physical content; Chapter 1's F-2 recurs in a new form (wrong if they are candidates; see OQ-7).**
Check: physical checklist, first two items; §1.5 *Allocation is not realization*; `term-physical-architecture` ("concrete parts that realize the logical components and confer values"). `nominal` and `slow` are usages of the subject def `Toaster` (DL-021), whose composition is the logical slots `heating : HeatingSystem` and `control : ControlSystem` (DL-020). Neither usage contains, redefines or types a part by a concrete def. `Heater`, the only part def with a part value (800 W), is still used nowhere (export: no `FeatureTyping` targets it). The only thing that distinguishes `slow` from `nominal` is the value of an emergent result. The chapter nevertheless calls them "design candidates" (notebook 01 cell 7, notebook 02 cell 3). Observed downstream: through `ch08-cumulative.sysml` both stay `part nominal : Toaster;` and `part slow : Toaster { attribute :>> cycleTime = 200.0 [SI::s]; }`, and they are the `satisfy` subjects from Chapter 3 onward, so the gap does not close by itself. I did not fix it.

**F-7. Judgment is recorded, but the one record cites as evidence the prescription it justifies, and the threshold judgment has no record (wrong for AC-001; a gap for the threshold).**
Check: cross-layer judgment item; §1.6; `term-asserted-context`, `term-assumption` (context enters an argument asserted to be appropriate).
- AC-001: `claim` is "120 seconds is the nominal cycle time for standard sliced bread". `criteria` is the declaration `attribute cycleTime : ISQ::DurationValue default = 120.0 [SI::s]`, and `evidence_refs` is `["ToasterDemo::Toaster::cycleTime default = 120.0 [SI::s]"]`. The only evidence offered for the value is the model's own declaration of that value. The rationale ("consistent with manufacturer guidance") cites no source. The claim also mixes a context (standard sliced bread, an operating condition) with a result (the cycle time under that condition). The fields §1.6 calls load-bearing are present: counterevidence "Thick-cut and frozen bread may require 180-240s" (which already exceeds the 180 s threshold), residual uncertainties, and disposition `pending`.
- `TimelyToast`'s 180 s threshold is a judgment, and it is recorded only as a `doc` rationale ("kitchen workflows typically span 5-15 minutes"), with no source, counterevidence or residual uncertainty. Whether a requirement's rationale needs a judgment record is not stated anywhere I read, so this half is a gap reported against the checklist, not a ruling.
I did not edit the record or the requirement.

**F-8. Chapter text disagrees with itself and with the model about what `slow` is and what a requirement definition binds (documentation consistency; not a layer defect in the model).**
- `slow` is called "two named design variants" (`index.md` Purpose and Method; `conclusion.md` line 5), "the operating conditions we are designing for ... encoding the assumption being evaluated" (notebook 02 cell 1), "a named design candidate ... that encodes a specific assumption about cycle time" (notebook 02 cell 3), and "two competing conditions to evaluate" (`conclusion.md` line 9). A prescription (candidate), a context (operating condition) and a result (cycle time) are different kinds (OQ-8).
- Notebook 01 cell 3: "any `Toaster` instance must satisfy this requirement". A requirement definition defines a constraint on its subject parameter (`def-sysml--requirement`). It binds a particular `Toaster` only through a requirement usage and a satisfy relationship, which is what Chapter 3 introduces. As written, the sentence also makes `slow`, a `Toaster` built to fail, a contradiction.
- `index.md` Method: "Notebook 02 adds the `nominal` and `slow` variants". `nominal` is added in notebook 01 (cell 6).
- Notebook 02 cell 5 attributes fixity to `:>>` ("`:>>` sets a fixed value, while `default =` sets a value that can be further overridden"). In the export, the redefinition (`:>>`) and the fixed binding (`=`, a non-default `FeatureValue`) are separate elements. The sentence merges them. This is outside layer scope and is reported for routing only.
- Notebook 01 cell 4 ("require constraint body not yet supported — toaster#11 / OpenSysML#597") and notebook 02 cell 4 ("anonymous attribute :>> redefinition not yet supported — toaster#10 / OpenSysML#596"): v0.9.0 parses both, and the export contains the `RequirementConstraintMembership` and the `Redefinition`. As with Chapter 1's F-4, the comments may refer to the editor API rather than parsing. Not checked.
Reported only; no edits.

**F-9. Chapter 2 shows no figure of the assembled model (content; not a layer defect).**
Check: cross-layer figures item; AGENTS.md §1.7 ("every chapter shows the assembled model"). The three notebooks have no diagram cell. Notebook 03 cell 2 prints the full model source. Whether printed text meets §1.7 is for the content pass. The Chapter 1 audit did not check figures, so I cannot say whether this is a pattern.

## Open questions (for the orchestrator to route)

**OQ-6. Is `TimelyToast` a MoE-type acceptance threshold (functional) or a MoP threshold (logical)?**
- Functional reading: it passes the substitution test (tongs-with-a-blowtorch can finish or fail to finish toast within 180 s). The rationale argues from the user's kitchen workflow and meal preparation, which is acceptance (who cares: the user). Nothing derives 180 s from another measure. The requirement sits on the whole, the subject.
- Logical reading: the skill says timing is "usually performance". SEBoK's MoP "yields design requirements necessary to satisfy a MoE" (`def-sebok--mop`), and "within the usability envelope for a countertop appliance" reads like a design envelope. "Countertop appliance" in the rationale excludes the tongs-with-a-blowtorch solution, so the justification (not the statement) assumes a solution class. Observed downstream, Chapter 3's verification method tests "at nominal input power", which presupposes an electrical mechanism.
- Recommended default: **functional (MoE-type acceptance threshold)**, not yet built (no tag, no means of collection until Chapter 3). The justification is recorded in Chapter 3 as DL-022 already directs. Separately, the ACE may want to say whether "countertop appliance" in a rationale is a solution commitment. I recommend treating it as stakeholder context, not a commitment, but I do not decide it.

**OQ-7. What layer are `nominal` and `slow`: physical candidates not yet built, or named usages of the subject (no layer)?**
- Physical (candidate) reading: the chapter calls them design candidates. From Chapter 3 on they are the `by` side of `assert satisfy`, the role a candidate plays. Under the §1.10 lens a candidate is a concrete point, and each is a single usage.
- Subject-usage reading: Q3 fails. They name no concrete part def and confer no part value (F-6). Their only content is `Toaster`'s arrangement, which DL-021 rules logical, and an emergent result. DL-019 and DL-021 rule the bare system-level def to be the named subject, and a usage that adds nothing but a name is its instance.
- Recommended default: **named usages of the subject, not layer elements**, with the "candidate" label unsupported until they contain concrete parts that realize the logical slots (F-6). This extends DL-019 and DL-021 from the def to its usages. The ACE should say whether that extension holds.

**OQ-8. What does `slow` denote: a design candidate, an operating condition, or a fixture for the failing branch of a check?**
- Candidate: `index.md` and `conclusion.md` ("design variants"); notebook 02 cell 3.
- Operating condition or assumption: notebook 02 cell 1 ("the operating conditions we are designing for ... encoding the assumption"); `conclusion.md` ("competing conditions"). Against this reading, a cycle time is a result, not an environmental condition (`term-assumption` concerns context entering an argument). AC-001's own counterevidence names the actual condition, bread thickness and whether it is frozen.
- Failing-branch fixture: notebook 01 cell 7 says `slow` exists "to demonstrate a candidate that fails the requirement", which is a negative-control role (§1.4, every chapter's loop has a negative control).
- Recommended default: **a fixture for the failing branch**, whose content is F-5 whatever it is called. If the re-derivation wants an operating-condition variant, the condition (bread thickness, supply voltage, starting temperature) is what varies, and the cycle time is derived under it. That is a content decision to route, not mine.

**OQ-9. Can an explicitly recorded assumption stand in for an emergent result until the result can be derived?**
- Yes: §1.6 says real design rests on assumptions. Hawkins lets context and assumptions enter an argument when asserted to be appropriate (`term-assumption`, `term-asserted-context`). AC-001 records counterevidence and residual uncertainty with a `pending` disposition, so it is honest about being an assumption.
- No, not as used here: DL-018 says cycle time is derived from the mechanism and the energy balance, and the attribute may exist as a slot without a default. AC-001's evidence is the default itself (F-7). `conclusion.md` then uses the assumed value to issue a pass verdict as though it had been derived (F-5).
- Recommended default: **an assumption about a result is legitimate only when it stays an assumption**: recorded, pointing at evidence other than the model's own declaration, and never compared with the threshold as if it were a derived value. On that default AC-001 does not cure F-5. This may extend DL-018 (from the attribute to judgment records about it), so the ACE should confirm.

**OQ-10. Is a judgment record (`ReviewRecord`) a layer element?**
- Not a layer element: it is analysis and evidence, like a verification case (DL-023, F4). It prescribes nothing and states no intent.
- Layer element: it carries a claim about a model value (120 s), and an assumption can shape the design space.
- Recommended default: **not a layer element**, classified by what it bears on (here an emergent result of the subject). DL-023 covers verification cases only, so this is an analogy the ACE should confirm or reject.

## Contract premises checked

1. **"Chapter 2 introduces requirements with the three-part anatomy."** Holds in part. The anatomy is taught (notebook 01 cell 1, "inspired by Brian Douglas, Part 4"). `TimelyToast` has the description and the rationale, both in one unstructured `doc` comment and separable only by the "Rationale:" prefix, so no query can tell them apart. The third part, the verification method, is not in Chapter 2. It is deferred to Chapter 3's `verification def TimelyToastTest`, where the method type ("test") is also only in a `doc` because the `VerificationMethodKind` metadata is unsupported (D-004, toaster#19; DL-005). By the anatomy's own rule ("A requirement without all three is incomplete", AGENTS.md Part 2 §1), the model's only requirement is incomplete at the end of Chapter 2. DL-005 records why: `verify` must target a requirement usage, which Chapter 3 introduces.
2. **"The Ch1 findings recur or not."**
   - F-1 (settable performance attributes): **recurs and is extended** (F-5). There is a new fixed binding on `slow` and a prose pass/fail verdict.
   - F-2 (unrealized physical parts): **recurs in a new form** (F-6). The new "candidates" contain no concrete part, and `Heater` is still unused.
   - F-3 (purpose on the subsystems): **does not recur**. Chapter 2 adds nothing that touches the `Subclassification`s, and its requirement is on the whole (`Toaster`), which is consistent with the subject reading. F-3 is unchanged, and it is why `TimelyToast` cannot be linked to the purpose statement (traceability note above).
   - F-4 (documentation consistency): **recurs in a new form** (F-8).
3. **"Vocabulary lint hits for this chapter: none."** Holds. `uv run python -m glossary lint` reports 8 hits, in ch01, ch05, ch09 and ch10, and none in `chapters/ch02-requirements/`.
4. **Context premise "a verification case is not a layer element (DL-023)"**: Chapter 2 adds no verification case, so it is not exercised. It holds for the downstream `TimelyToastTest`, which was observed but not audited.

## Constructs that could not be classified cleanly

- `nominal` and `slow`: part usages of the subject that add no part and no part value. The four questions do not settle them (OQ-7, OQ-8).
- `TimelyToast` and its constraint: classified functional by default, but the layer depends on a MoE or MoP judgment that is not recorded (OQ-6).
- `context_record` (AC-001): not a model element. Its classification rests on an analogy with DL-023 (OQ-10).
- The header comment: no engineering content.

## Not checked, and why

- **Notebook execution**: I loaded the fixtures directly and did not run the notebooks. I rebuilt AC-001 with the notebook's field values and ran `validate_record` on it (`[]`). I did not confirm that the notebooks' outputs match. They are stored without outputs.
- **Constraint target in the export**: the constraint's feature chain has a `FeatureReferenceExpression` whose `referent` id (`0c539f7c-...`) is not an element of the export. A separate `Membership` does name `ToasterDemo::Toaster::cycleTime`. So I confirmed from the text, not by following the chain in the export, that the constraint reads `Toaster::cycleTime`.
- **Query-surface disagreement (tool observation, not a layer finding)**: `model.query()` filtered on `PartUsage` returns `ToasterDemo::TimelyToast::toaster`, while the JSON export gives that element as a `ReferenceUsage`. I did not check which one the spec requires or whether a gap entry exists (§1.9 gap-tracking rule, for the orchestrator to route).
- **`exercises/ch02/exercise.ipynb`**: out of scope.
- **toaster#10 / OpenSysML#596 and toaster#11 / OpenSysML#597** (notebook comments): not checked (F-8).
- **Later chapters**: read only to see how Chapter 2 elements are used downstream. The statements about `ch03` to `ch08` are observations, not findings on those chapters. One downstream observation the orchestrator may want to route to the Chapter 3 audit: `ch03-cumulative.sysml` has `assert satisfy timely by slow;` although `slow` is built to violate `timely`.
- **Glossary sources**: `uv run python -m glossary check` passes (0 errors, 7 warnings). Source PDFs are not local, so source hashes are not verified. I relied on the glossary's recorded definitions.
- **Douglas timestamps**: not re-verified.
