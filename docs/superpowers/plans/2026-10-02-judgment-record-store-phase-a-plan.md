# Judgment-Record Store — Phase A (Survey) Implementation Plan

> **For agentic workers:** This plan's own tasks are NOT code-implementation tasks — there is no
> test-driven-development cycle, no `pytest`, no commit-per-step. Each task is a read-only research
> dispatch. Do not invoke `superpowers:subagent-driven-development` or
> `superpowers:executing-plans` for this plan; see "Execution mechanism" below.

**Goal:** Produce `decisions/judgment-record-store-survey.md` — a committed, concrete inventory of
every `ReviewRecord` constructed in Chapters 1 through 8, which of those are cited by a later
chapter (and therefore need the Phase B persistence retrofit), and the literal `save_record()`
insertion point for each one that does — so Phase B (a separate plan, written only after this
one's own output exists) has real content to implement against, not placeholders.

**Architecture:** One read-only research agent per chapter (8 agents, Ch1–Ch8, dispatched in
parallel), each given a fully-specified prompt instructing it to read every notebook in its own
chapter and report every `ReviewRecord` construction found, cross-checked against the
already-known cited-forward set. The orchestrator compiles the 8 reports into one document,
cross-referencing DL-097's own already-completed Ch9/Ch10 findings for the citing side.

**Tech Stack:** The `Agent` tool (`subagent_type: "Explore"`, read-only); Python/`grep` for the
orchestrator's own cross-identifier checks during compilation.

**Spec:** `docs/superpowers/specs/2026-10-02-judgment-record-store-design.md` — read "Decisions
already made," the Process section, and Non-goals before executing any task below.

## Global Constraints

- This plan makes no repository edits other than the single compiled survey document
  (`decisions/judgment-record-store-survey.md`), authored by the orchestrator directly — the same
  established administrative role used compiling `decisions/diagram-survey.md` and
  `decisions/diagram-text-integration-survey.md`.
- Every dispatched agent is read-only: no notebook edits, no file writes of any kind.
- Every agent must quote exact cell content — never paraphrase, never assume a `ReviewRecord`'s
  field values without reading the live cell.
- The already-known cited-forward identifier set, confirmed by DL-097: `AC-001`, `AC-C03`,
  `AS-C03`, `AI-C04`, `AC-C06`, `AS-C06`, `AI-C06`, `AS-C08`. An agent finding a construction with
  one of these identifiers reports it as a confirmed originating site. An agent finding a
  `ReviewRecord` construction with an identifier NOT in this list must grep the rest of the repo
  for that identifier string itself before concluding it is never cited — reporting "not cited
  elsewhere, confirmed by repo-wide grep" or "found an unexpected citation at `<path>`" as
  appropriate, never assuming silently.

## Review Focus

1. **An agent proposes a `save_record()` insertion for a record that is not actually cited
   anywhere else.** Task 9 (compilation) cross-checks every proposed insertion against the
   confirmed-cited-forward list and DL-097's own citation evidence before including it in the
   final citation graph.
2. **An agent misses a `ReviewRecord` construction** because it skims rather than reads every
   cell. Each task instructs the agent explicitly to read every notebook in full, cell by cell.
3. **An agent assumes a record is never cited elsewhere without actually grepping for it** —
   each task requires a repo-wide grep for the record's own identifier string before concluding
   "not cited," not an assumption based on the known list alone (the known list came from Ch9/Ch10
   only; a chapter between 1 and 8 could cite another chapter 1-8 record that DL-097 never saw).
4. **An agent quotes the wrong cell as the "insertion point"** — e.g. proposing to insert
   `save_record()` before `validate_record()` has actually run, which would persist an unvalidated
   record. Each task explicitly requires the insertion to come after a successful
   `validate_record(record, model=model)` call, and the agent must quote that call's own cell too,
   not just the record-construction cell.
5. **An agent proposes new code that doesn't actually exist yet** (calling `save_record()` before
   Phase B has built it). Each task's own proposed insertion is explicitly labeled as a Phase-B
   target, not something to run or verify now — the agent's job is to find the exact spot, not to
   simulate the call.

---

## Execution mechanism (read before Task 1)

