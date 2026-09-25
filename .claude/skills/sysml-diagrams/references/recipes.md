# Rendering recipes

Run from the tutorial repository root. `$SYSML` is the pinned OpenSysML CLI, `$PILOT_JAR` and `$PILOT_LIBRARY` identify the matched pilot bundle, and `$PLANTUML_JAR` identifies the pinned standalone renderer. `model.sysml` is the chapter-generated snapshot. Replace example qualified names with the chosen subject. Write outputs to an ignored `build/figures/` directory.

## Definition and decomposition — official pilot

Load all required source files and the matched standard library into one pilot session. Validate, then render the qualified subject with `TREE`. In the pilot Java API, use `process(source, true)` to index a loaded source, followed by `viz(names, views, styles, help)`. The equivalent notebook operation in a pilot kernel is `%viz --view TREE Qualified::Subject`.

The small Java harness shipped with this skill accepts:

```sh
java -Djava.awt.headless=true -cp "$PILOT_JAR" \
  "$DIAGRAM_SKILL/scripts/PilotFigure.java" "$PILOT_LIBRARY" \
  build/figures/decomposition.svg TREE TB \
  ToasterStudy::ElectricToaster -- model.sysml
```

Use a top-to-bottom arrangement for decomposition; show one structural level per teaching question. Read the diagram as a view of model containment and composition, keeping usages distinct from their definitions. Exposing an abstract definition alone should not imply an instantiated system.

Expected check: the selected system and intended children appear with the correct ownership. Include multiplicities and inherited members when they matter; select the pilot’s `SHOWINHERITED`, `NODEMULTIPLICITY`, or `EDGEMULTIPLICITY` styles as appropriate, then inspect the result. The default fixture establishes basic structure rendering, not every style combination.

## Interconnection — SysMLD, with model-derived intent

Use SysMLD as the layout and SVG engine. The notebook supplies the semantic projection, just as a plotting cell supplies arrays to Matplotlib. The starting inputs are the validated model, a selected system or subsystem, and small presentation settings.

Extract these facts using OpenSysML’s model API or an available semantic query engine:

| Projected fact | Source and mapping |
|---|---|
| Subject | Selected part definition or usage, with model identity. |
| Part nodes | Selected owned part usages; labels derive from usage name and type. |
| Ports | Port usages in each part’s context, including required inherited features; keep identity and type. |
| Connection edges | Resolved connection identity and endpoint feature paths. Preserve connector kind and any flow direction separately from drawing orientation. |
| Boundary connections | The selected subject’s external ports and their internal endpoints. |

Construct the compact intent schema consumed by `sysmld interconnection`: `subject`, `model_files`, `aliases`, `nodes`, `edges`, optional `boundary_inputs`, and presentation settings. Node and edge identifiers map back to the projected facts. For an ordinary binary connection, derive `from` and `to` from its endpoint owners and `source_label` / `target_label` from the corresponding port names. `from`/`to` is a layout convention for an undirected connection; it does not assert a physical flow direction. Use `label_mode: "both"` when both connection names and port labels are needed.

Keep the projection in memory until writing generated `interconnection.json`. The rendering sequence is:

```sh
sysmld interconnection build/figures/interconnection.json
sysmld render build/figures/interconnection.sysmld
sysmld validate build/figures/interconnection.sysmld --strict
```

Start with direction, node widths, rank spacing, and label detail. Add explicit rank/order or port-face settings only when the figure needs them. Preserve the generated intent and layout as inspectable artifacts.

Before rendering, assert that selected relationships and endpoints match the projected nodes and ports. After composing, check that the layout preserves those identities and connections. The tested composer generates port IDs from part pairs: repeated connections between the same pair, shared ports, and unconnected ports require particular care. For those cases, use explicit `.sysmld` elements and connections generated from the same facts, with stable per-port/per-connection IDs, rather than assuming the compact composer preserves them. Inspect the relevant schema before doing so.

This recipe specifies the projection contract; it does not supply a general SysML-to-SysMLD adapter. Implement the small query/projection required by the chapter and test its actual supported constructs. Keep full semantic validation in the model engine, and inspect any disagreement with SysMLD’s textual reference index.

## Action flow — OpenSysML and PlantUML

```sh
"$SYSML" model.sysml \
  -render '#action:ToasterStudy::Toast' \
  -render-form plantuml -o build/figures/actions.puml
java -Djava.awt.headless=true -jar "$PLANTUML_JAR" \
  -tsvg build/figures/actions.puml
```

Expected output: the declared actions, initial/final nodes, and successions. Check decisions, guards, forks, joins, and object flows whenever the selected model contains them. The basic toaster trial exercises a linear sequence.

Use the same model view to control scope; use PlantUML presentation directives for font, orientation, and spacing. Apply those directives programmatically to generated output or through a renderer configuration. Preserve action names and edge meaning. Distinguish a structural action-flow figure from an actual execution trace.

## State transition — official pilot

```sh
java -Djava.awt.headless=true -cp "$PILOT_JAR" \
  "$DIAGRAM_SKILL/scripts/PilotFigure.java" "$PILOT_LIBRARY" \
  build/figures/states.svg STATE TB \
  ToasterStudy::ToastCycle -- model.sysml
```

Show states and transitions for one behavioral question. Preserve initial entry and, when present, event triggers, guards, effects, and entry/do/exit compartments. Change orientation or split nested behavior into another figure when labels become crowded.

Check each transition’s source and target. For the study fixture, `idle → heating` branches to `ready` or `cancelled`. A changed target must change the corresponding arrow. Generated pilot hyperlinks contain session-specific identifiers; appearance or normalized semantic comparisons are more useful than raw byte identity.

## Sequence — OpenSysML and Mermaid

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
