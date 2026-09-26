# AGENTS.md — Toaster Multi-Agent Build Contract

This file is the binding contract for everyone who works on the Open-MBEE/toaster repository. It has two parts.

- **Part 1, Foundations**, says what the tutorial teaches, which sources define its terms, how the three architecture layers differ, and how models are built and queried. It is role-agnostic and stable. It governs wherever Part 2 conflicts with it.
- **Part 2, Roster and authority**, is the earlier role, file-authority and escalation material. It is **legacy, pending rebuild** in a later pass (see `decisions/next-passes.md`). Treat it as the current authority matrix until then.

A cold session should reach working alignment from `CLAUDE.md`, this Part 1, the skills it lists, and the glossary CLI. Nothing here depends on conversation history.

---

# Part 1 — Foundations

## 1.1 What the tutorial teaches

A learner recursively breaks a system down until the leaves are concrete component definitions that perform the intended behavior, connect through the specified interfaces, and are verified. The worked example is a toaster. The tutorial teaches, in this order of emphasis:

1. **SysML v2 is declarative, not procedural.** Its defining technical analogy is a database language: we build a model, then query and analyze it to check that it says what we intend.
2. **Functional (what), logical (how), physical (where)**, and the three boundaries between them (§1.5).
3. **Executable specifications** as the way to declare intended behavior.
4. **Recursive decomposition**, adding detail so that a design can be validated against intended behavior.
5. **Model checking and simulation are complementary**: formal properties on one side; scenarios, trajectories and analysis of results on the other.
6. **Sites of engineering judgment and the evidence base behind them.** Judgment is never eliminated (§1.6).
7. **Coverage and traceability** in service of the accountable engineer's sign-off.
8. **Explicit and implicit construction** balance a complete model against a readable narrative (§1.7).
9. **Diagrams are purposeful, judged views of the model** (§1.7).

The conceptual (stakeholder) layer above the functional layer and the procurement layer below the physical layer are out of scope by design. Only the boundaries between functional, logical and physical are taught.

## 1.2 Sources, and what kind of definition each supplies

The sources are not rivals. Each supplies a different **kind** of definition, and the kinds fit together:

| Kind | Source | Supplies |
|---|---|---|
| Idea (conceptual) | SEBoK v2.14; Hawkins et al. 2011 (judgment taxonomy); Åström and Murray and Sutton and Barto (for *mechanism* and *policy* only) | What the concept means and why it matters; generic and informal |
| Formal semantics | The OMG specs: SysML v2.0 language, API and Services v1.0, KerML 1.1 Beta 2 | Checkable semantics; the language we execute |
| Story (didactic) | Brian Douglas, *Systems Engineering* playlist, Parts 3 and 4 | Analogy, example, and the toaster case; how we convey the material, aligned with as far as possible to lower the learner's cost |
| Bridge | This tutorial | Contextual refinements that tie the kinds together for the learner |

**Toolchain, not sources.** OpenSysML, sysml-toolkit, the Pilot Implementation and the like execute the specs. They are cited only to flag a spec gap (§1.9), never to define a term.

**Refinement rule.** Canonical definitions come first. Our own definitions appear only as contextual refinements where needed to make learning easier, and each records the canonical edge it refines. A refinement narrows or clarifies; it never contradicts a source and never invents. One departure is approved: SEBoK's *logical architecture* contains the functional view, whereas the tutorial separates a functional layer from a logical one, so "logical" is a recorded `differsFrom` edge approved by Z (DL-015). Learners are told the word is used more narrowly than SEBoK uses it, and that Douglas's "who" is this tutorial's "how".

## 1.3 The glossary is the source of truth for terms

- Before defining or using a load-bearing term, look it up: `uv run python -m glossary lookup TERM` (all edges), `compare TERM`, and `tutorial TERM` (the idea, formal semantics and story that the tutorial uses, plus its own refinement if any).
- Definitions change only through the graph (`glossary/`), validated by `uv run python -m glossary check`. Agents propose; only Z confirms a definition.
- One-line glosses in this file sit between `<!-- gloss:ID -->` markers and are **generated** by `uv run python -m glossary render`. Do not edit them by hand.
- Use `uv run python -m glossary` for the command list. See the `tutorial-glossary` skill.

## 1.4 Two languages, one loop

