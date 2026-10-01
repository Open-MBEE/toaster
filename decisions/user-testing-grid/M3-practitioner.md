LEARNER M3-practitioner — SE Practitioner — Ch6

EXECUTION RESULTS:
- nb01 cell2(load)/cell12(TOASTER_INCREMENT+assert): model.ok=True, no diagnostics
- nb01 cell14: neg_ok=False | diagnostic: "unresolved reference: HeatingAssembly::undefinedSlot"
- nb01 cell16: output=`find_allocations` shows `HeatingAssembly::heatGenAllocation` with source ends `['HeatingSystem::applyHeat','ApplyHeat::generateHeat']`, target `['HeatingAssembly::heatGen']`; `perform_relationships` shows `HeatGenerator`→`GenerateHeat` — matches index.md's promised result exactly
- nb02 cell4(load): model.ok=True
- nb02 cell40: neg_ok=False | diagnostic: "unresolved reference: UndefinedCarrier"
- nb02 cell42: output=`rated.power=800W, heatGenerationReq(rated)=True`; `weak.power=400W, heatGenerationReq(weak)=False`
- nb02 cell16/cell30: `validate_record` → `[]` for AC-C06 and AS-C06
- nb03 cell2(load): model.ok=True
- nb03 cell4: neg_ok — AI-BAD (empty premises) correctly fails: `['asserted_inference requires at least one premise (Hawkins §3.1)']`
- nb03 cell18: `validate_record`→`[]` for AI-C06; Premises=['AC-C06','AS-C06','AS-C03','AI-C04']

All nine negative/positive checks in index.md's "Expected result" paragraph verified against real output.

NARRATIVE OBSERVATIONS:
1. "a resistive element responds to being switched on and off directly...while a combustion source needs separate ignition and fuel-metering machinery" — real engineering reasoning, explicitly flagged as a domain premise not derived from the model, with counterevidence ("does not rule out a combustion design... Joule heating's own relation... is still not modeled") honestly bounding the claim. Not hand-waved.
2. "energyIn has no producer wired to it... HeatingAssembly is not yet composed into any Toaster candidate... The 600 W threshold is not derived from any stated measure of effectiveness" — AI-C06 is candid about exactly what the stopping rule does and does not show; no overclaiming.
3. "model_ref=selection_model_ref" (= `"ToasterDemo::ResistanceCoil"`) — the anchor string is never resolved against the loaded model anywhere in the three notebooks, and `validate_record()` does not check it either; a stale or mistyped anchor would pass silently.

STRUCTURAL CHECKS:
- Cell 0 one sentence: yes (each is grammatically one semicolon-joined sentence, though dense)
- Cell 5/seam addressed without naming it: yes — each notebook's closing markdown cell ("the query results confirm...", "the evaluated results confirm...", "the evaluated results above, not the model's own declaration, are what this stopping judgment cites") points at printed SysML text, the load/validate step, and the query/eval output as three distinct, connected things a reader just watched happen.
- Cell 6 one sentence: yes
- conclusion.md three paragraphs + exercise reference: yes

NOTE ON CONTRACT PREMISE: the contract describes "a new subject_ref/ReviewRecordRef judgment-record anchor mechanism...retrofitted in the last 24 hours." No such type exists anywhere in the repo (`grep -r "ReviewRecordRef\|subject_ref"` returns nothing). What exists is `ReviewRecord.model_ref`, a plain string field present since the init commit (`git log -S model_ref` → `b095107`), used across AC-C06/AS-C06/AI-C06 plus the AI-BAD negative control. I report what I found rather than confirming the contract's framing, which does not match this worktree.

OVERALL: PASS — all cells execute as claimed, negative controls fire correctly, and the judgment records are honestly scoped; the one real gap is that the model_ref anchor is unvalidated.

## Structured findings
- id: M3-practitioner-01
  severity: positive
  location: chapters/ch06-recursive-decomp/02-second-level.ipynb cell 20/24/28 (AS-C06 claim/premises/counterevidence)
  quote: "a resistive element responds to being switched on and off directly...while a combustion source needs separate ignition and fuel-metering machinery to do the same"
  expected: a mechanism selection argued from a stated, checkable premise with honest limits
  actual: argued from an explicit domain premise, confirmed model fact (ControlSystem::durationOut), and counterevidence that concedes it does not rule out combustion and that Joule heating is not yet modeled — real engineering judgment, not hand-waved

- id: M3-practitioner-02
  severity: positive
  location: chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb cell 16 (counterevidence)
  quote: "energyIn has no producer wired to it... The 600 W threshold is not derived from any stated measure of effectiveness"
  expected: AI-C06 to state plainly what the stopping judgment does not establish, per AGENTS.md 1.6
  actual: four concrete, specific gaps listed (unwired energyIn, uncomposed HeatingAssembly, underived threshold, undecomposed sibling flows) — matches the honesty bar

- id: M3-practitioner-03
  severity: confusing
  location: src/toaster/evidence.py ReviewRecord.model_ref; chapters/ch06-recursive-decomp/02-second-level.ipynb cells 16/30, 03-stopping-judgment.ipynb cell 18
  quote: "framing_model_ref = \"ToasterDemo::heatGenerationReq\"" (and the parallel selection_model_ref, model_ref assignments)
  expected: a judgment-record "anchor" mechanism that is actually checked against the model (e.g. model.find(model_ref) resolving, or validate_record() flagging an unresolved one)
  actual: model_ref is a free-text string; no cell in any of the three notebooks resolves it against the loaded model, and validate_record() does not check it at all — a stale or mistyped anchor passes silently

- id: M3-practitioner-04
  severity: confusing
  location: work contract M3-PRACTITIONER (orchestrator-supplied), vs. src/toaster/evidence.py and repo-wide grep
  quote: "a new subject_ref/ReviewRecordRef judgment-record anchor mechanism...across three real records plus a fixed negative control"
  expected: the described subject_ref/ReviewRecordRef mechanism to be present and reviewable in this worktree
  actual: no such name exists anywhere in the repo; the actual mechanism is the pre-existing model_ref string field (present since the init commit), not a new retrofit — the contract's description does not match the code

- id: M3-practitioner-05
  severity: cosmetic
  location: chapters/ch06-recursive-decomp/01-subsystem-requirements.ipynb cell 0, 02-second-level.ipynb cell 0, 19/45/21 (exercise pointers)
  quote: "after running it you can see the nest-and-carry pattern that gave `ApplyHeat` its own logical carrier recur one level deeper"
  expected: a concept/exercise statement a learner reads at a glance
  actual: grammatically one sentence but semicolon/parenthetical-dense, longer than a typical "one sentence" reads; not blocking for a practitioner persona but adds parse time
