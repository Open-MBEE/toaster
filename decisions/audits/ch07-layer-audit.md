# Chapter 7 layer audit

Contract PASS2-011-B, 2026-09-27. Role: `.claude/agents/layer-auditor.md`. Model: claude-opus-5-5[1m] (effort high).
Branch `audit/ch07`, base commit `a84dceb`.

Subject: the elements Chapter 7 adds, that is, the diff between `models/ch06-cumulative.sysml` (82 lines) and `models/ch07-cumulative.sysml` (93 lines). Both are generated fixtures and were not edited. Apart from the header comment on line 3, the diff is lines 78 to 88 of the ch07 fixture:

```
state Cycle {
    entry; then idle;
    state idle;
    state heating;
    state ready;
    state cancelled;
    transition first idle accept Start then heating;
    transition first heating accept Finish then ready;
    transition first heating accept Cancel then cancelled;
}
```

Chapter 7 also adds analysis that creates no model element: a sympy binding of `DeliveredEnergy` (notebook 01), state traces (notebook 02) and a power sweep with a figure (notebook 03). These are on the analysis side of the loop. They are classified by what they bear on (DL-023, DL-033) and listed separately in the table.

Method: the four-question pass and the per-layer checklist in `.claude/skills/architecture-layers/SKILL.md`, AGENTS.md §1.4 to §1.9, `.claude/skills/ace-protocol/z-principles.md` (F1 to F7, P1 to P6), the glossary (`uv run python -m glossary tutorial` and `lookup` for simulation, policy, behavior, dynamical system, control law, function, emergence, mechanism, usage), and the ACE rulings DL-018 to DL-023 and DL-030 to DL-039 as settled precedent. I did not re-argue them. I cite rulings by the id in each `decisions/log.md` heading. Some other files cite the same rulings under different ids (see "Contract premises that did not hold", item 4).

Evidence collected by running things:
- Both fixtures load with OpenSysML v0.9.0 (`load_from_content`, `strict=False`): `model.ok == True`, no diagnostics.
- I diffed the API JSON export by qualified name (`ApiIndex` from `src/toaster/query.py`). Chapter 7 adds these elements:
  - one `StateUsage` `ToasterDemo::Cycle`, owned by the package;
  - four `StateUsage`s: `idle`, `heating`, `ready` and `cancelled`;
  - one `StateSubactionMembership` (`Cycle::@0`, kind `entry`) and one `SuccessionAsUsage` (`Cycle::@1`), which together form `entry; then idle;`;
  - three unnamed `TransitionUsage`s (`Cycle::@6`, `@7`, `@8`);
  - eight `FeatureMembership`s and one `OwningMembership`, which only hold the members.

  Nothing is removed. No `StateDefinition`, `ExhibitStateUsage` or `AcceptActionUsage` exists in the ch07 export. `perform_relationships(...) == []`.
- The transitions' `source` and `target` resolve to the substates. The trigger is exported only as a string: `"sysx:trigger": "Start"` (and `"Finish"`, `"Cancel"`). It is not a reference to `ToasterDemo::Start`.
- `uv run python scripts/check_conformance.py models/ch07-cumulative.sysml --stage 7,0` returned exit code 0, language `ok=True` and four `gap_findings`: two `allocate-between-definitions` and two `part-typed-only-by-item-def`. Both project checks (`port-type` and `satisfaction-claims-evaluated`) are `blocked` with the unblock criterion "no language-tier violation, per the spec, is present". The output for `models/ch06-cumulative.sysml --stage 6,0` is identical, so Chapter 7 adds no gap finding and changes no check status.
- `execute_state` probes on the ch07 fixture. `final_time` is `0.0` and `final_context` is `{}` in every run.

  | Events | States visited |
  |---|---|
  | `[Start, Finish]` | `[idle, heating, ready]` |
  | `[Start, Cancel]` | `[idle, heating, cancelled]` |
  | `[Start, Finish, Start]` | `[idle, heating, ready]` |
  | `[Finish]`, `[Cancel]`, `[Bogus]` and `[]` | `[idle]` |
