# Probe log: what was actually run, and what it showed

Rule (AGENTS.md 1.9): a construct is described as working only after it has been run. This file is the durable record; skills and gap records cite it and are updated from it. Add a dated section for each new probe round. Scripts live in `scripts/probes/`.

## 2026-09-26 (Pass 1 re-probes)

Environment: OpenSysML v0.9.0 (`uv run`), sysml-toolkit v0.9.1 built from `~/Documents/GitHub/sysml-toolkit` (Rust 1.97.1; `cargo build --release -p sysmlv2-cli`; Python binding via `maturin develop --release` in a scratch venv, not the repo environment). Reproduce the OpenSysML rows with `uv run python scripts/probes/reprobe_opensysml.py`.

### OpenSysML v0.9.0

| Gap | Construct | Result | Consequence |
|---|---|---|---|
| G3 | `allocation def X { end part logical : A; end part physical : B; allocate logical.component to physical.assembly; }` then `allocation a : X allocate system to device;` (spec 7.15.2) | **Works.** Also `allocate l to p;` and `allocation named_alloc allocate l to p;` | G3 is resolved: the earlier failure was our syntax, not a tool gap. Nothing to file. |
| G4 | `connect outlet.o to torch.fuelIn` with `PowerPort` to `FuelPort`; an `interface def` with `PowerPort` ends bound to a `FuelPort` | **No diagnostic** (`ok=True`) | Still open, but reframed (see the conformance note below): the spec text searched does not require the tool to reject it, so it is a **staged project conformance check** the tutorial supplies (recipe 5 in `.claude/skills/opensysml-query`), and at most a feature request upstream. |
| G2 | bare `perform ToastBread;` | Rejected: "references target must be a usage, found actionDef" | Correct per spec, not a gap. Use `perform action heat : ToastBread;` or `perform heatUse;` (a usage). |
| G1 | What `model.query()` sees | Named `allocation`, `connection`, `flow` are visible (`AllocationUsage`, `ConnectionUsage`, `FlowUsage`). `satisfy` cannot be named (`satisfy r1 by h;`) and is JSON-only. `MetadataUsage` is JSON-only. Named `perform action heat` appears as type `ActionUsage`, not `PerformActionUsage`. Inherited features are not expanded: a specializing part def or a usage of it shows only its own members. | Convention: name allocations, connections and flows. Chase inheritance through `Symbol.specializations`. Use the JSON helpers for satisfy and metadata. |
| MoE/MoP | `import ParametersOfInterestMetadata::*;` then `metadata MeasureOfEffectiveness about T::quality;` | Parses (`ok=True`); visible in JSON only | Usable for tagging. `Real` needs `import ScalarValues::*;`. |
| G7 | `import` across separately loaded sources | (2026-09-26, earlier probe) unresolved; concatenating sources works | Assembly by concatenation remains the OpenSysML pattern. |

### Conformance note (G4, Z's ruling 2026-09-26)

- **Two tiers** (AGENTS.md 1.9, Z-27): language conformance is always on and breaks the load; project conformance checks are staged, applied from a declared chapter and section, carry a negative control, and are reported open until applied.
- **Spec check (KerML 1.1 Beta 2, searched by constraint names):** `validateConnectorRelatedFeatures` requires only at least two related features of a concrete connector; the `validateSubsetting*` constraints cover constant, uniqueness and featuring-type conformance; `validateRedefinitionEndConformance` covers `isEnd`. No constraint found requiring the types of connected ends to be compatible. The SysML language text was searched for the same and returned nothing. This is a search result, not a proof of absence; before filing anything, read the connector semantics sections again.
- **Toolkit:** `sysmlv2 check` and `sysmlv2 lint` (default rules) both accept the mismatched connection with no finding (2026-09-26).

### sysml-toolkit v0.9.1

