# Diagram survey: re-running the tool trade study against real fixtures, then inventorying where diagrams belong

## Context

AGENTS.md §1.7 requires a figure per chapter. Every chapter re-derived or authored in Pass 4 deferred it, on the reasoning that a diagram of a model still being actively re-derived would need re-rendering every time an upstream fix changed what it showed. All 10 chapters are now stable (merged, reviewed, and independently confirmed by a 29-run simulated-learner battery with zero blocking findings), so that reason no longer holds.

Z had already commissioned and completed a trade study (`/Users/z/Downloads/toaster/diagram-study/`, dated 2026-09-25) comparing five SysML v2 rendering tools against a single common toaster-shaped fixture. The study's own conclusion: no tool wins on every view type, and its fixture was deliberately simpler than any real chapter of this tutorial (four parts, four ports, two connections, one action sequence, one small state machine — no recursion, no conjugated ports, no allocations, no formal verification). The study's own "next comparison corpus" section names exactly the features it didn't test.

Z's intent, from this session's conversation: not one diagram per chapter, but a systematic pass identifying every place across all 10 chapters where a diagram would communicate better than the current text/print output, potentially replacing that output rather than merely supplementing it — motivated by systems engineering's own visual, diagram-GUI-centric practice. Given the scale (10 chapters, ~30 notebooks) and the real risk that the study's tool-capability conclusions don't hold once the fixture stops being simplified, this is split into two phases. **This spec covers both; only phase 1's own findings determine what, if anything, becomes phase 2 (implementation).**

## Decisions already made (confirmed with Z via chat, not open questions)

1. **Multi-tool, per-view-type**, not one tool for everything. OpenSysML + Graphviz/DOT (`src/toaster/render.py::model_to_dot`, already "in force by decision," DL-001/DL-002, zero new dependencies) is the baseline for structure/containment and action/state views, where the original study found it rendered cleanly. **sysml-toolkit** is brought in specifically for port/interconnection views, the one view type the study found OpenSysML+Graphviz drops real information on (inherited ports collapse to part-level lines) and sysml-toolkit renders correctly (real inherited ports, named connections — though with its own layout/overlap issues still to solve). The OMG pilot (Java + a second parser, port-label overlap) and SysMLD (needs a second, separately-maintained model, and the study's own mutation-control test found it can silently go stale — a model change left a SysMLD-rendered diagram byte-for-byte unchanged) are **not adopted**, but not permanently ruled out either; noted as rejected-for-now with the reasons preserved.
2. **View types per chapter track what that chapter's own content actually has**, not a fixed template applied uniformly. Structure/containment applies everywhere (there's always an assembled model to show). Interconnection from Ch5 onward (first real port-typed connection). Action-flow from Ch4 onward (first real action decomposition). State from Ch7 onward (`Cycle` first exists there). A chapter's own diagram set grows to match its real content across the sequence.
3. **The Foundations' "explicit vs. implicit construction, made legible via diagrams" provenance problem is moot for this work.** As actually built, every chapter's model lives in one cumulative `.sysml` file; there is no separate implicit-parts module and no explicit/implicit split in the real model to encode. This is a real gap between what AGENTS.md Part 1 describes and what got built, but it's out of scope here — noted for a future pass, not solved by this one.
4. **Generation mechanism: live notebook cells**, matching Chapter 5's own existing interconnection-figure pattern — not a standalone build script that embeds pre-rendered static images into `index.md`. This means any diagram that gets added will require reopening and re-reviewing already-merged notebook content through the same builder/reviewer pipeline every other piece of this tutorial's content has gone through. This spec's own phase 1 (below) does not do that reopening; it only identifies where it should eventually happen.
5. **Scope is not "one diagram per chapter."** Multiple diagrams per chapter are expected, and a diagram may **replace** a text-heavy output, not just sit alongside it. This is the actual point of phase 1: find those places for real, not assume a fixed count.
6. **Phase 0 (re-running the trade study against real fixtures) matches the original study's own rigor** — pinned tool versions, hash-based repeatability checks, and specifically the mutation-control test (the one that caught SysMLD's silent staleness) — not a lighter spot-check. A full-complexity fixture is more likely to expose a correspondence bug like that, not less, so the check that caught it once is exactly the one to keep.

## Phase 0: re-run the trade study against real fixtures

**Why this is needed, not optional.** The original study is explicit that its own fixture is simpler than a real chapter and names the untested features directly: "recursive heating structure, typed/directed and conjugated ports, multiplicities, item flows, allocations, requirement satisfaction/verification, guarded transitions with effects, and action decisions/forks/joins." Building a 10-chapter, 30-notebook diagram inventory on tool-capability conclusions drawn from a fixture that small would be planning on an unrun construct — exactly what this project's own established discipline (P5, "probe before you assert") exists to prevent.

