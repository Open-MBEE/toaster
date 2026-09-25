---
name: sysml-diagrams
description: Generate publication-ready diagrams from SysML v2 models for the toaster tutorial, choosing a renderer by diagram type and keeping model content separate from presentation configuration.
---

# Diagram SysML models

Treat the SysML model as the dataset and the figure as a selected, purpose-specific view. Generate figures from the chapter’s `.sysml` snapshot or loaded model. Apply layout and styling as visualization code, with the same care used for a scientific plot.

## Choose the renderer by the question

Use one default pipeline for each figure type. Read only the relevant recipe in [Rendering recipes](references/recipes.md).

| Question / figure type | Default pipeline | Why |
|---|---|---|
| What is the system made of? Definition and decomposition view | Official SysML pilot `TREE` → SVG | Familiar definition/usage shapes, compartments, and composition notation. |
| How do parts connect through ports? Interconnection view | Model query → generated SysMLD intent → SysMLD SVG | Explicit port placement and orthogonal routing support readable interface views. The generated intent is a plotting input. |
| What happens next? Action-flow view | OpenSysML → PlantUML → SVG | Uses the existing model tool and produces familiar action nodes and control flow. |
| How does behavior change with events? State-transition view | Official SysML pilot `STATE` → SVG | Familiar state notation, transitions, and behavioral compartments. |
| Who sends what, in what order? Sequence view | OpenSysML sequence query → DOT → Graphviz SVG | White background, relationship-consistent rendering, no Mermaid dependency. Fallback: PlantUML if `opensysml -render-form dot` unsupported for sequences (confirmed at WP-1 and documented below). |
| Which requirement or function relates to which element? Traceability graph | Model query → Graphviz DOT → SVG | Explicit typed relationships and controllable grouping. Use a table when the purpose is exhaustive coverage. |
| How does a modeled quantity change? Scientific plot | Model execution results → Matplotlib → SVG | Axes, units, reference values, and parameter comparisons. |

These are working defaults for this tutorial, not universal tool rankings. Keep the same pipeline for a given figure type throughout the book. An unsupported construct warrants an explicit recipe change; a crowded figure usually warrants a smaller scope or better layout.

## Make a figure recipe

Record a short recipe alongside the notebook cell:

- **Question and subject:** the engineering question, qualified model name, and model snapshot.
- **Selection:** elements, relationship kinds, depth, and intentional exclusions.
- **Encoding:** what boxes, lines, arrows, colors, and labels mean.
- **Presentation:** orientation, grouping, spacing, label detail, and intended display width.
- **Checks:** the elements and relationships the figure must communicate.

Keep model content and presentation settings distinct. A small configuration object may specify order, coordinates, orientation, short display labels, or an exposed subset. Obtain identities, types, multiplicities, containment, connections, event order, and numerical values from model queries or execution results. Provide a key when shortening labels obscures identities or types.

## Keep intermediate representations small

Prefer the renderer’s direct `.sysml` input. Where projection is useful, generate only the data needed for the view, retaining model IDs or qualified names. Compute simple projections in the notebook; introduce a shared helper when the same operation is repeated.

PlantUML, Mermaid, DOT, and SysMLD intent/layout files are generated build products. Preserve them when useful for inspection; regenerate them after model changes. Do not separately maintain their engineering relationships. Store presentation configuration as the authored asset. For a simple direct export, a command and its arguments are sufficient configuration.

SysMLD needs an explicit projection: generate its nodes, ports, and edges from the model. Its reference-name check supplements the projection checks; the latter establish that displayed endpoints actually correspond to the selected model relationships. See the interconnection recipe for the required mapping.

## Tailor like a scientific figure

Start with one question and a small scope. Try orientation, label wrapping, and spacing before adding individual positions. Split an overloaded diagram into coordinated views when that explains the system better. Additional layout code is justified by readability, not by making every figure use identical geometry.

Use white backgrounds, readable typography, restrained color, and consistent names. Distinguish definition, usage, containment, connection, control flow, and dependency visually. **Never use Mermaid** — DOT is the default for sequence and relationship diagrams; SysMLD is first-class for interconnection. Prefer SVG for publication and notebook display.

## Diagram pipeline decisions (updated SA-9)

- **DOT/Graphviz** — default for sequence and relationship diagrams
- **SysMLD** — first-class for port-level interconnection; model-to-intent exporter built in WP-4 by A2
- **PlantUML** — action flow only (via `opensysml -render-form plantuml`)
- **Matplotlib** — quantitative figures only
- **Mermaid** — NOT used anywhere in this tutorial

**WP-1 probe result (2026-09-25): opensysml v0.9.0 has no native DOT or render-form CLI.** `sysml-grpc` is a gRPC server with no render flags; the Python API has `model.render_document()` for document queries only. There is no `-render-form dot` or equivalent.

**Confirmed approach:** DOT is generated directly from `model.query()` output in Python (via `src/toaster/render.py::model_to_dot()`). The function queries all elements, emits PartDefinition nodes and PartUsage composition/typing edges, then passes the DOT string to `render_dot()` → Graphviz `dot -Tsvg`.

For action flow: PlantUML remains the target (WP-4 implementation).
For interconnection: SysMLD intent dict built from `model.query()` + `model.to_api_json()` (WP-4).
Never use Mermaid as a fallback for anything.

## Check meaning and appearance

1. Run the chapter’s model-validation gate and inspect renderer diagnostics.
2. Check the selected node identities and relationship endpoints against the model. For sequences, check lifelines and message ordering. For plots, check units and numerical values.
3. Inspect the SVG at its intended book width. Resolve clipped labels, overlaps, ambiguous arrows, and lines through unrelated nodes or labels.
4. When introducing or changing a projection, change one source relationship and verify that the expected displayed relationship changes. Keep this as a focused regression check for reused helpers.
5. Caption the selection and interpretation. A diagram of a satisfaction relationship shows a modeled assertion; a verified verdict or human judgment must come from its own evidence.

Publish the exact SVG generated by the checked notebook. Record model/input hashes, selected subject, renderer version, and plotting configuration in the build manifest. Compare semantic content and numerical results; require identical SVG bytes only where the pipeline supports that guarantee.

Read [Environment and evidence](references/environment.md) when provisioning these recipes or reviewing what has been exercised.
