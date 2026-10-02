# Judgment-Record Store — Phase B (Implementation) Plan

> **For agentic workers:** This plan does NOT use `superpowers:subagent-driven-development` or
> `superpowers:executing-plans`. Every task below is a real `CONTRACT` per
> `decisions/work-contract-template.md`'s own exact field format, dispatched in its own git
> worktree per `decisions/task-states.md`'s own state machine and merge-gate rules. See "Execution
> mechanism" below.

**Goal:** Build `src/toaster/judgment_store.py` (persist a `ReviewRecord` once, where it's
authored; load it, never retype it, where it's cited) and retrofit every real citation this
tutorial has, per the Phase A survey's own literal findings.

**Architecture:** One foundation task (the module + tests), then nine notebook-retrofit tasks with
real sequencing dependencies — origin chapters must merge before the citing chapters that load
their records can be built or tested. This is NOT a fully-parallel plan.

**Tech Stack:** Python `dataclasses`/`json`/`pathlib` (no new dependency); `pytest`; `jupyter
nbconvert --execute` for notebook verification; this repo's own `Agent` tool dispatch to `builder`
(`claude-sonnet-5`) and `reviewer` (`claude-opus-5-5`) roles.

**Spec:** `docs/superpowers/specs/2026-10-02-judgment-record-store-design.md`

**Also required reading for every task:** `decisions/judgment-record-store-survey.md` (Phase A's
output — the literal source of every cell quoted below), `decisions/log.md` DL-097 (the gap
analysis that found the problem, with full literal quotes of the Ch9/Ch10 citing-side cells) and
DL-098 (Z's resolution of the survey's two open questions — the Ch8 scope extension and the
unconditional-insertion rule, both binding on this plan).

## Global Constraints

- Every task's blast zone is read-write only within its own named files. Only Task 1 (new module +
  test + README, no chapter files) and Task 6 (two of Ch8's own notebooks, per Z's own scope
  extension in DL-098) touch more than one file outside a single chapter's single notebook.
- Builder is `claude-sonnet-5`; reviewer is `claude-opus-5-5`; never the same model
  (`decisions/work-contract-template.md`'s own Rules line).
- Every task re-runs `uv run pytest tests/ glossary/tests/ -q` and `uv run python
  scripts/check_construction.py --check`, both clean, before the reviewer signs off.
- Every notebook-touching task re-executes every notebook it touches end-to-end (`jupyter
  nbconvert --execute`), zero cell errors.
- Tasks 2–6 each confirm, after execution, that the real JSON file was written under
  `decisions/judgment-records/` and commit it as part of that task's own diff — these are real,
  tracked build artifacts, the same status this repo already gives `figures/*.svg`.
- Tasks 7–8 confirm the hand-typed literal they replace is fully gone from the diff, not left
  alongside the new `load_record()` call.
- `save_record()` is inserted **unconditionally**, immediately after each originating cell's own
  existing `validate_record(...)` call — per DL-098, no new `assert errors == []` gate is added
  anywhere it doesn't already exist. Only Chapter 8's own `AS-C08` cell already has that assert;
  `save_record()` goes after it there specifically.
- Commits are plain, no co-author trailers (`decisions/work-contract-template.md`'s own Rules
  line). No task merges or pushes its own work — the orchestrator owns the merge gate.

## Review Focus

1. **A retrofit accidentally breaks or removes part of a notebook's own existing
   `validate_record`/`assert` logic while adding the new `save_record` line.** Every task's own
   diff-review step must confirm only an *addition*, never a removal, of existing code.
2. **A citing-chapter retrofit breaks downstream logic that depended on the literal's own exact
   field values** — especially Chapter 9's own stale-detection notebook (`check_stale(as_c06,
   source) is True` / `check_stale(as_c08, source) is False` must still hold after the retrofit)
   and Chapter 8's own `check_stale()` demo in `03-revision-flow.ipynb`. Tasks 6 and 7 must
   explicitly re-verify these two assertions still pass, not just that the notebook runs without a
   Python exception.
3. **`save_record()` is called on a record `validate_record()` actually flagged errors on.**
   Confirmed a non-issue in practice today (every real notebook's `validate_record()` call
   currently returns `[]` when executed normally) — but every origin task (2–6) must print and
   inspect the real `Validation errors: []` output as part of its own acceptance evidence, not
   assume it.
4. **JSON round-trip fidelity for `ReviewRecord`'s own list-typed fields** (`premises`,
   `assumption_refs`, `evidence_refs`) — pinned directly in Task 1's own test suite.
5. **A citing task (7 or 8) is dispatched or merged before its dependency origin tasks (2–6) have
   actually merged their own JSON files into the branch**, so `load_record()` fails to find a
   file that doesn't exist yet. Pinned in this plan's own Execution Handoff below as an explicit
   merge order, not just a task list.

---

## Execution mechanism (read before Task 1)

Every task is dispatched exactly as this session's own DL-092/DL-093 skill fix and the
diagram-text-integration Phase B work already proved on this repo:

1. `git worktree add .claude/worktrees/<slug> -b judgment-record-store/<slug>
   judgment-record-store` — base branch is `judgment-record-store`, **not** `main` and **not**
   `diagram-text-integration`.
2. Write `CONTRACT.md` in that worktree's root, using the exact field format below (copied
   directly into the file, not paraphrased).
3. Dispatch the `Agent` tool, `subagent_type: "builder"`, pinned to `claude-sonnet-5`, with the
   contract.
4. On the builder's report, dispatch `subagent_type: "reviewer"`, pinned to `claude-opus-5-5`,
   against the same contract's own Acceptance criteria.
5. On PASS: orchestrator merges (`git merge --no-ff`), pushes, removes the worktree and branch. On
   FAIL/CANT_TELL: one revision cycle; a second one routes to the ACE as an `other-judgment`
   escalation per `decisions/task-states.md`.

**Required merge order** (per this plan's own real dependencies, unlike the diagram-text-integration
Phase B's fully-parallel chapters): **Task 1 must merge before any of Tasks 2–6 start.** **Tasks
2–6 must all merge before Task 7 or Task 8 starts** (Task 7 depends on Tasks 5 and 6's own
committed JSON files for `AS-C06`/`AS-C08`; Task 8 depends on Tasks 3, 4, 5, and 6's own committed
JSON files for `AS-C03`/`AI-C04`/`AC-C06`/`AS-C06`/`AI-C06`/`AS-C08`). **Task 9 has no dependency on
anything in this plan and may run at any point, in parallel with everything else.** Tasks 2–6 are
mutually independent once Task 1 merges and may run in parallel with each other.

---

## Task 1: Build `src/toaster/judgment_store.py`

**Files:**
- Create: `src/toaster/judgment_store.py`
- Create: `tests/test_judgment_store.py`
- Create: `decisions/judgment-records/README.md`

**Interfaces:**
- Produces: `save_record(record: ReviewRecord, store_dir: Path | None = None) -> Path`,
  `load_record(identifier: str, store_dir: Path | None = None) -> ReviewRecord`,
  `records_citing(identifier: str, store_dir: Path | None = None) -> list[ReviewRecord]` — every
  later task in this plan consumes these three names and signatures exactly.

```
CONTRACT JRS-1 | 2026-10-02
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          ready, per decisions/task-states.md
Task:           Build src/toaster/judgment_store.py: a persisted JSON store for ReviewRecord
                (src/toaster/evidence.py), one file per identifier under
                decisions/judgment-records/. Three functions: save_record, load_record,
                records_citing. Full TDD cycle per the steps below.