**SysML v2 is declarative** and is the authoritative source of semantics: canonical semantics come from the specs; user-defined semantics live in the model (attribute types and units, `calc def` relations, MoE and MoP metadata, `doc`). **Scientific Python is the complementary procedural language.** It analyzes: simulation and sweeps, figures, and queries of the model. It never defines what the model means. A number produced in Python without a model-defined unit and relation is not evidence.

The engineer's job is to align the model to their intent through **loops of construction and analysis of what was constructed**. Every chapter is one turn of that loop, and a negative control shows that the loop can detect a mismatch. Simulations produce the evidence base; judgments about whether requirements are satisfied rest on that evidence and point at it. They do not replace it.

## 1.5 The three layers

<!-- gloss:functional-architecture -->Intended behavior, stated solution-independently: functions with typed flows, the phenomena relations among them, and the MoEs.<!-- /gloss -->

<!-- gloss:logical-architecture -->Prescribed mechanisms and policies carried by logical components, plus the interfaces between them; MoP thresholds are derived here.<!-- /gloss -->

<!-- gloss:physical-architecture -->Concrete parts that realize the logical components and confer values; each must fit the logical interfaces and meet the derived thresholds.<!-- /gloss -->

| Layer | Answers | Stated as | Measure | SysML v2 idiom |
|---|---|---|---|---|
| Functional | What | *Intents*: required behavior, with typed flows and the relations among phenomena (an energy **balance** inequality, which respects conservation without assuming perfect efficiency) | **MoE** | `action def` with typed in and out flows; calc or constraint for phenomena relations; behavioral `requirement def` |
| Logical | How | *Prescriptions* (mechanisms, policies, interfaces), plus the derived intents (MoP thresholds) they must meet | **MoP** | `abstract part def` with `perform action x : ActionDef`; `port def`, `interface def`, flows; constraints stating the principle; `allocate`; derived requirements |
| Physical | Where | *Prescriptions* (parts, values), plus the assessed results | **TPM** | concrete `part def` specializing the abstract logical part def; attribute values (assessed values are TPMs) |

Key terms (glossed from the glossary):

- **Mechanism.** <!-- gloss:mechanism -->A prescribed, comparatively deterministic input-to-output relation: a modeling decision grounded in engineering practice, a law we use to reason about behavior. Not itself the behavior.<!-- /gloss -->
- **Policy.** <!-- gloss:policy -->Decision guidance that selects inputs given the state, typically to close the loop under uncertainty; designed given the available mechanisms.<!-- /gloss -->
- **Logical component.** <!-- gloss:logical-component -->The prescribed carrier of a mechanism, with its interfaces; modeled here as an abstract part definition that performs an action.<!-- /gloss -->
- **Selection among alternatives.** <!-- gloss:selection-among-alternatives -->Choosing among alternative mechanisms by trade study against the derived measures.<!-- /gloss -->
- **MoE.** <!-- gloss:moe -->A measure of stakeholder satisfaction with the outcome: a measurable attribute with a unit and a means of collecting data (for the toaster, how evenly the bread is toasted). Stated at the functional layer.<!-- /gloss -->
- **MoP.** <!-- gloss:mop -->An engineering measure of performance: a measurable attribute with a unit and a means of collecting data (for the toaster, power efficiency). It characterizes a requirement, which also needs a threshold. Typically logical.<!-- /gloss -->
- **TPM.** <!-- gloss:tpm -->The value assessed on a design element by analysis or simulation: the evidence against a MoP threshold.<!-- /gloss -->
- **Allocation.** <!-- gloss:allocation -->Assigning functions to logical components, and components to parts: SEBoK's idea, SysML v2's allocate, Douglas's grouping.<!-- /gloss -->

**MoE → MoP → TPM is a derivation chain.** A MoE says what acceptance looks like; a MoP is a performance measure whose threshold is derived so that the MoE can be satisfied; a TPM is the value actually assessed on a design element. Each can be stated on any element as decomposition proceeds, and reasoned over from parts through interconnections to higher-order parts. In the SysML spec they are only metadata tags on attributes (§9.3.4), and neither SEBoK nor the spec ties them to layers, so the layer emphasis is a tutorial refinement. A MoP characterizes a requirement but does not make one: the requirement needs a threshold and a means of checking it. **Whether a measure is a MoE or a MoP is a modeling judgment for the case at hand**, recorded with its justification (who cares, and does it measure acceptance or engineering performance). How long toast takes could be either, and a hard case is a good place to show a judgment call.

