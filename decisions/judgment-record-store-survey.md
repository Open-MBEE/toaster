# Judgment-Record Store Survey

Compiled from 8 parallel chapter-survey agents (2026-10-02), per
`docs/superpowers/specs/2026-10-02-judgment-record-store-design.md`. Each chapter section reports
what that chapter's own agent found, with exact cell content quoted directly from each agent's own
report. The citation graph cross-references this document's own originating-side findings against
`decisions/log.md` DL-097's own already-completed citing-side findings for Ch9 and Ch10.

## Chapter 1: System and Purpose

**No `ReviewRecord` construction found.** All four notebooks read in full (68 cells total);
confirmed by both a cell-by-cell read and a repo-relative grep for `ReviewRecord`, `validate_record`,
`save_record`, `load_record` (zero matches). Chapter 1 contributes nothing to the citation graph
and needs no Phase B retrofit task.

## Chapter 2: Requirements and Assumptions

Notebooks 01 and 02 contain no `ReviewRecord` construction (confirmed by full read and grep).
Notebook 03 (`03-judgment-context.ipynb`) builds exactly one record.

**`AC-001`** — `chapters/ch02-requirements/03-judgment-context.ipynb`, cell index 24 (id `cell-17`):
```python
from toaster.query import get_review_record_refs

context_record = ReviewRecord(
    identifier="AC-001",
    kind="asserted_context",
    claim=claim,
    subject_ref=subject_ref,
    model_ref=model_ref,
    content_hash=hash_content(source),
    scope=scope,
    criteria=criteria,
    premises=premises,
    assumption_refs=assumption_refs,
    evidence_refs=evidence_refs,
    rationale=rationale,
    counterevidence=counterevidence,
    residual_uncertainties=residual_uncertainties,
    disposition="pending",
    dependency_freshness="current",
    engineering_conclusion="undetermined",
    record_kind="worked_example",
)

errors = validate_record(context_record, model=model)
tag = next((t for t in get_review_record_refs(model) if t["identifier"] == context_record.identifier), None)
print(f"Record: {context_record.identifier} | kind: {context_record.kind}")
print(f"Claim: {context_record.claim}")
print(f"Model tag: {tag}")
print(f"Validation errors: {errors}")
conn.close()
```
Construction and `validate_record` are co-located in this one cell; no gate on `errors` before
continuing. **Cited forward:** yes (confirmed set). **Proposed insertion** — immediately after the
`validate_record(...)` line, before `tag = ...` and before `conn.close()`:
```python
errors = validate_record(context_record, model=model)
save_record(context_record)
tag = next((t for t in get_review_record_refs(model) if t["identifier"] == context_record.identifier), None)
```

## Chapter 3: Measures of Success

Notebooks 02 and 04 contain no `ReviewRecord` construction (confirmed by full read). Notebooks 01
and 03 each build one.

**`AC-C03`** — `chapters/ch03-measures/01-moe-definition.ipynb`, cell index 23 (id `cell-19`):
```python
framing_record = ReviewRecord(
    identifier="AC-C03",
    kind="asserted_context",
    claim=claim, subject_ref=subject_ref, model_ref=model_ref,
    content_hash=hash_content(source), scope=scope, criteria=criteria,
    premises=premises, assumption_refs=assumption_refs, evidence_refs=evidence_refs,
    rationale=rationale, counterevidence=counterevidence,
    residual_uncertainties=residual_uncertainties,
    disposition="pending", dependency_freshness="current",
    engineering_conclusion="undetermined", record_kind="worked_example",
)
errors = validate_record(framing_record, model=model)
tag = next((t for t in get_review_record_refs(model) if t["identifier"] == framing_record.identifier), None)
print(f"Model tag: {tag}")
print(f"Validation errors: {errors}")
print(f"Record kind:       {framing_record.kind}")
conn.close()
```
No gate on `errors`. **Cited forward:** yes (confirmed set). **Proposed insertion:**
`save_record(framing_record)` immediately after the `validate_record(...)` line, before `tag = ...`.