Context:        docs/superpowers/specs/2026-10-02-judgment-record-store-design.md Decisions 1-2;
                src/toaster/evidence.py (the ReviewRecord dataclass and check_stale, which Step 7
                below exercises against a loaded record); src/toaster/query.py (for the existing
                one-file-per-source / one-module-one-responsibility pattern this new module
                follows).
Non-goals:      Do not modify src/toaster/evidence.py. Do not modify any chapter notebook. Do not
                implement a "list all records" or "delete a record" function -- not named by the
                spec, not needed by any later task in this plan.
Blast zone:     src/toaster/judgment_store.py, tests/test_judgment_store.py,
                decisions/judgment-records/README.md -- on branch judgment-record-store/jrs-1 in
                worktree .claude/worktrees/jrs-1.
Acceptance:     uv run pytest tests/test_judgment_store.py -v -- all new tests pass; uv run pytest
                tests/ glossary/tests/ -q -- full suite clean; uv run python
                scripts/check_construction.py --check -- clean (expected no-op for this task,
                confirm it stays clean regardless).
Premises:       ReviewRecord (src/toaster/evidence.py) is a @dataclass with default __eq__ -- two
                instances with equal field values compare equal; this is what the round-trip test
                below relies on. Verify this against the live file before writing the test (it
                should already be true, since @dataclass defaults to eq=True, but confirm rather
                than assume).
Questions to:   the orchestrator
Report:         branch and commit, model run on, full pytest output, everything flagged and not
                fixed, every premise that did not hold.
```

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_judgment_store.py
from toaster.evidence import ReviewRecord, check_stale, hash_content
from toaster.judgment_store import load_record, records_citing, save_record


def _sample_record(identifier="AC-TEST", premises=None):
    return ReviewRecord(
        identifier=identifier,
        kind="asserted_context",
        claim="A test claim.",
        subject_ref="ToasterDemo::Toaster",
        model_ref="ToasterDemo::Toaster",
        content_hash=hash_content("some model text"),
        scope="A test scope.",
        criteria="A test criterion.",
        premises=premises or [],
        assumption_refs=["AS-TEST-ASSUMPTION"],
        evidence_refs=["some evidence"],
        rationale="A test rationale.",
        counterevidence="A test counterevidence.",
        residual_uncertainties="A test residual uncertainty.",
        disposition="pending",
        dependency_freshness="current",
        engineering_conclusion="undetermined",
        record_kind="worked_example",
    )


def test_save_record_writes_one_json_file_per_identifier(tmp_path):
    record = _sample_record()
    path = save_record(record, store_dir=tmp_path)
    assert path == tmp_path / "AC-TEST.json"
    assert path.exists()


def test_round_trip_save_then_load_returns_equal_record(tmp_path):
    record = _sample_record()
    save_record(record, store_dir=tmp_path)
    loaded = load_record("AC-TEST", store_dir=tmp_path)
    assert loaded == record


def test_records_citing_finds_a_record_whose_premises_names_the_identifier(tmp_path):
    origin = _sample_record(identifier="AC-ORIGIN")
    citing = _sample_record(identifier="AI-CITING", premises=["AC-ORIGIN"])
    unrelated = _sample_record(identifier="AS-UNRELATED")
    save_record(origin, store_dir=tmp_path)
    save_record(citing, store_dir=tmp_path)
    save_record(unrelated, store_dir=tmp_path)

    citers = records_citing("AC-ORIGIN", store_dir=tmp_path)

    assert [r.identifier for r in citers] == ["AI-CITING"]


def test_loaded_record_still_works_with_check_stale(tmp_path):
    record = _sample_record()
    save_record(record, store_dir=tmp_path)
    loaded = load_record("AC-TEST", store_dir=tmp_path)

    assert check_stale(loaded, "some model text") is False
    assert check_stale(loaded, "different model text") is True
```

- [ ] **Step 2: Run to verify failure**

Run: `uv run pytest tests/test_judgment_store.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'toaster.judgment_store'`

- [ ] **Step 3: Write the implementation**

```python
# src/toaster/judgment_store.py
"""Persisted store for ReviewRecord: one JSON file per identifier under decisions/judgment-records/.

A judgment's content is authored once, where it was made (src/toaster/evidence.py's own
ReviewRecord, validated there); this module is the missing second half of that design -- save it,
then load it instead of retyping it in a later chapter. See
docs/superpowers/specs/2026-10-02-judgment-record-store-design.md.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from toaster.evidence import ReviewRecord

SCHEMA_VERSION = 1


def _default_store_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "decisions" / "judgment-records"


def save_record(record: ReviewRecord, store_dir: Path | None = None) -> Path:
    """Persist `record` as decisions/judgment-records/<identifier>.json. Returns the written path."""
    directory = store_dir or _default_store_dir()
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{record.identifier}.json"
    payload = {"schema_version": SCHEMA_VERSION, **asdict(record)}
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path


def load_record(identifier: str, store_dir: Path | None = None) -> ReviewRecord:
    """Load a previously-saved ReviewRecord by its own identifier."""
    directory = store_dir or _default_store_dir()
    data = json.loads((directory / f"{identifier}.json").read_text())
    data.pop("schema_version", None)
    return ReviewRecord(**data)


def records_citing(identifier: str, store_dir: Path | None = None) -> list[ReviewRecord]:
    """Every stored record whose own `premises` list names `identifier`."""
    directory = store_dir or _default_store_dir()
    out = []
    for path in sorted(directory.glob("*.json")):
        data = json.loads(path.read_text())
        if identifier in data.get("premises", []):
            data.pop("schema_version", None)
            out.append(ReviewRecord(**data))
    return out
```

