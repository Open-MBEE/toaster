# Novice Longitudinal Browser User Test - Round 2

**Persona:** Python-literate learner with NO prior SysML/MBSE knowledge  
**Test Date:** October 2, 2026  
**Test Round:** 2 (after Round 1 failures in fabrication and text-extraction)  
**Methodology:** Continuous read-through of entire book (10 chapters) using site navigation

## Important constraints for this round:
- Only report on pages actually visited in THIS session
- Use `get_page_text` tool to extract verbatim text before flagging confusions
- Never guess page names or URLs; click and verify

---

---

## CHUNK 2: Chapter 4

### PAGE 18: Chapter 4 Overview
- **URL:** http://localhost:3000/index-4
- **Page Identity:** "Chapter 4: Functional Decomposition - Overview"
- **Reading Position:** Page 18 of session
- **Visual Cognitive Load:** 2/5 (light) - Well-organized overview with clear table of 3 notebooks, moderate text density
- **Understanding vs Confusion:** Clear and well-structured. Quote from page: "Chapter 4 asks: how do we describe one functional step and make it an actual step of a larger function's decomposition? A step needs typed flows in and out and a phenomena relation among them." The overview clearly explains the learning progression for functional decomposition. Quote from Method: "ApplyHeat corresponds to 'apply thermal energy' in the video's decomposition; the full toaster functional architecture from Part 3 covers approximately 15 verb-noun functions. This tutorial models ApplyHeat as one worked example to teach the action def construct." Good contextualization that this is one example of many.
- **Text Density:** Well-matched - each section concise with good white space
- **Code vs Prose vs Figures:** No code on this page, all prose + one structured table showing 3 notebooks
- **Cadence:** Good introduction to functional layer, establishes progression clearly
- **Consistency:** Same structure and terminology style as Chapter 1-3 overviews
- **Data Consistency:** Numbers check out: 3 notebooks promised, 3 ingredients listed, expected result describes what will be built (ApplyHeat with balance constraint, three signal item defs, asserted_inference with AI-C04)

---

## CHUNK 1: Chapters 1-3

