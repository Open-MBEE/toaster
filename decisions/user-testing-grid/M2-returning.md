# Grid cell M2-returning — GitHub Pages, Returning Learner persona, Chapter 10

Branch: `user-testing/browser-pass1`. Model actually run on: Sonnet 5 (matches the
persona table's Returning Learner assignment; no mismatch to flag). Modality: read the
locally-served MyST dev build at http://localhost:3000 entirely in the browser pane, per
M2's own definition (no terminal opened; execution results below are the book's own
already-rendered cell output, not re-run by me).

## Execution results

**Ch9 conclusion skim** (`/conclusion-8`): read only, as instructed, to recover Returning
Learner context. "What comes next" states Chapter 10 builds the full traceability graph
Ch9's coverage report only samples one join of.

**index-10** (`/index-10`): orients correctly — states purpose, the one new model element
and why, and explicitly disclaims performing sign-off itself.

**Ch10-01** (`/traceability-graph`): concept-statement one sentence (semicolon-joined,
single terminal period) — yes. Context cell ties to Ch9's coverage report and Douglas's
traceability idea — yes. model.ok=True (assert passed, "The model loads cleanly").
Negative control: `bad.ok=False` printed directly. Demonstration: traceability graph
printed matches concept-statement claims (heatGenerationReq bidirectional, timely
one-sided); `deliveredEnergyBoundedBySupply` found untied, then tied via subsetting;
AC-C10 built, `Validation errors: []`, model tag confirmed. Seam: addressed strongly in
behavior, never named — the same SysML text is loaded by the tool and checked two
different ways (`model.verify_satisfaction()` vs `sysmlv2 verify --solve`), producing
genuinely different printed verdicts (error vs "undecided" vs "satisfied") from the same
written construct; "Legality is not the question; whether it does the work the construct
is for is" makes the three-way distinction explicit without naming it. Exercise pointer:
one sentence, describes the task.

**Ch10-02** (`/judgment-synthesis`): concept-statement one sentence — yes. model.ok=True.
Negative control: `validate_record()` errors=['asserted_inference requires at least one
premise (Hawkins §3.1)'] — correct rejection. Demonstration: AS-C06/AS-C08/AI-C06 each
validate with `errors=[]`; ledger output matches claims. Exercise pointer: one sentence.

**Ch10-03** (`/engineering-signoff`): concept-statement one sentence — yes. model.ok=True.
Negative control: errors=['counterevidence is empty'] — correct. Demonstration: AI-C10
built, `Validation errors: []`, `Model tag: None`, disposition="pending",
engineering_conclusion="undetermined" — matches index.md's "Expected result" exactly.

**Chapter 10 Conclusion** (`/conclusion-9`): three paragraphs (What we built / What this
establishes / What comes next) plus exercise reference — yes. Reads as a genuine capstone:
"What comes next" states plainly this is the tutorial's last chapter and what continues is
the reader's own accountable engineering, not another chapter.

## Structured findings

- id: M2-returning-01
  severity: positive
  location: http://localhost:3000/engineering-signoff
  quote: "AI-C10 carries no subject_ref and gets no ReviewRecordRef tag: the exemption validate_record() grants is this tutorial's own rule for the pure cross-record synthesis case -- an asserted_inference whose own premises are non-empty may leave subject_ref unset"
  expected: given the retrofit mentioned in my contract, I expected to find a residual contradiction between the stated validate_record() rule and its application to AI-C10.
  actual: the rule as stated earlier on the same page ("subject_ref present ... for asserted_context/asserted_solution or an asserted_inference with no premises") and its application to AI-C10 (non-empty premises → exempt) are logically consistent, and the printed `Model tag: None` / `Validation errors: []` confirm the exemption is actually exercised, not just claimed.

- id: M2-returning-02
  severity: positive
  location: http://localhost:3000/traceability-graph
  quote: "Model tag: {'tag': 'ToasterDemo::acC10Tag', 'identifier': 'AC-C10', 'annotated_element': 'ToasterDemo::EnergyConservationReq'}"
  expected: the new judgment-record-anchor mechanism to be shown actually working, not just described.
  actual: AC-C10 is tagged in the model via a `metadata ... : ReviewRecordRef` construct, and `get_review_record_refs()` returns a real tag that `validate_record()` confirms agrees with the Python record, with zero errors.

- id: M2-returning-03
  severity: positive
  location: http://localhost:3000/conclusion-8 and http://localhost:3000/index-10
  quote: "Chapter 10 builds the full traceability graph this chapter's coverage report only samples one join of, and asks what a real sign-off over that graph would actually require."
  expected: Chapter 10 to deliver on what Chapter 9's own conclusion promised.
  actual: index-10's purpose statement matches this almost in the same terms, including the explicit disclaimer that it does not itself perform sign-off — strong continuity for a returning learner.

- id: M2-returning-04
  severity: cosmetic
  location: http://localhost:3000/ (sidebar drawer, desktop viewport)
  quote: "(visual only — a duplicated, smaller-scale copy of the page overlapping the main zoomed content after several sidebar expand/scroll actions)"
  expected: a single, stable-scale sidebar overlay.
  actual: on one occasion the pane showed what looked like two overlapping layouts at different scales; this cleared after a hard navigate plus `resize_window` to the desktop preset and did not recur, so I cannot rule out this being an artifact of my own browser-automation tooling (viewport emulation) rather than a real rendering bug in the book itself — flagging for the ACE to weigh, not asserting it as a confirmed defect.

- id: M2-returning-05
  severity: friction
  location: http://localhost:3000/traceability-graph
  quote: "This notebook introduces a real traceability graph over two of the model's three named requirement usages (...); after running it you can tell, for each of the two, what functional intent it expresses, what allocation and realization carry it forward, and what verification evidence, if any, actually exists, and you will have found one of this tutorial's own strongest pieces of formal evidence tied to no requirement at all, then closed that gap directly."
  expected: a concept-statement that orients quickly, per the skill's usual expectation.
  actual: technically one sentence (single terminal period, semicolon-joined clauses, passes the skill's literal rule) but chains four distinct claims; defensible as deliberate capstone density, but borderline enough to flag.

## Overall

PASS — Chapter 10 is internally consistent (the retrofitted exemption-rule narration and
the judgment-record anchor both hold up under scrutiny), correctly builds on Chapter 9,
and reads as a genuine capstone rather than "one more chapter."