This plan has no builder/reviewer cycle, because it produces no code and nothing merges into
chapter content or `src/toaster/`. Per `decisions/work-contract-template.md`'s own state machine
(`decisions/task-states.md`), this phase never leaves `ready`/`in-progress` for a review state —
there is no `in-review` step here, because nothing is being authored against acceptance criteria
yet, only surveyed. The mechanism:

1. Dispatch all 8 chapter tasks (Task 1 through Task 8) as parallel `Agent` tool calls in a single
   message, `subagent_type: "Explore"`, each with the exact prompt text given in that task.
2. Collect each agent's own `SubagentHandback` report (delivered as a message, not a file).
3. Execute Task 9: compile all 8 reports, plus DL-097's own already-completed Ch9/Ch10 findings,
   into `decisions/judgment-record-store-survey.md`; commit.
4. Task 9's own completion is this plan's terminal state. Its own final step states explicitly:
   invoke `superpowers:writing-plans` again, for Phase B, using
   `decisions/judgment-record-store-survey.md` (now committed) as the primary input alongside the
   spec. This instruction is written here, on disk, specifically so it survives a context
   compaction that might otherwise lose it.

Real adversarial review happens in Phase B, once real `CONTRACT`s (per
`decisions/work-contract-template.md`'s own exact format — Role/Reviewer/State/Task/
Context/Non-goals/Blast zone/Acceptance/Premises/Questions to/Report) exist to review against.

---

## Task 1: Chapter 1 survey (System and Purpose)

**Files:** none modified (read-only). Chapter files read: `chapters/ch01-system-purpose/01-abstract-def.ipynb`, `02-part-def.ipynb`, `03-specialization.ipynb`, `04-composition.ipynb`.

- [ ] **Step 1: Dispatch the agent**

Use the `Agent` tool with `subagent_type: "Explore"`, this exact prompt:

```
Read docs/superpowers/specs/2026-10-02-judgment-record-store-design.md in full first --
specifically "Decisions already made" (items 1-5) and the Process section's own description of
what Phase A must establish. This is a READ-ONLY research task: you make no edits to any file.

Your chapter: chapters/ch01-system-purpose/ -- read every one of its four notebooks in full, cell
by cell, not a sample: 01-abstract-def.ipynb, 02-part-def.ipynb, 03-specialization.ipynb,
04-composition.ipynb.

Search every cell for a construction of a ReviewRecord -- the dataclass defined in
src/toaster/evidence.py (read that file first so you know its exact field names: identifier, kind,
claim, subject_ref, model_ref, content_hash, scope, criteria, premises, assumption_refs,
evidence_refs, rationale, counterevidence, residual_uncertainties, disposition,
dependency_freshness, engineering_conclusion, record_kind). A construction looks like
`ReviewRecord(identifier=..., kind=..., claim=..., ...)`.

For each ReviewRecord construction found:
1. Quote the exact cell content (the full construction call, not a paraphrase), and the notebook
   and cell index/id it's in.
2. Quote the exact nearby cell that calls `validate_record(record, model=model)` on it (this is
   the Phase-B insertion anchor -- save_record() will go immediately after this call succeeds).
   If no such call exists in this notebook, say so explicitly.
3. Check the record's own `identifier` value against this already-known cited-forward set:
   AC-001, AC-C03, AS-C03, AI-C04, AC-C06, AS-C06, AI-C06, AS-C08. If it matches, this is a
   CONFIRMED originating site needing the Phase B retrofit.
4. If the identifier does NOT match that list, grep the entire repository yourself for that exact
   identifier string (e.g. `grep -rn "AC-999"` or whatever the real value is) to check whether
   some other chapter cites it that DL-097's own Ch9/Ch10-only investigation never saw. Report
   "not cited elsewhere, confirmed by repo-wide grep" or "found an unexpected citation at
   <path>:<line>" -- never assume silently.
5. If this record IS cited forward (by #3 or #4), propose the exact literal insertion: the full
   text of a new line, `save_record(record)` (using whatever the actual local variable name for
   the record is in this cell -- quote it exactly), to be added immediately after the
   `validate_record(...)` call succeeds. If it is NOT cited forward, say explicitly "no retrofit
   needed -- this record is never cited elsewhere" and propose nothing.

This chapter's own notebooks may introduce NO ReviewRecord at all -- Chapter 1 is "System and
Purpose" (abstract/concrete part defs, specialization, composition), which may have no judgment
record. If you find no ReviewRecord construction anywhere in these four notebooks, report that
plainly: "No ReviewRecord construction found in Chapter 1" -- do not force a finding.

Report format:

CHAPTER: 1 (System and Purpose)
NOTEBOOKS READ: <list, confirming all 4 were read in full>
RECORDS FOUND: <count, or "none">

For each record found, one block:
NOTEBOOK: <path>
CELL: <index/id>
IDENTIFIER: <value>
FULL CONSTRUCTION (verbatim): <quoted code>
VALIDATE_RECORD CALL (verbatim, with its own cell location): <quoted code, or "none found">
CITED FORWARD: yes (confirmed set) | yes (found by grep: <path:line>) | no (confirmed by repo-wide
grep for "<identifier>")
PROPOSED save_record() INSERTION: <exact line, or "none needed">

Then an OPEN QUESTIONS section for anything that doesn't fit the above (an identifier that looks
like it should follow the AC-/AS-/AI- convention but doesn't, a record with no clear
validate_record call, etc.).
```