```markdown
<!-- decisions/judgment-records/README.md -->
# Judgment records

One JSON file per `ReviewRecord` (`src/toaster/evidence.py`), named `<identifier>.json`. Written
by `save_record()`, read by `load_record()` and `records_citing()`
(`src/toaster/judgment_store.py`). A chapter notebook that builds a judgment record saves it here
once, where the judgment is made; a later chapter that needs it loads it from here instead of
retyping it. See `docs/superpowers/specs/2026-10-02-judgment-record-store-design.md`.
```

- [ ] **Step 4: Run to verify success**

Run: `uv run pytest tests/test_judgment_store.py -v`
Expected: PASS, 4 passed.

- [ ] **Step 5: Run the full suite and commit**

```bash
uv run pytest tests/ glossary/tests/ -q
uv run python scripts/check_construction.py --check
git add src/toaster/judgment_store.py tests/test_judgment_store.py decisions/judgment-records/README.md
git commit -m "Build src/toaster/judgment_store.py: persist ReviewRecord once, load it thereafter"
```

---

## Task 2: Retrofit Chapter 2 (`AC-001`)

**Files:** Modify `chapters/ch02-requirements/03-judgment-context.ipynb` cell index 24 (id
`cell-17`). Create (via notebook execution) `decisions/judgment-records/AC-001.json`.

**Interfaces:** Consumes `save_record` from Task 1.

```
CONTRACT JRS-2 | 2026-10-02
Role:           builder, model claude-sonnet-5, effort low
Reviewer:       reviewer, model claude-opus-5-5
State:          ready (blocked_on: JRS-1 merged)
Task:           Retrofit chapters/ch02-requirements/03-judgment-context.ipynb to persist AC-001
                via save_record(), per decisions/judgment-record-store-survey.md's own Chapter 2
                section.
Context:        decisions/judgment-record-store-survey.md, "Chapter 2" section, for the cell's
                exact current content; decisions/log.md DL-098 (insert unconditionally, no new
                assert-gate).
Non-goals:      Do not touch any other cell in this notebook. Do not touch any other chapter.
Blast zone:     chapters/ch02-requirements/03-judgment-context.ipynb,
                decisions/judgment-records/AC-001.json (written by executing the notebook) -- on
                branch judgment-record-store/jrs-2 in worktree .claude/worktrees/jrs-2.
Acceptance:     Cell index 24 (id cell-17) gains exactly two new lines: an import of save_record
                from toaster.judgment_store, and `save_record(context_record)` immediately after
                `errors = validate_record(context_record, model=model)`, before the `tag = ...`
                line. `jupyter nbconvert --execute --to notebook --stdout
                03-judgment-context.ipynb` (from chapters/ch02-requirements/) exits 0, zero cell
                errors, and the cell's own printed "Validation errors: []" confirms the record
                validated cleanly before being saved. decisions/judgment-records/AC-001.json
                exists after execution, is valid JSON, and its own "identifier" field equals
                "AC-001". uv run pytest tests/ glossary/tests/ -q and uv run python
                scripts/check_construction.py --check both clean.
Premises:       The cell's current content matches decisions/judgment-record-store-survey.md's own
                quoted text for Chapter 2 exactly -- verify against the live file before editing,
                not assumed from the survey document alone (the survey itself was built by reading
                the live file once; confirm it hasn't drifted since).
Questions to:   the orchestrator
Report:         branch and commit, model run on, the full diff, the executed cell's own printed
                "Validation errors:" line, confirmation the JSON file was written and its content,
                every check's output.
```

- [ ] **Step 1:** Create worktree, write `CONTRACT.md`, dispatch builder.
- [ ] **Step 2:** Dispatch reviewer against the same contract.
- [ ] **Step 3:** Merge on PASS; commit includes both the notebook diff and the new JSON file.

---

## Task 3: Retrofit Chapter 3 (`AC-C03`, `AS-C03`)

**Files:** Modify `chapters/ch03-measures/01-moe-definition.ipynb` cell 23 (id `cell-19`) and
`chapters/ch03-measures/03-threshold-judgment.ipynb` cell 23 (id `cell-17`). Create
`decisions/judgment-records/AC-C03.json` and `decisions/judgment-records/AS-C03.json`.

**Interfaces:** Consumes `save_record` from Task 1.

```
CONTRACT JRS-3 | 2026-10-02
Role:           builder, model claude-sonnet-5, effort low
Reviewer:       reviewer, model claude-opus-5-5
State:          ready (blocked_on: JRS-1 merged)
Task:           Retrofit two Chapter 3 notebooks to persist AC-C03 and AS-C03, per
                decisions/judgment-record-store-survey.md's own Chapter 3 section.
Context:        decisions/judgment-record-store-survey.md, "Chapter 3" section; decisions/log.md
                DL-098.
Non-goals:      Do not touch chapters/ch03-measures/02-mop-candidate-eval.ipynb or
                04-verification-case.ipynb (both confirmed to have no ReviewRecord construction).
                Do not touch any other cell in either edited notebook.
Blast zone:     chapters/ch03-measures/01-moe-definition.ipynb,
                chapters/ch03-measures/03-threshold-judgment.ipynb,
                decisions/judgment-records/AC-C03.json, decisions/judgment-records/AS-C03.json --
                on branch judgment-record-store/jrs-3 in worktree .claude/worktrees/jrs-3.
Acceptance:     01-moe-definition.ipynb cell 23 (id cell-19) gains `save_record(framing_record)`
                immediately after `errors = validate_record(framing_record, model=model)`.
                03-threshold-judgment.ipynb cell 23 (id cell-17) gains
                `save_record(solution_record)` immediately after
                `errors = validate_record(solution_record, model=model)`. Both cells also gain the
                `from toaster.judgment_store import save_record` import. Both notebooks execute
                end to end with zero cell errors; both JSON files exist after execution with the
                correct "identifier" field. uv run pytest tests/ glossary/tests/ -q and uv run
                python scripts/check_construction.py --check both clean.
Premises:       Both cells' current content matches the survey's own quoted text exactly --
                verify against the live files before editing.
Questions to:   the orchestrator
Report:         branch and commit, model run on, the full diff for both notebooks, both executed
                cells' own printed "Validation errors:" lines, confirmation both JSON files were
                written, every check's output.
```

