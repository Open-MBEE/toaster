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
| What is the system made of? Definition and decomposition view | `model_to_dot()` (in-house, `src/toaster/render.py`) → Graphviz SVG | Draws the whole model's containment graph from a full `model.query()`, not one root's direct children — a real-fixture rerun of the diagram trade study (`decisions/diagram-study-real-fixtures.md`) found the OMG SysML v2 Pilot Implementation fails on all real chapter content (qualified-name `allocate` targets), and rendering a single root via the OpenSysML runtime's `#tree:` form only shows that root's own direct features, one level deep. |
| How do parts connect through ports? Interconnection view | Model query → `render_interconnection()` (in-house, `src/toaster/render.py`; the same real-fixture study found the actual third-party SysMLD tool cannot index real content at all) → Graphviz SVG | Draws part connectivity, port identity (as edge labels), and allocations, with zero dependency on a tool proven unreliable on real content. **Use sysml-toolkit instead specifically when port identity itself is the chapter's own pedagogical point** (e.g. a chapter introducing or exercising a conjugated port) — it draws real port names as their own boxes, not folded into one edge label, confirmed on every real fixture tested (`decisions/diagram-study-real-fixtures.md`). Otherwise default to the in-house renderer: a chapter using interconnection only to show an allocation or a connection, where port identity is not itself the point, does not need the extra external-binary dependency (`decisions/diagram-survey.md`, Ch5-vs-Ch6 example). |
| What happens next? Action-flow view | OpenSysML runtime CLI, `-render #action:element -render-form dot` → Graphviz SVG | Confirmed directly against real chapter content (Ch6's `ApplyHeat` action): exit 0, real action-flow notation. No in-house action-flow renderer exists yet. |
| How does behavior change with events? State-transition view | OpenSysML runtime CLI, `-render #state:element -render-form dot` → Graphviz SVG | The real-fixture study confirmed this directly against Ch7's real `Cycle` state machine — 100% success across both OpenSysML runtime render forms. The pilot (this table's earlier default) fails on all real chapter content; do not use it. |
| Who sends what, in what order? Sequence view | OpenSysML runtime sequence query → DOT → Graphviz SVG | White background, relationship-consistent rendering, no Mermaid dependency. Provisional: no chapter's real model has a `FlowUsage` yet, so this pipeline has not been exercised against real content. Fallback: PlantUML if `opensysml -render-form dot` unsupported for sequences (confirmed at WP-1 and documented below). |
| Which requirement or function relates to which element? Traceability graph | Model query → Graphviz DOT → SVG | Explicit typed relationships and controllable grouping. Use a table when the purpose is exhaustive coverage. |
| How does a modeled quantity change? Scientific plot | Model execution results → Matplotlib → SVG | Axes, units, reference values, and parameter comparisons. |

These are working defaults for this tutorial, not universal tool rankings, and are grounded in `decisions/diagram-study-real-fixtures.md` (a rerun of the original trade study against real chapter models, not the simplified toy fixture the original comparison used). Keep the same pipeline for a given figure type throughout the book. An unsupported construct warrants an explicit recipe change; a crowded figure usually warrants a smaller scope or better layout. **Never use the pilot or the third-party SysMLD/sysml2d tool for real chapter content** — both are confirmed, on real content, to fail entirely (pilot: qualified-name `allocate` targets; SysMLD: an indexer bug that mis-tracks brace scope on ordinary real syntax like a doc-comment block or an `assert constraint` body).

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

DOT and the `render_interconnection()` intent dict are generated build products. Preserve them when useful for inspection; regenerate them after model changes. Do not separately maintain their engineering relationships. Store presentation configuration as the authored asset. For a simple direct export, a command and its arguments are sufficient configuration.

The interconnection view needs an explicit projection: generate its nodes, ports, and edges from the model via `build_interconnection_intent()`. Checking that displayed endpoints actually correspond to the selected model relationships is a projection check, done the same way as any other view's — not a reference-name check from a third-party tool (the tutorial does not use SysMLD). See the interconnection recipe for the required mapping.