- [ ] **Step 2: Save the report**

Record the agent's full `SubagentHandback` text for use in Task 9. Do not summarize or discard any
of it.

---

## Task 2: Chapter 2 survey (Requirements and Assumptions)

**Files:** none modified. Read: `chapters/ch02-requirements/01-requirement-def.ipynb`, `02-assumptions.ipynb`, `03-judgment-context.ipynb`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-judgment-record-store-design.md in full first --
specifically "Decisions already made" (items 1-5) and the Process section. This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch02-requirements/ -- read every one of its three notebooks in full, cell
by cell: 01-requirement-def.ipynb, 02-assumptions.ipynb, 03-judgment-context.ipynb.

Search every cell for a construction of a ReviewRecord -- read src/toaster/evidence.py first for
its exact field names. 03-judgment-context.ipynb is this chapter's own judgment-record notebook
(an asserted_context record per its own concept statement) -- expect to find one there, but read
01 and 02 fully as well rather than assuming they have none.

For each ReviewRecord construction found:
1. Quote the exact cell content (the full construction call), and the notebook/cell it's in.
2. Quote the exact nearby cell that calls `validate_record(record, model=model)` on it (the
   Phase-B insertion anchor). If none exists, say so.
3. Check the record's own `identifier` against this already-known cited-forward set: AC-001,
   AC-C03, AS-C03, AI-C04, AC-C06, AS-C06, AI-C06, AS-C08. AC-001 specifically is expected to
   originate in this chapter -- confirm this directly by reading the live cell, don't assume the
   identifier string from this prompt is correct.
4. If the identifier does NOT match that list, grep the entire repository yourself for that exact
   identifier string to check for an uncaught citation elsewhere. Report "not cited elsewhere,
   confirmed by repo-wide grep" or "found an unexpected citation at <path>:<line>".
5. If cited forward, propose the exact literal `save_record(record)` insertion (quoting the real
   local variable name), immediately after the validate_record(...) call succeeds. If not cited
   forward, say so explicitly and propose nothing.

Report format:

CHAPTER: 2 (Requirements and Assumptions)
NOTEBOOKS READ: <list, confirming all 3 were read in full>
RECORDS FOUND: <count, or "none">

For each record found, one block:
NOTEBOOK: <path>
CELL: <index/id>
IDENTIFIER: <value>
FULL CONSTRUCTION (verbatim): <quoted code>
VALIDATE_RECORD CALL (verbatim, with its own cell location): <quoted code, or "none found">
CITED FORWARD: yes (confirmed set) | yes (found by grep: <path:line>) | no (confirmed by repo-wide
grep for "<identifier>")
PROPOSED save_record() INSERTION: <exact line, or "none needed">