**The system of interest is the subject the layers describe, not a layer.** Its purpose statement is functional, its parts and arrangement are logical, its realized parts are physical; a bare top-level part def that only names the whole is the named subject. Classify the pieces.

**A verification case is not itself a layer element.** A `verification def` (and the checks it runs) is the analysis half of the construct-and-analyze loop. Classify it by the layer of what it tests and by its tier (language, or staged project conformance); its verdict is evidence, and TPMs are the values it assesses.

**Allocation is not realization.** `allocate` assigns functions (and requirements, budgets) to elements. A concrete part def *specializes* the abstract logical part def to realize it. Usage-level allocation of a logical component to a part is optional.

**Constraints, split by solution-independence.** A constraint that holds for any solution (energy conservation) frames the problem and stays functional. A constraint that exists only because of a chosen mechanism or interface (Joule heating, I^2 R, as applied to a coil; outlet-to-plug compatibility; a derived MoP threshold) is logical. Physical laws such as Joule heating are mechanisms: modeling decisions grounded in established engineering practice, the laws we reason with. Stated for a chosen component, they are logical; a law that holds for any solution stays functional.

**Numbers.** A MoP's definition and threshold are requirements at the layer that states them. What a specific part has, or is estimated to have, is the TPM. Sizing choices (fuel volume, tong length) appear only when a physical part is chosen.

**Boundary tests**

- *Functional to logical (substitution test).* If a pop-up toaster and tongs-with-a-blowtorch would both satisfy the statement, it is functional. If it commits to a mechanism, it is logical.
- *Logical to physical.* If any part built to the stated interface and derived thresholds satisfies it, it is logical. It is physical when a specific part def is named and its values are chosen.
- *Conceptual to functional.* Would the stakeholder recognize it as a need? Do not invent functions they have not asked for.
- *Prescribed versus emergent.* Is it something the design chooses (an element, relationship, principle or parameter) or something expected to result from those choices (a behavior or performance)? Choices are stated in the model. Results are derived by analysis and checked against intent, and a result must never be entered as if it were a choice. A cycle time set as an attribute default and then "verified" against its threshold is a prescription tested against a threshold, not emergent behavior.

**Connectivity differs by layer.** Functional connectivity is behavioral dependency (you cannot apply heat without an energy source). Logical connectivity is interface compatibility: an outlet feeds a pop-up toaster, a fuel tank feeds a blowtorch, and the arrangement is settled before sizing.

## 1.6 Prescribed versus emergent, and judgment

A design can only *prescribe* elements, relationships and principles. <!-- gloss:behavior -->The emergent outcome of a system in use; not prescribed but derived by analysis or simulation and judged against intent.<!-- /gloss --> The aim is not to eliminate emergence but to make desirable emergence likely. So the model states intents and prescriptions, and behavior is derived and checked, never asserted.

Emergence: <!-- gloss:emergence -->Properties or behaviors that arise at the level of the whole and cannot be attributed to any one component. SEBoK distinguishes simple, weak and strong emergence.<!-- /gloss --> SEBoK's three kinds map onto the layers by how a value is obtained:

- **Simple** emergence (computable from well-understood parts and relations, such as a mass roll-up) is typical of the logical layer. Its MoPs are derived by composing relations symbolically, and the numbers arrive when a physical candidate supplies part values.
- **Weak** emergence (needs simulation, modeling or experiment) is typical of the functional layer's intents, such as "toasted to the user's liking". Stability straddles both: an analytic form that can be model checked, plus simulated trajectories and failure modes.
- **Strong** emergence (unanticipated; seen only in integration, test or operation) belongs to no layer. It is what sign-off judges.

These are tendencies, not rules. The stable distinction is *computed versus explored*.

**Judgment is never eliminated.** Prescribing does not guarantee, weak emergence is explored and not settled, and strong emergence cannot be anticipated, so real design rests on assumptions and on partly subjective calls. What makes them rigorous is an evidence base and explicit justification, which Hawkins's judgment taxonomy structures. <!-- gloss:judgment -->Completely mitigating all assurance deficits is not normally achievable, so a judgment on when they can be tolerated is necessary, assessed by expert judgment of likelihood and severity.<!-- /gloss --> <!-- gloss:assurance-deficit -->Any knowledge gap that prohibits total confidence.<!-- /gloss --> Engineers are not trying to remove judgment calls; they are experts at making contextually appropriate, evidence-informed ones. No tutorial text may describe a passing check as proof, imply that everything is reducible to what can be computed, or record a disposition as "accepted" (SA-7 stands). A judgment record's `counterevidence` and `residual_uncertainties` fields are load-bearing for this reason.

