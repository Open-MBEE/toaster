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
**Toaster issue:** (none — workaround is load-from-content; tracked here for awareness)

## D-005: Editor API does not support anonymous attribute redefinition (`:>>`)

`Editor.add_member()` cannot produce an anonymous `:>>` attribute redefinition.
The construct is defined in KerML spec §8.3.7 and accepted by the parser; the gap is in the
gRPC authoring allowlist. `attribute :>> cycleTime = 200.0 [SI::s]` must be loaded as notation.
Affects Ch2/nb02.

**Workaround:** Load `:>>` redefinitions via `conn.load_from_content(source, strict=False)`.
**Resolution:** Add anonymous redefinition path to the authoring API.
**Upstream issue:** Open-MBEE/OpenSysML#596
**Toaster issue:** (tracked here for awareness)

## D-006: Editor API does not support `require constraint` (RequirementConstraintMembership)

`Editor.add_member()` rejects `"require constraint"` as an illegal kind.
The construct is defined in SysML v2 spec formal/2026-03-02 §7.19 and accepted by the parser.
Affects Ch2/nb01.

**Workaround:** Load requirement defs including constraint bodies via `conn.load_from_content()`.
**Resolution:** Add `"require constraint"` or `add_require_constraint()` to the authoring API.
**Upstream issue:** Open-MBEE/OpenSysML#597
**Toaster issue:** (tracked here for awareness)

## D-007: Editor API does not support `assert satisfy` (SatisfyRequirementUsage authoring)

`Editor.add_member()` rejects `"assert satisfy"` as an illegal kind.
The construct is defined in SysML v2 spec formal/2026-03-02 §7.19 and accepted by the parser.
Note: combined with D-001, this construct has two distinct gaps: it cannot be added via authoring,
and it is not correctly returned by the OMG API query endpoint. Affects Ch3/nb01.

**Workaround:** Load `assert satisfy` declarations via `conn.load_from_content()`.
**Resolution:** Add `"satisfy"` / `"assert satisfy"` to the authoring allowlist.
**Upstream issue:** Open-MBEE/OpenSysML#598
**Toaster issue:** (tracked here for awareness)

## D-008: Editor API does not support `allocate` (AllocationUsage authoring)

`Editor.add_member()` rejects `"allocate"` as an illegal kind.
The construct is defined in SysML v2 spec formal/2026-03-02 §7.21 and accepted by the parser.
`generate.py` explicitly lists `allocation` as a "known skipped behavioral kind".
Affects Ch5/nb02.

**Workaround:** Load `allocate X to Y` declarations via `conn.load_from_content()`.
**Resolution:** Add `"allocate"` to the authoring allowlist and `add_allocate()` helper.
**Upstream issue:** Open-MBEE/OpenSysML#599
**Toaster issue:** (tracked here for awareness)
