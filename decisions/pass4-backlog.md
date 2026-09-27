# Pass 4 backlog: what the Ch1 to Ch5 audits found (2026-09-26)

Source: `decisions/audits/ch01-layer-audit.md` to `ch08-layer-audit.md` (independent auditors, Opus 5.5; tool and fact claims re-verified by Sonnet 5 spot reviews on Ch3, Ch5, Ch7, Ch8), the ACE rulings DL-018 to DL-023 and DL-030 to DL-049, and the vocabulary lint. Nothing has been edited: the current chapters and models are not a trusted baseline and are re-derived against the aligned harness in Pass 4. Each item says which ruling constrains the re-derivation. Ch9 and Ch10 are entirely stub notebooks (no model content, no cumulative fixture) and could not be layer-audited; see Coverage.

## 1. A result is entered as a choice, and the "verification" cannot fail (systematic, Ch1 to Ch8)

- `Toaster::cycleTime` is a settable default (120 s); `slow` binds 200 s; Ch2's threshold, Ch3's `assert satisfy` and the judgment records AC-001 and AS-C03 all compare that entered number with a limit (ch01 F-1, ch02 F-5, ch03 F-2). Rulings: DL-018, DL-022, DL-034. Re-derive: cycle time is derived from the mechanism and the energy balance and compared with intent; a setpoint, if any, lives on the policy carrier (`ControlSystem`).
- The model asserts `assert satisfy timely by slow` although `slow` (200 s) violates the 180 s limit; the same pattern appears with `weak` (400 W against 600 W) in Ch6 to Ch8. OpenSysML does not flag a false `assert satisfy`; `assert not satisfy` parses and can express a deliberate failing branch (ch03 F-3, confirmed by spot review). Rulings: DL-032 (`slow` is a fixture for the failing branch; not a candidate or an operating condition), DL-039 (a staged "satisfaction claims evaluated" check, with `slow` as the natural negative control).
- Assumptions: an assumption may enter as asserted context or a labelled estimate, never as the derived result (DL-034).

## 2. The functional layer mixes a mechanism and does not account for its flows (Ch3, Ch4)

- `ApplyHeat` takes `efficiency` as an input and assigns `energy := DeliveredEnergy(power, duration, efficiency)`, a deterministic conversion with a MoP parameter inside a functional action; the required functional relation, the balance inequality, is absent; efficiency is unbounded (`efficiency = 1.5` delivers 144 kJ from 96 kJ) (ch03 F-5, ch04 F-1, F-2). Ruling: DL-030. Re-derive: typed flows in and out (bread and energy in; toast, delivered energy and loss out), the balance inequality, efficiency bounded 0 to 1 and moved to the logical carrier.
- No decomposition and no parent function; `calculate` is not a verb-noun function (ch04 F-4). `Start`, `Finish`, `Cancel` are unconnected item defs whose names (events) contradict the chapter text (bread, toast) (ch04 F-3). Ruling: DL-036 (functional flow types; the model must state what each denotes).
- `duration` is an input slot copied from `DeliveredEnergy` (ch04 OQ-2). Ruling: DL-031 (functional input slot; never the quantity checked as time to toast).

## 3. The logical to physical chain is missing (Ch1, Ch2, Ch5)

- No `perform`, no abstract logical part def carrying a mechanism, `HeatingSystem` and `ControlSystem` are concrete groupings that specialize the whole's purpose type, `Heater` specializes nothing and is unused, `nominal` and `slow` contain no concrete part (ch01 F-2, F-3, ch02 F-6, ch05 F-2, F-4, F-6). Rulings: DL-020, DL-021, DL-032. Re-derive with the idiom in `architecture-layers` (`abstract part def` with `perform action`, concrete specialization, named `allocate` between usages).
- `BreadLoader`, `BreadEjector`, `BreadHandling` trace to no function, `BreadHandling` is not part of `Toaster`, and the flow is not an interface (no ports, unrelated item-typed ends, no payload) (ch05 F-4 to F-6). Ruling: DL-037 (name groupings by function, not by mechanism, until a selection is recorded), DL-038 and DL-039 for the interface check.

## 4. Measures: none are declared (Ch3)

