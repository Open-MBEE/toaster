# Pass 4 backlog: what the Ch1 to Ch5 audits found (2026-09-26)

Source: `decisions/audits/ch01-layer-audit.md` to `ch05-layer-audit.md` (independent auditors, Opus 5.5; the Ch3 and Ch5 tool and fact claims were re-verified by Sonnet 5 spot reviews), the ACE rulings DL-018 to DL-023 and DL-030 to DL-039, and the vocabulary lint. Nothing has been edited: the current chapters and models are not a trusted baseline and are re-derived against the aligned harness in Pass 4. Each item says which ruling constrains the re-derivation. Ch6 to Ch10 have not been audited (see Coverage).

## 1. A result is entered as a choice, and the "verification" cannot fail (systematic, Ch1 to Ch8)

- `Toaster::cycleTime` is a settable default (120 s); `slow` binds 200 s; Ch2's threshold, Ch3's `assert satisfy` and the judgment records AC-001 and AS-C03 all compare that entered number with a limit (ch01 F-1, ch02 F-5, ch03 F-2). Rulings: DL-018, DL-022, DL-035. Re-derive: cycle time is derived from the mechanism and the energy balance and compared with intent; a setpoint, if any, lives on the policy carrier (`ControlSystem`).
- The model asserts `assert satisfy timely by slow` although `slow` (200 s) violates the 180 s limit; the same pattern appears with `weak` (400 W against 600 W) in Ch6 to Ch8. OpenSysML does not flag a false `assert satisfy`; `assert not satisfy` parses and can express a deliberate failing branch (ch03 F-3, confirmed by spot review). Rulings: DL-033 (`slow` is a fixture for the failing branch; not a candidate or an operating condition), DL-039 (a staged "satisfaction claims evaluated" check, with `slow` as the natural negative control).
- Assumptions: an assumption may enter as asserted context or a labelled estimate, never as the derived result (DL-035).

## 2. The functional layer mixes a mechanism and does not account for its flows (Ch3, Ch4)

- `ApplyHeat` takes `efficiency` as an input and assigns `energy := DeliveredEnergy(power, duration, efficiency)`, a deterministic conversion with a MoP parameter inside a functional action; the required functional relation, the balance inequality, is absent; efficiency is unbounded (`efficiency = 1.5` delivers 144 kJ from 96 kJ) (ch03 F-5, ch04 F-1, F-2). Ruling: DL-030. Re-derive: typed flows in and out (bread and energy in; toast, delivered energy and loss out), the balance inequality, efficiency bounded 0 to 1 and moved to the logical carrier.
- No decomposition and no parent function; `calculate` is not a verb-noun function (ch04 F-4). `Start`, `Finish`, `Cancel` are unconnected item defs whose names (events) contradict the chapter text (bread, toast) (ch04 F-3). Ruling: DL-037 (functional flow types; the model must state what each denotes).
- `duration` is an input slot copied from `DeliveredEnergy` (ch04 OQ-2). Ruling: DL-031 (functional input slot; never the quantity checked as time to toast).

## 3. The logical to physical chain is missing (Ch1, Ch2, Ch5)

- No `perform`, no abstract logical part def carrying a mechanism, `HeatingSystem` and `ControlSystem` are concrete groupings that specialize the whole's purpose type, `Heater` specializes nothing and is unused, `nominal` and `slow` contain no concrete part (ch01 F-2, F-3, ch02 F-6, ch05 F-2, F-4, F-6). Rulings: DL-020, DL-021, DL-033. Re-derive with the idiom in `architecture-layers` (`abstract part def` with `perform action`, concrete specialization, named `allocate` between usages).
- `BreadLoader`, `BreadEjector`, `BreadHandling` trace to no function, `BreadHandling` is not part of `Toaster`, and the flow is not an interface (no ports, unrelated item-typed ends, no payload) (ch05 F-4 to F-6). Ruling: DL-038 (name groupings by function, not by mechanism, until a selection is recorded), DL-038 and DL-039 for the interface check.

## 4. Measures: none are declared (Ch3)

- No MoE, MoP or TPM metadata or measure-tagged attribute exists in any fixture Ch1 to Ch8; "MoE" and "MoP" appear only in two notebook file names; no MoE/MoP justification is recorded (ch03 F-1). Ruling: DL-036 (no label is ruled now; the re-derivation records the justification, and the measured quantity must be derived; if a MoP, its threshold is derived from a stated MoE).

## 5. Judgment and evidence are mislabeled (Ch2, Ch3, Ch4)

- `part evidence` is a container with no part holding claims; records cite the model's own assertion as evidence; the verification case is not linked to the claims (ch02 F-7, ch03 F-4). Ruling: DL-034 (records and satisfaction claims are not layer elements; the container is a defect; reserve "evidence" for analysis results).
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

## Cross-chapter dependencies

`DeliveredEnergy` (Ch3) is used from Ch4 onward and must be re-derived with `ApplyHeat`; the false-satisfy pattern persists Ch3 to Ch8; `Start` and `Finish` are used as part types in Ch5 and as state-machine triggers in Ch8; the `slow`/`weak` fixtures and the `heatingEvidence` claims must be redone together.

## Coverage and next

Audited: Ch1 to Ch5 (elements each chapter adds). Not audited: Ch6 to Ch10; the exercises; figures beyond what the reports read; the rendered pages. The Ch6 to Ch8 models repeat Ch3's patterns (confirmed for `weak`); a second audit wave should check the new elements (recursive decomposition, execution, checking) and Ch9 and Ch10 (coverage, sign-off).
