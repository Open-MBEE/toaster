# Judgment-record store: persist `ReviewRecord`s once, query them thereafter

## Context

A gap analysis this session (`decisions/log.md` DL-097 — ACE architectural diagnosis plus two
`simulated-learner` catalogues of concrete instances in Ch9 and Ch10) found why the tutorial's
last two chapters read as text-heavy in a different way than the diagram/text integration work
just fixed: `ReviewRecord` (`src/toaster/evidence.py`) has never been given the persisted form its
own original design ("SA-1") called for. Only the Python dataclass exists; no record is ever
serialized. So every later chapter that needs an earlier chapter's judgment (`AS-C06`, `AS-C08`,
and the records Ch10's own synthesis cites) has no way to load it — it re-types the entire record,
by hand, as a fresh Python literal. DL-097 found this done three times for `AS-C06`/`AS-C08` alone
(`ch09/02-evidence-completeness.ipynb`, `ch09/03-stale-detection.ipynb`,
`ch10/02-judgment-synthesis.ipynb`), each a ~70-line copy with nothing to catch drift between
copies or from the original.

This is separate from, and does not reopen, the diagram/text integration redesign (`docs/superpowers/specs/2026-10-02-diagram-text-integration-design.md`) or its PR (#25, merged). It is its own initiative, on its own branch (`judgment-record-store`, cut from `main` after that merge).

**Z's decision (DL-097, recorded verbatim in the log), governing this spec:**
1. A real persisted store, in the repo, for `ReviewRecord` content — not just the dataclass.
2. The Hawkins argument structure (which record is a premise of which) lives in that store, not
   as SysML model-side metadata. (`ReviewRecord.premises: list[str]` already exists and is already
   the right shape for this — no new field needed.)
3. A judgment's own prose is authored exactly once, in the chapter where that judgment was
   actually made. A later chapter that needs it queries/retrieves the stored record; it never
   re-authors it.
4. Not every chapter can inline a full judgment's own prose without bloating its own narrative —
   the store exists specifically so a later chapter can cite/summarize a record it did not write.

**What this spec does not reopen:** the model-side anchor (`ReviewRecordRef` metadata tag,
`get_review_record_refs()` in `src/toaster/query.py`, established by DL-084) is confirmed working
and stays exactly as-is — it still answers "which judgments exist, about what." This spec adds the
missing second half: "and what did each one actually say."

## Decisions already made (confirmed with Z, this session)

1. **New module, not an extension of `evidence.py`.** `src/toaster/judgment_store.py`:
   `save_record(record) -> Path`, `load_record(identifier) -> ReviewRecord`,
   `records_citing(identifier) -> list[ReviewRecord]` (every stored record whose own `premises`
   list names `identifier` — the argument-structure query DL-097's escalated question asked about).
   Keeps `evidence.py` focused on the dataclass and field-level validation; keeps persistence
   concerns in their own file, matching this repo's existing one-responsibility-per-module pattern
   (`query.py` is model queries only, `render.py` is diagrams only).
2. **One JSON file per record**, at `decisions/judgment-records/<IDENTIFIER>.json` (e.g.
   `decisions/judgment-records/AS-C06.json`) — not one aggregate file. Matches this repo's own
   bipartite-graph convention in `glossary/definitions/<source>.ttl` (one file per node, for
   parallel-worktree safety: two chapters' own contracts, each authoring a different record, never
   touch the same file). The JSON is `dataclasses.asdict(record)` plus a `schema_version` key.
3. **Authored once, at the point of construction.** Whichever notebook currently builds a record
   that is cited by a later chapter gets one additional line in its own construction zone:
   `save_record(record)`, immediately after `validate_record(record, model=model)` passes. This is
   additive — it does not change what that notebook already teaches or prints.
4. **Loaded, never re-typed, at the point of citation.** A later notebook that needs an earlier
   record calls `load_record("AS-C06")` and works with the returned `ReviewRecord` object directly
   (reading its own fields, e.g. `as_c06.claim`), rather than constructing a new literal with the
   same field values typed out again.
5. **Scope boundary, stated explicitly so Phase B does not drift:** this spec and its plan cover
   only (a) building `judgment_store.py` and its tests, (b) retrofitting the specific
   already-identified originating notebooks (the ones whose own records are actually cited
   forward — Phase A's own survey names them precisely) to persist, and (c) retrofitting Ch9's and
   Ch10's own citing notebooks to load instead of re-type. It does **not** retrofit every
   judgment-record notebook in the tutorial "for consistency" — a notebook whose own record is
   never cited elsewhere has nothing to gain from persisting it, and retrofitting it is not named
   here.

## Process: survey first, then implement — same two-phase shape the diagram/text integration work used, because it worked

**Phase A (survey).** DL-097's own investigation already covers the *citing* side in detail
(Ch9 and Ch10, with exact cell content quoted) — Phase A does not re-investigate that. What Phase A
must establish, with the same rigor (exact cell content, not descriptions), is the **originating**
side: for each of Chapters 1 through 8, does that chapter's own construction-zone build a
`ReviewRecord`? If so: its exact identifier, kind, and subject_ref; the exact cell(s) that
construct it; and whether that identifier is one of the ones already known to be cited forward
(`AC-001`, `AC-C03`, `AS-C03`, `AI-C04`, `AC-C06`, `AS-C06`, `AI-C06`, `AS-C08` — the set DL-097's
own investigation named) or a new citation Phase A's own agent discovers that this spec did not
anticipate (flagged as an open question, never assumed).

**Deliverable:** `decisions/judgment-record-store-survey.md` — one row per `ReviewRecord`
construction found across Ch1–8, each with: chapter/notebook/cell, identifier, whether it is cited
forward (and by whom, cross-referencing DL-097's own Ch9/Ch10 findings), and the literal proposed
`save_record(record)` insertion point. Plus a compiled citation graph (identifier → origin →
every citing site) that Phase B's own plan is generated from directly.

**Phase B (implementation).** Generated via `writing-plans` from Phase A's survey — one task per
originating chapter that needs the persistence retrofit, one task building `judgment_store.py`
itself (with tests, done first since every other task depends on it), one task per citing chapter
(Ch9, Ch10) retrofitted to load instead of retype, and one small, independent task for the two
authoring bugs DL-097 already found in Ch10 (`01-traceability-graph.ipynb`'s `traceability_graph`
dict, `03-engineering-signoff.ipynb`'s premises list — both retype a fact the same notebook's own
prior cell already computed into a live variable; this task has no dependency on the survey or on
`judgment_store.py` and can run first). Each task is its own `CONTRACT` per
`decisions/work-contract-template.md`'s own exact format, in its own worktree, author and reviewer
on different pinned models, merged only after independent review, exactly as the diagram/text
integration work already proved on this same repo.

## Non-goals

- No change to the model-side anchor (`ReviewRecordRef`, `get_review_record_refs()`) — confirmed
  working, not reopened.
- No retrofit of a judgment-record notebook whose own record is never cited elsewhere.
- No change to what any chapter teaches, or in what order — this is a persistence-and-retrieval
  mechanism change, not a content or didactic-sequencing change.
- No change to `ReviewRecord`'s own field set — `premises: list[str]` already carries the argument
  structure; nothing new is added to the dataclass.
- The two Ch10 authoring-bug fixes are included (they're free, already fully specified, and
  closely related) but are not blocked on, or blocking, the rest of this work.

## Verification

- `judgment_store.py`: round-trip test (`save_record` then `load_record` returns an equal
  `ReviewRecord`), a `records_citing()` test against at least two records where one's `premises`
  names the other, and a staleness test (`check_stale()` from `evidence.py` against a loaded
  record's own `content_hash`).
- Every retrofitted originating notebook: re-executed end-to-end, `validate_record()` still passes,
  and the newly-written JSON file under `decisions/judgment-records/` is a real, non-empty,
  schema-valid file (checked, not assumed).
- Every retrofitted citing notebook (Ch9, Ch10): re-executed end-to-end; the loaded record's own
  field values match what the notebook's prose claims about it; the hand-typed literal it replaces
  is gone from the diff.
- Full suite (`uv run pytest tests/ glossary/tests/ -q`) and `uv run python
  scripts/check_construction.py --check`, both clean, after every merge.
- At least one `simulated-learner` spot-check on a retrofitted citing notebook, confirming the
  loaded-not-retyped version still reads naturally and the record's content is still legible to a
  reader (same bar DL-097's own investigation already applied).
