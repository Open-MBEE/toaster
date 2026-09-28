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
**Upstream issue:** filed 2026-09-27, [OpenSysML#643](https://github.com/Open-MBEE/OpenSysML/issues/643)
**Toaster issue:** not filed

## D-016: Editor API does not support `perform action` authoring (gap G5)

`Editor.add_member()` has no kind for `perform action x : ActionDef` (SysML v2 formal/2026-03-02 7.17.6), the
construct that records which logical component is responsible for a function. Loading it as notation works.
Sibling of D-008 (`allocate`), D-009 (`flow`) and D-010 (state).

**Workaround:** Load `perform action` declarations via `conn.load_from_content(source, strict=False)` (Pattern B).
**Resolution:** Add `"perform"` support to the authoring allowlist. Re-confirmed 2026-09-27 against the current Editor: `add_member(kind="perform action", ...)` only queues the operation; `apply()` raises `IllegalMemberKindError`.
**Upstream issue:** filed 2026-09-27, [OpenSysML#644](https://github.com/Open-MBEE/OpenSysML/issues/644)
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
**Upstream issue:** filed 2026-09-27, [OpenSysML#645](https://github.com/Open-MBEE/OpenSysML/issues/645) (filed as a question about intended multi-resource loading, not a bug claim — the spec requirement was never established)
**Toaster issue:** not filed

## D-018: sysml-toolkit summary mode is not reachable from the CLI or Python (v0.9.1)

The v0.9.1 changelog adds summary mode for large tree graphs (collapsed containers with hidden counts, member and note
limits). It is `VizOptions::summary` in the Rust `sysmlv2-viz` crate and the WebAssembly controls only;
`sysmlv2 viz` and `Session.to_plantuml` have no such option (probed 2026-09-26, `decisions/probes.md`). Collapsing
implicit parts in notebook diagrams is therefore not available through the toolkit's CLI or Python API.

**Workaround:** choose the `element` root, the view and the filtered model slice per figure (AGENTS.md 1.7).
**Resolution:** Re-check after the next toolkit release, or request a CLI and Python option.
**Upstream issue:** filed 2026-09-27, [sysml-toolkit#5](https://github.com/Open-MBEE/sysml-toolkit/issues/5)
**Toaster issue:** not filed

## D-019: OpenSysML accepts an allocate between definitions (language conformance hole)

OpenSysML v0.9.0 loads `allocate ApplyHeat to HeatingSystem;` (an action definition and a part definition) with `ok=True`. sysml-toolkit v0.9.1 with the standard library rejects it: `ReferenceSubsetting::referencedFeature must refer to a Feature`. KerML 1.1 Beta 2 8.3.3.3.9 ReferenceSubsetting (PDF p. 203) defines the referenced element as a Feature. An allocate between usages loads in both tools. The tool rejects `perform ToastBread;` naming a definition (G2), so the allocate case is inconsistent with its own handling. Found by the Ch5 audit (`decisions/audits/ch05-layer-audit.md` F-1), confirmed by a spot review. Classified as language-tier non-conformance (DL-039); affects `models/ch05-cumulative.sysml` line 53 and the same line in ch06 to ch08.

**Workaround:** none in the model yet (Pass 4 re-derives with usages); the tutorial supplies a language-gap guard with a negative control (to be built).
**Resolution:** upstream fix in OpenSysML; re-test with `scripts/probes`.
**Upstream issue:** filed 2026-09-27, [OpenSysML#646](https://github.com/Open-MBEE/OpenSysML/issues/646) (cites and distinguishes from [OpenSysML#95](https://github.com/Open-MBEE/OpenSysML/issues/95) per the re-verification above)
**Toaster issue:** not filed

## D-020: Neither OpenSysML nor sysml-toolkit reports a part usage typed only by an item definition

`part bread : Start;` (`Start` an `item def`) loads with `ok=True` in OpenSysML v0.9.0 and passes sysml-toolkit v0.9.1 `check --lib`. SysML v2.0 (formal/2026-03-02) `validatePartUsagePartDefinition` (PDF p. 323): "At least one of the itemDefinitions of a PartUsage must be a PartDefinition" (`partDefinition->notEmpty()`). Found by the Ch5 audit (F-3), confirmed by a spot review. Classified as language-tier non-conformance (DL-039); affects `models/ch05-cumulative.sysml` lines 54 and 55 and later fixtures.

**Workaround:** the tutorial supplies a language-gap guard with a negative control (to be built).
**Resolution:** upstream fix in both tools.
**Upstream issue:** filed 2026-09-27, [OpenSysML#647](https://github.com/Open-MBEE/OpenSysML/issues/647) and [sysml-toolkit#6](https://github.com/Open-MBEE/sysml-toolkit/issues/6)
**Toaster issue:** not filed

## D-021: A false `assert satisfy` is accepted

`assert satisfy timely by slow` loads with no diagnostic while the constraint evaluates False (`slow.cycleTime` 200 s against 180 s), and the same holds for `weak` in Ch6 to Ch8 (400 W against 600 W). This is not language conformance (parse, name resolution and typing pass): it is a staged project check, "satisfaction claims evaluated" (DL-039). `assert not satisfy` parses (`isNegated: true`) and can express a deliberate failing branch. Found by the Ch3 audit (F-3), confirmed and extended by a spot review.

**Workaround:** none yet; a staged check with `slow` as its negative control is to be built.
**Resolution:** none upstream is expected (a semantic check); the tutorial owns it.
**Upstream issue:** none
**Toaster issue:** not filed

## D-022: `scripts/check_construction.py --check` now correctly fails on ch04 (predecessor-containment check, PASS2-010)

`scripts/check_construction.py` gained a predecessor-containment check (`check_predecessor_containment`, wired into `check_chapter`): for each `chNN-cumulative.sysml` where N > 1, every NAMED element present in `ch(N-1)-cumulative.sysml` (by qualified name and `@type`, via `toaster.query.ApiIndex` over the API-JSON export) must still be present in `chNN-cumulative.sysml`. Identity is restricted to NAMED elements (`_named_elements`): an unnamed member such as a `doc` has no stable qualified name to compare across two separately-edited fixtures, so it is out of scope for this check by design — a known, separate blind spot, not an oversight. It correctly reports ch04 as a failure: `models/ch04-cumulative.sysml` silently drops `ToasterDemo::TimelyToastTest` (the whole `VerificationCaseDefinition`, including its `toaster` subject reference — both NAMED) that is present in `models/ch03-cumulative.sysml` — the pre-existing defect recorded as F-5 in `decisions/audits/ch04-layer-audit.md`. The same F-5 finding's drop of `TimelyToast`'s doc/rationale is UNNAMED and is not, and cannot be, caught by this check. `scripts/check_construction.py --check` (default, no `--chapter`) now exits 1 where it previously exited 0, because this new check surfaces a real, already-existing fixture defect the old checks (fragment parses, cumulative loads) could not see. This is the correct, desired output of the new check, not a regression in the check or a fixture change: no model file was edited to make it pass. Confirmed clean for the other adjacent pairs the checker can reach through `check_chapter`'s default chapter set (ch01->ch02, ch02->ch03, ch04->ch05, ch06->ch07 — ch07 is itself a key in `CONSTRUCTION_NOTEBOOKS`, so ch06->ch07 already runs under the bare default, not only via `--chapter`) and via `--chapter=N` for the two pairs the bare default cannot reach, because chapters 6 and 8 are not keys in `CONSTRUCTION_NOTEBOOKS` (ch05->ch06, ch07->ch08) — see `tests/test_predecessor_containment.py`.

**Workaround:** none; this is not a tool gap, it is the check doing its job. Pass 4 (per the contract; see `decisions/pass4-backlog.md`) is expected to fix `models/ch04-cumulative.sysml` (restore `TimelyToast`'s rationale `doc` and `TimelyToastTest`) so the check passes again — do not silence or work around the failure before then.
**Resolution:** fix `models/ch04-cumulative.sysml` in a later pass; re-run `scripts/check_construction.py --check --chapter=4`.
**Upstream issue:** none (not a tool gap)
**Toaster issue:** not filed

## D-023: OpenSysML does not resolve state-machine transition trigger names

`accept <name>` in a transition usage is kept in the API-JSON export only as a string (`sysx:trigger`), never resolved against a declared element. A reference to an undefined name, or a typo of a defined name, loads with `ok=True` and no diagnostic; a typo'd trigger silently never fires at execution. sysml-toolkit v0.9.1 does resolve these names and warns on broken references. Found by the Ch7 audit (`decisions/audits/ch07-layer-audit.md` F-4), confirmed by independent spot review (four sub-claims reproduced on scratch models, plus confirmed the real Ch7 fixture's own triggers all resolve correctly today). A guard now exists (PASS4-000-B): `unresolved-transition-trigger` in `GAP_RULES`, `src/toaster/conformance.py` (`_unresolved_transition_trigger`), picked up automatically by `language_gap_findings`.

It flags an `accept` trigger (`sysx:triggerKeyword == "accept"`) whose payload name resolves to no declared element in scope. `sysx:trigger` is not always a plain name: it also covers a qualified name (`Outer::Start`), a named payload (`s : Start`, resolved by the part after the colon; `s :> sig`, a subsetting payload, resolved the same way), a time trigger (`accept after <duration>` or `accept at <clock-feature>`) and a change trigger (`accept when <expr>`) — the latter two are expressions, not names, and are skipped rather than flagged, as is an untriggered (unconditional) transition. The payload type can be any kind with a `declaredName` (an `item def`, `part def`, `port def`, `attribute def`, `enum def`, or an existing usage referenced by name), not only an `item def` — this also means an unqualified match is not restricted to type-like kinds at all (an unqualified trigger that happens to spell a state's own name would resolve too; an intentional, reviewed leniency, not a functional gap).

Scope (corrected in a second review round; the first round's same-package-only ruling was wrong, verified empirically before ruling again, not assumed: the real ch07 fixture itself wildcard-imports four external packages, so that scoping would have silently stopped checking exactly the fixture this guard exists to protect):

An unqualified name is resolved in three steps, in this order:

1. **Exact match.** Resolved against the declared name of *any* element anywhere in the loaded model, full stop, with no package or import modeling at all. This correctly handles a same-document, different-package reference through a wildcard or member import, and a nested/outer-package reference.
2. **Similarity match (typo detection).** If step 1 finds nothing, `difflib.get_close_matches` (Python stdlib, no new dependency) is tried against every declared name in the model, at a cutoff of 0.8. A close match is **flagged** as a plausible typo of a real local name — this is D-023's own headline case: `accept Strat` for a locally-declared `Start` (ratio 0.8) is exactly this.
3. **External-import fallback.** Only if steps 1 and 2 both find nothing does an unresolvable import in the document matter: if present, the name might be a member of it and is skipped, not flagged (the export gives no reliable, formatting-independent way to name an unresolved import's target to check further). With no such import either, the name is flagged.

**Round 3 fix, replacing an earlier round-2 mistake:** round 2's version skipped an unresolved unqualified name whenever the document had *any* unresolvable import, with no similarity check — i.e., step 3 with no step 2 in between. The reviewer found this defeats the rule's entire purpose: every real chapter model imports at least one external library (`ScalarValues`, `SI`, `ISQ`, `MeasurementReferences`), so that blanket rule silently skipped unqualified-name checking in every real chapter, including a plain `accept Strat` typo of a locally-declared `Start` — confirmed directly: replacing `Start` with `Strat` in the real ch07 and ch08 fixtures gave **zero** findings under round 2's rule. Step 2 (added this round) fixes it: a name that closely resembles something declared right here is flagged before the import fallback is even consulted, regardless of what else the document imports. This is now a permanent regression test (`test_unresolved_transition_trigger_real_fixture_typo_is_flagged`, parametrized over ch07 and ch08, using the real fixture files with the same one-word substitution) — it is what caught the bug and must keep catching a regression of it. A second dedicated test (`test_unresolved_transition_trigger_local_typo_still_flagged_with_unrelated_import`) pins the exact combination that broke: a genuine local typo, in a document that also has an unrelated external import.

The 0.8 similarity cutoff was chosen empirically against the real ch07 fixture's own 48 declared names, not picked arbitrarily: every typo form tried (`Strat`/`Start` 0.800, `Cancle`/`Cancel` 0.833, `Finsh`/`Finish` 0.909, and others) scores at or above 0.8, while the closest of 22 plausible standard-library member names tried (`Boolean`, `Vector`, `PowerValue`, ...) against that same vocabulary is `Vector` vs. the locally-declared part `ejector` at 0.769 — below 0.8, so it correctly falls through to the import-fallback step rather than being wrongly flagged. This is a fit to one real fixture's vocabulary, not a proof for all possible names; a future chapter could in principle need the cutoff re-tuned if its own vocabulary produces a false match near this boundary.

A qualified name is unaffected by this round's change: it is resolved by an exact match against every element's qualified name anywhere in the model, or a suffix match (so a legitimate relative qualification, e.g. `Inner::Start` when the full path is `P::Inner::Start`, also resolves). If neither matches, the qualified name's own top-level segment decides whether it is judged at all: a segment that names a real local package (any nesting depth) means the reference is judged and, if still unmatched, flagged as genuinely broken; a segment that does not name a local package but is a recognized standard-library package name (`ScalarValues`, `SI`, `ISQ`, `MeasurementReferences`, `Time` — the ones this repo's own models import, plus `Time`; not exhaustive of the OMG library) is treated as a probable external reference the rule cannot verify — skipped, not flagged. A segment matching neither is flagged: nothing backs reading it as external.

The round-2 final ruling on a genuine no-import cross-package reference stands unchanged this round, and is unaffected by the step-2/step-3 fix above: it is resolved at step 1, the same flat, package-blind exact match that resolves the legitimate with-import case, since step 1 never checks for an import at all. An unqualified name declared only in a different package, with no import at all bringing it into scope, is **not flagged** — a deliberate, accepted false negative (a real resolver would need the missing import for the reference to actually be legitimate; this guard cannot tell the two cases apart), disproportionate to fix with real import-graph resolution for a defect absent from every real fixture (`test_unresolved_transition_trigger_no_import_cross_package_not_flagged` still pins this down).

**Workaround:** `unresolved-transition-trigger` (see above) — now added to `language_gap_findings` in `src/toaster/conformance.py`.
**Resolution:** upstream fix (resolve triggers like `perform`/`allocate` targets are resolved); or a tutorial-supplied guard per DL-039's pattern.
**Upstream issue:** not filed — Draft 9 (`decisions/gap-issue-drafts.md`), citing SysML v2.0 formal/2026-03-02 8.3.18.8/8.3.18.9/8.3.17.2, is drafted and held for Z's review
**Toaster issue:** not filed

## D-024: RETRACTED — OpenSysML v0.9.0's Python binding cannot ask a "holds" question (sysml-toolkit can)

**Retracted the same day it was filed.** This entry originally concluded no tool in the toolchain could ask a "holds" question and that DL-046 must fall back to DL-006 standing. That was wrong: it checked only OpenSysML. `sysmlv2 verify --solve` (sysml-toolkit v0.9.1, already rebuilt in this pass) does exactly this via Z3, verified against a constructed tautology, contradiction and a bounded-range TimelyToast-shaped requirement (`decisions/probes.md`, correction entry). OpenSysML's own gap (its Python binding is evaluate-only) still stands as a fact, but is no longer a blocking gap for DL-046 since sysml-toolkit covers it. The remaining open point is architectural, not a tool gap: sysml-toolkit's Python binding has no `verify`/`solve` method, so using it from a notebook means a `subprocess` call to the Rust CLI binary rather than a Python method call. Routed to Z as a design question, not an upstream issue.

**Superseded by D-025** (below): Z decided the subprocess call is acceptable, wrapped in a utility function with an intent-to-deprecate record.

## D-025: `toaster.modelcheck` wraps `sysmlv2 verify --solve` via subprocess, intended for deprecation

sysml-toolkit's Python binding (`sysmlv2.Session`) has no `verify`/`solve` method (checked directly: not in `dir(Session)`); only the Rust CLI (`sysmlv2 verify --solve`) proves a constraint holds for all values of an unbound feature via Z3. `verify` also has no `--format json` (unlike `check`/`lint`), so the wrapper parses the CLI's stable text output. Per Z's ruling (2026-09-27, decisions/log.md DL-046): the subprocess call is accepted, wrapped in `src/toaster/modelcheck.py` so a chapter notebook sees only a clean Python function, never a shell-out, following the repo's standard gap-tracking pattern (patch, document, intend to delete once upstream supports it natively).

**Workaround:** `toaster.modelcheck.verify_holds(...)` shells out to the `sysmlv2` binary and parses its text output into a `Verdict`-shaped result.
**Resolution:** delete the wrapper and call a Python method directly once EITHER (a) sysml-toolkit's Python binding gains a `verify`/`solve` method, or (b) OpenSysML's Python binding gains a way to pose a holds/outcomes question to its own `check`/`smt` engines (D-024's original ask, still true as a fact about OpenSysML even though it is no longer blocking). **Watch specifically:** the PyPI name `sysmlv2` is already reserved by sysml-toolkit's own maintaining organization (confirmed 2026-09-27), currently holding a placeholder release, not the real package. Once that placeholder is replaced with the actual binding, check it for a `verify`/`solve` method first, before checking anywhere else.
**Provenance:** the `sysmlv2` binary this wrapper calls was built locally from `Open-MBEE/sysml-toolkit` commit `af839f0d22723772676e509213c65756d1e08ef2` (one commit past the tagged `v0.9.1` release, 2026-09-20). A learner following `docs/setup.md` instead downloads the current tagged release's pre-built binary, not this exact commit; the two have not been diffed against each other.
**Upstream issue:** not filed; not blocking (the workaround is sufficient and intended to be short-lived, not a missing-capability report)
**Toaster issue:** not filed
**CI note (PASS2-012 F7):** `tests/test_modelcheck.py` is skipped in CI — the `sysmlv2` binary is a local build artifact (`~/Documents/GitHub/sysml-toolkit/target/release/sysmlv2`), not something CI builds or installs, so the whole file is guarded by a `pytest.mark.skipif` on the binary's presence rather than run there.

## D-026: A nested step whose definition has an `in` parameter with no declared multiplicity is treated as required, though the spec's own default for it is `[0..*]`

Found building Chapter 4's own re-derivation (PASS4-004), corrected after two rounds
of independent review re-probing (Opus 5.5): nesting `ApplyHeat` as an actual step of
`ToastBread` (`action def ApplyHeat { in bread : Bread; in energy : ISQ::EnergyValue;
in duration : ISQ::DurationValue; ... }`, kept as typed, valueless functional input
slots per DL-030/DL-031's rulings) makes `model.eval()` fail on *any* attribute of a
`Toaster` part usage that transitively owns or performs that action graph, not only
on expressions that touch `ApplyHeat` itself. On the current model (`bread` bound to
`ToastBread::bread` per Q2's ruling; `energy` and `duration` left unbound),
`ToasterDemo::slow.cycleTime` (a directly-overridden literal, `200.0 [SI::s]`, with
no relation to `ApplyHeat`, `energy` or `duration` at all) raises `unbound
parameter: action ApplyHeat: input parameter energy is bound by no argument`, and so
does `ToasterDemo::timely(ToasterDemo::slow)` (the expression
`src/toaster/conformance.py::satisfaction_claims_evaluated` and Chapter 3's own
notebooks both use). Before `bread` was bound, the identical error named `bread`
instead; the isolation below was probed against a minimal model with one unbound
parameter, `bread`, and quotes that earlier message.

**The precise trigger, isolated:** a nested step whose definition has an `in`
parameter with **no declared multiplicity**, left unbound, which OpenSysML treats as
required even though the SysML v2 spec's own default for it is not `[1..1]`.
§7.6.3's tighter `[1..1]` default (SysML v2.0 formal/2026-03-02) applies only to "an
attribute usage, an item usage, ..., or a port usage" — a usage declared with a kind
keyword. `in bread : Bread;` has no kind keyword: per the grammar it is a
`DefaultReferenceUsage : ReferenceUsage` (§8.2.2.6.3), and §7.6.4 defines a
reference usage as exactly "a usage that is declared without any kind keyword." So
`bread`/`energy`/`duration` do not meet §7.6.3's condition for the `[1..1]` default;
the spec's own default for them is the general, unbounded `[0..*]` (KerML 1.1 Beta 2
agrees, calling this "the usual default"). The tool is therefore not merely being
strict about a genuinely-required parameter: it imposes a requirement the model text
does not even ask for. Seven variants were probed against the same minimal model
(`Toaster :> ToastingSystem { perform action toastBread : ToastBread { action
applyHeat : <variant>; } }`, `slow.cycleTime` evaluated):

| Variant | Result |
|---|---|
| `action def ApplyHeat { out toast : Toast; ... }` (only `out` parameters) | evaluates cleanly |
| `action applyHeat : ApplyHeat;` (`in bread`, no declared multiplicity, sequenced with `first`/`then`) | fails |
| `action applyHeat : ApplyHeat;` (`in bread`, no declared multiplicity, bare ownership, no succession, no `perform`) | fails identically |
| `ref action applyHeat : ApplyHeat;` | fails |
| `abstract action def ApplyHeat { ... }` | fails |
| `action applyHeat : ApplyHeat[0..*];` (multiplicity on the *usage*, not the parameter) | fails |
| `in bread : Bread[0..1];` (explicit multiplicity `[0..1]` stated on the **parameter itself**) | evaluates cleanly |

So the trigger is neither "any owned action" (only-`out` is fine) nor the
`perform`/succession machinery (`ref action`, bare ownership and `perform action`
all fail the same way) nor merely "any reference to a separate definition" (the
only-`out` variant is such a reference too, and it is fine, so a reference by
itself is not sufficient) — it is specifically an `in` parameter with no declared
multiplicity, left unbound. Abstractness (`abstract action def`) and multiplicity
stated on the *usage* rather than the parameter (`[0..*]`) do not rescue it, but
multiplicity stated directly on the parameter (`[0..1]`) does, confirming the
parameter's own declared multiplicity, not the reference or the step, is what the
tool keys on.

**Internal inconsistency (the clearest evidence this is a tool defect, not a
deliberate rule):** `ToastBread`'s own top-level `in bread : Bread;` has the
identical shape — no declared multiplicity, unbound — and the tool tolerates it
fine: `slow.cycleTime` evaluates cleanly when `ToastBread`'s body is `first start;
then done;` with no nested reference to a separate action definition at all. Only
the *nested* case — one level deeper, where the unbound parameter belongs to a
definition reached through another action usage rather than being the directly
performed action's own parameter — triggers the failure. Per KerML 1.1 Beta 2
§9.2.8.2.6 (`FeatureReadEvaluation`), a feature read's result is scoped to "the
values of `accessedFeature` of `onOccurrence`" — nothing in the read semantics
singles out a *nested* unbound feature for different treatment than a top-level
one, so this asymmetry is not something this citation explains.

A second, smaller inconsistency corroborates the first: the tool's own account of
what kind of feature these parameters are does not agree with itself.
`model.find("ToasterDemo::ApplyHeat::bread").kind` (and the same for `energy`,
`duration`) reports `attributeUsage`, while the same feature's API-JSON export
types it `ReferenceUsage` (confirmed directly, both checked against the real
fixture). Whichever is correct, the tool's two own surfaces for asking "what kind
of feature is this" disagree with each other, on the very parameters this gap is
about.

**Writing an explicit multiplicity bound is rejected on principle, regardless of
what the default turns out to be.** The spec's own default here is `[0..*]`, not
`[1..1]` as first thought, so `[0..1]` would *tighten* the declared multiplicity
rather than loosen it, not misstate the model in the direction first assumed. The
rejection does not depend on that direction, though: the model's real intent for
`bread`/`energy`/`duration` is exactly one value, not yet known — neither `[0..*]`
(genuinely optional, zero or many) nor `[0..1]` (genuinely optional, at most one)
states that; only an explicit `[1..1]` would, and `[1..1]` is what SysML's spec
default gives a kind-keyworded usage but not a bare reference usage like these
three. Writing `[0..1]` to silence the tool would still misstate the model to work
around a tool limitation, exactly what was rejected before, for the corrected
reason. Explicit `[1..1]` is the spec-accurate way to state the real intent, but
does **not** actually resolve this evaluability gap either way: confirmed by probe
(`in bread : Bread[1..1];`, otherwise unbound) that it fails identically to the
undeclared case (`unbound parameter: ... bound by no argument`), since the tool
already applies a `[1..1]`-shaped requirement whenever no multiplicity is stated.
So writing `[1..1]` everywhere it is spec-accurate is a genuine, separate
correctness improvement (stating the model's real intent honestly) that this gap
does not depend on and does not fix by itself. Whether to make that change is a
broader question than this gap: it would apply to every bare action and calc
parameter across every chapter (Ch1 through Ch8), not only Chapter 4's, and is out
of this contract's scope; logged separately (`decisions/next-passes.md`), not fixed
here.

**Binding one such parameter does not fix the others.** Binding `applyHeat`'s
`bread` to `ToastBread::bread` (itself unbound, but now a real reference rather
than nothing) removes `bread` from the unbound-parameter check entirely — the
error simply moves to the next unbound parameter with no declared multiplicity,
`energy` (`unbound parameter: action ApplyHeat: input parameter energy is bound by
no argument`). This is a real, if partial, improvement (Chapter 4's own
re-derivation now wires `bread` from the parent, the one flow actually available at
that level); it does not resolve the gap, since `energy` and `duration` remain
genuinely unbound (no energy source exists anywhere in the model yet).

**Workaround:** none technical that preserves the valueless-slot design DL-030 and
DL-031 require. `models/ch04-cumulative.sysml` keeps the nesting and the
declared-with-no-multiplicity, valueless `energy`/`duration` slots as ruled
(binding only `bread`, per the reason above); `src/toaster/conformance.py::
satisfaction_claims_evaluated` already treats any `model.eval` exception as a
distinguishable, reported finding rather than a silent skip or an uncaught crash,
so the resulting evaluation failure on `slow`'s Chapter-3-established `assert not
satisfy timely by slow;` claim is surfaced honestly (`tests/test_conformance.py::
test_satisfaction_claims_evaluated_scheduled_reports_execution_error_on_ch04`)
rather than hidden or worked around.
**Resolution:** upstream fix so attribute evaluation only executes the sub-graph an
expression actually depends on (lazy evaluation), so an unrelated attribute of a
part usage stays queryable while a genuinely undecided child action (typed flows
with no value, because no mechanism has been chosen yet) stays undecided; or a
documented capability to mark such a slot as "intentionally unresolved, skip if
irrelevant" for `run`-engine evaluation; or, separately, resolving the
`model.find(...).kind` vs API-JSON `@type` disagreement noted above.
**Upstream issue:** not filed — Draft 10 (`decisions/gap-issue-drafts.md`), citing
the exact reproduction, isolation table and spec citations above, is drafted and
held for Z's review.
**Toaster issue:** not filed
