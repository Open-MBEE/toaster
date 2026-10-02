# Diagram/Text Integration — Phase A (Survey) Implementation Plan

> **For agentic workers:** This plan's own tasks are NOT code-implementation tasks — there is no test-driven-development cycle, no `pytest`, no commit-per-step. Each task is a read-only research dispatch. Do not invoke `superpowers:subagent-driven-development` or `superpowers:executing-plans` for this plan; see "Execution mechanism" below for the actual procedure.

**Goal:** Produce `decisions/diagram-text-integration-survey.md` — a committed, concrete, per-notebook inventory of exactly which cells get Pattern 1 (construction-zone diagram-replaces-reflection), Pattern 1b (construction-zone reflection-print trimmed to a confirmation query, no diagram available), or Pattern 2 (whole-dump `print(source)` trimmed to a targeted excerpt) treatment, with literal proposed replacement text for each — so Phase B (a separate plan, written only after this one's own output exists) has real content to implement against, not placeholders.

**Architecture:** One read-only research agent per chapter (9 agents, Ch1–Ch8 and Ch10, dispatched in parallel), each given a fully-specified prompt (reproduced verbatim in each task below) instructing it to read every notebook in its own chapter and report structured, per-notebook findings. The orchestrator compiles the 9 reports into one document, with an explicit consistency-check pass before considering it final.

**Tech Stack:** The `Agent` tool (`subagent_type: "Explore"`, read-only — no `Edit`/`Write`/`NotebookEdit` access, appropriate since this phase makes no repository edits); Python for the orchestrator's own compilation and consistency-check scripting (reading notebook JSON, reading SVG `<title>` elements).

**Spec:** `docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md` — read Decisions 1–5, the Process section, "The two target patterns, specified precisely," the Parsimony heuristic, "Rolling cleanup, enumerated," and Non-goals before executing any task below.

## Global Constraints

- **Chapter 9 is out of scope** (spec Non-goals) — no task below covers it.
- **This plan makes no repository edits other than the single compiled survey document** (`decisions/diagram-text-integration-survey.md`), authored by the orchestrator directly, not by any dispatched agent — this is the orchestrator's own established administrative-record-keeping role (spec Decision 3's own carve-out), the same role used compiling `decisions/diagram-survey.md` from Phase 1's own agents.
- **Every dispatched agent is read-only**: no notebook edits, no figure re-renders, no file writes of any kind. Each agent's own report comes back as its `SubagentHandback` text, not as a file it wrote.
- **Every agent must quote exact line numbers and exact cell content from the real files it reads** — never paraphrase from `decisions/diagram-survey.md`'s own prior findings, and never assume a prior finding (including this plan's own stated Pattern-2 cell locations, confirmed as of 2026-10-02) is still accurate if the agent's own read of the live file disagrees. If a disagreement is found, the agent reports it as a finding, not a silent correction.
- **Pattern-2 whole-dump notebooks, confirmed by a direct repo-wide grep on 2026-10-02 (re-verify, don't re-derive from scratch, but flag if this list is stale by the time an agent runs):** `chapters/ch02-requirements/03-judgment-context.ipynb` (cell 2), `chapters/ch03-measures/03-threshold-judgment.ipynb` (cell 2), `chapters/ch04-functional-decomp/03-completeness-check.ipynb` (cell 2), `chapters/ch05-architecture/01-model-navigation.ipynb` (cell 2), `chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb` (cell 2). No other notebook in scope has a `print(source)` call — in particular, `chapters/ch08-checking/01-invariant-def.ipynb` and `chapters/ch10-traceability-signoff/01-traceability-graph.ipynb` do NOT have this pattern (an earlier draft of the spec wrongly included them; corrected before this plan was written).

## Review Focus

Five ways a chapter-survey agent's own report could be wrong in a way that would corrupt Phase B if not caught before the survey document is finalized:

1. **An agent proposes replacing a construction-zone reflection print with a diagram that doesn't actually exist for that notebook.** `decisions/diagram-survey.md` is the only source of truth for which notebooks already have a Phase 2 diagram; an agent must cite the specific diagram (tool, root/scope) it's proposing to reuse, not assume one exists because the chapter has diagrams elsewhere. Task 10 (compilation) cross-checks every Pattern-1 proposal against `decisions/diagram-survey.md`'s own table.
2. **An agent proposes a Pattern-2 trim that removes content the diagram doesn't actually cover.** The whole reason Phase 1 didn't trim these dumps originally is that the diagram only shows structure — a proposal that over-trims (removing a judgment-record field, a requirement body, an attribute default) would silently remove real information. Task 10's own consistency-check spot-checks a sample of Pattern-2 proposals against the real committed figure.
3. **An agent misses a construction notebook's own double-print entirely** because it skims rather than reads every cell. Each task below instructs the agent explicitly to read every notebook assigned to it in full, cell by cell, not to sample.
4. **An agent proposes new text that violates `tutorial-style-guide`'s own rules** (sentence word-count ceiling, caption sentence-count, no em-dash, no metanarration, no self-reference) — the exact class of defect the harness-bypass audit's own F5 finding caught. Each task instructs the agent to self-check its own proposed replacement text against these rules before reporting.
5. **An agent expands scope beyond the two named patterns and the enumerated cleanup items** — finding something that looks like a real improvement but isn't in the spec's own named scope. Each task instructs the agent to report such findings as an "open question" in its own report, never as a proposed edit.

---

## Execution mechanism (read before Task 1)

This plan has no builder/reviewer cycle, because it produces no code and nothing merges into chapter content. The mechanism:

1. Dispatch all 9 chapter tasks (Task 1 through Task 9) as parallel `Agent` tool calls in a single message, `subagent_type: "Explore"`, each with the exact prompt text given in that task.
2. Collect each agent's own `SubagentHandback` report (delivered as a message, not a file).
3. Execute Task 10: compile all 9 reports into `decisions/diagram-text-integration-survey.md`, run the consistency-check, commit.
4. Task 10's own completion is this plan's terminal state. Its own final step states explicitly: invoke `superpowers:writing-plans` again, for Phase B, using `decisions/diagram-text-integration-survey.md` (now committed) as the primary input alongside the same spec. This instruction is written here, on disk, specifically so it survives a context compaction that might otherwise lose it.

No independent review gate applies to Phase A's own output, because nothing here is shipped or merged into learner-facing content — Phase A's real adversarial check happens when Phase B's own tasks (generated from this phase's output) go through the full builder/reviewer harness, the same two-tier rigor the original diagram-survey mission used (Phase 1 undemanding, Phase 2 fully reviewed).

