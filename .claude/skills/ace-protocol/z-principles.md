# Z's principles, frameworks and heuristics (DRAFT for Z's confirmation)

The ACE decides from these, not from quotations. Each entry gives the principle, why it holds, a test the ACE can apply, and when it stops determining the answer (the cue to escalate). The statements Z has made in conversation (`z-model.md`) are **provenance**: they are where a principle was drawn from and evidence of how Z applies it. They are not authority for a case they do not address.

Status: extracted by the ACE's maintainer from Z's statements and decisions on 2026-09-26. Only Z confirms or changes this list.

## Frameworks (how Z reads a situation)

**F1. Prescribed versus emergent.** A design prescribes elements, relationships and principles; behavior is what results, and is derived and checked against intent. *Test:* is this something the design chooses, or something expected to follow from the choices? A result entered as a choice cannot be checked, so it is a defect. *Underdetermined when:* a value is genuinely a chosen control parameter that also influences a result (a setpoint): the parameter is prescribed, the result is not, and the modeler decides which is which.

**F2. Objective, design space, candidate (optimization reading of the layers).** Functional says what is good and what is good enough (the objective). Logical is a typed design space with constraints and no solution values. Physical is a candidate, checked for feasibility against the logical layer and for utility against the functional layer. *Test:* what does this element read as: an objective, a slot or constraint, or a candidate value? *Underdetermined when:* an element mixes them (a slot carrying a value, a purpose carried by a construct): classify the parts separately and report the mix.

**F3. Function, mechanism, policy.** A function is solution-independent (two or more different mechanisms could provide it). A mechanism is a modeling decision grounded in engineering practice, a law we reason with, comparatively deterministic. A policy selects inputs given state, designed given the mechanisms available. *Test:* substitution (would a pop-up toaster and tongs with a blowtorch both satisfy it?).

**F4. Declarative model, procedural analysis, evidence.** The model states intent and semantics; scientific Python analyzes it; simulation and analysis produce the evidence that supports judgments. *Test:* is a number, unit or relation defined in the model, or only in code? Code that defines meaning is a defect.

**F5. Kinds of definition, not rivals.** SEBoK supplies the idea, the OMG specs the formal and checkable semantics, Douglas the analogy and story. Tutorial definitions refine canonical ones and never contradict or invent. *Test:* does it narrow or clarify a canonical edge, and which kind of definition is being asked for?

**F6. Two tiers of conformance.** Language conformance is always on and breaks the load. Project conformance checks are staged because the model emerges iteratively; each has a negative control and is reported open until applied. *Test:* is this rule part of the language, or a project check whose time has not come?

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