**`AS-C03`** — `chapters/ch03-measures/03-threshold-judgment.ipynb`, cell index 23 (id `cell-17`):
```python
solution_record = ReviewRecord(
    identifier="AS-C03",
    kind="asserted_solution",
    claim=claim, subject_ref=subject_ref, model_ref=model_ref,
    content_hash=hash_content(source), scope=scope, criteria=criteria,
    premises=premises, assumption_refs=assumption_refs, evidence_refs=evidence_refs,
    rationale=rationale, counterevidence=counterevidence,
    residual_uncertainties=residual_uncertainties,
    disposition="pending", dependency_freshness="current",
    engineering_conclusion="supported", record_kind="worked_example",
)
errors = validate_record(solution_record, model=model)
tag = next((t for t in get_review_record_refs(model) if t["identifier"] == solution_record.identifier), None)
print(f"Model tag: {tag}")
print(f"Validation errors: {errors}")
print(f"Record kind:       {solution_record.kind}")
conn.close()
```
No gate on `errors`. **Cited forward:** yes (confirmed set). **Proposed insertion:**
`save_record(solution_record)` immediately after the `validate_record(...)` line, before `tag = ...`.

## Chapter 4: Functional Decomposition

Notebooks 01 and 02 contain no `ReviewRecord` construction (confirmed by full read and grep).
Notebook 03 builds exactly one record.

**`AI-C04`** — `chapters/ch04-functional-decomp/03-completeness-check.ipynb`, cell index 28 (id
`cell-22`):
```python
from toaster.query import get_review_record_refs

inference_record = ReviewRecord(
    identifier="AI-C04",
    kind="asserted_inference",
    claim=claim, subject_ref=subject_ref, model_ref=model_ref,
    content_hash=hash_content(source), scope=scope, criteria=criteria,
    premises=premises, assumption_refs=assumption_refs, evidence_refs=evidence_refs,
    rationale=rationale, counterevidence=counterevidence,
    residual_uncertainties=residual_uncertainties,
    disposition="pending", dependency_freshness="current",
    engineering_conclusion="supported", record_kind="worked_example",
)

errors = validate_record(inference_record, model=model)
tag = next((t for t in get_review_record_refs(model) if t["identifier"] == inference_record.identifier), None)
print(f"Model tag: {tag}")
print(f"Validation errors: {errors}")
print(f"Record kind:       {inference_record.kind}")
conn.close()
```
No gate on `errors`. **Cited forward:** yes (confirmed set — also independently corroborated by
repo-wide grep hits in `ch06/03-stopping-judgment.ipynb:468` and
`ch10/02-judgment-synthesis.ipynb:413`, both as a `premises` entry for `AI-C06`). **Proposed
insertion:** `save_record(inference_record)` immediately after the `validate_record(...)` line,
before `tag = ...`. Requires adding `from toaster.judgment_store import save_record` alongside the
existing `from toaster.evidence import ReviewRecord, hash_content, validate_record` import in cell
index 2 (id `cell-02`).

## Chapter 5: Architecture and Allocation

**No `ReviewRecord` construction found.** All three notebooks read in full (46 cells total);
confirmed by grep (zero matches for `ReviewRecord`, `validate_record`, `save_record`,
`load_record`) and by direct content read (navigation, allocation, and port/interface content
only — no judgment-record machinery anywhere). Chapter 5 contributes nothing to the citation
graph.

## Chapter 6: Recursive Decomposition

Notebook 01 contains no `ReviewRecord` construction. Notebook 02 builds two; notebook 03 builds
one real record plus one negative-control record.

**`AC-C06`** — `chapters/ch06-recursive-decomp/02-second-level.ipynb`, cell 19:
```python
framing_record = ReviewRecord(
    identifier="AC-C06", kind="asserted_context",
    claim=framing_claim, subject_ref=framing_subject_ref, model_ref=framing_model_ref,
    content_hash=hash_content(source), scope=framing_scope, criteria=framing_criteria,
    premises=framing_premises, assumption_refs=framing_assumption_refs,
    evidence_refs=framing_evidence_refs, rationale=framing_rationale,
    counterevidence=framing_counterevidence,
    residual_uncertainties=framing_residual_uncertainties,
    disposition="pending", dependency_freshness="current",
    engineering_conclusion="undetermined", record_kind="worked_example",
)
errors = validate_record(framing_record, model=model)
tag = next((t for t in get_review_record_refs(model) if t["identifier"] == framing_record.identifier), None)
print(f"Model tag: {tag}")
print(f"Validation errors: {errors}")
```
`subject_ref` = `"ToasterDemo::heatGenerationReq"`. No gate on `errors`. **Cited forward:** yes
(confirmed set). **Proposed insertion:** `save_record(framing_record)` immediately after the
`validate_record(...)` line in cell 19.

