# Chapter 8 layer audit

Contract PASS2-011-C, 2026-09-27. Role: `.claude/agents/layer-auditor.md`. Model: claude-opus-5-5[1m] (effort high).
Branch `audit/ch08`, base commit `a84dceb`.

Subject: the elements Chapter 8 adds, meaning the diff between `models/ch07-cumulative.sysml` (93 lines) and `models/ch08-cumulative.sysml` (93 lines). Both are generated fixtures, and I did not edit either. **The diff has one line, and it is a comment:**

```
3c3
< // Source: notebook cell-02 TOASTER_INCREMENT in chapter 7's construct-introducing notebooks.
---
> // Source: notebook cell-02 TOASTER_INCREMENT in chapter 8's construct-introducing notebooks.
```

Chapter 8 therefore adds **no model element**. What it does add is on the analysis side of the loop:
- `verify_satisfaction()` verdicts;
- two judgment records, `AS-C08` and `AS-C08-REV`;
- a stale-record pattern built on `check_stale()`;
- a transient threshold edit;
- three negative controls.

This audit classifies those under DL-023 and DL-033: they are not layer elements, so each is classified by what it bears on and by its tier. The audit also checks whether the inherited patterns recur in the model the chapter checks, as the contract asks.

Method: the four-question pass and the per-layer checklist in `.claude/skills/architecture-layers/SKILL.md`; AGENTS.md §1.1, §1.4 to §1.9; z-principles F1 to F7 and P1 to P6; and the glossary (`uv run python -m glossary tutorial` for verification, simulation, behavior, emergence, TPM, traceability, judgment, assumption, counter-evidence, requirement, asserted solution, query, dynamical system, validation). I cite the ACE rulings by the **headers in `decisions/log.md`**. I applied them and did not re-argue them. See O-1 for a numbering mismatch between the log and two other files.

Evidence I collected by running things:
- **Element diff.** I loaded both fixtures with OpenSysML v0.9.0 (`load_from_content`, `strict=False`), and both give `ok == True`. I then diffed the API JSON export by qualified name with `toaster.query.ApiIndex`. Each model has 87 elements. Added: none. Removed: none. Type changed: none.
- **Metaclass counts in ch08.** `VerificationCaseDefinition` 0, `VerificationCaseUsage` 0, `AnalysisCaseDefinition` 0, `ConstraintDefinition` 0, `MetadataUsage` 0. `SatisfyRequirementUsage` 4, `RequirementDefinition` 2, `RequirementUsage` 2, `CalculationDefinition` 1, `StateUsage` 5, `TransitionUsage` 3.
- **Conformance CLI.** `uv run python scripts/check_conformance.py models/ch08-cumulative.sysml --stage 8,0` (exit 0; by design, only `failed` gives exit 1) reported:
  - Language: `ok=True`, no diagnostics.
  - Four gap findings: `allocate-between-definitions` twice, on `ToasterDemo::@19`, and `part-typed-only-by-item-def` on `BreadLoader::bread` and `BreadEjector::bread`.
  - Project checks: `port-type` and `satisfaction-claims-evaluated` are both `blocked`, with the reason "language conformance failed" and the unblock criterion "no language-tier violation, per the spec, is present".
  - The ch07 fixture at stage 7,0 gives the identical report.
- **`model.verify_satisfaction()` on ch08.** Four verdicts:
  - `timely by nominal` holds, "observed by run".
  - `timely by slow` fails, "witnessed by run": `toaster.cycleTime <= 180.0 [SI::s]` evaluated to false.
  - `heating by efficient` holds, "observed by run".
  - `heating by weak` fails, "witnessed by run": `heater.power >= 600.0 [SI::W]` evaluated to false.
- **Engines.** `conn.list_engines()` lists these engines, all ready (z3 found at `/opt/homebrew/bin/z3`):

  | Engine | Authority | Answers |
  |---|---|---|
  | `check` | bounded | outcomes, holds, sensitive |
  | `explore` | proved | outcomes |
  | `run` | observed | evaluate |
  | `smt` | proved | holds, sensitive |
  | `solve` | proved | satisfiable |
  | `sweep` | observed | sweep |