- Trigger-resolution probes with OpenSysML v0.9.0:
  - A package containing `transition first a accept Missing then b` with no `Missing` declared loads with `ok=True` and no diagnostics. `execute_state(events=["Missing"])` then takes the transition.
  - `accept Thing`, where `Thing` is a `part def`, also loads.
  - A copy of the ch07 fixture with `item def Cancel;` deleted loads with `ok=True`, and the cancel trace still reaches `cancelled`.
  - A copy with `accept Cancle` (a typo) loads with `ok=True`, and the cancel trace stops at `[idle, heating]`.

  sysml-toolkit v0.9.1 (`sysmlv2 check --lib .../SysML-v2-Release/sysml.library`) reports both modified copies as `warning: unresolved reference` on line 86. It reports no such warning on the real ch07 fixture. Its only error there is the inherited line-53 allocation error. AGENTS.md §1.2 allows the toolchain to be cited only to flag a spec gap, which is the only way it is used here.
- The grammar vendored in the sysml-toolkit checkout (`spec-refs/SysML.xtext`, lines 1302 to 1307, 1450 to 1461 and 1854 to 1899) makes a transition trigger an `AcceptActionUsage`. Its payload parameter, written as a bare name, is an `OwnedFeatureTyping`. So `accept Start` types the accepted payload by `Start`, which requires name resolution.
- Alternative forms, probed only to see what the tool can express: `exhibit state S {...}` inside a `part def`, and a `state def SD {...}` with `exhibit state s : SD` in a part def. Both load and execute in v0.9.0.
- All three notebooks were executed in a scratch copy of the chapter with `nbclient`, and all three pass. Notebook 03 prints `Threshold crossed at: 600 W` and `Nominal (800 W): 67.2 kJ`. The committed notebooks carry no stored outputs.
- `uv run python -m glossary check` passes in this worktree (0 errors, 7 warnings). The warnings say the local source PDFs are absent. `uv run python -m glossary lint` reports no hit in `chapters/ch07-execution/`.

Evidence read for intent:
- `chapters/ch07-execution/index.md`, `conclusion.md`, and every cell of notebooks `01-calc-energy`, `02-state-traces` and `03-param-sweep`.
- `scripts/check_construction.py`, the `CONSTRUCTION_NOTEBOOKS` entry for notebook 02 (lines 149 to 155).
- `DEFERRED.md` D-010.
- `models/ch08-cumulative.sysml`, read only to see whether Chapter 8 changes `Cycle` (it does not; the diff is the header comment).

## Classification table

Elements from earlier chapters that the additions reference are shown in *italics* for context. They are not audited here.