**`AS-C06`** — same notebook, cell 36:
```python
selection_record = ReviewRecord(
    identifier="AS-C06", kind="asserted_solution",
    claim=selection_claim, subject_ref=selection_subject_ref, model_ref=selection_model_ref,
    content_hash=hash_content(source), scope=selection_scope, criteria=selection_criteria,
    premises=selection_premises, assumption_refs=selection_assumption_refs,
    evidence_refs=selection_evidence_refs, rationale=selection_rationale,
    counterevidence=selection_counterevidence,
    residual_uncertainties=selection_residual_uncertainties,
    disposition="pending", dependency_freshness="current",
    engineering_conclusion="undetermined", record_kind="worked_example",
)
errors = validate_record(selection_record, model=model)
tag = next((t for t in get_review_record_refs(model) if t["identifier"] == selection_record.identifier), None)
print(f"Model tag: {tag}")
print(f"Validation errors: {errors}")
```
`subject_ref` = `"ToasterDemo::ResistanceCoil"`. No gate on `errors`. **Cited forward:** yes
(confirmed set). **Proposed insertion:** `save_record(selection_record)` immediately after the
`validate_record(...)` line in cell 36.

**`AI-C06`** — `chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb`, cell 27:
```python
stopping_judgment = ReviewRecord(
    identifier="AI-C06", kind="asserted_inference",
    claim=claim, subject_ref=subject_ref, model_ref=model_ref,
    content_hash=hash_content(source), scope=scope, criteria=criteria,
    premises=premises, assumption_refs=assumption_refs, evidence_refs=evidence_refs,
    rationale=rationale, counterevidence=counterevidence,
    residual_uncertainties=residual_uncertainties,
    disposition="pending", dependency_freshness="current",
    engineering_conclusion="undetermined", record_kind="worked_example",
)
errors = validate_record(stopping_judgment, model=model)
tag = next((t for t in get_review_record_refs(model) if t["identifier"] == stopping_judgment.identifier), None)
print(f"Model tag: {tag}")
print(f"Validation errors: {errors}")
print(f"Premises: {stopping_judgment.premises}")
conn.close()
```
`premises` (set in cell 21) = `["AC-C06", "AS-C06", "AS-C03", "AI-C04"]` — this is the live
argument-structure data `records_citing()` is built to walk; `AI-C06` itself cites two records
authored earlier in this same chapter plus two from earlier chapters. No gate on `errors`.
**Cited forward:** yes (confirmed set). **Proposed insertion:** `save_record(stopping_judgment)`
immediately after the `validate_record(...)` line, before `conn.close()`.

**Negative control, not a retrofit target:** `03-stopping-judgment.ipynb` cell 6 builds
`incomplete` (`identifier="AI-BAD"`, empty `premises`) specifically to demonstrate
`validate_record()` rejecting an `asserted_inference` with no premises (Hawkins §3.1). Repo-wide
grep for `AI-BAD` found a same-named construction in `ch10/02-judgment-synthesis.ipynb` and
`exercises/ch10/exercise.ipynb` — confirmed, on inspection, to be an independently-built,
self-contained negative control reusing the same placeholder identifier string, not a citation of
this record (no `premises` link, no load dependency). No `save_record()` needed.

## Chapter 7: Execution and Experiments

**No `ReviewRecord` construction found.** All three notebooks read in full (68 cells total);
confirmed by grep (zero matches) and direct content read (energy calculation, state traces,
parameter sweep — no judgment-record vocabulary anywhere). Chapter 7 contributes nothing to the
citation graph.

## Chapter 8: Checking and Revision

Notebook 01 contains no `ReviewRecord` construction. Notebook 02 builds the chapter's one real
record; notebook 03 builds a negative control plus a third, undercounted duplicate of that same
record.

**`AS-C08`** — `chapters/ch08-checking/02-violation-witness.ipynb`, cell index 32 (id `cell-32`):
```python
from toaster.query import get_review_record_refs

record = ReviewRecord(
    identifier="AS-C08", kind="asserted_solution",
    claim=claim, subject_ref=subject_ref, model_ref=model_ref,
    content_hash=hash_content(source), scope=scope, criteria=criteria,
    premises=premises, assumption_refs=assumption_refs, evidence_refs=evidence_refs,
    rationale=rationale, counterevidence=counterevidence,
    residual_uncertainties=residual_uncertainties,
    disposition="pending", dependency_freshness="current",
    engineering_conclusion="supported", record_kind="worked_example",
)

errors = validate_record(record, model=model)
tag = next((t for t in get_review_record_refs(model) if t["identifier"] == record.identifier), None)
print(f"Model tag: {tag}")
print(f"Validation errors: {errors}")
assert errors == [], f"Validation errors: {errors}"
print(f"Record valid: identifier={record.identifier!r}  engineering_conclusion={record.engineering_conclusion!r}")
conn.close()
```
**This is the one originating cell across all 8 chapters that already gates on a passing
validation** (`assert errors == []`) before continuing — every other originating cell in Ch2–Ch6
just prints `errors` without asserting it. **Cited forward:** yes (confirmed set; also
independently corroborated by grep hits in both Ch9 notebooks and all three Ch10 notebooks,
matching DL-097 exactly). **Proposed insertion:** `save_record(record)` immediately after the
`assert errors == []` line, before the final `print(...)` and `conn.close()`.

