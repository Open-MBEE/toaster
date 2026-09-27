# Drafted gap issues (nothing filed)

Status: **drafts for Z's review.** Nothing here has been filed on any public repository. Each draft cites the exact source and asks only for what it supports. Tool versions: OpenSysML v0.9.0, sysml-toolkit v0.9.1. Probe evidence: `decisions/probes.md`; register: `DEFERRED.md` (D-014 to D-018). Z decides what is filed, where, and with what wording.

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

**Request.** Add `perform action` to the authoring allowlist, consistent with the existing requests for `allocate` (#599), `flow`, and state usages. **Before filing:** confirm against the current Editor that no `perform` path exists, and cross-link the sibling issues.

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

**Reference.** KerML 1.1 Beta 2, 8.3.3.3.9 ReferenceSubsetting (PDF p. 203): the referenced element of a ReferenceSubsetting, which identifies a connector's related features, is a Feature. SysML v2.0 (formal/2026-03-02) 7.15.2 allocates between usages in its examples.
**Not yet verified:** the exact validation-constraint wording in the formal 2026-03-02 release (the toolkit's message comes from the vendored 20250201 metamodel); re-check before filing. Check that no existing OpenSysML issue covers it.

**Request.** Diagnose an allocate whose ends are not features, as sysml-toolkit does.

---

## Draft 7 (OpenSysML and sysml-toolkit, bug): a part usage typed only by an item definition is accepted (D-020)

**Versions:** OpenSysML v0.9.0; sysml-toolkit v0.9.1 (`check --lib`).

**Observed.** `package P { item def Start; part def L { part bread : Start; } }` loads with `ok=True` in OpenSysML and exits 0 with no output in sysml-toolkit.

**Reference.** SysML v2.0 (formal/2026-03-02), `validatePartUsagePartDefinition` (PDF p. 323): "At least one of the itemDefinitions of a PartUsage must be a PartDefinition." (`partDefinition->notEmpty()`).

**Request.** Report a diagnostic for a part usage none of whose definitions is a part definition. Check for existing issues in both repositories first.

---

## Draft 8 (OpenSysML, feature request): no public method poses a "holds" question to the check/smt engines (D-024)

**Version:** OpenSysML v0.9.0.

**Observed.** `conn.list_engines()` declares `check` (bounded) and `smt` (proved) as answering question kinds `outcomes`, `holds` and `sensitive`, separate from `run`'s `evaluate`. But `verify_constraint(symbol_id, subject=None, engine="check")`, `verify_requirement(...)` and `validate_instance(...)` all pose an evaluate-style question regardless of the `engine=` argument: with a fully-determined subject they succeed via `run`-style evaluation; with an underdetermined one, `check`/`smt`/`explore`/`solve` each reply "<engine> does not answer evaluate questions — not covered", and no other method takes a holds/outcomes/satisfiable request.

**Reference.** The engine registration API itself (`list_engines()`/`EngineInfo.answers`) is the source for what each engine claims to answer; we found no corresponding entry point in `opensysml.model.Model` or `opensysml.connection.Connection` that constructs a holds-style request.

**Request.** Expose a way to ask the question `check` and `smt` say they answer — for example a `holds=True` argument on `verify_constraint`, or a dedicated `check_constraint`/`ask_holds` method — so a constraint over an underdetermined subject (the ordinary case for bounded model checking) can actually be posed to those engines.

**Repro:** `decisions/probes.md`, "2026-09-27 (DL-046 probe)".