- No MoE, MoP or TPM metadata or measure-tagged attribute exists in any fixture Ch1 to Ch8; "MoE" and "MoP" appear only in two notebook file names; no MoE/MoP justification is recorded (ch03 F-1). Ruling: DL-035 (no label is ruled now; the re-derivation records the justification, and the measured quantity must be derived; if a MoP, its threshold is derived from a stated MoE).

## 5. Judgment and evidence are mislabeled (Ch2, Ch3, Ch4)

- `part evidence` is a container with no part holding claims; records cite the model's own assertion as evidence; the verification case is not linked to the claims (ch02 F-7, ch03 F-4). Ruling: DL-033 (records and satisfaction claims are not layer elements; the container is a defect; reserve "evidence" for analysis results).
- Ch4's completeness record checks a weaker criterion than input/output accounting (ch04 F-2).

## 6. The system of interest and the purpose statement (Ch1, Ch2)

- The purpose is a `doc` on an abstract part def, and the subsystems specialize the whole's purpose type while the whole does not (ch01 F-3). Rulings: DL-019/DL-032 (the system of interest is the subject; the statement is functional; put the purpose in a functional construct the whole performs).

## 7. Tool and language-conformance gaps found by the audits (new)

- OpenSysML v0.9.0 accepts `allocate ApplyHeat to HeatingSystem;` between definitions; sysml-toolkit v0.9.1 with the library rejects it (`ReferenceSubsetting::referencedFeature must refer to a Feature`); an allocate between usages is accepted by both (ch05 F-1, confirmed).
- Both tools accept `part bread : Start` typed only by an item def, which violates SysML `validatePartUsagePartDefinition` (ch05 F-3, confirmed).
- OpenSysML does not flag a false `assert satisfy` (ch03 F-3, confirmed; a project check, not language conformance).
- Recording and guard: DL-039; DEFERRED D-019 to D-021; drafts 6 and 7 in `decisions/gap-issue-drafts.md` (not filed). The re-derived models must contain none of these constructs and the tutorial supplies a language-tier guard with negative controls.

## 8. Infrastructure and fixture defects (not layer questions)

- The Ch4 and Ch5 fixtures drop the Ch3 `TimelyToast` rationale doc and `TimelyToastTest`; `scripts/check_construction.py --check` passes because it does not check that each cumulative model contains its predecessor (ch04 F-5). Add a predecessor check.
- Ch4 notebook 03 fails with `NameError: ReviewRecord` (missing import; DL-014 fixed the same in Ch3 nb03) (ch04 F-6).
- Stale "not yet supported" comments cite toaster#10 and #11 although v0.9.0 parses both constructs (ch02 F-8). Spec section numbers in Ch5 notebooks (7.22, 7.23) disagree with the skill's (7.15.2, 7.12 to 7.14); which is right is unchecked (ch05 F-7).

## 9. Chapter text disagrees with the model (documentation)

- `index.md` says `Real` where the model uses ISQ types (Ch1, Ch3, Ch4); notebook and exercise counts and names disagree (Ch3 "three notebooks" vs four; the Ch4 exercise is `EjectToast`, `Brew` or `BrewUnit` depending on the file); `slow` is described four ways and a requirement def is said to bind "any instance" (Ch2); Ch5 says "functional-to-physical", "hardware component", "structural layer", and that `HeatingSystem` "realizes" `ApplyHeat` and that the SVG "confirms" the connectivity (against AGENTS.md 1.5, "Allocation is not realization", and 1.7, a diagram is not evidence).

## 10. Vocabulary and lens language

- Lint (8 hits): 6 "Tall seam" stub cells (Ch9, Ch10), "Concept Selection" (Ch5 index; the notebook file `01-concept-selection.ipynb` and its content, which teaches navigation not selection among alternatives, also need renaming), "physical architecture layer" (Ch1 index). About 64 seam cells in Ch1 to Ch8 use the world labels A-F and O-S; whether they count as naming the lens belongs to the recipe rewrite (DL-028).

## 11. Figures

- Ch2 and Ch4 show no view of the assembled model; Ch5's interconnection SVG is written to a temporary directory and never shown (AGENTS.md 1.7).

## 12. Chapter 6 findings (new)

