---
name: architecture-layers
description: Functional (what) / logical (how) / physical (where) boundary tests with toaster examples, SysML v2 idioms marked tested or untested, a per-layer audit checklist, and a source map. Definitions live in the glossary; this skill applies them.
---

# Architecture layers

Read AGENTS.md Part 1 (sections 1.5 and 1.6) first. This skill does not restate definitions. Look terms up with `uv run python -m glossary tutorial TERM`, and cite the glossary id (`term-mechanism`, `term-mop`, ...) when you rule on a term.

## Use it to classify any element in one pass

Ask in this order and stop at the first "yes":

1. **Would a pop-up toaster and tongs with a blowtorch both satisfy it?** Then it is **functional**: an intent, a typed flow, a relation among phenomena (energy, temperature, time), or a MoE.
2. **Does it commit to a mechanism, an interface, or a policy, but not to a specific part or value?** Then it is **logical**: a mechanism carried by an abstract component, a port or interface, a constraint that exists only because of that mechanism, or a derived MoP threshold.
3. **Does it name a specific part def or give a value that only a chosen part has?** Then it is **physical**: a concrete part, its attribute values, a TPM.
4. **Is it a result the design is expected to produce (a cycle time, an efficiency, a stability margin)?** Then it is *emergent*: it is derived by analysis and compared with intent. It is never entered as a choice.

The **system of interest** (the toaster itself) is the subject all three layers describe, not a layer. Classify its pieces: its purpose statement (functional), its parts and arrangement (logical), its realized parts and values (physical).

## Toaster examples

| Statement | Layer | Why |
|---|---|---|
| "Toasting takes bread and energy in and gives toast and lost energy out; energy to the bread plus loss cannot exceed energy supplied." | Functional | Holds for any solution. The inequality respects conservation without assuming perfect efficiency. |
| "The toast is browned to the user's liking." | Functional (MoE) | Acceptance. Explored against scenarios, not computed. |
| "A resistive coil turns electrical power into heat and must be fed from a mains outlet." | Logical | A mechanism plus an interface. A blowtorch would need a fuel port instead. |
| "Heating efficiency is at least 0.6." | Logical (MoP threshold) | A performance measure with a threshold derived from what the MoE needs; it characterizes a requirement and needs a means of checking. Whether a measure is a MoP or a MoE is a justified modeling judgment (see below). |
| "Joule heating: heat = I^2 R t in the coil." | Logical (mechanism) | A law we rely on to reason about a chosen component, a modeling decision grounded in engineering practice. A universal law (the energy balance) stays functional. |
| "Toast is ready within 150 s." | MoE or MoP, by judgment | Time is usually performance, but for toast it may be part of what the user accepts. Either is defensible if the justification is recorded (who cares; acceptance or engineering performance). |
| "The coil is an 800 W nichrome element." | Physical | A specific part with a value it confers. |
| "Measured heating efficiency is 0.71." or "Measured browning time on the built candidate is 118 s." | Physical (TPM), and an emergent result | A value assessed on a candidate by analysis or simulation: derived, not chosen, and the evidence against a MoP threshold. Classify it as physical when asked for a layer, and as an emergent result when asked whether it was prescribed. |
| "Cycle time = 120 s" set as an attribute default, then checked against a 150 s limit | Not a valid check | A prescription tested against a threshold. Derive cycle time from the mechanism and the energy balance, then compare. |

Toaster stories to lean on (Douglas, Part 3): the system described as functions, as logical components, or as physical parts (1:16); who or which components are responsible (1:56); where those components are implemented (2:05); a function has three parts (3:12); decomposing functions into finer functions (4:02); functions allocated to components grouped logically (4:12); trade studies with performance measures (13:40). The tongs-and-flamethrower comparison also appears in Part 3; its timestamp has not been re-verified here.

## SysML v2 idioms

`example-layers.sysml` in this directory is one small model showing all three layers. `tests/test_skill_snippets.py` loads it, so it stays runnable.

