# Diagram generation strategy: tool selection, scope-query separation, and gap tracking

## Context

Phase 0 (the real-fixture rerun of the original diagram-tool trade study) is complete: `decisions/diagram-study-real-fixtures.md`, logged as `DL-056`, open as [Open-MBEE/toaster#22](https://github.com/Open-MBEE/toaster/pull/22) against `pass1/harness-alignment`, not yet merged. Its headline finding: OpenSysML (both render forms) and sysml-toolkit hold up on real chapter content; the OMG pilot and the third-party SysMLD/sysml2d tool both fail on real content entirely, for two different, independently confirmed reasons (a parser gap and an indexer bug respectively).

This spec is the direct follow-on Z asked for: given that evidence, decide **how diagrams actually get built** across the tutorial, so that Phase 1 (the still-unrun per-chapter diagram survey from the original design spec) has a fixed, provable policy to apply consistently — rather than ten independent per-chapter agents each making their own tool-selection judgment call, which risks exactly the inconsistent, "willy nilly" outcome Z raised directly in this conversation: *"the didactics will be lost if the approach to diagramming feels willy nilly. ideally there is already a consistent strategy at play in which case its just a refinement. if on the other hand it turns out the plan is too ad hoc and would cause confusion as a result, we'd expect redesign around the new strategy."*

Two things drove this spec beyond Phase 0's own numbers:

1. **Z asked to actually render and inspect the drawings**, not just check exit codes and hashes (which is all Phase 0's own harness did). Doing this surfaced a real, previously undocumented problem: the existing `model_to_dot()` structure-diagram renderer produces a clean, legible diagram on a small model (Ch5) and an unreadably wide, cluttered one on a larger model (Ch8) — not because Graphviz's layout is bad, but because the function has no way to scope *what's in the diagram at all*.
2. **Z's own framing of the fix**: separate the model-query layer that decides what's in scope for a plot from the layout/routing that decides how it's arranged — the same separation of concerns matplotlib/networkx already have (a default render is "minimal sufficient" for simple cases; complex cases need customization layered on top, not a from-scratch rebuild).

Z's stated governing philosophy for the whole effort: acknowledging a tool's current limits is fine, as long as the gap is documented, worked around, and used to inform the tool's own developers.

## Decisions already made (confirmed in chat, this session)

1. **Tool-selection policy is "prove-then-use"** (Approach C, chosen over "toolkit-first" and "own everything"): use whichever already-proven pipeline handles a view type correctly on real content, preferring in-house code only where a real, load-bearing gap exists in every external option. See the table below.
2. **Content selection must be query-driven, never a hand-typed name list.** A root + relationship kinds + depth, re-evaluated against the live model every time — not a list of element names that can silently drift the way a hand-authored SysMLD intent file already proved it can (DL-055's own finding, one level up the stack).
3. **Layout/routing is a separate, secondary customization axis** — an escape hatch for the cases scoping alone doesn't fix, not the default remedy. What was actually observed: the state and interconnection diagrams were already clean with zero layout customization, because they were already naturally scoped to a small root; the structure diagrams were messy purely from lack of scoping, not bad routing.
4. **Gap documentation gets a new, dedicated register** (`decisions/diagram-tool-gaps.md`), separate from `DEFERRED.md` (which is already scoped, by a prior ACE ruling in `DL-055`, to gaps in constructs/dependencies the tutorial actually adopts — the pilot and SysMLD are explicitly not adopted, so they don't belong there). Upstream issue drafting reuses the existing `decisions/gap-issue-drafts.md` discipline unchanged: draft, hold for Z's review, file only on explicit instruction.
5. **Phase 1's per-chapter survey (already speced, not yet run) proceeds using this fixed tool table**, not free per-chapter tool choice. This is what actually closes the "willy nilly" risk: each of the ten per-chapter agents' job narrows to "which view types does this chapter's content warrant, from the fixed menu, and should a diagram replace or supplement the existing text" — tool selection is no longer a per-chapter decision to get inconsistently.
6. **Already applied** (`DL-057`, commit `6ed75bf`, done before this spec was written): renamed `render_sysmld` → `render_interconnection` throughout the repo (it never depended on the real SysMLD tool — its own docstring already said so) and corrected the `sysml-diagrams` skill's per-view-type table and "Diagram pipeline decisions" section, which had recommended the pilot for tree/state and (ambiguously) "SysMLD" for interconnection — both now proven wrong on real content by Phase 0.

## The tool-selection table

| View type | Renderer | Why |
|---|---|---|
| Structure/containment | `model_to_dot()` (in-house, `src/toaster/render.py`), **scoped** per this spec's query layer below | Draws the model's containment graph from a query, not one root's direct children (avoiding OpenSysML's `#tree:` one-level-deep limit) — but must be scoped to avoid the clutter this spec's own investigation found. |
| Action-flow | OpenSysML CLI, `-render #action:element -render-form dot` | Confirmed directly against real content (Ch6's `ApplyHeat`, probed in this conversation): exit 0, correct notation. No in-house renderer exists or is needed. |
| State | OpenSysML CLI, `-render #state:element -render-form dot` | Phase 0 confirmed this directly against Ch7's real `Cycle` state machine, both render forms, 100% success. |
| Interconnection | `render_interconnection()` (in-house, renamed per decision 6) | Draws part connectivity, port identity (as edge labels), and allocations, with zero dependency on either real candidate now proven broken on real content. sysml-toolkit remains the fallback where dedicated port boxes are pedagogically load-bearing enough to justify the external dependency — a per-chapter call for whoever builds that chapter's notebook, not a global default. |
| Sequence / traceability | OpenSysML → DOT (unchanged from the skill's prior guidance) | No chapter's real model has a `FlowUsage` yet, so this remains provisional until a chapter actually needs it. |
| Scientific plot | Matplotlib (unchanged) | Not affected by any of this. |

**Never used for real chapter content:** the OMG pilot (fails all real fixtures on qualified-name `allocate` targets) and the third-party SysMLD/sysml2d tool (fails to index any real content, an indexer bug — `DL-055`).

## Content selection: a query layer, not a name list

**The problem, observed directly.** `model_to_dot()` currently iterates the *entire* result of `model.query()` with no scoping parameter at all. On Ch5's small model this produces a legible "whole system" diagram. On Ch8 — a model that has accumulated test-fixture part usages (`nominal`, `slow`, `rated`, `weak`), a verification-test subject (`heatGenCheck`), and a requirement subject (`HeatGenerationReq::heatGen`) alongside the actual structural decomposition — it produces a sprawling, mostly-disconnected, unreadably wide diagram. This is not a Graphviz layout failure (no crossing edges, no overlaps); it is a content-selection failure. The function has no way to say "just the containment tree," so it draws everything.

**The fix is a query, evaluated fresh against the live model — never a maintained list of names.** A hardcoded include/exclude list would reintroduce, one level up the stack, exactly the integrity risk `DL-055` already found and ruled on: a hand-authored artifact silently drifting out of sync with the model it's supposed to represent, with nothing to notice.

New helper, `src/toaster/render.py`:

```python
def containment_subgraph(model, root: str, *, relations=("composition", "typing"), depth=None) -> list:
    """Elements reachable from `root` by the given relationship kinds, to `depth`
    (None = unbounded). Traverses model.query()'s own owner/type fields — the
    same fields model_to_dot() already reads per element — so this is a query
    against the live model, not a maintained list."""
```

`model_to_dot()` gets one new optional parameter: `elements: list | None = None`. When given a pre-selected list (typically from `containment_subgraph()`), it draws only those elements and their edges; when `None`, it keeps today's behavior (draw everything), which stays a reasonable default for genuinely small models. Scoping becomes necessary once a model has accumulated enough independent test-fixture and requirement-subject elements that "everything" stops being a good default — a judgment call each chapter's own notebook author makes, informed by looking at the unscoped render first (same as this investigation did).

`build_interconnection_intent()` already takes an explicit `fqn` root, so it is already query-scoped; extending it with the same `relations`/`depth` parameters as `containment_subgraph()` is a natural consistency improvement, not a new capability.

**Layout is a second, smaller, separate parameter.** `model_to_dot()`'s presentation options (rank direction, explicit same-rank groupings, per-edge routing hints) stay a distinct optional parameter from content selection — passed through to DOT emission as presentation-only settings, consistent with the `sysml-diagrams` skill's existing rule that presentation settings never carry engineering content. Given what was actually observed (the two diagram types that were already naturally root-scoped needed zero layout customization), this stays the exception path a chapter reaches for only when scoping alone leaves an awkward layout, not something every figure is expected to touch.

## Gap documentation and the upstream-feedback path

**New register, `decisions/diagram-tool-gaps.md`** — a living document distinct from `DEFERRED.md` (which stays scoped, per `DL-055`'s own ruling, to gaps in constructs/dependencies the tutorial actually adopts). One entry per confirmed rendering-tool capability gap or bug, format: tool + pinned version/commit, symptom, root cause if known, evidence paths, whether it blocks adoption, and status (drafted / held for review / filed with issue link). Seeded with Phase 0's two concrete findings, pulled out of `decisions/diagram-study-real-fixtures.md`'s prose into this structured, ongoing form:
- The OMG pilot's qualified-name `allocate`-target parser rejection (all real fixtures).
- SysMLD's indexer brace-scope bug (mis-tracks scope on a doc-comment block or an `assert constraint` body — ordinary real syntax the toy fixture never contained).

**Drafting and filing reuse the existing `decisions/gap-issue-drafts.md` discipline unchanged**: draft text that asks only for what the tool's own documented behavior implies it should do, cite exact evidence, hold for Z's explicit review, file only on instruction. File once a gap's picture is reasonably complete, not after every individual finding — Phase 1's own survey may well surface more instances of these same two root causes without adding new information, and that shouldn't produce issue spam.

**What does not get this treatment:** `model_to_dot()`'s missing selection parameter is this tutorial's own code, not a third-party gap — its fix is the query layer above, not a documented-and-avoided limitation. OpenSysML's undocumented `#kind:element` render shorthand is a quirk worth one line of documentation, not a capability-gap entry — it works correctly (independently confirmed during Phase 0's review to validate its inputs and reject bogus kinds), it simply isn't mentioned in the binary's own `-help` output.

## Non-goals

- **Phase 1's actual per-chapter survey is not run by this spec.** This spec produces the fixed policy Phase 1's agents will apply; the survey itself (which notebook, which cell, add-or-replace, per chapter) remains a separate, already-speced piece of work.
- **No chapter notebook beyond the already-applied `DL-057` corrections is touched here.** Building and inserting new diagrams into Ch1-Ch4, Ch6-Ch10 is implementation work that follows Phase 1's findings, not this spec.
- **No general-purpose "diagram spec" DSL.** Only the two parameters (`elements`, a layout override) needed to fix the concrete problem this investigation found — not a speculative configuration language for cases not yet observed.
- **The sysml-toolkit-vs-`render_interconnection()` choice stays a per-chapter call**, informed by this policy, not decided globally here — some chapters may need sysml-toolkit's dedicated port boxes badly enough to justify the dependency; most, per Ch5's own precedent, may not.
- **No upstream issue is filed by this spec.** Drafts only, per the existing, unchanged discipline.

## Verification

- `containment_subgraph()`: unit tests against real fixtures confirming a root + depth traversal returns exactly the expected element set — including the negative case Phase 0 already found (querying from `ToasterDemo::Toaster` never reaches `heatGen` at any depth, since `Toaster::heating` is typed by the abstract `HeatingSystem`, not the concrete `HeatingAssembly` that owns `heatGen` — confirming the helper reports this correctly rather than silently returning nothing for a different, wrong reason) and the positive case (rooting at `ToasterDemo::HeatingAssembly` directly reaches `heatGen` at depth 1).
- `model_to_dot(..., elements=None)` behavior is unchanged: full existing test suite (`tests/test_diagram_probe.py` and others) passes without modification.
- `model_to_dot(..., elements=containment_subgraph(...))` on Ch8, rooted at `Toaster`: re-render and visually confirm the test-fixture islands (`nominal`, `slow`, `rated`, `weak`, `heatGenCheck`, `TimelyToast`/`TimelyToastTest`) are excluded and the diagram is no longer implausibly wide.
- `render_interconnection()`'s existing 9 tests continue to pass unmodified (name change only, confirmed already in this conversation).
- Full test suite passes throughout.