| Element (qualified name) | Layer | Reason | Status |
|---|---|---|---|
| `ToasterDemo::Cycle` (`StateUsage`, owned by the package, no definition) | Functional (recommended default; OQ-1) | Q1: modes of waiting, heating, done and aborted hold for a pop-up toaster and for tongs with a blowtorch (substitution test, AGENTS.md §1.5; F3). The declaration is a prescription, not a result (F1). The skill's idiom table has no state construct, so this call rests on the four questions alone. Nothing composes or exhibits it, and its modes trace to no function. | FINDING F-1, F-2, F-3; OPEN-QUESTION OQ-1 |
| `ToasterDemo::Cycle::@0` (`StateSubactionMembership`, kind `entry`, an empty entry action) and `Cycle::@1` (`SuccessionAsUsage`, `then idle`) | Functional (follows `Cycle`) | This pair declares the initial mode. It commits to no mechanism. | PASS |
| `ToasterDemo::Cycle::idle` (`StateUsage`) | Functional (follows `Cycle`) | Waiting holds for any solution. | PASS |
| `ToasterDemo::Cycle::heating` (`StateUsage`) | Functional (follows `Cycle`) | Every solution heats, so the name commits to no mechanism (contrast DL-037). The state has no `do`, `entry` or `exit` action and no reference to `ApplyHeat`. | FINDING F-2 |
| `ToasterDemo::Cycle::ready` (`StateUsage`) | Functional (follows `Cycle`) | The mode holds for any solution. The state has no outgoing transition. | FINDING F-3 |
| `ToasterDemo::Cycle::cancelled` (`StateUsage`) | Functional (follows `Cycle`) | The mode holds for any solution. The state has no outgoing transition. | FINDING F-3 |
| `ToasterDemo::Cycle::@6`: `transition first idle accept Start then heating` (unnamed `TransitionUsage`) | Functional if `Start` is a user request (OQ-1) | DL-036: `Start` is a functional flow type under every admissible denotation. The trigger is a string in the export, and OpenSysML does not resolve it. | FINDING F-4; OPEN-QUESTION OQ-1 |
| `ToasterDemo::Cycle::@7`: `transition first heating accept Finish then ready` (unnamed `TransitionUsage`) | Functional or logical, depending on the denotation of `Finish` (OQ-1) | If `Finish` means "the toast is done", the transition is intent. If a timer or a thermostat issues it, the transition is part of a control policy (term-policy), which DL-020 and DL-022 place on `ControlSystem`. The model does not say which (DL-036). | FINDING F-4; OPEN-QUESTION OQ-1 |
| `ToasterDemo::Cycle::@8`: `transition first heating accept Cancel then cancelled` (unnamed `TransitionUsage`) | Functional (stop on demand; DL-036 reasoning) | The substitution test passes: any solution can be stopped. The trigger is unresolved in the tool. | FINDING F-4 |
| *`ToasterDemo::Start`, `Finish`, `Cancel` (ch04 `item def`, no doc)* | *Functional flow types, denotation undecided (DL-036)* | *Unchanged in Chapter 7, which adds a fourth use for them: accepted triggers. See premise 3.* | *context* |
| *`ToasterDemo::ApplyHeat`, `DeliveredEnergy`* | *Functional flows with a logical commitment inside (DL-030)* | *Referenced by notebooks 01 and 03.* | *context* |
| *`ToasterDemo::ControlSystem`, `Toaster`* | *Logical, not yet built (DL-020); the subject (DL-019, DL-021)* | *Neither owns or exhibits `Cycle`.* | *context* |
| Analysis, notebook 02: `execute_state` traces for `[Start, Finish]` and `[Start, Cancel]`, with hand-written expected traces | Not a layer element (DL-023; F4 as extended by DL-033). Bears on `Cycle` (functional). | The trace is derived by executing the model, not entered as a choice, so the F1 check passes. It follows entirely from the declared transition table, though, and so shows only that the tool executes what was declared (OQ-2). It is the only thing in the chapter that would catch a mistyped trigger (F-4). | PASS for "no result entered as a choice"; OPEN-QUESTION OQ-2 |
| Analysis, notebook 02 cell 10: negative control (undefined transition target makes the load fail) | Not a layer element; language tier (F6) | It shows target resolution failing, and it does fail. It does not cover trigger resolution, which does not fail (F-4). | PASS as a control of targets; see F-4 |
| Analysis, notebook 01: `BINDING`, `Q_sym`, `Q_fn`, and the `model.eval` cross-check at one point | Not a layer element. Bears on `DeliveredEnergy` (a logical conversion characterization, DL-030). | The relation is copied into Python by hand. The efficiency bound `[0, 1]` and the unit mapping exist only as Python strings (F4). Agreement at one point is called proof (§1.6). | FINDING F-5, F-8 |
| Analysis, notebook 03: `sweep_1d` over power, with `t = 120 s`, `eta = 0.7` and `threshold = 50 000 J` | Not a layer element. Bears on `HeatingReq` and the entered `cycleTime`. | The relation, the efficiency, the duration and the threshold are all defined only in Python (§1.4: not evidence). The threshold is not in the model, is derived from no MoE, and disagrees with the model's `HeatingReq`. The duration equals the entered `cycleTime` default (DL-018). | FINDING F-6 |
| Analysis, notebook 03: `ch07_param_sweep.svg` | Not a layer element; a view of analysis output (§1.7) | The figure is written to the working directory and closed, never shown. It has no caption, and its units are hard-coded rather than read from the model. `Cycle` has no figure at all. | FINDING F-7 |

Chapter 7 adds no MoE, MoP, TPM, requirement, constraint, attribute, metadata, port, allocation or specialization. It adds no physical element.

## Per-layer checklist results