- [ ] **Step 1:** Create worktree, write `CONTRACT.md`, dispatch builder.
- [ ] **Step 2:** Dispatch reviewer against the same contract.
- [ ] **Step 3:** Merge on PASS.

---

## Task 4: Retrofit Chapter 4 (`AI-C04`)

**Files:** Modify `chapters/ch04-functional-decomp/03-completeness-check.ipynb` cell index 28 (id
`cell-22`) and cell index 2 (id `cell-02`, for the import line). Create
`decisions/judgment-records/AI-C04.json`.

**Interfaces:** Consumes `save_record` from Task 1.

```
CONTRACT JRS-4 | 2026-10-02
Role:           builder, model claude-sonnet-5, effort low
Reviewer:       reviewer, model claude-opus-5-5
State:          ready (blocked_on: JRS-1 merged)
Task:           Retrofit chapters/ch04-functional-decomp/03-completeness-check.ipynb to persist
                AI-C04, per decisions/judgment-record-store-survey.md's own Chapter 4 section.
Context:        decisions/judgment-record-store-survey.md, "Chapter 4" section (note: the survey
                itself found the import line to extend is cell index 2, id cell-02, NOT the
                construction cell -- confirm this placement against the live file); decisions/
                log.md DL-098.
Non-goals:      Do not touch chapters/ch04-functional-decomp/01-action-def-ffbd.ipynb or
                02-heating-refinement.ipynb (both confirmed to have no ReviewRecord construction).
Blast zone:     chapters/ch04-functional-decomp/03-completeness-check.ipynb,
                decisions/judgment-records/AI-C04.json -- on branch
                judgment-record-store/jrs-4 in worktree .claude/worktrees/jrs-4.
Acceptance:     Cell index 28 (id cell-22) gains `save_record(inference_record)` immediately
                after `errors = validate_record(inference_record, model=model)`. Cell index 2 (id
                cell-02) gains `from toaster.judgment_store import save_record` alongside its own
                existing `from toaster.evidence import ReviewRecord, hash_content, validate_record`
                import. Notebook executes end to end, zero cell errors.
                decisions/judgment-records/AI-C04.json exists after execution with
                "identifier": "AI-C04". uv run pytest tests/ glossary/tests/ -q and uv run python
                scripts/check_construction.py --check both clean.
Premises:       The construction cell's current content matches the survey's own quoted text
                exactly -- verify against the live file before editing.
Questions to:   the orchestrator
Report:         branch and commit, model run on, the full diff, the executed cell's own printed
                "Validation errors:" line, confirmation the JSON file was written, every check's
                output.
```

- [ ] **Step 1:** Create worktree, write `CONTRACT.md`, dispatch builder.
- [ ] **Step 2:** Dispatch reviewer against the same contract.
- [ ] **Step 3:** Merge on PASS.

---

## Task 5: Retrofit Chapter 6 (`AC-C06`, `AS-C06`, `AI-C06`)

**Files:** Modify `chapters/ch06-recursive-decomp/02-second-level.ipynb` cells 19 and 36, and
`chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb` cell 27. Create
`decisions/judgment-records/AC-C06.json`, `AS-C06.json`, `AI-C06.json`.

**Interfaces:** Consumes `save_record` from Task 1. **Produces:** the three JSON files Tasks 7 and
8 both depend on (`AC-C06`, `AS-C06`, and `AI-C06` — the record whose own `premises` list
`["AC-C06", "AS-C06", "AS-C03", "AI-C04"]` is this tutorial's own clearest `records_citing()`
example).

```
CONTRACT JRS-5 | 2026-10-02
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          ready (blocked_on: JRS-1 merged)
Task:           Retrofit two Chapter 6 notebooks to persist AC-C06, AS-C06, and AI-C06, per
                decisions/judgment-record-store-survey.md's own Chapter 6 section.
Context:        decisions/judgment-record-store-survey.md, "Chapter 6" section; decisions/log.md
                DL-098. AI-C06's own cell 27 ends with conn.close() -- the save_record() insertion
                must come before that, not after.
Non-goals:      Do not touch chapters/ch06-recursive-decomp/01-subsystem-requirements.ipynb
                (confirmed to have no ReviewRecord construction). Do not touch the AI-BAD negative
                control in 03-stopping-judgment.ipynb cell 6 -- it is a deliberately-invalid record
                and is never saved.
Blast zone:     chapters/ch06-recursive-decomp/02-second-level.ipynb,
                chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb,
                decisions/judgment-records/AC-C06.json, decisions/judgment-records/AS-C06.json,
                decisions/judgment-records/AI-C06.json -- on branch
                judgment-record-store/jrs-5 in worktree .claude/worktrees/jrs-5.
Acceptance:     02-second-level.ipynb cell 19 gains `save_record(framing_record)` immediately
                after its own validate_record(...) line; cell 36 gains
                `save_record(selection_record)` the same way.
                03-stopping-judgment.ipynb cell 27 gains `save_record(stopping_judgment)`
                immediately after its own validate_record(...) line, before the cell's trailing
                conn.close(). Both notebooks execute end to end, zero cell errors. All three JSON
                files exist after execution with correct "identifier" fields; AI-C06.json's own
                "premises" field equals ["AC-C06", "AS-C06", "AS-C03", "AI-C04"] exactly (confirm
                this -- it is the data Tasks 7/8's own records_citing() reasoning depends on). uv
                run pytest tests/ glossary/tests/ -q and uv run python
                scripts/check_construction.py --check both clean.
Premises:       All three cells' current content matches the survey's own quoted text exactly --
                verify against the live files before editing.
Questions to:   the orchestrator
Report:         branch and commit, model run on, the full diff for both notebooks, all three
                executed cells' own printed "validation errors" lines, confirmation all three JSON
                files were written with correct content (quote AI-C06.json's own premises field
                specifically), every check's output.
```

