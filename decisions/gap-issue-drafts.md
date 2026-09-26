# Drafted gap issues (nothing filed)

Status: **drafts for Z's review.** Nothing here has been filed on any public repository. Each draft cites the exact source and asks only for what it supports. Tool versions: OpenSysML v0.9.0, sysml-toolkit v0.9.1. Probe evidence: `decisions/probes.md`; register: `DEFERRED.md` (D-014 to D-018). Z decides what is filed, where, and with what wording.

Resolved during Pass 1, no issue needed: **G2** (a bare `perform ToastBread;` naming an action *definition* is correctly rejected; SysML 7.17.6 has `perform` reference a usage) and **G3** (`allocation def` with typed ends and `allocation a : Def allocate x to y;` works; the earlier failure was our syntax). **G6** (broken `get_satisfy_relationships` and `find_allocations` in this repo) is fixed in `src/toaster/query.py` with tests.

---

## Draft 1 (OpenSysML): `model.query()` does not return unnamed connectors, `satisfy`, or metadata usages (G1, D-015)

**Version:** OpenSysML v0.9.0.

**Observed.** For a model that loads with `ok=True`: (a) a named `allocation`, `connection` or `flow` is returned by `model.query(where=@type=...)`; (b) the same element declared without a name is not; (c) `satisfy r by subject;` (which cannot take a name) is never returned as `SatisfyRequirementUsage`, and neither is a `MetadataUsage`. All of them are present in `json.loads(model.to_api_json().content)`. A named `perform action x : A` is returned with type `ActionUsage`, and the members a part inherits from its supertype are not listed for the subtype.

**Reference.** SysML API and Services v1.0 (formal/26-03-04), 7.2.2 ElementNavigationService: `getElements(project, commit)` "Get all the elements in a given project at the given commit", and the Query API Model (Figure 7, p. 24).

**Request.** Please confirm whether `model.query()` is intended to correspond to the API's element queries over all elements of the commit. If so, unnamed connectors, `satisfy` usages and metadata usages should be selectable by `@type`. If it is intentionally limited to named elements, please say so in the documentation.

**Repro.** `scripts/probes/reprobe_opensysml.py` (test `named-flow-satisfy-perform` and the `G1` section).

**Workaround in place.** `src/toaster/query.py` (`ApiIndex`).

---

## Draft 2 (OpenSysML, feature request): connecting ports of unrelated types is accepted without a diagnostic (G4, D-014)

**Version:** OpenSysML v0.9.0. sysml-toolkit v0.9.1 `check` and `lint` (default rules) also accept it.

**Observed.** `part def Outlet { port o : PowerPort; }`, `part def Torch { port fuelIn : FuelPort; }`, `connect outlet.o to torch.fuelIn;` loads with `ok=True` and no diagnostic. The same holds for an `interface def` with `PowerPort` ends bound to a `FuelPort`.

**What the spec says (as far as we found).** In KerML 1.1 Beta 2, `validateConnectorRelatedFeatures` requires only that a concrete connector have at least two related features; the `validateSubsetting*` constraints cover constant, uniqueness and featuring-type conformance; `validateRedefinitionEndConformance` covers `isEnd`. We did not find a validation constraint that requires the types of connected ends to be compatible. This was a search by constraint name, not a proof of absence.

**Request.** Not a bug report. If the maintainers agree that mismatched end types are worth diagnosing, we would welcome an optional diagnostic (a warning or a lint rule), since this is a fault an executable specification is meant to surface early. Please tell us if a language-level rule already covers this and we have missed it.

**Workaround in place.** A staged project conformance check, `toaster.query.port_type_mismatches`, applied from the chapter that declares the connection complete.

**Before filing:** re-read KerML connector semantics (8.4) and SysML 7.12 to 7.14 once more.

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
