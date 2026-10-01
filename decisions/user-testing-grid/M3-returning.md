LEARNER M3-returning — Returning Learner — Ch10

EXECUTION RESULTS:
- nb01 cell2: ok=True | model loaded from models/ch10-cumulative.sysml, no diagnostic
- nb01 cell4: neg_ok (bad.ok)=False | undeclared-feature allocate correctly fails to load
- nb01 cell13: output=coverage dict: heatGenerationReq covered=True (satisfied_by=['rated'], failed_by=['weak']); timely covered=False (satisfied_by=[], failed_by=['slow']); energyConservationReq covered=False (by design)
- nb01 cell18/33: output=deliveredEnergyBoundedBySupply tied to no requirement before remediation (False), tied after (True), via EnergyConservationReq::c subsetting
- nb01 cell29: output=all three assert-satisfy bindings FAIL identically ("no value for feature heatGenCheck.efficiency"), confirming the no-assert-satisfy design choice
- nb01 cell42/44: output=sysmlv2 verify --solve emits nothing for EnergyConservationReq without assert satisfy; emits "undecided" when assert satisfy is added back in a scratch file — negative control runs as described
- nb02 cell4: neg_ok=False | "asserted_inference requires at least one premise (Hawkins §3.1)"
- nb02 cell14: output=ledger of AS-C06 (undetermined), AS-C08 (supported), AI-C06 (undetermined), all disposition=pending, record_kind=worked_example
- nb03 cell4: neg_ok=False | "counterevidence is empty"
- nb03 cell24: output=AI-C10 validates with 0 errors, disposition=pending, record_kind=worked_example, engineering_conclusion=undetermined

All three notebooks executed end-to-end via `jupyter nbconvert --execute` from the chapter's own directory with zero cell errors.