- [ ] **Step 1:** Create worktree, write `CONTRACT.md`, dispatch builder.
- [ ] **Step 2:** Dispatch reviewer against the same contract.
- [ ] **Step 3:** Merge on PASS.

---

## Task 6: Retrofit Chapter 8 (`AS-C08`, origin and internal duplicate)

**Files:** Modify `chapters/ch08-checking/02-violation-witness.ipynb` cell index 32 (id
`cell-32`) and `chapters/ch08-checking/03-revision-flow.ipynb` cell 6. Create
`decisions/judgment-records/AS-C08.json`.

**Interfaces:** Consumes `save_record` and `load_record` from Task 1. **Produces:**
`decisions/judgment-records/AS-C08.json`, which Tasks 7 and 8 both depend on.

```
CONTRACT JRS-6 | 2026-10-02
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          ready (blocked_on: JRS-1 merged)
Task:           Two fixes in the same chapter, different in kind -- call this out explicitly so a
                future reader isn't confused why an "origin" task also contains a "load" fix. (1)
                Retrofit chapters/ch08-checking/02-violation-witness.ipynb to persist AS-C08 at its
                own origin. (2) Per Z's own scope extension in decisions/log.md DL-098, retrofit
                chapters/ch08-checking/03-revision-flow.ipynb cell 6 -- which rebuilds AS-C08 a
                SECOND time, by hand, purely as fixture input for that notebook's own
                check_stale() demonstration -- to load_record("AS-C08") instead, closing the exact
                drift risk this whole initiative exists to fix, one chapter earlier than DL-097's
                own Ch9/Ch10-scoped investigation happened to look.
Context:        decisions/judgment-record-store-survey.md, "Chapter 8" section, for both cells'
                exact current content; decisions/log.md DL-098 (the scope extension, and: AS-C08's
                own origin cell ALREADY HAS an assert errors == [] gate -- save_record() goes
                after that existing assert, not a new one).
Non-goals:      Do not touch chapters/ch08-checking/01-assert-constraint-def.ipynb (confirmed no
                ReviewRecord construction). Do not touch the "broken" negative control in
                03-revision-flow.ipynb cell 4 (identifier="", never cited, never saved).
Blast zone:     chapters/ch08-checking/02-violation-witness.ipynb,
                chapters/ch08-checking/03-revision-flow.ipynb,
                decisions/judgment-records/AS-C08.json -- on branch
                judgment-record-store/jrs-6 in worktree .claude/worktrees/jrs-6.
Acceptance:     02-violation-witness.ipynb cell index 32 (id cell-32) gains
                `save_record(record)` immediately after its own existing
                `assert errors == [], f"Validation errors: {errors}"` line, before the final print
                and conn.close(). 03-revision-flow.ipynb cell 6's entire ~25-line
                `record = ReviewRecord(identifier="AS-C08", ...)` literal is replaced with
                `record = load_record("AS-C08")`, importing load_record from
                toaster.judgment_store; the rest of that cell and the following check_stale()
                cells are otherwise unchanged. Both notebooks execute end to end, zero cell errors.
                decisions/judgment-records/AS-C08.json exists after execution with
                "identifier": "AS-C08". 03-revision-flow.ipynb's own check_stale() demonstration
                (the cells immediately after cell 6, which compare the loaded record's
                content_hash against a revised_source string) must produce the SAME stale/current
                verdict as before this retrofit -- re-run and compare explicitly, do not assume
                the load_record() swap is behaviorally transparent just because Task 1's own tests
                confirmed round-trip equality in isolation. uv run pytest tests/ glossary/tests/ -q
                and uv run python scripts/check_construction.py --check both clean.
Premises:       Both cells' current content matches the survey's own quoted text exactly --
                verify against the live files before editing. 02-violation-witness.ipynb's own
                cell-32 assert line is confirmed present (the survey's own finding: this is the
                one originating cell across all of Ch1-8 that already gates on a passing
                validation) -- re-confirm this directly rather than assuming.
Questions to:   the orchestrator
Report:         branch and commit, model run on, the full diff for both notebooks, the origin
                cell's own printed validation-errors line, confirmation the JSON file was written,
                the before-and-after check_stale() verdict comparison for the 03-revision-flow.ipynb
                retrofit specifically, every check's output.
```

- [ ] **Step 1:** Create worktree, write `CONTRACT.md`, dispatch builder.
- [ ] **Step 2:** Dispatch reviewer against the same contract, with particular attention to the
  check_stale() before/after comparison.
- [ ] **Step 3:** Merge on PASS.

---

## Task 7: Retrofit Chapter 9 (load `AS-C06`, `AS-C08` instead of retyping)

**Files:** Modify `chapters/ch09-coverage-sufficiency/02-evidence-completeness.ipynb` cells 6 and
8, and `chapters/ch09-coverage-sufficiency/03-stale-detection.ipynb` cells 6 and 8.

**Interfaces:** Consumes `load_record` from Task 1, and the real `AS-C06.json`/`AS-C08.json` files
from Tasks 5 and 6.

