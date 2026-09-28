# Decision log

## DL-018 | 2026-09-26 | PASS2-001 | F-1 confirmed: Toaster::cycleTime default is an emergent result entered as a choice

Path: Handled by ACE
Decision: F-1 stands. `attribute cycleTime : ISQ::DurationValue default = 120.0 [SI::s]` on `Toaster`, later checked against `<= 180 s` (ch02), is a result entered as a choice. In the re-derivation, cycle time is derived from the mechanism and the energy balance and compared with intent; the attribute may exist as a typed, unit-bearing slot without a default value. No edit now (current models are not a trusted baseline).
Principles applied: F1 (prescribed versus emergent), F4 (evidence comes from analysis), heuristic 5 (choice or result).
Reasoning: cycle time is the time to reach acceptable toast. It follows from the prescribed mechanism (power, heat transfer), the bread and the control, so a design can prescribe those but not the outcome. Setting it as a default makes the later check compare a chosen number with a limit, so the check can never fail for a reason about the design and verifies nothing.
Determined: yes.
Extension: no (the case AGENTS.md 1.5 already names).
Provenance: AGENTS.md 1.5; architecture-layers example table; z-model Z-6, Z-7, Z-22; audit report `decisions/audits/ch01-layer-audit.md` F-1.

## DL-019 | 2026-09-26 | PASS2-001 | OQ-1: the system of interest is the subject; ToastingSystem's purpose is functional

Path: Escalated to Z (ACE first ruled "logical construct carrying a functional statement" from stretched statements; re-reasoned under the principles, which did not determine the answer; Z ruled)
Decision: Z ruled: the system-of-interest is the subject all layers describe, not a layer (framework F7). The doc "Transform bread into toast acceptable to its user" is functional (substitution test) and the seed of a MoE. The abstract part def that names the whole is the named subject; the layer of each piece comes from what it commits to. Re-derivation guidance: the purpose belongs in a functional construct (an action def with typed flows, or a behavioral requirement def) that the whole performs. F-3 stands: `HeatingSystem :> ToastingSystem` and `ControlSystem :> ToastingSystem` make each subsystem a kind of whole-system purpose, which contradicts the subject reading.
Principles applied: F3 (substitution test) for the statement; F2 (objective, slot, candidate) for the construct, which fell short.
Reasoning: the statement is solution-independent, so functional. The construct is a typed part def with no mechanism or interface. F2 reads a value-free typed slot as design space, but does not say whether a bare part def that only names the whole is a logical element or merely the subject of the layers. A stated exception in F2 ("classify the parts separately and report the mix") did not settle it, so the principles underdetermined the answer.
Determined: no, at the step "what is a bare system-level part def?"; Z ruled.
Extension: yes (a new kind of case). The ruling became framework F7.
Provenance: Z's answer 2026-09-26 (subject all layers describe); z-principles.md F7; audit report OQ-1 and F-3.

## DL-020 | 2026-09-26 | PASS2-001 | OQ-2: HeatingSystem and ControlSystem are logical components, not yet built

Path: Handled by ACE
Decision: Logical, not yet built. Responsibility groupings (Douglas "who" = tutorial "how"), typed slots with no values, later the target of allocation. Incomplete, not wrong. For the re-derivation: the logical idiom is `abstract part def` that performs an action (these are concrete), `ControlSystem` carries any policy including a timer setpoint, and neither should specialize the whole's purpose type (F-3).
Principles applied: F2, F7, heuristics 3 (arrangement before sizing) and 4 (objective, slot, candidate).
Reasoning: each names a responsibility and carries no value and no mechanism yet. That is a slot in the design space, so logical. A logical component carries a mechanism and interfaces, and these carry neither, so the logical layer is present but incomplete. They are pieces of the subject (F7), so they are classified on their own commitments.
Determined: yes.
Extension: no.
Provenance: term-logical-component; def-douglas--logical-architecture; z-model Z-13, Z-14, Z-21; audit report OQ-2.

## DL-021 | 2026-09-26 | PASS2-001 | OQ-3: Toaster's composition is a logical arrangement; the whole is the subject

Path: Handled by ACE (revised after F7)
Decision: `Toaster` is the system of interest (the subject, F7), so it is not classified as a layer. Its composition into `heating` and `control` slots is a logical arrangement (no specific part, no part value). `cycleTime` is a result entered as a choice (DL-018), not a part value. `index.md`'s "physical architecture layer" contradicts Part 1 and is F-4 material for the re-derivation. F-2 (`Heater` specializes no logical def; 800 W is a physical sizing choice) stands.
Principles applied: F7, F2, heuristic 3, F1.
Reasoning: the whole names the subject; what it composes is two typed slots and no values, which is an arrangement settled before sizing (logical). A concrete part with a value is what makes something physical, and nothing on `Toaster` confers one.
Determined: yes, after F7.
Extension: no.
Provenance: AGENTS.md 1.5 (logical-to-physical test, Numbers, allocation is not realization); z-model Z-3, Z-8, Z-1; audit report OQ-3, F-2, F-4.

## DL-040 | 2026-09-27 | PASS2-011-A | Q-K: Heater::power is a chosen part rating at the leaf; on an assembly containing a coil and a supply it is derived