**Functional**
- *Typed inputs and outputs, all flows accounted for?* No. `Cycle` has no typed flows. Its inputs are three accepted triggers. The model states no relation between `Cycle` and `ApplyHeat`, the only function (F-2). Because the triggers' denotation is undecided (DL-036), flow accounting under §1.8 still cannot be applied.
- *Solution-independent (substitution test)?* PASS for the states and for the `Start` and `Cancel` transitions. The `Finish` transition depends on OQ-1.
- *Phenomena relations stated as relations?* None are added.
- *At least one MoE?* None are added. The inherited absence (backlog §4) stands.
- *Reads as an objective?* Partly. The machine says which modes exist and how requests move between them. It says nothing about what is good enough.

**Logical**
- Chapter 7 adds no logical element under the recommended default of OQ-1. If OQ-1 is ruled the other way, the `Finish` transition is a policy with no carrier: `ControlSystem` does not exhibit `Cycle`, and nothing is allocated to it (F-1).
- *Interfaces match?* Not applicable to the additions. The inherited checks are `blocked` (see the conformance run above).
- *No solution values, and no results entered as choices?* PASS for the model additions.

**Physical**
- Nothing is added. Notebook 03 sweeps heater power, a physical value, but no part def or candidate is involved. The 800 W point is a Python number that happens to equal `Heater::power`'s default; it is not read from the model.

**Across layers**
- *Stopping rule (§1.8):* no leaf meets it. Not yet built.
- *Emergent result set as a default and then "verified":* the model additions contain none. Notebook 03, though, holds duration at `t = 120 s`, which equals the entered `Toaster::cycleTime` default (DL-018), and the chapter calls the sweep the evidence Chapter 8's judgment record cites (F-6). Nothing in Chapter 7 derives cycle time.
- *Judgment recorded:* notebook 01 cell 5 calls the SysML-to-sympy mapping "an engineering judgment", but no judgment record is made. Notebook 03 introduces a 50 kJ design threshold with a one-line comment as its only justification (F-6).
- *Figures:* F-7.

## Findings

**F-1. `Cycle` is not part of the system of interest.**
Element: `ToasterDemo::Cycle`.
Check: F7 and DL-019/DL-021 (the whole is the subject; classify its pieces). This is the same pattern as ch05 F-6 (`BreadHandling`) and backlog §3 and §6.
What is wrong:
- `Cycle` is a package-level `StateUsage` with no definition. No `Toaster`, `ControlSystem` or other part exhibits or owns it: the export has no `ExhibitStateUsage`.
- The text calls it "the toaster's discrete operating modes" (notebook 02 cell 1, index), but in the model it is nobody's modes.
- The tool does not force this form. `exhibit state` inside a part def, and a `state def` with an exhibited usage, both load and execute in v0.9.0 (probed).

What I did not do: I did not move or retype `Cycle`, and I did not choose an owner. The owner depends on OQ-1.

**F-2. The modes trace to no function, and `heating` does nothing.**
Elements: `Cycle`, `Cycle::heating`.
Check: the functional checklist (typed flows, all flows accounted for; §1.8) and cross-layer traceability.
What is wrong:
- No state has an `entry`, `do` or `exit` action. No transition has an effect.
- Nothing references `ApplyHeat`, and nothing references its `duration` input, which DL-031 reads as either a signal from a control function or a timer setpoint.
- Notebook 02 cell 1 says the machine "complements" `ApplyHeat`, but the model states no relation between them. So "heating" is a label: executing the machine applies no heat and advances no time (`final_time` is `0.0`, `final_context` is `{}`).

What I did not do: I did not propose `do` actions or a link to `ApplyHeat`.

**F-3. `Cycle` does not cycle, and the model and text do not say whether that is intended.**
Elements: `Cycle::ready`, `Cycle::cancelled`.
Check: the conceptual-to-functional test (§1.5) and F4 (the model states its meaning).
What is wrong:
- `ready` and `cancelled` have no outgoing transitions, so each run ends there. `[Start, Finish, Start]` stays in `ready`.
- The name `Cycle` and the phrase "the toaster's operating cycle" (notebook 02 cell 0) suggest a return to `idle`.
- Neither the model nor the text says whether a single run is the intended scope.

This is minor. I record it because it is a statement of intent that the model and its name disagree on.

What I did not do: I did not add transitions.