- **Cross-file resolution works.** `sysmlv2 check base.sysml chapter.sysml` resolves `import Base::*`; only the library (`ScalarValues`) is unresolved without `--lib`. `Session.from_files([...])` reads several files. So G7 is specific to OpenSysML.
- **Unnamed elements are visible.** `Session.elements_of_metaclass` returns unnamed `FlowUsage`, `AllocationUsage` and `SatisfyRequirementUsage` (ch08: 1, 1, 4); `derived(e, "satisfyingFeature")` resolves. `connectorEnd` came back as `None` ("passthrough", needs the closure policy or a library); not explored further.
- **`viz` (CLI and `Session.to_plantuml`)** supports tree, interconnection, state, action, sequence, case and mixed, with `--color`, `--hide-metadata`, `--show-inherited`, `--show-imported`, `--link-template`, `--horizontal`. Works on `models/ch08-cumulative.sysml`. `plantuml` is at `/opt/homebrew/bin/plantuml`.
- **Correction: summary mode is not available in the CLI or Python.** The v0.9.1 changelog's summary mode (collapsed containers with hidden counts, member and note limits) is `VizOptions::summary` in the Rust `sysmlv2-viz` crate and the WebAssembly controls only. `sysmlv2 viz` and `Session.to_plantuml` have no such option. Do not plan notebook diagrams around collapsing implicit parts with the toolkit until that changes; use the `element` root, view choice and filtering instead.

### How other facts were verified (so they can be repeated)

- **Douglas quotes** (glossary edges `def-douglas--*`): re-read from fresh YouTube transcripts in Z's Chrome (Part 3 `UTm1ORuZ1dg`, Part 4 `Iblo2Il-pOA`). The built-in browser cannot load the transcript (empty response); in Chrome, click "Show transcript", wait 10 to 20 seconds for `ytd-transcript-segment-renderer` elements to appear, normalize and search. Locators corrected: requirement 1:43, traceability 9:43.
- **PDF quotes**: `uv run python -m glossary verify-sources` finds every quote on its recorded page (needs the gitignored PDFs in `glossary/sources/local/`).

## 2026-09-27 (DL-046 probe: does OpenSysML v0.9.0 answer a "holds" question?)

**Question:** Z gated DL-046 (whether Chapter 8 must deliver formal model checking) on whether `check` (or `smt`/`explore`/`solve`) can actually answer a bounded/formal verification question, as opposed to evaluating a fixed value.

**Method:** `conn.list_engines()` reports each engine's declared question kinds directly:
```
check: bounded, answers outcomes, holds, sensitive; ready
explore: proved, answers outcomes; ready
run: observed, answers evaluate; ready
smt: proved, answers holds, sensitive; ready
solve: proved, answers satisfiable; ready
sweep: observed, answers sweep; ready
```
So `check`/`smt` do declare "holds" as a question kind they answer. The question is whether any Python method actually *poses* a holds/outcomes/sensitive/satisfiable question, as opposed to an evaluate question.

**Result: no.** Every public method that takes an `engine=` argument (`verify_constraint`, `verify_requirement`, `validate_instance`) is documented and behaves as posing an "evaluate" question ("the verdict is about concrete values"; "each asserted constraint ... is evaluated against the object"). Tried on both a fully-determined subject and a deliberately underdetermined one (a part usage with no bound value), with and without an explicit `subject=`, naming the requirement usage and the constraint directly: every non-`run` engine replies `"<engine> does not answer evaluate questions — not covered"`; `run` (or no engine) replies with an evaluation failure ("no value for feature x.w — not covered by run") on the underdetermined case. No method in `opensysml.model.Model` (checked the full method list) takes a question-kind argument or otherwise exposes a holds/outcomes/sensitive/satisfiable request. `explore_state`/`explore_action` explore state machines and actions (schedule=explore), which is a different, already-used capability (Ch7), not a constraint-holds question.

**Conclusion:** the capability check/smt declare (bounded or proved verdicts on a "holds" question) exists at the engine-registration/protocol level but is not reachable through the OpenSysML v0.9.0 Python binding's public API. This is a real tool gap, not a usage error on the probe's part — four call shapes were tried, all producing the same "not covered" boundary.

**Consequence for DL-046:** Z's negative-probe fallback triggers. DL-006 stands: Chapter 8 does not deliver formal model checking against this tool version. The gap is drafted as a feature request (Draft 8, `decisions/gap-issue-drafts.md`) and registered (D-024). Chapter 8's prose defects ("formally satisfy", "proves", "bounded checks") are fixed regardless, per DL-046's determined part.