| Layer | Construct | Spec | Status |
|---|---|---|---|
| Functional | `action def` with `in`/`out` `item` and `attribute` flows | 7.17.2 | Tested (`ok`) |
| Functional | `constraint def` for a phenomena relation (energy balance) | 7.20.2 | Tested |
| Logical | `abstract part def` | 7.6.2, 7.11 | Tested |
| Logical | `perform action heat : ToastBread;` inside the abstract part def (the performer is responsible for the action) | 7.17.6 | Tested. A bare `perform ToastBread;` naming an action *def* is rejected; that is correct. `perform usage;` naming an action *usage* is accepted. |
| Logical | `port def`, `interface def`, `connection`, `flow` | 7.12 to 7.14 | Tested to parse. Mismatched port types are **not diagnosed** by the tool (gap G4, `decisions/probes.md`). Treat port-type compatibility as a staged project conformance check (AGENTS.md 1.9) and use recipe 5 in `opensysml-query`, with a negative control. |
| Logical | `requirement def` with `require constraint { ... }` for a derived MoP threshold | 7.21.2 | Tested |
| Any | `metadata MeasureOfPerformance about T::x;` after `import ParametersOfInterestMetadata::*;` | 9.3.4 | Tested to parse. Metadata is not visible to `model.query()` (JSON only). |
| Allocation | `allocate apply to source;` between usages; `allocation def` with typed ends plus `allocation a : Def allocate x to y;` | 7.15.2 | Both tested (`ok`). Name allocations so `model.query()` sees them. |
| Physical | `part def NichromeCoil :> HeatSource { attribute watts : Real = 800.0; }` (concrete specializes abstract) | 7.6.2 | Tested |
| Physical | `verification def` and `verify` | 7.24 | Existing chapters use it. Not re-probed in this pass. |

Allocation assigns; specialization realizes. A concrete part def specializes the abstract logical part def. Usage-level `allocate` of a function usage to a component usage is optional but is what makes the assignment queryable.

Spec facts you can cite: an allocation "denotes a mapping across the various structures and hierarchies of a system model" (7.15.1); a requirement definition defines "a constraint that a valid solution must satisfy" (8.3.21.8); MoE and MoP are only metadata that identify an attribute (9.3.4.2). SEBoK gives the wider ideas (MoE, MoP and TPM in its glossary; allocation under System Requirements Definition).

## Per-layer audit checklist

Run it on every element a chapter adds. Any "no" is a finding.

**Functional**
- Does each action state typed inputs and outputs, and are all flows accounted for at this level?
- Is every statement solution-independent (substitution test)?
- Are phenomena relations stated as relations (balance inequality), not as a specific part's behavior?
- Is there at least one MoE, about acceptance? If a timing or efficiency figure is filed as a MoE or a MoP, is the split justified for this case and recorded?
- Reads as an **objective**: what is good and what is good enough.

**Logical**
- Does each mechanism have a carrier (an abstract part def) and an interface that matches its neighbors?
- Do the interfaces actually match (an outlet to a power port, a tank to a fuel port)? Apply the port-type conformance check (`opensysml-query` recipe 5) from the point the connection is declared complete; before that it is reported open, not passed. The tool will not diagnose it.
- Are MoP thresholds derived from a MoE, with a means of checking, not free-standing numbers?
- Are there no solution values (no watts, no volumes) and no results entered as choices?
- Reads as a **design space**: typed, unit-bearing slots plus constraints, no solution.

**Physical**
- Is each part a concrete def that specializes an abstract logical def, and does it fit that def's interfaces?
- Do the values meet the derived thresholds, and is the TPM assessed (analysis or simulation), not asserted?
- Reads as a **candidate**: feasible against the logical layer, useful against the functional layer.

**Across layers**
- Is every leaf concrete, interfaced and verified (the stopping rule)?
- Is any emergent result set as an attribute default and then "verified"?
- Is engineering judgment recorded where it was exercised, with counterevidence and residual uncertainties, and with no "accepted" disposition?
- Do the figures show the assembled model, with what they omit stated in the caption?

## Source map

| Need | Where |
|---|---|
| A definition | `glossary` (`lookup`, `tutorial`) |
| Language semantics | SysML v2.0 spec (formal/2026-03-02), section numbers above; API spec for queries; KerML 1.1 Beta 2 for the kernel |
| Judgment records | `toaster-review-protocol`; Hawkins et al. 2011, sections 3.1 to 3.4 |
| Toaster story | Douglas Parts 3 and 4; anchors above |
| Tool behavior | `decisions/probes.md`, `opensysml-query` |
