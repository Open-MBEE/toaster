# Phase 1: the per-chapter diagram survey

A read-only inventory of where a diagram should be added to, or should replace a text-heavy
output in, each chapter's notebooks — per
[`docs/superpowers/specs/2026-09-28-diagram-survey-design.md`](../docs/superpowers/specs/2026-09-28-diagram-survey-design.md)'s
Phase 1. No notebook was edited, no diagram was rendered, and no implementation happened in
this pass: every finding below is a recommendation, not a committed change. Implementation
(actually building these diagrams, chapter by chapter, through the builder/reviewer pipeline)
is **not specced here**, per the design's own Non-goals, and starts only once Z has reviewed
this document.

## Method

Ten read-only research agents ran in parallel, one per chapter, each given: that chapter's real
notebooks, its real cumulative model, Phase 0's real-fixture capability matrix
([`decisions/diagram-study-real-fixtures.md`](diagram-study-real-fixtures.md)), the
already-corrected renderer-choice table (`.claude/skills/sysml-diagrams/SKILL.md`), the
`containment_subgraph()`/`model_to_dot()`/`build_interconnection_intent()` tooling already built
for scoped diagrams, and the fixed visual-syntax progression below (spec decisions 2 and 7),
which every agent was told not to redesign. Each agent scanned every notebook cell's output for
a large, dense text or string block — the concrete placement signal decision 7 names — and was
told explicitly not to invent a diagram for content no adopted tool can draw (no chapter
recommends the OMG pilot or SysMLD/sysml2d anywhere; both are confirmed broken on real content by
Phase 0).