- `Heater::power` is a chosen part rating (not DL-018's defect); `weak` (400 W) is a valid failing-branch fixture in kind, expressed wrongly as a false-positive `assert satisfy` instead of `assert not satisfy`. `HeatingReq`'s 600 W threshold is a free-standing number, underived from any MoE. Rulings: DL-040, DL-041, DL-049.
- `HeatingElement` is a mechanism-suggestive name for a not-yet-built logical grouping with no recorded selection among alternatives (extends DL-037). `PowerWire :> HeatingElement` is a real modeling error (a wire is not a kind of heating element). Ruling: DL-042.
- The recursion from `HeatingSystem` (logical, level 1) straight to `HeatingAssembly`/`ResistanceCoil`/`PowerWire` (physical, level 2) skips level-2 functional and logical content entirely (no sub-function, no interface, no mechanism) — incomplete recursion under AGENTS.md 1.8. Ruling: DL-043.
- `HeatingAssembly :> HeatingSystem` is the first concrete specialization of a logical component in the whole model (Ch1-Ch6), but nothing uses it: `Toaster::heating` still points at the abstract type, so there is still no candidate toaster. The requirement branch (`Heater`/`efficient`/`weak`) and the structure branch (`HeatingElement`/coil/wire) share no element.
- Ch4's `NameError: ReviewRecord` missing-import defect (DL-014's earlier fix) recurs in Ch6 notebook 3.

## 13. Chapter 7 findings (new)