**F-4. OpenSysML v0.9.0 does not resolve transition triggers. This is a language-tier hole that nobody tracks, and it hides whether the triggers refer to `Start`, `Finish` and `Cancel` at all.**
Elements: `Cycle::@6`, `@7` and `@8`, and their use of the three item defs.
Check: AGENTS.md §1.9 (language conformance includes name resolution; the gap-tracking rule), F6, P5, and DL-039 (the tier is set by the spec, not by the tool; the tutorial supplies a guard).
What is wrong:
- (a) By the grammar (`SysML.xtext` lines 1302 to 1307 and 1897 to 1899), `accept Start` is an `AcceptActionUsage` whose payload is typed by `Start`, so the name must resolve. OpenSysML v0.9.0 accepts `accept Missing` with `ok=True`, and it accepts a `part def` as the trigger type. Deleting `item def Cancel;` from the ch07 fixture changes neither the load nor the cancel trace. sysml-toolkit v0.9.1 resolves the names and warns when one is unresolved; it reports a warning, not an error.
- (b) The export carries the trigger only as the string `sysx:trigger`, with no `AcceptActionUsage`, no `TransitionFeatureMembership` and no typing. So neither `model.query()` nor the JSON export can answer "which event drives this transition" by reference. The language-gap guard behind `check_conformance.py` reads the export and cannot see the relation (it reports nothing new for ch07). The three transitions are also unnamed.
- (c) The `CONSTRUCTION_NOTEBOOKS` context stubs for notebook 02 (`item def Start; Finish; Cancel;`) are never exercised: the fragment loads without them. Notebook 02's negative control covers an undefined target, which the tool does resolve, and not an undefined trigger, which it does not.
- (d) On the real ch07 fixture, all three names resolve (the toolkit gives no warning). So the ch07 model is not non-conformant on this point. The defect is that nothing in the loop would detect it if it were. The trace assertions in notebook 02 would catch a typo only by accident.
- (e) No `DEFERRED.md` entry, probe row or issue draft covers it. D-010 covers only the Editor authoring gap.

What I did not do: I did not add a DEFERRED entry, a probe row or an issue draft, and I did not extend the guard. See the contract premise on this point below.

**F-5. Notebook 01 defines meaning in Python that the model does not state, and calls one-point agreement proof.**
Element: the analysis in notebook 01 (`BINDING`, `Q_sym`, `Q_fn`, the `model.eval` cross-check).
Check: F4 ("code that defines meaning is a defect"), AGENTS.md §1.4 and §1.6, and DL-030 (efficiency must be bounded 0 to 1 wherever the relation lives).
What is wrong:
- The efficiency domain `[0, 1]` and the unit strings exist only in the Python `BINDING` dict. They are not enforced: the sympy symbol is only `positive=True`. The model still leaves `efficiency` unbounded (DL-030 and backlog §2 recur).
- `Q_sym = P * t * eta` is copied by hand from the calc def, not read from the model. The cross-check with `model.eval` compares one point (800 W, 120 s, 0.7), and `conclusion.md` says it "proves that the calc def formula is correctly expressed". §1.6 forbids describing a passing check as proof, and agreement at one point does not establish that the two expressions are the same.
- Cell 5 names the mapping an engineering judgment but records none (P1).

What I did not do: I did not change the binding or the text.

**F-6. The sweep that Chapter 8 is said to cite as evidence rests on numbers and a threshold that exist only in Python, and on the entered cycle time.**
Element: the analysis in notebook 03 cell 5.
Check: AGENTS.md §1.4 ("A number produced in Python without a model-defined unit and relation is not evidence"), F4, DL-018, DL-030, DL-034 (an estimate enters only as a labelled estimate), and the logical checklist (MoP thresholds derived from a MoE, with a means of checking).
What is wrong:
- The relation is rebuilt as `P * t * eta` in cell 5. The model is loaded and never queried.
- `eta = 0.7` appears nowhere in the model, and it is not labelled as an estimate with a source.
- `t = 120 s` equals `Toaster::cycleTime`'s default, which DL-018 rules is a result entered as a choice.
- `threshold = 50 000 J` is a requirement-like number that is not in the model, is derived from no MoE, and is justified only by a code comment ("ensures toast within the cycle time at typical efficiency"). Cell 6 calls it "the requirement that delivered energy exceeds the design threshold", but no such requirement exists.
- The model's own `HeatingReq` requires `power >= 600 W`. At 120 s and 0.7, the 50 kJ threshold corresponds to 595.2 W.
- The printed "Threshold crossed at: 600 W" is the first grid point of `linspace(500, 1200, 50)` at or above 595.2 W. It coincides with the model's 600 W, which invites the reading that the sweep derived the requirement. `index.md` says the crossing is "between 590 W and 600 W".
- Notebook 03 cell 1 says the figure "is the simulation evidence referenced by the judgment record in Chapter 8". Under §1.4 it is not evidence as built.