**Fixed visual-syntax progression (not re-derived by any chapter's agent):**

| View type | First available | First actually introduced, per this survey |
|---|---|---|
| Structure/containment | Ch1 | **Ch1** — the tutorial's first diagram anywhere (two instances: edgeless boxes, then full composition+typing) |
| Action-flow | Ch4 | **Ch4** |
| Interconnection | Ch5 | **Ch5** |
| State | Ch7 | **Ch7** |

## Consistency check (per the spec's own Verification section)

- **Progression ordering:** confirmed. No chapter proposes a view type before the chapter the
  fixed table assigns it to; every "new" marking in the tables below lines up with exactly one
  first-introduction chapter per view type, matching the table above exactly.
- **Tool choice against Phase 0's capability matrix:** confirmed. No chapter recommends the OMG
  pilot or SysMLD/sysml2d (both confirmed to fail on all real content, `diagram-study-real-fixtures.md`).
  Every recommended tool/function (`model_to_dot()`, `containment_subgraph()`,
  `render_interconnection()`/`build_interconnection_intent()`, OpenSysML's `-render` CLI, and
  sysml-toolkit for one specific cell) is one Phase 0 or the `sysml-diagrams` skill already
  confirmed working on real content.
- **A real tool-rendering gap surfaced independently by nearly every chapter's agent, not
  assumed from one report alone:** `model_to_dot()` has no node/edge handling for
  `RequirementDefinition`/`RequirementUsage`, `ItemDefinition`, `ActionDefinition`/`ActionUsage`/
  `perform`, `SatisfyRequirementUsage`, `AllocationUsage`, `ConstraintUsage`, or specialization
  (`:>`) — only `PartDefinition` nodes and `PartUsage` composition/typing edges. Chapters 2, 3, 8,
  9, and 10 all independently rejected candidates specifically because their real content
  (requirements, satisfy claims, constraints, allocations, judgment-record prose) has no
  diagram-type representation in this tutorial's current toolset — not a gap in any one agent's
  effort, a real, confirmed, repeated limit on what a diagram can currently show here.
- **One cross-chapter tool-weighting question, not resolved by this survey, flagged for Z/
  implementation:** Ch5's agent recommends upgrading Ch5's own existing, shipped interconnection
  figure from the in-house `render_interconnection()` to **sysml-toolkit** (real port-name boxes,
  not just an edge label), because that chapter's whole point is a conjugated port. Ch6's agent,
  by contrast, keeps the in-house `render_interconnection()` for its own allocation-edge diagrams,
  reasoning that port-box detail isn't the pedagogical point there. Both are internally
  consistent, justified judgment calls — not a contradiction — but they mean "which renderer for
  interconnection" is not a single fixed answer across the tutorial. Decide this explicitly before
  implementation, rather than letting it default silently per notebook.

## Totals

16 diagram placements proposed across 9 of 10 chapters (Ch9 has zero — a legitimate, expected
null result, not a gap in the survey: its real content is coverage/sufficiency/staleness data
over judgment records, none of it model structure). 4 of those 16 introduce a view type for the
first time anywhere in the tutorial (Ch1 structure x2, Ch4 action-flow, Ch5 interconnection, Ch7
state — 5 "new" markings in total since Ch1 alone has two new-notation diagrams); the rest reuse
notation an earlier chapter already established.

---

## Chapter 1 — system-purpose

Chapter 1 sits at the very start of the visual-syntax progression, so it can only ever propose
structure/containment diagrams. The chapter's own narrative already splits structure into two
deliberate steps — bare, unrelated part defs (notebook 02) before a composed whole with real
composition/typing edges (notebook 04) — so the diagram sequence mirrors that: the plain box
first (zero edges), then the first diamond (composition) and dashed (typing) arrows together once
there is something to connect. Every notebook in this chapter loads the same already-complete
cumulative model, so every proposal below is scoped specifically to avoid showing the chapter's
own later content before it's taught. Notebooks 01 and 03 have no candidate: their content
(item/action defs, specialization) has no representation in `model_to_dot()` at all.

| notebook | cell/output under consideration | proposed diagram type | proposed tool/function | add-or-replace | visual notation introduced | rationale |
|---|---|---|---|---|---|---|
| `02-part-def.ipynb` | cell-09: a short print loop over `PartDefinition` names | Structure (nodes only, no edges) | `model_to_dot(model, elements=[hs, cs])` | add | **new** — first diagram in the tutorial, zero edges | Two disconnected boxes is the simplest instance of the vocabulary, matching the chapter's own text ("two part definitions can exist side by side with no relationship yet"); edges deliberately deferred to notebook 04. |
| `04-composition.ipynb` | cell-11: a 3-line `.id` dump of `parts()`/`attributes()` | Structure (full composition + typing) | `model_to_dot(model, elements=containment_subgraph(model, "ToasterDemo::Toaster", relations=("composition","typing"), depth=2))` | add | **new** — first diagram with any edge (diamond composition, dashed typing) | The chapter's structural capstone; completes the box-then-line progression right where the model becomes "structurally complete for Chapter 1." |

No candidate in `01-abstract-def.ipynb` (item/action-def content — the fixed table assigns this
to the action-flow view, Ch4, not Ch1; `model_to_dot()` also has no handling for it) or
`03-specialization.ipynb` (the `:>` relationship has no edge type in `model_to_dot()` at all, and
no approved tool draws one).

## Chapter 2 — requirements

Chapter 2 adds no new part-structure vocabulary — its only structural deltas are two new usages
(`nominal`, `slow`) typed by the already-existing `Toaster`. Its real new content (`requirement
def TimelyToast`, the `attribute :>> cycleTime` override, the Hawkins `asserted_context` judgment
record) is invisible to `model_to_dot()`: no node type for a requirement, no edge for an
override's value, and judgment-record fields are Python, not model structure. The one genuine
candidate reuses Ch1's vocabulary to orient the reader to the (mostly unchanged) part skeleton
before they read the requirement/override text in detail — it cannot and does not attempt to
show the requirement or override itself.

| notebook | cell/output under consideration | proposed diagram type | proposed tool/function | add-or-replace | visual notation introduced | rationale |
|---|---|---|---|---|---|---|
| `03-judgment-context.ipynb` | cell-02: `print(source)`, a ~45-line verbatim model dump, the chapter's densest output | Structure/containment | `model_to_dot(model)` (whole model) | add (not replace — the raw source still shows requirement/override syntax the diagram can't) | reused | Matches decision 7's placement signal exactly; lets the reader see the containment/typing skeleton at a glance before parsing the text in detail. |

