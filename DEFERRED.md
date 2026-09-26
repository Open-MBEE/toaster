# Deferred work

## D-001: Ch9 satisfy-coverage uses to_api_json() workaround

`model.query()` does not return `SatisfyRequirementUsage` elements (Open-MBEE/OpenSysML#TBD).
Ch9 `01-requirement-coverage.ipynb` uses `model.to_api_json()` and filters for
`@type == 'SatisfyRequirementUsage'` as a workaround.

The workaround is encapsulated in `src/toaster/query.py::get_satisfy_relationships(model)`.
Notebook cells call that function; the workaround does not appear in notebook code.

**Resolution:** When upstream fix ships, update `get_satisfy_relationships()` and the opensysml-api skill.
**Upstream issue:** Open-MBEE/OpenSysML#590
**Toaster issue:** Open-MBEE/toaster#1

**Update (Pass 1, 2026-09-26):** `get_satisfy_relationships()` now reads `.content` and is tested (`tests/test_query.py`); the wider visibility gap, including unnamed connectors and metadata, is D-015.

## D-002: Custom theme / CSS for site

SA-5 sets default book-theme, no custom CSS, for the first release.
Custom theming improves aesthetics and brand alignment but is deferred to avoid
maintenance burden unrelated to learning outcomes in v0.1.

**Resolution:** After v0.1 ships, design a MyST theme extension or custom CSS override.
**Toaster issue:** Open-MBEE/toaster#2

## D-003: efficiency typed via MeasurementReferences::DimensionOneValue, not ISQ::DimensionOneValue

`ISQ::DimensionOneValue` is not defined in opensysml v0.9.0 (Open-MBEE/OpenSysML#TBD).
`MeasurementReferences::DimensionOneValue` exists and is functionally correct, so ch03–ch08 models
import `MeasurementReferences::*` and use `DimensionOneValue` directly. `SI::one` is also absent.

The comment `// D-003` on the import line in each model file marks the workaround sites.

**Resolution:** When `ISQ::DimensionOneValue` and `SI::one` ship in opensysml:
- Remove `private import MeasurementReferences::*;` from ch03–ch08 models.
- Change `in efficiency : DimensionOneValue;` → `in efficiency : ISQ::DimensionOneValue;`.
- Update `sysml-v2-toaster-model` skill ISQ section.
**Upstream issue:** Open-MBEE/OpenSysML#594
**Toaster issue:** Open-MBEE/toaster#8

## D-004: Editor API does not support `abstract part def` authoring

`Editor.add_member()` has no way to set the `abstract` modifier on a newly created `PartDefinition`.
The construct is defined in the SysML v2 spec and accepted by the parser; the gap is in the
gRPC authoring allowlist only. Affects Ch1/nb01.

**Workaround:** Load `abstract part def` via `conn.load_from_content(source, strict=False)`.
**Resolution:** Add `abstract` modifier support to `Editor.add_part_def()` or `add_member()`.
**Upstream issue:** Open-MBEE/OpenSysML#595
**Toaster issue:** Open-MBEE/toaster#9

## D-005: Editor API does not support anonymous attribute redefinition (`:>>`)

`Editor.add_member()` cannot produce an anonymous `:>>` attribute redefinition.
The construct is defined in KerML spec §8.3.7 and accepted by the parser; the gap is in the
gRPC authoring allowlist. `attribute :>> cycleTime = 200.0 [SI::s]` must be loaded as notation.
Affects Ch2/nb02.

**Workaround:** Load `:>>` redefinitions via `conn.load_from_content(source, strict=False)`.
**Resolution:** Add anonymous redefinition path to the authoring API.
**Upstream issue:** Open-MBEE/OpenSysML#596
**Toaster issue:** Open-MBEE/toaster#10

## D-006: Editor API does not support `require constraint` (RequirementConstraintMembership)

`Editor.add_member()` rejects `"require constraint"` as an illegal kind.
The construct is defined in SysML v2 spec formal/2026-03-02 §7.19 and accepted by the parser.
Affects Ch2/nb01.

**Workaround:** Load requirement defs including constraint bodies via `conn.load_from_content()`.
**Resolution:** Add `"require constraint"` or `add_require_constraint()` to the authoring API.
**Upstream issue:** Open-MBEE/OpenSysML#597
**Toaster issue:** Open-MBEE/toaster#11

## D-007: Editor API does not support `assert satisfy` (SatisfyRequirementUsage authoring)

`Editor.add_member()` rejects `"assert satisfy"` as an illegal kind.
The construct is defined in SysML v2 spec formal/2026-03-02 §7.19 and accepted by the parser.
Note: combined with D-001, this construct has two distinct gaps: it cannot be added via authoring,
and it is not correctly returned by the OMG API query endpoint. Affects Ch3/nb01.

**Workaround:** Load `assert satisfy` declarations via `conn.load_from_content()`.
**Resolution:** Add `"satisfy"` / `"assert satisfy"` to the authoring allowlist.
**Upstream issue:** Open-MBEE/OpenSysML#598
**Toaster issue:** Open-MBEE/toaster#12

## D-008: Editor API does not support `allocate` (AllocationUsage authoring)

`Editor.add_member()` rejects `"allocate"` as an illegal kind.
The construct is defined in SysML v2 spec formal/2026-03-02 §7.21 and accepted by the parser.
`generate.py` explicitly lists `allocation` as a "known skipped behavioral kind".
Affects Ch5/nb02.

**Workaround:** Load `allocate X to Y` declarations via `conn.load_from_content()`.
**Resolution:** Add `"allocate"` to the authoring allowlist and `add_allocate()` helper.
**Upstream issue:** Open-MBEE/OpenSysML#599
**Toaster issue:** Open-MBEE/toaster#13

## D-009: Editor API does not support `flow` (ConnectionUsage / flow connection authoring)

`Editor.add_member()` rejects `"flow"` as an illegal kind (probed 2026-09-25).
`flow X.port to Y.port` connections are defined in SysML v2 spec formal/2026-03-02 §7.20
and accepted by the parser. Affects Ch5/nb03.

Note: `editor.add_member()` signature does not include `source`/`target` parameters either;
passing them raises a `TypeError`. The kind guard fires first when using just `kind="flow"`.

**Workaround:** Load flow connection declarations via `conn.load_from_content()`.
**Resolution:** Add `"flow"` / `"flow connection"` to the authoring allowlist and `add_flow()` helper.
**Upstream issue:** Open-MBEE/OpenSysML#601
**Toaster issue:** Open-MBEE/toaster#14

## D-010: Editor API does not support `state usage` or `transition usage` authoring

`Editor.add_member()` rejects `"state usage"` and `"transition"` as illegal kinds (probed 2026-09-25).
A bare `state def Cycle;` can be added via `editor.add_member(kind='state def', name='Cycle')`,
but adding sub-states (state usages) and transition usages (with accept/then) is not supported.
Full state machines with sub-states and transitions require Pattern B. Affects Ch7/nb02.

**Workaround:** Load the full state machine declaration via `conn.load_from_content()`.
**Resolution:** Add `"state usage"` and `"transition"` to the authoring allowlist.
**Upstream issue:** Open-MBEE/OpenSysML#602
**Toaster issue:** Open-MBEE/toaster#15

## D-011: Editor API `add_attribute` produces fixed binding, not `default =` modifier

`editor.add_attribute(owner, name, type=..., value=...)` produces `attribute x : T = v`
(a fixed binding that cannot be overridden) instead of `attribute x : T default = v`
(a default value that can be overridden with `:>>`). The `default` keyword is defined in
KerML formal/2026-03-02 §8.4.1 (FeatureValue) and accepted by the parser. Affects Ch1/nb02
and all notebooks that introduce attributes with default values.

**Workaround:** Write `attribute x : T default = v;` as a SysML string fragment and load via
`conn.load_from_content()`.
**Resolution:** Add a `default` boolean parameter to `add_attribute()` so that `default=True`
produces the `default =` form.
**Spec:** KerML formal/2026-03-02 §8.4.1 — FeatureValue (default keyword)
**Upstream issue:** Open-MBEE/OpenSysML#603
**Toaster issue:** Open-MBEE/toaster#16

## D-012: Editor API `add_calc_def` produces bare declaration only (no inputs, no return expression)

`editor.add_calc_def(owner, name)` produces `calc def X;` with no `in` parameters and no
`return` expression. The `add_member` kwargs (`type`, `multiplicity`, `value`, `specializes`)
do not map onto calc def body constructs; passing unsupported kwargs raises `TypeError`.
A bare calc def cannot be evaluated with `model.eval()`. Affects Ch3/nb02.

**Workaround:** Write the full calc def body as a SysML string fragment and load via
`conn.load_from_content()`.
**Resolution:** Add `inputs` (list of `(name, type)` tuples) and `return_expression` parameters
to `add_calc_def()`.
**Spec:** SysML v2 formal/2026-03-02 §7.16 — CalculationDefinition, CalcDefBodyPart
**Upstream issue:** Open-MBEE/OpenSysML#604
**Toaster issue:** Open-MBEE/toaster#17

## D-013: Editor API `add_action_def` produces bare declaration only (no params, sequencing, or nested actions)

`editor.add_member(kind='action def', name=...)` produces `action def X;` with no `in`/`out`
parameters, no `first`/`then` sequencing, and no nested `action` usages. Passing unsupported
kwargs raises `TypeError`. Both action def body constructs and succession usages are spec-defined.
Affects Ch4/nb01.

**Workaround:** Write the full action def body as a SysML string fragment and load via
`conn.load_from_content()`.
**Resolution:** Add typed helpers `add_action_def()` / `add_action()` (or extend `add_member`)
with support for `in`/`out` parameters, nested action usages, and `first`/`then` sequencing.
**Spec:** SysML v2 formal/2026-03-02 §7.15 (ActionDefinition), §7.20 (SuccessionAsUsage)
**Upstream issue:** Open-MBEE/OpenSysML#605
**Toaster issue:** Open-MBEE/toaster#18

## D-004: VerificationMethodKind metadata not supported

The spec-defined way to annotate the method kind of a verification case is:
```sysml
#verificationMethod = VerificationMethodKind::test;
```
inside a `verification def` body (SysML v2 formal/2026-03-02 §7.24 Table 22).
In OpenSysML v0.9.0 this raises "expected a body member" and `ok=False`.

Until fixed, the verification method type is documented as text in the `doc` comment
of the verification case definition (Ch3/nb04 and `models/ch03-cumulative.sysml`).

**Resolution:** When upstream adds metadata parsing, replace the doc comment workaround
with the formal `#verificationMethod` annotation and remove the gap comment.
**Spec:** SysML v2 formal/2026-03-02 §7.24 Table 22 (Verification Methods Compartment)
**Upstream issue:** Open-MBEE/OpenSysML#608
**Toaster issue:** Open-MBEE/toaster#19

## D-014: Mismatched port types on a connection are not diagnosed (gap G4)

OpenSysML v0.9.0 accepts `connect outlet.o to torch.fuelIn` between a `PowerPort` and a `FuelPort`, and an
`interface def` with `PowerPort` ends bound to a `FuelPort`, with `ok=True` and no diagnostic. sysml-toolkit v0.9.1
`check` and `lint` (default rules) accept it too. The KerML 1.1 Beta 2 text searched has no validation constraint
requiring compatible end types (`validateConnectorRelatedFeatures` requires only two related features), so this
is treated as a **staged project conformance check** (AGENTS.md 1.9), not as a language-conformance bug.
Probe record: `decisions/probes.md`. Affects the interface chapters (the chapter that first declares a connection).

**Workaround:** `toaster.query.port_type_mismatches(model)` (tested; recipe 5 in `opensysml-query`), applied from the
chapter and section where the connection is declared complete, with a negative control; reported open before then.
**Resolution:** SysML 7.12.1 defines when connected ports *conform* but no rule found requires a tool to reject a non-conforming connection; file only a feature request (see `decisions/gap-issue-drafts.md`).
**Upstream issue:** none; Z ruled this an internal clarification, no issue to file (2026-09-26)
**Toaster issue:** none

## D-015: `model.query()` does not see unnamed connectors, `satisfy`, or metadata (gap G1; extends D-001)

Probed 2026-09-26 (OpenSysML v0.9.0): named `allocation`, `connection` and `flow` are visible to `model.query()`;
unnamed ones, every `satisfy`/`verify` (cannot be named), and `MetadataUsage` are visible only in
`json.loads(model.to_api_json().content)`. A named `perform action` appears as `ActionUsage`, and inherited
members are not expanded. The API spec's `getElements` returns "all the elements" at a commit (API and Services v1.0,
7.2.2). The repository workaround is one module, `src/toaster/query.py` (`ApiIndex`), tested in `tests/test_query.py`.
Convention adopted: name allocations, connections and flows in the model.

Related: OpenSysML#590 (closed 2026-09-26). A maintainer said anonymous elements (satisfy, connect, bind, allocate) are currently skipped and that a fix would ship in the next nightly (`nightly-20260926`). Not verified against the nightly; v0.9.0 still shows the behavior. No new issue is to be filed for this (draft 1 held).

**Workaround:** `toaster.query` helpers; JSON route for satisfy, metadata and unnamed connectors.
**Resolution:** When `model.query()` exposes all elements, change `ApiIndex` only.
**Upstream issue:** not filed (draft awaiting Z's review)
**Toaster issue:** not filed

## D-016: Editor API does not support `perform action` authoring (gap G5)

`Editor.add_member()` has no kind for `perform action x : ActionDef` (SysML v2 formal/2026-03-02 7.17.6), the
construct that records which logical component is responsible for a function. Loading it as notation works.
Sibling of D-008 (`allocate`), D-009 (`flow`) and D-010 (state).

**Workaround:** Load `perform action` declarations via `conn.load_from_content(source, strict=False)` (Pattern B).
**Resolution:** Add `"perform"` support to the authoring allowlist. Confirm against the current Editor before filing.
**Upstream issue:** not filed (draft awaiting Z's review)
**Toaster issue:** not filed

## D-017: `import` across separately loaded sources does not resolve in OpenSysML (gap G7)

A chapter source that imports an implicit part's package fails with `unresolved reference`, both through
`conn.load_from_content` and `conn.load(path)` from the same directory; concatenating the sources into one load
works. sysml-toolkit v0.9.1 resolves the same imports across files (`sysmlv2 check base.sysml chapter.sysml`,
`Session.from_files`), so the capability exists elsewhere in the ecosystem. Needed for explicit and implicit
construction (AGENTS.md 1.7).

**Workaround:** assemble by concatenation: join the SysML text yielded by the implicit modules and the chapter's
explicit increment into one string and load once. Concatenation loses which source an element came from, so give
implicit parts their own package (or a metadata marker) to keep provenance queryable.
**Resolution:** Check the spec's package-import and the API's project and commit model for the multi-resource
resolution it requires; file only what the spec requires. Re-test when OpenSysML changes.
**Upstream issue:** not filed (draft awaiting Z's review)
**Toaster issue:** not filed

## D-018: sysml-toolkit summary mode is not reachable from the CLI or Python (v0.9.1)

The v0.9.1 changelog adds summary mode for large tree graphs (collapsed containers with hidden counts, member and note
limits). It is `VizOptions::summary` in the Rust `sysmlv2-viz` crate and the WebAssembly controls only;
`sysmlv2 viz` and `Session.to_plantuml` have no such option (probed 2026-09-26, `decisions/probes.md`). Collapsing
implicit parts in notebook diagrams is therefore not available through the toolkit's CLI or Python API.

**Workaround:** choose the `element` root, the view and the filtered model slice per figure (AGENTS.md 1.7).
**Resolution:** Re-check after the next toolkit release, or request a CLI and Python option.
**Upstream issue:** not filed (draft awaiting Z's review)
**Toaster issue:** not filed