What I did not do: I did not audit Chapter 8's record, and I did not change the sweep.

**F-7. The sweep figure is never shown, has no caption, and is not read from the model. The state machine has no figure.**
Check: AGENTS.md §1.7 (a plot of simulation output shows derived behavior, with units and relations read from the model; what a figure omits is stated), P3, and the last item of the cross-layer checklist. This recurs from backlog §11.
What is wrong:
- Notebook 03 writes `ch07_param_sweep.svg` into the working directory, which is the chapter folder when the notebook is run, and calls `plt.close(fig)`. The learner never sees it.
- The axis units ("W", "kJ") and the title's `t=120 s, η=0.7` are hard-coded.
- No figure of `Cycle` or of the assembled model appears in the chapter.

What I did not do: I did not render anything for the chapter.

**F-8. The chapter text contradicts the rules and the model.** This is documentation consistency, not a model defect.
- `conclusion.md`: "The sympy binding proves ..." (§1.6), and "the toaster model is behaviourally consistent". The traces only restate the transition table (OQ-2), and "consistent" is not defined.
- `index.md`: "the cumulative model has ... a sympy-bound energy expression ... and a matplotlib figure". Neither is in the model (§1.4: Python never defines what the model means).
- `index.md`: `model.find("ToasterDemo::Cycle")` returns "`kind='stateDef'` or equivalent". It returns `kind='stateUsage'`, and `Cycle` is a usage.
- Notebook 01 cell 3, notebook 02 cell 8 and notebook 03 cell 3 all say `Cycle` is "the first executable behavior in the model". Chapter 4's `ApplyHeat` already declares an action with successions. I did not check whether OpenSysML executes it, so this claim is unverified rather than wrong. Notebook 01 cell 3 and notebook 03 cell 3 also describe the state machine in notebooks that do not use it.
- Notebook 03 calls a sweep of a static algebraic relation "simulation evidence". term-simulation (SEBoK: a model that behaves like the system given controlled inputs) may admit it, but nothing evolves over time. I record this as a wording observation and do not rule on it.
- Notebook 02 cell 3 cites "§7.24 (StateUsage), §7.25 (TransitionUsage)". The architecture-layers skill cites 7.24 for `verification def`. I did not verify which numbering is correct, because the formal PDF is not local.
- The Tall seam cells (notebook 01 cell 13, notebook 02 cell 12, notebook 03 cell 6) use the world labels A-F, O-S and E. The lint finds no hit. Whether these labels name the lens is parked for Pass 4 (DL-028), so this is not a finding here.

Reported only; no edits.

## Open questions (for the orchestrator to route)

**OQ-1. What layer are `Cycle` and its transitions: an intended mode behavior (functional), or a control policy (logical, carried by `ControlSystem`)?**
- Reading A, functional.
  - The substitution test passes for every state and for the `Start` and `Cancel` transitions: the tongs-and-blowtorch user also waits, heats, finishes and can stop.
  - Under the four-question rule, Q1's "yes" ends the classification.
  - The machine selects no input. No state performs an action (F-2), so there is nothing a policy (term-policy: selects inputs given state) would select.
  - The text presents it as "discrete operating modes", which is a statement of intent.
- Reading B, logical (policy).
  - The glossary's policy is a mapping from state to action (Sutton and Barto). A state machine whose `heating` mode ends on a controller-issued `Finish` (timer expiry or a thermostat) is the control law, and DL-020 and DL-022 put any policy, including a timer setpoint, on `ControlSystem`.
  - Only a controller issues `Finish` under a timer design. A user issues it under tongs-and-blowtorch, and "toast is done" issues it as a phenomenon. So the `Finish` transition's layer depends on its denotation, which DL-036 leaves to the modeler and the model does not state.