No candidate in `01-requirement-def.ipynb` (the requirement's own `subject`/`require constraint`
body has no `model_to_dot()` representation; a diagram here would omit the notebook's whole
point) or `02-assumptions.ipynb` (no dense output; the `attribute :>>` override is also invisible
to the tool).

## Chapter 3 — measures

Chapter 3 adds a `RequirementUsage`, a folded satisfy claim, two judgment records, and a
`VerificationCaseDefinition` — almost none of it part/containment structure. `model_to_dot()`
cannot draw any of `TimelyToast`, `timely`, the satisfy assertion, or `TimelyToastTest`: the
strings "Requirement," "Verification," and "Satisfy" appear nowhere in that function. The one
legible diagram available is a part-skeleton view of what's structurally unchanged since Ch1/Ch2,
which can supplement but never fully replace the requirement/satisfaction-heavy text. No new
notation is introduced.

| notebook | cell/output under consideration | proposed diagram type | proposed tool/function | add-or-replace | visual notation introduced | rationale |
|---|---|---|---|---|---|---|
| `03-threshold-judgment.ipynb` | cell-02: an 83-line verbatim model dump, by far the densest output in the chapter | Structure/containment (parts only) | `model_to_dot(model)` | add (partial — cannot replace; see caveat) | reused | Matches the placement signal exactly, but the diagram can only orient the reader to the pre-existing part skeleton — it cannot show `TimelyToast`, the folded satisfy claim, or `TimelyToastTest`, which is the dump's actual point. |

No candidate in `01-moe-definition.ipynb`, `02-mop-candidate-eval.ipynb`, or
`04-verification-case.ipynb` — outputs are too short to trigger the signal, and each notebook's
real new construct (a requirement usage, a folded satisfy claim, a verification case def) has no
`model_to_dot()` representation regardless of output length.

## Chapter 4 — functional-decomp