Path: Handled by ACE (extension flagged for Z's skim)
Decision: `Heater::power` (default 800 W; `weak` binds 400 W) is a chosen physical part value as declared: a rated power is a property the part confers, stated by whoever chose it, and the model contains no relation that could derive it. DL-021's ruling ("800 W is a physical sizing choice") stands. It is not DL-018's defect. The rule for the re-derivation: a rating is prescribed only at the level where the part is a leaf. Once a candidate contains a coil (resistance) and a supply (voltage) in the same context, the assembly's power is a simple-emergent roll-up derived from them by the Joule-heating mechanism (logical, DL-030 pattern) and is never entered a second time; the leaf values (resistance, supply voltage) stay chosen. The power delivered in use, and the heat reaching the bread, remain results under any reading. `HeatingReq`'s comparison of a rating with a threshold is therefore legitimate in form (a feasibility check of a chosen part against a threshold); `weak`'s failure is a failure about a design choice, expressed wrongly (a false positive `assert satisfy`, DL-039(4)); see DL-049.
Principles applied: F1 (prescribed versus emergent), F2 (candidate checked for feasibility), heuristic 5 (choice or result), heuristic 2 (computed versus explored: derivable from defined parts is simple emergence), heuristic 3; DL-018, DL-021, DL-030 applied as decisions; AGENTS.md 1.5 (Numbers; MoE to MoP to TPM "reasoned over from parts through interconnections to higher-order parts"), 1.6 (simple emergence: a mass roll-up; the numbers arrive when a physical candidate supplies part values).
Reasoning: (1) Heuristic 5: could a design decision have set 800 W? Yes: a heater's rating is a catalogue property of the part chosen, which is the skill's own physical example ("The coil is an 800 W nichrome element"). (2) The discriminating test against `cycleTime`: a cycle time is an outcome of the system in use (term-behavior), which no part carries alone and no vendor states; a rating belongs to the part alone. So the rating is a candidate value (F2) and the cycle time is a result (DL-018). (3) The same quantity is derivable from finer parts (P = V^2/R) once they exist; 1.6's mass roll-up is the same shape: a chosen value at the leaf, a derived value at the assembly. F1 then forbids entering the roll-up as a choice, because a check on an entered roll-up cannot fail for a reason about the parts. (4) The check `power >= 600 W` compares a chosen part value with a threshold, which is the physical checklist's legitimate item ("do the values meet the derived thresholds"), provided the threshold is derived (DL-041). (5) Chapter 6's `resistance` (12, unit-less) without a supply cannot derive anything yet (ch06 F-9), so on the current model the leaf reading is the only one available.
Determined: yes.
Extension: yes. F1 and heuristic 2 applied to a quantity that is prescribed at one level of the recursion and derived at the next (the roll-up pattern, which 1.6 names for mass, applied to power).
Provenance: DL-021; DL-018; DL-030; z-model Z-3 (arrangement before sizing), Z-7 (simple emergence), Z-25 (Joule heating for a chosen coil is logical); architecture-layers example rows "800 W nichrome element" and "Measured heating efficiency"; glossary term-behavior, term-tpm; audits ch06 OQ-1, F-9, F-10; ch08 OQ-4 and its table row on `Heater::power`.

## DL-041 | 2026-09-27 | PASS2-011-A | Q-L: HeatingReq is logical (a threshold in the design space); its physical subject binding is a traceability defect; the label is left to the recorded justification; the 600 W must be derived

Path: Handled by ACE
Decision: `requirement def HeatingReq` with `require constraint { power >= 600 W }` is logical: a threshold on a component performance measure, which is the design-space form (any part meeting the bound satisfies it). Its subject typed by `Heater`, a concrete part def that realizes no logical slot, is a mix reported under F2: the constraint is logical, the binding is a traceability defect (ch06 F-3), and the requirement belongs on the logical carrier of heat generation in the re-derivation. No MoE or MoP label is ruled here (the DL-035 pattern, P2); the evidence on file for the author's justification points to MoP (who cares: the engineer; it measures engineering performance, not acceptance; SEBoK's MoP "yields design requirements necessary to satisfy a MoE"), and the opposite filing is weak but the justification is the modeler's to record. Whichever label: the 600 W is a free-standing number today and must be derived in the re-derivation from a stated MoE through the energy relation, with a means of checking (the logical checklist). Chapter 7's sweep does not derive it: it holds duration at the entered 120 s (DL-018) and a Python-only threshold (ch07 F-6).
Principles applied: F2 (objective, slot, candidate; classify a mix separately), F3 and heuristic 1 (substitution on what the statement requires), heuristic 4, P2 (contextual splits justified, not fixed); DL-035, DL-021 applied as decisions; AGENTS.md 1.5 (a derived MoP threshold is logical; Numbers: a MoP's threshold is a requirement at the layer that states it, what a part has is the TPM; logical-to-physical test).
Reasoning: (1) Heuristic 4: the element reads as a bound, not a value; a bound that any conforming part satisfies is a constraint in the design space (the logical-to-physical test: "if any part built to the stated interface and derived thresholds satisfies it, it is logical"). (2) The skill's idiom table names exactly this construct (`requirement def` with `require constraint` for a derived MoP threshold) as logical, and its example row ("Heating efficiency is at least 0.6") is the same shape. (3) The subject binding does not change the constraint's layer; F2 says classify the parts of a mix separately, and the binding is a commitment about what the requirement is levied on, which the audit already found to be outside the decomposition. (4) P2 forbids fixing the MoE/MoP label by rule; DL-035 applied the same restraint to `TimelyToast`. Power is not a case Z flagged as hard (Z-5 flagged toast time), so the justification should be short, but it is still the modeler's record. (5) The logical checklist requires a derivation and a means of checking; the model has neither (ch06 F-4).
Determined: yes (the layer; P2 determines that no label is ruled).
Extension: no.
Provenance: AGENTS.md 1.5; architecture-layers idiom table row 6 and example row 4; glossary term-mop (SEBoK and tutorial edges), term-requirement (SysML: a constraint a valid solution must satisfy); DL-035; DL-017 (MoE versus MoP is judgment); audits ch06 OQ-2, F-3, F-4; ch07 F-6.

## DL-042 | 2026-09-27 | PASS2-011-A | Q-M: HeatingElement is a mechanism-suggestive name; DL-037 applies directly

Path: Handled by ACE
Decision: `abstract part def HeatingElement` is logical, not yet built (DL-020 pattern: no perform, mechanism, port or value). Its name commits, in the learner's reading, to the resistive mechanism: "heating element" is the term of art for an electrical component that produces heat by Joule heating; a blowtorch's burner is not called one, and the model's own subtypes (`ResistanceCoil`, `PowerWire`) read it that way. Chapter 6 records no selection among alternatives before introducing it. DL-037's confirmed extension applies as ruled: the re-derivation names the responsibility grouping by the function it carries (heat generation; the exact name is content) and reserves a mechanism name for the logical component that carries Joule heating after the selection is recorded. Chapter 6 is a natural place to record that selection as a worked judgment site (trade against the derived measures, term-selection-among-alternatives); once recorded, a resistive-element name is admissible on that carrier.
Principles applied: F3 and heuristic 1 (what the element requires), P3 and P4 (what the learner reads), DL-037 applied as a confirmed extension, DL-020 applied as a decision; AGENTS.md 1.5 (selection among alternatives).
Reasoning: (1) The def has no content, so the model commits to nothing and the layer is logical, not yet built. (2) DL-037's test: would only one alternative mechanism satisfy the name? Yes: the term denotes a resistive element in ordinary engineering usage, and the tutorial's own example vocabulary uses "element" for the nichrome coil. (3) No selection is recorded, so the name pre-empts it in the reader's mind, which is the defect DL-037 rules.
Determined: yes.
Extension: no (DL-037 is a Z-confirmed extension; cited directly).
Provenance: z-principles confirmed extension "F3/P4 to naming (DL-037)"; DL-020; architecture-layers example row "The coil is an 800 W nichrome element"; glossary term-selection-among-alternatives, term-logical-component; audit ch06 OQ-3, F-6, F-7.

## DL-043 | 2026-09-27 | PASS2-011-A | Q-N: decomposing a logical grouping straight to concrete parts is incomplete recursion; each level carries its own functional and logical content

Path: Handled by ACE
Decision: Chapter 6's step from `HeatingSystem` (logical, level 1) to `HeatingAssembly`, `ResistanceCoil` and `PowerWire` (physical, level 2), with no level-2 function, interface or mechanism, is not a valid form of AGENTS.md 1.8's recursion; it is incomplete. 1.8 is binding and determines it: a leaf must perform its specified behavior (so a specified behavior exists at that level: the sub-functions of `ApplyHeat`, with every input and output of `ApplyHeat`, including `duration`, accounted for across the leaves), connect through its specified interfaces (so interfaces exist at that level: at least a power interface between wire and coil and a supply boundary), and have verification evidence. Those are the level-2 functional and logical contents; without them `coil` and `wire` are not leaves in 1.8's sense and `AI-C06`'s completeness claim cannot be true (ch06 F-12). Specialization of a logical def by a concrete def is the right realization shape (1.5), but realization presupposes something to realize: a carrier with a mechanism (Joule heating for the coil) and an interface. The tutorial's idiom for that content is the abstract logical part def that the concrete def specializes (1.5 table); how it is narrated (as a "pass" or interleaved) is content, not ruled.
Principles applied: AGENTS.md 1.8 (binding: "at each level the three boundaries apply again"; "account for every input and output"; stopping rule), F2 and heuristic 3 (arrangement before sizing), F3, F1; DL-020, DL-030, DL-031 applied as decisions; AGENTS.md 1.5 (allocation is not realization; connectivity differs by layer; Numbers: sizing appears only when a part is chosen).
Reasoning: (1) 1.8's stopping rule has three conditions, two of which name content that only the functional and logical layers supply at that level. Level 2 has neither (no perform, no port, no mechanism: ch06 F-6, F-8), so the rule is not met and the level is not finished. (2) Heuristic 3: level 2 has sizes (12 ohm, 14 gauge) with no arrangement, which inverts "arrangement before sizing". (3) The auditability clause ("account for every input and output at every level") is a functional statement at level 2 by construction; `duration` is unaccounted (DL-031). (4) Douglas and SEBoK stop functional decomposition where functions can be allocated to implementable elements, which presupposes level-2 functions to allocate; none exists.
Determined: yes.
Extension: no (the plain case 1.8 states).
Provenance: AGENTS.md 1.5, 1.8; ace-protocol key pattern "recursion ends at leaves that are concrete, interfaced and verified"; glossary term-decomposition (SEBoK and Douglas edges), term-logical-component; z-model Z-3; audits ch06 OQ-4, F-5, F-6, F-8, F-12(c).

## DL-044 | 2026-09-27 | PASS2-011-B | Q-O: Cycle is a functional mode machine as declared; the Finish transition follows Finish's denotation; a timer or thermostat that issues Finish is a policy on ControlSystem, separate from the machine

Path: Handled by ACE (extension flagged for Z's skim: no state-machine idiom exists in 1.5 or the skill)
Decision: `state Cycle` with `idle`, `heating`, `ready`, `cancelled` and the `Start` and `Cancel` transitions is functional: a substitution-independent description of operating modes and of which requests move between them. It selects no input given state (no state performs an action, no transition has an effect), so it is not a policy as declared. The `Finish` transition's layer follows what `Finish` denotes, which DL-036 already requires the model to state: if `Finish` denotes "heating is finished" as an event however it is determined, the transition is functional; if `Finish` is defined as timer expiry or a thermostat trip, the event is issued by a policy and that policy is logical, carried by `ControlSystem` (DL-020, DL-022). The two are kept apart in the re-derivation: the mode machine accepts a functional "done" event, and the policy on `ControlSystem` (with its setpoint, DL-022) issues it. Ownership follows the layer: a functional mode machine is exhibited by the subject (the whole, as DL-019 places the purpose), not by a logical component; `Cycle` today is nobody's modes (ch07 F-1). The trigger-resolution hole (ch07 F-4) is determined by DL-039 (record, guard with a negative control) and needs no new ruling.
Principles applied: F3 (function, mechanism, policy) and heuristic 1, F1 (a state machine is a prescription), F7 and DL-019 (the subject exhibits its functional pieces), F4 and DL-036 (the model states its meaning); DL-020, DL-022 applied as decisions; glossary term-policy.
Reasoning: (1) Substitution: the tongs-and-blowtorch user also waits, heats, finishes and can stop; every state and the Start and Cancel transitions pass. (2) Term-policy is "decision guidance that selects inputs given the state"; the machine selects nothing, so Reading B ("it is the control law") does not describe the element as declared. (3) The Finish transition says only "on Finish, leave heating"; what is solution-dependent is who issues Finish and by what rule. That rule, if a timer, is exactly a policy (F3) and DL-022 already places it on the policy carrier with its setpoint. So the frameworks separate the mode change (functional) from the issuing rule (logical) rather than assigning the whole machine to one side, contingent on the denotation DL-036 leaves to the modeler. (4) F7: a piece of the subject is classified by what it commits to; a mode machine that commits to no mechanism is a functional piece, and DL-019's guidance for the purpose (a functional construct the whole performs) transfers to it.
Determined: yes, for the layer and the rule; the denotation of Finish remains the modeler's under DL-036.
Extension: yes. F3 and F7 applied to a state machine, a construct with no idiom row in 1.5 or the skill; the separation "mode machine functional, issuing policy logical" is new.
Provenance: DL-036, DL-020, DL-022, DL-019; glossary term-policy (tutorial and Sutton and Barto edges), term-mechanism; z-model Z-6; probes in audit ch07 (`exhibit state` in a part def loads and executes in v0.9.0); audit ch07 OQ-1, F-1, F-2, F-4.

## DL-045 | 2026-09-27 | PASS2-011-B | Q-P: a trace of an untimed, action-free state machine is not an emergent result; it is specification analysis, not evidence about behavior

Path: Handled by ACE (extension flagged for Z's skim)
Decision: The `execute_state` traces in Chapter 7 are derived, not entered, so F1's check passes. They are not an emergent result of any kind: the glossary's emergence is a property at the level of the whole not attributable to any one component, and the trace is attributable entirely to one element's transition table and the event sequence the notebook chose, with no composition, no mechanism and no time (`final_time` 0.0, empty context). They are a legitimate turn of the loop in the sense of 1.1 item 1 (build the model, then query and analyze it to check that it says what we intend): a trace can catch a modeling mistake in the table, which is a mismatch about the specification, and that is worth a negative control of its own. They are not evidence about behavior (term-behavior: the outcome of a system in use) and not simulation in the weak-emergence sense of 1.6. Chapter 7's "proves" and "behaviourally consistent" overclaim (1.6, P1). Re-derivation note: once states carry actions and time (for example `heating` performs `ApplyHeat` for a duration set by the policy), a trace yields simple-emergent quantities such as elapsed cycle time, which is one place DL-018's derivation can live.
Principles applied: F1, F4, heuristic 2 (computed versus explored), P1 (a check is not proof), AGENTS.md 1.1 item 1, 1.4 (a negative control shows the loop can detect a mismatch), 1.6 (computed versus explored is the stable distinction); glossary term-emergence, term-behavior, term-simulation.
Reasoning: (1) Heuristic 5: nothing is entered; the trace is computed. (2) Heuristic 2 asks what kind of emergence; term-emergence's own condition (level of the whole, more than one component) is not met, so none, not even simple (a mass roll-up composes parts; this composes nothing). (3) What the trace can fail on is the table not being as intended, which is a property of the prescription; so the analysis is on the specification side of the loop, which 1.1 item 1 values, and not on the behavior side, which 1.6 reserves for derived outcomes. (4) Calling it proof or behavioral consistency violates 1.6 whichever reading holds.
Determined: yes.
Extension: yes. Heuristic 2 and F1 applied to state-machine execution output, a kind of analysis output not previously classified.
Provenance: AGENTS.md 1.1, 1.4, 1.6; glossary term-emergence (SEBoK), term-behavior, term-simulation; z-model Z-6, Z-7, Z-22; audit ch07 OQ-2, F-2, F-8, and its probe table (traces, `final_time` 0.0).

## DL-046 | 2026-09-27 | PASS2-011-C | Q-Q: whether DL-006 stands against AGENTS.md 1.1 item 5 (model checking) is Z's decision; determined now: the "formal / bounded / proof" prose is a defect

Path: Escalated to Z
Decision: Escalated: the question affects a listed learning outcome (1.1 item 5) and any use of an engine other than `check` reopens SA-6; both are Z's (P6). Determined regardless of Z's answer, and ruled now: (1) `verify_satisfaction()` on fixed-valued usages is claim evaluation by the `run` engine ("observed"), not model checking (facts confirmed by two spot reviews: every formal engine declines these as "evaluate questions"); prose that calls it "formally satisfy", "bounded checks", "formal engineering evidence" or a "violation witness" that is more than a failed claim is a 1.6 and P5 defect in any re-derivation. (2) The promised link between Chapter 7's simulation and Chapter 8's record (a figure cited as evidence) either exists in the record or the claim goes (P5). (3) DL-006's reading of SA-6 as "no external model checkers" was a handle-path reinterpretation made before Part 1 existed; it cannot by itself remove a Part 1 outcome, so the outcome must be delivered somewhere or amended by Z.
Principles applied: P6 (learning outcome; SA rule), P5 (probe before asserting; track the gap), P1 and AGENTS.md 1.6 (no check is proof), F4 (analysis produces evidence; a property the model does not state is not checkable), F6; AGENTS.md 1.1 item 5, 1.6 (stability straddles both: an analytic form model checked, plus simulated trajectories); SA-6.
Reasoning: the frameworks fix what model checking is not and what the prose may not say, but they do not rank the design space: whether Ch8 should deliver item 5 (versus a later chapter, or amending 1.1), and whether `smt`/`explore`/`solve` are inside SA-6, are scope and SA questions. Feasibility of a `holds` question in v0.9.0 is unproven (the auditor probed four forms; none worked), and P5 forbids planning on an unrun construct, so any "B" must be gated by a probe.
Determined: no, at the step "does the outcome belong in Ch8, and under which engine?"; Z decides.
Extension: yes (a pre-alignment handle ruling weighed against a Part 1 learning outcome).
Provenance: DL-006; AGENTS.md 1.1 item 5, 1.6, 1.9; SA-6; opensysml engine listing and probes in audit ch08 (engines ready; "not covered" on `check`, `smt`, `explore`, `solve`; `verify_constraint` on a requirement def raises `WrongKindError`; `explore_state` on `Cycle` "complete"); audit ch08 OQ-1, F-2, F-8; both Sonnet 5 spot reviews.
  Brief: as above (Objective / design space A, B, C / candidate B gated by probe / feasibility and utility / judgment).
  Z's decision: B, gated by a probe (2026-09-27). DL-006 is superseded IF the probe shows `check` can answer a 'holds' question on a small model; otherwise fall back to A (amend the AGENTS.md 1.1 item 5 outcome) and escalate the tool gap. The prose defects ("formally satisfy", "proves", "bounded checks") are fixed in either case.
  Z's rationale: (not separately captured beyond the option choice)
  Probe result (2026-09-27, decisions/probes.md): the first probe checked only OpenSysML v0.9.0 and found it evaluate-only; that led to a premature "fallback A, DL-006 stands" conclusion, retracted the same day when Z asked whether the capability was really unreachable or only unreachable through that one tool. **Corrected result: sysml-toolkit v0.9.1's `verify --solve` (already rebuilt in this pass) genuinely proves a constraint holds for all values of an unbound feature via Z3** — verified with a constructed tautology (reported `satisfied`), a contradiction (reported `VIOLATED`), and a bounded-range TimelyToast-shaped requirement (reported `satisfied`). **Fallback B applies: DL-006 is superseded.** Chapter 8 can deliver AGENTS.md 1.1 item 5 without the Pilot Implementation. Remaining question, routed to Z rather than decided here: sysml-toolkit's Python binding has no `verify`/`solve` method, so reaching this from a notebook means a `subprocess` call to the Rust CLI binary, unlike the rest of the tutorial's OpenSysML-based Python flow. D-024 and gap-issue-drafts Draft 8 (which had proposed filing an OpenSysML feature request) are retracted; nothing is filed upstream. **Z's decision on the remaining design question (2026-09-27):** accept the subprocess call. Wrap it in a simple utility function so the learner sees a clean Python call, never a shell-out; log it as a toolchain patch with intent to deprecate once a published package (the sysml-toolkit Python binding, or OpenSysML) exposes the capability natively. This is the repo's standard gap-tracking pattern applied to a capability gap, not a language-conformance gap: patch and document, intending to delete the patch once upstream supports it.

## DL-047 | 2026-09-27 | PASS2-011-C | Q-R: a chapter may add zero model elements; an analysis-only turn is a turn of the loop; conditional on Q-Q, a formal property is a model construct

Path: Handled by ACE
Decision: Yes, a chapter may add nothing to the model. SA-8 admits sub-notebooks that introduce one analysis operation and no construct, and depth notebooks that introduce neither; 1.4's loop turn is construction and analysis of what was constructed, and analysis of the previous chapter's construction is a turn. 1.8's "at every level" is a level of decomposition, not a chapter, so it does not force an addition per chapter. Conditions that do apply: the turn must earn its place (P4), it needs a negative control that shows the loop catching a mismatch of the kind the chapter teaches, not only a language-tier control (1.4; ch08 F-6), and the fixture must say what it is (a provenance comment claiming a chapter-8 increment that does not exist is a P5 defect, ch08 F-1). Conditional: if Z rules Q-Q to B, Chapter 8's formal property is stated in the model (F4: code that defines meaning is a defect) and the chapter then adds that construct; SA-8 then allows the construct and the engine call to sit in separate sub-notebooks.
Principles applied: SA-8, AGENTS.md 1.4, 1.7 (provenance never hidden), 1.8, P4, P5, F4.
Reasoning: (1) SA-8 names the case directly, so the general answer is a settled rule, not an inference. (2) 1.4's negative-control requirement is the substantive constraint on an analysis-only chapter, and ch08's controls are language-tier or record-validation controls, not controls of satisfaction evaluation or staleness. (3) F4 makes the Q-Q conditional automatic: a property checked by a formal engine must be in the model to be checkable.
Determined: yes.
Extension: no.
Provenance: SA-8 (ace-protocol SA table); AGENTS.md 1.4, 1.7, 1.8; sysml-v2-toaster-model line 56 (Ch8 "analysis operations, not new constructs"); audit ch08 OQ-2, F-1, F-6.

## DL-048 | 2026-09-27 | PASS2-011-C | Q-S: satisfaction-claims-evaluated applies from the section that first declares an assert satisfy; in the current sequence that is Chapter 3; not parked

Path: Handled by ACE
Decision: The applicability criterion is determined: the check applies from the chapter and section that first declares an `assert satisfy`, because that is the point at which its property (every asserted claim evaluates True against the model's values or a verification verdict, DL-039(4)) has something to test; the `slow` claim there is its negative control. In the current sequence that is Chapter 3 (the first `assert satisfy timely by slow`), so `applies_from` is set to that chapter and section now; the orchestrator sets the registry value. When the sequence is re-derived, the number follows the criterion, not this entry. This is not the parked case of DL-038: there the property's precondition (a port-typed connection) existed nowhere, so no chapter could be named; here the precondition exists. On the ch05 to ch08 fixtures the check stays `blocked` by the language-tier violations (DL-039), which scheduling does not change; on the ch03 and ch04 fixtures, which predate those violations, it can run and report the `slow` claim `failed`, which is the loop catching the fault DL-039 named.
Principles applied: F6 (each project check is declared as applied from a chapter and section, with a negative control), heuristic 8, P5 (a check with `applies_from=None` that reports "open: unscheduled" indefinitely is a skipped check); DL-023 (trigger: the chapter that declares the property's subject complete), DL-038(2) (applicability criterion), DL-039(4) applied as decisions.
Reasoning: (1) F6 requires a declared applies-from for every project check; leaving one unscheduled is the "silently skipped" case P5 forbids. (2) DL-023's trigger generalizes as "the point at which the property has something to test"; DL-038 fixed the port-type check's criterion the same way. (3) The criterion, applied to the current sequence, yields Chapter 3; nothing in the principles prefers Chapter 8 (the chapter that teaches evaluation) over the chapter that first makes a claim, and choosing the later one would leave a known false claim unreported for five chapters.
Determined: yes for the criterion and for the current-sequence placement; the re-derived number follows the criterion.
Extension: no.
Provenance: DL-023, DL-038, DL-039; AGENTS.md 1.9; `src/toaster/conformance.py` registry (`applies_from=None`, per the audits); audits ch06 F-1, ch08 OQ-3, F-4.

## DL-049 | 2026-09-27 | PASS2-011-C | Q-T: weak is a valid failing-branch fixture in kind; the assertion form, the unrealized slot and the underived threshold are separate defects

Path: Handled by ACE
Decision: `part weak : Heater { :>> power = 400 W }` is a valid failing-branch fixture in kind, unlike `slow`: under DL-040 its bound value is a chosen part rating, so `HeatingReq` fails because a 400 W part was chosen, which is a feasibility failure of a candidate part against a threshold (F2), a reason about the design; in `slow` the typed number is the measured result itself, so the check compares a number with itself. Three defects remain and are ruled separately: (i) the branch is expressed as a false positive `assert satisfy` (DL-039(4)); it is expressed as `assert not satisfy` or a computed check; (ii) `Heater` realizes no logical slot and sits outside the decomposition (ch06 F-3), so `weak` is a candidate part, not a candidate of the system in DL-032's sense; the re-derivation makes the failing part a realization of the heat-generation carrier inside a candidate toaster; (iii) the 600 W threshold is underived (DL-041), so until it is derived the failure is against a free-standing number; that is a defect of the requirement, not of the fixture's kind.
Principles applied: F2 (feasibility of a candidate), F1, heuristic 5; DL-032 (confirmed extension: a fixture is valid only if the check fails for a reason about the design), DL-039(4), DL-040, DL-041 applied as decisions.
Reasoning: (1) DL-032's criterion turns on what makes the check fail; here a design choice does. (2) The three remaining defects each have their own ruling and none changes the kind of the fixture.
Determined: yes, conditional on DL-040.
Extension: no.
Provenance: z-principles confirmed extension "F7 to usages (DL-032)"; DL-039; DL-040; DL-041; audits ch06 F-1, F-3, F-5; ch08 OQ-4, F-4.

## DL-030 | 2026-09-26 | PASS2-008 | Q-A: ApplyHeat's efficiency-parameterized equality is a logical commitment inside a functional action; DeliveredEnergy classified the same

Path: Handled by ACE
Decision: `action def ApplyHeat`'s typed inputs `power`, `duration` and output `energy` are functional flows. `in efficiency` and the body `energy := DeliveredEnergy(power, duration, efficiency)` are a logical commitment: a characterized conversion whose parameter is a MoP (power efficiency), placed inside a functional action. The functional phenomena relation the layer requires is the energy-balance inequality (delivered energy plus loss cannot exceed supplied energy), which the model does not state. `calc def DeliveredEnergy` (ch03) is the same relation and is classified the same way: not the functional phenomena relation; a conversion characterization that belongs with the logical carrier, where efficiency is a MoP slot with a derived threshold. Wherever it lives, efficiency must be bounded (0 to 1) so the relation respects the conservation the functional layer states. Re-derivation: ApplyHeat states typed flows (bread and energy in; toast, delivered energy and loss out) and the balance inequality as a constraint; the equality with efficiency moves to the logical component that carries the conversion (HeatingSystem), and Joule heating for a chosen coil is the mechanism proper. No edit now.
Principles applied: F3 (function, mechanism, policy), F2 (objective, slot, candidate), F1; heuristics 1 (substitution) and 4; AGENTS.md 1.5 (functional idiom: balance inequality; constraints split by solution-independence; MoP typically logical).
Reasoning: (1) Substitution test on the signature: any heat source takes power for a duration and delivers energy, so the flows are functional. (2) Substitution test on the relation: E = P t eta holds for every solution only when eta is defined as delivered over supplied, and then it is a definition, not a relation that constrains anything; the content that constrains any solution is E <= P t, the inequality 1.5 names as the functional form. (3) With eta taken as a given input, the output is a deterministic function of the inputs (the shape of term-mechanism) and presupposes a characterized conversion: a value that exists only once a mechanism has been chosen and measured. 1.5 and the glossary place that value as a MoP, typically logical. (4) So the element mixes an objective (the flows) with a design-space commitment (the characterized conversion); F2 says classify the parts separately and report the mix, which is what the auditor did. (5) Unbounded eta admits E > P t, violating the conservation the functional layer must respect, so the bound follows from 1.5 whichever layer the relation sits in. The ace-protocol handle case "a mechanism stated inside a functional action: move it to the logical component that carries it" applies.
Determined: yes.
Extension: yes. The handle case names a physical law applied to a chosen component (I^2 R); this applies F3 and 1.5 to a lumped conversion characterized by a MoP parameter, with no named law and no component chosen yet.
Provenance: AGENTS.md 1.5 (layer table functional row; constraints split; Numbers); z-model Z-2 (energy conservation as an inequality, efficiency as a MoP), Z-4, Z-25; glossary term-mechanism, term-mop, def-douglas--function (inputs are material, energy, signals); architecture-layers example rows 1, 4, 5; audits ch03 OQ-3 and F-5, ch04 OQ-1, F-1, F-2, ch05 OQ-4; models/ch04-cumulative.sysml lines 33 to 49.

## DL-031 | 2026-09-26 | PASS2-008 | Q-B: ApplyHeat::duration is a functional input slot; its denotation is the re-derivation's decision, constrained by DL-018 and DL-022

Path: Handled by ACE
Decision: As declared, `in duration : ISQ::DurationValue` is a functional input slot: typed, unit-bearing, no value, and its source is not modeled. It is not a result: a result cannot be an input of the function that produces it. Which of the two prescribed readings it takes is the modeler's decision in the re-derivation: (a) a signal from a control function ("heat for this long", which any solution supplies, by a timer or a user), or (b) a timer setpoint, in which case it is named as a setpoint on the policy carrier (ControlSystem) and flows from there. Under either reading it is never the quantity a requirement checks as time to acceptable toast, which is derived (DL-018, DL-022). Because the parameter was copied from DeliveredEnergy's inputs (nb01 cell-05) rather than derived from the function's flows, the re-derivation fixes its denotation explicitly rather than inheriting it.
Principles applied: F1 (with its stated underdetermination clause: a setpoint is prescribed, the result is not, and the modeler decides which is which), F2, F3 (policy); heuristics 1, 4 and 5; DL-018, DL-022 applied as decisions.
Reasoning: (1) Heuristic 4: a typed slot with no value reads as design-space or functional input, not as a candidate value. (2) Substitution: "apply heat for a given duration" is satisfied by a pop-up toaster and by tongs with a blowtorch. (3) Heuristic 5: as an input it is something a design or a controller sets, so it is a choice, not the result; the result (time to acceptable toast) depends on it together with power, bread and heat transfer (DL-022 reasoning). (4) F1's own clause says the modeler decides whether a duration is a setpoint; the principles fix only the expression: setpoint on the policy carrier, cycle time derived.
Determined: yes, for the layer and the constraint; the choice between (a) and (b) is delegated to the modeler by F1 itself, so it is not an open question for Z.
Extension: no.
Provenance: DL-018, DL-022; AGENTS.md 1.5 (policy gloss; connectivity: functional connectivity is behavioral dependency); glossary term-policy; audit ch04 OQ-2; models/ch04-cumulative.sysml line 41.

## DL-032 | 2026-09-26 | PASS2-008 | Q-C: nominal and slow are usages of the subject with no layer of their own; slow is a failing-branch fixture, not a candidate or an operating condition

Path: Handled by ACE
Decision: `part nominal : Toaster` and `part slow : Toaster { :>> cycleTime = 200 s }` are usages of the subject (F7 extended from the definition to its usages). A usage is classified by what it commits to beyond its definition: `nominal` adds nothing, so it is the subject named again and takes no layer; `slow` adds one thing, a fixed binding of an emergent result, which is DL-018's defect in its stronger form (F-5). Neither is a physical candidate: no concrete part def, no part value, nothing that realizes a logical slot (F-6). The "design candidate" label is unsupported until a usage contains a concrete part that specializes an abstract logical def. `slow` is not an operating condition: a condition is a prescribed context (bread thickness, supply voltage, starting temperature) under which the cycle time is derived; a cycle time is the result of a condition, not the condition. Its only role consistent with the chapter's own text and with 1.4 (every chapter's loop has a negative control) is the fixture for the failing branch, and its present content does not validly play that role, because a check that fails only because a number was typed in is not the loop catching a fault about the design. Re-derivation: the failing branch is a candidate (or an injected fault) whose derived cycle time exceeds the bound, or a deliberately negated claim; how it is built is a content decision inside these constraints.
Principles applied: F7, F2, F1; heuristics 3, 4 and 5; DL-018, DL-019, DL-021 applied as decisions.
Reasoning: (1) F7 says classify the pieces of the subject by what each commits to. A usage of the subject's def is not a piece; it is an occurrence of the whole. What it adds is what gets classified. (2) `nominal` adds nothing: no layer. (3) `slow` adds a fixed value of a result: heuristic 5 says a cycle time must be produced by analysis; DL-018 already rules the default form; a non-default binding is the same kind of defect, stronger. (4) F2's candidate is a concrete point checked for feasibility and utility; heuristic 3 says sizes and part numbers are physical; both usages lack any such content, so "candidate" is not established. (5) A condition is something the design or the environment prescribes; the cycle time results from it (F1), so `slow` cannot be a condition as declared. (6) The only remaining reading is the chapter's stated one ("to demonstrate a candidate that fails"), and 1.4 requires such a branch; the content that would make it valid is the re-derivation's to build.
Determined: yes.
Extension: yes. F7 was confirmed for "a bare top-level part def that only names the whole"; this applies it to usages of that def, with the rule "classify what the usage adds".
Provenance: z-principles F7 (Z, 2026-09-26); DL-018, DL-019, DL-021; AGENTS.md 1.4 (negative control), 1.5 (logical-to-physical test; Numbers; prescribed versus emergent); glossary term-usage, term-behavior, term-assumption; audit ch02 OQ-7, OQ-8, F-5, F-6, F-8; models/ch04-cumulative.sysml lines 22 to 23.

## DL-033 | 2026-09-26 | PASS2-008 | Q-D: judgment records and satisfaction claims are not layer elements; part evidence is a container defect

Path: Handled by ACE
Decision: (1) A judgment record (the Python AC-, AS-, AI- ReviewRecords) is not a layer element. It is a judgment site on the analysis side of the loop: it prescribes nothing and states no intent. It is classified by what its claim bears on (an emergent result, a threshold, a completeness criterion) and audited on its P1 fields: the evidence it cites must be analysis or external data, and counterevidence and residual uncertainties stay load-bearing. (2) An `assert satisfy R by X` is a cross-layer traceability claim (requirement to design element) with no layer of its own. It is a claim, not evidence and not analysis: its truth is established by the verification case's verdict on X, and a record that cites the assertion as evidence cites nothing (ch03 F-4). Its tier is project conformance (satisfy coverage and claim evaluation, staged; see DL-039). (3) `part evidence` is not a layer element and not a piece of the subject (nothing composes it). It is a modeling defect: a part usage with no part, used as a namespace, named "evidence" for things that are claims. The re-derivation replaces it with the idiom it chooses for claims (satisfy in the candidate's context, or a verification case's objective) and reserves "evidence" for analysis results.
Principles applied: F4 (declarative model, procedural analysis, evidence; verification-case clause), F2, F7, P1, AGENTS.md 1.4.
Reasoning: (1) F2 admits three kinds of layer element (objective, slot, candidate); a record about the model and a relation between a requirement and an element are neither. (2) F4 places analysis and argument outside the model's layers, and 1.4 says Python never defines what the model means; a ReviewRecord is Python, so it is on the analysis side by construction, an easier case than the verification def Z ruled on. (3) 1.4: judgments about satisfaction "rest on that evidence and point at it. They do not replace it." An assertion is a judgment's conclusion stated in the model; it is not the evidence. (4) A satisfy relation is what the glossary calls traceability (design traces to the requirement it implements); allocation was classified the same way as a cross-layer relation in ch05. (5) The container: SysML's part usage denotes an occurrence of a part (term-usage); one with no definition and no owner in the system denotes nothing the layers describe.
Determined: yes.
Extension: yes. F4's Z-confirmed clause covers verification cases; this applies the same framework to judgment records (not model elements) and to satisfy assertions (model elements that are claims).
Provenance: z-principles F4 (verification clause, Z 2026-09-26); DL-023; AGENTS.md 1.4, 1.5 (a verification case is not a layer element), 1.6 (counterevidence and residual uncertainties load-bearing); SA-7; glossary term-traceability, term-asserted-inference, term-verification, term-usage; audits ch02 OQ-10, F-7; ch03 OQ-4, F-3, F-4; ch04 AI-C04 row.

## DL-034 | 2026-09-26 | PASS2-008 | Q-E: an assumption may stand in for an emergent result only as an assumption; AC-001 does not cure the entered cycleTime

Path: Handled by ACE
Decision: A recorded assumption can enter the argument in two legitimate forms: as an asserted context (an operating condition such as "standard sliced bread", which is a prescribed input, not a result) or as an explicitly labelled provisional estimate of a TPM ("cycle time is estimated at about 120 s from prior data"), resting on evidence other than the model's own declaration and carrying its residual uncertainty. In neither form does it become the derived result: a comparison of an assumed value with a threshold is conditional on the assumption, is reported as such, and is never reported as the candidate's assessed performance. AC-001 does neither: its claim is the result's value, its evidence is the model's declaration of that value, and the chapter then issues a pass verdict from it. So AC-001 does not cure F-5. Re-derivation: keep "standard sliced bread" as asserted context; derive the cycle time under it; if an estimate is used before the derivation exists, label it as an estimate with its source, and report any check against it as resting on the assumption.
Principles applied: F1, F4, P1; heuristic 5; DL-018 applied as a decision; AGENTS.md 1.5 (Numbers: "what a specific part has, or is estimated to have, is the TPM"), 1.6.
Reasoning: (1) F1: a result entered as a choice cannot be checked; wrapping the entered value in a record does not change what the model enters. (2) F4: evidence comes from analysis; the model's declaration of a value is the thing to be evidenced, so citing it as evidence is circular (the auditor's F-7). (3) P1 permits assumptions and requires their justification, evidence and residual uncertainty; Hawkins admits context and assumptions asserted to be appropriate. That licenses the assumption as context or estimate, not as the derived result. (4) 1.5 admits an estimated TPM, so an explicitly labelled estimate is a legitimate stand-in with its own evidence; 1.6 forbids presenting a check on it as settled. (5) AC-001 mixes a context (bread) with a result (120 s) and grounds the result in the declaration, so both tests fail.
Determined: yes.
Extension: yes. DL-018 rules on the attribute; this applies F1 and F4 to judgment records about the attribute and states when an estimate is admissible.
Provenance: DL-018; AGENTS.md 1.5, 1.6; glossary term-assumption, term-asserted-context, term-tpm, term-judgment; audit ch02 OQ-9, F-7, F-5; toaster-review-protocol (asserted-context record type).

## DL-035 | 2026-09-26 | PASS2-008 | Q-F: TimelyToast carries no MoE or MoP label now; the Chapter 3 re-derivation records the justification

Path: Handled by ACE
Decision: No label is applied to `TimelyToast` / `timely` now, and the ACE does not choose one. The label is a case-specific modeling judgment that the Chapter 3 re-derivation records with its justification (who cares; acceptance or engineering performance), as DL-022 already directs. Both readings have evidence on file for the author: the rationale argues from the user's kitchen workflow (acceptance); the verification doc tests at nominal input power (performance). Whichever is chosen: the measured quantity must be derived, not entered (DL-018); if MoP, the 180 s threshold must be derived from a stated MoE with a means of checking; if MoE, it needs a unit and a means of collecting data (the verification case). The phrase "countertop appliance" in the rationale is stakeholder context (where and how the user uses it), not a mechanism commitment: the substitution test applies to the requirement statement, which passes. The re-derivation phrases it as usage context to remove the appearance of a solution class.
Principles applied: P2 (contextual splits justified, not fixed), P6, F3 (substitution on the statement); DL-017, DL-022 applied as decisions.
Reasoning: (1) P2 forbids a fixed rule for this split and requires a recorded, case-specific justification; the ace-protocol handle case says the same. (2) The justification is the modeler's to write and the ACE's to check for presence and coherence, so ruling a label here would substitute a fixed rule for the judgment. (3) A rationale is not a requirement; the boundary test applies to what the statement requires, and "complete a cycle within 180 s" is solution-independent. (4) The layer of `timely` follows the label, so it stays open in the audit tables until the justification is recorded, as the auditors did.
Determined: yes (P2 determines that no label is ruled here).
Extension: no.
Provenance: DL-017 (Z: contextual judgment, toast time could be either), DL-022; AGENTS.md 1.5 (MoE to MoP to TPM; "how long toast takes could be either"); glossary term-moe, term-mop; architecture-layers example row "Toast is ready within 150 s"; audits ch02 OQ-6, F-7; ch03 OQ-1, F-1.

## DL-036 | 2026-09-26 | PASS2-008 | Q-G: Start and Finish are functional flow types; the model must state what they denote

Path: Handled by ACE
Decision: `Start`, `Finish` and `Cancel` are functional flow types under any of the three denotations (material, event, both): each passes the substitution test. Which denotation they carry is a modeling decision for the re-derivation, not a layer call, and the current model does not make it: the names say events, the chapter text says bread and toast, ch05 uses them as part types and ch08 as accepted triggers. The rule the principles impose is that the model states its own meaning: each item def gets a name and a doc that agree on what it denotes, and if bread, toast and control events are all needed they are distinct, named defs (an accepted item can legitimately be both a payload and a trigger, so "both" is admissible only when declared). Until that is done the denotation is recorded as undecided and flow accounting (1.8) cannot be applied to these flows.
Principles applied: F4 (the model is the authority on meaning; code or prose that supplies it is a defect), F3 and heuristic 1, P3, P5; AGENTS.md 1.8 (account for every input and output).
Reasoning: (1) Substitution holds for bread in, toast out, and stop-on-demand, so the layer is functional regardless. (2) F4 makes the model the source of semantics; here the denotation lives only in notebook prose and contradicts the names, so the model does not say what it means. (3) 1.8 completeness needs a fixed denotation to check that every flow is accounted for; the auditor could not apply it (ch04 F-2, F-3; ch05 OQ-2). (4) The choice among admissible denotations is not one the frameworks rank, and it changes no learning outcome by itself, so it belongs to the modeler under the stated rule.
Determined: yes, for the layer and the rule; the denotation choice is the modeler's.
Extension: no.
Provenance: AGENTS.md 1.4, 1.8; glossary def-douglas--function (inputs are material, energy, signals); audits ch04 OQ-3, F-3; ch05 OQ-2, F-5(b); models/ch04-cumulative.sysml lines 50 to 52.

## DL-037 | 2026-09-26 | PASS2-008 | Q-H: BreadEjector is a responsibility grouping; its name leans on one alternative and is renamed by function in the re-derivation

Path: Handled by ACE
Decision: `part def BreadEjector` is a responsibility grouping, logical and not yet built (the DL-020 pattern): the element carries no mechanism, constraint, port or value, so the model records no selection among alternatives. The name is not a model commitment, but it is learner-facing content that pre-empts the selection in the reader's mind: "eject" is what a spring-loaded pop-up does and tongs do not eject. The re-derivation names responsibility groupings by the function they carry (bread loading, bread removal) and reserves mechanism names for the logical component that carries the chosen mechanism after a recorded selection. The same applies to any other name that describes a mechanism before one is selected.
Principles applied: F3 (substitution test on what the element requires), F2, P3 and P4 (what the learner sees), heuristic 1; DL-020 applied as a decision; AGENTS.md 1.5 (selection among alternatives; conceptual-to-functional: do not invent functions not asked for).
Reasoning: (1) F3's test asks what the statement requires; a def with no content requires nothing, so it commits to no mechanism and the layer is logical, not yet built. (2) P3 and P4: learner content is judged by what it conveys; a name that only one alternative satisfies teaches that the choice is made when the model has not made it, and 1.5 requires selection by trade study against derived measures. (3) The stakeholder need is that toast is removed, not that it is ejected, so the functional name is the one the conceptual-to-functional test supports.
Determined: yes.
Extension: yes (mild): F3 and P4 applied to a name rather than to a declared relation.
Provenance: DL-020; AGENTS.md 1.5; glossary term-selection-among-alternatives, term-logical-component; z-model Z-10; audit ch05 OQ-1, F-4.

## DL-038 | 2026-09-26 | PASS2-008 | Q-I: interface-compatibility check: staged tier and applicability criterion determined; chapter placement and a flow-end check parked

Path: Handled by ACE
Decision: Determined: (1) The check is staged project conformance whose property is interface compatibility, logical (DL-023). (2) Its applicability criterion is that a port-typed connection is declared: an interface is a connection whose ends are all ports (glossary), and the check compares port types. (3) On the ch05 model the check is `open` with the reason "no port-typed connection declared; the flow's ends are part usages typed by item defs": recipe 5's empty result is vacuous and is not reported as a pass. If the item-typed part usages are confirmed as language non-conformance (DL-039), the status is `blocked` with that unblock criterion instead. (4) Recipe 5 is not widened to item-typed ends: a check's scope follows the property it tests, and widening it would let a connection without ports pass an interface check. Not determined here and parked with the placement decision: which re-derived chapter and section the check applies from, and whether a separate "flow end and payload type compatibility" check is declared (with its own negative control) for flows between non-port ends. That depends on the re-derived model's connection idiom; the tutorial's logical idiom is ports and interfaces, so the need may not arise.
Principles applied: F6, heuristic 8, P1 (no verdict from an empty result), P5; DL-023, DL-024, DL-025 applied as decisions.
Reasoning: (1) DL-023 fixes the tier and the trigger ("the chapter that declares the connection complete"); the criterion that makes a connection checkable by this check is that its ends have port types to compare. (2) DL-024's reasoning: a "passed" that would hold whatever the model's state is not a verdict; an empty mismatch list on a model with no port ends is exactly that. (3) F6 requires each check to be declared with a negative control; a widened recipe 5 would have a different property and would need its own declaration and control, so it is a new check, not an extension of this one. (4) Placement of staged checks in the re-derived sequence is a parked decision by the orchestrator's statement; nothing in the principles forces a chapter.
Determined: yes for tier, criterion, current status and scope; placement not decided (parked, not underdetermined).
Extension: no.
Provenance: DL-023, DL-024, DL-025; AGENTS.md 1.5 (connectivity differs by layer), 1.9; DEFERRED.md D-014; decisions/probes.md G4 conformance note; glossary def-sysml--interface; opensysml-query recipe 5; audit ch05 OQ-3, F-5(e).

## DL-039 | 2026-09-26 | PASS2-008 | Q-J: tool-accepted invalid SysML is language-tier non-conformance; a false assert satisfy is a staged project check

Path: Handled by ACE (extension flagged for Z's skim). The tool behaviour was confirmed by two independent spot reviews (Sonnet 5, 2026-09-26). **Part (1) amends Z's DL-025. Z accepted the ACE's reading (2026-09-27).** DL-025's unblock criterion is now read as "no language-tier violation, per the spec, is present"; `model.ok` is a proxy, not the definition. The other parts (recording, tutorial-supplied guard, the false-satisfy check as project-tier) stand as ruled.
Decision: (1) Tier. A spec validation constraint (KerML `ReferenceSubsetting::referencedFeature` typed `Feature`, so `allocate ApplyHeat to HeatingSystem` between definitions is invalid; SysML `validatePartUsagePartDefinition`, so `part bread : Start` typed only by an item def is invalid) is a language-conformance rule. A model that violates one is language non-conformant per the spec, whether or not the tool loads it. `model.ok` is the available proxy for language conformance, not its definition; DL-025's unblock criterion "language conformance passes" is read accordingly, and project checks on such a model are `blocked` with the unblock criterion "no language-tier violation, per the spec, is present". (2) Recording, per the gap-tracking rule: each case gets a DEFERRED entry, a comment cell wherever the construct appears, and a drafted upstream issue citing the exact constraint (a bug report, since the spec requires the diagnosis, unlike G4 where it did not): OpenSysML for both cases; sysml-toolkit for the item-typed part usage. Nothing is filed until Z reviews the text. (3) Guard. Until upstream fixes a hole, the tutorial supplies a language-gap guard that runs on every load (always on, reported as language conformance, not as a staged check) from the JSON export, with a negative control per rule; the toolkit's `check` is corroboration for the rules it catches (the allocation case) and is not a chapter dependency. (4) `assert satisfy timely by slow` evaluating False is not language conformance (parse, name resolution, typing all pass). It is a staged project check, "satisfaction claims evaluated": every asserted satisfy is evaluated against the model's own values or the verification verdict, and a False claim is `failed`. The current `slow` assertion is the natural negative control for it, and a deliberately failing branch is expressed as `assert not satisfy` or as a computed check, not as a false positive assertion. (5) Re-derived models carry none of the three constructs; the guard and the check exist so the loop detects them.
Principles applied: F6 (two tiers) and heuristic 8, P5 (do not paper over; track gaps), P1 (a check is not proof; a claim is not evidence), F4; AGENTS.md 1.9 (gap-tracking rule, binding; "tools may not diagnose a fault themselves, so the tutorial supplies the check"); DL-023, DL-024, DL-025 applied as decisions.
Reasoning: (1) F6's test asks whether a rule is part of the language or a project check whose time has not come; a normative validation constraint in the metamodel is part of the language, so the tier is fixed by the spec, not by which tool enforces it. (2) F6's purpose ("breaks the load") is that non-conformance is discovered at once; when a tool leaves a hole, P5 and 1.9 say the tutorial supplies the check and tracks the gap, rather than downgrading the rule to a staged check or accepting the model as conformant. (3) The upstream draft is a bug rather than a feature request because the spec text names the constraint (contrast D-014, where no constraint was found). (4) Evaluating an assertion is semantics, outside the language tier's parse, resolve and type; it is the construct-and-analyze loop's own job, which 1.4 says must be able to detect a mismatch. (5) The proxy reading of DL-025 keeps its substance (a project check is blocked until the model is language conformant) while removing a dependence on a tool that has a known hole.
Determined: yes, conditional on the reviewers' confirmation of the tool behaviour; the classification logic does not depend on it, only the entries do.
Extension: yes. F6 and DL-025 were framed for a tool that enforces the language tier; this applies them to holes in that enforcement and adds a tutorial-supplied language-tier guard.
Provenance: AGENTS.md 1.2 (toolchain cited only to flag a spec gap), 1.4, 1.9; z-model Z-27; DL-017 (conformance), DL-025; decisions/probes.md G2 (the tool does reject a def where a usage is required for perform, so the allocate hole is inconsistent with its own rule), G4 conformance note; DEFERRED.md D-014; audits ch03 F-3 (false assertion; `assert not satisfy` parses), ch05 F-1, F-3 (toolkit error on line 53; XMI constraints read from the vendored OMG 20250201 metamodel, not yet confirmed against formal/2026-03-02).

## DL-028 | 2026-09-26 | PASS2-007 | `tall-named` lint rule matches any naming of Tall or the three worlds in learner content

Path: Handled by ACE
Decision: The `tall-named` rule matches any capitalised standalone "Tall" and the phrase "three worlds" (any case, hyphen or whitespace between the words) in learner content, not only possessive, lens-phrase and year forms. Rare false positives are handled by the baseline mechanism, not by narrowing the rule. The six "Tall seam" hits in ch09 and ch10 are real violations already tracked as the recipe-versus-rule contradiction parked for Pass 4 and may be baselined only while that entry stands. Pass 4 inputs, not decided: about 64 seam cells in ch01 to ch08 use the world labels A-F and O-S without the word "Tall" (whether those labels count as naming the lens belongs to the recipe rewrite), and whether docs/ contributor pages that must name the lens need a scope carve-out.
Principles applied: AGENTS.md 1.10 (binding), P4, P5, F6.
Reasoning: 1.10 is an absolute ("never names"), so there is no per-case judgment site; the question is only whether the check's match set covers the prohibition. Each phrasing the reviewer listed names Tall, so a check that reports conformance while missing them has not established it (P5) and lacks a working negative control for its own fault (F6). The rule's object is the lens, so naming it without the author is the same violation. The precision cost is remote in this corpus and the baseline already classifies accepted hits.
Determined: yes.
Extension: yes (F6 and P5, written for model conformance checks, applied to the design of a prose lint).
Provenance: AGENTS.md 1.10; ace-protocol key pattern on Tall; decisions/next-passes.md sections 4 and 6; independent review PASS2-007-R; scan of learner content on 2026-09-26.

## DL-029 | 2026-09-26 | PASS2-007 | `stale-partition` stays literal; the ch01 "implementation-agnostic" sentence is a content defect; plural allowed in `stale-physical-layer`

Path: Handled by ACE
Decision: `stale-partition` stays the literal phrase "partitioned into implementation-agnostic" (zero hits is a passed guard, not a dead rule). It is not widened. The sentence at chapters/ch01-system-purpose/conclusion.md line 9 remains a Pass 4 content input, already recorded (audit F-4, pass2-run-001, next-passes 7.1). `stale-physical-layer` also matches "physical architecture layers".
Principles applied: F2, heuristics 3 and 4, P2, P5, F6.
Reasoning: "Implementation-agnostic" is live vocabulary for functions, so "the structure is implementation-agnostic" is not stale phrasing. It is false for Chapter 1 only because that model carries an 800 W value and an arrangement, a per-case layer classification of model elements that a regex cannot evaluate; encoding it as a fixed phrase would be the fixed rule P2 forbids. The defect is already tracked, so P5 holds without the lint. A phrasing rule matches its number variants.
Determined: yes.
Extension: yes (P2 applied to lint-rule design; F6 applied to a prose rule).
Provenance: AGENTS.md 1.5; audit report F-4; the old A10 framing rule quoted in decisions/log.md; glossary tutorial edges for functional, logical and physical architecture.

## DL-026 | 2026-09-26 | PASS2-006 | Near-verbatim canonical wording on the public glossary page: Z accepts short attributed wording

Path: Escalated to Z (the ACE could not determine it: a licence acceptance and a change to confirmed definitions); Z chose option A
Decision: Z accepts reproducing short definitional wording from canonical sources on the public glossary page when the source is attributed and the wording is not put in quotation marks as if verbatim. Recorded as a rule in `tutorial-glossary` (rule 3): a single definitional sentence of at most 200 characters may reproduce canonical wording in `gl:text` or `gl:gloss`; longer text is paraphrased; `gl:quote` is never rendered publicly. No graph edits. Quotation marks around the on-page gloss (option C) were rejected by the ACE, and printing `gl:quote` is not allowed. The page stays out of any published deploy until the WP-8 deploy job exists; merging publishes nothing (the deploy job is a placeholder).
Principles applied: P6 (licensing; Z keeps the decision), F5, P5, heuristic 7.
Reasoning: the ACE found 16 confirmed edges whose text reproduces a run of 8 or more consecutive source words, so the question is a rule for a class of edges. Whether attributed near-verbatim wording may be published is a licence acceptance that only Z gives; a paraphrase for each would change confirmed definitions. Z accepted the attributed wording.
Determined: no for the ACE (P6); decided by Z.
Extension: yes (new class of case).
Provenance: ACE triage 2026-09-26; the existing edges' text lengths (longest 186 characters); glossary/README.md; tutorial-glossary rules 3 and 4. Note for Z: the option offered said "about 160 characters"; the rule states 200 because existing confirmed edges reach 186. Adjust if you want a tighter limit; the page is unaffected until then.

## DL-027 | 2026-09-26 | PASS2-006 | docs/glossary.md renders every confirmed term; Tutorial entry, locators and departure note

Path: Handled by ACE (DL-601, DL-602 and the docs-page scope ruling, numbered here)
Decision: (1) The page renders every confirmed term as `render` output of the confirmed graph; the `tutorial-supporting-pages` row for `docs/glossary.md` is corrected to say so. (2) The Tutorial entry is an attribution derived from `gl:refines` (last in Sources), not a source with a builder-facing locator. (3) "(PDF n)" is stripped from every rendered locator; graph strings and `gl:pdfPage` unchanged. (4) A bridge edge with a `gl:differsFrom` gets the line "This tutorial uses this term differently from <source>." (binding rule AGENTS.md 1.2, orchestrator-required).
Principles applied: P4 (earn your place), P3 (derived from the source of truth), F5, P5.
Reasoning: the learner must be able to tell canonical paraphrase from the tutorial's own sharpening (F5), and builder-facing locators (AGENTS.md, PDF indexes into gitignored local files) do not help a learner (P4); the page is derived from the graph, not hand-curated (P3); the approved departure must be visible to learners (AGENTS.md 1.2).
Determined: yes.
Extension: yes (P4 applied to citation locators; P3 applied to a generated reference page).
Provenance: ACE triage 2026-09-26; independent review PASS2-006-R (Opus 5.5); myst.yml toc; AGENTS.md 1.2 and 1.3.

## DL-025 | 2026-09-26 | PASS2-004 | Conformance statuses: add blocked (with unblock criterion) and wont-do; supersedes DL-024's "no fourth status". **Amended by DL-039, Z accepted 2026-09-27: the unblock criterion is spec-based language conformance, not model.ok alone.**

Path: Escalated to Z (Z's own ruling; the ACE had recommended against a fourth status in DL-024 and flagged the alternative)
Decision: Z ruled that project checks carry five statuses: `open` (not yet applied: unscheduled or stage not reached), `passed`, `failed`, `blocked` (cannot be applied until a stated condition holds, and the result records that condition), and `wont-do` (dropped because something changed and the check is no longer needed, with the reason and the change that removed the need). A project check on a model that fails language conformance is `blocked`, with the unblock criterion "language conformance passes (model.ok is True)"; it is not `open`. The same vocabulary and a basic task state machine (ready, in-progress, in-review, escalated, blocked, done, wont-do) coordinate the orchestrator's work (`decisions/task-states.md`); the orchestrator proposes `wont-do` and the ACE rules.
Principles applied: F6 (tier of the check), P5 (record the reason), P4 (a status must earn its place), P6 (Z keeps the decision).
Reasoning: DL-024 argued that a `blocked` status would not earn its place because the reason field carried the cause. Z decided otherwise: a distinct status with a checkable unblock criterion makes coordination explicit (what is waiting, on what, and when it may proceed) and lets the orchestrator and the ACE use clear language. The ACE's alternative (B) in DL-024 was the one chosen. `wont-do` records scope changes without deleting the reasoning.
Determined: yes, by Z.
Extension: yes (applies the coordination vocabulary to conformance results).
Provenance: Z, 2026-09-26; DL-024 (option B, "blocked", flagged there as the principled alternative); `decisions/task-states.md`.

## DL-024 | 2026-09-26 | PASS2-002 | Project checks report open, with reason, when the model fails language conformance

Path: Handled by ACE (extension flagged for Z's skim). **Superseded by DL-025**: Z chose the alternative it flagged, a distinct `blocked` status.
Decision: A project conformance check is not applied to a model that fails language conformance. `report()` checks language conformance first; when `model.ok` is false every project result is `open` with the reason "not applied: language conformance failed", never `passed` or `failed`. `Result` carries a `reason` so "stage not reached", "unscheduled" and "model did not load" are distinguishable. No fourth status is added.
Principles applied: F6 (two tiers), heuristic 8 (tier of the check), P1 (a check is not proof; no verdict from absence of evidence), P5 (record the reason), P4 (a new status must earn its place).
Reasoning: language conformance is tier one and breaks the load, so a model that fails it is not a loaded model and no project check has been applied to it. The report rule for an unapplied project check is open, not passed. Reporting "passed" from no findings on an incomplete model is a verdict that would hold whatever the model's state, so it is not a verdict. The module already refuses to count findings on a non-ok model in `prove_negative_control`; the same rule applies to the absence of findings. The reason is recorded so nothing is silently absorbed. A fourth status ("blocked") would add vocabulary without making anything easier to read, since the language block and the reason field already carry the cause.
Determined: yes for "not passed, reason recorded"; the choice of `open` over a new status rests on P4 and on reading "applied" as "run against a loaded model". The alternative, a "blocked" status, remains if Z prefers the status field to carry the distinction.
Extension: yes. "Open until applied" was framed for staging (the check's chapter has not come); this applies it to a precondition failure (the chapter has come, the model did not load).
Provenance: AGENTS.md 1.9; DL-017 (conformance), DL-023 (a check is analysis, classified by tier); evidence: `part def A :> Missing;` with `strict=False` gave `model.ok == False` and a scheduled check returned "passed" with no findings; implemented in commit `3bb58df`'s successor by contract PASS2-003.

## DL-023 | 2026-09-26 | Dry run 3 | A verification case is not a layer element

Path: Escalated to Z; Z ruled option A
Decision: A `verification def` (and the check it runs) is not itself a functional, logical or physical element. It is the analysis half of the construct-and-analyze loop, classified by the layer of what it tests and by its tier (language, or staged project conformance). The AGENTS.md 1.5 layer table no longer lists `verification def` in the physical row; TPMs are the assessed values. For a port-type conformance check: the property tested (interface compatibility) is logical, the check is staged project conformance, and it is applied from the chapter that declares the connection complete.
Principles applied: F4 (declarative model, procedural analysis, evidence), F6 (tier of the check), F2 (objective, slot, candidate), heuristic 3 (arrangement before sizing), P5 (probe before asserting).
Reasoning: the property checked is interface compatibility, an arrangement matter, so logical. F6 makes the check staged project conformance. F2 classifies what the design prescribes and intends; a check is none of those, and F4 places it on the analysis side. The principles did not say whether a check is a layer element, so the ACE escalated with options (not a layer element / logical / physical) and recommended "not a layer element"; Z chose that.
Determined: no, at the step "is a verification case a layer element?"; Z ruled.
Extension: yes; the ruling was added to framework F4 in `z-principles.md`.
Provenance: Z's answer 2026-09-26; ACE round 3 request 5 (`decisions/ace-dry-run.md`); AGENTS.md 1.5 and 1.9; recipe 5 in `opensysml-query`.

## DL-022 | 2026-09-26 | PASS2-001 | OQ-4: cycleTime is not a timer setpoint as declared; F-1 stands

Path: Handled by ACE
Decision: A timer setpoint is a legitimate prescribed policy parameter but a different element: it lives on the control component, is named as a setpoint, and is never the quantity a requirement checks as time to acceptable toast. Whether the re-derived design uses a timer is the modeler's choice; the rule constrains only its expression (setpoint on the policy carrier, cycle time derived). OQ-5 (MoE versus MoP for toast timing) acknowledged without action: Chapter 3's re-derivation carries a recorded justification (P2).
Principles applied: F1, F3 (policy), heuristic 5, P2.
Reasoning: a setpoint is a chosen input of a policy that selects inputs given state, so it is prescribed. The time to acceptable toast depends on the setpoint together with power, mass and heat transfer, so it is a result under any control scheme. The element as declared sits on the whole and is checked against a requirement limit, which treats it as a result.
Determined: yes.
Extension: no.
Provenance: z-model Z-6, Z-22; AGENTS.md 1.5; audit report OQ-4, OQ-5.

## DL-017 | 2026-09-26 | Pass 1 (M2) | Z walk-through: mechanisms as laws, MoE/MoP as judgment, two-tier conformance

Status: COMPLETE

Path: Escalated to Z. The ACE dry run (DL-101..114 in `decisions/ace-dry-run.md`) ruled three scenarios from Z-statements that were recorded too rigidly; Z corrected them by popup on 2026-09-26.

Decision:
- **Mechanisms (Z):** physical laws such as Joule heating (I^2 R) are mechanisms: modeling decisions grounded in established engineering practice, the laws we use to reason about behavior. "Sub-behavior" is dropped from prompts, keys and skills. A law that holds for any solution (energy balance) stays functional; the same kind of law as applied to a chosen component is logical. The confirmed tutorial definition of *mechanism* was extended with the modeling-decision framing (Z chose "add the modeling-decision framing").
- **MoE versus MoP (Z):** contextual modeling judgment, justified for each case; how long toast takes could be either. Tutorial edges for *MoE* and *MoP* now say so and no longer fix examples. The earlier ACE ruling that swapped the two was wrong.
- **Conformance (Z):** two tiers. Language conformance is always on; project conformance is staged (applied from a declared chapter and section, negative control, open until applied). G4 is reframed accordingly; recipe 5 in `opensysml-query` is the port-type check, tested against a mismatch and a specialization.
- Wording changes: AGENTS.md 1.5 and 1.9, `architecture-layers`, `opensysml-query`, `ace-protocol`, `z-model.md` (Z-5, Z-6 revised; Z-25 to Z-27 added).

Rationale: Z's corrections; nothing else changed. Confirmed glossary definitions (mechanism, MoE, MoP) were edited at Z's direction in this walk-through and are shown to Z for review; `glossary check` passes.

Z's decision: as above. Read-back (2026-09-26): AGENTS.md Part 1 approved as is. *mechanism* approved as written. *MoE* and *MoP*: revise for clarity and SEBoK compatibility, keep them as semantic overlays that help people define, measure and interpret criteria (a measure needs a unit and a means of collecting data), and do not overload them; redraft applied 2026-09-26 with Z's changes: MoE example is "how evenly the bread is toasted" (concrete, measurable, something a user cares about); MoP example is power efficiency (the fraction of electrical power converted into heat). Both are described as semantic overlays on a measurable attribute (unit plus a means of collecting the data), open with SEBoK's idea, and keep one short sentence that the MoE/MoP split is a justified judgment. The redraft was presented to Z with the exact text and applied on Z's answer to change the examples. DL-204: Z chose option A (each kind of emergence is named where its value is first obtained).

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

Status: COMPLETE (2026-09-26). Z read back and approved AGENTS.md Part 1 (as is) and `decisions/next-passes.md` (all four clusters as written), 2026-09-26. Gap drafts 1 and 2 approved for filing subject to Z's go on the final text; drafts 3 to 5 held for Z's review; nothing is filed.

Path: Escalated to Z — this pass was specified interactively by Z (plan approved 2026-09-26, `/Users/z/.claude/plans/now-we-re-starting-to-merry-music.md`). Because Z directed it, the skill-editor escalate-to-Z gates (multi-archetype change, >20% of a skill, new capability, learning-outcome effect) are satisfied by this entry; this is a one-off Z override, not a change to file authority.

Decision (intended change, one sentence): align AGENTS.md (new Part 1 Foundations, existing roster kept as legacy Part 2), CLAUDE.md, `ace-protocol`, `skill-editor`, and three new skills (`architecture-layers`, `opensysml-query`, `tutorial-glossary`) with Z's what/how/where intent, backed by a new local glossary knowledge graph (`glossary/`), a query-helper fix in `src/toaster/query.py`, gap records G1-G7, and a handoff file `decisions/next-passes.md`.

Skill edit pre-entry (skill-editor step 1; Z-directed pass): existing skills `ace-protocol`, `skill-editor` and `opensysml-api` are edited in this pass. Revert record: their text at commit `21d4842` (`git show 21d4842:.claude/skills/<skill>/SKILL.md`), which precedes the first edit. No work package is mid-loop; this is a Z-directed alignment pass.

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

What comes next: `decisions/next-passes.md` (pass sequence with entry and exit criteria, operating model, model-pinning rule, audit findings, parked decisions, content-pass inputs). Records produced in this pass: `decisions/probes.md`, `decisions/ace-dry-run.md`, `decisions/cold-start.md`, `decisions/gap-issue-drafts.md`, DL-016 (glossary triage), DL-017 (Z walk-through), and `DEFERRED.md` D-014 to D-018.

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

## DL-050 | 2026-09-27 | PASS3-001-C | Pass 3 dry run: simulated-learner mechanism PASS on ch01 nb01; seam-label finding confirmed as DL-028's open item, not new

Path: Handled by ACE — user-test finding
Decision: The simulated-learner evaluation mechanism passes its dry run: two persona reports (Novice on Haiku 4.5, SE Practitioner on Sonnet 5) on chapters/ch01-system-purpose/01-abstract-def.ipynb, index.md and conclusion.md were reproduced exactly by the ACE's own execution and triaged to zero blocking items. Five items classified: (1) the seam cell's "(A-F)", "(O-S)", "(E)" tags — minor, the same issue DL-028 left undecided and next-passes §6 parks for the Pass 4 recipe rewrite, now with learner evidence recorded; (2) the "abstract modifier not yet supported" comment names the D-004 gap without saying it is the Editor API's — minor, new Pass 4 wording input; (3) TOASTER_INCREMENT is consumed by scripts/check_construction.py but the link is invisible from the notebook — minor, already next-passes §7 item 6; (4) the tall-named lint does not match the world labels (verified: `glossary/lint_rules.toml`'s regex is `\b(?-i:Tall)\b|\bthree[\s-]+worlds\b`, which cannot match "A-F", "O-S" or "(E)") — not a new gap, recorded in DL-028 as a not-decided Pass 4 input; no widening until the recipe rewrite decides whether the labels name the lens, then widen (A-F, O-S; skills scope carved out) in the same contract as the seam-cell rewrite; (5) index.md line 26 and conclusion.md line 9 layer vocabulary — already tracked (pass4-backlog line 54, DL-029). No minor item is decided here. Pass 3 does not gate content; Pass 4 does.
Principles applied: AGENTS.md 1.10 (both clauses, binding), P4, heuristic 6, P5, F6, P6; DL-028 applied as a prior decision; DL-029 and D-004 applied as prior records.
Reasoning: (a) Blocking, per user-testing, is a non-executing cell, a multi-sentence concept statement, a seam that names Tall or "three worlds" or does not address the seam in behavior, a passing negative control, or a broken cumulative model; the ACE re-ran every cell and none holds, and both learners could point concretely to model text, loading tool and printed result, so the seam is behaviorally addressed. (b) The world labels: whether they name the lens (1.10 first clause) is DL-028's undecided question and is not reopened; the learner evidence bears on 1.10's second clause and P4, whose test is whether removal makes understanding harder — the Novice reports the tags obscure the connection and the Practitioner read the sentence as complete without them, so removal makes understanding easier, the opposite of earning a place. DL-003 found the same confusion under the pre-Foundations regime (naming three worlds was then a PASS criterion); under 1.10 the remedy reverses from defining the abbreviations to dropping them. The notebook conforms to toaster-recipe line 143 and tutorial-style-guide line 59, which is the recorded recipe-versus-rule contradiction; removing a required element from the recipe requires Z, and that decision is already parked, so nothing is escalated anew. (c) Lint: DL-028 applied F6 and P5 to lint design — a check establishes only the prohibition it is defined to cover, and the world labels were explicitly left to the recipe rewrite; widening now would decide that question by regex, "(E)" is unmatchable regardless, and the lint-plus-behavioral-judgment split is exactly what this dry run exercised and confirmed. (d) Probes: at v0.9.0 the abstract increment loads alone, isAbstract is recorded, and a direct usage of the abstract def loads without diagnostic (legal SysML), so the caveat is correct only as a statement about the Editor API (D-004); check_construction.py lines 11-13, 196, 212 consume TOASTER_INCREMENT. (e) Mechanism observation: neither persona flagged the index.md/conclusion.md layer-vocabulary defects; the learner checklist has no such step and the layer-auditor role is the tool for that, so the two evaluation workflows catch disjoint things as intended.
Determined: yes.
Extension: no (P4 and 1.10 second clause are written for lens vocabulary in learner content; DL-028 is applied as a decision, not extended).
Provenance: AGENTS.md 1.10; DL-028 (Pass 4 inputs, not decided); DL-029; DL-003 (WP-2 checkpoint, pre-Foundations "all Tall seams name three worlds" as a PASS criterion); DEFERRED.md D-004 (toaster#9 / OpenSysML#595, verified); glossary/lint_rules.toml `tall-named` regex (verified); `.claude/skills/toaster-recipe/SKILL.md` lines 103-106, 143, 156; `.claude/skills/tutorial-style-guide/SKILL.md` line 59; `.claude/skills/sysml-v2-toaster-model/SKILL.md` line 156; scripts/check_construction.py lines 11-13, 196, 212; models/ch01-cumulative.sysml header; learner reports `decisions/dryrun/pass3-learner-novice-ch01.md`, `decisions/dryrun/pass3-learner-practitioner-ch01.md`; ACE execution and probes of nb01 and nb02, 2026-09-27.

## DL-052 | 2026-09-28 | PASS4-011 | COMPLETE: opensysml-query's three stale recipes fixed to match the real, re-derived model; Z-directed directly in chat

Path: Z-directed alignment pass (Z: "go ahead and start on next-passes.md item 17")
Decision: Fixed Recipe 1's assertion (`"ToasterDemo::Heater" in names`, a part def removed by Chapter 6/7's re-derivation) to `"ToasterDemo::HeatGenerator" in names`; Recipe 2's assertion (`"ToasterDemo::HeatingSystem" in realizers` of `ToastingSystem`, a specialization DL-019 removed) to `"ToasterDemo::Toaster" in realizers`; Recipe 3's assertion (`assert flows and allocs`, since the re-derived model has zero `FlowUsage` elements) to `assert allocs` plus an explicit `assert flows == []` with a one-line note that this reference model legitimately has no `FlowUsage` elements. Also fixed one adjacent docstring (`end_path`'s own example path, still citing the removed `BreadHandling`/`BreadLoader` chained-feature example) to a real, current single-segment path, found during the Step 4 post-edit re-read of the modified section's immediate neighborhood. No other structural change. Per the skill-editor's Z-directed-alignment-pass clause, this entry (recording Z's direct chat instruction to start item 17) satisfied Step 2's escalate-to-Z gates for the edits it names; none of the blast-radius table's own triggers applied independently (single skill; no prohibition removed; no new capability added; `sysml-v2-toaster-model`'s construct list untouched; no learning outcome affected).
Revert record: `git show 84f1b15:.claude/skills/opensysml-query/SKILL.md` (the commit immediately preceding this edit) has the pre-edit text.
Principles applied: skill-editor Step 1 (pre-edit gate), Step 3 (minimal-change rule: fixed only the three stale assertions plus one adjacent stale docstring found during the mandatory adjacent-section re-read, no restructuring), Step 4 (post-edit check: re-read the modified section and its immediate neighbors, `glossary check` clean, full test suite green).
Reasoning: `decisions/next-passes.md` item 17 (found during PASS4-008) and `decisions/pass4-run-009.md`/`pass4-run-010.md` (both carrying the same item forward, unfixed, since neither builder had skill-editor authority) already established these three assertions were stale against the real, current model; this was a direct, mechanical correction, not a new judgment call.
Determined: yes.
Extension: no.
Provenance: `decisions/next-passes.md` item 17; `decisions/audits/ch08-layer-audit.md` F-8; `tests/test_skill_snippets.py::test_opensysml_query_recipes_run_against_ch08` and `::test_port_type_conformance_recipe_catches_mismatch_and_accepts_specialization` (the two tests this fix closes; full suite now 310 passed, 0 failed, the first fully green run of this whole pass).

## DL-051 | 2026-09-27 | PASS4-000 | SA-8 relaxed for structural (layer-separation) increments; Z's decision, escalated directly, not an ACE ruling

Path: Escalated to Z
Decision: Z relaxes SA-8 ("one new construct or analysis operation per sub-notebook") for a structural increment specifically: a notebook whose job is separating what one existing element conflates across the functional/logical/physical layers (DL-030's fix — moving `efficiency` to a bounded logical carrier and adding a separate energy-balance inequality is the motivating case) may introduce the small set of constructs one layer boundary genuinely requires together (for example `perform action`, an `abstract part def`, and a named `allocate`, introduced as one coherent idea), rather than being forced to spread them across more notebooks or being blocked by SA-8's letter. SA-8's spirit (no combining unrelated constructs for unrelated reasons) is unchanged; the exception is scoped to layer-separation, not general convenience. Options considered and not chosen: redrawing notebook boundaries to keep SA-8 exactly as written (more, smaller notebooks per chapter); an unscoped case-by-case exception (rejected as too open-ended to log or apply consistently).
Principles applied: P6 (reopening SA-1 to SA-9 is Z's alone; the ACE and the orchestrator do not rule on it, only surface it); F6 is preserved (the boundary tests and per-layer idiom are unchanged, only the notebook-granularity packaging is relaxed).
Reasoning: Pass 4's re-derivation is required by DL-030 to properly separate a mechanism, its interface, and its carrier from the functional layer — that separation is one idea with several necessary parts, not several unrelated ideas; forcing it across artificially split notebooks would fragment one coherent boundary-test explanation into pieces that don't stand alone, which works against the same didactic clarity SA-8 exists to protect. The relaxation is scoped narrowly (structural/layer-separation increments only) so it does not license combining unrelated constructs for convenience elsewhere.
Determined: yes.
Extension: yes — SA-8 is a binding Standing Assumption; this is Z reopening and narrowing it, not the ACE applying it to a new case.
Provenance: AGENTS.md (SA-1 to SA-9 binding); ace-protocol "Never re-open SA-1 through SA-9 without A8 logging and routing to Z"; decisions/next-passes.md §6 (the SA-3/SA-8 collision, flagged); DL-030 (the motivating fix); decisions/pass4-backlog.md §2.