**Fixtures.** Real chapter cumulative models, chosen to cover the study's own named gaps against what the tutorial actually contains:

| Study's untested feature | Real chapter that has it | Notes |
|---|---|---|
| Recursive heating structure | Ch6 (`models/ch06-cumulative.sysml`) | `HeatGenerator` → `ResistanceCoil`, the level-2 decomposition |
| Conjugated ports | Ch5 (`models/ch05-cumulative.sysml`) | `~DurationPort` |
| Allocations | Ch5/Ch6 | `heatAllocation`, `heatGenAllocation`, both named/usage-level |
| Requirement satisfaction/verification | Ch3, Ch6, Ch8 | `assert satisfy`/`assert not satisfy`; Ch8 additionally has a real Z3-proved formal property (`deliveredEnergyBoundedBySupply`), which no version of the original study or its fixture touched at all |
| State machine with transitions | Ch7 (`models/ch07-cumulative.sysml`) | `Cycle`, exhibited by `ToastingSystem` |
| Item flows | **none** | Confirmed during Ch9's own build: the real, current model has zero `FlowUsage` elements anywhere. Not testable against this tutorial's real content; not a gap to manufacture a fixture for. |
| Guarded transitions, forks/joins | **none** | Not present anywhere in the real model either. Same treatment. |

Representative set: **Ch5, Ch6, Ch7, Ch8** cover every feature the real tutorial actually has that the original study didn't test. Ch9 and Ch10 add no new model element (confirmed in their own run logs), so they're not needed as additional fixtures for this phase, though phase 1's survey still covers them for the "where should a diagram replace text" question.

**Method.** Reuse the original study's own harness where possible (`run_study.py`, `check_sysmld_mutation.py`) against all four tools the original study covered, not just the two adopted ones: OpenSysML+Graphviz/DOT and sysml-toolkit (the two being carried forward), plus the OMG pilot and SysMLD (both "not adopted" but rerun anyway, for comparison completeness — "not adopted" isn't the same as "not worth reconfirming," and the harness already exists, so the marginal cost of running all four instead of two is small against the value of grounding the adoption decision on real structure instead of leaving it resting on the toy-fixture result). Record, per tool per fixture: exit status, timing, output hash, a raster comparison, and a real-model mutation-control test (change one real element the way Ch7's own D-023 typo probe already does, re-render, diff — this is the exact check that caught SysMLD's staleness the first time, so it runs again here, not just once).

**Deliverable.** An updated capability matrix (same shape as the original study's "Alternatives exercised" table), scoped to the four real fixtures, written to `decisions/diagram-study-real-fixtures.md` alongside a `decisions/diagram-study-real-fixtures/` evidence folder (renders, hashes, logs) mirroring the original study's own `evidence/` structure.

## Phase 1: the per-chapter diagram survey

**Method.** One read-only research agent per chapter (10 in parallel — the full 30-notebook breadth is too much for a single pass to read without losing context budget), each given: that chapter's real notebooks, that chapter's real cumulative model, and phase 0's real-fixture capability matrix (not the original study's simplified one). Each agent returns a structured finding, not prose: a table of (notebook, cell/output under consideration, proposed diagram type, proposed tool, add-or-replace, rationale).

**Compiled output.** One document, `decisions/diagram-survey.md`: a short prose paragraph per chapter on its overall diagram strategy, followed by that chapter's compiled table. This is a design document — no notebooks are touched, no diagrams are actually built, in this phase.

## Non-goals (explicit, so a future reader doesn't assume more happened)

- No notebook is reopened or edited in either phase.
- No diagram is actually rendered and committed to any chapter in either phase (phase 0's renders are throwaway trade-study evidence, same as the original study's; phase 1 produces recommendations only).
- The explicit/implicit construction provenance problem (decision 3 above) is not solved.
- Implementation (actually building the recommended diagrams, chapter by chapter, through the builder/reviewer pipeline) is **not specced here** and does not start until phase 1's findings exist and Z has reviewed them — this is the same "survey first, plan implementation once you can see what it found" decomposition Z already confirmed.
- The exercise track's own full re-derivation (a separate decision Z made the same session) is unrelated to this spec and is not sequenced against it here.

## Verification

- Phase 0: each tool's render for each of the four real fixtures actually executes (exit 0), produces a real SVG (not empty/error output), and the mutation-control test is actually run (a real element changed, re-rendered, diffed) for every candidate, not just the ones expected to pass.
- Phase 1: every one of the ~30 real notebooks is confirmed read by its chapter's own agent (not assumed); the compiled `decisions/diagram-survey.md` is checked for internal consistency against phase 0's actual capability matrix (a recommendation citing a tool for a view type that matrix marked as failing would be a defect in the survey itself).