- The two readings agree on `idle`, `ready`, `cancelled` and the `Start` and `Cancel` transitions (functional). They differ on the `heating` to `ready` transition and on who owns `Cycle` (F-1).
- The skill and AGENTS.md §1.5 list no state-machine idiom for either layer, so this is also a gap in the idiom table.
- Recommended default: Reading A as declared, with the `Finish` transition marked "layer contingent on the denotation of `Finish`" until the re-derivation states it. If the re-derivation introduces a timer, the transition that timer drives is logical and belongs on the policy carrier.

**OQ-2. Is the state trace a derived result (simple emergence) or a restatement of the prescription? This decides premise 2.**
- Reading A, simple emergence (§1.6): the trace is computed from prescribed relations, like a mass roll-up. It is not entered, so Chapter 7 does derive a result.
- Reading B, not an emergent result. term-emergence requires properties "at the level of the whole" that "cannot be attributed to any one component". The trace follows entirely from one element's own transition table and the event sequence the notebook chooses, with no mechanism, no time and no composition. The check therefore confirms the tool's execution semantics and guards against regressions in the table. It cannot fail for a reason about the design, which is the DL-018 concern in another form, although nothing is entered as a choice here.
- Recommended default: Reading B. The chapter derives no emergent result of the design. Its traces are specification execution: valid analysis that is not evidence about behavior in use. No ruling is needed to keep F-8's first bullet, which stands under either reading because "proves" and "behaviourally consistent" overclaim.

The handling of F-4 is not raised as an open question. It appears determined by §1.9 (name resolution is language tier) and DL-039 (record it, and have the tutorial supply a guard). One point may still need the orchestrator: whether the guard should resolve the `sysx:trigger` string, which is an OpenSysML export extension and not spec JSON, against the export. That is a builder-scope implementation choice under DL-039(3), and I did not assess it further.

## Contract premises that did not hold, and premises verified

1. **"Chapter 7 introduces simulation or state-machine execution, as its title claims."** This holds for state-machine execution: `execute_state` runs `Cycle` for two event sequences, and I reproduced both results. It holds only weakly for simulation.
   - The execution is untimed and has no context (`final_time` is `0.0`, `final_context` is `{}`). No mode performs anything (F-2), and unmatched events are silently dropped.
   - Notebook 03 evaluates a static relation over a grid. Whether that is "simulation" in term-simulation's sense is a wording question (F-8), not a model construct.
   - The chapter adds no dynamics, meaning no state-update relation (term-dynamical-system, Åström and Murray: `dx/dt = f(x, u)`).
2. **"Chapter 7 finally derives an emergent result instead of entering one as a choice."** This does not hold under the recommended default of OQ-2.
   - Credit where due: the model additions enter no result as a choice (PASS).
   - The only derived outputs are the state traces, which restate the prescription, and a Python-only evaluation of `DeliveredEnergy`.
   - Nothing derives cycle time. The sweep holds duration at the entered 120 s (F-6). DL-018's defect is therefore inherited unchanged and now feeds the analysis that Chapter 8 is said to cite.
3. **"Is the denotation of Start/Finish/Cancel resolved here?"** No. It is still undecided and the model still does not state it.
   - The three item defs are unchanged from Chapter 4 and have no `doc`.
   - Chapter 7 adds a fourth, event-like use (accepted triggers; notebook 02 cell 6: "waiting, running, finished, and aborted"). `BreadLoader::bread : Start` and `BreadEjector::bread : Finish` still type bread by them, and Chapter 4's text still says bread entering and toast exiting.
   - F-4 adds that, in the tool, the triggers do not even refer to the item defs. The model as loaded does not connect `Cancel` to the cancel transition.
4. **The citation "DL-037: undecided, model must state it" is wrong.** The Start/Finish/Cancel ruling is DL-036. DL-037 is `BreadEjector`'s naming. The same off-by-one drift appears elsewhere. These files are outside my blast zone; I report the drift and do not fix it.
   - `decisions/pass4-backlog.md`:
     - §1 cites DL-033 for `slow` (the log has DL-032) and DL-035 for assumptions (DL-034).
     - §2 cites DL-037 for the item defs (DL-036).
     - §3 cites DL-038 for naming (DL-037).
     - §4 cites DL-036 for measures (DL-035).
     - §5 cites DL-034 for judgment records (DL-033).
   - The "Confirmed extensions" list in `z-principles.md` cites:
     - DL-033 for F7 applied to usages (the log has DL-032);
     - DL-034 for judgment records (DL-033);
     - DL-035 for assumptions (DL-034);
     - DL-038 for naming (DL-037).
