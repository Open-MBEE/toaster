# Drafted gap issues

Status: **Drafts 1, 3, 4, 5, 6 and 7 filed 2026-09-27**, per Z's explicit instruction, after the re-verification below. Draft 2 stays internal-only (Z's ruling, 2026-09-26) and Draft 8 is retracted; neither was ever meant to be filed. **Draft 9 (D-023, added Pass 4 Phase 0) is new and held for Z's review — not filed. Draft 10 (D-026, added PASS4-004) is new and held for Z's review — not filed.** Each draft cites the exact source and asks only for what it supports. Tool versions: OpenSysML v0.9.0, sysml-toolkit v0.9.1. Probe evidence: `decisions/probes.md`; register: `DEFERRED.md` (D-014 to D-020, D-023 and D-026, each with its filed issue link where one exists).

| Draft | Filed as |
|---|---|
| 1 | [OpenSysML#643](https://github.com/Open-MBEE/OpenSysML/issues/643) |
| 3 | [OpenSysML#644](https://github.com/Open-MBEE/OpenSysML/issues/644) |
| 4 | [OpenSysML#645](https://github.com/Open-MBEE/OpenSysML/issues/645) (filed as a question, not a bug claim) |
| 5 | [sysml-toolkit#5](https://github.com/Open-MBEE/sysml-toolkit/issues/5) |
| 6 | [OpenSysML#646](https://github.com/Open-MBEE/OpenSysML/issues/646) |
| 7 | [OpenSysML#647](https://github.com/Open-MBEE/OpenSysML/issues/647), [sysml-toolkit#6](https://github.com/Open-MBEE/sysml-toolkit/issues/6) |

**Drafts 6 and 7 re-verified 2026-09-27** (Pass 2 wrap-up), per Z's request before Pass 3: both repros re-run against the current OpenSysML v0.9.0 and sysml-toolkit v0.9.1 binaries and reconfirmed exactly as drafted; both spec citations re-checked page-by-page directly against the PDFs in `sysmlv2-testing/sources/local/` (Draft 6's KerML citation is precise but the constraint is a structural attribute-typing fact, not a named OCL rule — corrected in the draft text; its SysML §7.15.2 citation, initially doubted, is confirmed correct); both checked against every open and closed issue on `Open-MBEE/OpenSysML` and `Open-MBEE/sysml-toolkit` — no duplicate found for either, but Draft 6 is closely adjacent to the open, unresolved `Open-MBEE/OpenSysML#95` ("Subsetting type conformance is not checked"), which the draft must now cite and distinguish from (see Draft 6, below) to avoid the same "not a bug" reply that issue already received for a related-but-different claim.

Resolved during Pass 1, no issue needed: **G2** (a bare `perform ToastBread;` naming an action *definition* is correctly rejected; SysML 7.17.6 has `perform` reference a usage) and **G3** (`allocation def` with typed ends and `allocation a : Def allocate x to y;` works; the earlier failure was our syntax). **G6** (broken `get_satisfy_relationships` and `find_allocations` in this repo) is fixed in `src/toaster/query.py` with tests.

---

## Draft 1 (OpenSysML): `model.query()` does not return unnamed connectors, `satisfy`, or metadata usages (G1, D-015)

**Version:** OpenSysML v0.9.0.

**Observed.** For a model that loads with `ok=True`: (a) a named `allocation`, `connection` or `flow` is returned by `model.query(where=@type=...)`; (b) the same element declared without a name is not; (c) `satisfy r by subject;` (which cannot take a name) is never returned as `SatisfyRequirementUsage`, and neither is a `MetadataUsage`. All of them are present in `json.loads(model.to_api_json().content)`. A named `perform action x : A` is returned with type `ActionUsage`, and the members a part inherits from its supertype are not listed for the subtype.

**Reference.** SysML API and Services v1.0 (formal/26-03-04), 7.2.2 ElementNavigationService (PDF p. 41, printed p. 27): `getElements(project, commit)` documented as "Get all the elements in a given project at the given commit"; and the Query API Model, Figure 7 (PDF p. 38, printed p. 24). Citations checked against the PDF on 2026-09-26.

**Request.** Please confirm whether `model.query()` is intended to correspond to the API's element queries over all elements of the commit. If so, unnamed connectors, `satisfy` usages and metadata usages should be selectable by `@type`. If it is intentionally limited to named elements, please say so in the documentation.

**Repro.** `scripts/probes/reprobe_opensysml.py` (test `named-flow-satisfy-perform` and the `G1` section).

**Workaround in place.** `src/toaster/query.py` (`ApiIndex`).

---

## Draft 2 (INTERNAL ONLY, not to be filed): no diagnostic when a connection joins ports whose types do not conform (G4, D-014)

> Z ruled 2026-09-26: this draft is an internal clarification for us and needs no upstream issue. Kept as the record of what the spec does and does not say. We never want a connection between unrelated ports in a model; the mismatched example is a deliberately faulty model used as a negative control.

**Version:** OpenSysML v0.9.0. sysml-toolkit v0.9.1 `check` and `lint` (default rules) also accept it.

**Observed.** `part def Outlet { port o : PowerPort; }`, `part def Torch { port fuelIn : FuelPort; }`, `connect outlet.o to torch.fuelIn;` loads with `ok=True` and no diagnostic. The same holds for an `interface def` with `PowerPort` ends bound to a `FuelPort`.

**What the spec says (as far as we found).** In KerML 1.1 Beta 2, `validateConnectorRelatedFeatures` requires only that a concrete connector have at least two related features; the `validateSubsetting*` constraints cover constant, uniqueness and featuring-type conformance; `validateRedefinitionEndConformance` covers `isEnd`. We did not find a validation constraint that requires the types of connected ends to be compatible. This was a search by constraint name, not a proof of absence. KerML 1.1 Beta 2 does describe compatibility as a matter of meaningfulness: for binding connectors, "to be meaningful, the declared co-domains of the related features ... must at least overlap" (KerML 1.1 Beta 2, 7.4.6 Connectors, PDF p. 73), and each connector end redefines an association end and subsets a related feature. That sentence is about binding connectors; applying the same idea to ports of unrelated types on an ordinary connection is our inference, not a statement in the spec. SysML v2.0 (formal/2026-03-02), 7.12.1 Ports Overview (PDF p. 93) does define conformance for connected ports: "Two ports are said to conform if each feature of one port has a matching feature on the other port. In this case, if the two ports are connected, it is possible to have a flow between every directed feature of one port and the matching feature on the other port." The spec therefore says what conforming ports are; we found no rule that a tool must reject a connection between ports that do not conform.

**Request.** Not a bug report. If the maintainers agree that mismatched end types are worth diagnosing, we would welcome an optional diagnostic (a warning or a lint rule), since this is a fault an executable specification is meant to surface early. Please tell us if a language-level rule already covers this and we have missed it.

**Workaround in place.** A staged project conformance check, `toaster.query.port_type_mismatches`, applied from the chapter that declares the connection complete.

**Before filing:** KerML 7.4.6 (Connectors) and SysML 7.12.1 (Ports) were re-read on 2026-09-26; SysML 7.13 and 7.14 (connections, interfaces) were not searched beyond `compatib`/`conform` in 7.12 to 7.14.

---

## Draft 3 (OpenSysML): `Editor` cannot author `perform action` (G5, D-016)

**Version:** OpenSysML v0.9.0.

**Observed.** `Editor.add_member()` has no kind for a perform action usage. `perform action heat : ToastBread;` inside an `abstract part def` is accepted when loaded as text.

**Reference.** SysML v2.0 (formal/2026-03-02) 7.17.6 Perform Action Usages.

**Request.** Add `perform action` to the authoring allowlist, consistent with the existing requests for `allocate` (#599), `flow`, and state usages.

**Re-verified 2026-09-27:** `editor.add_member(kind="perform action", ...)` does not raise immediately (the call only queues the operation) but `editor.apply()` does raise `IllegalMemberKindError: kind "perform action" is not legal`, confirmed against the current v0.9.0 Editor. Claim holds.

---

## Draft 4 (OpenSysML): `import` across separately loaded sources does not resolve (G7, D-017)

**Version:** OpenSysML v0.9.0.

**Observed.** With `base.sysml` = `package Base { part def Heater; part def Timer; }` and `chapter.sysml` = `package Chapter { private import Base::*; part def Toaster { part heater : Heater; part timer : Timer; } }`, loading the chapter alone (from text, or `conn.load(path)` from the same directory) fails with `unresolved reference`; concatenating both into one source loads `ok`. sysml-toolkit v0.9.1 resolves the same pair (`sysmlv2 check base.sysml chapter.sysml`).

**Reference to check before filing.** What the SysML/KerML package-import semantics and the API's project and commit model require of multi-resource resolution. We have not established that the spec requires this behavior for separately loaded models, so the request should be phrased as a question about intended behavior unless that reading is done.

**Request.** Document how a model spanning several files or commits is expected to be loaded, or support resolving imports across them.

---

## Draft 5 (sysml-toolkit, feature request): summary mode is not exposed in the CLI or Python (D-018)

**Version:** sysml-toolkit v0.9.1.

**Observed.** CHANGELOG v0.9.1 lists "summary mode for large tree graphs". It is `VizOptions::summary` in the `sysmlv2-viz` crate and the WebAssembly controls. `sysmlv2 viz` has no flag for it, and `Session.to_plantuml` takes no such argument.

**Request.** Expose the summary and member and note limits in the CLI and in `Session.to_plantuml`, or document that they are library and WebAssembly only.

---

## Draft 6 (OpenSysML, bug): an allocate between definitions is accepted (D-019)

**Version:** OpenSysML v0.9.0. sysml-toolkit v0.9.1 with the standard library rejects the same source.

**Observed.** `package P { action def A; part def H; allocate A to H; }` loads with `ok=True` and no diagnostic. With usages instead (`part def S { action a : A; part h : H; allocate a to h; }`) it loads in both tools. sysml-toolkit `check --lib <sysml.library>` on the definition form reports `ReferenceSubsetting::referencedFeature must refer to a Feature` at the allocate. OpenSysML rejects `perform A;` naming an action definition (correctly: a perform references a usage), so it already distinguishes definitions from usages there.

**Reference, re-verified 2026-09-27 directly against the PDFs (`sysmlv2-testing/sources/local/`), not carried over from the first pass.** KerML 1.1 Beta 2, 8.3.3.3.9 ReferenceSubsetting (PDF p. 203, confirmed): `referencedFeature : Feature {redefines subsettedFeature}` — the attribute's declared type is `Feature`. This section's own **Constraints** subsection reads "None": there is no named OCL `validateXXX` invariant for `referencedFeature`'s type, because none is needed — it is a structural (metamodel attribute-typing) requirement, not a business-rule constraint layered on top. A `part def`/`action def` is a `Definition`-kind element, not a `Feature`, so `allocate A to H` naming two definitions cannot satisfy this typing at all; this is a different and more fundamental thing than a type-*conformance* judgment. SysML v2.0 (formal/2026-03-02) 7.15.2 Allocation Definitions and Usages (PDF p. 112, section number confirmed correct, contrary to my initial doubt): its own worked example allocates only usages, both directly (`allocate logical.component to physical.assembly` inside the allocation def, both ends usages) and via the outer `allocation systemToDevice : ... allocate logical ::> system to physical ::> device;` — the spec's own canonical example never allocates two bare definitions.

**Directly relevant, found this pass: [OpenSysML#95](https://github.com/Open-MBEE/OpenSysML/issues/95) (open, unresolved) — "Subsetting type conformance is not checked."** Same family of relationship (`ReferenceSubsetting` is a kind of `Subsetting`), but a **different** claim: #95 is about general Subsetting's *type-conformance* (does the subsetting feature's declared type specialize the subsetted feature's?), which the maintainer investigated carefully and ruled **not a bug** — KerML 8.3.3.3.10 has no type-conformance constraint on plain Subsetting, only `validateSubsettingConstantConformance`, `validateSubsettingFeaturingTypes`, `validateSubsettingUniquenessConformance` and a multiplicity warning. This draft's claim is different in kind, not degree: it is not that `A` and `H`'s types fail to conform to each other (a Subsetting type-conformance question), it is that `A` and `H` are not `Feature`s **at all** (a `ReferenceSubsetting`-specific attribute-typing requirement, independent of the type-conformance debate #95 already settled). **Filing this without citing #95 risks the same "not a bug" reply for the wrong reason; filing it should explicitly distinguish the two.**

**No existing issue duplicates this** (checked OpenSysML open/closed issues and sysml-toolkit's single closed issue, 2026-09-27).

**Request.** Diagnose an allocate whose ends are not features, as sysml-toolkit does — citing #95 to distinguish this from that issue's already-settled question.

---

## Draft 7 (OpenSysML and sysml-toolkit, bug): a part usage typed only by an item definition is accepted (D-020)

**Versions:** OpenSysML v0.9.0; sysml-toolkit v0.9.1 (`check --lib`).

**Observed, re-confirmed 2026-09-27 against the current binaries.** `package P { item def Start; part def L { part bread : Start; } }` loads with `ok=True` and no diagnostics in OpenSysML v0.9.0; sysml-toolkit v0.9.1 exits 0 with no output on both `check --lib` and `lint --lib` (checked both commands this pass, not just `check`).

**Reference, re-verified 2026-09-27 directly against the PDF, page citation confirmed exact.** SysML v2.0 (formal/2026-03-02), section 8.3.11 Parts Abstract Syntax (the constraint sits in the PartUsage constraints block, PDF p. 323): `validatePartUsagePartDefinition` — "At least one of the itemDefinitions of a PartUsage must be a PartDefinition." (`partDefinition->notEmpty()`). Prose right above it on PDF p. 322 states the same rule in plain language: "A PartUsage is a usage of a PartDefinition to represent a system or a part of a system. At least one of the itemDefinitions of the PartUsage must be a PartDefinition."

**No existing issue duplicates this** (checked OpenSysML open/closed issues and sysml-toolkit's single closed issue, 2026-09-27; nothing on `PartDefinition`, item-definition typing, or this constraint name).

**Request.** Report a diagnostic for a part usage none of whose definitions is a part definition.

---

## Draft 9 (OpenSysML, likely bug): a transition's trigger is exported as an opaque string, never resolved against a declared type (D-023)

**Version:** OpenSysML v0.9.0.

**Observed.** For `state def Cycle { entry; state idle; state heating; transition first idle accept Start then heating; }` (`Start` an `item def` in scope): the model loads `ok=True`, and `model.to_api_json()` exports the transition as a `TransitionUsage` whose `sysx:trigger` is the bare string `"Start"` — not a reference to the `Start` item def, not an `AcceptActionUsage` element at all. A reference to an undefined name (`accept Nonexistent`), or a typo of a defined one, loads `ok=True` with no diagnostic either; the trigger then silently never fires at execution, and nothing in the export lets a downstream tool tell the two cases apart. sysml-toolkit v0.9.1 does resolve trigger names and warns on an unresolved one.

**Reference.** SysML v2.0 (formal/2026-03-02): `8.3.18.9 TransitionUsage` (PDF p. 373-374) declares `/triggerAction : AcceptActionUsage [0..*] {subsets ownedFeature}` and `deriveTransitionUsageTriggerAction` derives it from an owned `TransitionFeatureMembership` — a trigger is a full, structured `AcceptActionUsage` element, not a string. `8.3.18.8 TransitionFeatureMembership` (PDF p. 371-372), `validateTransitionFeatureMembershipTriggerAction`: "If the kind of a TransitionUsage is trigger, then its transitionFeature must be a kind of AcceptActionUsage." **`8.3.17.2` `AcceptActionUsage` (PDF p. 341-342; corrected 2026-09-27 — an earlier draft of this citation misidentified the section as 8.3.16, which is Flow Abstract Syntax; caught by an independent review of unrelated code that cited the same source)** gives that element a `payloadParameter : ReferenceUsage`, which is exactly where a payload/signal type would be resolved and checked. We could not find a single named constraint that says in so many words "an accept trigger's name must resolve to a declared type" — the case rests on the structural fact that the spec models a trigger as a resolvable, typed element throughout, and the export collapses all of that into an opaque string.

**Broader than the one example above (found 2026-09-27 building the tutorial's own guard for this gap):** OpenSysML resolves none of the forms the spec's grammar admits for an accept trigger — not a qualified name (`accept P::Start`), not a named payload (`accept s : Start`), not a time or change trigger (`accept after 5 [s]`, `accept when flag`) — and does not restrict the payload type to `item def` either (a `part def`, `port def`, attribute def or enum def can legitimately type one). The repro above is the simplest case, not the only one.

**Before filing:** we have not exhaustively searched every `AcceptActionUsage`/signal-reception constraint in KerML for a more direct textual rule; if the maintainers know of one, it would strengthen this from "the export loses structure the spec establishes" to "the export violates a named rule." Also check whether there's an existing internal issue about `AcceptActionUsage` export fidelity that this duplicates (a broad search on 2026-09-27 found none).

**Request.** Either (a) export a transition's trigger as a real reference to the `AcceptActionUsage`/payload type it names, so a downstream tool can tell a resolved trigger from an unresolved one, or (b) if `sysx:trigger` is deliberately a display-only string, add a diagnostic when it doesn't resolve to anything in scope — the way sysml-toolkit already does.

**Workaround in place:** a language-conformance guard is being added to the tutorial's own conformance tooling (`src/toaster/conformance.py`) that resolves each trigger string against in-scope item defs itself and flags a miss.

---

## Draft 10 (OpenSysML, likely bug): an implicit and an explicit-but-spec-identical `[0..*]` multiplicity are treated differently for an `in` parameter reachable through a nested action step (D-026)

**Version:** OpenSysML v0.9.0.

**Headline.** `in energy : ISQ::EnergyValue;` (no multiplicity written) and `in energy : ISQ::EnergyValue[0..*];` (the multiplicity SysML v2.0's own default already gives the first form — see Reference below) are spec-identical declarations. Both load (`model.ok == True`), but only the second keeps a model containing it evaluable: the first raises on evaluating an attribute that has no relation to it at all.

**Observed.** `part def Toaster { attribute cycleTime : ISQ::DurationValue; }`, with `attribute :>> cycleTime = 200.0 [SI::s];` on a usage (`slow`), where `Toaster` also (transitively, through an abstract supertype's `perform action toastBread : ToastBread;`) owns an action graph whose `ToastBread` step contains a nested action typed by a separate action definition with an unbound `in` parameter declared with no multiplicity (`action def ApplyHeat { in bread : Bread; in energy : ISQ::EnergyValue; in duration : ISQ::DurationValue; ... }`): `model.eval("...::slow.cycleTime")` raises `unbound parameter: action ApplyHeat: input parameter bread is bound by no argument`, even though `cycleTime` has no relation whatsoever to `ApplyHeat`, `bread`, `energy` or `duration`. Writing `in energy : ISQ::EnergyValue[0..*];` (nothing else changed) makes the identical expression evaluate normally.

**Isolating the precise trigger.** Eight variants were probed against the same minimal model (below), each substituted for `ApplyHeat`/its nested step, evaluating `slow.cycleTime`:

| Variant | Result |
|---|---|
| Only `out` parameters (`action def ApplyHeat { out toast : Toast; ... }`) | evaluates cleanly |
| `in bread`, no declared multiplicity, sequenced (`first start; then action applyHeat : ApplyHeat; then done;`) | fails |
| `in bread`, no declared multiplicity, bare ownership (`action applyHeat : ApplyHeat;`, no succession, no `perform`) | fails identically |
| `ref action applyHeat : ApplyHeat;` | fails |
| `abstract action def ApplyHeat { ... }` | fails |
| `action applyHeat : ApplyHeat[0..*];` (multiplicity on the usage) | fails |
| `in bread : Bread[0..1];` (explicit `[0..1]`, narrower than the spec default) | evaluates cleanly |
| `in energy : ISQ::EnergyValue[0..*];` (explicit `[0..*]`, the **same** value as the spec's own implicit default) | evaluates cleanly |

The last row is the headline finding: `[0..*]` written out is not a narrower or looser claim than the bare form — per the spec reading below it is the identical claim — and the tool still treats it differently. So the trigger is not "any owned action" (only-`out` is fine), not the `perform`/succession machinery (`ref action`, bare ownership, and `perform action` all fail the same way), not merely "any reference to a separate definition" (the only-`out` variant is such a reference too, and it is fine), and not really multiplicity in any semantic sense: the `[0..*]` row shows the tool does not key on what the multiplicity *means*, it keys on whether a multiplicity token is *present in the source text*.

**The clearest evidence, an internal inconsistency:** `ToastBread`'s own top-level `in bread : Bread;` has the identical shape — no declared multiplicity, unbound — and the tool tolerates it fine: `slow.cycleTime` evaluates cleanly when `ToastBread`'s body is `first start; then done;`, with no nested reference to a separate action definition at all. Only the *nested* case (one level deeper) triggers the failure, for the identical parameter shape.

A second, smaller inconsistency corroborates the first: `model.find("...::ApplyHeat::bread").kind` (and the same for `energy`, `duration`) reports `attributeUsage`, while the same feature's API-JSON export types it `ReferenceUsage`. Whichever is correct, the tool's two own surfaces for asking what kind of feature this is disagree with each other.

An explicit `[1..1]` fails identically to the undeclared case (confirmed: `in bread : Bread[1..1];`, otherwise unbound, raises the same "bound by no argument" error) — further evidence against a coherent multiplicity rule, since `[1..1]` is the one multiplicity that would spec-accurately state these parameters mean exactly one value, not yet known, and it does not help either. Only a multiplicity token being present at all (`[0..*]` or `[0..1]`) avoids the failure, regardless of what it states.

**Reference.** KerML 1.1 Beta 2 §9.2.8.2.6 (`FeatureReadEvaluation`): a feature read's result is scoped to "the values of `accessedFeature` of `onOccurrence`" — nothing here distinguishes a nested unbound feature from a top-level one, so the internal inconsistency above is not explained by this rule. SysML v2.0 formal/2026-03-02 §7.6.3 (implicit multiplicity defaults): its tighter `[1..1]` default applies only to "an attribute usage, an item usage, ..., or a port usage" — a usage declared with a kind keyword. `in bread : Bread;` (and `in energy`, `in duration`) have none: per the grammar they are `DefaultReferenceUsage : ReferenceUsage` (§8.2.2.6.3), and §7.6.4 defines a reference usage as exactly "a usage that is declared without any kind keyword." So they do not meet §7.6.3's condition for `[1..1]`; the spec's own default for them is the general, unbounded `[0..*]` (KerML 1.1 Beta 2 agrees, calling this "the usual default") — exactly the value we write explicitly to work around this gap. SysML v2.0 formal/2026-03-02 §8.3.17.14 / §8.4.13.11 (`PerformActionUsage`): its only additional constraints concern specialization and reference typing, nothing about parameter binding — consistent with the bare-ownership probe (no `perform` at all) failing identically to the `perform`-based one, and confirming `perform` itself adds nothing relevant to this behavior.

**Request.** Please confirm whether it is by design that OpenSysML v0.9.0 treats an implicit multiplicity and its spec-identical explicit spelling-out (`[0..*]` on a bare reference usage) differently for attribute evaluation, and if so, what governs the distinction — since it is not the multiplicity's declared meaning (the `[0..*]` row above rules that out), not the `perform`/succession machinery (the bare-ownership row rules that out), and not depth alone (the top-level `ToastBread::bread` case, identically shaped, is tolerated). If unintended: we would welcome either (a) honoring the implicit default the same as its explicit spelling, or (b) a documented lazy-evaluation fix so only the sub-graph a queried expression actually depends on needs full binding — so an unrelated attribute of a part usage stays queryable while a genuinely undecided child action (a functional-decomposition step whose flows are typed but deliberately not yet valued, because no mechanism has been chosen at this stage of a model's development) stays undecided.

**Repro.**
```
package Probe {
    private import ScalarValues::*;
    private import SI::*;
    private import ISQ::*;
    item def Bread;
    item def Toast;
    action def ApplyHeat {
        in bread : Bread;
        in energy : ISQ::EnergyValue;          // implicit [0..*]: fails
        // in energy : ISQ::EnergyValue[0..*];  // explicit, spec-identical: evaluates cleanly
        in duration : ISQ::DurationValue;
        out toast : Toast;
        out delivered : ISQ::EnergyValue;
        out loss : ISQ::EnergyValue;
        assert constraint balance {
            delivered >= 0.0 [SI::J] and loss >= 0.0 [SI::J] and delivered + loss <= energy
        }
    }
    action def ToastBread {
        in bread : Bread;
        out toast : Toast;
        action applyHeat : ApplyHeat;   // or: first start; then action applyHeat : ApplyHeat; then done;
    }
    abstract part def ToastingSystem {
        perform action toastBread : ToastBread;
    }
    part def Toaster :> ToastingSystem {
        attribute cycleTime : ISQ::DurationValue;
    }
    part slow : Toaster { attribute :>> cycleTime = 200.0 [SI::s]; }
}
```
`conn.load_from_content(src, strict=False).ok` is `True` either way; `model.eval("Probe::slow.cycleTime")` raises with `energy` as shown, and returns `200 [SI::s]` with the commented-out line swapped in instead. Removing `ApplyHeat`'s `in` parameters entirely (only `out` parameters left) also makes it evaluate cleanly; so does declaring `ToastBread`'s own body as `first start; then done;` with no nested `applyHeat` step at all.

**Before filing:** we have not exhaustively searched every evaluation-related KerML constraint beyond §9.2.8.2.6 for a rule that would explain the top-level-versus-nested asymmetry directly (as opposed to simply not ruling it out); if the maintainers know of one, it would sharpen this from "the export/execution loses a distinction the read semantics don't make" to "the execution violates a named rule." We also have not checked whether sysml-toolkit's execution engine (separate from OpenSysML) exhibits the same asymmetry, since evaluating a requirement/attribute is not currently part of our sysml-toolkit usage (`DEFERRED.md` D-024/D-025 cover what we do use it for).

**Workaround in place.** Writing the multiplicity explicitly as `[0..*]` — the applied fix in the toaster tutorial (`models/ch04-cumulative.sysml`), not a documented-and-rejected alternative: it states nothing the bare declaration did not already mean per §7.6.3/§7.6.4 above, so it changes nothing about the model's intended design (typed, valueless functional-input slots on an unallocated action, per this tutorial's own layer discipline — DL-030, DL-031), only whether the tool honors that meaning. `[0..1]` was considered and rejected: it also silences the tool, but narrows the multiplicity below the spec default and misstates these inputs as genuinely optional, which they are not.

---

## Draft 8: RETRACTED

**Retracted the same day, before filing.** OpenSysML's Python binding is genuinely evaluate-only (that observation stands), but sysml-toolkit v0.9.1's `verify --solve` already does what this draft was asking OpenSysML to add, via Z3. No upstream issue needed; DL-046 does not depend on OpenSysML gaining this capability. See `decisions/probes.md` and `DEFERRED.md` D-024.