NARRATIVE OBSERVATIONS:
1. "Chapter 10 builds the full traceability graph this chapter's coverage report only samples one join of" (Ch9 conclusion.md) — delivered: nb01 builds a real two-requirement graph plus a reverse "is this proof tied to any requirement" search, closing a real gap (deliveredEnergyBoundedBySupply) live in the notebook, not asserted in prose.
2. "its own need was identified retroactively, after Chapter 8's proof already existed" (AC-C10, verified in cell 36/48 output) — honestly disclosed rather than smoothed over; the premise count in AI-C10 (5 items: nb01's graph, AS-C06, AS-C08, AI-C06, AC-C10) matches what notebook 03 actually cites, no inflated count found.
3. My work contract described this chapter as retrofitted with "a judgment-record anchor mechanism and a corrected exemption-rule narration (a factual overclaim... fixed by independent review)." I could not find this anywhere in my checked-out worktree: `src/toaster/evidence.py`'s `ReviewRecord` has no `subject_ref`, `tag`, or "exemption" field at all, and `git merge-base --is-ancestor 7a3e135 HEAD` (the commit recording "DL-084: Hawkins judgment records anchored to the model") returns false — that work, and the related Task 9/10 "exemption overclaim" fixes, exist elsewhere in repo history but are not on this branch (`user-testing/browser-pass1`, HEAD=120c65d). I executed and checked internal consistency of the chapter as it actually exists here; I did not fabricate verification of a retrofit that isn't present.

STRUCTURAL CHECKS:
- Cell 0 one sentence: yes (nb01/02/03 each one long semicolon-joined sentence, consistent with this tutorial's established dense style)
- Cell 5 / seam addressed without naming it: yes — concretely pointable in nb01 cells 42/44: the same SysML text (`models/ch10-cumulative.sysml`, with and without an added `assert satisfy` line) is read by two different tools (`model.verify_satisfaction()` vs. `sysmlv2 verify --solve`), producing two different printed verdicts ("require condition evaluation failed" vs. "undecided, indeterminate over unbound features") — model text, tool, and rendered result are all three concretely distinguishable from what actually printed, with no "three worlds" language anywhere.
- Cell 6 one sentence: yes, each notebook's final cell is one sentence pointing to exercises/ch10/exercise.ipynb
- conclusion.md three paragraphs + exercise reference: yes (What we built / What this establishes / What comes next, plus Exercise section)

OVERALL: PASS (for the chapter as actually checked out on this branch) — all cells execute, outputs are internally consistent with index.md/conclusion.md's claims, and the one premise-count/exemption check the contract asked for checks out; but the contract's framing assumed a retrofit (anchor mechanism, exemption-rule fix) that is not present in this worktree, which I could not verify and am flagging rather than guessing at.

## Structured findings
- id: M3-returning-01
  severity: positive
  location: chapters/ch10-traceability-signoff/01-traceability-graph.ipynb cells 42/44
  quote: "Lines mentioning EnergyConservationReq/energyConservationReq: []" vs "companion-check-scratch/ch10_with_satisfy.sysml:291:9  c (ConstraintUsage, satisfies ToasterDemo::energyConservationReq): undecided (result is indeterminate over unbound features)"
  expected: The Tall seam (model text / tool / rendered result) should be addressable in behavior without naming it.
  actual: Confirmed concretely — the same underlying model text produces two different tool outputs depending on which tool (model.verify_satisfaction vs sysmlv2 verify --solve) and which variant of the text is used; all three elements are independently pointable from real printed output.

- id: M3-returning-02
  severity: confusing
  location: work contract (orchestrator-provided) vs. src/toaster/evidence.py on branch user-testing/browser-pass1 (HEAD 120c65d)
  quote: "a judgment-record anchor mechanism and a corrected exemption-rule narration (a factual overclaim was found and fixed by independent review)"
  expected: Chapter 10's AI-C10/AC-C10 records should show a subject_ref/anchor field and exemption narration I could check for the described overclaim-then-fix.
  actual: ReviewRecord (src/toaster/evidence.py) has no subject_ref, tag, or exemption-related field; `git merge-base --is-ancestor 7a3e135 HEAD` returns false, confirming DL-084 and the related Task 9/10 exemption-overclaim fix commits are not ancestors of this branch's HEAD. The described retrofit is not present on this branch, so I could not evaluate it.

- id: M3-returning-03
  severity: positive
  location: chapters/ch10-traceability-signoff/03-engineering-signoff.ipynb cell 18 (premises list)
  quote: "its own premises are literally the other two notebooks' findings" (index.md Method section)
  expected: AI-C10's premises list should correspond exactly to notebook 01's graph findings plus notebook 02's three records (and AC-C10).
  actual: Verified directly — 5 premises: (1) notebook 01's coverage/tie summary, (2) AS-C06, (3) AS-C08, (4) AI-C06, (5) AC-C10. Matches the claim; no inflated or missing premise found.

- id: M3-returning-04
  severity: cosmetic
  location: decisions/user-testing-grid/ (directory did not exist before this report) and docs/superpowers/specs/2026-10-01-large-scale-user-testing-design.md
  quote: "see docs/superpowers/specs/2026-10-01-large-scale-user-testing-design.md for the exact schema"
  expected: A findings-schema spec file to confirm the structured findings format against.
  actual: That file does not exist anywhere in this worktree (`find . -iname "*large-scale-user-testing*"` returns nothing). I used the schema given verbatim in the work contract instead.

- id: M3-returning-05
  severity: positive
  location: chapters/ch10-traceability-signoff/02-judgment-synthesis.ipynb cell 14; chapters/ch09-coverage-sufficiency/conclusion.md "What comes next"
  quote: "Chapter 10 builds the full traceability graph this chapter's coverage report only samples one join of, and asks what a real sign-off over that graph would actually require."
  expected: As a Returning Learner fresh off Ch9, I expect Ch10 to extend coverage into a full graph and address sign-off directly.
  actual: Delivered as promised — nb01 builds the graph, nb02 builds a ledger of three real records (not asserted about), nb03 explicitly states in prose why the synthesis record is not sign-off itself. No gap between Ch9's promise and Ch10's delivery.