5. **"Start/Finish/Cancel are used as state-machine triggers in Ch8"** (backlog, "Cross-chapter dependencies"). They are introduced as triggers in Chapter 7. Chapter 8's fixture differs from Chapter 7's only in the header comment.
6. **"Notebook 02 uses Start/Finish/Cancel per the CONSTRUCTION_NOTEBOOKS context stubs."** This holds as text (lines 149 to 155). The stubs have no effect, though, because OpenSysML does not resolve the trigger names (F-4(c)).
7. **"Lint hits: none for ch07."** Verified: `glossary lint` reports no hit in `chapters/ch07-execution/`.
8. **Conformance CLI.** It ran as specified. Chapter 7 adds no gap finding. Both project checks stay `blocked` on the inherited ch05 violations, with exit code 0, since only `failed` sets exit code 1.
9. **Audit coverage of the baseline.** There is no `ch06-layer-audit.md`, so the ch06 baseline (`HeatingElement`, `ResistanceCoil`, `PowerWire`, `HeatingAssembly`, `weak`, `efficient`, `heatingEvidence`, `HeatingReq`) has not been audited. It appears here only where the Chapter 7 analysis touches it (`HeatingReq`, `Heater::power`).

## Constructs that could not be classified cleanly

- `Cycle` and its transitions: the skill and AGENTS.md §1.5 give no state-machine idiom for any layer. I classified them by the four questions alone, and the `Finish` transition depends on OQ-1.
- The trigger relation between each transition and `Start`, `Finish` and `Cancel`. The spec makes it a typed accept payload. The tool keeps only a string, so I could classify it only from the source text, not from any query surface (F-4).
- The eight `FeatureMembership`s and the `OwningMembership` are ownership relationships with no content of their own. They are not classified.

## Recurrence of known patterns (`decisions/pass4-backlog.md`)

| Backlog item | In Chapter 7's additions |
|---|---|
| §1 result entered as a choice | Not in the model additions. It recurs in the analysis: the sweep fixes duration at the entered 120 s (F-6). |
| §2 mechanism inside the functional layer; efficiency unbounded | Recurs in the analysis: the bound is stated only in Python (F-5). |
| §3 logical-to-physical chain missing | Recurs: `Cycle` has no carrier, no `exhibit` and no `perform` (F-1). |
| §4 no measures declared | Recurs: a Python-only 50 kJ threshold stands in for a measure (F-6). |
| §5 judgment and evidence mislabeled | Recurs: a Python-only sweep is called "simulation evidence" for Chapter 8's record (F-6). |
| §6 system of interest | Recurs in the ch05 F-6 form (F-1). |
| §7 tool gaps | New: trigger name resolution (F-4). |
| §8 fixture and infrastructure | New: construction stubs that are never exercised (F-4(c)). |
| §9 text disagrees with the model | Recurs (F-8). |
| §10 lint | No hits. World labels are present (parked under DL-028). |
| §11 figures | Recurs (F-7). |

## Not checked, and why

- **Chapter 8's judgment record** that notebook 03 says cites the sweep: it belongs to another chapter.
- **The Chapter 7 exercise** (`exercises/ch07/exercise.ipynb`): out of scope.
- **Whether OpenSysML executes `ApplyHeat`** (F-8, "first executable behavior"): not probed.
- **The spec's section numbers for states and transitions:** the formal/2026-03-02 PDF is not in `glossary/sources/local/`. The grammar facts come from the `SysML.xtext` vendored in the sysml-toolkit checkout, not from the formal release. I did not confirm that the release's grammar for triggers is identical.
- **Whether sysml-toolkit's "unresolved reference" should be an error:** not assessed. I cite it only as corroboration that the names are resolvable and that OpenSysML does not resolve them.
- **Open upstream issues for F-4:** not checked, and nothing was filed.
- **The rendered SVG:** I produced it only in a scratch copy and did not inspect its content. F-7 rests on the cell source and on the fact that the file is written and never displayed.
