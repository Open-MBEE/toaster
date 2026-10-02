# Diagram/Text Integration — Phase B (Implementation) Plan

> **For agentic workers:** This plan's own tasks are NOT generic TDD-cycle tasks and do NOT use
> `superpowers:subagent-driven-development` or `superpowers:executing-plans`. This project has its
> own established implementation harness — see "Standard execution procedure" below, which every
> task references instead of restating it. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement every fix `decisions/diagram-text-integration-survey.md` (Phase A's complete
output) proposes — construction-zone reflection-print removal, whole-dump trimming, and the four
enumerated cleanup items — across Chapters 1–8 and 10, through this repo's own builder/reviewer
harness, with zero direct orchestrator edits to chapter content.

**Architecture:** One task per chapter (9 tasks, Ch1–Ch8 and Ch10), each its own `CONTRACT.md`
executed in its own git worktree: builder on `claude-sonnet-5`, reviewer on `claude-opus-5-5`
(always a different model), up to 2 revision cycles then escalate to the ACE, orchestrator merges
after PASS. This is the exact mechanism this session already used and proved for the DL-092/DL-093
skill fix (worktree `skill-fix-092-093`, commits `fbdbc1d`/`e6b54e5`, merged `0fcd4af`) — not
`writing-plans`' own generic Subagent-driven/Native choice. A tenth task is a small administrative
correction to a historical document, done directly by the orchestrator under its own established
record-keeping role (same role used compiling this survey), not a contract.