## Tailor like a scientific figure

Start with one question and a small scope. Try orientation, label wrapping, and spacing before adding individual positions. Split an overloaded diagram into coordinated views when that explains the system better. Additional layout code is justified by readability, not by making every figure use identical geometry.

Use white backgrounds, readable typography, restrained color, and consistent names. Distinguish definition, usage, containment, connection, control flow, and dependency visually. **Never use Mermaid** — DOT/Graphviz is the default for structure, sequence, and relationship diagrams; `render_interconnection()` (in-house, DOT-based) is first-class for interconnection. Prefer SVG for publication and notebook display.

## Diagram pipeline decisions (updated after the real-fixture diagram study, 2026-09-29)

- **DOT/Graphviz** — default for structure, interconnection, sequence, and relationship diagrams
- **`render_interconnection()`** (in-house, `src/toaster/render.py`) — first-class for port-level interconnection; the intent dict is built from `model.query()` + `model.to_api_json()`. This function does not use, and never used, the third-party SysMLD tool — see the real-fixture study for why that tool is now confirmed unusable on real content.
- **OpenSysML runtime CLI (`-render-form dot`)** — action flow and state views, confirmed directly against real chapter content
- **Matplotlib** — quantitative figures only
- **Mermaid** — NOT used anywhere in this tutorial
- **The OMG SysML v2 Pilot Implementation** — NOT used anywhere in this tutorial; confirmed to fail on all real chapter content (qualified-name `allocate` targets)
- **The third-party SysMLD/sysml2d tool** — NOT used anywhere in this tutorial; confirmed to fail to index any real chapter content (an indexer bug, see `decisions/log.md` DL-055)

**A note on an earlier finding, corrected by the real-fixture study (`decisions/diagram-study-real-fixtures.md`):** an earlier probe (WP-1, 2026-09-25, against a small hand-written test model, not a real chapter model) found the OpenSysML runtime had no native DOT or render-form CLI, and that finding drove a stopgap of generating DOT directly from `model.query()` output for the structure view. That stopgap (`model_to_dot()`) is still the right choice for structure specifically (it draws the whole model, not one root), but the earlier finding about the OpenSysML runtime's CLI no longer holds: the pinned binary's `-render #kind:element -render-form dot` (or `plantuml`) form is real, works on real chapter content (confirmed for both action-flow and state views), and is simply undocumented in the binary's own `-help` output.

For action flow and state: the OpenSysML runtime's own `-render` CLI, not a custom Python renderer — none exists yet for action flow, and none is needed.
For interconnection: `render_interconnection()`'s intent dict, built from `model.query()` + `model.to_api_json()` (unchanged from WP-4; only the function's name changed, since it never depended on the tool its old name implied).
Never use Mermaid as a fallback for anything.

## Check meaning and appearance

1. Run the chapter’s model-validation gate and inspect renderer diagnostics.
2. Check the selected node identities and relationship endpoints against the model. For sequences, check lifelines and message ordering. For plots, check units and numerical values.
3. Inspect the SVG at its intended book width. Resolve clipped labels, overlaps, ambiguous arrows, and lines through unrelated nodes or labels.
4. When introducing or changing a projection, change one source relationship and verify that the expected displayed relationship changes. Keep this as a focused regression check for reused helpers.
5. Caption the selection and interpretation. A diagram of a satisfaction relationship shows a modeled assertion; a verified verdict or human judgment must come from its own evidence.

Publish the exact SVG generated by the checked notebook. Record model/input hashes, selected subject, renderer version, and plotting configuration in the build manifest. Compare semantic content and numerical results; require identical SVG bytes only where the pipeline supports that guarantee.

Read [Environment and evidence](references/environment.md) when provisioning these recipes or reviewing what has been exercised.