## 1.7 Building the model and showing it

**Explicit and implicit construction.** The model needs more parts than a learner should build by hand, so two kinds of construction coexist. **Explicit** constructions are walked through in the notebook. **Implicit** ones are coded in other Python files that the notebook only imports. The model is complete by the end, with only explicit construction on the page.

- Implicit parts obey the same layer rules and the glossary as everything else, and their provenance is never hidden.
- Legibility comes through diagrams: every chapter shows the assembled model so that explicit and implicit parts are distinguishable without reading the Python.
- Implicit parts are authored and verified before the notebooks that import them.
- OpenSysML v0.9.0 does not resolve `import` across separately loaded sources. A notebook therefore assembles the SysML text from the imported modules plus its explicit increment into one source and loads that (gap G7, §1.9).

**Diagrams are views of the model, drawn like scientific plots.** The model is the data; a diagram is a selected, purpose-specific view of it, produced by query and encoding, never hand-drawn and never a second source of engineering facts. The tools supply methods. They do not decide the figure. We judge what to include and exclude and how to present it, according to what the diagram must communicate in its notebook, and record that in the figure's recipe and caption. Presentation settings (layout, orientation, short labels) never carry engineering content. A diagram of a modeled assertion is not evidence that the assertion holds: evidence comes from its own analysis. A structural diagram shows prescriptions; a plot of simulation output shows derived behavior, with units and relations read from the model. See the `sysml-diagrams` skill.

## 1.8 Recursion and stopping rule

Decompose until every leaf is a concrete component def that **performs** its specified behavior, **connects** through its specified interfaces, and has **verification evidence**. At each level the three boundaries in §1.5 apply again. Completeness is auditable: at every level, account for every input and output.

## 1.9 Querying, and tracking gaps

Three surfaces, in order of preference for a chapter notebook (recipes and limits are in the `opensysml-query` skill):

1. `model.query()` in OpenSysML: the API Query (select, where, scope, inverse; no traversal). It sees named elements only. Name your allocations, connections and flows and it sees those too.
2. `json.loads(model.to_api_json().content)`: the full export, including unnamed `satisfy`, `perform` and connector elements. Use it through the helpers in `src/toaster/query.py`, never ad hoc.
3. `Symbol` navigation (`model.find`, `.specializations`, `.children`).

The sysml-toolkit Python binding (`Session.from_files`) is a fourth surface that reads several files at once and sees unnamed elements. It is toolchain, not part of the chapter dependencies.

**Conformance has two tiers.** *Language conformance* (parse, name resolution, typing) is always on: a declaration that violates it breaks the load. *Project conformance checks* (interface compatibility, port types, flows accounted, coverage) are **staged**, because the model emerges iteratively and is not born complete: each check is declared as applied from a chapter and section onward, has a negative control that shows it catching a fault, and is reported as **open**, not passed, until it is applied. Discovering non-conformance early and flagging it to the user is what executable specifications are for. Tools may not diagnose a fault themselves (OpenSysML v0.9.0 accepts a power port connected to a fuel port; the KerML 1.1 spec searched has no validation constraint for it), so the tutorial supplies the check (recipe 5 in `opensysml-query`).

**Gap-tracking rule.** Use the spec-anchored construct. If a tool cannot express it, use a bare SysML fragment or custom Python. Every gap gets (a) a `DEFERRED.md` entry, (b) a toaster issue and, where the tool is at fault, an upstream issue, each citing the exact spec section and asking only for what the spec says, and (c) a comment cell wherever the workaround appears. Never work around a gap silently. Nothing is filed on a public repository until Z has reviewed the text.

**Probe before you assert.** A construct is described as working only after it has been run. The skills mark constructs as tested or untested.

## 1.10 Builder-facing lenses (never in learner content)

Some habits of thought guide how we build and validate the tutorial and are not part of what it teaches.