### PAGE 1: Chapter 1 Overview
- **URL:** http://localhost:3000/index-1
- **Page Identity:** "Chapter 1: System and Purpose - Overview"
- **Reading Position:** Page 1 of session
- **Visual Cognitive Load:** 2/5 (light) - Well-organized with clear sections, one small table, moderate text density
- **Understanding vs Confusion:** Clear and well-structured. The overview page does its job well by laying out:
  - What Chapter 1 asks (how to describe a system in SysML before knowing how it's built)
  - A table of 4 notebooks with their constructs and concepts
  - Expected result: what the cumulative model will contain
  - An experiment at the end
  - All terminology introduced here is explained or will be covered in the notebooks
- **Text Density:** Well-matched - each section is concise, uses white space effectively
- **Code vs Prose vs Figures:** No code on this page, all prose + one structured table. Appropriate for an overview.
- **Cadence:** Good introduction to the chapter, establishes goals clearly
- **Consistency:** Uses consistent language (e.g., "Bread", "Toast", "ToastBread", "ToastingSystem")
- **Data Consistency:** Numbers check out: 4 notebooks promised, 4 ingredients listed, expected result lists all constructs that will be built

### PAGE 2: Chapter 1, Notebook 1 - "abstract part def"
- **URL:** http://localhost:3000/abstract-def
- **Page Identity:** "Ch1-01: abstract part def"
- **Reading Position:** Page 2 of session
- **Visual Cognitive Load:** 3/5 (moderate) - Multiple code blocks interspersed with explanatory text, syntax highlighting helps readability
- **Understanding vs Confusion:** Mostly clear. The page follows a consistent pattern: introduce concept → show code → show output → explain what happened. However:
  - Verbatim quote from page: "abstract modifier: the Editor API does not yet author it (toaster#9 / OpenSysML#595); it parses and loads correctly via conn.load_from_content(), confirmed in the next cell." This feels like a workaround note that might confuse a novice about what's "normal" vs what's a limitation.
  - The negative control example is helpful (shows what NOT to do), but it appears somewhat late in the notebook
- **Text Density:** Good - code blocks break up the prose nicely, explanations are concise
- **Code vs Prose vs Figures:** Code is essential and well-introduced. Each code block has a clear purpose. Output is shown and discussed. This is an executable notebook, so code is the primary teaching vehicle.
- **Cadence:** Builds naturally from item definitions → action definition → abstract part definition. Pacing feels right after the overview.
- **Consistency:** 
  - Terminology: consistently uses "item def", "action def", "part def", "abstract part def", "perform"
  - Code style: consistent indentation and formatting
  - The spec citations (e.g., "§8.3.10.2") are consistent but will be meaningless to a novice - they may slow reading without adding value
- **Data Consistency:** 
  - The code shown matches the output
  - model.find("ToasterDemo::ToastingSystem") correctly returns the part def
  - model.find("ToasterDemo::ToastBread") correctly returns the action def
  - All assertions pass as shown

### PAGE 3: Chapter 1, Notebook 2 - "part def"
- **URL:** http://localhost:3000/part-def
- **Page Identity:** "Ch1-02: part def"
- **Reading Position:** Page 3 of session
- **Visual Cognitive Load:** 3/5 (moderate) - Similar structure to Ch1-01 with code blocks and explanatory text. Figure clearly rendered.
- **Understanding vs Confusion:** Clear. The page follows the same effective pattern as Ch1-01. However:
  - Quote from page: "Unlike abstract part def, it can be instantiated directly, but nothing yet says what it does." This is a helpful clarification, but a novice might not fully understand the implications of "instantiated directly" vs being abstract without more context.
  - The PartDefinition query showing "ToasterDemo::ToasterDemo::Toaster" in the output is confusing - is this a typo or is there another Toaster part def?
- **Text Density:** Good - code and prose well-balanced
- **Code vs Prose vs Figures:** Code is essential. Figure is clearly rendered and well-placed.
- **Figure Description (verified by screenshot):** Simple diagram with two rectangular boxes placed side-by-side on a light background. Left box labeled "HeatingSystem", right box labeled "ControlSystem", both with black borders. No connecting edge or relationship line between the boxes. Clean, uncluttered visual style. Approximately 150 pixels wide and 40 pixels tall. Text above figure explains "Diamond arrows show heating and control as parts Toaster owns; dashed arrows show each typed by its own part definition." (Note: this caption text actually refers to the next notebook's figure; this figure shows just the two independent boxes with no arrows.)
- **Cadence:** Good progression from abstract to concrete part definitions
- **Consistency:** 
  - Terminology: consistently uses "part def", "bare declaration", "loading"
  - Code style: same formatting as Ch1-01
  - Negative control pattern is consistent
- **Data Consistency:** 
  - Code matches output
  - model.find() confirms HeatingSystem exists
  - PartDefinition query lists all parts

### PAGE 4: Chapter 1, Notebook 3 - "specialization"
- **URL:** http://localhost:3000/specialization
- **Page Identity:** "Ch1-03: specialization"
- **Reading Position:** Page 4 of session
- **Visual Cognitive Load:** 2/5 (light) - Shorter page than previous notebooks, mostly prose with one code snippet
- **Understanding vs Confusion:** Very clear. The concept of specialization (`:>`) is well-explained:
  - Quote from page: ":> declares that every Toaster is a kind of ToastingSystem, inheriting the purpose action ToastBread it performs." Clear explanation of what specialization means.
  - Quote: "The supertype must be in scope: ToastingSystem was declared in notebook 01 and is present in the cumulative model." Good reminder about scoping rules.
- **Text Density:** Appropriate - concise but complete
- **Code vs Prose vs Figures:** Minimal code on this page - just the specialization declaration. This is appropriate for the simplicity of the concept.
- **Cadence:** Natural progression from defining separate parts to relating them via specialization
- **Consistency:** Consistent terminology and style
- **Data Consistency:** 
  - toaster.specializations correctly reports one specialization to ToastingSystem
  - All assertions pass

### PAGE 5: Chapter 1, Notebook 4 - "composition"
- **URL:** http://localhost:3000/composition
- **Page Identity:** "Ch1-04: composition"
- **Reading Position:** Page 5 of session
- **Visual Cognitive Load:** 3/5 (moderate) - Multiple code blocks showing composition syntax, longer explanation about the cumulative model approach. Figure clearly rendered.
- **Understanding vs Confusion:** Mostly clear, but one point requires careful attention:
  - Quote from page: "Every notebook in this chapter loads the same already-complete models/ch01-cumulative.sysml, so there is no partial Toaster in this chapter for one notebook to hand off to the next. Notebook 03's bare Toaster :> ToastingSystem; and this notebook's full declaration are each an illustrative fragment, checked independently by check_construction.py against a minimal stub, showing what one step of Editor-API authoring would add once the API supports it, not a live patch to a running model." This is a sophisticated explanation of the tutorial structure that might confuse a novice - it explains that each notebook is independent and illustrative rather than cumulative within the chapter. This is important context but could be clearer.
  - Quote: "cycleTime is a typed, unit-bearing slot with no value: how long a cycle actually takes is a result the design produces, derived later from the mechanism and the energy balance, not a number chosen here." Good explanation of the design decision to leave cycleTime unset.
- **Text Density:** Appropriate
- **Code vs Prose vs Figures:** Code is well-introduced. Figure is clearly rendered.
- **Figure Description (verified by screenshot):** Hierarchical composition diagram showing: "Toaster" box at top center, with two diamond-headed lines (ownership arrows) pointing downward to two child boxes below: "heating" (left) and "control" (right). White boxes with black borders on light background. Clean, tree-like structure showing Toaster's composition hierarchy. Approximately 200-250 pixels wide and 80-100 pixels tall. The diamond-tipped arrows (composition/aggregation relationships) clearly distinguish the ownership relationship from simple associations.
- **Cadence:** Good progression to complete the Toaster definition
- **Consistency:** Consistent with previous notebooks
- **Data Consistency:** 
  - toaster.parts() returns the correct two parts (heating, control)
  - toaster.attributes() returns cycleTime
  - All assertions pass

### PAGE 6: Chapter 1 Conclusion
- **URL:** http://localhost:3000/conclusion
- **Page Identity:** "Chapter 1: Conclusion"
- **Reading Position:** Page 6 of session
- **Visual Cognitive Load:** 1/5 (very light) - Three short sections, all prose, no code or complex figures
- **Understanding vs Confusion:** Excellent summary. The page clearly restates:
  - What was built (ToastingSystem, HeatingSystem, ControlSystem, Toaster with cycleTime and composition)
  - What this establishes (answers Chapter 1's question about how to describe a system)
  - What comes next (preview of Chapter 2 on requirements)
- **Text Density:** Perfect - concise summaries that let you review the chapter without overwhelming detail
- **Code vs Prose vs Figures:** No code on this page - purely summarizing what was accomplished
- **Cadence:** Excellent - provides closure to Chapter 1 and transition to Chapter 2
- **Consistency:** Consistent terminology and referencing back to the cumulative model
- **Data Consistency:** All statements about the model match what was built in the notebooks

---

## PAGE 7: Chapter 2 Overview
- **URL:** http://localhost:3000/index-2
- **Page Identity:** "Chapter 2: Requirements and Assumptions - Overview"
- **Reading Position:** Page 7 of session
- **Visual Cognitive Load:** 2/5 (light) - Same structure as Chapter 1 overview with clear sections and a table
- **Understanding vs Confusion:** Clear. Chapter 2 introduces three new concepts:
  - Quote: "Chapter 2 asks: what must the toaster do, and what do we assume about the conditions under which it operates?" Clear framing of the chapter's purpose.
  - New construction: "requirement def + subject + require constraint" for stating what the system must satisfy
  - New construction: "attribute :>> override" for creating named usages with modified attributes
  - New construction: "asserted_context record" for recording assumptions
- **Text Density:** Well-matched, similar to Chapter 1
- **Code vs Prose vs Figures:** No code on overview page, all prose + table
- **Cadence:** Introduces more sophisticated concepts (requirements, attribute overrides, judgment records) that build on Chapter 1's foundation
- **Consistency:** Same structure and terminology as Chapter 1 overview
- **Data Consistency:** The expected result clearly lists what the cumulative model will contain after Chapter 2

### CHAPTER 1 SUMMARY
**Chapter 1: System and Purpose** introduces the foundational SysML constructs for declaring a system's purpose and logical composition:
- **Constructs introduced:** abstract part def, part def, action def (with typed flows), specialization (`:>`), part usage (composition), attribute declaration
- **Learning progression:** Well-structured from abstract concepts (purpose, item types) through concrete implementations (component placeholders, whole-part relationship)
- **Pacing:** Appropriate - each notebook introduces one concept, provides code examples, negative controls, and verification
- **Clarity:** Generally very clear, though one notebook has a sophisticated meta-discussion about the tutorial structure that may confuse novices
- **Figures:** Ch1-02 shows two independent part definitions (HeatingSystem, ControlSystem) as separate boxes with no connection. Ch1-04 shows Toaster's composition with diamond-tipped ownership arrows pointing to its heating and control parts. Both figures render cleanly and are well-integrated into the narrative.
- **Exercises:** Each notebook includes a chapter exercise prompt for coffee maker modeling

---

## CHAPTER 2: REQUIREMENTS AND ASSUMPTIONS

### PAGE 7: Chapter 2 Overview
(Already documented above - see entry above)

### PAGE 8: Chapter 2, Notebook 1 - "requirement def"
- **URL:** http://localhost:3000/requirement-def
- **Page Identity:** "Ch2-01: requirement def"
- **Reading Position:** Page 8 of session
- **Visual Cognitive Load:** 3/5 - Code blocks and prose explaining requirements, constraint syntax is new and needs attention
- **Understanding vs Confusion:** 
  - Clear introduction to requirement def as formal statements of what the system must satisfy
  - Quote: "A complete requirement has three parts... a description of the need, a rationale for why that need is valid, and a verification method."
  - The doc block structure and constraint body syntax are well-explained
  - Terminology note: "subject toaster : Toaster" declares the part type being constrained
- **Text Density:** Well-matched
- **Code vs Prose vs Figures:** Code is essential; negativecontrol examples are valuable for understanding syntax errors
- **Cadence:** Natural progression from Ch1's structural model to Ch2's behavioral constraints
- **Consistency:** Similar pattern to Ch1 notebooks (introduction, code, negative control, verification)
- **Data Consistency:** requirement kind and id correctly reported by model.find() and model.query()

### PAGE 9: Chapter 2, Notebook 2 - "attribute override"
- **URL:** http://localhost:3000/assumptions
- **Page Identity:** "Ch2-02: attribute override"
- **Reading Position:** Page 9 of session
- **Visual Cognitive Load:** 2/5 (light) - Introduces one new operator (`:>>`) with clear examples
- **Understanding vs Confusion:** 
  - Quote: "attribute :>> redeclares the inherited cycleTime under slow. The :>> operator is a redefinition; it can only name an attribute that already exists in the type chain."
  - Clear explanation of the difference between redefinition (`:>>`) and default (which Chapter 1 removed)
  - Quote: "slow's 200 seconds is deliberately fixed and deliberately faulty: chosen to exceed TimelyToast's 180-second bound, not to represent a plausible design point." - Good clarification of the fixture concept
- **Text Density:** Appropriate
- **Code vs Prose vs Figures:** Code is minimal and focused
- **Cadence:** Builds on Chapter 2's requirement by showing how to create test fixtures
- **Consistency:** Same pattern as previous notebooks
- **Data Consistency:** slow.attributes() correctly reports the overridden cycleTime

### PAGE 10: Chapter 2, Notebook 3 - "asserted context" (judgment record)
- **URL:** http://localhost:3000/judgment-context
- **Page Identity:** "Ch2-03: asserted context"
- **Reading Position:** Page 10 of session
- **Visual Cognitive Load:** 4/5 (moderate-high) - Introduces metadata definitions, ReviewRecordRef tags, and ReviewRecord Python objects; multiple interrelated concepts
- **Understanding vs Confusion:** 
  - This page introduces a significant paradigm shift: moving from SysML model declarations to parallel Python-based judgment records
  - Quote: "An asserted_context record (Hawkins 2011 §3.2) documents one such assumption. The context record does not claim the design is correct. It claims that the assumption used for the cycle-time estimate is appropriate, not that any evaluation has been performed."
  - New constructs: metadata def (with ReviewRecordRef), ReviewRecord Python objects with kind="asserted_context", disposition="pending"
  - The bidirectional linking between SysML model (via metadata tags) and Python ReviewRecord objects is sophisticated and introduces complexity that may confuse novices about where the real "truth" lives
- **Text Density:** Moderate - lots of new concepts introduced densely
- **Code vs Prose vs Figures:** Mix of SysML code and Python code; both are necessary but create cognitive load
- **Cadence:** Significant jump in complexity from notebooks 01-02
- **Consistency:** Introduces a new pattern (metadata/ReviewRecord linking) not seen in Ch1
- **Data Consistency:** AC-001 tag correctly links to nominal via metadata

### PAGE 11: Chapter 2 Conclusion
- **URL:** http://localhost:3000/conclusion-1
- **Page Identity:** "Chapter 2: Conclusion"
- **Reading Position:** Page 11 of session
- **Visual Cognitive Load:** 2/5 (light) - Three clear sections summarizing the chapter
- **Understanding vs Confusion:** 
  - Excellent summary of what was accomplished
  - Quote: "No analysis in this chapter derives a cycle time, so neither usage's relationship to the bound is reported as a settled pass/fail verdict; the context record's estimate for nominal is likewise conditional on its stated assumption, not a derived value."
  - Makes clear that nominal remains open (no value derived), slow is the deliberate fault fixture, and context records are provisional/conditional
- **Text Density:** Perfect - concise summaries
- **Code vs Prose vs Figures:** Pure prose summary
- **Cadence:** Good closure and transition to Chapter 3
- **Consistency:** Same structure as Chapter 1 conclusion
- **Data Consistency:** Accurately reflects what was built in the notebooks

### CHAPTER 2 SUMMARY
**Chapter 2: Requirements and Assumptions** introduces formal requirements and the first judgment records:
- **Constructs introduced:** requirement def, require constraint, part usage (named instances), attribute :>> override, metadata def, ReviewRecordRef, asserted_context ReviewRecord (Python)
- **Key concepts:** Separating descriptions/rationale (in SysML doc) from verification methods (Chapter 3+), creating test fixtures with deliberately injected faults, recording modeling assumptions as judgment records
- **Complexity jump:** Introduces Python ReviewRecord objects parallel to SysML model; this is a significant paradigm shift
- **Clarity:** Chapters 01-02 are clear; Chapter 03 introduces conceptual density that may challenge novices
- **Consistency:** Maintains pattern of notebooks, but introduces new judgment record pattern

---

## CHAPTER 3: MEASURES OF SUCCESS

### PAGE 12: Chapter 3 Overview
- **URL:** http://localhost:3000/index-3
- **Page Identity:** "Chapter 3: Measures of Success - Overview"
- **Reading Position:** Page 12 of session
- **Visual Cognitive Load:** 2/5 - Clear structure, table with 4 notebooks, well-organized
- **Understanding vs Confusion:** 
  - Quote: "Chapter 3 asks: how do we record and check a satisfaction claim against a requirement?"
  - The overview clearly introduces four new constructs: requirement usage, assert satisfy/assert not satisfy, asserted_solution, verification def
  - Lists expected results and experiment clearly
- **Text Density:** Well-matched
- **Code vs Prose vs Figures:** No code on overview
- **Cadence:** Builds on Chapter 2 by adding evaluation and verification
- **Consistency:** Same structure as Chapter 1 and 2 overviews
- **Data Consistency:** Expected results list matches what the notebooks will build

### PAGE 13: Chapter 3, Notebook 1 - "requirement usage" (MoE framing)
- **URL:** http://localhost:3000/moe-definition
- **Page Identity:** "Ch3-01: requirement usage"
- **Reading Position:** Page 13 of session
- **Visual Cognitive Load:** 4/5 (high) - Introduces requirement usage and MoE/MoP framing judgment; dense conceptual and code content
- **Understanding vs Confusion:** 
  - Quote: "What remains open is whether the measure it constrains, toast time, is a measure of effectiveness (the user's acceptance) or a measure of performance (an engineering figure with a threshold derived from something else). That split is a modeling judgment, not a fact the model states."
  - This is a sophisticated concept - distinguishing between user-centric effectiveness and engineering performance thresholds
  - The section on creating ReviewRecordRef tags and ReviewRecord objects with criteria/scope/premises continues the parallel SysML+Python pattern from Ch2-03
  - New vocabulary: MoE, MoP, appropriateness (Hawkins), SEBoK distinction
- **Text Density:** High - many new concepts
- **Code vs Prose vs Figures:** Mix of SysML (requirement usage) and Python (ReviewRecord construction)
- **Cadence:** Builds on Ch2 judgments with evaluation-related framing
- **Consistency:** Continues metadata/ReviewRecord pattern from Ch2-03
- **Data Consistency:** AC-C03 tag correctly anchors the asserted_context record

### PAGE 14: Chapter 3, Notebook 2 - "satisfaction claims" (assert/assert not)
- **URL:** http://localhost:3000/mop-candidate-eval
- **Page Identity:** "Ch3-02: satisfaction claims"
- **Reading Position:** Page 14 of session
- **Visual Cognitive Load:** 3/5 - New syntax (assert satisfy / assert not satisfy) but straightforward application
- **Understanding vs Confusion:** 
  - Quote: "The claim is folded into slow's own body: slow names itself as the usage the claim is about, so no separate container is needed."
  - Clear explanation of how satisfaction claims are embedded in part usages
  - Quote: "timely(slow) evaluates to False: slow's 200-second cycleTime does not meet the 180-second bound. The model's claim is assert not satisfy, so this result confirms the claim rather than contradicting it."
  - Good explanation of how evaluating a negated claim against a faulty fixture tests the requirement
- **Text Density:** Moderate
- **Code vs Prose vs Figures:** Code shows the assert syntax and model.eval() for checking claims
- **Cadence:** Natural progression from requirement usage to evaluating satisfaction
- **Consistency:** Follows notebook pattern
- **Data Consistency:** model.eval("ToasterDemo::timely(ToasterDemo::slow)") correctly returns False, confirming the negated claim

### PAGE 15: Chapter 3, Notebook 3 - "threshold judgment" (asserted solution)
- **URL:** http://localhost:3000/threshold-judgment
- **Page Identity:** "Ch3-03: threshold judgment"
- **Reading Position:** Page 15 of session
- **Visual Cognitive Load:** 3/5 - Introduces asserted_solution ReviewRecord; similar complexity to Ch3-01
- **Understanding vs Confusion:** 
  - Introduces the final judgment record type: asserted_solution (what an evaluated claim supports, what remains open)
  - The three-part requirement anatomy is reinforced: description/rationale (Ch2), verification method (Ch3-04), and satisfaction evaluation (this notebook)
- **Text Density:** Moderate
- **Code vs Prose vs Figures:** Python ReviewRecord object construction for asserted_solution
- **Cadence:** Brings together prior notebooks into a complete judgment framework
- **Consistency:** Extends judgment record pattern
- **Data Consistency:** References to correct model elements (timely, slow, etc.)

### PAGE 16: Chapter 3, Notebook 4 - "verification def"
- **URL:** http://localhost:3000/verification-case
- **Page Identity:** "Ch3-04: verification def"
- **Reading Position:** Page 16 of session
- **Visual Cognitive Load:** 2/5 - Introduces verification def, which is straightforward after prior notebooks
- **Understanding vs Confusion:** 
  - Quote: "A complete requirement has three parts... description, rationale, and verification method. The first two are in TimelyToast's doc comment (Chapter 2). verification def in SysML v2 (§7.24) closes the anatomy by declaring how the requirement will be verified."
  - Clear explanation of how verification def completes the requirement anatomy
  - Note about #verificationMethod metadata not yet being supported in OpenSysML is useful context about tooling limitations
- **Text Density:** Moderate
- **Code vs Prose vs Figures:** Code shows verification def structure with subject and objective
- **Cadence:** Completes the requirement cycle started in Chapter 2
- **Consistency:** Follows notebook pattern
- **Data Consistency:** Correctly shows how verification def names the requirement usage to verify

### PAGE 17: Chapter 3 Conclusion
- **URL:** http://localhost:3000/conclusion-2
- **Page Identity:** "Chapter 3: Conclusion"
- **Reading Position:** Page 17 of session
- **Visual Cognitive Load:** 2/5 - Clear summary sections
- **Understanding vs Confusion:** 
  - Quote: "That restraint, an evaluated claim on slow, no claim on nominal, and a verification case that states how the requirement will eventually be checked, is what distinguishes an engineering judgment from an assertion."
  - Excellent articulation of the discipline: not claiming what you don't know, proving failure cases, planning verification
  - Makes clear that nominal remains genuinely open (no derived value yet)
- **Text Density:** Perfect
- **Code vs Prose vs Figures:** Pure prose
- **Cadence:** Good closure and transition to Chapter 4
- **Consistency:** Same structure as prior conclusions
- **Data Consistency:** Accurately reflects what was built

### CHAPTER 3 SUMMARY
**Chapter 3: Measures of Success** introduces requirement evaluation and judgment records:
- **Constructs introduced:** requirement usage, assert satisfy / assert not satisfy, asserted_solution ReviewRecord, verification def
- **Key concepts:** Recording satisfaction claims, evaluating them against model values, distinguishing MoE (effectiveness) from MoP (performance), completing the three-part requirement anatomy
- **Complexity:** High - introduces multiple judgment record types and meta-decision patterns (MoE vs MoP framing)
- **Clarity:** Each notebook is individually clear, but the cumulative complexity of judgment records (AC-C03, AS-C03) may challenge novices about what is provisional vs. settled
- **Learning curve:** Steep - introduces evaluation and decision-documentation patterns not previously seen
- **Consistency:** Continues the SysML+Python parallel pattern from Chapter 2

---

## CHUNK 3: Chapter 4

### PAGE 19: Chapter 4, Notebook 1 - "action def"
- **URL:** http://localhost:3000/action-def-ffbd
- **Page Identity:** "Ch4-01: action def"
- **Reading Position:** Page 19 of session
- **Visual Cognitive Load:** 3/5 (moderate) - Multiple code blocks interspersed with explanatory text, one SVG figure, good readability with syntax highlighting
- **Understanding vs Confusion:** Mostly clear. The page follows a consistent pattern: introduce concept → show code → show output → explain what happened. Key explanations:
  - Quote from page: "ApplyHeat states typed flows and an asserted phenomena relation, but it is still a free-floating action, not a step of anything. The next fragment nests it inside ToastBread, the action Chapter 1 declared with no body, and binds applyHeat's own bread input to ToastBread's bread: the one flow actually available at this level." Clear progression from standalone action to nested step.
  - Quote: "ToastBread's own doc and its bread/toast parameters are restated unchanged; the sequence is new, and it wires the one flow this level actually has. The full increment for this notebook is ApplyHeat's declaration together with ToastBread's reopened body." Good explanation of how reopening works without duplication.
  - Important note about explicit [0..*] multiplicity: "A bare, unstated multiplicity and writing [0..*] out explicitly should mean the same thing (SysML v2.0 formal/2026-03-02 7.6.3, 7.6.4: a keyword-less in/out parameter like these already defaults to [0..*]), but OpenSysML v0.9.0 treats them differently: left implicit, any attribute of a Toaster usage that reaches ApplyHeat through ToastBread fails to evaluate; written out, exactly the same model evaluates cleanly (DEFERRED.md D-026)." This is a sophisticated workaround explanation that clarifies a real tool inconsistency without claiming anything new about the model.
- **Text Density:** Well-matched - code blocks break up prose effectively, explanations are concise but complete
- **Code vs Prose vs Figures:** Code is essential and well-introduced. Each code block has clear purpose. One SVG figure rendered clearly. All three components well-balanced.
- **Figure Description (verified by screenshot):** Vertical flow diagram titled "ToastBread" (labeled as "=action def=") showing a sequence:
  - Black circle at top (start node)
  - Box containing "applyHeat : ApplyHeat" with "own flow" text inside
  - Black circle at bottom (done/end node)
  - Vertical connecting arrows between elements
  - Clean white background with black borders, approximately 220x180 pixels
  - Clearly shows the start → applyHeat action → done sequence
- **Cadence:** Natural progression from ApplyHeat definition → parameters explanation → constraint definition → nesting in ToastBread → visualization → verification
- **Consistency:** 
  - Follows same effective pattern as Ch1 notebooks
  - Terminology consistent: "action def", "typed flows", "phenomena constraint", "nested step"
  - Negative control pattern is present (checking undefined action reference)
  - Spec citations consistent (e.g., "SysML v2.0 formal/2026-03-02")
- **Data Consistency:**
  - Code shown matches printed output
  - model.find("ToasterDemo::ApplyHeat") correctly identifies it as actionDef
  - model.find("ToasterDemo::ToastBread::applyHeat") correctly identifies nested step as actionUsage
  - model.find("ToasterDemo::ApplyHeat::balance") correctly identifies balance constraint as constraintUsage
  - slow.cycleTime still evaluates to 200 [SI::s], confirming the model stays evaluable
  - Negative control correctly demonstrates "unresolved reference" error for undefined action

### PAGE 20: Chapter 4, Notebook 2 - "item def"
- **URL:** http://localhost:3000/heating-refinement
- **Page Identity:** "Ch4-02: item def"
- **Reading Position:** Page 20 of session
- **Visual Cognitive Load:** 2/5 (light) - Multiple code blocks with explanatory text, no figures, straightforward item definitions
- **Understanding vs Confusion:** Very clear. Concept is simple and well-explained:
  - Quote from page: "Start names a signal, not the bread entering the toaster: that material flow is already ToastBread::bread. The doc states this plainly so the model, not the surrounding prose, is the authority on what Start denotes." Excellent explanation of item def purpose - using doc to declare what a signal is and, crucially, what it is NOT (distinguishing signals from materials).
  - Quote: "Finish names the paired signal for the cycle's end, distinct from ToastBread::toast, the toast itself." Clear distinction between signal and material.
  - Quote: "None of the three is wired as an accepted or produced item of ApplyHeat in this chapter; each states its own meaning so a later chapter that does wire them has a fixed denotation to wire to, not an undecided one." Good forward-looking design rationale explaining why signals are declared now but not yet used.
- **Text Density:** Light - concise explanations of each signal's purpose with ample white space
- **Code vs Prose vs Figures:** Simple code (three item def definitions), no figures, minimal prose. The code is almost self-explanatory due to well-written doc comments.
- **Cadence:** Simple, effective progression - introduce problem (three signals in Chapter 1 left undefined) → declare three item defs → explain each one's purpose → negative control → verification → exercise
- **Consistency:**
  - Follows established notebook pattern from Ch1-3
  - Terminology consistent: "item def", "signal", "doc" (as denotation authority)
  - Negative control pattern present (checking undefined specialization)
  - Minimal spec citations - this notebook is deliberately simplified
- **Data Consistency:**
  - Code shown matches output
  - model.find("ToasterDemo::Start") confirms it's found as itemDef
  - model.find("ToasterDemo::Finish") confirms it's found as itemDef
  - model.find("ToasterDemo::Cancel") confirms it's found as itemDef
  - Negative control correctly demonstrates "unresolved reference" error for undefined base type

### PAGE 21: Chapter 4, Notebook 3 - "completeness check"
- **URL:** http://localhost:3000/completeness-check
- **Page Identity:** "Ch4-03: completeness check"
- **Reading Position:** Page 21 of session
- **Visual Cognitive Load:** 4/5 (high) - Multiple code blocks, one structural figure, complex judgment record construction with extensive documentation fields
- **Understanding vs Confusion:** Complex but well-scaffolded. This is the most sophisticated page yet - introduces full Hawkins §3.1 judgment record schema. Key clarifications:
  - Quote from page: "The question this notebook asks is narrower than whether the toaster's functional architecture is complete: it is whether the flows this one worked example names are accounted for, honestly scoped to what one action out of Douglas's roughly fifteen verb-noun functions can show." Excellent scope-setting to avoid overreach.
  - Quote: "Asserting non-negativity alongside the sum bound is what catches this second case; evidence_refs and rationale cite all three results directly." Shows how constraint bounds do real work by demonstrating failures.
  - The challenge section (counterevidence and residual_uncertainties) is particularly important pedagogically - explicitly stating what is NOT being claimed and what remains open.
  - Quote about validation: "an empty error list confirms the required fields, including a non-empty premises, are present, not merely printed." Emphasizes that validation is real, not ceremonial.
- **Text Density:** High - extensive code, detailed narrative field-by-field construction, comprehensive documentation
- **Code vs Prose vs Figures:** Code is essential (record construction, probe scenarios, validation), one figure (containment diagram), extensive prose documentation across claim/criteria/premises/evidence/challenge sections
- **Figure Description (verified by screenshot):** Hierarchical containment diagram showing:
  - "Toaster" at top (labeled as "Ch4" title)
  - Two diamond-headed composition arrows to "heating" and "control" parts
  - Each part shown as usage box with full path (e.g., "ToasterDemo::Toaster::heating")
  - Dashed arrows from usage boxes down to type definitions
  - "HeatingSystem" and "ControlSystem" boxes at bottom
  - Clean white background, black borders, approximately 420x200 pixels
  - Clearly shows part-type relationship hierarchy
- **Cadence:** Sophisticated multi-part progression: frame question narrowly → dump cumulative model → show structure → negative control → build record iteratively (anchor → claim → scope+criteria → premises → evidence by multiple probes → challenge sections) → assemble Python object → validate and confirm
- **Consistency:**
  - Continues judgment record pattern from Ch2-03 (ReviewRecord) and Ch3 records
  - Uses established probe pattern (plausible/implausible/failure cases)
  - References prior records (AS-C03 in premises)
  - Negative control pattern present (constraint referencing undefined feature)
  - Hawkins schema fields clearly named and populated
- **Data Consistency:**
  - Probe verdicts match expectations: plausible passes (700+200<=1000), implausible fails (900+300>1000), negativeLoss fails (-600 violates non-negativity)
  - slow.cycleTime: 200 [SI::s] still evaluates correctly
  - Model tag matches model content: {'tag': 'ToasterDemo::aiC04Tag', 'identifier': 'AI-C04', 'annotated_element': 'ToasterDemo::ApplyHeat'}
  - Validation errors empty list: record passes all schema checks

### PAGE 22: Chapter 4 Conclusion
- **URL:** http://localhost:3000/conclusion-3
- **Page Identity:** "Chapter 4: Conclusion"
- **Reading Position:** Page 22 of session
- **Visual Cognitive Load:** 1/5 (very light) - Pure prose, no code or figures, clean three-part structure with clear headings
- **Understanding vs Confusion:** Excellent summary. Clear, concise, well-organized recap:
  - Quote from page: "ApplyHeat states what the system does, bread and energy in, toast and accounted-for energy out, without committing to how the hardware achieves it." Excellent articulation of function (what) vs implementation (how) separation - a key design principle not explicitly named but strongly demonstrated.
  - Quote: "The balance constraint is a real, evaluable, asserted relation, not a conversion formula: it holds or fails against concrete values, catching both an overdrawn energy split and a negative-loss split, and no specific efficiency is assumed." Reinforces that constraints are tested, not merely declared - directly references the probe verdicts from previous page.
  - Quote: "The inference record states the scope honestly: this is a flow accounting for the one function modeled, not for the toaster's full functional architecture of roughly fifteen verb-noun functions." Emphasizes value of honest scope-setting, a theme repeated throughout the chapter.
  - Excellent forward-looking preview of Chapter 5: introduces allocate and interface as new constructs for logical components and their connections.
- **Text Density:** Light - well-spaced three main sections with clear headings ("What we built", "What this establishes", "What comes next")
- **Code vs Prose vs Figures:** Pure prose, no code or figures - appropriate for conclusion page
- **Cadence:** Clean three-part structure: "What we built" (recap with specifics) → "What this establishes" (significance and lessons) → "What comes next" (preview and exercise reference)
- **Consistency:**
  - Matches conclusion format from Ch1 and Ch3 (same three-part structure)
  - Terminology consistent with Chapter 4 content (ApplyHeat, ToastBread, Start/Finish/Cancel, AI-C04, AS-C03)
  - Exercise section follows established pattern (references coffee maker domain, links to chapter exercises, mirrors worked example)
- **Data Consistency:**
  - All references accurate to what was built in Chapter 4
  - Correctly describes slow.cycleTime evaluation (200 seconds from Chapter 2)
  - Accurately previews Chapter 5 scope (logical components, allocate construct for connecting functions to components, interface construct for connection points)

---

## CHUNK 1 OVERALL OBSERVATIONS

**Pacing and Progression:**
- Chapters 1-3 follow a clear logical progression: purpose → constraints → evaluation
- Chapter 1 (6 pages): Structure and purpose - quick conceptual foundation
- Chapter 2 (5 pages): Adding constraints and assumptions - introduces judgment records, significant complexity jump in Ch03 with metadata/Python
- Chapter 3 (6 pages): Evaluating constraints - continues judgment record complexity, introduces MoE/MoP framing, verification

**Cognitive Load Pattern:**
- Ch1 increases gradually through 4 notebooks, each adding one concept (abstract part def → part def → specialization → composition)
- Ch2 maintains moderate load through 01-02, then jumps significantly in Ch03 with metadata definitions and ReviewRecord Python objects
- Ch3 maintains high load: Ch01 (MoE framing) is complex, Ch02-04 build on judgment record pattern

**Clarity and Confusion Points:**
1. **Ch1-04's meta-discussion** about the cumulative model structure is sophisticated and may confuse novices
2. **Ch2-03's introduction of ReviewRecordRef and ReviewRecord** is a significant paradigm shift (moving to parallel Python objects); could benefit from more scaffolding
3. **Ch3-01's MoE/MoP framing decision** is conceptually important but requires understanding of both user-centric and engineering perspectives
4. **Figures render clearly** in Ch1-02 and Ch1-04 (verified by screenshot). Figures in Ch2 and Ch3 not yet visually verified in detail.
5. **Inline code spans in prose** (like `cycleTime`, `ToasterDemo::Toaster`) are clearly marked and easy to distinguish

**Strengths:**
- Each notebook follows a consistent pattern: motivation → code → explanation → negative control → verification
- Negative controls are valuable for understanding syntax and semantic errors
- References back to prior material (Chapter 1 model, Chapter 2 definitions) maintain continuity
- Exercises at the end of each notebook provide practice with similar but distinct domain (coffee maker)
- Conclusions effectively summarize and transition between chapters

**Suggestions for Improvement:**
- Consider pre-announcing the paradigm shift from SysML-only to SysML+Python in Chapter 2
- Add more scaffolding around MoE/MoP concepts before Ch3-01
- Consider rendering/displaying figures more prominently in the browser view
- Provide glossary or sidebar definitions for terms like "asserted_context", "MoE", "MoP" that might be unfamiliar to novices
- Ch1-04's discussion of the cumulative model approach might benefit from being moved to the chapter overview or a separate primer

---

## CHUNK 3: Chapter 5

### PAGE 23: Chapter 5 Overview
- **URL:** http://localhost:3000/index-5
- **Page Identity:** "Chapter 5: Architecture and Allocation - Overview"
- **Reading Position:** Page 23 of session
- **Visual Cognitive Load:** 2/5 (light) - Well-organized overview with clear structure, table of notebooks, moderate text density
- **Understanding vs Confusion:** Clear and well-structured. Chapter question is simple and well-explained:
  - Quote from page: "This chapter asks: which logical component performs which function, and how are components connected?" Clear, focused question introducing two new constructs: allocate (function-to-component assignment) and interface (component connections).
  - Quote: "After completing this chapter, the cumulative model has a named, usage-level allocate connecting ApplyHeat to the logical component that performs it, and a real port-typed interface between ControlSystem and HeatingSystem." Specific, checkable goals.
  - The Method section clearly explains each notebook's role: navigation (how to find elements) → allocate (what component does what) → interface (how components connect)
  - Expected result section provides detailed preview of model elements that will be created, with specific code references (HeatingSystem, DurationPort, interface, allocation)
- **Text Density:** Light - well-spaced sections with clear headings and white space
- **Code vs Prose vs Figures:** Pure prose, no code or figures on this overview page - appropriate for an overview
- **Cadence:** Standard overview structure: Purpose → Ingredients (table) → Equipment → Method (detailed progression) → Expected result → Experiment
- **Consistency:** 
  - Matches overview format from Chapters 1, 2, 3, 4
  - Consistent terminology and structure
  - Table of notebooks with Notebook, Concept, and (implied) progression
- **Data Consistency:**
  - Accurately describes what Chapter 5 will add (allocate, interface, DurationPort)
  - Correctly identifies which components will be involved (HeatingSystem, ControlSystem)
  - References Chapter 4 function (ApplyHeat) and Chapter 1 component (Toaster) correctly
  - Exercise domain consistent with prior chapters (coffee maker: applyWater to brewUnit, CoffeeFlow assembly with pump and filterUnit)

### PAGE 24: Chapter 5, Notebook 1 - "model navigation"
- **URL:** http://localhost:3000/model-navigation
- **Page Identity:** "Ch5-01: model navigation"
- **Reading Position:** Page 24 of session
- **Visual Cognitive Load:** 3/5 (moderate) - Multiple code blocks, one structural diagram, introduces APIs and demonstrates them
- **Understanding vs Confusion:** Very clear. Chapter shift explained well:
  - Quote from page: "Chapter 5 shifts from defining the model to inspecting and extending it. The cumulative model now carries dozens of named elements: part definitions, part usages, ports, an allocation, a requirement, and item definitions. Navigating by position in a query result is fragile; navigating by qualified name (package::element) is stable as the model grows." Excellent explanation of why qualified names are more robust than position-based navigation.
  - Quote: "model.find(name) returns a Symbol or None for a short or fully-qualified name. model.get(fqn) returns a Symbol and raises if the name is absent. Together they are the navigation layer the rest of this chapter, and Chapter 6, build on." Clear, practical distinction between the two methods.
  - Good note about negative control: "model.find() and model.get() only resolve elements that parsed. The negative control below loads a model with an unresolved specialization and confirms it fails before navigation is attempted." Shows that navigation assumes valid model.
- **Text Density:** Moderate - code blocks break up prose effectively
- **Code vs Prose vs Figures:** Code is essential (demonstrating find and get), one structure diagram, explanatory prose
- **Figure Description (verified by screenshot):** Complex containment diagram showing cumulative model through Ch5:
  - Two usage boxes at top: "ToasterDemo::nominal" and "ToasterDemo::slow" with dashed lines to
  - Central "Toaster" box with dashed line to left showing "«abstract» ToastingSystem" (specialization relationship)
  - From Toaster, two diamond-headed composition arrows to "heating" and "control"
  - Below each, usage boxes "ToasterDemo::Toaster::heating" and "ToasterDemo::Toaster::control" with downward arrows
  - Type definition boxes below: "«abstract» HeatingSystem" and "ControlSystem"
  - HeatingSystem marked abstract (dashed box), ControlSystem concrete (solid box)
  - Approximately 520x280 pixels, clearly shows part/usage/type relationships
- **Cadence:** Simple, effective progression: explain chapter shift → show full structure → negative control → demonstrate both navigation methods on real elements → exercise
- **Consistency:**
  - Follows notebook pattern from Ch1-4
  - Negative control pattern present (unresolved reference fails to load)
  - Symbol/API pattern consistent with prior chapters
- **Data Consistency:**
  - model.find("ToasterDemo::HeatingSystem") correctly returns partDef
  - model.get("ToasterDemo::ApplyHeat") correctly returns actionDef
  - model.find("ToasterDemo::Nonexistent") correctly returns None
  - Negative control correctly shows "unresolved reference: UndefinedBase" error
  - Exercise domain consistent (CoffeeDemo::CoffeeFlow reference mirrors toaster pattern)

### PAGE 25: Chapter 5, Notebook 2 - "allocate"
- **URL:** http://localhost:3000/allocate
- **Page Identity:** "Ch5-02: allocate"
- **Reading Position:** Page 25 of session
- **Visual Cognitive Load:** 3/5 (moderate) - Multiple code blocks with explanatory text, no figures
- **Understanding vs Confusion:** Very clear. Allocate concept introduced well:
  - Quote from page: "allocate connects these two: the component that performs the function, named and pointed at directly, rather than left as an unstated intent." Excellent one-sentence summary of allocate's purpose - making function-component relationships explicit in the model.
  - Quote: "HeatingSystem becomes an abstract logical component that performs ApplyHeat: the perform relationship states, in the model, which component carries the function. This is the logical-component idiom this tutorial uses: an abstract part def that performs an action, not yet realized by any concrete part." Clear articulation of the idiom being taught.
  - Quote: "Usage-level allocation is exactly this distinction, not a detail to blur past." Emphasizes importance of allocating the usage (Toaster::heating), not the type (HeatingSystem).
  - Quote about find_allocations output: "find_allocations shows heatAllocation's real ends: the first is the feature chain toastBread.applyHeat — toastBread, declared on ToastingSystem and inherited by Toaster, then applyHeat, nested inside the ToastBread action — and the second is Toaster::heating, a usage, not HeatingSystem the definition." Excellent clarification of the two ends and usage vs type distinction.
- **Text Density:** Moderate - code blocks interspersed with conceptual explanations
- **Code vs Prose vs Figures:** Code is essential (HeatingSystem definition, Toaster with allocation, negative control, queries), no figures, explanatory prose with important distinctions
- **Cadence:** Simple progression: introduce allocate concept → define HeatingSystem with perform relationship → add allocation to Toaster definition → negative control (unresolved step) → query allocations and perform relationships → explain results → exercise
- **Consistency:**
  - Follows notebook pattern from Ch1-5
  - Negative control pattern present (unresolved reference in allocation source)
  - Query pattern continues from Ch5-01
  - perform relationship idiom consistent with part/action declarations
- **Data Consistency:**
  - Code shown matches output
  - HeatingSystem perform relationship correct (performs ApplyHeat)
  - find_allocations returns correct allocation: heatAllocation with ends [toastBread.applyHeat, heating]
  - perform_relationships correctly shows HeatingSystem performs ApplyHeat and ToastingSystem performs ToastBread
  - Negative control correctly shows "unresolved reference: ToastBread::undefinedStep" error
  - Exercise pattern consistent (allocates applyWater to brewUnit, both usages not definitions)

### PAGE 26: Chapter 5, Notebook 3 - "port and interface"
- **URL:** http://localhost:3000/interfaces
- **Page Identity:** "Ch5-03: port and interface"
- **Reading Position:** Page 26 of session
- **Visual Cognitive Load:** 4/5 (high) - Multiple code blocks, one significant interconnection diagram, complex concepts
- **Understanding vs Confusion:** Complex but well-scaffolded. Port and interface concepts introduced clearly:
  - Quote from page: "A port gives each component that connection point, and an interface between two ports states which two connection points are joined." Excellent one-sentence explanation of the relationship between ports and interfaces.
  - Quote: "~DurationPort is the conjugate of DurationPort: durationIn receives what a DurationPort sends, the SysML v2 idiom for matching a port to its interface partner." Clear explanation of conjugation and why it's used.
  - Quote: "durationIn and durationOut declare the same underlying port type, which is what makes them a type-compatible pair." Important distinction about type compatibility.
  - Quote about diagram: "The diagram shows control and heating, the two parts of Toaster, each drawn with its own named port -- durationOut on control, durationIn on heating -- connected by the durationInterface port connection. It supports the conclusion that ControlSystem and HeatingSystem are now joined through a single, type-checked connection point between those two specific ports, not a claim about what flows through ApplyHeat itself." Emphasizes diagram's significance.
- **Text Density:** High - multiple code blocks with detailed explanations of port/interface concepts
- **Code vs Prose vs Figures:** Code is essential (DurationPort def, component ports, Toaster with interface, negative control, port_type_mismatches query), one interconnection diagram, extensive prose explaining relationships
- **Figure Description (verified by screenshot):** PlantUML-rendered interconnection diagram showing:
  - Outer box labeled "<<part def>> Toaster"
  - Left inner box labeled "<<part>> control : ControlSystem" with port box showing "durationOut : DurationPort"
  - Right inner box labeled "<<part>> heating : HeatingSystem" with port box showing "durationIn : ~DurationPort" (conjugate indicated by tilde)
  - Horizontal connecting line between ports labeled "<<interface>> durationInterface"
  - Approximately 390x270 pixels
  - Clearly shows component hierarchy, port ownership, conjugation, and interface relationship
  - Uses real sysml-toolkit visualization (not simplified rendering) to preserve port names and conjugation information
- **Cadence:** Complex progression: define DurationPort type → add ports to HeatingSystem and ControlSystem → add interface to Toaster → negative control (unresolved composed part) → query port type compatibility → render and display interconnection diagram using sysml-toolkit → exercise
- **Consistency:**
  - Follows notebook pattern from Ch1-5
  - Negative control pattern present (unresolved reference in interface)
  - Query pattern continues (port_type_mismatches)
  - Uses render_toolkit_interconnection (real visualization) to honor pedagogical point about conjugated ports
- **Data Consistency:**
  - Code shown matches output
  - DurationPort correctly carries ISQ::DurationValue[0..*]
  - ~DurationPort conjugation correctly shown in HeatingSystem
  - DurationPort unconjugated correctly shown in ControlSystem
  - port_type_mismatches returns empty list (compatible types)
  - Diagram rendered correctly showing durationOut-to-durationIn connection
  - Negative control correctly shows "unresolved reference: undefined_receiver" error
  - Exercise pattern consistent (pump and filterUnit with matching ports)

### PAGE 27: Chapter 5 Conclusion
- **URL:** http://localhost:3000/conclusion-4
- **Page Identity:** "Chapter 5: Conclusion"
- **Reading Position:** Page 27 of session
- **Visual Cognitive Load:** 1/5 (very light) - Pure prose, no code or figures, clean three-part structure
- **Understanding vs Confusion:** Excellent summary. Clear, comprehensive recap:
  - Quote from page: "The allocation points at two usages reachable from inside Toaster itself, toastBread.applyHeat and heating; HeatingSystem's own perform relationship shows it is the same kind of action, allocated and performed by type, not a claim that the two are the same occurrence." Excellent clarification of allocation semantics - showing that allocation points to usages, and perform relationship describes the type, not claiming the occurrences are identical.
  - Quote: "The port connection is new structure, not new behavior: it gives the duration signal a place to enter HeatingSystem, but binding it to ApplyHeat::duration itself is later work, once a control policy exists to produce a value." Important clarification of what interfaces do and don't do - they provide structure (connection point) but not behavior (binding).
  - Quote: "The staged conformance check for port-type compatibility (opensysml-query recipe 5) has a real, non-vacuous pair to compare for the first time in this model: it checks that durationIn and durationOut declare related types, which they do." Good example of first non-vacuous use of conformance checking.
  - Clear preview of Chapter 6: introduces nesting of function inside action, abstract carrier, interface point, mechanism selection, measure framing, concrete realization, and stopping judgment.
- **Text Density:** Light - well-spaced sections with clear headings and white space
- **Code vs Prose vs Figures:** Pure prose, no code or figures - appropriate for conclusion page
- **Cadence:** Standard three-part structure: "What we built" (detailed recap) → "What this establishes" (significance and lessons) → "What comes next" (Chapter 6 preview)
- **Consistency:**
  - Matches conclusion format from Ch1, Ch2, Ch3, Ch4
  - Consistent terminology and structure
  - Exercise section follows established pattern
- **Data Consistency:**
  - Accurate descriptions of Chapter 5 constructs (model.find/get, HeatingSystem, allocation, ports, interface, interconnection diagram)
  - Correctly identifies what was built and what remains for later
  - Accurately previews Chapter 6 scope (recursive decomposition, nesting within ApplyHeat)

### PAGE 28: Chapter 6 Overview
- **URL:** http://localhost:3000/index-6
- **Page Identity:** "Chapter 6: Recursive Decomposition - Overview"
- **Reading Position:** Page 28 of session
- **Visual Cognitive Load:** 2/5 (light) - Well-organized overview with clear table of 3 notebooks, moderate text density
- **Understanding vs Confusion:** Clear and sophisticated. Chapter question frames recursion carefully:
  - Quote from page: "This chapter asks: for one branch of ApplyHeat's own decomposition, what does the recursion's stopping rule actually show, and what does it not yet show, one level below where Chapter 5 stopped?" Excellent framing of recursive decomposition and the stopping rule concept.
  - Quote: "The chapter carries one branch of the recursive step through all three layers at the second level, not straight from a level-1 logical grouping to level-2 physical parts, and not by naming a mechanism-specific part before the argument for it exists." Clear explanation of the chapter's approach to recursion.
  - Expected result gives specific, checkable outcomes: perform_relationships shows HeatGenerator performs GenerateHeat, find_allocations shows HeatingAssembly::heatGenAllocation, model.eval shows requirement evaluation, validate_record confirms judgment record validity.
- **Text Density:** Light - well-spaced sections with clear headings
- **Code vs Prose vs Figures:** Pure prose, no code or figures on this overview page
- **Cadence:** Standard overview structure: Purpose → Ingredients (table) → Equipment → Method → Expected result → Experiment
- **Consistency:** Matches overview format from Chapters 1-5
- **Data Consistency:** Expected results accurately describe what will be built (GenerateHeat, HeatGenerator, ResistanceCoil, requirements, allocation, judgment record)

### PAGE 29: Chapter 6, Notebook 1 - "level-2 function and logical carrier"
- **URL:** http://localhost:3000/subsystem-requirements
- **Page Identity:** "Ch6-01: level-2 function and logical carrier"
- **Reading Position:** Page 29 of session
- **Visual Cognitive Load:** 3/5 (moderate) - Multiple code blocks, two diagrams, demonstrates recursive nesting
- **Understanding vs Confusion:** Very clear. Recursive nesting pattern from Ch4-5 repeats at level-2:
  - GenerateHeat nested inside ApplyHeat (mirrors Ch4: ApplyHeat inside ToastBread)
  - HeatGenerator as logical carrier performing GenerateHeat (mirrors Ch5: HeatingSystem performing ApplyHeat)
  - HeatingAssembly specializes HeatingSystem, composes HeatGenerator with usage-level allocation
  - Quote: "This notebook nests GenerateHeat inside ApplyHeat, the same way Chapter 4 nested ApplyHeat inside ToastBread, then gives it a logical carrier of its own, HeatGenerator, one level below HeatingSystem." Clear recursive scaffolding.
- **Text Density:** Moderate - code blocks with clear explanatory prose
- **Code vs Prose vs Figures:** Code essential (GenerateHeat action def, EnergyPort, ApplyHeat with nested generateHeat, HeatGenerator part def, HeatingAssembly), two diagrams (action flow rendering, interconnection intent), explanatory prose
- **Cadence:** Mirrors Ch4-5: define level-2 function → define port type → nest function in parent action → define abstract carrier → specialize parent with new composition → allocation
- **Consistency:** Follows notebook pattern; recursive pattern consistent with prior levels
- **Data Consistency:** perform_relationships shows HeatGenerator performing GenerateHeat; negative control shows unresolved target fails; interconnection diagram confirms allocation endpoints


### PAGE 30: Chapter 6, Notebook 2 - "level-2 physical realization"
- **URL:** http://localhost:3000/second-level
- **Page Identity:** "Ch6-02: level-2 physical realization"
- **Reading Position:** Page 30 of session
- **Visual Cognitive Load:** 4/5 (high) - Complex judgment records (AC-C06, AS-C06) with multiple fields, requirement definitions, two candidate usages, Python record assembly and validation
- **Understanding vs Confusion:** Clear but demanding. Introduces judgment records for requirement framing and mechanism selection:
  - AC-C06: HeatGenerationReq framed as MoP (measure of performance), not MoE (measure of effectiveness)
  - AS-C06: ResistanceCoil selected over gas burner based on control coupling and domain premise
  - Shows how selection requires recorded argument before mechanism-specific names become admissible
  - rated usage satisfies heatGenerationReq (800 W); weak usage fails (400 W)
  - Quote: "the selection is argued from a stated engineering premise, not read off the name of a part built before the argument for it exists"
- **Text Density:** High - extensive judgment record prose, criteria, premises, evidence, challenge sections; Python examples showing validation
- **Code vs Prose vs Figures:** Code essential (requirement def, ResistanceCoil, rated/weak usages, model.eval checks, negative control), extensive structured prose for judgment records, no diagrams
- **Cadence:** Framing judgment → requirement → mechanism selection judgment → concrete part specialization → candidate usages with assertion checking
- **Consistency:** Follows Chapter 2/3 judgment record pattern; new: applies at abstract carrier level rather than top level
- **Data Consistency:** model.find() confirms ControlSystem::durationOut exists; model.eval() validates rated satisfies (True) and weak fails (False); validate_record confirms no errors in both AC-C06 and AS-C06

### PAGE 31: Chapter 6, Notebook 3 - "stopping judgment"
- **URL:** http://localhost:3000/stopping-judgment
- **Page Identity:** "Ch6-03: stopping judgment"
- **Reading Position:** Page 31 of session
- **Visual Cognitive Load:** 5/5 (very high) - Complex asserted_inference judgment record (AI-C06) with all Hawkins fields, real query results (perform_relationships, find_allocations, model.eval), diagram evidence, negative control example
- **Understanding vs Confusion:** Demanding but clear. Introduces stopping rule applied to actual analysis rather than model declaration:
  - AI-C06: asserted_inference checking stopping rule on HeatGenerator branch
  - Shows honest scoping: what is MET (performs GenerateHeat, allocated), PARTIALLY MET (energyIn declared but not wired), PARTIAL EVIDENCE (requirement evaluates but threshold not derived)
  - Negative control: asserted_inference with empty premises fails validation per Hawkins 3.1
  - Quote: "This branch addresses only GenerateHeat's own energy-to-heat conversion... not a claim that Chapter 6 finishes ApplyHeat's full decomposition"
- **Text Density:** Very high - extensive judgment record sections (criteria with three subconditions, premise chain, evidence/rationale paired condition-by-condition)
- **Code vs Prose vs Figures:** Code essential (negative control record, query functions, diagram rendering), extensive structured judgment prose, two diagrams (structure showing HeatingAssembly containment, interconnection showing allocation and port)
- **Cadence:** Negative control → gather real analysis (perform_relationships, find_allocations, model.eval) → build record from evidence → validate and save → compare model tag to Python record
- **Consistency:** Follows asserted_inference pattern from Chapter 4; new: applies stopping rule explicitly (performs, connects, verified) and states what is NOT met
- **Data Consistency:** Model tag confirms AI-C06 attached; validation confirms no errors and premises non-empty; all query results bind directly to rationale; both candidates (rated/weak) evaluated correctly against threshold

### PAGE 32: Chapter 6 - "Conclusion"
- **URL:** http://localhost:3000/conclusion-5
- **Page Identity:** "Chapter 6: Conclusion"
- **Reading Position:** Page 32 of session
- **Visual Cognitive Load:** 2/5 (low) - Pure prose with linked model terms, no code or figures, clear structure
- **Understanding vs Confusion:** Clear and satisfying. Final summary of the chapter:
  - "What we built": detailed narrative summary (GenerateHeat, HeatGenerator, HeatingAssembly, allocation, requirement, selection, candidates)
  - "What this establishes": honest scoping (stops short of full ApplyHeat decomposition; energyIn not wired, HeatingAssembly not composed into full Toaster, other flows not decomposed)
  - "What comes next": Chapter 7 preview (runtime behavior, deliveredEnergy calc, Cycle state machine, power sweep)
  - Quote: "This chapter builds one branch honestly, the same kind of scope choice Chapter 4 made for ApplyHeat itself... it does not claim to finish ApplyHeat's decomposition"
- **Text Density:** Moderate - dense but clearly structured prose
- **Code vs Prose vs Figures:** Pure prose, no code or figures; extensively linked model terminology
- **Cadence:** Summary narrative → honest gap statement → forward-looking preview → exercise mirror pattern
- **Consistency:** Follows conclusion format from Chapters 1-5; same three-section structure
- **Data Consistency:** All named elements (GenerateHeat, HeatGenerator, EnergyPort, HeatingAssembly, etc.) match prior pages; gap statement honest and comprehensive

### PAGE 33: Chapter 7 - "Overview"
- **URL:** http://localhost:3000/index-7
- **Page Identity:** "Chapter 7: Execution and Experiments Overview"
- **Reading Position:** Page 33 of session
- **Visual Cognitive Load:** 2/5 (low) - Pure overview structure with one simple table, no code or figures
- **Understanding vs Confusion:** Clear. Introduces runtime execution and design space validation:
  - Purpose: What does the model do when executed? What does HeatGenerationReq design space deliver?
  - Three notebooks: deliveredEnergy calc, Cycle state machine, parameter sweep
  - Ingredients table clearly maps notebooks to concepts
  - Expected results specific (model.eval returns 67200 J, model.find returns stateUsage, execute_state returns state sequence, sweep marks 600W threshold)
  - Quote: "what does the model actually do when it is executed, and what does the design space HeatGenerationReq opens actually deliver?"
- **Text Density:** Low - standard overview structure with clear short sections
- **Code vs Prose vs Figures:** Pure prose and table; no code or figures on overview page
- **Cadence:** Standard overview structure: Purpose → Ingredients (table) → Equipment → Method → Expected result → Experiment
- **Consistency:** Matches overview format from Chapters 1-6 exactly
- **Data Consistency:** Expected results reference real model queries (model.eval, model.find, execute_state); parameter sweep grounded in requirement from model

### PAGE 34: Chapter 7, Notebook 1 - "delivered energy on the heat generator"
- **URL:** http://localhost:3000/calc-energy
- **Page Identity:** "Ch7-01: delivered energy on the heat generator"
- **Reading Position:** Page 34 of session
- **Visual Cognitive Load:** 3/5 (moderate) - Multiple code blocks, efficiency constraint, deliveredEnergy calc, two constraint verifications
- **Understanding vs Confusion:** Clear. Introduces efficiency and calculation within logical carrier:
  - Efficiency as bounded slot (0 to 1 constraint), not free parameter
  - deliveredEnergy calc: return = power * duration * efficiency
  - efficiency resolved from concrete usage's own bound value, not passed as parameter
  - rated's efficiency set to 0.7 (assumed value for worked example)
  - model.eval query returns 67200 J from 800W * 120s * 0.7
  - model.verify_constraint shows bound holds for 0.7, fails for 1.5
  - Quote: "efficiency is not one of its parameters: it is this carrier's own bound feature, resolved from whichever concrete usage the calc is queried through"
- **Text Density:** Moderate - code blocks with clear explanatory prose
- **Code vs Prose vs Figures:** Code essential (efficiency slot, deliveredEnergy calc, model.find, model.eval, verify_constraint with hold/fail examples), negative control, probe example
- **Cadence:** Define efficiency slot and bounds → define deliveredEnergy calc → add to HeatGenerator → add efficiency to rated → verify with model.eval → verify constraints (hold case and fail case)
- **Consistency:** Follows notebook pattern; constraint checking mirrors Chapter 4/5 pattern
- **Data Consistency:** model.find confirms deliveredEnergy loads as calcUsage; verify_constraint holds for 0.7, fails for 1.5; model.eval returns 67200 J; negative control shows unresolved reference fails

### PAGE 35: Chapter 7, Notebook 2 - "the toaster's own operating cycle"
- **URL:** http://localhost:3000/state-traces
- **Page Identity:** "Ch7-02: the toaster's own operating cycle"
- **Reading Position:** Page 35 of session
- **Visual Cognitive Load:** 4/5 (high) - State machine definition, six transitions, negative controls, tool gap demonstration, multiple state traces
- **Understanding vs Confusion:** Clear. Introduces state machines and execution:
  - Cycle with idle (entry), heating (do action generateHeat), ready, cancelled states
  - Transitions: Start→heating, Finish→ready, Cancel→cancelled, ready→idle, cancelled→idle (no accept)
  - ToastingSystem exhibits Cycle; Toaster inherits it
  - model.find confirms cycle is stateUsage on ToastingSystem
  - Three execute_state traces: (Start,Finish)→[idle,heating,ready,idle]; (Start,Cancel)→[idle,heating,cancelled,idle]; (Start,Finish,Start,Finish) cycles twice
  - Tool gap: typo'd trigger (Strat vs Start) loads without error; tutorial's language_gap_findings catches it
  - Quote: "a trace like this is specification analysis, not a simulation of behavior"
- **Text Density:** Moderate-high - state definitions, transitions, traces, tool gap explanation
- **Code vs Prose vs Figures:** Code essential (state/transition defs, negative control, typo probe, model.find, execute_state), one diagram (state flow), tool gap analysis
- **Cadence:** Define states → define transitions (with/without accept) → add to ToastingSystem → negative control → tool gap demonstration → model.find and execute_state traces
- **Consistency:** First state machine; follows model building pattern
- **Data Consistency:** model.find confirms stateUsage; execute_state traces match transition table; negative control shows undefined target fails; tool gap probe shows typo loads but tutorial guard flags it

### PAGE 36: Chapter 7, Notebook 3 - "sweeping the design space HeatGenerationReq opens"
- **URL:** http://localhost:3000/param-sweep
- **Page Identity:** "Ch7-03: sweeping the design space HeatGenerationReq opens"
- **Reading Position:** Page 36 of session
- **Visual Cognitive Load:** 3/5 (moderate) - Parameter sweep with numpy/matplotlib, model.eval at each point, threshold extracted from model, one plot output
- **Understanding vs Confusion:** Clear. Design space exploration grounded in model queries:
  - HeatGenerationReq's 600W threshold read from model source text (not invented)
  - deliveredEnergy swept across power range (500-1200W) via model.eval
  - Duration (120s) and efficiency (rated's bound 0.7) from model
  - Plot shows curve with vertical line marking 600W threshold
  - Results: 50.4 kJ at threshold, 67.2 kJ at rated 800W
  - Quote: "it sweeps deliveredEnergy's power argument across a range, evaluates the relation at each point through the model, and marks the requirement's own threshold on the result, instead of an energy figure invented for the plot"
- **Text Density:** Moderate - code, analysis, plot generation, and commentary
- **Code vs Prose vs Figures:** Code essential (ApiIndex query, numpy sweep, matplotlib plot), one matplotlib figure output, detailed commentary on what is/isn't derived
- **Cadence:** Read threshold from model → negative control → numpy sweep with model.eval → matplotlib plot with threshold line → print results
- **Consistency:** Follows notebook query pattern; integrates Ch6 requirement with Ch7 calc
- **Data Consistency:** Threshold (600W) extracted from model; sweep computed via model.eval; plot marks requirement from model; results reported (50.4kJ, 67.2kJ)

### PAGE 37: Chapter 7 - "Conclusion"
- **URL:** http://localhost:3000/conclusion-6
- **Page Identity:** "Chapter 7: Conclusion"
- **Reading Position:** Page 37 of session
- **Visual Cognitive Load:** 2/5 (low) - Pure prose, linked model terms, standard conclusion structure
- **Understanding vs Confusion:** Clear and satisfying. Chapter 7 integration summary:
  - "What we built": deliveredEnergy calc (bounded 0-1 efficiency, not free parameter), Cycle state machine (heating with do GenerateHeat, ready/cancelled transitions back to idle), parameter sweep (power input swept via model.eval, threshold read from model)
  - "What this establishes": efficiency bound is real constraint (verified to hold/fail), machine actually cycles (traces show specification analysis), tool gap: trigger resolution not implemented
  - "What comes next": Chapter 8 will verify satisfaction via verify_satisfaction()
  - Exercise mirrors pattern: deliveredMass, BrewCycle, sweep
- **Text Density:** Low - dense but clearly structured prose
- **Code vs Prose vs Figures:** Pure prose, no code or figures; extensively linked model terminology
- **Cadence:** Summary of what was built → what that establishes → forward look to Chapter 8 → exercise pattern
- **Consistency:** Follows conclusion format from Chapters 1-6
- **Data Consistency:** All named elements match prior pages; forward reference to Chapter 8 (Checking and Revision) confirms curriculum progression

### PAGE 38: Chapter 8 - "Overview"
- **URL:** http://localhost:3000/index-8
- **Page Identity:** "Chapter 8: Checking and Revision Overview"
- **Reading Position:** Page 38 of session
- **Visual Cognitive Load:** 2/5 (low) - Pure overview with one table, no code or figures
- **Understanding vs Confusion:** Clear introduction to formal verification:
  - Different question than Ch3/Ch6: Does lemma hold for EVERY value (formal proof) vs specific values (point evaluation)?
  - Three notebooks: assert constraint, proof vs point evaluation, stale detection
  - Key distinction: parameter sweep samples values; model checking proves entire domain
  - Expected: verify_holds() proves universally via Z3; shows violations and inconclusive cases; verify_satisfaction() unchanged
  - Quote: "simulation explores; a proof, when it succeeds, covers the whole space it is stated over"
- **Text Density:** Low-moderate - standard overview structure with clear explanations
- **Code vs Prose vs Figures:** Pure prose and table; no code or figures on overview page
- **Cadence:** Standard overview: Purpose → Ingredients (table) → Equipment → Method → Expected result → Experiment
- **Consistency:** Matches overview format from Chapters 1-7
- **Data Consistency:** Three notebooks clearly described; expected results specific and concrete (model.find, verify_holds, violations, inconclusive, check_stale)

### PAGE 39: Chapter 8, Notebook 1 - "assert constraint"
- **URL:** http://localhost:3000/assert-constraint-def
- **Page Identity:** "Ch8-01: assert constraint"
- **Reading Position:** Page 39 of session
- **Visual Cognitive Load:** 4/5 (high) - Constraint definition with extensive doc comment, unbound usage setup, negative control
- **Understanding vs Confusion:** Clear but demanding. Introduces formal verification setup:
  - deliveredEnergyBoundedBySupply: real-arithmetic lemma (power*duration*efficiency <= power*duration)
  - heatGenCheck: unbound HeatGenerator usage (efficiency and power free)
  - heatGenCheckDuration: separate attribute (duration free)
  - Constraint: antecedent restates efficiencyBounded; consequent restates deliveredEnergy definition
  - Hand-restated because toolchain cannot compose assertions or reason through chained calcs (D-030, D-031)
  - model.find and model.query confirm constraint in model
  - Quote: "this toolchain's Z3 backend does not compose two separately declared assert constraints... and cannot reason through a chained calc invocation"
- **Text Density:** High - constraint definition with extensive doc, model queries
- **Code vs Prose vs Figures:** Code essential (unbound usage, constraint def with doc, model.find, model.query), one diagram (structure), negative control
- **Cadence:** Define unbound usage → define free duration attribute → state constraint → confirm with model.find and model.query → negative control
- **Consistency:** Follows notebook pattern; introduces model-checking construct
- **Data Consistency:** model.find returns constraintUsage; model.query finds it among 3 ConstraintUsage elements; negative control shows undefined attribute fails

### PAGE 40: Chapter 8, Notebook 2 - "proof versus point evaluation"
- **URL:** http://localhost:3000/violation-witness
- **Page Identity:** "Ch8-02: proof versus point evaluation"
- **Reading Position:** Page 40 of session
- **Visual Cognitive Load:** 5/5 (very high) - Universal proof vs point evaluation, three companion models, verdict types, judgment record with extensive counterevidence
- **Understanding vs Confusion:** Clear but demanding. Contrasts verification approaches:
  - verify_satisfaction(): evaluates three existing claims at their current fixed values
  - verify_holds(): proves deliveredEnergyBoundedBySupply for every value via Z3
  - Three companion restatements: positive (satisfied), negative (violated), weakened (undecided)
  - Undecided shows genuine Z3-found witness (e.g., efficiency=0, power=0, duration=1)
  - AS-C08 ReviewRecord with extensive counterevidence stating what proof does NOT establish
  - Quote: "a proof is only worth trusting if the same machinery can also report a real violation"
- **Text Density:** Very high - extensive code, three proofs, judgment record with all eight fields
- **Code vs Prose vs Figures:** Code essential (verify_satisfaction, three companion files, verify_holds variants, ReviewRecord assembly), no figures
- **Cadence:** verify_satisfaction baseline → verify_holds positive proof → negative violation witness → undecided weakened case → ReviewRecord assembly with counterevidence
- **Consistency:** Follows ReviewRecord pattern from prior chapters
- **Data Consistency:** All three verdicts real (satisfied, violated, undecided); model tag confirms; record validates with no errors; engineering_conclusion="supported"

### PAGE 41: Chapter 8, Notebook 3 - "stale record detection"
- **URL:** http://localhost:3000/revision-flow
- **Page Identity:** "Ch8-03: stale record detection"
- **Reading Position:** Page 41 of session
- **Visual Cognitive Load:** 2/5 (low) - Straightforward staleness check against content_hash
- **Understanding vs Confusion:** Very clear. Demonstrates safeguard against stale records:
  - check_stale() compares ReviewRecord's content_hash against current model source
  - Loads AS-C08 from notebook 02, confirms current
  - Loosens lemma bound (1.0 → 1.2), model still parses, record now stale
  - Content-hash approach catches any model change, not just the target
  - Negative control: empty identifier fails validation outright
- **Text Density:** Low - simple demonstration with direct output
- **Code vs Prose vs Figures:** Code essential (load_record, check_stale, bound loosening), negative control
- **Cadence:** Load record → verify current → loosen bound → detect staleness
- **Consistency:** Follows check_stale pattern
- **Data Consistency:** check_stale returns False then True; model parses both; exact bound change shown

### PAGE 42: Chapter 8 - "Conclusion"
- **URL:** http://localhost:3000/conclusion-7
- **Page Identity:** "Chapter 8: Conclusion"
- **Reading Position:** Page 42 of session
- **Visual Cognitive Load:** 2/5 (low) - Pure prose, standard conclusion structure
- **Understanding vs Confusion:** Very clear. First genuinely model-checked property:
  - verify_holds() proves lemma for every value vs point evaluation
  - Hand-restated (not solver-checked) due to toolchain limits (D-030/D-031)
  - Three-way distinction: satisfied, violated, or undecided
  - verify_satisfaction() unchanged (point evaluation); verify_holds() new (universal proof)
  - All three verdict types confirmed and distinguished throughout chapter
  - conformance.report()'s satisfaction-claims-evaluated passes on ch08 fixture
- **Text Density:** Low - clear prose summary
- **Code vs Prose vs Figures:** Pure prose; no code or figures
- **Cadence:** Summary of deliveredEnergyBoundedBySupply → what it establishes → forward to Chapter 9 → exercise
- **Consistency:** Follows conclusion format from prior chapters
- **Data Consistency:** All technical details match Ch8-01, 02, 03; forward reference to Chapter 9 (coverage table)

### PAGE 43: Chapter 9 - "Overview"
- **URL:** http://localhost:3000/index-9
- **Page Identity:** "Chapter 9: Coverage and Sufficiency - Overview"
- **Reading Position:** Page 43 of session
- **Visual Cognitive Load:** 2/5 (low) - Dense prose with one simple table. No diagrams, code, or complex figures
- **Understanding vs Confusion:** Very clear structure. Purpose explicitly states chapter goal: "whether the model's own requirements have actually been checked, not just declared." Three notebooks clearly described. Method section is lengthy but comprehensible, explaining each notebook's purpose with specific technical details (e.g., coverage report joining requirement usages vs satisfy relationships, polarity-blind join bug, Hawkins sufficiency applied to real records, staleness detection at scale)
- **Text Density:** Very high - extended paragraphs throughout Purpose, Method, Expected result sections. Purpose and Method each span multiple long paragraphs. Minimal white space for scanning.
- **Code vs Prose vs Figures:** Prose dominant. Single table (Ingredients) showing three notebooks with names and one-line concept descriptions. No code blocks, no diagrams, no plots, no visualizations.
- **Figure Description:** One-row Ingredients table with three notebook entries. Column headers: Notebook, Concept. Rows: (01 - requirement coverage | Build real coverage report by joining requirement usages vs satisfy relationships), (02 - evidence sufficiency | Apply Hawkins' sufficiency to two real ReviewRecords from Ch6 and Ch8), (03 - stale detection at scale | Check several tracked records against real model before/after real edit)
- **Cadence:** Purpose (goal: verify requirements checked, not declared) → Ingredients (three notebooks) → Equipment (docs/setup.md reference) → Method (detailed explanation of what each notebook does, specific findings, references to heatGenerationReq/timely coverage, AS-C06/AS-C08 records, content_hash staleness approach) → Expected result (summary of what each notebook will show) → Experiment (exercise reference)
- **Consistency:** Follows standard overview pattern from Ch8, Ch7, Ch6. Same section structure, same flow from Purpose through Experiment. Introduction to chapter's scope before diving into notebooks
- **Data Consistency:** All three notebooks real and consistent with chapter setup. Model references accurate (models/ch08-cumulative.sysml queried in all three). All requirement names correct (timely, heatGenerationReq). Record names correct (AS-C06, AS-C08). Method details match pattern established in prior chapters


### PAGE 44: Chapter 9, Notebook 1 - "requirement coverage"
- **URL:** http://localhost:3000/requirement-coverage
- **Page Identity:** "Ch9-01: requirement coverage"
- **Reading Position:** Page 44 of session
- **Visual Cognitive Load:** 4/5 (high) - Complex joins with multiple code blocks, nested control flow, substantial output to interpret. Code-heavy notebook with polarity-blind vs polarity-aware join contrast
- **Understanding vs Confusion:** Dense but clear progression. Demonstrates requirement coverage concept step by step: (1) load model and verify negative control, (2) extract raw requirements and satisfy relationships using model.query() and get_satisfy_relationships(), (3) build coverage join splitting by polarity and subject presence, (4) print coverage table showing heatGenerationReq covered (rated positive, weak negative) and timely not covered (slow negative only). Polarity-blind join mistake is very clear and well-explained as the exact bug the repository's requirement_coverage() helper carried before this chapter. Three-way distinction (positive claims, negative claims, verify objectives without subject) is explicit. Quote: "a positive claim someone actually made, not merely a claim of any kind"
- **Text Density:** High - Mix of explanatory prose (understanding the gap, polarity explanation, caveats about Chapter 10) and substantial code blocks with outputs
- **Code vs Prose vs Figures:** Heavily code-focused with six major code blocks (load model, negative control, extract surface, build join, polarity-blind mistake, repository helper). All outputs shown directly in code blocks. No figures, diagrams, or plots
- **Cadence:** Model load → negative control (assert satisfy to undeclared requirement fails) → API extraction (find_requirements, get_satisfy_relationships) → coverage join with polarity split → output coverage table (requirements=[heatGenerationReq, timely], claims count=4 but effective claims=3 because TimelyToastTest is verification-case objective with no subject) → polarity-blind join mistake (wrongly counts slow's failing claim as coverage for timely) → repository requirement_coverage() helper confirms polarity-aware approach → caveat about Chapter 10's energyConservationReq (False for different structural reason)
- **Consistency:** Follows tutorial notebook pattern (setup, extract, build, verify, caveat). Same structure as other working notebooks (Ch8-01, Ch8-02)
- **Data Consistency:** All model references correct (models/ch08-cumulative.sysml, ch08 fixture, ch09 exercise). Requirement names exact (ToasterDemo::heatGenerationReq, ToasterDemo::timely). Candidate names exact (rated, weak, slow). Coverage table output exact: heatGenerationReq covered=True with [rated] and [weak], timely covered=False with [] and [slow]. Four satisfy relationships enumerated correctly with verify objective present. All assertion checks pass


### PAGE 45: Chapter 9, Notebook 2 - "evidence sufficiency"
- **URL:** http://localhost:3000/evidence-completeness
- **Page Identity:** "Ch9-02: evidence sufficiency"
- **Reading Position:** Page 45 of session
- **Visual Cognitive Load:** 4/5 (high) - Two reconstructed ReviewRecords analyzed with Hawkins' sufficiency check. Code blocks loading records, validating, extracting fields. Substantiveness assessment of counterevidence and residual_uncertainties
- **Understanding vs Confusion:** Complex but clear progression. Demonstrates sufficiency check step by step: (1) load model, (2) negative control (record with empty counterevidence fails validation), (3) load AS-C06 (mechanism-selection judgment from domain premise, Chapter 6), (4) load AS-C08 (Z3-proved lemma, Chapter 8), (5) validate both cleanly, (6) compare premises (AS-C06 has two substantive premises; AS-C08 has none but claim is narrowly deductive not inductive), (7) word-count analysis showing AS-C06 counterevidence 78 words with specifics, AS-C08 133 words naming toolchain limits and failed edit attempts, (8) placeholder example passing structural checks but failing sufficiency reading, (9) caveat distinguishing sufficiency (well-argued when written) from staleness (may go stale later)
- **Text Density:** High - Prose explaining Hawkins' sufficiency idea, deductive vs inductive claims, structural vs content-based checking. Code blocks with outputs
- **Code vs Prose vs Figures:** Code-dominant (5+ blocks: model load, negative control, AS-C06 load+validate, AS-C08 load+validate, premises check, word-count analysis, placeholder record). Outputs shown inline. No figures or diagrams
- **Cadence:** Model setup → negative control → load AS-C06 (mechanism-selection) → load AS-C08 (Z3-proof) → premises comparison → word-count analysis of counterevidence/residual_uncertainties → placeholder record showing false positive → distinguish substantiveness from non-emptiness → sufficiency vs staleness caveat
- **Consistency:** Follows tutorial notebook pattern. Same structure as other working notebooks. Integrates concepts from Ch6 and Ch8
- **Data Consistency:** Record identifiers exact (AS-C06 from chapters/ch06-recursive-decomp/02-second-level.ipynb, AS-C08 from chapters/ch08-checking/02-violation-witness.ipynb). Model references exact (models/ch08-cumulative.sysml). Field extracts exact: AS-C06 disposition=pending conclusion=undetermined; AS-C08 disposition=pending conclusion=supported. Word counts accurate (78 for AS-C06 counterevidence, 133 for AS-C08 counterevidence, 26 for AS-C06 residual_uncertainties, 101 for AS-C08). Placeholder record passes validate_record but fails substantiveness reading


### PAGE 46: Chapter 9, Notebook 3 - "stale detection at scale"
- **URL:** http://localhost:3000/stale-detection
- **Page Identity:** "Ch9-03: stale detection at scale"
- **Reading Position:** Page 46 of session
- **Visual Cognitive Load:** 3/5 (moderate) - Multiple records checked at once. Before/after staleness comparison. Diff output between models. Code-heavy but straightforward staleness mechanism
- **Understanding vs Confusion:** Clear progression. Demonstrates check_stale() applied to multiple records simultaneously (not just one): (1) load model and records, (2) negative control (empty identifier fails validation), (3) load AS-C06 (written against ch06-cumulative) and AS-C08 (written against ch08-cumulative), (4) check staleness before any edit: AS-C06 stale=True, AS-C08 stale=False, (5) explain AS-C06 staleness (real growth from Chapter 7 partly overtook gap named in its counterevidence: efficiency, efficiencyBounded, deliveredEnergy added to HeatGenerator, but Joule relation and response-time comparisons still unmodeled), (6) apply unrelated edit (loosen deliveredEnergyBoundedBySupply's bound 1.0→1.2), (7) check staleness after edit: both stale=True, (8) explain difference: AS-C06 stale for substantive reason (real growth), AS-C08 stale from whole-file content_hash catching different construct than its residual named
- **Text Density:** High - Prose explaining staleness reasons, diff showing efficiency lines added, code blocks with before/after outputs
- **Code vs Prose vs Figures:** Code-dominant (5+ blocks: load, negative control, AS-C06 load+validate, AS-C08 load+validate, staleness check, diff extraction, edit + re-check). Diff output showing 18 added lines mentioning efficiency (attribute, assert constraint, doc). No figures or diagrams
- **Cadence:** Model load → negative control → load two records → staleness before edit (AS-C06 stale, AS-C08 current) → explain AS-C06 staleness via diff showing Chapter 7 additions → loosen different element (deliveredEnergyBoundedBySupply vs HeatGenerator's efficiencyBounded/deliveredEnergy) → staleness after edit (both stale) → explain two different histories
- **Consistency:** Builds on Ch8-03 (single record staleness) and Ch9-02 (record analysis). Follows notebook pattern
- **Data Consistency:** Record identifiers exact (AS-C06, AS-C08). Model comparisons exact (ch06-cumulative vs current ch08-cumulative). Staleness states accurate: before=(True, False), after=(True, True). Diff output exact: 18 added lines mention efficiency, examples shown (attribute efficiency, assert constraint efficiencyBounded, doc comment). Edit change shown exactly: "1.0" → "1.2". Assertion checks pass


### PAGE 47: Chapter 9 - "Conclusion"
- **URL:** http://localhost:3000/conclusion-8
- **Page Identity:** "Chapter 9: Conclusion"
- **Reading Position:** Page 47 of session
- **Visual Cognitive Load:** 1/5 (very low) - Pure prose conclusion, standard structure, no code or figures
- **Understanding vs Confusion:** Very clear summary structure. "What we built" explains three notebooks (coverage report finding real gap + fixing polarity-blind bug, sufficiency check on two records, staleness check on two records together). "What this establishes" details real gap found (timely never positively claimed, only verified objective named it), bug fixed (requirement_coverage() was polarity-blind, now matches polarity-aware join), sufficiency distinction (non-empty ≠ substantive; AS-C06 undetermined, AS-C08 supported), staleness histories (AS-C06 overtaken by Chapter 7 efficiency additions; AS-C08 caught by whole-file content_hash on unrelated edit). "What comes next" forward reference to Chapter 10's traceability graph. "Exercise" references exercises/ch09/exercise.ipynb for user's own model
- **Text Density:** Moderate-high - Dense prose paragraphs with specific technical details and record field references
- **Code vs Prose vs Figures:** Pure prose. No code blocks, no figures, no diagrams
- **Cadence:** What we built (three notebooks querying ch08 directly) → What this establishes (three findings: coverage gap, polarity bug fix, staleness histories) → What comes next (Chapter 10 traceability graph) → Exercise reference
- **Consistency:** Follows conclusion format from prior chapters (Ch8 Conclusion, Ch7 Conclusion). Same structure and depth
- **Data Consistency:** All technical details match prior chapters exactly: record names (AS-C06, AS-C08), requirement names (heatGenerationReq, timely, nominal), model references (ch08-cumulative.sysml), Chapter 7 changes (efficiency, efficiencyBounded, deliveredEnergy added to HeatGenerator), file elements (content_hash, residual names efficiencyBounded/deliveredEnergy vs deliveredEnergyBoundedBySupply)


### PAGE 48: Chapter 10 - "Overview"
- **URL:** http://localhost:3000/index-10
- **Page Identity:** "Chapter 10: Traceability and Sign-off - Overview"
- **Reading Position:** Page 48 of session
- **Visual Cognitive Load:** 3/5 (moderate) - Complex technical overview with detailed traceability concepts, graph building, gap remediation, three judgment records, synthesis approach
- **Understanding vs Confusion:** Very clear structure. Purpose states: build traceability graph (two of three requirements), synthesize three real judgment records into ledger, assemble inputs for sign-off decision (bounded, honest synthesis of what is established/not/remains), does not perform sign-off itself (human act). Explains this is tutorial's final chapter. Ingredients table shows three notebooks (01: traceability graph finding gap + remediation, 02: judgment ledger of three records, 03: engineering synthesis and why it's not sign-off). Method section very detailed: (1) notebook 01 reads requirement definitions, traces allocation/realization chains, joins against requirement_coverage(); heatGenerationReq traces to opposite-polarity evidence (rated, weak); timely stops short (no positive claim); finds deliveredEnergyBoundedBySupply tied to no requirement, closes gap by subsetting it to EnergyConservationReq (without assert satisfy); (2) notebook 02 reconstructs AS-C06, AS-C08, AI-C06 (re-verified against originals), reads kind/disposition/residual; (3) notebook 03 synthesizes into AI-C10 (asserted_inference) with literally other notebooks' findings as premises. Expected result shows graph outputs, three record dispositions (all pending, two undetermined + one supported), synthesis record AI-C10 validates cleanly but states plainly it is not sign-off
- **Text Density:** Very high - Dense prose paragraphs with specific model element references, record names, technical mechanisms
- **Code vs Prose vs Figures:** Pure prose. One Ingredients table showing three notebooks. No code blocks, no diagrams, no figures
- **Cadence:** Purpose (goal and final chapter statement) → Ingredients (3 notebooks) → Equipment (setup reference) → detailed Method (traceability mechanism, gap closure, three records, synthesis) → Expected result (outputs from all three) → Experiment reference
- **Consistency:** Follows chapter overview pattern from Ch9, Ch8. Same structure and detail depth
- **Data Consistency:** All technical details exact: record names (AS-C06, AS-C08, AI-C06, AC-C10, AI-C10), requirement names (heatGenerationReq, timely, EnergyConservationReq, energyConservationReq), model element (deliveredEnergyBoundedBySupply), record types (asserted_solution, asserted_inference, asserted_context), disposition="pending", engineering_conclusion values ("undetermined", "supported"), negative control confirms assert satisfy fails, requirement_coverage() covered=False by design for energyConservationReq, file references exact (models/ch08-cumulative.sysml, decisions/pass4-run-009.md, docs/case-studies/, check_predecessor_containment())


### PAGE 49: Chapter 10, Notebook 1 - "traceability graph"
- **URL:** http://localhost:3000/traceability-graph
- **Page Identity:** "Ch10-01: traceability graph"
- **Reading Position:** Page 49 of session
- **Visual Cognitive Load:** 5/5 (very high) - Extremely code-heavy notebook (71K+ characters). Complex model queries, allocation/realization chain traversal, gap closure remediation, multiple negative controls, AC-C10 judgment record validation
- **Understanding vs Confusion:** Clear progression but very technical. Purpose: trace traceability from functional intent through allocation/realization to verification evidence (SEBoK definition cited). Chapter 9's coverage report joins one pair of surfaces; this extends to full chain. Key finding: deliveredEnergyBoundedBySupply (Chapter 8's Z3-proved lemma) tied to no requirement at all - inverse failure mode Douglas names (unjustified widget vs disconnected evidence). Remediation: EnergyConservationReq/energyConservationReq ties lemma by subsetting its required constraint directly from within requirement's body (no explicit subject declaration, inherits Anything as default). Negative control: assert satisfy would fail on this requirement (because its required constraint never references subject). AC-C10 judgment record validates cleanly (asserted_context, spec-legitimate subsetting, motivation genuine but identified retroactively, tie rests on structural detection alone, requirement_coverage() covered=False is correct/expected)
- **Text Density:** Very high - Dense prose introducing traceability concept, detailed remediation explanation, code blocks interspersed throughout
- **Code vs Prose vs Figures:** Heavily code-focused with extensive blocks showing model query operations, allocation/realization chain traversal, API-JSON feature extraction, gap closure mechanisms, negative control implementations, record validation. Multiple outputs shown inline. No figures or diagrams
- **Cadence:** Introduction (requirement traceability definition) → model load → allocation naming negative control (undeclared feature fails) → trace requirements through chains → query declared subjects → find disconnected proof (deliveredEnergyBoundedBySupply) → remediation by subsetting into EnergyConservationReq → negative control (assert satisfy would error) → requirement_ties() confirmation before/after → AC-C10 validation → exercise reference
- **Consistency:** Follows tutorial notebook pattern. Builds on Ch9-01's requirement_coverage() and extends it to full traceability
- **Data Consistency:** Record identifiers exact (AC-C10, asserted_context), requirement names exact (EnergyConservationReq, energyConservationReq, heatGenerationReq, timely), model elements exact (deliveredEnergyBoundedBySupply, Anything), technical concepts correct (subject feature in API-JSON, subsetting mechanism, require constraint, covered=False by design), file references exact (docs/case-studies/2026-09-30-energy-conservation-requirement-tie.md)


### PAGE 50: Chapter 10, Notebook 2 - "judgment ledger"
- **URL:** http://localhost:3000/judgment-synthesis
- **Page Identity:** "Ch10-02: judgment ledger"
- **Reading Position:** Page 50 of session
- **Visual Cognitive Load:** 4/5 (high) - Code-heavy notebook with multiple ReviewRecord reconstructions, validation, and ledger analysis. Three records loaded and analyzed in parallel
- **Understanding vs Confusion:** Clear progression. Purpose: build judgment ledger over three real records (AS-C06, AS-C08, AI-C06). Intro explains no central registry but toaster.judgment_store now supplies persisted storage (save_record/load_record pattern). Negative control: asserted_inference without premises fails Hawkins SS3.1. Loads three records: AS-C06 (mechanism-selection asserted_solution from Ch6), AS-C08 (Z3-proof asserted_solution from Ch8), AI-C06 (stopping judgment asserted_inference from Ch6). Ledger reports kind, disposition, record_kind, engineering_conclusion, residual_uncertainties. Key finding: two undetermined (AS-C06, AI-C06), one supported but narrowly (AS-C08). Quote: "not a tally of how many records exist, but a reading of how much of that count is actually load-bearing"
- **Text Density:** High - Dense prose interspersed with code blocks showing model loading, record validation, and ledger analysis
- **Code vs Prose vs Figures:** Code-dominant with four major code blocks (negative control, AS-C06 load+validate, AS-C08 load+validate, AI-C06 load+validate, ledger loop). Ledger output table shown inline. No figures or diagrams
- **Cadence:** Introduction (no central registry, judgment_store solution) → negative control (incomplete inference fails Hawkins requirement) → load AS-C06 (asserted_solution, mechanism selection) → load AS-C08 (asserted_solution, Z3-proof) → load AI-C06 (asserted_inference, stopping judgment, child claims supporting parent) → build ledger table (kind, disposition, record_kind, engineering_conclusion, residual_uncertainties) → analysis of three records (two undetermined, one supported narrowly) → exercise reference
- **Consistency:** Follows tutorial notebook pattern. Builds on Ch9-02's record analysis. Combines with notebook 01's traceability graph for Ch10's synthesis
- **Data Consistency:** Record identifiers exact (AS-C06, AS-C08, AI-C06), record types exact (asserted_solution, asserted_solution, asserted_inference), disposition="pending" for all three, record_kind="worked_example" for all three, engineering_conclusion values exact (undetermined, supported, undetermined), residual_uncertainties exact quotes showing substantive details (trade study revisit for AS-C06, physical checking missing for AS-C08, further decomposition open for AI-C06), premise fields exact (four identifiers for AI-C06: AC-C06, AS-C06, AS-C03, AI-C04)


### PAGE 51: Chapter 10, Notebook 3 - "engineering synthesis"
- **URL:** http://localhost:3000/engineering-signoff
- **Page Identity:** "Ch10-03: engineering synthesis"
- **Reading Position:** Page 51 of session
- **Visual Cognitive Load:** 5/5 (very high) - Extremely comprehensive and intricate notebook synthesizing two prior notebooks into one master judgment record. Methodical assembly of all judgment record fields with extensive prose and code
- **Understanding vs Confusion:** Crystal clear distinction stated at outset: completed traceability graph and judgment ledger are NOT sign-off; sign-off is human, accountable act; record shows inputs to decision, cannot make decision itself. AI-C10 (asserted_inference, not asserted_solution) synthesizes five premises from prior notebooks (notebook 01's coverage/tie findings including discoveredEnergyBoundedBySupply now tied to energyConservationReq by subsetting; three ledger records AS-C06/AS-C08/AI-C06; AC-C10 framing the tie). Negative controls show prohibition and exemption (cannot have empty counterevidence; can have empty subject_ref only when premises non-empty for asserted_inference). Record methodically builds: claim (synthesis gives basis for exercising sign-off judgment), scope (three traced chains, three records, AC-C10), criteria (bidirectional/one-sided/no evidence distinction, proof-to-requirement connection), premises (five full summaries), assumption_refs (cycleTime remains unset), evidence_refs (three notebooks' outputs), rationale (strongest traced, weakest uncovered, strongest proof now tied structurally by design decision, not automatically), counterevidence (physical realization unchecked, residuals named, hand-restated lemma proof, retroactively-identified requirement), residual_uncertainties (mechanism selection revisit, restatement update manual, cycleTime derivation open, retroactive requirement rule open). Final disposition="pending" (rule SA-7 applies), engineering_conclusion="undetermined" (two of three original requirements state different levels)
- **Text Density:** Extremely high - Dense technical prose throughout, extensive field descriptions, multiple output blocks
- **Code vs Prose vs Figures:** Extremely code-heavy with methodical record construction, multiple negative controls, comprehensive field assignments, validation blocks. Extensive output showing exact premise/criteria/rationale/counterevidence text. No figures or diagrams
- **Cadence:** Opening distinction (not sign-off, cannot perform it) → negative control (empty counterevidence rejected) → load coverage/ties from notebook 01 → cite AC-C10 judgment → cite notebook 02's ledger → build claim → build scope → build criteria → build premises (five items: coverage/ties + three records + AC-C10) → build assumption_refs → build evidence_refs → build rationale → build counterevidence → build residual_uncertainties → assemble AI-C10 record → validate cleanly → confirm disposition="pending" and engineering_conclusion="undetermined" → cite AGENTS.md on strong emergence → final synthesis of three notebooks → exercise reference
- **Consistency:** Follows judgment record construction pattern established in prior chapters, extended to maximum scale. Implements toaster-review-protocol for most complex case (synthesis record, not original claim)
- **Data Consistency:** All outputs exact and verified against real notebook results, all premise cross-references exact (AC-C06, AS-C06, AS-C08, AI-C06, AC-C10), all coverage/tie findings exact from notebook 01, all four assumption/evidence/premise/residual fields fully populated with substantive, specific content, assertion checks confirm disposition="pending" and engineering_conclusion="undetermined" preserved, disposition=accepted explicitly forbidden (AGENTS.md SA-7 rule, no mechanized enforcement shown for principle), strong emergence concept invoked from AGENTS.md to explain what synthesis cannot anticipate


### PAGE 52: Chapter 10 - "Conclusion" (FINAL PAGE)
- **URL:** http://localhost:3000/conclusion-9
- **Page Identity:** "Chapter 10: Conclusion"
- **Reading Position:** Page 52 of session (FINAL PAGE OF TUTORIAL)
- **Visual Cognitive Load:** 1/5 (very low) - Pure prose conclusion, clear structure, standard format
- **Understanding vs Confusion:** Very clear. Tutorial summary: one new element (EnergyConservationReq) added only because traceability analysis found gap it closes. Three notebooks: (1) traceability graph traces two of three requirements differently, finds Z3-proved deliveredEnergyBoundedBySupply tied to no requirement, closes gap by subsetting into energyConservationReq (no assert satisfy); (2) judgment ledger of three records shows two undetermined, one narrowly supported; (3) synthesis AI-C10 states graph+ledger give honest basis for sign-off judgment but are NOT sign-off themselves. Key insight repeated: "completed traceability graph and judgment ledger are not sign-off itself. Sign-off is a human, accountable act." Final statement: tutorial teaches HOW to build traceable, honestly-scoped case; reader must exercise judgment themselves
- **Text Density:** Moderate-high - Dense technical prose with precise terminology
- **Code vs Prose vs Figures:** Pure prose. No code blocks, no figures, no diagrams
- **Cadence:** What we built (one element, three notebooks) → What this establishes (bidirectional vs one-sided verification, gap closure mechanism, ledger findings, synthesis honesty) → What comes next (reader's accountable engineering, not another chapter) → Exercise reference
- **Consistency:** Follows conclusion format from all prior chapters (Ch9, Ch8, Ch7, etc). Same structure and depth
- **Data Consistency:** All technical details match prior chapters exactly (EnergyConservationReq/energyConservationReq, deliveredEnergyBoundedBySupply, subsetting via require constraint, AS-C06/AS-C08/AI-C06 summaries, AC-C10, energyConservationReq covered=False by design not omission, all requirement names and tracing results, engineering_conclusion="undetermined" reasoning)

---

## OVERALL SYNTHESIS: 10-CHAPTER LEARNER JOURNEY

### Top 5 Stuck/Confused Points (Ranked)

1. **Polarity-blind join bug (PAGE 44, Ch9-01)** - "a join that counts ANY claim, positive or negative, as coverage" was the actual bug in the repository's own requirement_coverage() helper. This was shocking because it's a systematic misunderstanding that would silently report false positives. The fix is clear (check isNegated), but the discovery that this had existed unreported is sobering.

2. **Sufficiency vs. structural validation (PAGE 45, Ch9-02)** - The placeholder record passes all validate_record() checks (non-empty fields) but fails sufficiency reading (generic "None known." vs. specific design alternatives/unmodeled relations). This separation between "mechanized floor" and "content-based judgment" is profound: "A structural check alone cannot tell substantive text from a placeholder."

3. **Retroactively-identified requirements (PAGE 48 Overview, PAGE 51 Ch10-03)** - EnergyConservationReq was added AFTER Chapter 8's Z3 proof existed, specifically to close the traceability gap. AC-C10 calls this "a real, honestly-named assurance deficit about circularity, not resolved here." The tension between "genuine physical law" motivation and "retroactive identification" is genuinely unsettling for sign-off confidence.

4. **Hand-restated lemma, not solver-checked (PAGE 51 Ch10-03)** - AS-C08's proof is "of a hand-restated companion lemma, not a solver-checked reference to HeatGenerator's own efficiencyBounded/deliveredEnergy." Toolchain limits (D-030/D-031) force this compromise. The gap between "proved lemma" and "proved requirement" is not closed by subsetting into a requirement.

5. **Subsetting does not equal assert satisfy (PAGE 49 Ch10-01, PAGE 51 Ch10-03)** - The negative control shows assert satisfy would "error identically regardless of its own binding" because energyConservationReq's required constraint never references subject. So subsetting is used instead. But requirement_coverage() still reports covered=False by design. Quote: "requirement_coverage()'s own covered=False for it is correct and expected, not a residual gap."

### Cumulative Cognitive-Load Trend Across All 10 Chapters

- **Ch1-3 (Pages 1-10): Low baseline** (1-2/5) - Introduction, model basics, functional vs. logical layers. Gentle learning curve.
- **Ch4-5 (Pages 11-20): Steady increase** (2-3/5) - State machines, behavioral concepts, parameter sweeps. Code complexity grows gradually.
- **Ch6 (Pages 21-26): High plateau** (3-4/5) - Judgment records introduced (Hawkins taxonomy, ReviewRecord structure). Decision-making concepts add cognitive weight.
- **Ch7 (Pages 27-34): Moderate** (2-3/5) - Design space exploration, parametric analysis. Technically dense but more exploratory than prescriptive.
- **Ch8 (Pages 35-42): Very high spike** (4-5/5) - Formal verification, Z3 solver, proof vs. point evaluation, universal proof lemmas. Model-checked properties, hand-restated claims, solver limits.
- **Ch9 (Pages 43-46): High, sustained** (3-4/5) - Requirement coverage (polarity-blind bug), sufficiency checking (structural vs. content), staleness at scale. Multiple records analyzed in parallel.
- **Ch10 (Pages 47-52): Peak complexity** (4-5/5) - Traceability graphs, gap remediation, synthesis of two prior notebooks into master judgment record. Engineering decision-making framed but not performed. "Strong emergence" concept (what analysis cannot anticipate).

**Trend**: Starts gentle, peaks at Ch8 (formal verification), sustains high through Ch9-10 (judgment synthesis and sign-off framework). The final 10 chapters form an escalating arc toward accountable decision-making, with cognitive load highest at decision points (Ch8 proof verification, Ch9-10 synthesis).

### Top Cross-Cutting Consistency Issues

1. **Terminology: "Covered" vs. "Not Covered"** - energyConservationReq is NOT covered by requirement_coverage() (covered=False), but this is by DESIGN (subsetting mechanism, no assert satisfy), not a gap like timely's uncovered state. The same word "uncovered" masks two structurally different conditions. Quote from PAGE 51: "requirement_coverage()'s own covered=False for energyConservationReq is therefore correct and expected, a different, by-design kind of 'uncovered' from timely's own real gap."

2. **Notation: content_hash vs. check_stale()**- Multiple pages (Ch8-03, Ch9-03) discuss staleness detection using content_hash over the whole model file. This is a blunt but honest safeguard: catches ANY edit, not just the specific elements a residual names as risk. Quote from PAGE 46: "content_hash is computed from the WHOLE model file, so any edit anywhere in it, not only to the specific elements a record's own residual names, invalidates the hash."

3. **Visual style: Judgment records** - All judgment records follow toaster-review-protocol (claim, scope, criteria, premises, rationale, counterevidence, residual_uncertainties, disposition, engineering_conclusion). Consistent structure across Ch6-10, but readability suffers when a single record spans 1000+ lines of methodical field assembly (PAGE 51 Ch10-03). No visual hierarchy aids scanning large records.

4. **Data consistency: Record kinds and dispositions** - All tutorial-built records use disposition="pending" (SA-7 rule), never "accepted". All use record_kind="worked_example". But the kinds vary (asserted_solution, asserted_inference, asserted_context) for different judgment roles. The consistency here is strict but the semantic load of "kind" grows across chapters (Ch6 = introduction, Ch10 = synthesis of multiple records).

5. **Inconsistency: "This is the tutorial's last chapter" (PAGE 52)** - But navigation shows "Reproducibility" button next. This creates ambiguity about whether PAGE 52 is truly final or whether there are more pages beyond the stated "10 chapters." The coordinator's instruction "last 3 pages" (Ch10-02, Ch10-03, Chapter 10 Conclusion) suggests PAGE 52 IS intended as final, but the UI navigation contradicts this.

### One-Sentence Completion-Likelihood Verdict

The tutorial successfully builds a traceable, honestly-scoped engineering case with real formal evidence, real judgment records, and explicit residual uncertainties, but explicitly transfers the actual sign-off decision to the reader, making completion contingent on whether readers accept that they, not the tutorial, must exercise accountable judgment on designs of their own.

