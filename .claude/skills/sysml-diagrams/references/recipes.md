# Rendering recipes

**Corrected 2026-10-01** (this file was not updated when `decisions/log.md` `DL-057`
corrected `sysml-diagrams/SKILL.md`'s own renderer-choice table, so it kept describing the
OMG SysML v2 Pilot Implementation and SysMLD/sysml2d as the defaults for two view types after both were confirmed
to fail entirely on real content, `decisions/diagram-study-real-fixtures.md`; Phase 1's own
survey, `decisions/diagram-survey.md`, caught the gap). **Never use the pilot or
SysMLD/sysml2d for real chapter content.** Run from the tutorial repository root. `$SYSML`
is the pinned OpenSysML runtime CLI; `model.sysml` is the chapter-generated snapshot. Replace example
qualified names with the chosen subject. Write outputs to an ignored `build/figures/`
directory.

## Definition and decomposition — in-house, `model_to_dot()`

```python
from toaster.render import model_to_dot, containment_subgraph, render_dot

dot_source = model_to_dot(model, title="Decomposition")
# Or, once the full model is too large to be a legible single figure:
scoped = containment_subgraph(model, "ToasterDemo::Toaster", relations=("composition", "typing"), depth=2)
dot_source = model_to_dot(model, title="Decomposition", elements=scoped)
render_dot(dot_source, "build/figures/decomposition.svg")
```

Nodes are `PartDefinition`s (dashed border if abstract); edges are composition (diamond
arrowhead, owner to usage) and typing (dashed open arrow, usage to its type). `elements=None`
(the default) draws the whole `model.query()` result — right for a small model where
"everything" is itself a legible view. Use `containment_subgraph()`'s `root`/`depth` to scope
once the model grows too large, picking the root that actually reaches the content the chapter
teaches (`decisions/diagram-study-real-fixtures.md`'s own "wrong root chosen" finding: a usage's
qualified name does not own anything itself, only its *type* does, so the chapter's own new
content may sit at a different root than the familiar top-level one). **Known gap:** this
function has no node/edge handling for `RequirementDefinition`, `ItemDefinition`,
`ActionDefinition`/`ActionUsage`/`perform`, `SatisfyRequirementUsage`, `AllocationUsage`,
`ConstraintUsage`, or specialization (`:>`) — only `PartDefinition` and `PartUsage` composition/
typing. Do not propose this recipe for a notebook cell whose real content is one of those; no
diagram type in this tutorial currently covers them (`decisions/diagram-survey.md`'s own
repeated finding, Chapters 2/3/8/9/10).

Expected check: the selected elements and intended children appear with the correct ownership,
and nothing the chapter hasn't yet taught (a later chapter's own structure) leaks into an
earlier chapter's figure.

## Interconnection — in-house `render_interconnection()`, or sysml-toolkit when port identity is the point

**Default: `render_interconnection()`** (in-house, `src/toaster/render.py`), zero dependency on
a third-party tool:

```python
from toaster.render import build_interconnection_intent, render_interconnection

intent = build_interconnection_intent(model, "ToasterDemo::Toaster", depth=1)
render_interconnection(intent, "build/figures/interconnection.svg")
```

`build_interconnection_intent()` extracts parts, flows, and allocations from the model via
`model.query()`/`to_api_json()` — nothing is hand-authored, so there is no second,
separately-maintained model to drift out of sync (the exact risk `decisions/log.md` `DL-055`
found SysMLD/sysml2d's own intent-file approach carries, and which that tool's own indexer bug
now independently blocks on real content regardless). Port identity is drawn as an edge label,
not a dedicated box.