- Adds one element: `state Cycle` (idle/heating/ready/cancelled, triggered by Start/Finish/Cancel). It is functional as declared (a mode-machine description, substitution-independent); the Finish transition's layer follows what Finish denotes (still undecided, DL-036); if a timer/thermostat issues Finish, that issuing rule is a policy on `ControlSystem`, kept separate from the mode machine itself. Ruling: DL-044.
- `Cycle` is not exhibited or owned by any part (nobody's modes) — the same missing-realization pattern as Ch1-Ch6, confirmed independently by spot review via two query surfaces.
- Two of four states (`ready`, `cancelled`) are dead ends; the machine does not cycle.
- State execution traces (`execute_state`) are not an emergent result of any kind — they are deterministic replay of a prescribed table, valid as specification analysis but not evidence about behavior. The chapter's "proves" language overclaims (AGENTS.md 1.6). Ruling: DL-045.
- **New tool gap, confirmed by spot review: OpenSysML v0.9.0 does not resolve state-machine transition trigger names at all.** A reference to an undefined item def loads `ok=True` and fires; a typo'd trigger loads `ok=True` and silently never fires; the API-JSON export keeps the trigger only as a string, not a resolved reference. sysml-toolkit v0.9.1 does resolve these names and warns on broken references. Nothing currently tracks this gap (no DEFERRED entry). The real Ch7 fixture is not itself broken — the gap is that nothing would catch it if it were.
- Notebook 01 defines the efficiency bound and formula meaning in Python, not the model (a repeat of the F4 concern); calls single-point agreement "proves". The sweep in notebook 03 rests on numbers (0.7 efficiency, 50 kJ threshold) that exist only in Python, none derived from a model relation or MoE.

## 14. Chapter 8 findings (new)

- **Adds zero model elements.** ch07-cumulative.sysml and ch08-cumulative.sysml are identical except the header comment (confirmed independently by spot review, both by text diff and JSON element-by-element diff). This is a valid form of the loop under SA-8 and AGENTS.md 1.4 (an analysis-only turn is a legitimate turn), ruled DL-047 — but the fixture's own provenance comment falsely claims a Chapter 8 increment exists, and no chapter-8 entry exists in `check_construction.py`'s `CONSTRUCTION_NOTEBOOKS`.
- **No formal model checking exists anywhere in the chapter, despite the title "Constraint Checking" and AGENTS.md 1.1 item 5 naming model checking and simulation as complementary.** Everything is `verify_satisfaction()`, Python claim evaluation on fixed usage values (the `run` engine, rated "observed"), confirmed by spot review to be exactly what both false-satisfy findings already flagged (`timely`/`slow`, `heating`/`weak`). Formal engines (`check`, `smt`, `explore`, `solve`, including z3) are installed and available but unused; every form tried was declined as "not covered" because nothing in the model has anything to quantify over. Chapter prose says "formally satisfy", "bounded checks", "formal engineering evidence" — none of which the analysis delivers (AGENTS.md 1.6, P1). **Resolved (DL-046): DL-006 is superseded.** sysml-toolkit v0.9.1's `verify --solve` (Z3) genuinely proves a constraint holds for all values of an unbound feature — OpenSysML alone cannot, but sysml-toolkit already covers it, confirmed by probe (`decisions/probes.md`), no Pilot Implementation needed. **Resolved for Pass 4:** `src/toaster/modelcheck.py` (`verify_holds`, `holds`) wraps the CLI call so a chapter notebook sees a plain Python function, per Z's ruling (DL-046) and DEFERRED D-025 (patch-and-document, intended for deletion once a published binding supports this natively). Tested against the real binary, 25 tests, independently reviewed twice. The prose defects ("formally satisfy", "proves", "bounded checks") are fixed regardless.
- `satisfaction-claims-evaluated` (DL-039) is currently unscheduled (`applies_from=None`). Ruled: it should apply from the chapter/section that first declares an `assert satisfy` — currently Chapter 3 — not parked like the port-type check, since its precondition (a satisfy claim to evaluate) already exists. Ruling: DL-048. **Builder follow-up:** set `applies_from` in `src/toaster/conformance.py`'s `REGISTRY` accordingly.
- Ch8 is the most-referenced fixture in the test suite (used throughout `tests/test_query.py`, `tests/test_conformance.py`) and is neither "full" nor valid SysML under the spec: it lacks any verification case and carries both language-tier gap findings (DL-039). Three existing tests pass on vacuous or misleadingly-named conditions, confirmed by spot review: `test_port_type_check_is_clean_on_ch08` (0 port usages, so the mismatch check is vacuously empty), `test_language_ok_on_valid_model` (checks only `model.ok`, not `gap_findings`, despite the fixture having 4), and the "skip verify without subject" test never reaches that branch (0 verify relationships in ch08) — its own later test admits this in a code comment.
- Two skill/tool disagreements: `opensysml-api` names a nonexistent `ir` engine and calls `verify_constraint` on a requirement def (wrong kind); `sysml-v2-toaster-model` places satisfaction evaluation and stale detection in Chapter 9, but Chapter 8 introduces both.

## 15. Process finding: a citation error, self-correcting via independent audits

DL-030 to DL-039's Q-letter to DL-number mapping was mistranscribed by the orchestrator when logging the original ACE batch (`decisions/log.md`'s own headers were always correct; the error was in `z-principles.md`'s "Confirmed extensions" section, this file, and `decisions/pass2-run-006.md`). All three Ch6-8 auditors independently noticed and flagged the mismatch before being told about it. Fixed in commit `6995a84`; the confirmed *content* of Z's approval was unaffected, only the numbers pointing to it. Lesson: cross-reference a batch ruling's citations against the log's own headers once, right after logging it, rather than trusting the transcription.

## Cross-chapter dependencies

`DeliveredEnergy` (Ch3) is used from Ch4 onward and must be re-derived with `ApplyHeat`; the false-satisfy pattern persists Ch3 to Ch8; `Start` and `Finish` are used as part types in Ch5 and as state-machine triggers in Ch8; the `slow`/`weak` fixtures and the `heatingEvidence` claims must be redone together.

## Coverage and next

Audited: Ch1 to Ch8 (elements each chapter adds; Ch8 adds none, confirmed). **Ch9 and Ch10 could not be audited**: both are entirely stub notebooks (`[TODO]` placeholders throughout index.md/conclusion.md; every notebook's model-loading cell is `source = """\n# stub — replace with full model\n"""`) with no cumulative fixture (`models/ch09-cumulative.sysml` and `ch10-cumulative.sysml` do not exist). Their layer audit is deferred until Pass 4 gives them real content; auditing a stub would produce nothing. Not audited: the exercises; figures beyond what the reports read; the rendered pages.

Every systematic pattern from the Ch1-5 audit (settable result, false satisfy, missing perform/realization) is confirmed present through Ch8. One new pattern appears at Ch7: OpenSysML's language-conformance surface has a further hole (state-machine trigger resolution) not covered by the existing gap guard.