Then an OPEN QUESTIONS section for anything that doesn't fit.
```

- [ ] **Step 2: Save the report**

---

## Task 3: Chapter 3 survey (Measures of Success)

**Files:** none modified. Read: `chapters/ch03-measures/01-moe-definition.ipynb`, `02-mop-candidate-eval.ipynb`, `03-threshold-judgment.ipynb`, `04-verification-case.ipynb`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-judgment-record-store-design.md in full first --
specifically "Decisions already made" (items 1-5) and the Process section. This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch03-measures/ -- read every one of its four notebooks in full, cell by
cell: 01-moe-definition.ipynb, 02-mop-candidate-eval.ipynb, 03-threshold-judgment.ipynb,
04-verification-case.ipynb.

Search every cell for a construction of a ReviewRecord -- read src/toaster/evidence.py first for
its exact field names. 03-threshold-judgment.ipynb is this chapter's own judgment-record notebook
-- expect to find at least one there (AC-C03 and/or AS-C03 per the already-known cited-forward
set), but read all four notebooks fully rather than assuming the others have none.

For each ReviewRecord construction found:
1. Quote the exact cell content (the full construction call), and the notebook/cell it's in.
2. Quote the exact nearby cell that calls `validate_record(record, model=model)` on it. If none
   exists, say so.
3. Check the record's own `identifier` against this already-known cited-forward set: AC-001,
   AC-C03, AS-C03, AI-C04, AC-C06, AS-C06, AI-C06, AS-C08.
4. If the identifier does NOT match that list, grep the entire repository yourself for that exact
   identifier string. Report "not cited elsewhere, confirmed by repo-wide grep" or "found an
   unexpected citation at <path>:<line>".
5. If cited forward, propose the exact literal `save_record(record)` insertion (quoting the real
   local variable name), immediately after the validate_record(...) call succeeds. If not cited
   forward, say so explicitly and propose nothing.

Report format:

CHAPTER: 3 (Measures of Success)
NOTEBOOKS READ: <list, confirming all 4 were read in full>
RECORDS FOUND: <count, or "none">

For each record found, one block:
NOTEBOOK: <path>
CELL: <index/id>
IDENTIFIER: <value>
FULL CONSTRUCTION (verbatim): <quoted code>
VALIDATE_RECORD CALL (verbatim, with its own cell location): <quoted code, or "none found">
CITED FORWARD: yes (confirmed set) | yes (found by grep: <path:line>) | no (confirmed by repo-wide
grep for "<identifier>")
PROPOSED save_record() INSERTION: <exact line, or "none needed">

Then an OPEN QUESTIONS section for anything that doesn't fit.
```

- [ ] **Step 2: Save the report**

---

## Task 4: Chapter 4 survey (Functional Decomposition)

**Files:** none modified. Read: `chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb`, `02-heating-refinement.ipynb`, `03-completeness-check.ipynb`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-judgment-record-store-design.md in full first --
specifically "Decisions already made" (items 1-5) and the Process section. This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch04-functional-decomp/ -- read every one of its three notebooks in full,
cell by cell: 01-action-def-ffbd.ipynb, 02-heating-refinement.ipynb, 03-completeness-check.ipynb.

Search every cell for a construction of a ReviewRecord -- read src/toaster/evidence.py first for
its exact field names. 03-completeness-check.ipynb is this chapter's own judgment-record notebook
(an AI_C04_TAG metadata anchor was found there during an earlier, unrelated Phase B pass this
session, so a ReviewRecord construction is expected there too -- likely identifier AI-C04, in the
already-known cited-forward set) -- confirm this directly by reading the live cell, read all three
notebooks fully rather than assuming.

For each ReviewRecord construction found:
1. Quote the exact cell content (the full construction call), and the notebook/cell it's in.
2. Quote the exact nearby cell that calls `validate_record(record, model=model)` on it. If none
   exists, say so.
3. Check the record's own `identifier` against this already-known cited-forward set: AC-001,
   AC-C03, AS-C03, AI-C04, AC-C06, AS-C06, AI-C06, AS-C08.
4. If the identifier does NOT match that list, grep the entire repository yourself for that exact
   identifier string. Report "not cited elsewhere, confirmed by repo-wide grep" or "found an
   unexpected citation at <path>:<line>".
