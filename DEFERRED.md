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