**Use sysml-toolkit instead specifically when port identity itself is the chapter's own
pedagogical point** (e.g. a chapter introducing or exercising a conjugated port, per
`decisions/diagram-survey.md`'s Ch5 recommendation):

```sh
sysmlv2 viz model.sysml --view interconnection --element ToasterDemo::Toaster -o build/figures/interconnection.puml
java -Djava.awt.headless=true -jar "$PLANTUML_JAR" -tsvg build/figures/interconnection.puml
```

Confirmed on every real fixture tested (`decisions/diagram-study-real-fixtures.md`): draws real
port names (e.g. `durationIn`, `durationOut`) as their own boxes inside the owning part, not
folded into one edge label the way the OpenSysML runtime's own interconnection export does. Otherwise, a
chapter using interconnection only to show a connection or an allocation — where port identity
is not itself the point — does not need the extra external-binary dependency; default to
`render_interconnection()`.

Before rendering, assert that selected relationships and endpoints match the model's own real
parts, ports, and connections — never author a separate relationship model by hand for either
pipeline.

## Action flow — OpenSysML runtime

```sh
"$SYSML" model.sysml \
  -render '#action:ToasterDemo::ToastBread' \
  -render-form dot -o build/figures/actions.dot
dot -Tsvg build/figures/actions.dot -o build/figures/actions.svg
```

Confirmed directly against real chapter content (`decisions/diagram-study-real-fixtures.md`;
Ch6's `ApplyHeat` action, exit 0, real action-flow notation). No in-house action-flow renderer
exists yet. Expected output: the declared actions, initial/final nodes, and successions. Check
decisions, guards, forks, joins, and object flows whenever the selected model contains them —
every real chapter fixture tested so far exercises only a linear sequence.

Distinguish a structural action-flow figure from an actual execution trace.

## State transition — OpenSysML runtime

```sh
"$SYSML" model.sysml \
  -render '#state:ToasterDemo::Cycle' \
  -render-form dot -o build/figures/states.dot
dot -Tsvg build/figures/states.dot -o build/figures/states.svg
```

Confirmed directly against real chapter content (`decisions/diagram-study-real-fixtures.md`):
100% success across both OpenSysML runtime render forms on Ch7's real `Cycle` state machine, and the
mutation-control test (retargeting a transition) correctly changes the rendered output. Show
states and transitions for one behavioral question. Preserve initial entry and, when present,
event triggers, guards, effects, and entry/do/exit compartments. Change orientation or split
nested behavior into another figure when labels become crowded.

Check each transition's source and target against the real model, not an assumed shape — a
changed target must change the corresponding arrow.

## Sequence — OpenSysML runtime and Mermaid

```sh
"$SYSML" model.sysml \
  -render '#sequence:ToastMessages::ToastExchange' \
  -render-form mermaid -o build/figures/sequence.mmd
mmdc -i build/figures/sequence.mmd \
  -o build/figures/sequence.svg -b white
```

The model owns lifelines, message endpoints, payloads, and event successions. Mermaid owns spacing, typography, and lifeline display. Use a small Mermaid configuration file when needed, committed as presentation configuration and supplied with `mmdc -c`.

Check message order against modeled event precedence, not source declaration order. The exercised example has three lifelines and four messages: start, energize, complete, notify. A sequence figure is a modeled interaction; label it as an observed trace only when its data actually comes from execution.

## Traceability graph — Graphviz

Query requirement, function, part, and verification relationships into rows with `source_id`, `relationship_kind`, and `target_id`, plus the selected nodes’ names and metaclasses. Use the engine’s resolved relationships, rather than inferring an edge from names or matching prose.

Generate DOT from these rows: stable IDs identify nodes; display labels contain model names and kinds; each edge carries its relationship kind. Group by subsystem or concern when that answers the question. Preserve direction according to the relationship’s semantics. Use a restrained dashed dependency style for assertion/allocation links, with an explicit legend; keep it distinct from composition and physical connections.

```sh
dot -Tsvg build/figures/traceability.dot \
  -o build/figures/traceability.svg
```

Assert edge tuples against the query result and inspect arrow direction and labels. Use a model-derived table or matrix instead when the question is whether every selected requirement/function has coverage. Leave missing relationships visible. A graph of `satisfy` or `verify` relationships does not substitute for evaluated evidence.

## Quantitative figures — Matplotlib

Use values obtained from model evaluation or execution. Keep any extracted table small and keyed by run, parameters, units, and model version. Set axis labels and units, distinguish targets from predictions and observations, and show uncertainty only when supported by the data.

```python
fig, ax = plt.subplots()
ax.plot(duration_s, delivered_energy_j)
ax.set(xlabel="Duration (s)", ylabel="Delivered energy (J)")
fig.savefig("build/figures/energy.svg", bbox_inches="tight")
```

Here the arrays come from the notebook’s model experiments. Verify selected reference values independently and state the numerical tolerance. Plotting code may transform units or summarize results, with the transformation visible.

## Notebook and book output

```python
from IPython.display import SVG, display
display(SVG(filename="build/figures/sequence.svg"))
```

Stage the same generated SVG for MyST. Give it a caption explaining scope and a text alternative describing its main information. Keep build commands and dependency details in setup/reproducibility references; the chapter explains the engineering question and interpretation.