5. If cited forward, propose the exact literal `save_record(record)` insertion (quoting the real
   local variable name), immediately after the validate_record(...) call succeeds. If not cited
   forward, say so explicitly and propose nothing.

Report format:

CHAPTER: 4 (Functional Decomposition)
NOTEBOOKS READ: <list, confirming all 3 were read in full>
RECORDS FOUND: <count, or "none">

For each record found, one block:
NOTEBOOK: <path>
CELL: <index/id>
IDENTIFIER: <value>
FULL CONSTRUCTION (verbatim): <quoted code>
VALIDATE_RECORD CALL (verbatim, with its own cell location): <quoted code, or "none found">
CITED FORWARD: yes (confirmed set) | yes (found by grep: <path:line>) | no (confirmed by repo-wide
grep for "<identifier>")
PROPOSED save_record() INSERTION: <exact line, or "none needed">

Then an OPEN QUESTIONS section for anything that doesn't fit.
```

- [ ] **Step 2: Save the report**

---

## Task 5: Chapter 5 survey (Architecture and Allocation)

**Files:** none modified. Read: `chapters/ch05-architecture/01-model-navigation.ipynb`, `02-allocate.ipynb`, `03-interfaces.ipynb`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-judgment-record-store-design.md in full first --
specifically "Decisions already made" (items 1-5) and the Process section. This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch05-architecture/ -- read every one of its three notebooks in full, cell by
cell: 01-model-navigation.ipynb, 02-allocate.ipynb, 03-interfaces.ipynb.

Search every cell for a construction of a ReviewRecord -- read src/toaster/evidence.py first for
its exact field names. This chapter is navigation/allocation/interfaces-focused; it may have NO
judgment-record notebook at all -- read all three notebooks fully and report plainly if none is
found, do not force a finding.

For each ReviewRecord construction found (if any):
1. Quote the exact cell content (the full construction call), and the notebook/cell it's in.
2. Quote the exact nearby cell that calls `validate_record(record, model=model)` on it. If none
   exists, say so.
3. Check the record's own `identifier` against this already-known cited-forward set: AC-001,
   AC-C03, AS-C03, AI-C04, AC-C06, AS-C06, AI-C06, AS-C08.
4. If the identifier does NOT match that list, grep the entire repository yourself for that exact
   identifier string. Report "not cited elsewhere, confirmed by repo-wide grep" or "found an
   unexpected citation at <path>:<line>".
5. If cited forward, propose the exact literal `save_record(record)` insertion (quoting the real
   local variable name), immediately after the validate_record(...) call succeeds. If not cited
   forward, say so explicitly and propose nothing.

Report format:

CHAPTER: 5 (Architecture and Allocation)
NOTEBOOKS READ: <list, confirming all 3 were read in full>
RECORDS FOUND: <count, or "none">

For each record found, one block (omit entirely if none found -- just state "No ReviewRecord
construction found in Chapter 5"):
NOTEBOOK: <path>
CELL: <index/id>
IDENTIFIER: <value>
FULL CONSTRUCTION (verbatim): <quoted code>
VALIDATE_RECORD CALL (verbatim, with its own cell location): <quoted code, or "none found">
CITED FORWARD: yes (confirmed set) | yes (found by grep: <path:line>) | no (confirmed by repo-wide
grep for "<identifier>")
PROPOSED save_record() INSERTION: <exact line, or "none needed">

Then an OPEN QUESTIONS section for anything that doesn't fit.
```

- [ ] **Step 2: Save the report**

---

## Task 6: Chapter 6 survey (Recursive Decomposition)

**Files:** none modified. Read: `chapters/ch06-recursive-decomp/01-subsystem-requirements.ipynb`, `02-second-level.ipynb`, `03-stopping-judgment.ipynb`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-judgment-record-store-design.md in full first --
specifically "Decisions already made" (items 1-5) and the Process section. This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch06-recursive-decomp/ -- read every one of its three notebooks in full,
cell by cell: 01-subsystem-requirements.ipynb, 02-second-level.ipynb, 03-stopping-judgment.ipynb.

