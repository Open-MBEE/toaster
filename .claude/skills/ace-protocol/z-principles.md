# Z's principles, frameworks and heuristics (DRAFT for Z's confirmation)

The ACE decides from these, not from quotations. Each entry gives the principle, why it holds, a test the ACE can apply, and when it stops determining the answer (the cue to escalate). The statements Z has made in conversation (`z-model.md`) are **provenance**: they are where a principle was drawn from and evidence of how Z applies it. They are not authority for a case they do not address.

Status: confirmed by Z on 2026-09-26 (F1 to F6, P1 to P6, the heuristics; F7 added from Z's answer the same day). Extracted from Z's statements and decisions. Only Z confirms or changes this list.

## Frameworks (how Z reads a situation)

**F1. Prescribed versus emergent.** A design prescribes elements, relationships and principles; behavior is what results, and is derived and checked against intent. *Test:* is this something the design chooses, or something expected to follow from the choices? A result entered as a choice cannot be checked, so it is a defect. *Underdetermined when:* a value is genuinely a chosen control parameter that also influences a result (a setpoint): the parameter is prescribed, the result is not, and the modeler decides which is which.

**F2. Objective, design space, candidate (optimization reading of the layers).** Functional says what is good and what is good enough (the objective). Logical is a typed design space with constraints and no solution values. Physical is a candidate, checked for feasibility against the logical layer and for utility against the functional layer. *Test:* what does this element read as: an objective, a slot or constraint, or a candidate value? *Underdetermined when:* an element mixes them (a slot carrying a value, a purpose carried by a construct): classify the parts separately and report the mix.

**F3. Function, mechanism, policy.** A function is solution-independent (two or more different mechanisms could provide it). A mechanism is a modeling decision grounded in engineering practice, a law we reason with, comparatively deterministic. A policy selects inputs given state, designed given the mechanisms available. *Test:* substitution (would a pop-up toaster and tongs with a blowtorch both satisfy it?).

**F4. Declarative model, procedural analysis, evidence.** The model states intent and semantics; scientific Python analyzes it; simulation and analysis produce the evidence that supports judgments. *Test:* is a number, unit or relation defined in the model, or only in code? Code that defines meaning is a defect. A verification case is analysis, not a layer element: classify it by what it tests and by its tier (confirmed by Z, 2026-09-26).

**F5. Kinds of definition, not rivals.** SEBoK supplies the idea, the OMG specs the formal and checkable semantics, Douglas the analogy and story. Tutorial definitions refine canonical ones and never contradict or invent. *Test:* does it narrow or clarify a canonical edge, and which kind of definition is being asked for?

**F6. Two tiers of conformance.** Language conformance is always on and breaks the load. Project conformance checks are staged because the model emerges iteratively; each has a negative control and is reported open until applied. *Test:* is this rule part of the language, or a project check whose time has not come?

**F7. The system of interest is the subject, not a layer.** The system-of-interest is what the functional, logical and physical layers each describe. Its purpose statement is functional; its parts and arrangement are logical; its realized parts are physical. A bare top-level part def that only names the whole is the named subject, and the layer of each piece comes from what that piece commits to. *Test:* is this element the subject itself, or a piece of it? Classify the pieces, not the subject. (Confirmed by Z, 2026-09-26.)

## Principles (what Z holds to)

**P1. Judgment is never eliminated; it is made rigorous.** Engineers make contextual, evidence-informed calls with recorded justification, and never present a check as proof. *Test:* is the judgment site identified, the evidence cited, the residual uncertainty stated?

**P2. Contextual splits are justified, not fixed.** Where a classification depends on context (MoE versus MoP, function versus mechanism), require the case-specific justification; do not apply a fixed rule. *Test:* would the opposite filing be defensible for this case, and is the reason recorded?

**P3. Teach through the model, and through views of it.** What the learner sees is derived from the model (diagrams are queries plus judged inclusion and exclusion, recorded). *Test:* could this figure or claim be regenerated from the model, and is what it omits stated?

**P4. Earn your place; keep it small.** Added content, vocabulary or lens language must make the learner's task easier, and is never load-bearing. Builder-facing lenses never appear in learner content. *Test:* if removed, does understanding get harder?

**P5. Do not paper over.** Gaps are tracked (register, drafted issue with the exact spec citation, comment at the workaround). A construct is described as working only after it has been run. Learnings are recorded durably in the repo.

**P6. Z keeps the substantive decisions.** The ACE rules only where the frameworks and principles determine the answer. It escalates when they underdetermine it, conflict, affect a learning outcome, touch a licensing question, or would change a confirmed definition or an SA rule.

## Heuristics (quick tests the ACE applies before reasoning at length)

1. *Substitution test*: solution-independent means functional.
2. *Computed versus explored*: derivable from defined parts is simple emergence (logical); needs simulation is weak (functional); unanticipated is strong (belongs to no layer, judged at sign-off).
3. *Arrangement before sizing*: interfaces and arrangement are logical; sizes and part numbers are physical.
4. *Objective, slot, candidate*: which one does the element read as?
5. *Choice or result*: could a design decision have set this, or must analysis produce it?
6. *Does it earn its place*: what gets harder for the learner without it?
7. *Which kind of definition is asked for*: idea, formal semantics, or story?
8. *Tier of the check*: language always on, or project staged?

## How principles and provenance relate

A ruling states the frameworks and principles it applies and the reasoning from them to the answer. It then lists provenance: statements, glossary edges, spec passages and test results that support the reasoning. If the only support for an answer is a quotation stretched over a case it does not address, the principles do not determine it: escalate.

## Confirmed extensions (Z, 2026-09-27)

The following extensions of the frameworks and principles above to new kinds of case were flagged by the ACE and confirmed by Z as matching Z's own judgment (not merely unobjected-to inferences). Cite these directly; the case no longer needs re-flagging as an extension.

- **F3/F2 to a parameterized conversion (DL-030):** a deterministic input-to-output relation whose parameter is a characterized value (for example an efficiency) is a logical commitment even with no named law and no component chosen yet; the functional-layer relation among the same phenomena is the solution-independent form (a balance inequality, not an equality with a free parameter).
- **F7 to usages of the subject (DL-032):** a usage of the system-of-interest's definition is classified by what IT adds beyond the definition, not by the definition's own classification. A usage that adds nothing takes no layer. A usage that fixes an emergent result is DL-018's defect. "Candidate" requires a concrete part that realizes a logical slot; absent that, a usage built to fail a check is at most a failing-branch fixture, valid only if its content makes the check fail for a reason about the design, not because a number was typed in.
- **F4 to judgment records and satisfaction claims (DL-033):** a Python judgment record is not a layer element (it is analysis, by construction, per F4). An `assert satisfy` relation is a cross-layer traceability claim, not evidence and not analysis; its truth is established by a verification verdict, not by the assertion. A container (e.g. a part usage) holding only such claims, with no part and no owner in the system, denotes nothing the layers describe.
- **F1/F4 to assumptions (DL-034):** a recorded assumption may enter as asserted context (a prescribed condition) or as an explicitly labelled, evidenced estimate of a TPM — never as the derived result itself. A check against an assumed value is reported as conditional on the assumption, never as the candidate's assessed performance.
- **F3/P4 to naming (DL-037):** a name for a not-yet-built logical component that only one alternative mechanism would satisfy pre-empts an unrecorded selection among alternatives in the learner's reading, even though the model itself commits to nothing. Name responsibility groupings by the function they carry; reserve mechanism-suggestive names for after a selection is recorded.
- **F6/DL-025 to tool enforcement holes (DL-039):** language conformance is defined by the spec's validation constraints, not by whether a given tool's `ok` flag happens to catch a violation. A model violating a normative constraint is language non-conformant regardless of `model.ok`; project checks stay `blocked` until no such violation is present. Where a tool has a known hole, the tutorial supplies its own always-on guard (with a negative control) rather than accepting the model as conformant. A false `assert satisfy` (parses, resolves and type-checks, but evaluates False) is not a language-conformance question; it is a staged project check ("satisfaction claims evaluated").