**Tech Stack:** `git worktree`, the `Agent` tool (`subagent_type: "builder"` / `"reviewer"`),
`uv run pytest`, `uv run python scripts/check_construction.py --check`, `jupyter nbconvert
--execute` (or this repo's own equivalent end-to-end notebook check), the `simulated-learner` agent
type for the Pattern-2 spot-checks.

**Spec:** `docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md`

**Also required reading for every task:** `decisions/diagram-text-integration-survey.md` (Phase
A's output — the literal source of every proposed cell change quoted below) and `decisions/log.md`
DL-092/DL-093 (both `COMPLETE` — the two skills every chapter's own reviewer checks against,
`tutorial-style-guide/SKILL.md`, `toaster-recipe/SKILL.md`, `toaster-review-protocol/SKILL.md`, are
already updated to require "assign, not print").

## Global Constraints

- Chapter 9 is out of scope (spec Non-goals).
- No chapter's taught content, model, or didactic sequencing changes — only presentation
  (diagram vs. print, full dump vs. targeted excerpt) (spec Non-goals).
- No change to `render.py` or any rendering function (spec Non-goals).
- No prose trimming beyond the two named patterns and the four enumerated cleanup items (spec
  Non-goals, Parsimony heuristic).
- Every task's blast zone is read-write only within its own chapter's own files, plus the specific
  cross-chapter reference files Task 8 (Ch8 rename) enumerates — no task touches another chapter's
  own notebook, model, or figure.
- Builder is `claude-sonnet-5`; reviewer is `claude-opus-5-5`; never the same model (spec Decision
  3).
- The survey's own proposed cell content is each task's acceptance criterion, verbatim — not
  something the builder re-derives or improves (spec Decision 2, Process).
- Every task re-runs `uv run pytest tests/ glossary/tests/ -q` and `uv run python
  scripts/check_construction.py --check`, both clean, before the reviewer signs off (spec
  Verification).
- Every task that modifies a Pattern-2 (whole-dump) notebook confirms the trimmed `print()` call's
  output is byte-for-byte / line-range-verified against the real, current `models/chNN-cumulative.sysml`
  file — not just that the cell runs without error (spec Verification; this is how Phase A's own
  consistency-check was done, and Phase B must not regress it).
- At least one `simulated-learner` persona spot-check on every notebook whose prose shrank
  materially (spec Decision 3, Verification) — specifically the five Pattern-2 trims: Ch2-03,
  Ch3-03, Ch4-03, Ch5-01, Ch6-03.
- No skill-content change in this plan — DL-092/DL-093 already closed that work. If a task's own
  builder or reviewer finds a *new* skill contradiction, it is routed to the ACE exactly as
  DL-092/DL-093 were, never fixed inline inside a chapter contract (spec Non-goals).

## Review Focus

1. **A builder reprints more or less than the survey's own exact proposed line range for a
   Pattern-2 trim**, silently drifting from the already-verified residual. Pinned to: Tasks 2, 3,
   4, 5, 6's own acceptance criteria quote the survey's exact line ranges and exact excerpt code;
   each task's Verification step re-diffs the committed trim against those exact ranges.
2. **A builder "fixes" a seam-cell or bridge sentence the survey didn't flag as needing a wording
   change**, introducing scope creep the harness exists to catch. Pinned to: every task's Non-Goals
   section states explicitly which sentences are in scope to reword and that no other prose may
   change; every task's reviewer step checks the diff for any touched line outside the enumerated
   list.
3. **The Ch8 rename misses one of the 6 enumerated reference-update files**, breaking a link
   silently. Pinned to: Task 8's own Step 2 enumerates all 6 files plus the notebook itself as
   separate, individually-checked sub-steps; its reviewer step re-greps the whole repo for the old
   filename string after the builder's own commit.
4. **A builder re-adds a confirmation query where the survey explicitly found one already exists
   downstream**, creating a NEW duplication while fixing the old one. Pinned to: every Pattern-1b
   task's acceptance criteria state explicitly, per notebook, whether a new confirmation cell is
   needed (Ch7-01 only) or an existing one already suffices (every other Pattern-1b instance in
   this plan) — the reviewer checks for exactly the stated outcome, not "a confirmation exists
   somewhere."
5. **A notebook's own cell-execution order breaks** (a cell references a variable from a cell that
   was deleted or reordered). Pinned to: every task's Verification step requires an actual
   end-to-end notebook execution (`jupyter nbconvert --execute --to notebook --stdout <nb>` run
   from the notebook's own directory, exit 0, zero cell errors), not just inspecting the diff.

---

## Standard execution procedure (every chapter task, Tasks 1–9, follows this exactly)

This is the same mechanism this session already used for the DL-092/DL-093 skill fix. Each task
below gives the chapter-specific blast zone and acceptance criteria; apply this procedure to
execute it.

- [ ] **Step A: Create the worktree and branch**

```bash
cd /Users/z/Documents/GitHub/toaster
git worktree add .claude/worktrees/<task-slug> -b phase-b/<task-slug> diagram-text-integration
```

- [ ] **Step B: Write `CONTRACT.md` in that worktree's root**, containing exactly: the task's own
  "Blast zone" list, "Acceptance criteria" (the literal cell content given below), "Non-goals"
  (the literal list given below), and "Verification" (the standard checks: `uv run pytest tests/
  glossary/tests/ -q`; `uv run python scripts/check_construction.py --check`; end-to-end execution
  of every touched notebook; for a Pattern-2 task, the byte/line-range check against the real
  cumulative model file; and, for the five Pattern-2 tasks, a note that a `simulated-learner`
  spot-check follows after merge, per Step F below).

- [ ] **Step C: Dispatch the builder**

Use the `Agent` tool, `subagent_type: "builder"`, prompt: "Work in the git worktree at
`/Users/z/Documents/GitHub/toaster/.claude/worktrees/<task-slug>` (branch `phase-b/<task-slug>`,
based on `diagram-text-integration`). Read `CONTRACT.md` in that worktree's root and execute it
exactly. Commit (no co-author trailer, per this repo's own convention), do not push. Report the
full diff and every check's output."

- [ ] **Step D: Dispatch the reviewer**

Use the `Agent` tool, `subagent_type: "reviewer"`, different model from the builder by
construction (the `reviewer` role is pinned to `claude-opus-5-5`). Prompt: "Review the builder's
commit on branch `phase-b/<task-slug>` in the worktree at
`/Users/z/Documents/GitHub/toaster/.claude/worktrees/<task-slug>`, against that worktree's own
`CONTRACT.md`. Re-run every check yourself; verify every acceptance-criterion cell content
byte-for-byte; verify the blast zone was not exceeded. Report PASS, FAIL, or CANT_TELL with
evidence for each acceptance criterion."

- [ ] **Step E: On PASS, merge**

```bash
git -C /Users/z/Documents/GitHub/toaster merge --no-ff phase-b/<task-slug> -m "Merge phase-b/<task-slug>: <one-line summary>"
git -C /Users/z/Documents/GitHub/toaster push
git -C /Users/z/Documents/GitHub/toaster worktree remove .claude/worktrees/<task-slug>
git -C /Users/z/Documents/GitHub/toaster branch -d phase-b/<task-slug>
```

On FAIL or CANT_TELL: one revision cycle (builder fixes, same reviewer re-checks). A second FAIL or
CANT_TELL routes to the ACE per `orchestrator-protocol`'s own escalation triggers, not back to the
builder a third time.

- [ ] **Step F (Pattern-2 tasks only — Tasks 2, 3, 4, 5, 6): dispatch the `simulated-learner`
  spot-check**, after merge, on the trimmed notebook. Use the `Agent` tool, `subagent_type:
  "simulated-learner"`, with a persona per the `user-testing` skill's own protocol, prompt:
  "Read and execute `<notebook path>` on the merged `diagram-text-integration` branch. Specifically
  check whether the trimmed `print()` cell plus the chapter's own structure diagram still let you
  reconstruct what the chapter's own judgment record (`<the specific judgment record this
  notebook's remainder depends on>`) needs — the attribute values, requirement body, or
  metadata-tag content the diagram cannot show. Report PASS or NEEDS-FIX per the `user-testing`
  skill's fixed report format." If NEEDS-FIX, route to the ACE (this is new reader-facing evidence
  contradicting an already-merged change, not a routine revision cycle).

---

## Task 1: Chapter 1 (System and Purpose)

**Files:**
- Modify: `chapters/ch01-system-purpose/01-abstract-def.ipynb`, `02-part-def.ipynb`,
  `03-specialization.ipynb`, `04-composition.ipynb`

**Blast zone:** exactly these four notebooks. No `index.md` change (survey found no drift).

**Acceptance criteria** (verbatim from the survey's Chapter 1 table):

1. `01-abstract-def.ipynb`, cell 8 (`cell-07`): remove the `print(TOASTER_INCREMENT)` line only.
   Before:
   ```python
   TOASTER_INCREMENT = f"{BREAD_DEF}\n{TOAST_DEF}\n{TOASTBREAD_DEF}\n{TOASTING_SYSTEM_DEF}"
   print(TOASTER_INCREMENT)
   source = Path("../../models/ch01-cumulative.sysml").read_text()
   model = conn.load_from_content(source, strict=False)
   assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
   ```
   After:
   ```python
   TOASTER_INCREMENT = f"{BREAD_DEF}\n{TOAST_DEF}\n{TOASTBREAD_DEF}\n{TOASTING_SYSTEM_DEF}"
   source = Path("../../models/ch01-cumulative.sysml").read_text()
   model = conn.load_from_content(source, strict=False)
   assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
   ```
   No other cell in this notebook changes — cells 12/14's existing `model.find()` calls already
   serve as the confirmation; the existing seam cell (16) already points at them, not at the
   removed print.

2. `02-part-def.ipynb`, cell 6 (`cell-06`): same single-line removal.
   Before: `TOASTER_INCREMENT = f"{HEATING_SYS_DEF}\n{CONTROL_SYS_DEF}"` + `print(TOASTER_INCREMENT)`
   + the load block.
   After: same minus the `print(TOASTER_INCREMENT)` line.
   Cells 11 (bridge) and 12 (diagram) are unchanged — already correctly positioned. The existing
   seam cell (16) already refers to the still-present individual fragment prints and the cell-10
   query, not the removed reprint, so it needs no edit.

3. `03-specialization.ipynb`, cell 4 (`cell-04`): same single-line removal.
   Before: `TOASTER_INCREMENT = TOASTER_SPEC_DEF` + `print(TOASTER_INCREMENT)` + the load block.
   After: same minus the print line.
   Cell 8's existing `toaster.specializations` query already serves as the confirmation; seam cell
   10 is unaffected.

4. `04-composition.ipynb`, cell 8 (`cell-08`) AND seam cell 18 (`cell-13`) both change:
   Cell 8 before:
   ```python
   TOASTER_INCREMENT = f"{TOASTER_DEF}\n{CYCLE_TIME_ATTR}\n{HEATING_PART}\n{CONTROL_PART}\n}}"
   print(TOASTER_INCREMENT)
   source = Path("../../models/ch01-cumulative.sysml").read_text()
   model = conn.load_from_content(source, strict=False)
   assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
   ```
   Cell 8 after: same minus the print line.
   Seam cell 18 before: "`part def Toaster :> ToastingSystem { ... }` printed above loaded without
   error, and `toaster.parts()` returns the two part symbols shown below, confirming the
   composition is now part of the model."
   Seam cell 18 after: "The assembled `Toaster` declaration loaded without error, and the diagram
   above confirms `heating` and `control` are part of the model."
   This is the one notebook in this chapter where the seam cell MUST change — it quotes a literal
   closed-brace block only the removed print ever produced, so leaving it as-is would make it
   factually wrong once the print is gone. Cells 13 (bridge) and 14 (diagram) are unchanged.

**Non-goals:** Do not touch the single-sentence figure captions in `02-part-def.ipynb` cell 13 or
`04-composition.ipynb` cell 15 (survey flagged these as pre-existing style-guide drift, out of
scope for this redesign). Do not touch `index.md` (no drift found).

**Simulated-learner spot-check:** not required (no Pattern-2 trim in this chapter).

---

## Task 2: Chapter 2 (Requirements and Assumptions)

**Files:**
- Modify: `chapters/ch02-requirements/01-requirement-def.ipynb`, `02-assumptions.ipynb`,
  `03-judgment-context.ipynb`

**Blast zone:** exactly these three notebooks. No `index.md` change (survey found no drift).

**Acceptance criteria:**

1. `03-judgment-context.ipynb`, cell 2 (Pattern 2): replace the full `print(source)` dump with an
   excerpt covering only the `TimelyToast` requirement body and the `cycleTime` override line.
   Before:
   ```python
   from pathlib import Path
   import opensysml
   from toaster.report import format_diagnostics

   conn = opensysml.connect(version="v0.9.0")
   source = Path("../../models/ch02-cumulative.sysml").read_text()
   print(source)
   model = conn.load_from_content(source, strict=False)
   assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
   ```
   After:
   ```python
   from pathlib import Path
   import opensysml
   from toaster.report import format_diagnostics

   conn = opensysml.connect(version="v0.9.0")
   source = Path("../../models/ch02-cumulative.sysml").read_text()
   requirement_block = source[source.index("requirement def"):source.index("part nominal")].strip()
   override_line = next(l.strip() for l in source.splitlines() if "attribute :>> cycleTime" in l)
   print(requirement_block)
   print(override_line)
   model = conn.load_from_content(source, strict=False)
   assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
   ```
   Builder must re-verify this still executes correctly against the live `models/ch02-cumulative.sysml`
   (the survey verified this by direct execution against the file as of 2026-10-02; confirm the
   file hasn't changed shape since, and if it has, report a FAIL to the reviewer rather than
   silently adjusting the slice logic).

2. `03-judgment-context.ipynb`, cells 8–12 (newly resolved by DL-093, NOT in the survey's own
   table — this notebook's judgment-record tag anchor, per `toaster-review-protocol`'s own
   now-fixed "assign, not print" rule): locate the cell matching the pattern `TOASTER_INCREMENT =
   <tag fragment variable>` followed immediately by `print(TOASTER_INCREMENT)` (this is the
   anchor-group's own second code cell, per `toaster-review-protocol/SKILL.md`'s documented
   construction-zone shape — the tag fragment itself, e.g. `REVIEW_RECORD_REF_DEF`/`AC001_TAG` or
   however this notebook's own variables are actually named, was already printed in the cell(s)
   immediately before it). Remove only the `print(TOASTER_INCREMENT)` line; keep the assignment.
   Do not touch the markdown narration immediately before or after this cell unless it explicitly
   says "printed above" about the now-removed reprint specifically (if so, reword minimally to
   point at the individual tag-fragment prints instead, matching the style of Task 1's `04-composition.ipynb`
   seam-cell fix above). Confirm the notebook's own later `get_review_record_refs(model)` /
   `Model tag:` print (per the Ch2 survey's own report, this already exists later in the notebook)
   is untouched and still runs — this is the confirmation step DL-093 relies on; do not add a new
   one.

3. `01-requirement-def.ipynb`, cell 8, AND seam cell 13:
   Cell 8 before: `TOASTER_INCREMENT = f"{TIMELY_TOAST_REQ}{CONSTRAINT_BODY}\n}}\n{NOMINAL_PART}"` +
   `print(TOASTER_INCREMENT)` + load block.
   Cell 8 after: same minus the print line.
   Seam cell 13 before: "The `requirement def TimelyToast { doc /* ... */ subject toaster :
   Toaster; require constraint { toaster.cycleTime <= 180.0 [SI::s] } }` printed above loaded
   without error, and `model.find()` returns its symbol while `model.query()` lists it as a
   `RequirementDefinition`, confirming it's now part of the model."
   Seam cell 13 after: "The `TimelyToast` fragments printed above loaded without error, and
   `model.find()`/`model.query()` confirm it's now part of the model."
   (Must change — quotes a closed-brace block only the removed print produced.)

4. `02-assumptions.ipynb`, cell 6, AND seam cell 11:
   Cell 6 before: `TOASTER_INCREMENT = f"{SLOW_PART}\n{CYCLE_OVERRIDE}\n}}"` + `print(TOASTER_INCREMENT)`
   + load block.
   Cell 6 after: same minus the print line.
   Seam cell 11 before: "The `part slow : Toaster { attribute :>> cycleTime = 200.0 [SI::s]; }`
   printed above loaded without error, and `slow.attributes()` returns the overridden symbol shown
   above, confirming the redeclaration is now part of the model."
   Seam cell 11 after: "The `slow` fragments printed above loaded without error, and
   `slow.attributes()` confirms the override is now part of the model."
   (Must change — same reason as item 3.)

**Non-goals:** Do not touch any other cell in `03-judgment-context.ipynb` beyond cell 2 and the
cells-8–12 anchor fix. Do not resolve the `assumption_refs`/record-triad methodological question
this notebook's own judgment record raises (DL-075, closed by DL-084 — not reopened here).

**Simulated-learner spot-check: required**, on `03-judgment-context.ipynb` post-merge. Check
specifically whether the requirement/override excerpt plus the structure diagram still lets the
reader see what the AC-001 judgment record (asserted context) needs: that `TimelyToast` is bound
by a real constraint and that `slow` really overrides `cycleTime` to 200s.

---

## Task 3: Chapter 3 (Measures of Success)

**Files:**
- Modify: `chapters/ch03-measures/01-moe-definition.ipynb`, `02-mop-candidate-eval.ipynb`,
  `03-threshold-judgment.ipynb`, `04-verification-case.ipynb`

**Blast zone:** exactly these four notebooks. No `index.md` change (survey found no drift).

**Acceptance criteria:**

1. `03-threshold-judgment.ipynb`, cell 2 (Pattern 2): replace the full `print(source)` dump (81
   lines as of 2026-10-02 — use the real, current line count, not the spec's stale "83") with:
   ```python
   lines = source.splitlines()
   excerpt = "\n".join(lines[35:47] + ["    ..."] + lines[61:65] + ["    ..."] + lines[66:80])
   print(excerpt)
   ```
   inserted where `print(source)` currently is (keep `source = Path(...).read_text()` and the
   `model = conn.load_from_content(...)` / `assert model.ok` lines unchanged, exactly as the
   survey's own proposed content shows). Builder must re-verify the line ranges `35:47` (the
   `TimelyToast` requirement def + usage), `61:65` (the `slow` override + folded satisfy claim),
   and `66:80` (`TimelyToastTest`) against the live file before committing — if the file has moved
   since 2026-10-02, recompute the ranges by searching for `requirement def TimelyToast`, `part
   slow : Toaster {`, and `verification def TimelyToastTest` rather than trusting the hardcoded
   numbers, and report the new ranges to the reviewer explicitly as a deviation (not a silent
   change).

2. `03-threshold-judgment.ipynb`, cell 13 (second finding, same notebook, already resolved by
   DL-093 and already given full content in the survey): remove the `print(TOASTER_INCREMENT)`
   line only.
   Before: `TOASTER_INCREMENT = AS_C03_TAG` + `print(TOASTER_INCREMENT)`.
   After: `TOASTER_INCREMENT = AS_C03_TAG` (print line removed).
   The existing cell-23 `get_review_record_refs(model)` confirmation, narrated by cell 24, is
   untouched and already serves as the confirmation.

3. `01-moe-definition.ipynb`, cell 11: remove the print line only.
   Before: `TOASTER_INCREMENT = f"{TIMELY_USAGE}\n{AC_C03_TAG}"` + `print(TOASTER_INCREMENT)`.
   After: same minus the print line.
   Existing cell 6 (`model.find`+`model.query` for `TIMELY_USAGE`) and cell 23
   (`get_review_record_refs` for the metadata tag) already serve as confirmations.

4. `02-mop-candidate-eval.ipynb`, cell 4: remove the print line only.
   Before:
   ```python
   SLOW_WITH_CLAIM = (
       "part slow : Toaster {\n"
       "    attribute :>> cycleTime = 200.0 [SI::s];\n"
       f"{SLOW_NOT_SATISFY}\n"
       "}"
   )
   TOASTER_INCREMENT = SLOW_WITH_CLAIM
   print(TOASTER_INCREMENT)

   source = Path("../../models/ch03-cumulative.sysml").read_text()
   model = conn.load_from_content(source, strict=False)
   assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
   ```
   After: same minus the `print(TOASTER_INCREMENT)` line. Existing cell 8 (`satisfy_relationships`
   + `model.eval()`) already serves as the confirmation, narrated by seam cell 10.

5. `04-verification-case.ipynb`, cell 10: remove the print line only.
   Before: `TOASTER_INCREMENT = f"{VERIF_DEF_OPEN}\n{DOC_COMMENT}\n{SUBJECT_DECL}\n{OBJECTIVE_BODY}\n}}"`
   + `print(TOASTER_INCREMENT)` + load block.
   After: same minus the print line. Existing cell 14 (`model.find()`+`model.query()`) already
   serves as the confirmation, narrated by seam cell 15.

**Non-goals:** Do not touch the `TimelyToast` `doc` block's own cross-chapter duplication with
Chapter 2 (survey explicitly declined to touch this as outside Pattern 2's own scope).

**Simulated-learner spot-check: required**, on `03-threshold-judgment.ipynb` post-merge. Check
whether the trimmed excerpt plus the chapter's own parts-only diagram still lets the reader see
`TimelyToast`'s own threshold, the `slow` candidate's failure, and what `TimelyToastTest` checks.

---

## Task 4: Chapter 4 (Functional Decomposition)

**Files:**
- Modify: `chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb`, `02-heating-refinement.ipynb`,
  `03-completeness-check.ipynb`

**Blast zone:** exactly these three notebooks. No `index.md` change (already confirmed accurate).

**Acceptance criteria:**

1. `01-action-def-ffbd.ipynb`, cell 14 (Pattern 1): remove the print line only; cells 15 (bridge)
   and 16 (diagram, renders `ToastBread`) are unchanged.
   Before:
   ```python
   TOASTBREAD_REOPENED = (
       "action def ToastBread {\n"
       "    doc /* Transform bread into toast acceptable to its user. */\n"
       "    in bread : Bread;\n"
       "    out toast : Toast;\n"
       f"{TOASTBREAD_SEQUENCE}\n"
       "}"
   )
   TOASTER_INCREMENT = f"{APPLY_HEAT_DEF}\n{TOASTBREAD_REOPENED}"
   print(TOASTER_INCREMENT)

   source = Path("../../models/ch04-cumulative.sysml").read_text()
   model = conn.load_from_content(source, strict=False)
   assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
   ```
   After: same minus the `print(TOASTER_INCREMENT)` line.

2. `02-heating-refinement.ipynb`, cell 8 (Pattern 1b): remove the print line only.
   Before: `TOASTER_INCREMENT = f"{START_DEF}\n{FINISH_DEF}\n{CANCEL_DEF}"` + `print(TOASTER_INCREMENT)`
   + load block.
   After: same minus the print line. Existing cell 12 (`model.find()` loop over `Start`/`Finish`/`Cancel`)
   already serves as the confirmation.

3. `03-completeness-check.ipynb`, cell 2 (Pattern 2): replace the full 117-line `print(source)`
   dump with:
   ```python
   lines = source.splitlines()
   new_this_chapter = "\n".join(lines[16:32] + lines[37:47] + lines[107:116])
   print(new_this_chapter)
   ```
   (keep `source = Path(...).read_text()` and the load/assert lines unchanged). Builder must
   re-verify ranges `16:32` (`ApplyHeat`), `37:47` (`ToastBread`'s reopened body), `107:116` (the
   three item defs) against the live `models/ch04-cumulative.sysml` before committing, same
   deviation-reporting rule as Task 3 item 1.

4. `03-completeness-check.ipynb`, cells 9–11 (newly resolved by DL-093, NOT in the survey's own
   table — the `AI_C04_TAG` judgment-record anchor): remove only the `print(TOASTER_INCREMENT)`
   line from the cell matching `TOASTER_INCREMENT = AI_C04_TAG` (or however this notebook's own
   variable is named — confirm against the live cell before editing, per the same bounded
   search-and-verify procedure as Task 2 item 2). Keep the assignment. Confirm cell 28's existing
   `tag = next(...); print(f"Model tag: {tag}")` confirmation is untouched and still runs.

**Non-goals:** Do not touch the single-sentence captions in `01-action-def-ffbd.ipynb` cell 17 or
the bridge sentence in `03-completeness-check.ipynb` cell 3 (survey flagged both as pre-existing
style issues, out of scope). Do not reclassify this notebook's own status in
`decisions/declarative-construction-plan.md` (that document's staleness is DL-093's own concern,
not this task's — do not edit that file).

**Simulated-learner spot-check: required**, on `03-completeness-check.ipynb` post-merge. Check
whether the 35-line excerpt plus the chapter's own scoped (`Toaster`/depth-2) diagram still lets
the reader see `ApplyHeat`'s balance constraint, `ToastBread`'s reopened sequence, and the three
item defs well enough to follow the completeness-check judgment record that follows.

---

## Task 5: Chapter 5 (Architecture and Allocation)

**Files:**
- Modify: `chapters/ch05-architecture/01-model-navigation.ipynb`, `02-allocate.ipynb`,
  `03-interfaces.ipynb`, `index.md`

**Blast zone:** exactly these three notebooks plus `index.md`.

**Acceptance criteria:**

1. `01-model-navigation.ipynb`, cell 2 (Pattern 2, residual: none): delete the `print(source)`
   line entirely — no replacement excerpt. The chapter's own unscoped diagram was independently
   confirmed (by both the Ch5 survey agent and the orchestrator's own spot-check against the real
   `figures/ch05-structure.svg`) to cover every structural fact in the dump; this notebook's own
   narrow teaching purpose (`model.find()`/`model.get()` navigation) needs none of the non-structural
   content the dump also showed.

2. `02-allocate.ipynb`, cell 6 (Pattern 1b): remove the print line only.
   Before: `TOASTER_INCREMENT = f"{HEATING_SYSTEM_DEF}\n{TOASTER_WITH_ALLOCATION}"` +
   `print(TOASTER_INCREMENT)` + load block.
   After: same minus the print line. Existing cell 10 (`find_allocations`/`perform_relationships`)
   already serves as the confirmation. Seam cell 12 currently says "The definitions printed above
   loaded without error..." — reword minimally to "The assembled definitions loaded without
   error..." (do not invent new content; this is the same class of fix as Task 1's
   `04-composition.ipynb` and Task 2's seam fixes — only reword the clause that would otherwise
   misdescribe what happened).

3. `03-interfaces.ipynb`, cell 10 (Pattern 1): remove the print line only.
   Before: `TOASTER_INCREMENT = (f"{DURATION_PORT_DEF}\n{HEATING_SYSTEM_PORT}\n{CONTROL_SYSTEM_PORT}\n{TOASTER_WITH_INTERFACE}")`
   + `print(TOASTER_INCREMENT)` + load block.
   After: same minus the print line. Existing cell 14 (`port_type_mismatches`) already serves as
   the confirmation; cell 16's diagram (`render_toolkit_interconnection`) is unchanged. Seam cell 18
   currently says "The port and interface definitions printed above loaded without error..." —
   same minimal reword as item 2 above.

4. `index.md` line 17: fix the heading-case drift.
   Before: `[01: Model Navigation](01-model-navigation.ipynb)`
   After: `[01: model navigation](01-model-navigation.ipynb)`
   (Only the link text's case changes; the rest of the row, and every other row, is untouched.)

**Non-goals:** Do not propose or make any further change to `02-allocate.ipynb` or
`03-interfaces.ipynb` beyond item 2/3 above — the survey's own open question (whether these two
notebooks also re-print the full dump) was investigated and found to be a factual error in the
*prior* `decisions/diagram-survey.md` document, not a real defect in these live files; see Task 10
for the document correction. Do not touch `03-interfaces.ipynb`'s own `render_toolkit_interconnection()`
diagram cell.

**Simulated-learner spot-check: required**, on `01-model-navigation.ipynb` post-merge. Check
specifically whether removing the dump entirely (residual: none) still leaves the reader able to
follow the `model.find()`/`model.get()` navigation this notebook actually teaches, given only the
diagram and cell 1's own prose summary.

---

## Task 6: Chapter 6 (Recursive Decomposition)

**Files:**
- Modify: `chapters/ch06-recursive-decomp/01-subsystem-requirements.ipynb`, `02-second-level.ipynb`,
  `03-stopping-judgment.ipynb`, `index.md`

**Blast zone:** exactly these three notebooks plus `index.md`.

**Acceptance criteria:**

1. `03-stopping-judgment.ipynb`, cell 2 AND markdown wrap-up cell 3 (Pattern 2, the largest cut in
   the tutorial — 213 lines to 66):
   Cell 2 after (replace the full `print(source)` dump with):
   ```python
   lines = source.splitlines()
   print("\n".join(lines[137:164] + lines[173:212]))
   ```
   (keep the `source = Path(...).read_text()` / load / assert lines unchanged). Builder must
   re-verify ranges `137:164` (`EnergyPort` through `HeatGenerator`) and `173:212`
   (`HeatGenerationReq` through `weak`) against the live `models/ch06-cumulative.sysml`, same
   deviation-reporting rule as Task 3/4.
   Cell 3 before: "The cumulative model prints above: `GenerateHeat` nested inside `ApplyHeat`,
   `HeatGenerator` performing it through a declared energy port, `HeatingAssembly` composing that
   carrier, the usage-level allocation between them, and `ResistanceCoil`'s two candidates, `rated`
   and `weak`, checked against `heatGenerationReq`. The next cell checks what happens when an
   inference record's own required field is left empty."
   Cell 3 after: "HeatGenerator, EnergyPort, HeatGenerationReq, ResistanceCoil, rated and weak
   loaded without error, and the diagram confirms HeatingAssembly composing heatGen, typed by
   HeatGenerator. The next cell checks what happens when an inference record's own required field
   is left empty." (Must change — the original names facts, like the allocation, the trimmed print
   no longer shows.)

2. `03-stopping-judgment.ipynb`, cell 11 (second finding, resolved by DL-093 — already given full
   content in the survey, previously flagged "if adopted," now unconditional): remove the print
   line only.
   Before: `TOASTER_INCREMENT = AI_C06_TAG` + `print(TOASTER_INCREMENT)`.
   After: `TOASTER_INCREMENT = AI_C06_TAG` (print line removed; assignment kept — required by
   `scripts/check_construction.py`). Existing cell 22 (`get_review_record_refs`) already serves as
   the confirmation.

3. `01-subsystem-requirements.ipynb`, cell 14 (Pattern 1): remove the print line only.
   Before: `TOASTER_INCREMENT = (f"{GENERATE_HEAT_DEF}\n{ENERGY_PORT_DEF}\n{APPLY_HEAT_INCREMENT}\n{HEAT_GENERATOR_DEF}\n{HEATING_ASSEMBLY_DEF}")`
   + `print(TOASTER_INCREMENT)` + load block.
   After: same minus the print line. The two existing diagrams (action-flow + interconnection)
   immediately after are unchanged; cell 20's "printed above" claim resolves to the still-present
   individual fragment prints (cells 2/4/6/8/10), unaffected.

4. `02-second-level.ipynb` (Phase A coverage gap — the survey's own Ch6 agent did not report on
   this notebook at all, despite being asked to check it; closing that gap is this task's own
   responsibility, not a re-opening of Phase A): read this notebook cell by cell first. If it has
   a construction-zone reflection-print duplication (a `TOASTER_INCREMENT = ...` assignment
   immediately followed by `print(TOASTER_INCREMENT)`, reprinting fragments already printed
   individually above it), apply Pattern 1b exactly as every other instance in this plan: remove
   only the print line, keep the assignment, and confirm whether an existing `model.find()`/
   `model.query()`/`model.eval()` or `query.py`-helper confirmation already exists later in the
   notebook (if so, rely on it and add nothing; if genuinely none exists, add one short confirmation
   cell against the construct this notebook declares, in the same idiom Task 7 item 2 below uses
   for `ch07/01-calc-energy.ipynb`). If this notebook has no construction zone at all, report "no
   construction zone, no finding" to the reviewer — do not force a finding. Report the actual cell
   content found (not a placeholder) in the builder's own report, so the reviewer can verify it
   against the live file directly, the same rigor every other item in this plan already has.

5. `index.md`: fix the heading-case drift in all three rows.
   Before:
   ```
   [01: Level-2 Function and Logical Carrier](01-subsystem-requirements.ipynb)
   [02: Level-2 Physical Realization](02-second-level.ipynb)
   [03: Stopping Judgment](03-stopping-judgment.ipynb)
   ```
   After:
   ```
   [01: level-2 function and logical carrier](01-subsystem-requirements.ipynb)
   [02: level-2 physical realization](02-second-level.ipynb)
   [03: stopping judgment](03-stopping-judgment.ipynb)
   ```
   (Only the link text's case changes in each row; concept-column prose and hrefs untouched.)

**Non-goals:** Do not touch the `assumption_refs` text in cell 16 (survey confirmed it already
supports the Pattern-2 trim correctly; no change needed, verify only). Do not fix the three real
em-dash violations the Ch7 survey found (different chapter, out of this task's blast zone).

**Simulated-learner spot-check: required**, on `03-stopping-judgment.ipynb` post-merge — this is
the single largest cut in the tutorial. Check specifically whether the 66-line excerpt plus the
scoped (`HeatingAssembly`/depth-2) diagram still lets the reader see `HeatGenerationReq`'s own
threshold and both `rated`/`weak` candidates' values well enough to follow the stopping-judgment
record that depends on them.

---

## Task 7: Chapter 7 (Execution and Experiments)

**Files:**
- Modify: `chapters/ch07-execution/01-calc-energy.ipynb`, `02-state-traces.ipynb`

**Blast zone:** exactly these two notebooks (`03-param-sweep.ipynb` and `index.md` are both
confirmed to need no change — the survey found this chapter's own index table already matches its
notebooks byte-for-byte, including the apostrophe form).

**Acceptance criteria:**

1. `02-state-traces.ipynb`, cell 16 (Pattern 1): remove the print line only; cells 17 (bridge) and
   18 (diagram) are unchanged.
   Before: `TOASTER_INCREMENT = f"{CYCLE_DEF}\n{TOASTING_SYSTEM_INCREMENT}"` + `print(TOASTER_INCREMENT)`
   + load block.
   After: same minus the `print(TOASTER_INCREMENT)` line (and its trailing blank line).

2. `01-calc-energy.ipynb`, cell 9 AND markdown cell 10 (Pattern 1b — this is the ONE notebook in
   this entire plan where a genuinely NEW confirmation cell must be added, since no existing query
   elsewhere in the notebook covers this construct):
   Cell 9 before:
   ```python
   TOASTER_INCREMENT = f"{HEAT_GENERATOR_INCREMENT}\n{RATED_INCREMENT}"
   print(TOASTER_INCREMENT)

   source = Path("../../models/ch07-cumulative.sysml").read_text()
   model = conn.load_from_content(source, strict=False)
   assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
   ```
   Cell 9 after:
   ```python
   TOASTER_INCREMENT = f"{HEAT_GENERATOR_INCREMENT}\n{RATED_INCREMENT}"

   source = Path("../../models/ch07-cumulative.sysml").read_text()
   model = conn.load_from_content(source, strict=False)
   assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
   delivered_energy = model.find("ToasterDemo::HeatGenerator::deliveredEnergy")
   print(f"HeatGenerator::deliveredEnergy: kind={delivered_energy.kind!r}, id={delivered_energy.id!r}")
   ```
   Cell 10 (markdown) before: "A constraint that references an attribute the definition never
   declares fails to load. The negative control below asserts a bound on a name `Widget` does not
   have."
   Cell 10 after: "`HeatGenerator::deliveredEnergy` is now part of the loaded model, confirmed by
   `model.find`. A constraint that references an attribute the definition never declares fails to
   load. The negative control below asserts a bound on a name `Widget` does not have."

**Non-goals:** Do not touch `03-param-sweep.ipynb` (confirmed to have no construction zone at all
— `cell 2` loads the cumulative model directly). Do not fix the three em-dash violations in
`02-state-traces.ipynb` cells 29/32, or the two intermediate sub-assembly reprints flagged in the
survey's open questions (cell 12 of `02-state-traces.ipynb`, cell 7 of `01-calc-energy.ipynb`) —
both outside the two named patterns' own scope, per the survey's own explicit flag-not-fix
instruction. Do not touch `index.md` (confirmed byte-for-byte accurate, including the apostrophe
form).

**Simulated-learner spot-check:** not required (no Pattern-2 trim in this chapter; the changes are
small single-line removals plus one short addition, not material prose shrinkage).

---

## Task 8: Chapter 8 (Checking and Revision)

**Files:**
- Modify: `chapters/ch08-checking/01-invariant-def.ipynb` (renamed to
  `01-assert-constraint-def.ipynb`), `02-violation-witness.ipynb`, `index.md`
- Modify (reference updates for the rename): `myst.yml`, `exercises/ch08/exercise.ipynb`,
  `scripts/check_construction.py`, `DEFERRED.md`

**Blast zone:** exactly the two Ch8 notebooks, Ch8's own `index.md`, plus the 5 named cross-chapter
reference files below (not 6 — the rename touches the notebook's own index.md, counted once, plus
5 other files; see Step 2 for the authoritative enumeration matching the survey's own RENAME
section exactly).

**Acceptance criteria:**

1. `01-invariant-def.ipynb`, cell-08 (Pattern 1b): remove the print line only.
   Before: `TOASTER_INCREMENT = f"{HEAT_GEN_CHECK_USAGE}\n{CHECK_DURATION_ATTR}\n\n{DELIVERED_ENERGY_BOUND}\n"`
   + `print(TOASTER_INCREMENT)` + load block.
   After: same minus the print line. Existing cell-09/cell-10 (`model.find()`+`model.query()`)
   already serves as the confirmation. Diagram cells (cell-03a/03b/03d) are already correct —
   confirmed by the survey, no change.

2. `02-violation-witness.ipynb`, cell-20 (Pattern 1b): remove the print line only.
   Before: `TOASTER_INCREMENT = AS_C08_TAG` + `print(TOASTER_INCREMENT)`.
   After: `TOASTER_INCREMENT = AS_C08_TAG` (print line removed). Rely on the existing later
   cell-32/33 `get_review_record_refs` confirmation — do not insert a nearer one (the survey's own
   open question recommended relying on the existing one for parsimony; this plan adopts that
   recommendation).

3. **Rename, exactly as the survey's own RENAME section specifies:**
   - `git mv chapters/ch08-checking/01-invariant-def.ipynb chapters/ch08-checking/01-assert-constraint-def.ipynb`
   - Update `myst.yml` line ~67: `- file: chapters/ch08-checking/01-invariant-def` →
     `- file: chapters/ch08-checking/01-assert-constraint-def`
   - Update `chapters/ch08-checking/index.md` line 17's link target (see item 4 below, same edit).
   - Update `chapters/ch08-checking/02-violation-witness.ipynb`, cell-01 (markdown): `See
     [Ch8-01](01-invariant-def.ipynb) for the construct itself.` → `See
     [Ch8-01](01-assert-constraint-def.ipynb) for the construct itself.` (link target only — the
     surrounding sentence is untouched).
   - Update `exercises/ch08/exercise.ipynb` line ~28: the prose path reference
     `chapters/ch08-checking/01-invariant-def.ipynb` → `chapters/ch08-checking/01-assert-constraint-def.ipynb`.
   - Update `scripts/check_construction.py` line ~280: the registry entry `"path":
     "chapters/ch08-checking/01-invariant-def.ipynb"` → `"path":
     "chapters/ch08-checking/01-assert-constraint-def.ipynb"`.
   - Update `DEFERRED.md` lines ~693 and ~798 (D-029/D-030/D-031's own live "Workaround" notes that
     point at this file by path) — update the path reference only, do not touch surrounding prose.
   - Do NOT touch: `decisions/diagram-survey.md`, `decisions/log.md`, `decisions/audits/ch08-layer-audit.md`,
     `decisions/user-testing-grid/M2-practitioner.md`, `docs/superpowers/plans/2026-10-01-diagram-survey-phase2-plan.md`
     (all historical-record files, per the exact convention the Ch5 rename precedent already
     established — leave the old filename string in all of these). Also do NOT touch this Phase B
     plan file itself or the governing spec (both name the old filename as a record of what Phase A
     found; leave them as-is, per the survey's own explicit recommendation).
   - After the rename, grep the whole repo for the literal string `invariant-def` and confirm the
     only remaining hits are in the 5 historical/ambiguous files just listed as untouched, plus
     this plan document and the governing spec.

4. `index.md`: fix the separator convention (dash → colon) in all three rows, and update row 1's
   link target for the rename.
   Before:
   ```
   | [01 - assert constraint](01-invariant-def.ipynb) | State `deliveredEnergyBoundedBySupply` as a real SysML constraint; confirm it is really in the loaded model. |
   | [02 - proof versus point evaluation](02-violation-witness.ipynb) | Contrast `verify_holds()`'s universal proof with `verify_satisfaction()`'s point evaluation; show the loop catching a fully broken variant as `violated` and a merely weakened variant as `undecided`; record the proof as engineering evidence with its own real limits stated. |
   | [03 - stale record detection](03-revision-flow.ipynb) | Loosen the lemma's own bound; show `check_stale()` marking the existing record for re-review. |
   ```
   After:
   ```
   | [01: assert constraint](01-assert-constraint-def.ipynb) | State `deliveredEnergyBoundedBySupply` as a real SysML constraint; confirm it is really in the loaded model. |
   | [02: proof versus point evaluation](02-violation-witness.ipynb) | Contrast `verify_holds()`'s universal proof with `verify_satisfaction()`'s point evaluation; show the loop catching a fully broken variant as `violated` and a merely weakened variant as `undecided`; record the proof as engineering evidence with its own real limits stated. |
   | [03: stale record detection](03-revision-flow.ipynb) | Loosen the lemma's own bound; show `check_stale()` marking the existing record for re-review. |
   ```
   (Only the separator character and row 1's link target change; concept-column prose untouched.)

**Non-goals:** Do not touch `03-revision-flow.ipynb` (confirmed to have no construction zone).
Do not resolve whether `02-violation-witness.ipynb` should get a nearer confirmation query (survey's
own open question; this plan's item 2 above already adopts the "rely on the existing one" answer —
do not re-litigate).

**Simulated-learner spot-check:** not required (no Pattern-2 trim in this chapter).

---

## Task 9: Chapter 10 (Traceability and Sign-off)

**Files:**
- Modify: `chapters/ch10-traceability-signoff/01-traceability-graph.ipynb`, `index.md`

**Blast zone:** exactly this one notebook plus `index.md` (`02-judgment-synthesis.ipynb` and
`03-engineering-signoff.ipynb` are both confirmed to have no construction zone — no change).

**Acceptance criteria:**

1. `01-traceability-graph.ipynb`, cell 33 (delete) and cell 32 (one-word edit) — already resolved
   as in-scope by DL-093 ("the survey's proposed deletion plus the one-word edit to cell 32
   stands"):
   Cell 32 (markdown) before, last sentence: "The subsetting construct below is how that is
   stated."
   Cell 32 after, last sentence: "The subsetting construct shown above is how that is stated."
   Cell 33 (code) before: `print(ENERGY_CONSERVATION_REQ_DEF)` — a verbatim reprint of cell 27's
   own fragment.
   Cell 33 after: deleted outright. Cell 34's markdown ("`models/ch10-cumulative.sysml` already
   carries this construct forward...") still reads correctly immediately after cell 32 with no
   cell 33 between them.

2. `index.md`: fix the separator convention (dash → colon) in all three rows.
   Before:
   ```
   | [01 - traceability graph](01-traceability-graph.ipynb) | ... |
   | [02 - judgment ledger](02-judgment-synthesis.ipynb) | ... |
   | [03 - engineering synthesis](03-engineering-signoff.ipynb) | ... |
   ```
   After (concept-column text unchanged — only the bracketed link-text prefix in each row
   changes):
   ```
   | [01: traceability graph](01-traceability-graph.ipynb) | ... |
   | [02: judgment ledger](02-judgment-synthesis.ipynb) | ... |
   | [03: engineering synthesis](03-engineering-signoff.ipynb) | ... |
   ```

**Non-goals:** Do not touch `02-judgment-synthesis.ipynb` or `03-engineering-signoff.ipynb` (both
confirmed to have no construction zone). Do not touch the diagram in cell 6 (confirmed unscoped and
unaffected by the cell 33 fix).

**Simulated-learner spot-check:** not required (no Pattern-2 trim; this is a single-cell deletion
plus a one-word wording fix, not material prose shrinkage).

---

## Task 10: Correct the factual error in `decisions/diagram-survey.md` (administrative, not a contract)

**Files:**
- Modify: `decisions/diagram-survey.md`
- Modify: `decisions/log.md` (new DL entry)

This is the orchestrator's own established administrative record-keeping role — the same role used
compiling both `decisions/diagram-survey.md` (Phase 1) and `decisions/diagram-text-integration-survey.md`
(Phase A) — not a builder contract, per spec Decision 3's own carve-out. No worktree, no builder,
no reviewer; the orchestrator makes this edit directly and logs it.

- [ ] **Step 1: Correct the row.**
  `decisions/diagram-survey.md` line 169, currently:
  ```
  | `02-allocate.ipynb` cell-06 / `03-interfaces.ipynb` cell-10 | same 131-line dump, repeated verbatim | — | — | **no candidate** | — | Identical content already shown once in this chapter; a second/third copy would be diagram fatigue, not a real reduction in parsing burden. |
  ```
  Replace with:
  ```
  | `02-allocate.ipynb` cell-06 / `03-interfaces.ipynb` cell-10 | ~~same 131-line dump, repeated verbatim~~ — **correction, 2026-10-02 (diagram/text integration Phase A):** this row was factually wrong. Direct re-read of the live files (and of this document's own commit history) confirms neither cell ever printed the full 131-line dump — each prints only its own small `TOASTER_INCREMENT` fragment (9 and ~15 lines respectively). See `decisions/diagram-text-integration-survey.md`'s own Chapter 5 section for the real finding and fix. | — | — | **no candidate** | — | Identical content already shown once in this chapter; a second/third copy would be diagram fatigue, not a real reduction in parsing burden. (Rationale for "no candidate" stands; the premise describing what these two cells print was wrong, not the conclusion.) |
  ```

- [ ] **Step 2: Log it.**
  Append a new `DL-NNN` entry (next sequential number after whatever Phase B's own skill/chapter
  work has already logged by the time this step runs — check `decisions/log.md`'s own current max
  before assigning) stating: what was wrong (the row above), how it was found (the Ch5 Phase A
  survey agent's direct read plus a `git show` of the commit that produced the original document),
  that the correction is a one-line edit to a historical document's own factually incorrect premise
  (not a reversal of its conclusion), and citing `decisions/diagram-text-integration-survey.md`'s
  own cross-chapter open question 3 as the source.

- [ ] **Step 3: Commit directly** (orchestrator's own administrative role, no worktree needed):
  ```bash
  git add decisions/diagram-survey.md decisions/log.md
  git commit -m "Correct decisions/diagram-survey.md: ch05's claimed triple-dump does not exist in the real files"
  git push
  ```

---

## Self-review

**1. Spec coverage.** Decision 1 (scope: both patterns) → every chapter task covers both Pattern
1/1b and Pattern 2 where applicable. Decision 2 (Approach A) → every Pattern-1 task keeps the
diagram in place and only removes the print; every Pattern-2 task shrinks the dump to the exact
survey-stated residual. Decision 3 (harness) → every chapter task is a CONTRACT.md in its own
worktree with builder sonnet / reviewer opus, zero direct orchestrator edits to chapter content;
Task 10 is explicitly carved out as the one permitted administrative exception, matching the spec's
own Decision 3 language exactly. Decision 4 (enumerated cleanup) → item 1 (index heading drift) in
Tasks 5, 6; item 2 (separator convention) in Tasks 8, 9; item 3 (Ch8 rename) in Task 8; item 4
(D-037) not reopened anywhere in this plan. Decision 5 (durability) → this plan is fully
self-contained; no task depends on this conversation's own history.

**2. Placeholder scan.** Every cell-content before/after pair is quoted verbatim from the survey.
The two genuinely new items not in the survey's own table (Task 2 item 2, Task 4 item 4) are given
as bounded, fully-specified mechanical procedures (find this exact pattern shape, remove only this
one line) rather than vague instructions — this mirrors how Phase A's own agents were given
precise search-and-propose instructions rather than pre-written text in cases where the exact
variable names weren't yet known. Task 6 item 4 (the `02-second-level.ipynb` coverage gap) is
likewise a bounded procedure with an explicit "no finding" fallback, not an open "also look for
stuff" instruction — it closes one specific, named Phase A gap, not a new discovery mandate.

**3. Type consistency.** Every chapter task uses the same acceptance-criteria shape (before/after
code or markdown blocks, quoted verbatim) and the same Non-goals/Simulated-learner-requirement
structure, so the Standard execution procedure applies uniformly across all 9 chapter tasks.

**4. Review Focus.** All five items are pinned to specific tasks and specific verification steps
above, not left to each task's own judgment alone.

## Execution handoff

This plan uses this repo's own established implementation harness — CONTRACT.md per chapter task,
each in its own git worktree, builder `claude-sonnet-5` and reviewer `claude-opus-5-5` (always a
different model), merged by the orchestrator after an independent PASS — exactly the mechanism this
session already used and proved for the DL-092/DL-093 skill fix earlier today. This is not
`writing-plans`' own generic Subagent-driven/Native choice; per spec Decision 5 and
`orchestrator-protocol`'s own "Plan-driven non-chapter work" section, this project's established
contract mechanism is the execution method for this plan, full stop.

Per the spec's own Process section ("these 9 chapters' own text-integration tasks are independent
of each other... and can run in parallel, the same way Phase 2's 9 chapter tasks did"), Tasks 1–9
have no inter-task dependency and may be dispatched in parallel, each in its own worktree. Task 10
(the administrative correction) has no dependency on any other task either and may run at any
point.

Plan complete and saved to `docs/superpowers/plans/2026-10-02-diagram-text-integration-phase-b-plan.md`.
Please review the plan. Does it capture what you want?