Search every cell for a construction of a ReviewRecord -- read src/toaster/evidence.py first for
its exact field names. This chapter is expected to be the richest source in Ch1-8: the
already-known cited-forward set includes AC-C06, AS-C06, and AI-C06, all plausibly originating
here (02-second-level.ipynb and 03-stopping-judgment.ipynb are this chapter's own judgment-record
notebooks per earlier work this session). Confirm each by reading the live cells directly -- do
not assume the identifiers or their originating notebook from this prompt's own description;
read and quote the real cells.

For each ReviewRecord construction found:
1. Quote the exact cell content (the full construction call), and the notebook/cell it's in.
2. Quote the exact nearby cell that calls `validate_record(record, model=model)` on it. If none
   exists, say so.
3. Check the record's own `identifier` against this already-known cited-forward set: AC-001,
   AC-C03, AS-C03, AI-C04, AC-C06, AS-C06, AI-C06, AS-C08.
4. If the identifier does NOT match that list, grep the entire repository yourself for that exact
   identifier string. Report "not cited elsewhere, confirmed by repo-wide grep" or "found an
   unexpected citation at <path>:<line>".
5. If cited forward, propose the exact literal `save_record(record)` insertion (quoting the real
   local variable name), immediately after the validate_record(...) call succeeds. If not cited
   forward, say so explicitly and propose nothing.

Report format:

CHAPTER: 6 (Recursive Decomposition)
NOTEBOOKS READ: <list, confirming all 3 were read in full>
RECORDS FOUND: <count, or "none">

For each record found, one block:
NOTEBOOK: <path>
CELL: <index/id>
IDENTIFIER: <value>
FULL CONSTRUCTION (verbatim): <quoted code>
VALIDATE_RECORD CALL (verbatim, with its own cell location): <quoted code, or "none found">
CITED FORWARD: yes (confirmed set) | yes (found by grep: <path:line>) | no (confirmed by repo-wide
grep for "<identifier>")
PROPOSED save_record() INSERTION: <exact line, or "none needed">