```
CONTRACT JRS-7 | 2026-10-02
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          ready (blocked_on: JRS-1, JRS-5, JRS-6 all merged -- AS-C06.json and AS-C08.json
                must exist in the repository before this task's own notebooks can load them)
Task:           Replace both Chapter 9 notebooks' hand-retyped AS-C06/AS-C08 reconstructions with
                load_record() calls, per decisions/log.md DL-097's own exact quoted cell content
                (both notebooks currently carry byte-identical ~70-line literals).
Context:        decisions/log.md DL-097 for the exact current cell content of both notebooks (the
                literal ReviewRecord(...) constructions this task removes). Pay particular
                attention to 03-stale-detection.ipynb's own staleness-check cell, which asserts
                `check_stale(as_c06, source) is True` and `check_stale(as_c08, source) is False`
                -- these two assertions are the actual teaching point of that notebook and MUST
                still hold, with the same values, after the retrofit.
Non-goals:      Do not touch either notebook's own negative-control cells (AS-BAD in
                02-evidence-completeness.ipynb, the empty-identifier "broken" record in
                03-stale-detection.ipynb) or the placeholder_record demonstration in
                02-evidence-completeness.ipynb -- none of these represent a real citation, per the
                survey's own findings. Do not touch any other cell narrating what AS-C06/AS-C08
                mean -- only the construction cells themselves change.
Blast zone:     chapters/ch09-coverage-sufficiency/02-evidence-completeness.ipynb,
                chapters/ch09-coverage-sufficiency/03-stale-detection.ipynb -- on branch
                judgment-record-store/jrs-7 in worktree .claude/worktrees/jrs-7.
Acceptance:     In both notebooks: the full ReviewRecord(...) construction for as_c06 (currently
                spanning what was cell 6 in each notebook, including the now-unneeded
                `ch06_source = Path("../../models/ch06-cumulative.sysml").read_text()` line) is
                replaced with `as_c06 = load_record("AS-C06")`; the full construction for as_c08
                (cell 8 in each notebook) is replaced with `as_c08 = load_record("AS-C08")`.
                `from toaster.judgment_store import load_record` is added to each notebook's own
                imports. The subsequent `errors = validate_record(as_c06, model=model)` /
                `print(f"AS-C06 validation errors: {errors}")` lines (and the as_c08 equivalent)
                stay -- validating a loaded record against the live model is still meaningful and
                is NOT removed. Both notebooks execute end to end, zero cell errors.
                02-evidence-completeness.ipynb's own word-count/substantive-reading cells (cell 12
                onward) still produce the same qualitative findings quoted in that notebook's own
                markdown narration (AS-C06's counterevidence names a valve-controlled burner and
                Joule heating; AS-C08's names DEFERRED.md D-029/D-030/D-031) -- confirm the loaded
                record's own field content matches, word for word, since load_record() must
                reproduce exactly what save_record() persisted. 03-stale-detection.ipynb's own
                `assert check_stale(as_c06, source) is True` and
                `assert check_stale(as_c08, source) is False` both still pass -- re-run and confirm
                explicitly, this is the Review Focus item most likely to silently break. uv run
                pytest tests/ glossary/tests/ -q and uv run python scripts/check_construction.py
                --check both clean.
Premises:       decisions/judgment-records/AS-C06.json and AS-C08.json exist in the repository at
                the time this task starts (confirm via `ls decisions/judgment-records/` before
                writing any code) -- if either is missing, STOP and report to the orchestrator
                rather than proceeding, since JRS-5/JRS-6 may not actually be merged yet despite
                this contract's own blocked_on field saying they should be.
Questions to:   the orchestrator
Report:         branch and commit, model run on, the full diff for both notebooks, explicit
                before/after confirmation of the two check_stale() assertions in
                03-stale-detection.ipynb, every check's output.
```

- [ ] **Step 1:** Confirm `decisions/judgment-records/AS-C06.json` and `AS-C08.json` exist on the
  `judgment-record-store` branch (i.e. Tasks 5 and 6 have actually merged) before creating this
  task's worktree.
- [ ] **Step 2:** Create worktree, write `CONTRACT.md`, dispatch builder.
- [ ] **Step 3:** Dispatch reviewer against the same contract, with particular attention to the
  staleness-assertion comparison.
- [ ] **Step 4:** Merge on PASS.

---

## Task 8: Retrofit Chapter 10's judgment synthesis (load `AS-C03`, `AI-C04`, `AC-C06`, `AS-C06`, `AI-C06`, `AS-C08`)

**Files:** Modify `chapters/ch10-traceability-signoff/02-judgment-synthesis.ipynb` cells 6, 8, 10,
and 12.

**Interfaces:** Consumes `load_record` from Task 1, and the real JSON files from Tasks 3, 4, 5, 6.

```
CONTRACT JRS-8 | 2026-10-02
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          ready (blocked_on: JRS-1, JRS-3, JRS-4, JRS-5, JRS-6 all merged)
Task:           Replace chapters/ch10-traceability-signoff/02-judgment-synthesis.ipynb's three
                record reconstructions (AS-C06 and AS-C08, both hand-retyped verbatim; AI-C06,
                rebuilt by re-running live queries against a freshly loaded Chapter 6 model rather
                than retyped) with load_record() calls for all three. decisions/log.md DL-097
                called the AI-C06 live-requery approach "the better pattern" relative to retyping
                AS-C06/AS-C08 -- state explicitly in this task's own commit message why that
                praised pattern is ALSO being replaced here: now that AI-C06 itself is persisted
                at its own origin (Chapter 6, Task 5 of this plan), re-deriving it from scratch via
                live queries every time it's needed is itself a redundant pattern once the store
                exists, per spec Decision 4 ("loaded, never re-typed, at the point of citation").
Context:        decisions/log.md DL-097 for the exact current cell content (all three
                constructions, plus the live-query cell AI-C06's own evidence_refs are built from).
                AI-C06's own `premises` field is `["AC-C06", "AS-C06", "AS-C03", "AI-C04"]` --
                this notebook's cell 1 own narration already explains this is "the clearest
                example in this tutorial of Hawkins' own 'child claims supporting a parent'
                idea"; after this retrofit, that explanation stays accurate since
                load_record("AI-C06") returns the exact same premises list.
Non-goals:      Do not touch chapters/ch10-traceability-signoff/01-traceability-graph.ipynb or
                03-engineering-signoff.ipynb -- those are Task 9's own blast zone, a fully
                independent fix. Do not touch the AI-BAD negative control in this notebook's own
                cell 4. Do not touch cell 14 (the ledger-printing/assertion cell) beyond whatever
                is strictly necessitated by the variable names staying the same (as_c06, as_c08,
                ai_c06) -- it should need no change at all if the loaded objects are assigned to
                the same variable names the removed constructions used.
Blast zone:     chapters/ch10-traceability-signoff/02-judgment-synthesis.ipynb -- on branch
                judgment-record-store/jrs-8 in worktree .claude/worktrees/jrs-8.
Acceptance:     Cell 6 (as_c06 construction, including its own now-unneeded
                `ch06_source = Path(...)` line) replaced with `as_c06 = load_record("AS-C06")`.
                Cell 8 (as_c08 construction, including `ch08_source = Path(...)`) replaced with
                `as_c08 = load_record("AS-C08")`. Cell 10 (the live perform_relationships/
                find_allocations/model.eval cell, whose only purpose was feeding AI-C06's own
                construction) is REMOVED ENTIRELY -- confirm nothing else in the notebook
                references `performs`, `allocations`, `rated_holds`, or `weak_holds` before
                removing it. Cell 12 (the ai_c06 construction) replaced with
                `ai_c06 = load_record("AI-C06")`. `from toaster.judgment_store import load_record`
                added to the notebook's own imports. Cell 14's own ledger-printing/assertion logic
                (iterating `ledger = {"AS-C06": as_c06, "AS-C08": as_c08, "AI-C06": ai_c06}`)
                requires no change and still passes its own
                `assert all(r.disposition == "pending" for r in ledger.values())` and
                `assert all(r.record_kind == "worked_example" for r in ledger.values())`
                assertions. Notebook executes end to end, zero cell errors. The notebook's own
                markdown narration in cells 5, 7, and 9 (which describes each record's content)
                remains accurate against the loaded objects' real field values -- spot-check at
                least one quoted fact per record (e.g. AS-C06's own counterevidence mentioning a
                valve-controlled burner) against the loaded object directly. uv run pytest tests/
                glossary/tests/ -q and uv run python scripts/check_construction.py --check both
                clean.
Premises:       decisions/judgment-records/AS-C03.json, AI-C04.json, AC-C06.json, AS-C06.json,
                AI-C06.json, and AS-C08.json all exist in the repository at the time this task
                starts (confirm via `ls decisions/judgment-records/` before writing any code) --
                if any is missing, STOP and report to the orchestrator.
Questions to:   the orchestrator
Report:         branch and commit, model run on, the full diff, confirmation cell 10 was removed
                cleanly with no dangling references, confirmation cell 14's own two assertions
                still pass, the spot-checked narration-vs-loaded-field comparison, every check's
                output.
```