Chapter 4's real payload is the tutorial's first action decomposition (`ApplyHeat` nested inside
`ToastBread`'s body) — exactly the chapter decision 7 marks as the first-available slot for
action-flow notation. The primary new diagram is an action-flow view of `ToastBread`, sitting next
to (not replacing) the text that teaches the construct's syntax. Structure/containment is also
present (the carried-forward part hierarchy) but reused, not new, and secondary to the action-flow
opportunity. Notebook 02 (three deliberately unwired signal `item def`s) has no candidate — there
is no relational content for any diagram type to show.

| notebook | cell/output under consideration | proposed diagram type | proposed tool/function | add-or-replace | visual notation introduced | rationale |
|---|---|---|---|---|---|---|
| `01-action-def-ffbd.ipynb` | cell-14: a ~19-20 line raw-text dump of `ApplyHeat` and `ToastBread`'s reopened body | Action-flow | OpenSysML CLI, `-render #action:ToasterDemo::ToastBread -render-form dot` | add | **new** — first action-flow diagram in the tutorial | The cell is literally the raw text of the chapter's one real decomposition; a drawn `start → applyHeat → done` sequence replaces eye-parsing with a picture, at the chapter decision 7 names as the main pedagogical opportunity. |
| `03-completeness-check.ipynb` | cell-02: a 115+-line verbatim model dump | Structure/containment, scoped | `model_to_dot(elements=containment_subgraph(model, "ToasterDemo::Toaster", depth=2))` | add, not full replace (covers only the Part-structure portion of the dump) | reused | Densest text block in the chapter; lets the reader visually confirm "same composed `Toaster`, unchanged" instead of re-reading boilerplate. Redundant with notebook 01's action-flow diagram if both are adopted — no second action-flow diagram needed here. |

## Chapter 5 — architecture

Chapter 5 should do two things: tame its one genuinely dense, three-times-repeated text block (the
full cumulative-model source, printed verbatim in all three notebooks) with a reused structure
diagram added once, not three times; and carry the chapter's one new notation, the
interconnection/port view — already rendered today via `build_interconnection_intent()` +
`render_interconnection()` in `03-interfaces.ipynb`. Because this chapter's entire narrative arc
is a conjugated port, and Phase 0 confirmed on this exact fixture that OpenSysML's interconnection
export collapses port identity to one edge label while sysml-toolkit draws real port boxes,
**port-box detail is judged pedagogically load-bearing here** — recommending an upgrade to
sysml-toolkit for this one cell (see the cross-chapter flag in Consistency check, above).
`02-allocate.ipynb` gets no diagram of its own: no tool exposes a dedicated allocation view, and
its one allocation is already shown, as an edge, in notebook 03's own interconnection diagram.

| notebook | cell/output under consideration | proposed diagram type | proposed tool/function | add-or-replace | visual notation introduced | rationale |
|---|---|---|---|---|---|---|
| `01-concept-selection.ipynb` | cell-02: a 131-line verbatim model dump | Structure/containment | `model_to_dot()` (unscoped — model still small) | add | reused | Densest text block in the chapter; the model is "too large to navigate by position," per the notebook's own text. |
| `02-allocate.ipynb` cell-06 / `03-interfaces.ipynb` cell-10 | ~~same 131-line dump, repeated verbatim~~ — **correction, 2026-10-02 (diagram/text integration Phase A):** this row was factually wrong. Direct re-read of the live files (and of this document's own commit history) confirms neither cell ever printed the full 131-line dump — each prints only its own small `TOASTER_INCREMENT` fragment (9 and ~15 lines respectively). See `decisions/diagram-text-integration-survey.md`'s own Chapter 5 section for the real finding and fix. | — | — | **no candidate** | — | Identical content already shown once in this chapter; a second/third copy would be diagram fatigue, not a real reduction in parsing burden. (Rationale for "no candidate" stands; the premise describing what these two cells print was wrong, not the conclusion.) |
| `03-interfaces.ipynb` | cell-16 (existing): the chapter's own pre-existing interconnection figure | Interconnection (port-level) | **sysml-toolkit** `--view interconnection --element ToasterDemo::Toaster` (upgrade from the in-house `render_interconnection()`) | replace (same cell, swap the rendering tool) | **new** — first interconnection view in the tutorial | Phase 0 confirmed directly on this fixture: OpenSysML draws zero port-name tokens (only the interface-level edge label); sysml-toolkit draws the real `durationIn`/`durationOut` port names. The chapter's entire subject is this one conjugated port — port identity belongs in a drawn box here, and this sets the visual vocabulary every later chapter's interconnection view reuses. |

## Chapter 6 — recursive-decomp

Chapter 6 introduces no new notation — its whole diagram job is to show the same three
already-established view types (structure, interconnection/allocation, action-flow) one level
deeper than any earlier chapter went, which is exactly the chapter's own content (a function
nested inside a function; a carrier composed inside a carrier). The chapter's own fixture is the
live demonstration that "deeper" isn't free: `Toaster::heating` is typed by the abstract
`HeatingSystem`, with no edge to the concrete `HeatingAssembly`/`heatGen` — any diagram rooted at
`Toaster` (the familiar Ch1/Ch5 root) silently fails to show this chapter's new content, so every
proposal below roots at `HeatingAssembly` instead.

| notebook | cell/output under consideration | proposed diagram type | proposed tool/function | add-or-replace | visual notation introduced | rationale |
|---|---|---|---|---|---|---|
| `01-subsystem-requirements.ipynb` | cell-06: the `ApplyHeat` increment with its nested `generateHeat` step | Action-flow of `ApplyHeat` | OpenSysML CLI, `-render #action:ToasterDemo::ApplyHeat -render-form dot` | add | reused | Phase 0 confirms this exact element already renders cleanly on real content. The action-level counterpart of this chapter's "nest one level deeper" pattern. |
| `01-subsystem-requirements.ipynb` | cell-18: two multi-entry printed dict lists (`Allocations`, `Perform relationships`) | Interconnection/allocation of `HeatingAssembly` | `render_interconnection(build_interconnection_intent(model, "ToasterDemo::HeatingAssembly", depth=1))` | replace (the `Allocations` line only; perform relationships stay text, no supported edge kind) | reused | First occurrence of the new allocation; easier to parse as a picture than a nested list-of-dicts with a two-segment source chain. |
| `02-second-level.ipynb` | — | — | — | **no candidate** | — | Content is Hawkins judgment-record prose (measure-framing, mechanism-selection arguments) — human judgment, not a derived model view. The one structural addition (`ResistanceCoil :> HeatGenerator`) needs node/edge kinds `model_to_dot()` doesn't implement. |
| `03-stopping-judgment.ipynb` | cell-02: a 213-line verbatim model dump, the densest block in the chapter | Structure/containment, rooted at `HeatingAssembly` | `model_to_dot(elements=containment_subgraph(model, "ToasterDemo::HeatingAssembly", depth=2))` | add (the full source print stays) | reused, at the chapter's new root | This exact root/depth is the literal worked example in `containment_subgraph()`'s own test suite. Re-rooting at `Toaster` instead would reproduce Phase 0's own "wrong root chosen" pitfall and never reach `heatGen`. |
| `03-stopping-judgment.ipynb` | cell-06: perform/allocation dicts plus two eval booleans — AI-C06's own evidence base | Same interconnection/allocation view as the `01` row | `render_interconnection(build_interconnection_intent(model, "ToasterDemo::HeatingAssembly", depth=1))` | replace (allocation line only) | reused | Grounds the stopping judgment's own `subject_ref` in a picture at the exact point the judgment is assembled. |

## Chapter 7 — execution

Chapter 7's diagram strategy centers entirely on the state view: `Cycle` is the tutorial's first
state machine, and Phase 0 confirmed this exact fixture renders cleanly and correctly tracks a
real transition-retargeting mutation. This is decision 7's designed entry point for state
notation. `01-calc-energy.ipynb` and `03-param-sweep.ipynb` introduce nothing new — their content
is calc-level numeric characterization and a sweep already shown as a Matplotlib plot — so no
diagram is proposed for either.

| notebook | cell/output under consideration | proposed diagram type | proposed tool/function | add-or-replace | visual notation introduced | rationale |
|---|---|---|---|---|---|---|
| `02-state-traces.ipynb` | cell-12: the fully assembled `Cycle` state-def text | State-transition diagram of `Cycle` | OpenSysML CLI, `-render #state:ToasterDemo::Cycle -render-form dot` | add | **new** — first state diagram in the tutorial | `Cycle` is the tutorial's first state machine; Phase 0 confirmed 100% success and correct mutation-tracking on this exact fixture. |
| `02-state-traces.ipynb` | cell-20/21: the trigger-typo negative control (`accept Start` → `accept Strat`), caught only by the tutorial's own guard | State-transition diagram of the typo'd `Cycle` | Same OpenSysML CLI, run against the typo'd source | add | reused (same notation, two cells later) | **Flagged as unconfirmed by its own agent**: plausibly the renderer labels edges with the trigger name, letting a reader catch "Strat" by eye — but this needs to be confirmed by actually running the renderer before being adopted, not assumed. |
| `02-state-traces.ipynb` | cell-22/24: three short `execute_state` traces | State diagram with the traced path highlighted | Same base diagram; path highlighting is presentation-only | add (supplement, not replace — traces are short enough to read as-is) | reused | Lets a reader see the traced path against the full transition table at a glance. |

## Chapter 8 — checking

Chapter 8 introduces no new notation and adds no new part/port/connection/action/state element —
only a package-level constraint and an unbound usage. Its real hallmark (the hand-restated lemma,
the Z3 proof, the `violated`/`undecided` contrast) is entirely satisfy/verify/proof content, and
per Phase 0's own "Scope and non-coverage" finding, no adopted tool has a dedicated requirement or
satisfaction view. This chapter's actual point — that a property can be proved, refuted, or
genuinely left undecided — has no diagram-type representation in this tutorial's toolset, and
none is invented. The one candidate is a modest reuse of the structure view to ground a specific
prose claim, not a stand-in for the proof narrative.

| notebook | cell/output under consideration | proposed diagram type | proposed tool/function | add-or-replace | visual notation introduced | rationale |
|---|---|---|---|---|---|---|
| `01-invariant-def.ipynb` | cell-03 markdown: the claim that `heatGenCheck` sits alongside `rated`/`weak` as "just another usage" of `HeatGenerator` | Structure/containment | `model_to_dot()` (whole model) | add | reused | Grounds a structural claim the reader currently has to take on faith; does not and cannot show the lemma, constraint, or proof. |

No candidate anywhere else in the chapter — every other dense block is satisfy/verify/proof
content or judgment-record prose, neither diagrammable by any tool this tutorial has adopted.

## Chapter 9 — coverage-sufficiency

Chapter 9 adds no new model element and its content — a coverage join, a Hawkins sufficiency
reading over judgment-record text fields, a staleness check — is fundamentally Python-side
analysis, not SysML model structure. The one topically relevant view type (a requirement/coverage
diagram) does not exist in any adopted tool. Every notebook's printed output is also already
short — the dense-output signal never independently fires here either. **This chapter has zero
diagram candidates, an honest null result the spec itself anticipated, not a gap in the survey.**

| notebook | cell/output under consideration | proposed diagram type | proposed tool/function | add-or-replace | visual notation introduced | rationale |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | No candidates proposed in any of the three notebooks. |

## Chapter 10 — traceability-signoff

As the capstone, Ch10 queries the Ch8 model rather than adding structure of its own, so its
content is almost entirely dense dicts and long argumentative `ReviewRecord` prose — exactly the
output type the placement signal targets, but nearly all of it is traceability, judgment, or
sign-off *data*, not model *structure*, and no adopted tool draws a requirement, an allocation
chain, or a review record. The one genuine opportunity is orientation: before the chapter narrates
two parallel subject chains and dumps them into a dense table, a structure diagram could show the
real physical hierarchy underneath both. No new notation is introduced.

| notebook | cell/output under consideration | proposed diagram type | proposed tool/function | add-or-replace | visual notation introduced | rationale |
|---|---|---|---|---|---|---|
| `01-traceability-graph.ipynb` | Before the `requirement_coverage`/`traceability_graph` dict dumps, the chapter's densest structural printout | Structure/containment, whole-model (not root-scoped) | `model_to_dot()` | add | reused | The traceability table traces two subject chains, one of which (`nominal`/`slow`, typed-but-not-owned by `Toaster`) is unreachable by `containment_subgraph()`'s forward-only typing traversal from any single root — the same "wrong root chosen" pitfall Phase 0 already found. The whole-model default avoids it, at the cost of a larger figure needing scope/grouping at implementation time. |

No candidate in `02-judgment-synthesis.ipynb` (duplicates notebook 01's structural content without
showing anything new) or `03-engineering-signoff.ipynb` (adds no model structure; its content is
dict reprints and the sign-off record's own undiagrammable prose).