Then an OPEN QUESTIONS section for anything that doesn't fit -- specifically flag if you find
MORE than 3 records in this chapter (e.g. if AC-C06/AS-C06/AI-C06 aren't the only ones), since the
cited-forward set names exactly three for this chapter and a fourth would be new information.
```

- [ ] **Step 2: Save the report**

---

## Task 7: Chapter 7 survey (Execution and Experiments)

**Files:** none modified. Read: `chapters/ch07-execution/01-calc-energy.ipynb`, `02-state-traces.ipynb`, `03-param-sweep.ipynb`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-judgment-record-store-design.md in full first --
specifically "Decisions already made" (items 1-5) and the Process section. This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch07-execution/ -- read every one of its three notebooks in full, cell by
cell: 01-calc-energy.ipynb, 02-state-traces.ipynb, 03-param-sweep.ipynb.

Search every cell for a construction of a ReviewRecord -- read src/toaster/evidence.py first for
its exact field names. This chapter is execution/simulation-focused (energy calc, state traces,
param sweep); it may have NO judgment-record notebook at all -- read all three notebooks fully and
report plainly if none is found, do not force a finding.

For each ReviewRecord construction found (if any):
1. Quote the exact cell content (the full construction call), and the notebook/cell it's in.
2. Quote the exact nearby cell that calls `validate_record(record, model=model)` on it. If none
   exists, say so.
3. Check the record's own `identifier` against this already-known cited-forward set: AC-001,
   AC-C03, AS-C03, AI-C04, AC-C06, AS-C06, AI-C06, AS-C08.
4. If the identifier does NOT match that list, grep the entire repository yourself for that exact
   identifier string. Report "not cited elsewhere, confirmed by repo-wide grep" or "found an
   unexpected citation at <path>:<line>".
5. If cited forward, propose the exact literal `save_record(record)` insertion (quoting the real
   local variable name), immediately after the validate_record(...) call succeeds. If not cited
   forward, say so explicitly and propose nothing.

Report format:

CHAPTER: 7 (Execution and Experiments)
NOTEBOOKS READ: <list, confirming all 3 were read in full>
RECORDS FOUND: <count, or "none">

For each record found, one block (omit entirely if none found -- just state "No ReviewRecord
construction found in Chapter 7"):
NOTEBOOK: <path>
CELL: <index/id>
IDENTIFIER: <value>
FULL CONSTRUCTION (verbatim): <quoted code>
VALIDATE_RECORD CALL (verbatim, with its own cell location): <quoted code, or "none found">
CITED FORWARD: yes (confirmed set) | yes (found by grep: <path:line>) | no (confirmed by repo-wide
grep for "<identifier>")
PROPOSED save_record() INSERTION: <exact line, or "none needed">

Then an OPEN QUESTIONS section for anything that doesn't fit.
```

- [ ] **Step 2: Save the report**

---

## Task 8: Chapter 8 survey (Checking and Revision)

**Files:** none modified. Read: `chapters/ch08-checking/01-assert-constraint-def.ipynb`, `02-violation-witness.ipynb`, `03-revision-flow.ipynb`.

- [ ] **Step 1: Dispatch the agent**

```
Read docs/superpowers/specs/2026-10-02-judgment-record-store-design.md in full first --
specifically "Decisions already made" (items 1-5) and the Process section. This is a READ-ONLY
research task: you make no edits to any file.

Your chapter: chapters/ch08-checking/ -- read every one of its three notebooks in full, cell by
cell: 01-assert-constraint-def.ipynb, 02-violation-witness.ipynb, 03-revision-flow.ipynb. (Note:
01 was renamed from 01-invariant-def.ipynb in an earlier, unrelated pass this session -- this is
its current, correct filename.)

Search every cell for a construction of a ReviewRecord -- read src/toaster/evidence.py first for
its exact field names. 02-violation-witness.ipynb is expected to contain this chapter's own
judgment-record notebook (AS-C08 is in the already-known cited-forward set and plausibly
originates here) -- confirm directly by reading the live cell, read all three notebooks fully
rather than assuming.

For each ReviewRecord construction found:
1. Quote the exact cell content (the full construction call), and the notebook/cell it's in.
2. Quote the exact nearby cell that calls `validate_record(record, model=model)` on it. If none
   exists, say so.
3. Check the record's own `identifier` against this already-known cited-forward set: AC-001,
   AC-C03, AS-C03, AI-C04, AC-C06, AS-C06, AI-C06, AS-C08.
4. If the identifier does NOT match that list, grep the entire repository yourself for that exact
   identifier string. Report "not cited elsewhere, confirmed by repo-wide grep" or "found an
   unexpected citation at <path>:<line>".
5. If cited forward, propose the exact literal `save_record(record)` insertion (quoting the real
   local variable name), immediately after the validate_record(...) call succeeds. If not cited
   forward, say so explicitly and propose nothing.

Report format:

CHAPTER: 8 (Checking and Revision)
NOTEBOOKS READ: <list, confirming all 3 were read in full>
RECORDS FOUND: <count, or "none">

For each record found, one block:
NOTEBOOK: <path>
CELL: <index/id>
IDENTIFIER: <value>
FULL CONSTRUCTION (verbatim): <quoted code>
VALIDATE_RECORD CALL (verbatim, with its own cell location): <quoted code, or "none found">
CITED FORWARD: yes (confirmed set) | yes (found by grep: <path:line>) | no (confirmed by repo-wide
grep for "<identifier>")
PROPOSED save_record() INSERTION: <exact line, or "none needed">

Then an OPEN QUESTIONS section for anything that doesn't fit.
```

- [ ] **Step 2: Save the report**

---

## Task 9: Compile the survey document

**Files:**
- Create: `decisions/judgment-record-store-survey.md`

- [ ] **Step 1: Compile the document**

Structure:

```markdown
# Judgment-Record Store Survey

Compiled from 8 parallel chapter-survey agents (2026-10-02), per
docs/superpowers/specs/2026-10-02-judgment-record-store-design.md. Each chapter section reports
what Task 1-8's own agent found, verbatim. The citation graph cross-references this document's
own originating-side findings against DL-097's own already-completed citing-side findings
(decisions/log.md).

## Chapter 1: System and Purpose
[Task 1's own report, verbatim]

## Chapter 2: Requirements and Assumptions
[Task 2's own report, verbatim]

[... one section per chapter, Ch1 through Ch8 ...]

## Citation graph

| Identifier | Originating chapter/notebook/cell | `validate_record` cell | Cited by (chapter/notebook/cell) | Phase B action |
|---|---|---|---|---|
[one row per identifier found across Tasks 1-8, cross-referenced against DL-097's own Ch9/Ch10
findings for the "Cited by" column -- quote DL-097's own exact findings rather than re-deriving
them. "Phase B action" is either "retrofit to save" (originating side) or "already covered by
DL-097's own Ch9/Ch10 investigation" (citing side, no new work needed from this survey).]

## Cross-chapter open questions
[every OPEN QUESTIONS entry from every task, attributed to its chapter, unresolved -- for Z/the
orchestrator to triage before Phase B's own plan is written]
```

- [ ] **Step 2: Cross-check against DL-097**

Before finalizing, re-read `decisions/log.md` DL-097 in full (both the ACE's own architectural
diagnosis and the two simulated-learner reports it references) and confirm every identifier this
survey's own Tasks 1-8 found matches, or explicitly reconciles with, what DL-097 already
established about the citing side. Flag and resolve any mismatch (e.g. DL-097 says `AS-C06`
originates in "Chapter 6", this survey's own Task 6 should confirm the exact notebook/cell) before
finalizing — do not finalize a survey that contradicts the already-approved gap analysis without
noting it explicitly as a correction.

- [ ] **Step 3: Commit**

```bash
git add decisions/judgment-record-store-survey.md
git commit -m "Compile the judgment-record store survey (Phase A complete)"
```

- [ ] **Step 4: State the next step explicitly**

Phase A is now complete. The next step — recorded here so it survives a context compaction — is
to invoke `superpowers:writing-plans` again, for **Phase B** (implementation), using
`decisions/judgment-record-store-survey.md` (just committed) and
`docs/superpowers/specs/2026-10-02-judgment-record-store-design.md` as its two inputs. Phase B's
own plan will have: one task building `src/toaster/judgment_store.py` and its tests (first, since
every other task depends on it); one task per originating chapter confirmed by this survey,
retrofitting it to call `save_record()`; one task per citing chapter (Ch9, Ch10) retrofitting it to
call `load_record()` instead of retyping; and one independent task for the two Ch10 authoring bugs
DL-097 already found (no dependency on the rest). Each task is its own `CONTRACT` per
`decisions/work-contract-template.md`'s own exact format, in its own worktree, author and reviewer
on different pinned models, merged only after independent review.

---

## Self-review

**1. Spec coverage.** Decision 1 (module/API shape) → Phase B's own concern, not this plan's;
named here only so Phase A's agents know what `save_record()` will eventually be called. Decision
2 (file-per-record storage) → same, Phase B concern. Decision 3 (authored once) → every task's own
"propose the save_record() insertion point" step is exactly this. Decision 4 (loaded, never
retyped) → already covered by DL-097 for the citing side; this plan's own scope is the originating
side only, per the spec's own Process section. Decision 5 (scope boundary — only retrofit cited
records) → every task's own step 5 explicitly says "if not cited forward, propose nothing."

**2. Placeholder scan.** No task says "propose appropriate insertion" without the literal
instruction to quote exact code; every agent prompt is reproduced in full. The one deliberate
exception — the actual `save_record()` call's own exact text — is not a placeholder: it's literally
what Phase A exists to produce, the same way the original diagram-survey's own agents produced
its own table content, not this plan.

**3. Type consistency.** Every task uses the identical report format
(`NOTEBOOK/CELL/IDENTIFIER/FULL CONSTRUCTION/VALIDATE_RECORD CALL/CITED FORWARD/PROPOSED
save_record() INSERTION`), so Task 9's own compilation step can process all 8 uniformly.

**4. Review Focus.** All five items (false-positive insertion, skim-risk, unverified
not-cited claims, wrong insertion point, simulating not-yet-built code) are addressed as explicit
instructions inside every one of the 8 agent prompts.

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-10-02-judgment-record-store-phase-a-plan.md`.
This plan does not use `superpowers:subagent-driven-development` or `superpowers:executing-plans`
— see "Execution mechanism" above. Please review the plan. Does it capture what you want?