- **Engine probes.**
  - `verify_satisfaction(engine=...)` returns "does not answer evaluate questions — not covered" for each of `check`, `smt`, `explore` and `solve`. `engine="all"` returns the four `run` verdicts above.
  - `verify_constraint("ToasterDemo::TimelyToast", subject=..., engine="check")` returns "not covered" (the result DL-006 recorded). With `run` or `auto` it raises `WrongKindError`, because `TimelyToast` is a requirement def and not a constraint.
  - `engine="ir"` raises `InvalidRequestError`: "no engine named "ir"; the engines are check, explore, run, smt, solve, sweep, or auto, or all".
  - `verify_requirement("ToasterDemo::timely", subject=...)` returns "not covered by run" ("no value for feature toaster").
  - In a scratch model, three `constraint def`s with no subject were also classified as "evaluate questions" and declined by every formal engine.
  - `explore_state("ToasterDemo::Cycle", events=["Start","Finish"])` returns "finalState ready; visits idle, heating, ready (1 linearizations; no choice points); complete (1 runs)".
- **The registered check, run directly.** I ran `conformance.satisfaction_claims_evaluated(ch08)` by hand to see what it would find. This is not a verdict: the check is blocked on ch08 and unscheduled (`applies_from=None`). It finds two false claims: `evidence::@1` (`timely(slow)` is False) and `heatingEvidence::@1` (`heating(weak)` is False).
- **The notebooks.** I executed every code cell of the three Chapter 8 notebooks in order, from the chapter directory. All ran. The printed outputs match the chapter's stated expected results.
- **Construction check.** `uv run python scripts/check_construction.py --check` reports 2 failures, both the known ch03-to-ch04 predecessor-containment failure: `ToasterDemo::TimelyToastTest` and its `toaster` reference usage are missing from ch04. The script's construction map has no entry for chapters 6 or 8.
- **Hashes.** `hash_content(ch07 source) != hash_content(ch08 source)`, although the two differ only in a comment.
- **Glossary.** `uv run python -m glossary check` gives ok (0 errors, 7 warnings: the local source PDFs are absent). `uv run python -m glossary lint` has no hit under `chapters/ch08-checking`; the 8 hits are all elsewhere. There is no glossary term for "model checking", "evidence", "violation witness" or "verification case".

Evidence I read for intent:
- `chapters/ch08-checking/index.md`, `conclusion.md`, and every cell of notebooks 01, 02 and 03.
- Chapter 7 `index.md` and the markdown and demo cells of its three notebooks, read only to compare simulation with checking. I did not audit them.
- The skills `opensysml-api` (lines 80 to 119) and `sysml-v2-toaster-model` (lines 20 to 59), `src/toaster/conformance.py` (lines 330 to 459), `scripts/check_conformance.py`, `scripts/check_construction.py` (lines 1 to 170), and the tests in `tests/test_conformance.py` and `tests/test_query.py` that take the `ch08` fixture.
- `decisions/log.md`: DL-006, DL-007, DL-017 to DL-025, and DL-030 to DL-039.
- `decisions/pass4-backlog.md`.

## Classification table

Rows in *italics* are inherited elements that Chapter 8 exercises. They are shown so the recurrence check has a place to live. I did not audit them again: the ruling cited is the classification, and the status says whether the pattern recurs at the ch08 stage.

**A. Model elements Chapter 8 adds**

