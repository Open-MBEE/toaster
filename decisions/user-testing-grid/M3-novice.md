# LEARNER M3-novice — Novice — Ch2

## EXECUTION RESULTS

- nb01 (requirement def): model.ok=True | no diagnostics
- nb01 negative-control: neg_ok=False | diagnostic: "unresolved member: nonExistentAttr"
- nb01 demonstration: TimelyToast found; kind=requirementDef; query returns RequirementDefinition element
- nb02 (attribute override): model.ok=True | no diagnostics
- nb02 negative-control: neg_ok=False | diagnostic: "unresolved reference: nonExistent"
- nb02 demonstration: nominal and slow found; slow has 1 overridden attribute (cycleTime)
- nb03 (asserted context): model.ok=True | no diagnostics
- nb03 negative-control: neg_ok=False | diagnostic: "unresolved member: nonExistentAttr"
- nb03 demonstration: ReviewRecord created with kind=asserted_context, disposition=pending; validation errors=0

## NARRATIVE OBSERVATIONS

1. "This notebook introduces `requirement def`; after running it you can declare a formal requirement with a subject and a constraint expression." — Concept is clear and delivered accurately; the executed cells show both the text and the loaded model element, establishing the connection.

2. "attribute :>> redeclares the inherited `cycleTime` under `slow`. The `:>>` operator is a redefinition; it can only name an attribute that already exists in the type chain." — The explanation of `:>>` semantics is precise; negative control correctly catches the fault when a non-existent attribute is overridden.

3. "The `ch02-cumulative.sysml` file adds the first requirements construct: `requirement def TimelyToast`..." — The notebook markdown shows metadata tags (`ReviewRecordRef`) as part of the expected model content, but the actual loaded model file does not yet contain them; this creates a gap between what the prose says and what is actually in the file.

## STRUCTURAL CHECKS

- Concept-statement cells are one sentence: yes (all three notebooks: nb01, nb02, nb03 each have single-sentence concept statements ending with periods)
- Seam addressed in behavior without naming it: yes — each notebook shows SysML text being printed, loaded via opensysml.connect() and load_from_content(), and results queried back (RequirementDefinition found, attributes overridden, ReviewRecord validated). A reader sees three distinct things connecting: the source text, the tool loading it, and the rendered results. The seam is clear without ever naming "three worlds" or "Tall."
- Exercise-pointer cells are one sentence: yes (all three notebooks have single-sentence exercise pointers)
- conclusion.md has three paragraphs + exercise reference: yes (structure is "What we built" / "What this establishes" / "What comes next" plus exercise pointer)

## OVERALL

**NEEDS-FIX** — Notebooks execute cleanly and concept statements are clear, but notebook 03's documentation shows the cumulative model should include `ReviewRecordRef` metadata tags, while the actual loaded model (`ch02-cumulative.sysml`) does not yet contain them. This creates friction: a learner following the text would expect the model they load to match what the notebook shows, but it does not. The mismatch suggests either (a) the model file needs to be regenerated to include the new metadata mechanism mentioned in the contract, or (b) the notebook documentation is aspirational pending a later update. Either way, the gap between documented and actual content creates confusion for a Novice reader.

---

## Structured findings

- id: M3-novice-01
  severity: confusing
  location: notebook 03, cell-02 (markdown cell showing expected model content)
  quote: "The `ch02-cumulative.sysml` file adds the first requirements construct: `requirement def TimelyToast` constrains `cycleTime <= 180.0 [SI::s]` with a typed `subject` and `require constraint` body. `nominal` (`cycleTime` unset) and `slow` (`cycleTime` fixed at 200 s, a deliberately injected fault) are declared for later comparison. The `assert satisfy` pattern comes in Chapter 3; for now these usages exist without a recorded claim."
  expected: The model file loaded should contain the metadata definitions and tags shown in the printed output (ReviewRecordRef definition and ac001Tag metadata tag about nominal).
  actual: The actual ch02-cumulative.sysml file contains the requirement definition, nominal and slow usages, but does not yet include the ReviewRecordRef metadata definition or the ac001Tag metadata tag. The model loads successfully, but lacks elements the notebook documentation shows.

- id: M3-novice-02
  severity: positive
  location: notebook 01, cells showing model loading and querying
  quote: "model.ok = True; Model loaded successfully with no diagnostics" (from execution output)
  expected: Model should load without errors when containing a requirement definition with a subject and constraint.
  actual: Model loads successfully; model.ok is True; no diagnostics produced; TimelyToast is found and queried as a RequirementDefinition element.

- id: M3-novice-03
  severity: positive
  location: notebook 02, negative-control cell
  quote: "bad.ok = False; Expected error: unresolved reference: nonExistent"
  expected: The negative control should fail when attempting to override a non-existent attribute with `:>>`.
  actual: bad.ok is False as expected; the diagnostic correctly identifies "unresolved reference: nonExistent"; the negative control demonstrates the language's enforcement of referential integrity.

- id: M3-novice-04
  severity: positive
  location: notebook 03, ReviewRecord validation
  quote: "Record identifier: AC-001; Record kind: asserted_context; Record disposition: pending; Validation errors: 0"
  expected: ReviewRecord should be created with all required fields and pass validation against the model.
  actual: ReviewRecord created with identifier AC-001, kind=asserted_context, disposition=pending, record_kind=worked_example; validate_record returns zero errors; all required fields accepted.

- id: M3-novice-05
  severity: positive
  location: notebooks 01, 02, 03 concept-statement cells
  quote: "This notebook introduces `requirement def`; after running it you can declare a formal requirement with a subject and a constraint expression." (nb01); "This notebook introduces `attribute :>>` override; after running it you can override an inherited attribute value on a named usage." (nb02); "This notebook introduces the `asserted_context` judgment record; after running it you can declare and inspect the assumptions that frame an engineering requirement." (nb03)
  expected: Each concept-statement cell should be exactly one sentence stating what the notebook teaches.
  actual: All three concept-statement cells are single sentences (one terminal period each) and accurately state what each notebook teaches.

- id: M3-novice-06
  severity: positive
  location: notebooks 01, 02, 03 seam addressing (behavior without naming Tall/three worlds)
  quote: "TIMELY_TOAST_REQ printed; TOASTER_INCREMENT created; model.ok = True; req found: True; requirement kind: requirementDef" (and similar for nb02 and nb03)
  expected: The seam between SysML text, the tool loading it, and rendered results should be addressed in behavior without naming the three worlds or Tall lens.
  actual: Each notebook shows: (1) SysML/Python text printed/defined, (2) loaded via opensysml.connect() and load_from_content(), (3) results queried/validated back. The three stages are distinct and observable; a reader can point to each one without the text ever naming "Tall" or "three worlds."

- id: M3-novice-07
  severity: positive
  location: conclusion.md
  quote: "The Chapter 2 model adds `TimelyToast`, a requirement definition... No analysis in this chapter derives a cycle time, so neither usage's relationship to the bound is reported as a settled pass/fail verdict; the context record's estimate for `nominal` is likewise conditional on its stated assumption..."
  expected: conclusion.md should have three paragraphs (what was built / what this establishes / what comes next) plus an exercise pointer.
  actual: conclusion.md has three paragraph sections: "What we built", "What this establishes", "What comes next", followed by "Exercise:" pointer. Structure matches specification.