**Negative control, not a retrofit target:** `03-revision-flow.ipynb` cell 4 builds `broken`
(`identifier=""`) specifically to demonstrate `validate_record()` rejecting an empty identifier.
Not cited anywhere (confirmed: an empty-string identifier cannot be a citation target). No
`save_record()` needed.

**Undercounted duplicate, flagged as a cross-chapter open question below (not proposed as a fix
by this survey):** `03-revision-flow.ipynb` cell 6 rebuilds `AS-C08` a third time, by hand, as a
~25-line literal, purely as fixture input for a `check_stale()` demonstration (the notebook's own
cell-05 markdown says "`AS-C08` is rebuilt here exactly as notebook 02 built it"). DL-097 counted
`AS-C08` retyped three times, all in Ch9/Ch10; this is a **fourth** occurrence, one chapter
earlier, that DL-097's Ch9/Ch10-scoped investigation never saw. No `validate_record()` call exists
on this duplicate (it's immediately consumed by `check_stale()` instead), so there is no
pass-validation anchor to insert `save_record()` after even if this were in scope — and per the
spec's own Decision 3, the correct fix here would be `load_record("AS-C08")` replacing the literal
entirely, not a `save_record()` insertion. This notebook is not Ch9 or Ch10, so it falls outside
the spec's own Decision 5 scope boundary as currently written.

## Citation graph

| Identifier | Originating chapter/notebook/cell | Gates on pass? | Cited by (chapter/notebook/cell, per DL-097 and this survey) | Phase B action |
|---|---|---|---|---|
| `AC-001` | Ch2 `03-judgment-context.ipynb` cell 24 | no | *(not cited by Ch9/Ch10 per DL-097; originates and is used only within Ch2 in the material surveyed so far)* | Retrofit to save |
| `AC-C03` | Ch3 `01-moe-definition.ipynb` cell 23 | no | Ch6 `02-second-level.ipynb` cell 19 (`framing_premises` — to be confirmed against that cell's real premises list in Phase B); Ch10 `02-judgment-synthesis.ipynb` (per DL-097, `AI-C06`'s rebuilt premises) | Retrofit to save |
| `AS-C03` | Ch3 `03-threshold-judgment.ipynb` cell 23 | no | Ch6 `03-stopping-judgment.ipynb` cell 27 (`AI-C06`'s own `premises`, confirmed: `["AC-C06", "AS-C06", "AS-C03", "AI-C04"]`); Ch10 `02-judgment-synthesis.ipynb` (per DL-097) | Retrofit to save |
| `AI-C04` | Ch4 `03-completeness-check.ipynb` cell 28 | no | Ch6 `03-stopping-judgment.ipynb` cell 27 (confirmed in `AI-C06`'s own `premises`); Ch10 `02-judgment-synthesis.ipynb:413` (confirmed by grep) | Retrofit to save |
| `AC-C06` | Ch6 `02-second-level.ipynb` cell 19 | no | Ch6 `03-stopping-judgment.ipynb` cell 27 (own chapter, confirmed in `AI-C06`'s `premises`); Ch9 (per DL-097); Ch10 `02-judgment-synthesis.ipynb` (per DL-097) | Retrofit to save |
| `AS-C06` | Ch6 `02-second-level.ipynb` cell 36 | no | Ch6 `03-stopping-judgment.ipynb` cell 27 (own chapter, confirmed in `AI-C06`'s `premises`); Ch9 `02-evidence-completeness.ipynb`, `03-stale-detection.ipynb` (per DL-097, retyped verbatim); Ch10 `02-judgment-synthesis.ipynb` (per DL-097, retyped verbatim) | Retrofit to save |
| `AI-C06` | Ch6 `03-stopping-judgment.ipynb` cell 27 | no | Ch10 `02-judgment-synthesis.ipynb` (per DL-097 — the one record in that notebook already built by re-running live queries, not pure retyping) | Retrofit to save |
| `AS-C08` | Ch8 `02-violation-witness.ipynb` cell 32 | **yes** (`assert errors == []`) | Ch8 `03-revision-flow.ipynb` cell 6 (**new finding, this survey** — a 4th retyped copy, intra-chapter); Ch9 `02-evidence-completeness.ipynb`, `03-stale-detection.ipynb` (per DL-097, retyped verbatim); Ch10 `01-traceability-graph.ipynb`, `02-judgment-synthesis.ipynb`, `03-engineering-signoff.ipynb` (per DL-097) | Retrofit to save (origin); retrofit to load at every citing site, now including Ch8-03 |

All eight identifiers in the already-known cited-forward set are now accounted for with a
confirmed originating cell. No chapter in Ch1–Ch8 contained an unexpected `ReviewRecord`
construction outside this set (Ch6's `AI-BAD` and Ch8's `broken` are both confirmed negative
controls, never cited).

## Cross-chapter open questions

1. **A fourth retyped copy of `AS-C08` exists, one chapter earlier than DL-097's own count.**
   `ch08/03-revision-flow.ipynb` cell 6 rebuilds `AS-C08` by hand for a `check_stale()` demo — the
   exact same drift risk this whole initiative exists to close, but inside Ch8 itself, not Ch9 or
   Ch10. The spec's own Decision 5 scope boundary names only "Ch9's and Ch10's own citing
   notebooks" for the load-instead-of-retype retrofit. Recommend Phase B's plan extend this one
   specific site to `load_record("AS-C08")` too, since leaving a known instance of the exact
   problem out of scope on a technicality seems wrong — but this is a scope decision, not
   something this survey settles; flagged for Z/the orchestrator.

2. **No originating cell in Ch2/Ch3/Ch4/Ch6 currently gates on `validate_record()` passing before
   continuing** — each just prints `errors` unconditionally. Only Ch8's `AS-C08` cell has an
   explicit `assert errors == []`. The spec's own Decision 3 says `save_record()` goes "immediately
   after `validate_record(record, model=model)` passes" — recommend Phase B read this as "insert
   right after the existing `validate_record(...)` call, unconditionally, matching each notebook's
   own current convention" rather than retroactively adding a new assert-gate to five notebooks
   that don't have one today (which would be a larger, more invasive change than this initiative's
   own stated scope). This is a design-reading question for Z/the orchestrator to confirm before
   Phase B's contracts are written, not a judgment call this survey makes unilaterally.

3. **The `AC-C03`/`AS-C03` citation into `AC-C06`'s own `framing_premises`** (Ch6, cell 19) was not
   independently re-verified against that cell's own real premises list by Chapter 3's or Chapter
   6's own agent (Chapter 6's agent quoted the construction but not the full contents of
   `framing_premises`, built in cells 7-17). Phase B's own Ch6 contract should re-confirm this
   exact citation directly before relying on it.

4. **`AI-BAD` identifier-string reuse across chapters (Ch6, Ch10, `exercises/ch10`) is a same-named
   coincidence, not a real citation**, confirmed by inspection in both this survey and DL-097's own
   scope. Worth noting for whoever builds `records_citing()`: identifier-string matching alone is
   sufficient for this tutorial's own real citations (which use real `premises` list references),
   but a reused placeholder name in an unrelated negative control is not evidence of a real
   citation relationship — this is already handled correctly by this survey's own agents checking
   for a real `premises` link rather than a bare string match, and Phase B's own query function
   should do the same (walk `premises`, never just grep identifier strings).

## Next step

Phase A is now complete. Per `docs/superpowers/plans/2026-10-02-judgment-record-store-phase-a-plan.md`'s
own Task 9, the next step is to invoke `superpowers:writing-plans` again, for **Phase B**
(implementation), using this document and
`docs/superpowers/specs/2026-10-02-judgment-record-store-design.md` as its two inputs. Phase B's
own plan will have: one task building `src/toaster/judgment_store.py` and its tests (first, since
every other task depends on it); one task per originating chapter confirmed above (Ch2, Ch3, Ch4,
Ch6, Ch8) retrofitting it to call `save_record()`; one task per citing chapter (Ch9, Ch10)
retrofitting it to call `load_record()` instead of retyping (per DL-097's own exact findings,
reused directly rather than re-derived); and one independent task for the two Ch10 authoring bugs
DL-097 already found. Open questions 1 and 2 above need Z's or the orchestrator's own answer before
those specific tasks are written, so Phase B's plan is not placeholder-laden on those two points.