---

## Task 1: Chapter 1 survey (System and Purpose)

**Files:** none modified by this task (read-only). Chapter files read: `chapters/ch01-system-purpose/01-abstract-def.ipynb`, `02-part-def.ipynb`, `03-specialization.ipynb`, `04-composition.ipynb`, `index.md`.

**Interfaces:**
- Consumes: the dispatch prompt below (self-contained; no other task's output).
- Produces: a structured report (format specified in the prompt) consumed by Task 10.

- [ ] **Step 1: Dispatch the agent**

Use the `Agent` tool with `subagent_type: "Explore"`, this exact prompt:

```
Read docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md in full
first -- specifically "The two target patterns, specified precisely," the
Parsimony heuristic, and "Rolling cleanup, enumerated." This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch01-system-purpose/ -- read every one of its four
notebooks in full, cell by cell, not a sample: 01-abstract-def.ipynb,
02-part-def.ipynb, 03-specialization.ipynb, 04-composition.ipynb. Also read
index.md.

This chapter has NO Pattern-2 whole-dump notebook (confirmed by direct grep,
2026-10-01) -- you are checking for Pattern 1/1b only (construction-zone
reflection-print duplication). Per decisions/diagram-survey.md, this chapter's
own diagrams already exist in 02-part-def.ipynb (two disconnected boxes,
model_to_dot(elements=[...])) and 04-composition.ipynb (full composition +
typing, model_to_dot(elements=containment_subgraph(...))) -- confirm these are
still there and still match that description by reading the real cells, don't
assume.

For EACH of the four notebooks:
1. Find the construction-zone sequence: fragment-declare cells (each printed),
   ending in a TOASTER_INCREMENT assignment, a print of it, then the real
   cumulative-model load. Confirm this pattern is actually present (per
   toaster-recipe/SKILL.md, not every notebook in this tutorial has it --
   report "no construction zone, no finding" if a notebook genuinely lacks
   this structure rather than forcing a finding).
2. If 02-part-def.ipynb or 04-composition.ipynb has this pattern AND a diagram
   already exists for it: propose Pattern 1 -- the exact new cell sequence
   (quote the literal markdown/code you propose for the bridge cell and for
   the TOASTER_INCREMENT cell with its print removed), confirming the diagram
   cell's own existing code doesn't need to move.
3. If 01-abstract-def.ipynb or 03-specialization.ipynb has this pattern and NO
   diagram exists: propose Pattern 1b -- the exact replacement for the
   reflection-print cell (drop the print, keep the TOASTER_INCREMENT
   assignment, add a short model.find()/model.query() confirmation of the
   construct just declared; quote the literal code).
4. Self-check every piece of proposed replacement markdown text against
   tutorial-style-guide/SKILL.md's rules before including it: sentences <=20
   words, no em-dash (the real "—" character; "--" is this tutorial's own
   established convention and is fine), no metanarration, figure captions (if
   any) exactly 2 sentences.

Rolling cleanup: none of the four enumerated items in the spec name Chapter 1
specifically -- do not propose any cleanup edit for this chapter unless you
find something new, in which case report it as an open question (see below),
never as a proposed edit.

Report format, one entry per notebook (skip notebooks with no finding, but
say so explicitly -- "01-abstract-def.ipynb: no construction-zone duplication
found, cell N already differs from the pattern because X" is a valid,
useful report):

NOTEBOOK: <path>
PATTERN: 1 | 1b | none
CELLS IN SCOPE: <cell indices/ids>
CURRENT CONTENT: <literal quote of what's there now>
PROPOSED CONTENT: <literal replacement text/code, not a description>
RATIONALE: <one or two sentences>

Then a final "OPEN QUESTIONS" section for anything you found that doesn't fit
the above (including any Pattern-2-like dump you notice despite this chapter
being marked as having none -- re-verify with grep, don't trust this prompt's
own claim blindly), and a final "INDEX.MD CHECK" section confirming whether
this chapter's own Ingredients table already matches each notebook's current
first-line heading (Ch1's own table was already confirmed accurate as of
2026-10-02 -- note if you find it's drifted since).
```

- [ ] **Step 2: Save the report**

Record the agent's full `SubagentHandback` text for use in Task 10. Do not summarize or discard any of it.

---

## Task 2: Chapter 2 survey (Requirements and Assumptions)

**Files:** none modified. Read: `chapters/ch02-requirements/01-requirement-def.ipynb`, `02-assumptions.ipynb`, `03-judgment-context.ipynb`, `index.md`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md in full
first -- specifically "The two target patterns, specified precisely," the
Parsimony heuristic, and "Rolling cleanup, enumerated." This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch02-requirements/ -- read every one of its three
notebooks in full, cell by cell: 01-requirement-def.ipynb, 02-assumptions.ipynb,
03-judgment-context.ipynb. Also read index.md.

This chapter HAS a Pattern-2 whole-dump notebook: 03-judgment-context.ipynb,
cell 2, print(source) over the full cumulative model (~45 lines as of
2026-10-01 -- confirm the current line count yourself). Per
decisions/diagram-survey.md, a structure diagram (model_to_dot(model), whole
model) was already added nearby in Phase 2 -- confirm it's still there,
confirm exactly what it draws by reading the real committed figures/ch02-structure.svg
(grep its own <title> elements for node/edge names), and propose: (a) the
exact trimmed or removed print(source) call, (b) exactly what residual text
(if any) must stay because the diagram doesn't cover it -- 03-judgment-context.ipynb
is a judgment-record (asserted_context) notebook, so check specifically
whether the requirement's own require-constraint body, or any
ReviewRecord/judgment-record field content, is part of what print(source)
currently shows and the diagram cannot. Quote exact line ranges for whatever
you propose keeping.

01-requirement-def.ipynb and 02-assumptions.ipynb: check each for the
construction-zone reflection-print pattern (fragment-declare cells ending in
a TOASTER_INCREMENT print). Per decisions/diagram-survey.md, neither has a
diagram of its own -- if the pattern is present, propose Pattern 1b (drop the
print, keep the assignment, add a model.find()/model.query() confirmation;
quote the literal replacement code). If either notebook's own structure
doesn't actually match this pattern, say so rather than forcing a finding.

Self-check every piece of proposed replacement text against
tutorial-style-guide/SKILL.md: sentences <=20 words, no literal "—" character,
no metanarration, captions exactly 2 sentences.

Rolling cleanup: none of the four enumerated items name Chapter 2
specifically. Report anything else you find as an open question, not a
proposed edit.

Report format (same as Task 1's own spec): one NOTEBOOK/PATTERN/CELLS IN
SCOPE/CURRENT CONTENT/PROPOSED CONTENT/RATIONALE entry per finding, an OPEN
QUESTIONS section, and an INDEX.MD CHECK section (Ch2's table was already
confirmed accurate as of 2026-10-02 -- note if drifted).
```

- [ ] **Step 2: Save the report**

---

## Task 3: Chapter 3 survey (Measures of Success)

**Files:** none modified. Read: `chapters/ch03-measures/01-moe-definition.ipynb`, `02-mop-candidate-eval.ipynb`, `03-threshold-judgment.ipynb`, `04-verification-case.ipynb`, `index.md`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md in full
first -- specifically "The two target patterns, specified precisely," the
Parsimony heuristic, and "Rolling cleanup, enumerated." This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch03-measures/ -- read every one of its four notebooks
in full, cell by cell: 01-moe-definition.ipynb, 02-mop-candidate-eval.ipynb,
03-threshold-judgment.ipynb, 04-verification-case.ipynb. Also read index.md.

This chapter HAS a Pattern-2 whole-dump notebook: 03-threshold-judgment.ipynb,
cell 2, print(source) over the full cumulative model (83 lines as of
2026-10-01 -- confirm the current line count yourself). A structure diagram
(model_to_dot(model), parts only) was already added nearby in Phase 2 --
confirm it's still there by reading the real committed figures/ch03-structure.svg
(grep its own <title> elements). decisions/diagram-survey.md's own original
note on this dump said the diagram "cannot show TimelyToast, the folded
satisfy claim, or TimelyToastTest, which is the dump's actual point" -- verify
this is still true against the live figure and model, and propose: (a) the
exact trimmed print(source) call, (b) exactly what residual text must stay
(quote exact line ranges -- likely the TimelyToast requirement declaration,
the satisfy claim, and/or TimelyToastTest's own declaration, but confirm by
reading the real file, don't assume this list is complete or correct).

01-moe-definition.ipynb, 02-mop-candidate-eval.ipynb, 04-verification-case.ipynb:
check each for the construction-zone reflection-print pattern. None has its
own diagram per decisions/diagram-survey.md -- if the pattern is present in
any of them, propose Pattern 1b (drop the print, keep the TOASTER_INCREMENT
assignment, add a model.find()/model.query() confirmation; quote the literal
replacement code).

Self-check every piece of proposed replacement text against
tutorial-style-guide/SKILL.md: sentences <=20 words, no literal "—" character,
no metanarration, captions exactly 2 sentences.

Rolling cleanup: none of the four enumerated items name Chapter 3
specifically. Report anything else you find as an open question.

Report format (same as Task 1's own spec): NOTEBOOK/PATTERN/CELLS IN
SCOPE/CURRENT CONTENT/PROPOSED CONTENT/RATIONALE per finding, OPEN QUESTIONS,
INDEX.MD CHECK (Ch3's table was already confirmed accurate as of 2026-10-02).
```

- [ ] **Step 2: Save the report**

---

## Task 4: Chapter 4 survey (Functional Decomposition)

**Files:** none modified. Read: `chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb`, `02-heating-refinement.ipynb`, `03-completeness-check.ipynb`, `index.md`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md in full
first -- specifically "The two target patterns, specified precisely," the
Parsimony heuristic, and "Rolling cleanup, enumerated." This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch04-functional-decomp/ -- read every one of its three
notebooks in full, cell by cell: 01-action-def-ffbd.ipynb,
02-heating-refinement.ipynb, 03-completeness-check.ipynb. Also read index.md.

This chapter HAS a Pattern-2 whole-dump notebook: 03-completeness-check.ipynb,
cell 2, print(source) over the full cumulative model (115+ lines as of
2026-10-01 -- confirm the current line count yourself). Per
decisions/diagram-survey.md, a SCOPED structure diagram
(model_to_dot(elements=containment_subgraph(model, "ToasterDemo::Toaster",
depth=2))) was already added nearby -- confirm it's still there by reading
the real committed figures/ch04-structure.svg, and note this diagram is
SCOPED (rooted at Toaster, depth 2), not whole-model -- it will NOT show
everything the full dump shows even structurally (anything outside that
scope). decisions/diagram-survey.md's own original note said the diagram
"covers only the Part-structure portion of the dump" -- verify this against
the real figure and model, and propose: (a) the exact trimmed print(source)
call, (b) exactly what residual text must stay, including anything outside
the diagram's own Toaster/depth-2 scope as well as anything non-structural
(the completeness-check judgment record's own content, if cell 2's dump is
shared with that). Quote exact line ranges.

01-action-def-ffbd.ipynb already has its own diagram (action-flow of
ToastBread, via render_action_flow -- NOT ApplyHeat; confirm this against the
real cell and figures/ch04-toastbread-flow.svg, since an earlier, now-corrected
draft of this redesign's own spec mis-stated which action this chapter's
diagram renders). Check it for the construction-zone reflection-print pattern;
if present, propose Pattern 1 (the diagram takes over the reflection step --
quote the exact new bridge cell and the TOASTER_INCREMENT cell with its print
removed).

02-heating-refinement.ipynb: no diagram per decisions/diagram-survey.md --
check for the construction-zone pattern; if present, propose Pattern 1b (drop
the print, keep the assignment, add a confirmation query; quote the literal
code).

Self-check every piece of proposed replacement text against
tutorial-style-guide/SKILL.md: sentences <=20 words, no literal "—" character,
no metanarration, captions exactly 2 sentences.

Rolling cleanup: none of the four enumerated items name Chapter 4
specifically. Report anything else as an open question.

Report format (same as Task 1's own spec): NOTEBOOK/PATTERN/CELLS IN
SCOPE/CURRENT CONTENT/PROPOSED CONTENT/RATIONALE per finding, OPEN QUESTIONS,
INDEX.MD CHECK (Ch4's table was already confirmed accurate as of 2026-10-02 --
it already names both diagrams explicitly, per DL-089's own earlier fix;
confirm this is still true).
```

- [ ] **Step 2: Save the report**

---

## Task 5: Chapter 5 survey (Architecture and Allocation)

**Files:** none modified. Read: `chapters/ch05-architecture/01-model-navigation.ipynb`, `02-allocate.ipynb`, `03-interfaces.ipynb`, `index.md`, `conclusion.md`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md in full
first -- specifically "The two target patterns, specified precisely," the
Parsimony heuristic, and "Rolling cleanup, enumerated." This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch05-architecture/ -- read every one of its three
notebooks in full, cell by cell: 01-model-navigation.ipynb, 02-allocate.ipynb,
03-interfaces.ipynb. Also read index.md and conclusion.md.

This chapter HAS a Pattern-2 whole-dump notebook: 01-model-navigation.ipynb,
cell 2, print(source) over the full cumulative model (131 lines as of
2026-10-01 -- confirm the current line count yourself). Per
decisions/diagram-survey.md, an UNSCOPED structure diagram (model_to_dot(),
whole model) was already added nearby -- confirm it's still there by reading
the real committed figures/ch05-structure.svg. Since this diagram is
unscoped, it likely covers the dump's own structural content fully; propose
(a) the exact trimmed or removed print(source) call, (b) exactly what
residual text must stay (if any -- it is plausible the answer here is "none,
the dump can be fully removed," unlike Ch2/Ch3/Ch4's own cases; confirm by
actually comparing what the dump shows against what the diagram draws, don't
assume). Quote exact line ranges for anything you propose keeping.

NOTE: 02-allocate.ipynb and 03-interfaces.ipynb each separately re-print this
SAME 131-line dump again (decisions/diagram-survey.md's own row for them:
"same 131-line dump, repeated verbatim... no candidate... diagram fatigue, not
a real reduction"). Check whether these two notebooks' own dumps are STILL
present as of your own read -- if so, this is a genuine duplication Pattern 2
as originally scoped does not quite cover (the SAME content printed three
times across one chapter, not once per notebook) -- report this explicitly as
a finding even though it doesn't fit either named pattern cleanly, proposing
what you think the right trim is (most likely: remove the repeat dumps
entirely from 02/03, since 01's own dump already establishes this content and
Chapter 1's own established convention is that later notebooks reference
rather than re-dump earlier content), but flag it as an OPEN QUESTION for Z/
the orchestrator rather than treating your own proposal as settled, since it's
outside this plan's own named scope.

03-interfaces.ipynb ALSO has its own separate diagram
(render_toolkit_interconnection(), sysml-toolkit-based, the conjugated-port
figure) -- this is unrelated to the whole-dump question above; just confirm
it's still present and unaffected by the duplicate-dump finding above.

Check 01-model-navigation.ipynb, 02-allocate.ipynb, 03-interfaces.ipynb for
the construction-zone reflection-print pattern separately from the Pattern-2
question above -- if present in any, propose Pattern 1 (if a diagram exists
for that specific construct) or Pattern 1b (if not); quote literal
replacement text.

Self-check every piece of proposed replacement text against
tutorial-style-guide/SKILL.md: sentences <=20 words, no literal "—" character,
no metanarration, captions exactly 2 sentences.

Rolling cleanup -- THIS CHAPTER IS NAMED in enumerated item 1: Ch5's own
index.md Ingredients table says "Model Navigation" (title case) while
01-model-navigation.ipynb's own current heading is "model navigation"
(lowercase) -- confirm this mismatch against the live files and propose the
exact corrected table row (sync to the notebook's own current heading
exactly). Also check enumerated item 2 (Ch1-7 use "01:" separator, Ch8-10 use
"01 -") -- Ch5 already uses "01:" per the convention item 2 recommends
keeping, confirm this is still true, no change needed if so.

Report format (same as Task 1's own spec): NOTEBOOK/PATTERN/CELLS IN
SCOPE/CURRENT CONTENT/PROPOSED CONTENT/RATIONALE per finding, OPEN QUESTIONS
(including the triple-dump finding above), INDEX.MD CHECK (propose the exact
corrected "Model Navigation" -> "model navigation" row text).
```

- [ ] **Step 2: Save the report**

---

## Task 6: Chapter 6 survey (Recursive Decomposition)

**Files:** none modified. Read: `chapters/ch06-recursive-decomp/01-subsystem-requirements.ipynb`, `02-second-level.ipynb`, `03-stopping-judgment.ipynb`, `index.md`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md in full
first -- specifically "The two target patterns, specified precisely," the
Parsimony heuristic, and "Rolling cleanup, enumerated." This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch06-recursive-decomp/ -- read every one of its three
notebooks in full, cell by cell: 01-subsystem-requirements.ipynb,
02-second-level.ipynb, 03-stopping-judgment.ipynb. Also read index.md.

This chapter HAS a Pattern-2 whole-dump notebook: 03-stopping-judgment.ipynb,
cell 2, print(source) over the full cumulative model (213 lines as of
2026-10-01, the densest single block in this entire tutorial -- confirm the
current line count yourself). Per decisions/diagram-survey.md, a SCOPED
structure diagram (model_to_dot(elements=containment_subgraph(model,
"ToasterDemo::HeatingAssembly", depth=2))) was already added nearby, and this
chapter's own original Phase 2 contract explicitly chose "add (the full
source print stays)" rather than trimming -- this is the single largest
remaining text-reduction opportunity in the whole tutorial. Confirm the
diagram is still there via figures/ch06-structure.svg, and propose: (a) the
exact trimmed print(source) call, (b) exactly what residual text must stay
(the diagram is scoped to HeatingAssembly/depth-2, so anything about Toaster
itself, or non-structural content like the AI-C06 stopping-judgment's own
fields, would need to stay or move elsewhere -- quote exact line ranges, read
the real file, don't guess).

01-subsystem-requirements.ipynb already has TWO diagrams of its own
(action-flow of ApplyHeat via render_action_flow, and an interconnection
diagram of HeatingAssembly via build_interconnection_intent/render_interconnection)
plus its own construction-zone reflection-print pattern (confirmed present
earlier this session, fixed once already for a different defect -- re-read
the live file, don't rely on memory). Propose Pattern 1 for its own
reflection-print cell: the diagram(s) already sit nearby per this chapter's
own existing bridge-cell convention (cells already named cell-ch06-applyheat-flow-caption
etc. -- read the real current cell IDs and content) -- confirm whether the
reflection print itself is still separately present and duplicative on top of
that, and if so, propose its exact removal (quote the resulting cell
sequence).

02-second-level.ipynb: no diagram per decisions/diagram-survey.md -- check for
the construction-zone pattern; if present, propose Pattern 1b.

Self-check every piece of proposed replacement text against
tutorial-style-guide/SKILL.md: sentences <=20 words, no literal "—" character,
no metanarration, captions exactly 2 sentences.

Rolling cleanup -- THIS CHAPTER IS NAMED in enumerated item 1: Ch6's own
index.md table likely shows "Stopping Judgment" (title case) against
03-stopping-judgment.ipynb's own current heading "stopping judgment"
(lowercase) -- confirm against the live files and propose the exact corrected
row. Also check whether any OTHER table row in this chapter has drifted from
its own notebook's current heading (01-subsystem-requirements.ipynb's heading
is "level-2 function and logical carrier" as of 2026-10-01 -- confirm the
table matches). Item 2 (separator convention): Ch6 already uses "01:", confirm
no change needed.

Report format (same as Task 1's own spec): NOTEBOOK/PATTERN/CELLS IN
SCOPE/CURRENT CONTENT/PROPOSED CONTENT/RATIONALE per finding, OPEN QUESTIONS,
INDEX.MD CHECK (propose exact corrected row text for any mismatch found).
```

- [ ] **Step 2: Save the report**

---

## Task 7: Chapter 7 survey (Execution and Experiments)

**Files:** none modified. Read: `chapters/ch07-execution/01-calc-energy.ipynb`, `02-state-traces.ipynb`, `03-param-sweep.ipynb`, `index.md`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md in full
first -- specifically "The two target patterns, specified precisely," the
Parsimony heuristic, and "Rolling cleanup, enumerated." This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch07-execution/ -- read every one of its three
notebooks in full, cell by cell: 01-calc-energy.ipynb, 02-state-traces.ipynb,
03-param-sweep.ipynb. Also read index.md.

This chapter has NO Pattern-2 whole-dump notebook (confirmed by direct grep,
2026-10-01) -- Pattern 1/1b only.

02-state-traces.ipynb already has its own state diagrams (base Cycle, plus a
typo-probe negative control, via render_state_flow -- OpenSysML's own CLI)
and its own construction-zone pattern. Propose Pattern 1 for its reflection
print if still present on a fresh read (quote exact replacement).

01-calc-energy.ipynb and 03-param-sweep.ipynb: no diagram per
decisions/diagram-survey.md -- check each for the construction-zone pattern;
if present, propose Pattern 1b (quote literal replacement code).

Self-check every piece of proposed replacement text against
tutorial-style-guide/SKILL.md: sentences <=20 words, no literal "—" character,
no metanarration, captions exactly 2 sentences.

Rolling cleanup -- THIS CHAPTER IS NAMED in enumerated item 1: Ch7's own
index.md table entry for 02-state-traces.ipynb was flagged as showing a
curly apostrophe ("the toaster's own operating cycle," with a typographic
apostrophe) where the notebook's own real heading may use a straight one, or
vice versa -- read both the table text and the notebook's own current cell-0
heading byte-for-byte (do not rely on how your own tool renders the
character; check the raw text) and propose the exact corrected row, matching
whichever form the notebook's own live heading actually uses. Also check the
other two rows (01-calc-energy.ipynb, 03-param-sweep.ipynb) for the same
title-vs-table drift pattern. Item 2 (separator convention): Ch7 already
uses "01:", confirm no change needed.

Report format (same as Task 1's own spec): NOTEBOOK/PATTERN/CELLS IN
SCOPE/CURRENT CONTENT/PROPOSED CONTENT/RATIONALE per finding, OPEN QUESTIONS,
INDEX.MD CHECK (propose exact corrected row text, byte-for-byte on the
apostrophe question).
```

- [ ] **Step 2: Save the report**

---

## Task 8: Chapter 8 survey (Checking and Revision)

**Files:** none modified. Read: `chapters/ch08-checking/01-invariant-def.ipynb`, `02-violation-witness.ipynb`, `03-revision-flow.ipynb`, `index.md`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md in full
first -- specifically "The two target patterns, specified precisely," the
Parsimony heuristic, and "Rolling cleanup, enumerated." This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch08-checking/ -- read every one of its three
notebooks in full, cell by cell: 01-invariant-def.ipynb,
02-violation-witness.ipynb, 03-revision-flow.ipynb. Also read index.md.

This chapter has NO Pattern-2 whole-dump notebook -- confirmed directly:
01-invariant-def.ipynb does NOT contain a print(source) call (an earlier,
now-corrected draft of the redesign spec wrongly claimed it did; verify this
for yourself rather than trusting either claim blindly). Pattern 1/1b only.

01-invariant-def.ipynb has its own structure diagram (model_to_dot(), whole
model) grounding one specific claim (heatGenCheck/rated/weak sibling-usage
and ResistanceCoil's own specialization of HeatGenerator) via a bridge cell
and a caption cell, both already rewritten once this session for accuracy --
read the current live cells (around cell ids cell-03, cell-03a, cell-03b,
cell-03d, cell-03c as of 2026-10-01, but CONFIRM the real current ids/indices,
they may have shifted) and check specifically for the construction-zone
reflection-print pattern SEPARATELY from this existing diagram work -- does
cell 2's own declare-and-print of heatGenCheck get re-printed again anywhere
as a redundant reflection, independent of the diagram? If so, propose Pattern
1 (quote exact replacement). If the existing diagram cells already fully
occupy the "E" seam role with no separate duplicate print, say so explicitly
-- this notebook may already be in a mostly-correct state from prior fixes
this session, and your job here is to confirm that, not assume more work is
needed.

02-violation-witness.ipynb, 03-revision-flow.ipynb: no diagram per
decisions/diagram-survey.md -- check each for the construction-zone pattern;
if present, propose Pattern 1b (quote literal replacement code).

Self-check every piece of proposed replacement text against
tutorial-style-guide/SKILL.md: sentences <=20 words, no literal "—" character,
no metanarration, captions exactly 2 sentences.

Rolling cleanup -- THIS CHAPTER IS NAMED in enumerated items 2 and 3:
(2) Ch8's own index.md table uses "01 - <title>" (dash separator); the spec
recommends switching to "01: <title>" (colon) to match Ch1-7's own majority
convention -- propose the exact corrected table text for all three rows.
(3) chapters/ch08-checking/01-invariant-def.ipynb's own filename and URL slug
still say "invariant-def" even though its heading was already corrected to
"assert constraint" earlier this session (the notebook declares an assert
constraint, not a formal invariant) -- propose a rename (to, e.g.,
01-assert-constraint-def.ipynb or similar; your own best proposal, following
exactly the precedent chapters/ch05-architecture/01-model-navigation.ipynb's
own earlier rename already set) and enumerate EVERY file in the repo that
would need its own reference updated (grep for "invariant-def" and
"invariant_def" repo-wide yourself, don't guess which files reference it --
expect myst.yml at minimum, confirm what else).

Report format (same as Task 1's own spec): NOTEBOOK/PATTERN/CELLS IN
SCOPE/CURRENT CONTENT/PROPOSED CONTENT/RATIONALE per finding, OPEN QUESTIONS,
INDEX.MD CHECK (propose exact corrected rows for the separator fix), plus a
separate RENAME section listing the proposed new filename and every reference
site found.
```

- [ ] **Step 2: Save the report**

---

## Task 9: Chapter 10 survey (Traceability and Sign-off)

**Files:** none modified. Read: `chapters/ch10-traceability-signoff/01-traceability-graph.ipynb`, `02-judgment-synthesis.ipynb`, `03-engineering-signoff.ipynb`, `index.md`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md in full
first -- specifically "The two target patterns, specified precisely," the
Parsimony heuristic, and "Rolling cleanup, enumerated." This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch10-traceability-signoff/ -- read every one of its
three notebooks in full, cell by cell: 01-traceability-graph.ipynb,
02-judgment-synthesis.ipynb, 03-engineering-signoff.ipynb. Also read index.md.

This chapter has NO Pattern-2 whole-dump notebook -- confirmed directly:
01-traceability-graph.ipynb does NOT contain a print(source) call (an
earlier, now-corrected draft of the redesign spec wrongly claimed it did;
verify this for yourself rather than trusting either claim blindly). Pattern
1/1b only.

01-traceability-graph.ipynb has its own UNSCOPED structure diagram
(model_to_dot(), deliberately whole-model because the chapter's own two
traced chains aren't both reachable from any single containment root) --
check for the construction-zone reflection-print pattern separately from this
existing diagram work, the same question as Task 8's own Ch8-01 check: does
this chapter's own model-increment cell (if any -- this notebook may be
query/analysis-only with no new construct of its own, confirm by reading it)
duplicate text the diagram or earlier cells already show? If a genuine
construction-zone pattern exists, propose Pattern 1 or 1b as appropriate
(quote exact replacement). If this notebook has no construction-zone pattern
at all (plausible -- it may be purely query-and-trace, not declaring new
SysML), say so explicitly rather than forcing a finding.

02-judgment-synthesis.ipynb, 03-engineering-signoff.ipynb: no diagram per
decisions/diagram-survey.md -- check each for the construction-zone pattern;
if present, propose Pattern 1b.

Self-check every piece of proposed replacement text against
tutorial-style-guide/SKILL.md: sentences <=20 words, no literal "—" character,
no metanarration, captions exactly 2 sentences.

Rolling cleanup -- THIS CHAPTER IS NAMED in enumerated item 2: Ch10's own
index.md table uses "01 - <title>" (dash separator); propose the exact
corrected "01: <title>" text for all three rows, matching Ch1-7's own
convention.

Report format (same as Task 1's own spec): NOTEBOOK/PATTERN/CELLS IN
SCOPE/CURRENT CONTENT/PROPOSED CONTENT/RATIONALE per finding, OPEN QUESTIONS,
INDEX.MD CHECK (propose exact corrected rows for the separator fix).
```

- [ ] **Step 2: Save the report**

---

## Task 10: Compile the survey document

**Files:**
- Create: `decisions/diagram-text-integration-survey.md`

**Interfaces:**
- Consumes: the 9 saved reports from Tasks 1–9 (exact text, not summarized).
- Produces: the committed survey document Phase B's own `writing-plans` invocation reads as its primary input.

- [ ] **Step 1: Compile the document**

Structure, matching `decisions/diagram-survey.md`'s own shape:

```markdown
# Diagram/Text Integration Survey

Compiled from 9 parallel chapter-survey agents (2026-10-02), per
docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md.
Each chapter section: a short prose strategy paragraph, then a table
(Notebook | Cells | Pattern | Current content | Proposed content | Rationale).

## Chapter 1: System and Purpose
[paragraph + table, from Task 1's own report, verbatim proposed content]

## Chapter 2: Requirements and Assumptions
[...]

[... one section per chapter, Ch1 through Ch8, Ch10 ...]

## Cross-chapter open questions
[every OPEN QUESTIONS entry from every task, attributed to its chapter,
unresolved -- for Z/the orchestrator to triage before Phase B's own plan
is written]

## Index.md corrections
[every INDEX.MD CHECK proposed row, by chapter]

## Proposed rename (Ch8)
[Task 8's own RENAME section, verbatim]
```

- [ ] **Step 2: Run the consistency check**

For every Pattern-1 proposal (construction notebook with an existing diagram): confirm the cited diagram is real by grepping `decisions/diagram-survey.md`'s own table for that notebook. For a sample of at least 3 Pattern-2 proposals (not all — the full check belongs to Phase B's own per-task acceptance criteria): read the real committed `figures/chNN-*.svg` for that chapter and confirm the proposed "residual text" claim is plausible against what the diagram actually draws (its own node/edge `<title>` elements). Flag and correct any inconsistency found before finalizing — do not finalize a known-inconsistent survey.

- [ ] **Step 3: Commit**

```bash
git add decisions/diagram-text-integration-survey.md
git commit -m "Compile the diagram/text integration survey (Phase A complete)"
```

- [ ] **Step 4: State the next step explicitly**

Phase A is now complete. The next step — recorded here so it survives a context compaction — is to invoke `superpowers:writing-plans` again, for **Phase B** (implementation), using `decisions/diagram-text-integration-survey.md` (just committed) and `docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md` as its two inputs. Phase B's own plan will have one task per chapter (or per notebook, where warranted), each a `CONTRACT.md` executed through this repo's own builder/reviewer harness exactly as every Phase 2 chapter task was — builder `claude-sonnet-5`, reviewer `claude-opus-5-5`, a `simulated-learner` spot-check for any notebook whose prose shrank materially, per spec Decision 3 and the Verification section.

---

## Self-review

**1. Spec coverage.** Decision 1 (scope) → Tasks 1–9 each cover both patterns per chapter. Decision 2 (approach) → the two patterns are specified identically in every task prompt, quoting the spec's own before/after shapes. Decision 3 (harness discipline) → this plan makes zero chapter-content edits; Task 10's own compilation is the only write, and it's the orchestrator's own established administrative role. Decision 4 (enumerated cleanup) → items 1–3 are assigned to the specific tasks that name them (Tasks 5, 6, 7 for item 1; Tasks 8, 9 for item 2; Task 8 for item 3); item 4 (D-037, informational only) is referenced in every task implicitly via the shared spec read. Decision 5 (durability) → Task 10 Step 4 states the next step explicitly, on disk.

**2. Placeholder scan.** No task says "propose appropriate changes" without the literal prompt text to generate them; every agent prompt is reproduced in full rather than described. The one deliberate exception — proposed replacement TEXT itself is not pre-written in this plan — is correct, not a placeholder: that text is literally what Phase A exists to produce, the same way Phase 1's own agents (not its own plan) produced `decisions/diagram-survey.md`'s own table content.

**3. Type consistency.** Every task uses the identical report format (`NOTEBOOK/PATTERN/CELLS IN SCOPE/CURRENT CONTENT/PROPOSED CONTENT/RATIONALE`, `OPEN QUESTIONS`, `INDEX.MD CHECK`), so Task 10's own compilation step can process all 9 uniformly.

**4. Review Focus.** All five items (diagram-exists-check, over-trim-check, skim-risk, style-guide self-check, scope-creep-to-open-question) are addressed as explicit instructions inside every one of the 9 agent prompts, not left to the agents' own judgment alone.

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-10-02-diagram-text-integration-phase-a-plan.md`. This plan does not use `superpowers:subagent-driven-development` or `superpowers:executing-plans` — see "Execution mechanism" above. Please review the plan. Does it capture what you want?