- [ ] **Step 1:** Confirm all six dependency JSON files exist on the `judgment-record-store`
  branch before creating this task's worktree.
- [ ] **Step 2:** Create worktree, write `CONTRACT.md`, dispatch builder.
- [ ] **Step 3:** Dispatch reviewer against the same contract, with particular attention to cell
  10's clean removal and cell 14's unchanged assertions.
- [ ] **Step 4:** Merge on PASS.

---

## Task 9: Chapter 10's two independent authoring-bug fixes, plus one `DEFERRED.md` entry

**Files:** Modify `chapters/ch10-traceability-signoff/01-traceability-graph.ipynb` cells 8 and 17;
`chapters/ch10-traceability-signoff/03-engineering-signoff.ipynb` cell 19; create one new entry in
`DEFERRED.md`.

**Interfaces:** None — fully independent of every other task in this plan.

```
CONTRACT JRS-9 | 2026-10-02
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          ready (no blocked_on -- independent of every other task in this plan, may run at
                any time)
Task:           Two authoring-bug fixes in Chapter 10, both already found by DL-097 (a notebook
                retyping, as a fresh literal, a fact a prior cell in the SAME notebook already
                computed into a live variable -- nothing to do with the judgment-record store
                itself). Plus one DEFERRED.md entry for a real, previously-untracked tool gap
                found in the same chapter.
Context:        decisions/log.md DL-097 for the full narrative context. The two bugs, with their
                real current cell content (verify against the live files before editing, this
                plan's own quoted text may have drifted):

                (1) chapters/ch10-traceability-signoff/01-traceability-graph.ipynb cell 17 builds a
                `traceability_graph` list of two dicts. Each dict's own "allocation" key is a
                hand-typed string (e.g. "heatGenAllocation: applyHeat.generateHeat -> heatGen
                (nested in HeatingAssembly)" for the first row, "heatAllocation:
                toastBread.applyHeat -> heating (nested in Toaster)" for the second) that restates,
                as fresh prose, exactly what `heatgen_allocations` (computed in cell 10, via
                `allocations_for(model, "ToasterDemo::HeatingAssembly::heatGen", inherit=True,
                index=idx)`) and `toaster_allocations` (computed in cell 13, via
                `allocations_for(model, "ToasterDemo::Toaster::heating", inherit=True,
                index=idx)`) already returned. Fix: generate each "allocation" string from
                `heatgen_allocations[0]` / `toaster_allocations[0]` respectively (each element is a
                dict shaped `{id, type, ends}` per `src/toaster/query.py`'s own `find_allocations`
                docstring) rather than a fresh literal. The exact f-string format is NOT specified
                here -- as a first step, run the notebook up through cell 13 and inspect the real
                printed shape of `heatgen_allocations[0]` and `toaster_allocations[0]` with your
                own eyes before writing the replacement line, then confirm the resulting printed
                "allocation" text still describes the same real facts (same allocation id, same
                two ends) as the current literal, even if the exact phrasing differs since it is
                now generated rather than hand-typed.

                (2) chapters/ch10-traceability-signoff/03-engineering-signoff.ipynb cell 19 builds
                a `premises` list for the AI-C10 synthesis record. Its first element is a long
                hand-typed string restating `heatGenerationReq`'s and `timely`'s own coverage
                facts (e.g. "heatGenerationReq covered=True (satisfied_by=['rated'],
                failed_by=['weak'])...") that were already computed into the `coverage` dict in
                cell 7, twelve cells earlier in the same notebook, and already asserted against
                directly there (`assert coverage["ToasterDemo::heatGenerationReq"]["covered"] is
                True`, etc.). Fix: convert this bullet into an f-string that interpolates the real
                values from `coverage["ToasterDemo::heatGenerationReq"]` and
                `coverage["ToasterDemo::timely"]` (and `tied_to_a_requirement`/`ties` for the
                deliveredEnergyBoundedBySupply clause in the same bullet) directly, the same
                pattern chapters/ch10-traceability-signoff/02-judgment-synthesis.ipynb's own
                AI-C06 construction already uses for ITS evidence_refs (f-strings pulling from
                `performs`/`allocations`/`rated_holds`/`weak_holds`). Do not touch the other three
                elements of this premises list (the AS-C06/AS-C08/AI-C06/AC-C10 summary bullets) --
                those are citations by identifier and conclusion, not raw query-result restatement,
                and are not the bug DL-097 found.

                (3) chapters/ch10-traceability-signoff/01-traceability-graph.ipynb cell 8 defines
                `requirement_subject()`, which reads each candidate feature's own `sysx:sourceText`
                in the API-JSON export for the literal `subject` keyword, because (per DL-097's own
                live probe) the API export has no `subjectParameter` key on `RequirementDefinition`
                to read structurally instead. This gap has no DEFERRED.md entry today (confirmed:
                grep DEFERRED.md for "subjectParameter" and "sourceText", zero hits). Add one new
                entry, following this file's own existing entry format exactly (read a few
                existing entries first to match the format), describing: the gap (no structural
                `subjectParameter` access, forcing a text-scrape workaround), where it's worked
                around (this cell, cite the file and function name), and that it's tracked but not
                blocking (the workaround is correct and already in place). Add a one-line code
                comment in cell 8 itself pointing at the new entry's own D-number.
Non-goals:      Do not touch anything related to the judgment-record store itself (no save_record/
                load_record call anywhere in this task). Do not touch
                chapters/ch10-traceability-signoff/02-judgment-synthesis.ipynb (Task 8's own blast
                zone). Do not touch ac_c10_summary (cell 10) or ledger_summary (cell 12) in
                03-engineering-signoff.ipynb -- both are already correctly-scoped minimal
                citations by identifier and conclusion, not the bug this task fixes.
Blast zone:     chapters/ch10-traceability-signoff/01-traceability-graph.ipynb,
                chapters/ch10-traceability-signoff/03-engineering-signoff.ipynb, DEFERRED.md -- on
                branch judgment-record-store/jrs-9 in worktree .claude/worktrees/jrs-9.
Acceptance:     Both fixes produce a diff that is generated-from-a-variable, not hand-typed, per
                the Context field's own description. Both notebooks execute end to end, zero cell
                errors, and each fixed cell's own printed output still states the same real facts
                the removed literal stated (confirm by reading the new printed output, not by
                assuming the f-string is correct). DEFERRED.md gains exactly one new, correctly
                numbered entry (confirm the next sequential D-number by reading the file's own
                last entry first) matching the file's own existing format. uv run pytest tests/
                glossary/tests/ -q and uv run python scripts/check_construction.py --check both
                clean.
Premises:       All three target cells' current content matches what this contract's own Context
                field describes -- verify against the live files before editing, and if any has
                drifted (especially cell/variable names, since this plan was written from a
                snapshot), report the actual current state to the orchestrator rather than silently
                adapting the fix to something materially different from what's specified here.
Questions to:   the orchestrator
Report:         branch and commit, model run on, the full diff for both notebooks and DEFERRED.md,
                the real printed output of both fixed cells (to confirm the facts stated didn't
                change), the new DEFERRED.md entry's own D-number, every check's output.
```