- **Tall's three worlds** (education and cognitive science) stay behind the scenes. Learner content never names them. Evaluation checks that the seam between model text, the tool that loads it, and the rendered result is addressed; that is an emergent behavioral requirement, not prescribed text.
- **Optimization and control.** Read the layers as objective (functional: what is good, what is good enough), design space (logical: typed, unit-bearing slots plus equality and inequality constraints, no solution values), and candidate (physical: a concrete point, checked for feasibility against the logical layer and for utility against the functional layer). Ask of any element which of the three it reads as.
- **Generalized dynamical systems.** A mechanism is a state-update relation, a policy selects inputs given the state, and we design policies from the mechanisms available. This informs Z's thinking and is not a source.

Learner-facing vocabulary from these lenses is allowed only where it makes a term easier to learn, and never load-bearing.

## 1.11 How alignment changes

Alignment passes (changes to this Part 1, the glossary's confirmed definitions, or the ACE skills) are Z-initiated. The ACE triages what needs Z: it rules and logs where Z's frameworks and principles determine the answer (and shows the reasoning), and escalates to Z with a concise request where they do not. Decisions are logged in `decisions/log.md` (§7 below). To reach the ACE, route the question through the orchestrator; if there is no orchestrator in your session, state the question and your recommended default in your report and it will be triaged. Proposals to the glossary (new terms, sources or edges) go to the ACE the same way; only Z confirms.

---

# Part 2 — Roster and authority (legacy, pending rebuild)

Roles rebuilt in Pass 2 live in `.claude/agents/` (currently `orchestrator`, `layer-auditor`, `ace`); where a role file exists it governs that role's duties, model and authority, and the matching legacy row below is superseded. Everything below is the earlier role and file-authority material, kept unchanged except where Part 1 or a rebuilt role replaced it. Where it conflicts with Part 1, Part 1 governs. Role ids (A1-A10) belong to this legacy roster only.

## 1. Shared domain context (story source: Douglas)

Every agent on this project knows Parts 3 and 4 of Brian Douglas's *Systems Engineering: Managing System Complexity* series (MathWorks MATLAB Tech Talks, 2020) cold. Both parts use a domestic toaster as the worked example; together they establish the engineering ground truth this tutorial re-implements in SysML v2 and Python.

### Part 3 — The Benefits of Functional Architectures (Oct 15, 2020, 14:24)

**Entry model.** Bread (input) → `toast bread` (function) → toast (output).

**First decomposition.** Three child functions: load/position bread, apply thermal energy, remove toast.

**Full decomposition.** Approximately 15 verb-noun functions covering: heat conversion, heat transfer, heat regulation, energy conversion, control signals, crumb management, bread handling, and sensory feedback.

**Function anatomy.** A function has three parts: inputs (material, energy, or signals), the process, and outputs. Functions describe WHAT, not HOW. They are implementation-agnostic.

**Auditing completeness.** Functional completeness is auditable: at every decomposition level you must be able to account for every input and every output. Any unaccounted flow is a gap.

### Part 4 — An Introduction to Requirements (Oct 28, 2020, 15:05)

**Requirement anatomy.** Every requirement has three parts: a description of the need, a rationale for why it is valid, and a verification method. A requirement without all three is incomplete.

**Verification method types.** Inspection, analysis, test, and demonstration. These four types classify how compliance will be checked and determine what evidence counts as meeting the requirement.

**Requirement types.** Functional ("shall convert electrical energy to thermal energy"), performance ("capable of up to 100 W conversion"), constraint ("mass less than 5 kg"), environmental, human factors, reliability, safety. The toaster illustrates each type.

**Requirement hierarchy.** Requirements cascade from stakeholder needs down to components. The toaster examples span from "must fit on a kitchen countertop" (system level) through spring specifications at the component level. Parent requirements decompose into child requirements; every child must be traceable to a parent.

**Verification vs. validation.** Verification: does the design comply with the requirement? Validation: does the requirement trace to a real stakeholder need? Both are needed.

**Connection to Part 3.** The functional architecture from Part 3 is the structure requirements attach to. A functional requirement is a claim about a function; a performance requirement quantifies an output flow.

---

## 2. File authority matrix

| Archetype | Can edit | Cannot edit |
|---|---|---|
| A2 Builder | `src/toaster/` (all 8 modules + `__init__.py`), `tests/`, `.github/`, `pyproject.toml`, `uv.lock`, `package.json`, `package-lock.json`, `myst.yml`, `scripts/`, `.gitignore`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `DEVELOPMENT_PLAN.md` | Chapter prose cells, `docs/` prose, `models/*.sysml`, `skills/` |
| A3 Modeler | SysML source cells in `chapters/*.ipynb`, `models/*.sysml` | Python code cells, prose cells, `tests/`, CI config |
| A4 Educator | Markdown/prose cells in `chapters/*.ipynb`, `docs/*.md`, `exercises/ch{N}/exercise.ipynb` (exercise problem statement only) | Python code cells in chapters, SysML source cells, `tests/`, CI config |
| A5 Technical Reviewer | READ ONLY | All source files |
| A6 Didactic Reviewer | READ ONLY | All source files |
| A7 Visualization Assessor | `figures/*.svg` (regenerate only when assigned) | All source files |
| A1 Orchestrator | READ ONLY | All source files |
| A8 ACE | `decisions/log.md`, `.claude/skills/**/*.md` | All source files (chapters, models, tests, CI, docs) |
| A9 Simulated Learner | READ ONLY | All source files |
| A10 Systems Architect | Narration markdown cells in `chapters/ch01-*/` and `chapters/ch04-*/` (functional architecture framing); SysML source cells in `chapters/ch02-requirements/` (requirement anatomy); SysML source cells in `chapters/ch03-measures/04-verification-case.ipynb`; `models/ch02-cumulative.sysml`, `models/ch03-cumulative.sysml` | Calculation defs, action defs, state machines, test files, CI config, `docs/` pages |

---

## 3. Editing discipline rules

1. One logical change per session. Commit immediately after the change.
2. A2: targeted tests pass before the session ends.
3. A3: `model.ok = True` for all chapter models before the session ends.
4. A4: never touch Python code cells or SysML source strings.
5. A5/A6: produce a structured review object; never edit source.
6. All agents: if a required change touches a file outside your remit, flag to the orchestrator.

---

## 3b. A10 Systems Architect

**Purpose:** Authors functional architecture narrative (verb-noun convention throughout), requirement definitions with full 3-part anatomy, and verification case specifications. Makes validation judgments over behavioral requirements.

**Layer framing:** the three-layer framing (what, how, where; prescriptions versus derived results) is defined in Part 1, section 1.5. A10 narrates the layers in that order and uses verb-noun convention for functions. The earlier wording here, which defined the logical layer as partitioning plus interfaces, is superseded (DL-015; the verbatim old text is recorded there).

**Skills loaded:** `sysml-v2-toaster-model`, `toaster-recipe`, `tutorial-style-guide`, `toaster-review-protocol`

**Coordination:** When A4 writes functional architecture narration (Ch1, Ch4), A10 reviews for verb-noun compliance and functional-first framing before A6 didactic review. A10 does not write physical architecture narrative.

**What A10 must never do:** Invent verification method kinds not in the SysML v2 spec; write `verify X` where X is a requirement def (it must be a usage); narrate physical implementation choices as functional requirements.

## 4. Escalation chain

A1 routes to A8. A8 handles, escalates to Z, or returns to A1. A1 never contacts Z directly.

---

## 5. What every agent must never do

- Never edit files outside your remit.
- Never produce `|| true` in shell commands.
- Never assert `model.ok` without actually loading and checking the model.
- Never set `record_kind = "actual_review"` — all records are worked examples (SA-7).
- Never invent opensysml API shapes not in the adapter file.
- Never re-open SA-1 through SA-9 without A8 logging and routing to Z.
- A5: never report PASS on a green test that doesn't exercise the claim — insufficient coverage = CANT_TELL.

---

## 6. Review output format

Reviewers return a structured dict:

```python
{
  "wp": "WP-N",
  "archetype": "A5",
  "verdict": "PASS|FAIL|CANT_TELL",
  "findings": [
    {
      "criterion": "...",
      "status": "PASS|FAIL|CANT_TELL",
      "evidence": "..."
    }
  ]
}
```

Overall verdict rule: any FAIL → FAIL; any CANT_TELL (with no FAIL) → CANT_TELL; all PASS → PASS.

---

## 7. Decision log format

Entries in `decisions/log.md` follow this structure:

```
## DL-NNN | YYYY-MM-DD | WP-N | [summary]

Path: Handled by ACE / Escalated to Z / Returned to A1
Decision: [what was decided]
Rationale: [why; what Z-pattern applied]
```