| Element (qualified name) | Layer | Reason | Status |
|---|---|---|---|
| (none) | None | The JSON export diff is empty: 87 = 87 elements, no additions, no removals, no type changes. The chapter says so itself (notebooks 01 to 03 cell 3: "identical to the Chapter 7 model ... not new SysML constructs"), and so does `sysml-v2-toaster-model` line 56. | FINDING F-1 (the fixture's provenance comment says otherwise) |
| Line 3 header comment, "chapter 8's construct-introducing notebooks" | Not a model element | A comment. Chapter 8 has no construct-introducing notebook and no `TOASTER_INCREMENT`, and `check_construction.py` has no chapter 8 entry. | FINDING F-1 |

**B. Analysis-side constructs Chapter 8 introduces (not layer elements: AGENTS.md §1.5, DL-023, DL-033, F4)**

| Construct | What it bears on, and its tier | Reason | Status |
|---|---|---|---|
| `model.verify_satisfaction()` (nb01 cell-05; nb02 cell-05) | Evaluates the four `assert satisfy` traceability claims (DL-033). This is the property of the staged project check "satisfaction claims evaluated" (DL-039 (4)), but here it runs ad hoc, outside the conformance registry. Engine `run`, authority "observed". | It is analysis, not a layer element (F4). It is point evaluation of fixed-valued usages, not model checking: every formal engine declines these as "evaluate questions". | FINDING F-2, F-4; OPEN-QUESTION OQ-1, OQ-3 |
| Verdict `satisfy timely by nominal` (holds) | A comparison of `Toaster::cycleTime`'s entered default (120 s) with 180 s | AGENTS.md §1.5, prescribed versus emergent ("a cycle time set as an attribute default and then 'verified' against its threshold is a prescription tested against a threshold"); DL-018. | FINDING F-3 |
| Verdict `satisfy timely by slow` (fails; the chapter's "violation witness") | A comparison of `slow`'s bound value (200 s) with 180 s | DL-018 and DL-032: `slow` is a failing-branch fixture that fails only because a number was typed in. DL-039 (4): a False positive assertion is a `failed` claim, not a lesson outcome. | FINDING F-3, F-4 |
| Verdict `satisfy heating by efficient` (holds) | A comparison of `Heater::power`'s default (800 W) with 600 W | A part value is a prescribed physical sizing choice (DL-021 on the 800 W), not an emergent result, so this is the legitimate form of check ("do the values meet the derived thresholds", physical checklist). Whether the 600 W threshold is derived was not checked (ch06 element). | PASS on the settable-result check; the threshold is unchecked |
| Verdict `satisfy heating by weak` (fails) | A comparison of `weak`'s bound part value (400 W) with 600 W | The failure concerns a design choice, which differs from `slow`. It still rests on a false positive `assert satisfy` (DL-039 (4)). | FINDING F-4; OPEN-QUESTION OQ-4 |
| ReviewRecord `AS-C08` (nb02 cell-05; `kind="asserted_solution"`, `engineering_conclusion="refuted"`) | A judgment record, not a layer element (DL-033). Its claim bears on an emergent result entered as a choice (`slow.cycleTime`). | `counterevidence` and `residual_uncertainties` are present and load-bearing, and the disposition is `pending`, not "accepted" (§1.6, SA-7: PASS). But the evidence it cites is the verdict of point-evaluating the entered value: the model's declaration read back (DL-034). | FINDING F-5 |
| ReviewRecord `AS-C08-REV` (nb03 cell-05; `engineering_conclusion="supported"`) | A judgment record, not a layer element. Its claim bears on `nominal.cycleTime`. | The rationale states the circularity itself: "The attribute is set at the part definition level with no override." A "supported" conclusion drawn from an entered result is what DL-034 rules out. | FINDING F-5 |
| `check_stale()` / `hash_content()` (nb03) | Record freshness, which is infrastructure. Not a layer element, not a conformance tier. | Freshness is keyed to the whole source text, not to `model_ref` (see O-2). | PASS (observation O-2) |
| `revised_source` (nb03: `toaster.cycleTime <= 180.0` edited to `<= 150.0`, loaded, not saved) | A transient edit of `TimelyToast`'s threshold. It is in no fixture. | It is used only to trigger staleness. The layer of the threshold stays open (DL-035). The edit changes a threshold with no derivation, which is harmless for a staleness demo. | PASS (note) |
| Negative control nb01 cell-04 and nb02 cell-04 (an undeclared attribute in a `require constraint` fails the load) | Language tier (name resolution) | This is a valid language-tier control. It is not a control for the chapter's own check. The nb02 comment ("produces no failure verdicts (empty list or error)") does not match its assertion (`not bad.ok`). | FINDING F-6 |
| Negative control nb03 cell-04 (an empty identifier fails `validate_record`) | Record validation (infrastructure) | A valid control for record validation, not for staleness. | FINDING F-6 |

**C. Inherited elements Chapter 8 exercises: the recurrence check at the ch08 stage**

| Element (qualified name) | Classification (ruling) | Recurs at ch08? | Status |
|---|---|---|---|
| *`ToasterDemo::Toaster::cycleTime` (`default = 120.0 [SI::s]`)* | *An emergent result entered as a choice (DL-018, DL-022)* | Yes, unchanged. Chapter 8 is where it is "verified", and two records conclude from it. | FINDING F-3 |
| *`ToasterDemo::slow` (`:>> cycleTime = 200.0 [SI::s]`)* | *A usage of the subject; a failing-branch fixture, not a candidate (DL-032)* | Yes. Chapter 8 calls it a "design candidate" (index Purpose, "do the design candidates formally satisfy"). | FINDING F-3 |
| *`ToasterDemo::nominal`* | *A usage of the subject that adds nothing, so it takes no layer (DL-032)* | Yes. Chapter 8 calls it "the nominal design" (conclusion). | FINDING F-3 |
| *`ToasterDemo::TimelyToast`, `ToasterDemo::timely`* | *Layer open until the MoE/MoP justification is recorded (DL-035)* | Unchanged. No label or justification has been added. | context |
| *`ToasterDemo::evidence::assert satisfy timely by slow`* | *A cross-layer traceability claim (DL-033). It is False (DL-039 (4)).* | Yes. The chapter's lesson is built on it. | FINDING F-4 |
| *`ToasterDemo::heatingEvidence::assert satisfy heating by weak`* | *The same kind of claim; also False* | Yes. The same pattern, with the Ch6 fixture. | FINDING F-4 |
| *`ToasterDemo::evidence`, `ToasterDemo::heatingEvidence` (part usages holding only claims)* | *A container defect (DL-033)* | Yes, both. `heatingEvidence` is the Ch6 instance of the same defect. | FINDING F-4 (recurrence noted) |
| *`ToasterDemo::Heater::power` (800 W), `ToasterDemo::weak` (400 W)* | *A physical part value (DL-021, "800 W is a physical sizing choice")* | The settable-result pattern **does not** recur here: a rated power is a choice. `Heater` still specializes no logical def (ch01 F-2, DL-021). | context; OPEN-QUESTION OQ-4 |
| *`ToasterDemo::TimelyToastTest` (ch03 `verification def`)* | *Analysis, not a layer element (DL-023)* | **Absent** from ch08. It was dropped from ch04 onward (backlog §8; `check_construction.py` reports the ch03-to-ch04 containment failure). The checking chapter runs on a model with no verification case. | FINDING F-2, F-7 |
| *`allocate ApplyHeat to HeatingSystem` (`@19`); `BreadLoader::bread`, `BreadEjector::bread`* | *Language non-conformant per the spec (DL-039 (1))* | Yes, all three. Both project checks are `blocked` on ch08. | context (ch05 F-1, F-3) |

## Per-layer checklist results

**Functional.** Chapter 8 adds no functional element. The only intent it touches, `TimelyToast`, has its layer open (DL-035). No MoE is added. The inherited `ApplyHeat` mix (DL-030) is not exercised in Chapter 8.

**Logical.**
- No mechanism, interface or derived MoP threshold is added.
- *Are there no results entered as choices?* In the model Chapter 8 checks, no: `cycleTime` is one (F-3).
- *Do the interfaces match?* The check is `blocked` on ch08 (DL-038, DL-039), not passed.

**Physical.**
- No concrete part def or value is added.
- *Is the TPM assessed and not asserted?* For `Heater::power` the value is a prescribed rating, so comparing it with a threshold is legitimate in form. No TPM (an assessed value) exists anywhere in the model, because nothing is derived.
- For `cycleTime` the "assessed" value is the entered one (F-3).

**Across layers.**
- *Stopping rule* (§1.8): not met. It is unchanged from ch07.
- *Emergent result set as a default and then "verified"*: **yes**. This is Chapter 8's main operation (F-3).
- *Judgment recorded with counterevidence and residual uncertainties, and no "accepted" disposition*: the fields are present and the dispositions are `pending`, so it passes in form. The evidence cited is circular (F-5).
- *Figures*: Chapter 8 shows none. No view of the assembled model appears in the chapter. That is recorded here and not raised as a separate finding, because the chapter adds no model element to show.

## Findings

**F-1. Chapter 8 adds no model element, and the fixture's provenance comment says it does.**
Element: `models/ch08-cumulative.sysml` line 3.
Check: AGENTS.md §1.7 (implicit parts' "provenance is never hidden") and §1.4 ("Every chapter is one turn of that loop").
What is wrong:
- The file says its source is "notebook cell-02 TOASTER_INCREMENT in chapter 8's construct-introducing notebooks". No Chapter 8 notebook defines `TOASTER_INCREMENT`. Every cell-02 only reads this file.
- `scripts/check_construction.py` has no chapter 8 entry (and no chapter 6 entry), so nothing generates or checks the ch08 fixture from notebooks. It is a copy of ch07 with the comment edited.
- The notebook file names promise constructs that do not exist: `01-invariant-def.ipynb` (titled "Satisfaction evaluation"; no invariant is defined) and `03-revision-flow.ipynb` (titled "Stale record detection").

What I did not do: I did not change the comment, the file names or the construction map. Whether a chapter may add nothing to the model is OQ-2.

**F-2. Chapter 8 has no formal model-checking construct. The distinction between model checking and simulation is drawn neither in the model nor in the prose, and the prose mislabels what is done.**
Check: AGENTS.md §1.1 item 5 ("Model checking and simulation are complementary: formal properties on one side; scenarios, trajectories and analysis of results on the other"), §1.9 ("probe before you assert"), P1, P5.
What is wrong:
- **In the model.** There is no `verification def`, no `verify`, no `constraint def`, no invariant, and no property stated over a state or parameter space. The ch03 verification def `TimelyToastTest` is absent from ch08 (context row above). Chapter 8 adds nothing (F-1).
- **In the analysis.**
  - `verify_satisfaction()` is answered only by the `run` engine, whose authority the tool reports as "observed". The verdicts say "observed by run" and "witnessed by run".
  - The engines with formal authority (`check`: bounded; `smt`, `explore`, `solve`: proved) are installed and ready, but they decline these questions as "evaluate questions — not covered". Every claim is about a usage whose values are fixed, so there is nothing to quantify over.
  - DL-006 (2025-09-25, before the Pass 1 alignment) replaced `verify_constraint(engine="check")` with `verify_satisfaction()` because the former returned "not covered". It read SA-6 ("bounded model checking: opensysml `check` engine only") as meaning in spirit "no external model checkers". That substitution is where model checking left the chapter.
  - My probe shows a further point: `verify_constraint` on `TimelyToast` is a wrong-kind call, because it is a requirement def.
- **In the prose.** The prose claims a formality the analysis does not have:
  - index Purpose: "do the design candidates formally satisfy the stated requirements";
  - notebooks 01 to 03 cell 3: "Chapter 8's bounded checks" (the engine used is not the bounded one);
  - conclusion: "The violation witness is formal engineering evidence";
  - nb02 cell-06: "a simulation-backed engineering judgment" (no simulation is run or cited).
- **Between chapters.** Chapter 7 nb03 cell 1 says "The matplotlib figure is the simulation evidence referenced by the judgment record in Chapter 8". No Chapter 8 record references it: `AS-C08`'s `evidence_refs` is the verdict string, and `AS-C08-REV` has none. The one link between simulation and checking that the prose promises is missing.
- So the §1.1 item 5 learning outcome is not delivered in Chapter 8, and Chapter 8 does not contrast its checking with Chapter 7's simulation.

What I did not do: I did not propose a formal property or an engine call, and I did not find the API form that poses a "holds" question to the formal engines (see *Not checked*).

**F-3. The settable-result pattern recurs, and Chapter 8 is the chapter that "verifies" it.**
Elements: `Toaster::cycleTime`, `nominal`, `slow`, and the two `timely` verdicts.
Check: AGENTS.md §1.5, prescribed versus emergent (the exact case it names); DL-018, DL-022, DL-032; F1; heuristic 5.
What is wrong:
- Chapter 8 compares an entered 120 s and an entered 200 s with 180 s, and presents the result as findings about designs:
  - conclusion: "the requirement boundary is real and correctly encoded: the nominal design (cycleTime=120) satisfies TimelyToast; the slow design (cycleTime=200) does not";
  - index: "design candidates".
- DL-018: such a check "can never fail for a reason about the design and verifies nothing". DL-032: neither usage is a candidate, and `slow` is a fixture.
- nb01 cell-07 goes further: its exercise invites the learner to add `fast : Toaster` with `cycleTime = 90.0` and "confirm" that it satisfies the requirement. That teaches the pattern as practice. It also disagrees with the exercise that `index.md` and `conclusion.md` describe (a `weak` witness and HeatingReq staleness).

What I did not do: I did not edit the text or the exercise prompt.

**F-4. The false-satisfy pattern recurs, twice, and the chapter's lesson depends on it.**
Elements: `evidence::assert satisfy timely by slow` and `heatingEvidence::assert satisfy heating by weak`. The `heatingEvidence` container is a second instance of the DL-033 container defect.
Check: DL-039 (4) ("a False claim is `failed` ... a deliberately failing branch is expressed as `assert not satisfy` or as a computed check, not as a false positive assertion"; "Re-derived models carry none"); DL-033 (a claim is not evidence).
What is wrong:
- The model asserts two satisfactions that are False. Chapter 8 does not report them as failed claims. It calls one a "violation witness" and turns it into a record with `engineering_conclusion="refuted"`. So the false assertion is treated as the intended content, when DL-039 says it is the fault the loop should catch.
- The registered project check for this property (`satisfaction-claims-evaluated`) is unscheduled (`applies_from=None`) and `blocked` on ch08 by the language-tier gap findings. Run directly, it flags exactly these two claims.
- So the chapter evaluates satisfaction claims by a route outside the conformance model, while the check that would report them as `failed` is not applied anywhere. Placement is OQ-3.

What I did not do: I did not rewrite either assertion, and I did not schedule the check.

**F-5. The two judgment records cite the model's own entered value as their evidence.**
Elements: `AS-C08` (nb02) and `AS-C08-REV` (nb03).
Check: DL-033 ("a record that cites the assertion as evidence cites nothing"), DL-034 (an entered result is not cured by a record; a check against it is not the candidate's assessed performance), F4, P1, AGENTS.md §1.6 (no passing check described as proof).
What is wrong:
- `AS-C08`'s evidence is the `run` verdict of `slow.cycleTime=200.0 <= 180.0`. Its rationale calls this "direct computational evidence".
- `AS-C08-REV` concludes "supported" for `nominal` and says in its rationale that the value is set on the definition.
- In both, the evidence is the model's declaration read back.
- The conclusion then calls the witness "formal engineering evidence ... not just a test result".
- What passes: `counterevidence` and `residual_uncertainties` are substantive (`AS-C08` even says `slow` "is a synthetic stress case, not a production design", which agrees with DL-032), and both dispositions are `pending`.

What I did not do: I did not edit the records. I did not check `AS-C03`, which `AS-C08` cites in `assumption_refs`.

**F-6. No negative control shows the chapter's own loop catching a fault about the design.**
Check: AGENTS.md §1.4 ("a negative control shows that the loop can detect a mismatch"); DL-032 (`slow` cannot validly play that role, because it fails only because a number was typed in).
What is wrong:
- nb01 and nb02 use the same language-tier control, an unresolved name in a constraint.
- nb03's control is record validation.
- None shows satisfaction evaluation or staleness detection catching a fault. The only failing case is `slow` (DL-032), plus `weak` (OQ-4).
- The nb02 cell-04 comment describes a different outcome ("no failure verdicts (empty list or error)") from the one it asserts (`not bad.ok`).

What I did not do: I did not add controls.

**F-7. The ch08 fixture, the repository's most-referenced "full" reference model, is language non-conformant per the spec, lacks the tutorial's only verification case, and three tests encode readings that the rulings reject.**
This is not a layer finding. The contract asked that anything about this fixture be treated as significant.
Check: DL-039 (1) (`model.ok` is a proxy, not the definition of language conformance), DL-038 (3) (an empty `port_type_mismatches` on a model with no port ends is vacuous and is not reported as a pass), DL-023.
What is wrong:
- **Who references it.** `models/ch08-cumulative.sysml` is referenced by two test files (`tests/test_query.py`, `tests/test_conformance.py`), by the default set in `scripts/check_conformance.py`, and by `scripts/probes/query_helpers_draft.py`. Each of ch01 to ch05 is referenced by one test file; ch06 and ch07 by none.
- **It is not "full".** It lacks `TimelyToastTest` and its `verify timely` (dropped since ch04), so no fixture from ch04 onward has a verification case.
- **Three tests.**
  - `tests/test_conformance.py::test_language_ok_on_valid_model(ch08)` names ch08 a "valid model". The same file's `test_language_gap_findings_on_real_fixture(ch08)` finds gap violations in it. Under DL-039 (1) it is non-conformant. The assertion itself (`["ok"] is True`) tests only the proxy.
  - `tests/test_query.py::test_port_type_check_is_clean_on_ch08` asserts that `port_type_mismatches(ch08) == []` and calls that "clean". ch08 has no `PortUsage`, so the result is vacuous (DL-038 (3), ch05 F-5 (e)).
  - `tests/test_conformance.py::test_satisfaction_claims_evaluated_skips_verify_without_subject(ch08)` is meant to exercise the `verify`-without-subject branch. ch08 has no `verify` relationship, so the branch is never reached and the assertion passes vacuously.

What I did not do: I did not edit tests or fixtures.

**F-8. The skills and the chapter documentation disagree with the tool and with each other.**
- `.claude/skills/opensysml-api/SKILL.md` lines 95 and 96 show `verify_constraint("ToasterDemo::TimelyToast", ..., engine="check")` and say `# engine values: "check", "ir"`. The tool has no `ir` engine; it lists check, explore, run, smt, solve, sweep, auto and all. `TimelyToast` is a requirement def, so `verify_constraint` on it raises `WrongKindError` under `run` and `auto` (`verify_requirement` is the matching call). The skill does not record the engines' authorities (observed, bounded, proved), and those are exactly what separates evaluation from model checking.
- `.claude/skills/sysml-v2-toaster-model/SKILL.md` lines 36 and 38 place satisfaction evaluation (A2) and stale-dependency detection (A4) in Chapter 9. Chapter 8 introduces both (DL-006: "the introduction point moves to Ch8"; DL-006 also says "SA-6 skill entry to be updated").
- The glossary has no term for *model checking*, although AGENTS.md §1.1 item 5 names it as a learning outcome.

Reported only. Skills and the glossary are outside my blast zone.

## Open questions (for the orchestrator to route)

**OQ-1. Does DL-006 still stand now that AGENTS.md §1.1 item 5 makes "model checking and simulation are complementary" a learning outcome?**
- **Reading A: DL-006 stands.** Chapter 8 is "constraint checking" by evaluation, and the formal side is taught elsewhere or not at all.
  - For: DL-006 is a recorded ruling; `verify_constraint(engine="check")` does return "not covered" on these claims; the model as built has nothing for a formal engine to quantify over.
  - Against: AGENTS.md §1.1 postdates DL-006. The chapter title and prose promise formality. I did not audit Chapters 9 and 10, so I cannot say the outcome is delivered elsewhere.
- **Reading B: DL-006 is superseded on this point.** The re-derived Chapter 8 states at least one formal property and checks it with an engine of bounded or proved authority, and contrasts that with Chapter 7's observed runs.
  - For: the engines are installed and ready (z3 found). The state machine `Cycle` already explores (`explore_state`: one linearization, complete). AGENTS.md §1.6 says stability "straddles both: an analytic form that can be model checked, plus simulated trajectories". Once cycle time is derived rather than entered (DL-018), a property over a parameter domain becomes checkable.
  - Against: I have not shown that a formal engine will answer a "holds" question in any form (see *Not checked*).
- **Recommended default:** Reading B. Escalate to Z, because it affects a learning outcome (P6) and the ruling it would supersede predates the alignment. Which property and which engine to use are not the auditor's call.

**OQ-2. May a chapter add nothing to the model?**
- **Reading A: yes.** §1.4 says each chapter is "one turn of that loop", and an analysis-only turn on the previous chapter's construction is still a turn. `sysml-v2-toaster-model` line 56 records Chapter 8 as "analysis operations, not new constructs".
- **Reading B: no.** The chapter's formal property is itself a construct (an invariant as a `constraint def`, or a `verification def` with an objective). The file name `01-invariant-def` suggests one was intended. Under §1.4 the construct half is what the analysis half checks.
- **Recommended default:** decide it together with OQ-1. If OQ-1 goes to Reading B, Reading B here follows.

**OQ-3. From which chapter does the "satisfaction claims evaluated" check apply?**
- **Reading A: from Chapter 8**, the chapter that teaches evaluation of satisfaction claims.
- **Reading B: from Chapter 3**, the chapter that first declares `assert satisfy`. This is by analogy with DL-023's trigger ("applied from the chapter that declares the connection complete"), and it would catch the false `slow` claim when it is written.
- Evidence: DL-038 parked the placement of staged checks; DL-039 (4) defines the check and names `slow` as its natural negative control; the registry has `applies_from=None`. On ch08 the check is `blocked` by the language gaps whichever reading is chosen.
- **Recommended default:** Reading B, routed to the parked placement decision. Chapter 8 would then teach the evaluation of claims that the check has already been screening since Chapter 3.

**OQ-4. Is `weak` a valid failing-branch fixture under DL-032, given that its failure comes from a chosen part value rather than an entered result?**
- **Reading A: valid in kind.** A rated power is a prescribed physical value (DL-021), so "400 W is below 600 W" is a fact about a design choice. That is the kind of failure DL-032 asks for. The defects around it are separate: it is expressed as a false positive `assert satisfy` (DL-039 (4)), and `Heater` realizes no logical def (ch01 F-2).
- **Reading B: not valid yet.**
  - The 600 W threshold is a free-standing number, not shown to be derived from a MoE, so failing it is failing a typed number.
  - `weak` is a usage of `Heater`, which realizes no logical slot, so it is not a candidate (DL-032's "candidate" test).
  - Note: `HeatingReq` and `weak` are Chapter 6 elements, and I did not audit Chapter 6.
- **Recommended default:** Reading A for the form of the failure. Keep F-4 for the assertion, and route the question of threshold derivation to a Chapter 6 audit.

## Other observations (not layer findings)

**O-1. The DL numbers in the backlog and in z-principles are shifted by one from the log headers for DL-032 to DL-037.**
- `decisions/log.md` headers: DL-032 is nominal/slow, DL-033 records and claims, DL-034 assumptions, DL-035 TimelyToast label, DL-036 Start/Finish, DL-037 BreadEjector naming, DL-038 the interface check.
- `decisions/pass4-backlog.md` cites DL-033 for `slow`, DL-034 for records, DL-035 for assumptions, DL-036 for the label, DL-037 for flow types and DL-038 for naming.
- `.claude/skills/ace-protocol/z-principles.md` "Confirmed extensions" cites DL-033 for usages of the subject, DL-034 for judgment records, DL-035 for assumptions and DL-038 for naming.
- This report cites the log headers. The Z-confirmed extension list points at the wrong entries, which matters for anyone following a citation. Route it to whoever owns those files.

**O-2. Staleness is keyed to the whole source text, not to the referenced element.** `hash_content` differs between ch07 and ch08, although the files differ only in a comment. A record written against ch07 therefore reads as stale on ch08 with no semantic change, and a change elsewhere in the file stales a record whose `model_ref` it does not touch. This is a design property of `toaster.evidence`, not a layer matter. I did not test it beyond the hash comparison.

## Contract premises that did not hold

1. **"Audit the elements Chapter 8 adds."** There are none (F-1). The table therefore classifies the analysis-side constructs Chapter 8 introduces and the inherited elements it exercises.
2. **"This is where model checking / bounded verification appears per the chapter title."** The chapter title is "Constraint Checking". No model-checking construct appears: there is no verification def, no `engine="check"` call, and no formal property. The verdicts come from the `run` engine, whose authority is "observed". The phrase "bounded checks" in cell 3 does not match the engine used (F-2).
3. **"A verification def running with engine="check" or similar, per the opensysml-api skill."** The skill's example is a wrong-kind call, and it names a non-existent `ir` engine (F-8). The only verification def the tutorial ever had is absent from ch08.
4. **"Whether Chapter 8 draws a real functional/model-checking distinction from Chapter 7's simulation."** It does not, in the model or in the prose. The one promised link, Chapter 7's figure cited by a Chapter 8 record, does not exist (F-2).
5. **"Whether the false-satisfy and settable-result patterns recur."**
   - False-satisfy: yes, for both `slow` and `weak` (F-4).
   - Settable result: yes, for `cycleTime` (F-3). No, for `Heater::power`, which is a part value (DL-021; OQ-4).
6. **"The model used throughout the existing test suite as the reference 'full' fixture."** Partly. It is the most-referenced fixture (two test files, plus the CLI default and a probe draft), but it is not full: it lacks the ch03 verification case, and it is language non-conformant per the spec (F-7).
7. **"Lint hits: none for ch08."** Holds.

## Constructs that could not be classified cleanly

- Nothing in the model: no element was added.
- The analysis-side constructs are not layer elements (DL-023, DL-033). I classified each by what it bears on and by its tier, which is the ruled method. `check_stale` and `hash_content` are record infrastructure, with neither a layer nor a conformance tier.
- `revised_source` is a transient model that is never saved. I classified it by the element it edits (`TimelyToast`'s threshold, whose layer is open under DL-035).

## Not checked, and why

- **Whether any API form makes a formal engine (`check`, `smt`, `explore`, `solve`) answer a "holds" question on this model or a small variant.** Every form I tried was classified as an "evaluate question" and declined: `verify_satisfaction`, `verify_constraint` with and without a subject, and three subject-less `constraint def`s. This leaves OQ-1 Reading B unproven, and I have not described any formal check as working (§1.9).
- **Chapters 9 and 10**, which might introduce model checking: outside this contract.
- **Chapter 6 elements** (`HeatingReq` and its 600 W threshold, `efficient`, `weak`, `heatingEvidence`, `HeatingAssembly`): not audited. They appear only as context and in OQ-4. I also did not check whether Chapter 6 notebooks define a `TOASTER_INCREMENT` that the construction map omits.
- **The Chapter 8 exercise** (`exercises/ch08/exercise.ipynb`): not read. F-3's exercise point rests on nb01 cell-07 and on `index.md` and `conclusion.md`.
- **Record `AS-C03`**, cited by `AS-C08`: not located or read.
- **Spec text on verification cases** (SysML v2 §7.24) and on the semantics of `assert satisfy`: not re-read, because the local PDFs are absent (`glossary check` warnings).
- **Rendered pages**: not built.