- [ ] **Step 1:** Create worktree, write `CONTRACT.md`, dispatch builder.
- [ ] **Step 2:** Dispatch reviewer against the same contract.
- [ ] **Step 3:** Merge on PASS. (No dependency on any other task — may happen before, during, or
  after Tasks 1–8.)

---

## Self-review

**1. Spec coverage.** Decision 1 (module location, API) → Task 1. Decision 2 (one file per
record) → Task 1's own `save_record` implementation. Decision 3 (authored once, at construction)
→ Tasks 2–6. Decision 4 (loaded, never re-typed) → Tasks 7–8 (and Task 6's own second half, the
Ch8-internal duplicate). Decision 5 (scope boundary) → every origin task's own Non-goals
explicitly names which notebooks in that chapter are NOT touched because their own records are
never cited; DL-098's extension of that boundary to Ch8's own duplicate is Task 6's own explicit
charge.

**2. Placeholder scan.** Every task's Acceptance criteria name exact cells, exact variable names,
and exact current content (quoted from the survey/DL-097 directly), except Task 9 item 1's own
exact f-string text, which is deliberately left to the builder's own live inspection rather than
guessed — the Context field names exactly what data to pull from (`heatgen_allocations[0]`) and
what the result must still say (the same real allocation facts), which is a concrete,
checkable instruction, not a vague "add appropriate formatting."

**3. Type consistency.** `save_record`/`load_record`/`records_citing`'s exact names and signatures
are defined once in Task 1 and used identically (never renamed, never given different parameter
order) in every later task's own Acceptance criteria.

**4. Review Focus.** All five items are pinned to specific tasks: item 1 (accidental breakage) to
every task's own diff-review requirement; item 2 (staleness logic) explicitly to Tasks 6 and 7;
item 3 (saving an invalid record) to every origin task's own "print and inspect Validation errors"
requirement; item 4 (JSON round-trip) directly to Task 1's own test suite; item 5 (sequencing) to
this plan's own Execution Handoff below.

## Execution handoff

This plan uses this repo's own real development harness: `decisions/work-contract-template.md`'s
exact `CONTRACT` field format for every task, `decisions/task-states.md`'s own state machine and
merge-gate rules, worktrees cut from the `judgment-record-store` branch (not `main`, not
`diagram-text-integration`), builder `claude-sonnet-5` and reviewer `claude-opus-5-5` always on
different models. This is explicitly stated here rather than offering `writing-plans`' own generic
Subagent-driven/Native choice, per the spec's own Process section and this session's own
established practice.

**This is NOT a fully-parallel plan.** Required order: **Task 1 first, alone.** Once it merges,
**Tasks 2–6 may run in parallel with each other** (they touch disjoint chapters' files). **Only
once every one of Tasks 2–6 has merged** may Task 7 and Task 8 start (each depends on specific
JSON files those tasks produce — see each task's own `blocked_on` and Premises fields for exactly
which ones). **Task 9 has no dependency on anything in this plan and may run at any point**,
including right now, in parallel with Task 1.

Plan complete and saved to
`docs/superpowers/plans/2026-10-02-judgment-record-store-phase-b-plan.md`. Please review the plan.
Does it capture what you want?
