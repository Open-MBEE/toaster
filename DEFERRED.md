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

**Workaround:** the tutorial supplies a language-gap guard, `allocate-between-definitions` (`src/toaster/conformance.py`, `GAP_RULES`), with its own negative control -- the guard already exists (corrected 2026-09-29, DL-059 ADDENDUM: this line previously said "to be built" after the guard had already landed). Extended 2026-09-29 (DL-059 ADDENDUM 3, Task 7 F-1): originally checked only the connector end's own final target (`end[-1]`); now checks EVERY segment of a chained end, since a MIDDLE segment resolving to a Definition (e.g. `allocate doApply to toaster.Inner.heater;` where `Inner` is a nested `part def`) is the same ReferenceSubsetting violation and was previously invisible to every rule. This also makes `allocate-between-definitions` the sole owner of the chain-ROOT-is-a-Definition case: `allocate-connector-end-accessibility` (D-032) used to check that case on its own, and its own now-redundant chain-root check was removed in the same fix to avoid double-flagging -- the division of labor is now: `allocate-between-definitions` (D-019) checks whether every segment of an end is a Feature, not a Definition, regardless of position in the chain; `allocate-connector-end-accessibility` (D-032) checks whether the chain's first segment, GIVEN that it is a Feature, is actually accessible from the allocation's own context.
**Resolution:** upstream fix in OpenSysML; re-test with `scripts/probes`.
**Upstream issue:** filed 2026-09-27, [OpenSysML#646](https://github.com/Open-MBEE/OpenSysML/issues/646) (cites and distinguishes from [OpenSysML#95](https://github.com/Open-MBEE/OpenSysML/issues/95) per the re-verification above)
**Toaster issue:** not filed

## D-020: Neither OpenSysML nor sysml-toolkit reports a part usage typed only by an item definition

`part bread : Start;` (`Start` an `item def`) loads with `ok=True` in OpenSysML v0.9.0 and passes sysml-toolkit v0.9.1 `check --lib`. SysML v2.0 (formal/2026-03-02) `validatePartUsagePartDefinition` (PDF p. 323): "At least one of the itemDefinitions of a PartUsage must be a PartDefinition" (`partDefinition->notEmpty()`). Found by the Ch5 audit (F-3), confirmed by a spot review. Classified as language-tier non-conformance (DL-039); affects `models/ch05-cumulative.sysml` lines 54 and 55 and later fixtures.

**Workaround:** the tutorial supplies a language-gap guard, `part-typed-only-by-item-def` (`src/toaster/conformance.py`, `GAP_RULES`), with its own negative control -- the guard already exists (corrected 2026-09-29, DL-059 ADDENDUM: this line previously said "to be built" after the guard had already landed).
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

**PASS4-007 note.** Chapter 7's own re-derivation rebuilt `Cycle` as a real `state def`, exhibited by `ToastingSystem` (the abstract subject; `Toaster` inherits it, per DL-019/DL-044), with the same `Start`/`Finish`/`Cancel` triggers this entry already covers. `chapters/ch07-execution/02-state-traces.ipynb` now demonstrates the guard directly, the first chapter notebook to do so: a scratch copy of the real, loaded `ch07-cumulative.sysml` with `Start` typo'd to `Strat` loads with `ok=True` (OpenSysML itself does not catch it), and `language_gap_findings` flags it as `unresolved-transition-trigger`. This is the same construct and mechanism this entry already documents; no new finding, no new draft.

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

## D-026: OpenSysML treats an implicit and an explicit-but-spec-identical `[0..*]` multiplicity differently for an `in` parameter reachable through a nested action step

**Headline finding:** writing a bare `in` parameter's already-implicit multiplicity
out explicitly, changing nothing about what the declaration means, changes whether
OpenSysML v0.9.0 can evaluate the model. `in energy : ISQ::EnergyValue;` (no
multiplicity written) and `in energy : ISQ::EnergyValue[0..*];` (the multiplicity
SysML v2.0's own default already gives the first form, §7.6.3/§7.6.4, see below) are
spec-identical declarations. The tool accepts both (`model.ok == True`), but only
the second keeps the model evaluable.

Found building Chapter 4's own re-derivation (PASS4-004), corrected across five
rounds of independent review re-probing (Opus 5.5): nesting `ApplyHeat` as an actual
step of `ToastBread` (`action def ApplyHeat { in bread : Bread; in energy :
ISQ::EnergyValue; in duration : ISQ::DurationValue; ... }`, kept as typed, valueless
functional input slots per DL-030/DL-031's rulings) made `model.eval()` fail on
*any* attribute of a `Toaster` part usage that transitively owns or performs that
action graph, not only on expressions that touch `ApplyHeat` itself.
`ToasterDemo::slow.cycleTime` (a directly-overridden literal, `200.0 [SI::s]`, with
no relation to `ApplyHeat`, `energy` or `duration` at all) raised `unbound
parameter: action ApplyHeat: input parameter energy is bound by no argument` (and
`bread`, before it was bound to `ToastBread::bread` per Q2's ruling), and so did
`ToasterDemo::timely(ToasterDemo::slow)` (the expression
`src/toaster/conformance.py::satisfaction_claims_evaluated` and Chapter 3's own
notebooks both use).

**The precise trigger, isolated in two separate experiments.**

*Experiment 1 (which construction reaches the parameter at all).* Six variants,
each varying only how `ApplyHeat` is referenced, all tested on the same single
parameter (`in bread : Bread;`, left as declared, no multiplicity written), against
the same minimal model (`Toaster :> ToastingSystem { perform action toastBread :
ToastBread { action applyHeat : <variant>; } }`, `slow.cycleTime` evaluated):

| Variant | Result |
|---|---|
| `action def ApplyHeat { out toast : Toast; ... }` (only `out` parameters, no `in` at all) | evaluates cleanly |
| `action applyHeat : ApplyHeat;` (sequenced with `first`/`then`) | fails |
| `action applyHeat : ApplyHeat;` (bare ownership, no succession, no `perform`) | fails identically |
| `ref action applyHeat : ApplyHeat;` | fails |
| `abstract action def ApplyHeat { ... }` | fails |
| `action applyHeat : ApplyHeat[0..*];` (multiplicity on the *usage*, not the parameter) | fails |

So the trigger is not "any owned action" (only-`out` is fine), not the
`perform`/succession machinery (`ref action`, bare ownership and `perform action`
all fail the same way), and not merely "any reference to a separate definition"
(the only-`out` variant is such a reference too, and it is fine). It is specifically
an unbound `in` parameter, reached through a nested step, that matters — which
motivates Experiment 2.

*Experiment 2 (what about the parameter's declared multiplicity matters).* With the
nesting held fixed at the failing shape above, only `energy`'s declared multiplicity
was varied, one value at a time, each tested in isolation (no other unresolved `in`
parameter present in that run):

| Declared multiplicity on `energy` | Result |
|---|---|
| none written (the bare, implicit form) | fails |
| `[1..1]` (explicit) | fails |
| `[1]` | fails |
| `[1..*]` | fails |
| `[2..*]` | fails |
| `[0..*]` (explicit, spec-identical to the implicit default — see below) | evaluates cleanly |
| `[0..1]` | evaluates cleanly |
| `[0..2]` | evaluates cleanly |
| `[*]` | evaluates cleanly |

**The mechanism this evidence actually supports:** OpenSysML v0.9.0 gives a
keyword-less `in` parameter (a `ReferenceUsage` per the grammar, §8.2.2.6.3) the
tighter `[1..1]` default that SysML v2.0 formal/2026-03-02 §7.6.3 reserves for "an
attribute usage, an item usage, ..., or a port usage" — usages declared *with* a
kind keyword, which a bare `in` parameter is not (§7.6.4: "a reference usage is a
usage that is declared without any kind keyword"). This matches the tool's own
`model.find(...).kind` reporting `attributeUsage` for these parameters even though
the API-JSON export types them `ReferenceUsage` (a second, smaller inconsistency,
kept below as corroborating evidence). Having applied that wrong `[1..1]`-shaped
default, the tool then raises whenever a nested step's parameter has an effective
lower bound of 1 or more and is left unbound — which is why every multiplicity with
lower bound ≥ 1 (bare, `[1..1]`, `[1]`, `[1..*]`, `[2..*]`) fails identically, and
every multiplicity with lower bound 0 (`[0..*]`, `[0..1]`, `[0..2]`, `[*]`)
evaluates cleanly. This is a coherent, if wrong, rule — not, as an earlier draft of
this entry claimed, a tool that "keys on whether a multiplicity token is present in
the text" regardless of what it means: that reading is contradicted by explicit
`[1..1]` failing exactly like the bare form.

The spec's own default for `bread`/`energy`/`duration`, none of which carries a kind
keyword, is the general, unbounded `[0..*]` (KerML 1.1 Beta 2 agrees, calling this
"the usual default"), not the `[1..1]` the tool applies. Writing `[0..*]` out
explicitly states nothing the bare declaration did not already mean per §7.6.3/
§7.6.4 — it is spec-identical to the implicit default — and it evaluates cleanly.
That is the headline finding: an implicit and an explicit-but-spec-identical
declaration should behave the same under any coherent reading of the spec, and in
this tool they do not.

**Reproducing the applied fix precisely.** `ApplyHeat` as built has *three*
unbound-by-default `in` parameters (`bread`, `energy`, `duration`), not one — a
reader who changes only one of them (say, `energy`'s multiplicity) on the full,
real `ApplyHeat` and expects `slow.cycleTime` to evaluate will still see the
failure, now naming whichever of the other two parameters is still unresolved
(`bread`, then `duration`, in declaration order). This is expected, not a
contradiction of Experiment 2 above (which isolates one parameter at a time in a
model with no other unresolved `in` parameter) or of the applied fix (which
resolves all three: `bread` by reference-binding to `ToastBread::bread`, per Q2's
ruling, and `energy`/`duration` by explicit `[0..*]`). All three must be resolved,
by whichever means, before the model is fully evaluable again.

**Internal inconsistency (further evidence this is a tool defect, not a
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

`[1..1]` (which would be the spec-accurate way to state that
`bread`/`energy`/`duration` mean exactly one value, not yet known, rather than
`[0..*]`'s "any number, including none") fails identically to the bare form, per
Experiment 2 above — expected under the mechanism this entry now gives, since
`[1..1]` has lower bound 1, same as the tool's own wrong default. Whether to write
`[1..1]` everywhere it is spec-accurate across the tutorial, trading the tool's
current bug (which the model does not need to work around, since `[0..*]` already
does) for stating each parameter's true intended cardinality, is a broader, separate
question than this gap, spanning every chapter's action and calc parameters, not
just Chapter 4's; logged separately (`decisions/next-passes.md` item 11).

**`[0..1]` is a real technical workaround, considered and rejected; `[0..*]` is the
applied fix.** `[0..1]` does avoid the failure (confirmed above), but it is **not
used**: it narrows the multiplicity below the spec's own `[0..*]` default and
asserts `bread`/`energy`/`duration` are genuinely optional (zero-or-one) inputs to
`ApplyHeat`, neither of which is true — the action needs all three to mean
anything; they are simply not yet bound to a value at this stage of decomposition.
`[0..*]`, by contrast, is not a rejected workaround: `models/ch04-cumulative.sysml`
now declares `in energy : ISQ::EnergyValue[0..*]` and `in duration :
ISQ::DurationValue[0..*]` (`bread` stays unannotated, already bound to
`ToastBread::bread` per Q2). This is **the applied fix**, not a documented
alternative, because writing it states nothing the bare declaration did not already
mean per §7.6.3/§7.6.4: DL-030/DL-031's requirement (typed, unit-bearing, no value)
is completely unaffected, the parameter is exactly as valueless and exactly as
"not yet bound" as before, and the model's claim about `energy`/`duration` has not
changed at all. Verified: `model.ok == True`; `slow.cycleTime` and
`timely(slow)` both evaluate normally again (`slow.cycleTime` returns `200 [SI::s]`,
`timely(slow)` returns `False`, matching Chapter 3's own established result); the
balance constraint (`assert constraint balance { delivered >= 0.0 [SI::J] and loss
>= 0.0 [SI::J] and delivered + loss <= energy }`) still evaluates correctly against
`energy[0..*]`, holding for a plausible split and failing for both an overdrawn and
a negative-loss one.

**Side effect worth noting:** under explicit `[0..*]`, the tool also now accepts a
*multi-valued* `energy` (more than one bound value), which the balance constraint's
`<= energy` cannot evaluate (reports a type mismatch between a quantity and a
sequence). Nothing in the tutorial ever supplies more than one value, so this has
no practical effect here, but it shows `[0..*]` only really makes sense for these
parameters because exactly one value is what every actual use assumes — reinforcing
that `[1..1]` is the spec-accurate statement of intent (`decisions/next-passes.md`
item 11), even though `[0..*]` is what the tool currently requires.

**Workaround:** the applied fix above (explicit `[0..*]` on `energy` and
`duration`) is spec-neutral and needs no separate workaround language:
`src/toaster/conformance.py::satisfaction_claims_evaluated` now reports Chapter 4's
`slow` claim exactly as it reports Chapter 3's (`passed`, no findings;
`tests/test_conformance.py::
test_satisfaction_claims_evaluated_scheduled_reports_no_findings_on_ch04`).
**Resolution:** upstream fix so an implicit and an explicit-but-identical
multiplicity are treated the same (the headline finding above), or documentation
explaining why they are not; separately, resolving the `model.find(...).kind` vs
API-JSON `@type` disagreement noted above.
**Upstream issue:** not filed — Draft 10 (`decisions/gap-issue-drafts.md`), citing
the exact reproduction, isolation table and spec citations above, is drafted and
held for Z's review.
**Toaster issue:** not filed

**PASS4-007 note.** Chapter 7's state machine hits this exact gap. `Cycle`'s
`heating` state was first tried with `do action applyHeat : ApplyHeat;`, invoking
`ApplyHeat` directly, the same action `HeatingSystem` performs. `execute_state`
then raised `ExecutionError: state machine execution failed: do action in state
heating: unbound parameter: action ApplyHeat: input parameter bread is bound by
no argument`: `ApplyHeat`'s own `bread` input (deliberately left bare, per Q2's
ruling, since it is always reference-bound wherever `ApplyHeat` is actually
invoked, e.g. `ToastBread::applyHeat { in bread = ToastBread::bread; }`) has no
value at this level of decomposition, and `Cycle` has no bread instance to bind
it to. Confirmed this is genuine execution, not a load-time artifact: temporarily
breaking `GenerateHeat`'s own already-fixed `[0..*]` multiplicity on `energyIn`
reproduces the identical failure shape (`unbound parameter: action GenerateHeat:
input parameter energyIn is bound by no argument`), proving the do action really
executes whatever it names. `GenerateHeat` was used instead
(`do action generateHeat : GenerateHeat;`): its own input is already `[0..*]`
(this entry's own applied fix), so it stays executable with no value bound. This
is not itself a new instance of D-026 (the unbound `bread` failure is correct
tool behavior given a genuinely unresolved required input, not the eager-eval bug
this entry documents), but it depends directly on D-026's applied fix to work at
all, so it is recorded here rather than as a separate entry.

## D-027: a second declaration reopening an existing namespace member's name loads with warnings, then crashes `to_api_json()`

**Found:** PASS4-005 (Chapter 5 re-derivation), while probing whether a definition
could be extended across two separate declarations sharing one name (a pattern
briefly considered, then not used, for spreading `HeatingSystem`'s construction
across two notebooks). Independently reproduced by the reviewer, who caught that
an earlier draft of this repro was missing the import `Real` needs and so
actually failed with `ok=False` (`unresolved: Real`), a different error than the
one this entry documents; the corrected repro below was re-verified directly.

**Observed.** `package P { private import ScalarValues::*; part def X; part def
X { attribute a : Real; } }` (two owned members of the same package sharing the
name `X`) loads with `model.ok == True` and two `severity='warning'`,
`code='name-conflict'` diagnostics ("Duplicate of other owned member name"),
one per declaration. `model.find("P::X")` returns a single resolved symbol.
Calling `model.to_api_json()` on the same loaded model raises `ConversionError:
cannot convert the duplicate declaration of "X" at <content>:L:C: a name
identifies an element in the graph, so two members of one namespace cannot
share it`, not a diagnostic on the model itself.

**Why this matters for the tutorial.** Every helper this repo uses for anything
beyond `model.query()`/`model.find()` (`toaster.query.ApiIndex` and everything
built on it: `find_connectors`, `find_allocations`, `perform_relationships`,
`port_type_mismatches`, `build_interconnection_intent`, and
`scripts/check_construction.py`'s own predecessor-containment check) goes
through `to_api_json()`. A model that loads cleanly by every check that reads
`model.ok` or iterates `model.query()` can still be silently unusable by every
one of those helpers, with the actual cause (a name collision loudly warned
about at load time) two calls removed from the crash site.

**Not yet resolved which of two readings is correct:** (a) `to_api_json()`
should tolerate what `load_from_content` already accepts with only a warning,
returning some deterministic disambiguation; or (b) a same-namespace,
same-name second declaration should itself be a load-time error (elevate the
warning), since two OpenSysML surfaces (load, and the API-JSON conversion this
model uses for everything else) disagreeing about whether the model is valid
is the more fundamental problem, independent of which one is "right." No
spec constraint naming this exact case was checked against the PDF text
directly (only the diagnostic message and the observed behavior); this entry
does not claim a specific spec section, unlike D-019/D-020.

**Workaround:** none needed in shipped content; PASS4-005 designed around the
pattern entirely rather than using it (every construction-zone fragment that
extends an earlier notebook's type restates it completely, rather than
reopening it). Flagged here so a future builder does not reach for the
"reopen to add a member" idiom expecting it to be safe.
**Resolution:** none attempted; needs Z's read on which of the two framings
above is the actual bug, before filing an upstream report.
**Upstream issue:** not filed — Draft 11 (`decisions/gap-issue-drafts.md`),
citing the exact reproduction above and naming the two unresolved framings, is
drafted and held for Z's review.
**Toaster issue:** not filed

## D-028: `model.execute_state`'s `performer` argument has no effect on the result

**Found:** PASS4-007 (Chapter 7 re-derivation, round 3 review), while checking a
notebook claim that naming a specific usage (e.g. `ToasterDemo::nominal`) as
`performer` demonstrates that `Toaster` inherits and executes the state machine
`ToastingSystem` exhibits. Independently reproduced by the orchestrator directly
against the real, committed `models/ch07-cumulative.sysml` before this entry was
written, not just taken from the reviewer's report.

**Observed.** `model.execute_state("ToasterDemo::Cycle", events=["Start","Finish"])`
returns the identical `{"states_visited": [...], "final_context": {}, "final_time":
0.0}` regardless of `performer`: no argument at all, `ToasterDemo::nominal` (a real
`Toaster` usage that inherits `cycle`), `ToasterDemo::rated` (a `ResistanceCoil`
usage that exhibits nothing at all), and `ToasterDemo::Bread` (an `item def`, not
even a part) all give the same trace. Only a `performer` name that resolves to no
symbol at all changes anything (`ExecutionError: symbol not found`). The tool does
not check that the named performer actually exhibits the state being executed, and
does not vary the trace by what it is given.

**Why this matters for the tutorial.** `execute_state` runs a state def's own
transition table in isolation; it is not, as written, a way to demonstrate that a
particular usage inherits and can execute an exhibited state machine through
specialization. That inheritance is a fact about the model's structure (checkable
via `model.find`, e.g. `Toaster::cycle` resolving to `None` the same way
`Toaster::toastBread` does, both inherited from `ToastingSystem` and not
redeclared), not something the execution trace itself shows.

**Workaround:** none needed in shipped content; Chapter 7's own re-derivation
(`chapters/ch07-execution/02-state-traces.ipynb`) states the distinction directly
rather than claiming the trace demonstrates inheritance.
**Resolution:** none attempted; would need `execute_state` to validate that
`performer` (when given) actually exhibits the named state, and ideally to be
usable at all as a way to execute a state machine through a specific realizing
usage rather than only through the state def's own qualified name.
**Upstream issue:** not filed; not blocking (a documentation/API-surface gap, not
a load-time or evaluation-correctness defect).
**Toaster issue:** not filed

## D-029: `toaster.modelcheck.verify_holds`'s line parser cannot read a `verify --solve` verdict for an `assert satisfy`/`assert not satisfy` declaration

**Found:** PASS4-008 (Chapter 8 re-derivation), while probing whether `verify_holds`
could run directly against the real, committed `models/ch08-cumulative.sysml`
(which carries Chapter 3's and Chapter 6's `assert satisfy`/`assert not satisfy`
declarations forward from Chapter 7) rather than a small companion file.

**Observed.** For an ordinary `constraint`/`assert constraint`, the CLI's verdict
line is `<file>:<line>:<col>  <name> (<Kind>): <status>[ (<reason>)]`, which
`toaster/modelcheck.py`'s `_LINE_RE` already parses. For a constraint that is also
the subject of an `assert satisfy`/`assert not satisfy` declaration, the real CLI
instead prints one extra verdict line per such declaration, with the kind
parenthetical widened to `(<Kind>, satisfies <requirement>)` and no separate reason
parenthetical, e.g. (all three lines reproduced verbatim from a real run against
`models/ch08-cumulative.sysml`):

    <file>:83:30  <anonymous> (ConstraintUsage, satisfies ToasterDemo::timely): VIOLATED
    <file>:184:30  <anonymous> (ConstraintUsage, satisfies ToasterDemo::heatGenerationReq): satisfied
    <file>:184:30  <anonymous> (ConstraintUsage, satisfies ToasterDemo::heatGenerationReq): VIOLATED

**Correction (round 2 review, PASS4-008):** the first draft of this entry claimed
the CLI also prints a `not satisfies <requirement>` variant for a negative
declaration (`assert not satisfy ... by ...`). Checked directly against the real
CLI and found false: every satisfy/not-satisfy declaration prints the identical
`satisfies <requirement>` wording (there is no `not satisfies` form at all), and
the two are disambiguated only by the verdict word, which reports whether the
requirement's own constraint holds for that subject, not whether the surrounding
`assert`/`assert not` declaration's own polarity was upheld. The line 83 example
above is `slow`'s `assert not satisfy timely by slow;`: `VIOLATED` means the
constraint `toaster.cycleTime <= 180.0` is false for `slow` (cycleTime 200), which
is exactly what the negated declaration correctly asserts should happen. The two
line-184 examples are `rated`'s `assert satisfy heatGenerationReq by rated;`
(`satisfied`: `heatGen.power >= 600.0` is true, power 800) and `weak`'s
`assert not satisfy heatGenerationReq by weak;` (`VIOLATED`: the same constraint
body is false for `weak`, power 400, again the outcome the negated declaration
correctly asserts): the same source line and column because both usages check the
same `require constraint` body text, against different subjects.

`_LINE_RE` matches `(?P<kind>\w+)` only, so the comma and the trailing
`satisfies ...` text do not match, and `verify_holds` raises
`ModelCheckError(f"could not parse verdict line {line!r}")` on any file containing
such a declaration, real CLI output that is well-formed, not a CLI error.

**Why this matters for the tutorial.** `models/ch08-cumulative.sysml` (like
`ch03-cumulative.sysml` onward) carries `assert satisfy`/`assert not satisfy`
declarations forward from Chapter 3 and Chapter 6, so `verify_holds` cannot be run
directly against the real, committed cumulative fixture at all right now, only
against a file that carries no such declaration.

**Workaround:** `chapters/ch08-checking/02-violation-witness.ipynb` runs
`verify_holds` against a small companion file assembled in the notebook itself (not
committed to `models/`), restating only `deliveredEnergyBoundedBySupply` and the
two usages it needs, which carries no `assert satisfy` declaration and so never
hits this parser gap. The construct itself is real, committed content in
`models/ch08-cumulative.sysml` (introduced in
`chapters/ch08-checking/01-invariant-def.ipynb`); only the file handed to
`verify_holds` is a restatement, and the notebook says so. See D-030 and D-031 for
the separate, deeper reason this construct is a hand-restated lemma rather than a
solver-checked reference to `HeatGenerator`'s own `efficiencyBounded` and
`deliveredEnergy`, which is a real limit of this toolchain, not only a parser gap.
**Resolution:** widen `_LINE_RE` (or add a second pattern) to accept an optional
`, satisfies <requirement>` segment inside the kind parenthetical (no `not`
variant exists, per the correction above), verified against the real CLI's exact
text before shipping the fix, per the module's own requirement that every case be
checked against a real run. **Caution for whoever fixes this:** a naive fix that
only widens the regex, without also teaching `holds()`'s own status precedence
about the satisfy/not-satisfy distinction, would make `holds()` read the real
model's own *correct* negative claims (`assert not satisfy timely by slow`,
`assert not satisfy heatGenerationReq by weak`, both `VIOLATED` verdicts exactly
as intended) as if they were failures of the model, since `holds()`'s
violated-beats-everything precedence has no way to know a `VIOLATED` verdict on a
`not satisfy` declaration is the correct, desired outcome. Fixing the parser alone
is not enough; the caller-facing semantics need the same care `satisfaction_claims_evaluated`
already gives this distinction (its own `is_negated` handling in `src/toaster/conformance.py`).
**Upstream issue:** not filed; not applicable (this is this repository's own
wrapper, not a claim about the `sysmlv2` CLI, which is behaving correctly).
**Toaster issue:** not filed; not blocking (the companion-file workaround is
sufficient for this chapter; `src/toaster/modelcheck.py` is outside this
contract's blast zone).

**Note (round 2 review, PASS4-008): a `satisfied` verdict can come from interval
propagation alone, not necessarily Z3.** `verify --solve` runs propagation first
and only hands Z3 whatever propagation left undecided (per the CLI's own `--help`
text), so a verdict's `reason` can read `(propagation: holds for all values in the
narrowed ranges)` with no `z3:` text at all, even though the summary line and the
top-level status are identical to a genuinely solver-proved `satisfied`. Confirmed
directly against the real committed `models/ch08-cumulative.sysml`:
`efficiencyBounded` itself (`0.0 <= efficiency and efficiency <= 1.0`, a bound with
no other feature to relate) is reported `satisfied (propagation: holds for all
values in the narrowed ranges)`, never invoking Z3 at all, while
`deliveredEnergyBoundedBySupply` (an implication over three unbound features) is
reported `satisfied (z3: holds for all values of unbound features)`. Anyone
checking "was this actually proved by the solver, not merely by range narrowing"
should read the verdict's `reason` text, not just its `status`; `ConstraintVerdict`
carries both, and `chapters/ch08-checking/02-violation-witness.ipynb` asserts on
the reason text for exactly this purpose.

## D-030: two independently-declared `assert constraint`s are never composed by `verify --solve`, whether sibling or inherited

**Found:** PASS4-008 round 2 review (Opus 5.5), confirming that
`deliveredEnergyBoundedBySupply` (Chapter 8's new construct) is not actually
solver-linked to `HeatGenerator`'s own `efficiencyBounded` and `deliveredEnergy`,
despite the chapter's first-round prose claiming it proves the entailment those
two already imply. Independently reproduced by the builder with two further
constructed probes before writing this entry.

**Observed.** `verify --solve` checks each `assert constraint` (or `constraint`)
body entirely on its own: nothing in the tool treats an already-declared sibling
or inherited constraint as an assumed-true hypothesis available to a different
constraint's own body, even when both are members of the exact same part def.
Three constructed reproductions, all giving `undecided` with a genuine Z3 witness
(not a parse error, not a trivial fold):

1. **Sibling, same def, bare (non-dotted) feature references:** a second
   `assert constraint` added directly inside `HeatGenerator` alongside
   `efficiencyBounded`, referencing the bare `power`/`efficiency` features (no
   `heatGenCheck.` qualification) plus a new local `duration`-typed attribute, with
   no restated bound in its own antecedent:
   `undecided (result is indeterminate over unbound features) (z3: satisfiable,
   e.g. power = 0 [W], checkDuration = -1 [s], efficiency = 2)`. `efficiencyBounded`
   itself still reports `satisfied` alongside it, unaffected, and does nothing to
   constrain the second constraint's own check.
2. **Inherited via specialization:** the same second constraint moved onto a new
   subtype `HeatGeneratorCheck :> HeatGenerator`, so it inherits `efficiencyBounded`
   through specialization rather than sibling membership: identical `undecided`
   verdict and witness.
3. **Confirms the point directly on the real committed model:** loosening
   `efficiencyBounded`'s own literal bound in `models/ch08-cumulative.sysml` from
   `<= 1.0` to `<= 1.5`, or doubling `deliveredEnergy`'s own definition from
   `power * duration * efficiency` to `power * duration * efficiency * 2.0`, leaves
   `deliveredEnergyBoundedBySupply`'s verdict unchanged (`satisfied`) either way,
   because the construct's own antecedent restates its own copy of the bound and
   its own copy of the arithmetic rather than referencing either original element.

**Why this matters for the tutorial.** Any assert constraint meant to state "given
some other already-declared constraint holds, prove this" must restate that other
constraint's own hypothesis inline (which is legitimate and is what
`tests/test_modelcheck.py`'s own `TIMELY_TOAST` fixture already does); it cannot
rely on inheritance or same-scope membership to import the other constraint's
truth automatically. A property phrased this way is therefore only ever a
standalone lemma of the same shape as the original elements, never a solver-
checked reference to them, and re-checking it after either original element
changes is a manual, not automatic, step.

**Workaround:** `deliveredEnergyBoundedBySupply`'s own doc comment, and Chapter 8's
prose (`chapters/ch08-checking/01-invariant-def.ipynb`,
`02-violation-witness.ipynb`, `index.md`, `conclusion.md`), state this limit
plainly rather than claiming a link the toolchain cannot check.
**Resolution:** none attempted; would need `verify --solve` (or a successor tool)
to treat already-proved sibling or inherited constraints as background axioms
when checking a new one, a nontrivial solver-integration feature, not a parsing
fix.
**Upstream issue:** not filed; a real capability gap in `sysml-toolkit`'s
`verify --solve`, worth raising once this pattern recurs enough to justify asking
for it, not this contract's call to file alone.
**Toaster issue:** not filed

## D-031: a chained calc/function invocation inside an `assert constraint` is not in Z3's solvable fragment

**Found:** PASS4-008 round 2 review (Opus 5.5), same probe session as D-030;
independently reproduced by the builder.

**Observed.** `assert constraint c { ... heatGenCheck.deliveredEnergy(power, duration) <= power * duration ... }`
(calling a `calc` through a usage's own dotted path, rather than restating the
calc's body inline) gives:
`undecided (result is indeterminate over unbound features; z3: not in the
solvable fragment: chained function references)`, regardless of what the calc's
own definition actually computes (confirmed alongside D-030's probe 3: the verdict
does not change even when the calc's own definition is edited).

**Why this matters for the tutorial.** A property that needs to reason about what
a `calc` actually computes cannot invoke the calc from inside an `assert
constraint` and expect Z3 to reason through the call; the calc's own body must be
restated inline in the constraint (exactly what `deliveredEnergyBoundedBySupply`
does), which is why the tutorial's new construct is a hand-restated lemma rather
than a call into `deliveredEnergy` itself.

**Workaround:** none needed; the chapter's own construct never attempts a chained
calc invocation, and its prose says why.
**Resolution:** none attempted; would need `verify --solve`'s Z3 encoding to
inline or symbolically expand a calc invocation, a solver-integration feature.
**Upstream issue:** not filed, for the same reason as D-030.
**Toaster issue:** not filed

## D-032: OpenSysML accepts an allocate connector end that reaches into another type's nested feature by qualified name, with no featuring context to make it accessible (GUARDED)

OpenSysML v0.9.0 loads `allocate <expr> to <Def>::<usage>;` (a package-level allocate whose end is a bare qualified-name reference into a feature nested inside a Definition the allocation is not itself featured within — e.g. `allocate ToastBread::applyHeat to Toaster::heating;`) with `ok=True` and no diagnostic; sysml-toolkit v0.9.1 accepts it too (its `connectors.rs` documents a "one-hop featuring lift" with no counterpart in the spec). KerML 1.1 Beta 2 validateSubsettingFeaturingTypes (8.3.3.3.4, p. 204) requires `subsettingFeature.canAccess(subsettedFeature)`, which requires the referenced feature to be `isFeaturedWithin` one of the connector end's featuringTypes (canAccess 8.3.3.3.4 p. 188; isFeaturedWithin p. 190); checkConnectorTypeFeaturing (8.3.4.5.3, pp. 214-215) finds no featuringType in common between the two definitions either, so no implied TypeFeaturing rescues it. Ruled DL-058: the tutorial's own ch05-ch08 fixtures carried exactly this construct (`ToastBread::applyHeat to Toaster::heating`) before this remediation effort; Tasks 1-3 rewrote every chapter (ch05-ch10) to the conformant nested/dot-chain idiom (`allocate toastBread.applyHeat to heating;`, nested inside the owning definition, or an equivalent same-context qualified reference). Task 4 added `allocate-connector-end-accessibility`, a `GapRule` in `src/toaster/conformance.py`, as an always-on guard against regression back into the non-conformant idiom.

The algorithm has now been independently reviewed and hardened twice, each round verified against the OMG pilot as ground truth rather than merely re-derived. **Task 5 (DL-059 ADDENDUM)** found two bugs in Task 4's first cut: it did not recognize that canAccess/isFeaturedWithin treat a featuring type as accessible when it (transitively) specializes, or (for a Usage owner) is typed by, the declaring context (false positives on `part def BetterToaster :> Toaster { allocate doApply to heater; }` and on a plain `part toaster : Toaster { allocate doApply to heater; }`, both pilot-accepted); and it trusted ANY multi-segment (dot-chain) end as already accessible, when in fact only the segments AFTER the chain's first one are proven safe by successful loading — the first segment needs the same accessibility test as a bare single-segment end (false negatives on `Toaster.heater` and `Outer::box.t`-style ends, both pilot-rejected). **Task 6 (DL-059 ADDENDUM 2)** found two more bugs in Task 5's fix: `query.supertypes_transitively` (Task 5's fix for the first bug) builds its graph from NAMED elements only (`model.query(select=["name"])`), so it still returned nothing for an UNNAMED or redefining owner (e.g. `part redefines heater { ... }`, qualified name `P::Better::@0`) even when that owner clearly redefines or retypes an accessible declaring context — five more pilot-accepted constructs wrongly flagged; and a single-segment end resolving whole to a NESTED Definition (`allocate doApply to Toaster::Inner;` where `Toaster::Inner` is a `part def` nested inside `part def Toaster`) was double-flagged by both this rule and `allocate-between-definitions`, when the pilot gives exactly one error — the rule computed a declaring context for the end without first checking whether the end itself was already a Definition (a check that existed for a multi-segment chain root, but not for an ordinary single-segment end).

The rule now (as of Task 6): for the end's own resolved element (single-segment case), skips entirely if it is itself a Definition (leaving it to `allocate-between-definitions`, regardless of nesting depth); otherwise accepts a declaring context equal to the owner, a plain package, or (transitively) a supertype/type/subset/redefinition target of the owner, computed via `query.supertypes_transitively_raw` (a new ApiIndex-native BFS over the raw API-JSON `type`, `subsets`, `redefines` and `specializes` reference fields, added to `src/toaster/query.py`, which works for named and unnamed elements alike — confirmed to reproduce `supertypes_transitively`'s own results exactly on every named case, so it replaces that call unconditionally rather than as a hybrid fallback); flags a chain root that is itself a Definition (never an accessible Feature); and applies the declaring-context test to the first segment of every end, single- or multi-segment alike.

**Task 7 (DL-059 ADDENDUM 3)** found two more bugs, both pre-dating Task 6 (design gaps from Task 4's original design, not introduced by Tasks 5/6). **F-1:** a Definition in the MIDDLE of a multi-segment chain (not the first segment, which this rule's own chain-root check covered, and not the last segment, which `allocate-between-definitions` covered) was invisible to every rule — e.g. `allocate doApply to toaster.Inner.heater;` where `Inner` is a nested `part def` between `toaster` and `heater`; OpenSysML accepted it with zero findings, the pilot rejected it. Fixed by extending `allocate-between-definitions` (D-019) to check every segment of a chained end, not only the last; since that now also covers the chain-root case this rule's own chain-root Definition check duplicated, the chain-root check was removed from THIS rule as redundant, closing the double-flag risk that removal would otherwise have reopened. **F-2:** the declaring-context exemption for the ordinary top-level pattern compared `@type == "Package"` by exact match, missing `LibraryPackage` (a distinct `@type` for a `library package`) — both a direct qualified reference into a library package (`L::heat`) and a `private import`-then-bare-reference form were wrongly flagged even though the pilot accepts both. Fixed by matching `.endswith("Package")` instead, this file's own established convention for metaclass-family checks.

The rule's own remaining job, after Task 7, is now narrower and more precisely stated: not "is this end's target a Feature or a Definition" (D-019's job, on every segment) but "is the chain's first segment, GIVEN that it resolves to a Feature, actually accessible from the allocation's own context" — declaring-context equality, package/library-package membership, or specialization/typing via `supertypes_transitively_raw`.

**Status: GUARDED.** D-019 and D-020 ALSO already have their own guards (`allocate-between-definitions` and `part-typed-only-by-item-def`, both predating this whole effort) — an earlier version of this entry and of DL-059 wrongly said they "remain open tool holes with no guard"; corrected 2026-09-29 (DL-059 ADDENDUM). The tutorial's own model (`models/ch01-cumulative.sysml` through `ch10-cumulative.sysml`, no ch09 fixture) is confirmed clean under the now four-times-hardened rule pair (this rule plus its now-extended sibling `allocate-between-definitions`); a regression back into the non-conformant idiom is now caught, with the algorithm bugs fixed and re-validated against the pilot across ~50 targeted probe fixtures (Tasks 5, 6 and 7 combined). The underlying OpenSysML/sysml-toolkit acceptance-without-diagnostic gap itself remains open upstream — this entry documents the gap and its guard, not a fix to either tool. After four independent review rounds each finding and fixing real bugs, and Task 7 fixing the last two named ones, further open-ended hardening is deliberately NOT being pursued (DL-059 ADDENDUM 3's own stopping rationale): this is a well-validated best-effort scoping check for an always-on tutorial guard rule, not a claim of formal completeness.

**Workaround:** `allocate-connector-end-accessibility` (Task 4, hardened Task 5, hardened again Task 6, hardened again Task 7) together with the now-extended `allocate-between-definitions` (D-019), an always-on language-gap `GapRule` pair, each with its own negative control, following D-019/D-020's own shape.
**Resolution:** upstream fix in both OpenSysML and sysml-toolkit; re-test with `scripts/probes`.
**Upstream issue:** not yet filed (drafted upstream bug reports for both tools remain open follow-up work, `decisions/next-passes.md` item 23(c)).
**Toaster issue:** not filed

## D-033: OpenSysML's `eval()` does not simplify a product against a `DimensionOneUnit` factor, or fold an SI base-unit expansion back into its derived-unit symbol

Found while fixing a separate, real pilot warning (`efficiency`'s own bare-literal binding, no DEFERRED entry needed — that was a straightforward conformance fix, not a tool gap): once `attribute :>> efficiency = 0.7;` (`DimensionOneValue`, unbound to any measurement reference) is corrected to the conformant `attribute :>> efficiency = 0.7 [MeasurementReferences::one];`, `deliveredEnergy`'s own result — `power * duration * efficiency`, a `ISQ::PowerValue * ISQ::DurationValue * DimensionOneValue` product — prints as an unsimplified compound expression, `67200 [MeasurementReferences::one*SI::'kg⋅m²⋅s⁻²']`, instead of the clean, expected `67200 [SI::J]`. **This is a display-label defect only, not an arithmetic one**: confirmed directly, `model.eval(...) == 67200.0 [SI::J]` evaluates `True` on the fixed model (`model.eval("ToasterDemo::rated.deliveredEnergy(ToasterDemo::rated.power, 120.0 [SI::s])")`, ch07-cumulative.sysml) — the returned `Quantity`'s `scale_num` (1000.0) and SI base-unit factors (`gram`¹, `metre`², `second`⁻²) are byte-identical between the base (bare-literal) and fixed (bracketed) forms; only the `Unit.text` label differs, gaining a spurious `MeasurementReferences::one*` prefix. OpenSysML DOES normally resolve a `kg⋅m²⋅s⁻²` base-unit product to its own calc's declared return type's unit symbol (`deliveredEnergy`'s own `EnergyValue` return prints plain `SI::J` on the unfixed model, while an unlabeled raw `800.0 [SI::W] * 120.0 [SI::s]` prints the base-unit expansion, not `SI::J` — so the derived-unit naming already works when nothing else interferes); it is specifically the leftover `MeasurementReferences::one` identity factor from multiplying by a properly-bound `DimensionOneValue` that blocks that resolution. So the one missing simplification step is: drop an identity (`DimensionOneUnit`) factor from a product before naming the result's unit — not a general derived-unit-naming gap.

**Workaround:** none; the affected notebook (`chapters/ch07-execution/01-calc-energy.ipynb`, cells 14, 17 and 18) and `chapters/ch07-execution/index.md`'s "Expected result" state the physically meaningful unit ("J") in prose alongside the numeric value, with a note that OpenSysML's own printed output shows an unsimplified unit expression rather than that clean symbol.
**Resolution:** upstream fix in OpenSysML's `eval()`/`Quantity`/`Unit` display logic (dropping an identity `DimensionOneUnit` factor from a product before naming the result); re-test once available. No probe committed under `scripts/probes` yet — this file's own neighboring entries point there, but this finding was confirmed via ad hoc `model.eval()` calls during review, not yet reduced to a committed regression probe.
**Upstream issue:** not yet filed.
**Toaster issue:** not filed

## D-034: `filter` is a reserved word in the real SysML v2 grammar; OpenSysML alone accepts it as a bare feature name with no diagnostic

Found while re-deriving the Chapter 5 exercise (exercise-track re-derivation, DL-061/062): a `part filter : FilterBasket;` declaration (a bare, ordinary-looking feature name, not qualified or unusual in any way) loads with `model.ok == True` and zero diagnostics in OpenSysML v0.9.0. `filter` is a reserved token in the real SysML v2 grammar (used for view-filter conditions, `ViewUsage`/`ViewDefinition` filtering; confirmed directly against both the pilot's own ANTLR token table and sysml-toolkit's own `SysML.xtext` grammar file). **Corrected 2026-09-29 (independent review): this is a one-of-three-tools gap, not the two-of-three "tolerate" pattern first recorded here.** sysml-toolkit v0.9.1 correctly REJECTS bare `filter` too (`sysmlv2 check`: exit 1, two real parse errors — `expected ';' or '{', found 'filter'` at the declaration, `expected a name, found 'filter'` at the reference site) — only OpenSysML silently tolerates it. The real OMG pilot also rejects it (`ERROR:no viable alternative at input 'filter'`, exit 1). So sysml-toolkit and the pilot AGREE this is invalid; OpenSysML alone is the outlier.

Confirmed empirically: `part 'filter' : FilterBasket;` (escaping the reserved word with single quotes, SysML v2's own escaped-identifier syntax) is accepted cleanly by both the pilot and sysml-toolkit — so the underlying construct is fine; only the bare, unescaped identifier collides with the grammar. Escaping was tried and rejected as the fix for the exercise's own use (see Workaround): it works, but a downstream tool (`toaster.render.build_interconnection_intent`) renders the escaped identifier's literal quote characters into its own flow-endpoint strings (`"'filter'.waterIn"`), which would appear as a stray, unexplained artifact in a rendered diagram label — worse than simply not using the reserved word as an identifier in the first place.

**Workaround:** don't use `filter` as a bare feature, part, or definition name anywhere in this tutorial's own model content; the Chapter 5 exercise renamed its own `filter` part to `filterUnit` instead of escaping it. No language-gap `GapRule` guard has been built for this (unlike D-019/D-020/D-032, which have their own always-on `GapRule`s) — this is a narrower, purely lexical collision (a fixed, small set of reserved words) rather than a structural/semantic non-conformance pattern, so a full guard rule was judged disproportionate; a simple reserved-word check against the model's own declared names would be a lighter-weight alternative if this recurs.
**Resolution:** upstream fix in OpenSysML alone (diagnose a reserved-word-as-identifier collision at parse time, matching sysml-toolkit's and the pilot's own behavior); re-test once available.
**Upstream issue:** not yet filed.
**Toaster issue:** not filed

## D-035: sysml-toolkit reports an `assert satisfy`/`assert not satisfy` naming an undeclared requirement as a warning, not an error; OpenSysML and the pilot both reject it outright

Found while re-deriving the Chapter 9 exercise (exercise-track re-derivation, DL-062). Chapter 9's own negative control (`chapters/ch09-coverage-sufficiency/01-requirement-coverage.ipynb` cell `9bae63f2`, mirrored in the exercise) asserts that a `satisfy` claim naming a requirement the model never declares fails to load — confirmed correct against OpenSysML v0.9.0 (`bad.ok == False`) and the OMG pilot 0.62.0-SNAPSHOT (`hasErrors=true`, "Couldn't resolve reference to Feature", "Must reference a constraint", "Must reference a requirement"). sysml-toolkit v0.9.1, run against the identical fixture via `sysmlv2 check --lib ...`, instead reports `warning: unresolved reference 'missingReq'` and exits 0 — the same construct that two of three pinned tools treat as a hard load failure, the third tool treats as a non-fatal warning. This is the same three-way disagreement shape as D-032/D-033/D-034 (one pinned tool disagrees with the other two on a real construct's validity), but in the OPPOSITE direction from all three of those: there, OpenSysML alone was the outlier tolerating something the other two correctly rejected; here, sysml-toolkit alone is the outlier, MORE permissive than the other two, not less.

**Workaround:** this tutorial's own negative controls (Chapter 9's own, and the exercise's mirror) assert against OpenSysML's behavior only, matching the pattern real Chapter 9 notebook 01 already uses (`bad.ok == False`); a control written to also assert against sysml-toolkit's exit code alone would need to check the warning text, not the exit code, to catch this class of error, since exit 0 alone doesn't distinguish a clean load from this one.
**Resolution:** upstream fix in sysml-toolkit (report an unresolved reference in a `satisfy` claim's own `subsets` as an error, matching OpenSysML's and the pilot's own behavior); re-test once available.
**Upstream issue:** not yet filed.
**Toaster issue:** not filed
