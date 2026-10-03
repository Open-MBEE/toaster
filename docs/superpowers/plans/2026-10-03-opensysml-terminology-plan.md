# OpenSysML Terminology Revision Implementation Plan

> **For agentic workers:** every task is a CONTRACT per `decisions/work-contract-template.md`, run through `decisions/task-states.md`: author and reviewer on different pinned models, one worktree per task created by the orchestrator, plain commits (no trailers), subagents never push or merge, judgment goes to the ACE. Steps use checkbox syntax.

**Goal:** Revise this repository's prose so "OpenSysML" names the open-source SysML v2 tool stack (opensysml.org) and every claim that is true of one tool names that tool (the OpenSysML runtime or sysml-toolkit), without changing any code, model, record, stored output or published anchor.

**Architecture:** One integration branch `terminology` (off `pages-publishing`). Stage 1 is read-only inventory (one table row per occurrence, classified, with the proposed replacement), plus a protected-token diff checker. Stage 2 is edit contracts by area that apply inventory rows exactly. Stage 3 is the skills (ACE only) and the lasting lint guard. Stage 4 is a whole-branch regression gate. The branch merges back into `pages-publishing` only after the gate passes.

**Authority:** Z's direction of 2026-10-03 (`decisions/opensysml-terminology/website-review.md`); ACE ruling DL-116 (`decisions/log.md`). Pilot membership is escalated to Z with default OUT; nothing in this plan depends on the answer.

**Why heavy:** the umbrella meaning changes truth conditions. "OpenSysML cannot X" is true of the runtime and false where sysml-toolkit does X (DEFERRED D-017, D-023 and others). So this is a scope correction of claims, not a find-and-replace.

## Normative convention (builders quote this; from DL-116)

> OpenSysML (opensysml.org) is the open-source SysML v2 tool stack. This tutorial uses two of its components and names them by role: **the OpenSysML runtime** (Go; repo Open-MBEE/OpenSysML; Python package `opensysml`; pinned v0.9.0) and **sysml-toolkit** (Rust; `sysmlv2` binary; pinned v0.9.1). The OMG SysML v2 Pilot Implementation (EPL-2.0) is the conformance baseline and is always named as such. A bare "OpenSysML" is used only for a statement about the whole stack. Any claim that is true of one component, or that was probed against one component (a gap, a limitation, an API, a version), names that component; a version number always attaches to a component name. Contrasts name both components ("the OpenSysML runtime accepts X; sysml-toolkit v0.9.1 rejects it"); "OpenSysML or/and/versus sysml-toolkit", "neither OpenSysML nor", "OpenSysML alone/itself/cannot" are not written. On a published page the first mention uses the full component name; "the runtime" and "the toolkit" may follow on that page. Code identifiers, imports, environment variables, package, directory and file names, URLs, repo and issue references, `models/*.sysml`, judgment records, stored outputs, DEFERRED.md headings, the decision log and dated evidence under `decisions/`, and quoted tool output never change. Before DL-116, a bare "OpenSysML" in this repository means the runtime.

Additional rules: running text says "sysml-toolkit" (its own name), never "the OpenSysML toolkit" except as a first-mention gloss; "the OpenSysML runtime" in running text, then "the runtime" within the page; the runtime's tracker is "the runtime's tracker (`Open-MBEE/OpenSysML#NNN`)" where prose names it; the Pilot is always "the OMG SysML v2 Pilot Implementation" (then "the pilot") and is never counted among "both tools". The stack is defined once each on `docs/setup.md`, `docs/references.md` (its "OpenSysML" section becomes the definition) and `docs/reproducibility.md`, with a link to https://opensysml.org/.

## Protected zones (reviewer-checked in every contract)

Never change: code cells and their stored outputs in notebooks; `models/**`; `decisions/judgment-records/**`; `figures/**`; `decisions/log.md` and every dated file under `decisions/` (append-only; DL-116 carries the reading rule); `docs/superpowers/**`; `tests/**`, `src/**`, `scripts/**` (including comments); `uv.lock`; DEFERRED.md headings (their GitHub anchors are linked from published pages); skill directory names and `name:` frontmatter; code fences inside skills (executed by `tests/test_skill_snippets.py`). Protected tokens whose per-file counts must be unchanged: `import opensysml`, `opensysml.` (API calls), `OPENSYSML_VERSION`, `OPENSYSML_GRPC_VERSION`, `~/.opensysml`, `Open-MBEE/OpenSysML`, `Open-MBEE/sysml-toolkit`, `OpenSysML#NNN`, `sysml-toolkit#N`, `toaster#N`, `opensysml-api`, `opensysml-query`, and every URL.

Repo checks that must stay clean at every merge: `uv run pytest tests/ glossary/tests/ -q`, `uv run python -m glossary check`, `uv run python scripts/check_construction.py --check`.

## Review Focus

1. A claim that was true for the runtime becomes false or unprobed for the stack; the truth classification (toolkit-differs / toolkit-same / toolkit-unprobed against the DEFERRED entry) is the main correctness risk, not typography.
2. A notebook edit that touches a code cell or output changes `AS-C08`'s content hash or a persisted record; only markdown cells and `index.md`/`conclusion.md` are editable.
3. A DEFERRED.md heading edit breaks published anchors; headings stay byte-identical.
4. A skill edit that alters a code fence breaks `tests/test_skill_snippets.py`, or a rename breaks CLAUDE.md/AGENTS.md references.
5. Replacing the bare name with "the OpenSysML runtime" in a sentence that really is about the stack makes the stack sound smaller than it is; sentences that are truly about the stack keep the bare name.

---

## Task 0: Branch and ordering (orchestrator, done)

- [x] `terminology` branch off `pages-publishing` (66531c9, includes DL-115 and DL-116). Worktrees: `git worktree add .claude/worktrees/<name> -b term/<name> terminology`; merges into `terminology` use `--no-ff`; `pages-publishing` is untouched until the Task 8 gate passes.
- [ ] Order: OT-1a, OT-1b and OT-2 in parallel; orchestrator merges the two inventories into `decisions/opensysml-terminology/inventory.md`; then OT-3A, OT-3B, OT-4, OT-5 in parallel; then OT-6 (ACE edits skills); then OT-7 (lint rules); then OT-8 (gate).

## Task 1: Inventory (OT-1a, OT-1b), read-only

Rows follow `decisions/pages-publishing/a4-dangling-references.md`'s style: `| row | file | locator | quoted sentence | class | proposed replacement |`. Classes: `KEEP-ID` (protected token or zone), `KEEP-STACK` (truly about the stack), `RUNTIME` (rewrite to name the runtime), `TOOLKIT` (rewrite to name sysml-toolkit), `BOTH` (name both), `FALSE-UNDER-STACK` / `SAME` / `UNPROBED` (the truth class for capability claims, against the DEFERRED entry id), `DEFINE` (stack definition site), `AMBIGUOUS` (needs the ACE; give the options). Every `RUNTIME`/`TOOLKIT`/`BOTH` row has the exact replacement wording, applying the normative convention.

```
CONTRACT OT-1a | 2026-10-03
Role:           general-purpose research agent (read-only), model claude-sonnet-5
Reviewer:       reviewer, model claude-opus-5-5 (samples 40 rows, rechecks every FALSE-UNDER-STACK and AMBIGUOUS)
State:          ready
Task:           Inventory every occurrence of OpenSysML / opensysml / "Open-MBEE/OpenSysML" and every sentence that
                contrasts or conflates the runtime with sysml-toolkit in the LEARNER-FACING surface: chapters/**
                (markdown cells and index.md/conclusion.md; list code-cell occurrences as KEEP-ID with a note when a
                markdown cell must clarify them), exercises/**, docs/*.md, docs/case-studies/*.md, README.md.
Context:        DL-116 and the normative convention; DEFERRED.md entries D-014, D-017, D-019, D-020, D-023, D-024,
                D-025, D-032..D-036 (they hold both tools' probe results); decisions/opensysml-terminology/website-review.md.
Non-goals:      No edits. No decisions on ambiguous rows (classify AMBIGUOUS with options).
Blast zone:     read-only; output file decisions/opensysml-terminology/inventory-a.md in worktree .claude/worktrees/inv-a.
Acceptance:     Every file's occurrences accounted for (report counts per file, class totals, and a machine check:
                the number of lines in the surface that match /opensysml/i equals the number of rows plus
                explicitly listed duplicates); each capability claim carries its DEFERRED entry id and truth class;
                each proposed replacement quotes the convention rule it applies.
Report:         branch/commit, counts, AMBIGUOUS list, FALSE-UNDER-STACK list.
```

```
CONTRACT OT-1b | 2026-10-03
Role:           general-purpose research agent (read-only), model claude-sonnet-5
Reviewer:       reviewer, model claude-opus-5-5
Task:           Same inventory for the BINDING surface: AGENTS.md (Part 1 and Part 2), CLAUDE.md, DEFERRED.md (headings
                protected; list bodies that name only the runtime; propose the dated note for the top), .claude/skills/*
                (14 skills; separate prose from code fences; list name/description frontmatter), .claude/agents/*,
                glossary/README.md and glossary definitions mentioning OpenSysML, docs/superpowers/** (KEEP, count only).
                Include the ACE's wording for AGENTS.md 1.2/1.7/1.9 and the CLAUDE.md sources line as DEFINE rows.
Blast zone:     read-only; output decisions/opensysml-terminology/inventory-b.md in worktree .claude/worktrees/inv-b.
Acceptance:     as OT-1a; plus for each skill: lines of prose vs inside code fences, and the exact set of snippets run by
                tests/test_skill_snippets.py (so skill edits cannot touch them).
```

- [ ] Orchestrator verifies counts (git grep -ic per file) against each report before merging the inventory files.

## Task 2: Protected-token diff checker (OT-2)

```
CONTRACT OT-2 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          ready
Task:           Write scripts/check-terminology-edit.py and tests/test_check_terminology_edit.py. Usage:
                `uv run python scripts/check-terminology-edit.py --base <rev> [--head <rev>]` (head defaults to the working
                tree/HEAD). It fails (exit 1, one line per violation) if between base and head: (a) any protected zone
                changed (models/**, decisions/judgment-records/**, figures/**, decisions/** except new files,
                tests/**, src/**, scripts/** other than this checker's own files, uv.lock, docs/superpowers/**); (b) any
                notebook code cell's source, any cell outputs, execution_count, id, metadata, cell count or order changed
                (compare with json; markdown cell `source` is the only editable notebook field); (c) the per-file count
                of any protected token changed (list in the plan; counted with word-boundary regexes over the whole file
                for non-notebooks and over code cells for notebooks); (d) any `## D-0nn` heading line in DEFERRED.md
                changed; (e) any fenced code block in .claude/skills/**/SKILL.md or reference files changed (compare the
                fenced blocks as a list); (f) any skill directory or `name:` frontmatter changed; (g) any URL string
                present in base is missing in head in a changed file. It prints PASS/FAIL per rule.
Non-goals:      Does not judge prose. Does not edit anything.
Blast zone:     scripts/check-terminology-edit.py, tests/test_check_terminology_edit.py -- on branch term/guard,
                worktree .claude/worktrees/guard. NOTE tests/test_no_local_paths.py scans scripts/ and tests/: do not write
                forbidden strings (use string concatenation in fixtures or add nothing to the allowlist).
Acceptance:     Offline tests build small git repos in tmp_path (git init, two commits) and assert each rule passes on a
                clean prose-only change and fails on: a changed model file, a changed judgment record, a changed code
                cell, a changed cell output, a changed DEFERRED heading, a changed skill code fence, a removed URL, a
                changed protected-token count, a renamed skill directory. Run against the real repo: base=pages-publishing
                head=terminology must PASS (no changes yet except decisions/ and docs/superpowers/ additions, which are
                new files). Mutation-check three rules. Repo checks clean.
Report:         branch/commit, tests, real-repo run output, mutation evidence.
```

## Task 3: Learner prose edits (OT-3A, OT-3B), Task 4: docs (OT-4), Task 5: binding docs (OT-5)

All four apply `decisions/opensysml-terminology/inventory.md` rows exactly (the file is the source of truth, as `a4-dangling-references.md` was for PUB-6). Rules common to every edit contract:

```
Rules:          1. Apply every row in the blast zone whose class is RUNTIME, TOOLKIT, BOTH, DEFINE, FALSE-UNDER-STACK,
                   SAME or UNPROBED using the row's replacement wording exactly. KEEP-* rows: no change. AMBIGUOUS rows:
                   no change, listed for the orchestrator (the ACE rules them). If applying a replacement would change
                   a number, a verdict, a pinned version or a claim beyond naming the component, STOP and report that row.
                2. Notebooks: patch only the `source` of MARKDOWN cells named by rows, by direct JSON text substitution
                   asserting exactly one match; no nbconvert; code cells, outputs, ids, metadata untouched. Where a
                   code-cell string is wrong under the umbrella (protected), the row names an adjacent MARKDOWN cell to
                   carry the clarification: edit that markdown cell only.
                3. Commits are plain one-line messages with no trailers. Put the mapping from each edit to the convention
                   rule it applies in the report.
                4. Protected zones and tokens untouched (checker: scripts/check-terminology-edit.py --base terminology).
Acceptance (all): (1) counts of rows applied by class and skipped by reason; sum equals the rows for the blast-zone files;
                (2) the checker passes against base=terminology; (3) cell-by-cell json comparison for each notebook: only
                named markdown cells differ, only in `source`; (4) site build `BASE_URL=/toaster npx myst build --html`
                (npm ci first) has the same 98 warnings as the parent; (5) full suite, glossary check, check_construction;
                (6) `git grep -n` of the edited files for the banned patterns (OpenSysML or/and/vs/nor sysml-toolkit,
                "OpenSysML v0.9", "OpenSysML alone|itself|cannot") returns nothing except in KEEP-ID rows.
```

- **OT-3A:** `chapters/ch01..ch06/**` markdown and index/conclusion; branch `term/ch-a`.
- **OT-3B:** `chapters/ch07..ch10/**`, `exercises/**` markdown cells; branch `term/ch-b`. Includes the toolkit-differs cells in ch07 nb02 (cells 9, 23, 25 and the markdown clarification for code cell 22) per D-023.
- **OT-4:** `docs/setup.md` (line ~147 "does one thing OpenSysML cannot yet" is self-contradictory under the umbrella), `docs/references.md` (its OpenSysML section becomes the stack definition with the opensysml.org link), `docs/reproducibility.md`, `docs/case-studies/*.md`, `README.md`; also add the stack definition sentence to setup and reproducibility; branch `term/docs`.
- **OT-5:** `AGENTS.md` (Part 1 1.2, 1.7, 1.9; Part 2 only if a row says so), `CLAUDE.md` sources line, and one dated terminology note at the top of `DEFERRED.md` (headings untouched). Wording for the Part 1 edits is in DL-116's ACE report (quoted in the inventory-b DEFINE rows); branch `term/binding`. The orchestrator reads the final Part 1 text itself before merge (Part 1 governs the project).

## Task 6: Skills (OT-6), ACE only

Per DL-116 and skill-editor: the ACE edits the 14 skills' PROSE as one logical change in one session, after OT-3..OT-5 merge (no mid-loop edit), with DL-116 as the pre-edit record and the revert record the commit preceding the first skill edit (record its SHA in the report). `opensysml-api` and `opensysml-query` names and frontmatter `name:` stay; `opensysml-query` H1 and description say "the OpenSysML runtime v0.9.0"; `opensysml-api` description stays ("opensysml v0.9.0 interface" uses the package name). No code fence changes. Reviewer: `reviewer` on a different model than the ACE, running the checker (rule e,f) and `tests/test_skill_snippets.py`.

## Task 7: Lasting guard (OT-7)

```
CONTRACT OT-7 | 2026-10-03
Role:           builder, model claude-sonnet-5, effort medium
Reviewer:       reviewer, model claude-opus-5-5
State:          blocked_on OT-3A, OT-3B, OT-4 merged
Task:           Add learner-scope error rules to glossary/lint_rules.toml (data-driven, see glossary/lint.py) and tests:
                OpenSysML\s+(or|and|nor|vs\.?|versus)\s+sysml-toolkit ; sysml-toolkit\s+(or|and)\s+OpenSysML ;
                neither\s+OpenSysML ; not\s+OpenSysML ; OpenSysML\s+(alone|itself|cannot|can't|does\s+not|doesn't|only) ;
                OpenSysML\s+v0\.9 . Each rule carries a message pointing at the convention (AGENTS.md 1.2).
Blast zone:     glossary/lint_rules.toml, glossary/tests/<new or existing lint test file>.
Acceptance:     the lint is clean on the real learner surface (chapters, docs) at this commit; a test per rule fails on a
                fixture sentence and passes on the sanctioned rewrite; `uv run python -m glossary lint` error count does not
                increase versus base (record the base count; the repo has a known large baseline of other findings:
                compare per-rule counts, not the total); glossary check and the full suite clean.
```

## Task 8: Whole-branch regression gate (reviewer, no builder)

- [ ] Reviewer (Opus, fresh): (1) `scripts/check-terminology-edit.py --base pages-publishing --head terminology` PASS; (2) protected-token counts per file identical (independent grep); (3) `git diff pages-publishing..terminology --stat` touches only the editable surface; (4) full suite with the tool env vars and `TOASTER_REQUIRE_TOOLS=1`; (5) executed build `BASE_URL=/toaster uv run --frozen npx myst build --html --execute --strict` with provisioned tools: exit 0, `scripts/check-site.py` passes the checks it passes at base (the two exercise/DEFERRED published-file checks are cleared by earlier work: record actual), figures == 18; stored outputs of every executed notebook equal to base (join adjacent same-stream chunks); `AS-C08.json` content_hash still equals sha256 of `models/ch08-cumulative.sysml`; (6) built-page text diff base vs head limited to rows in the inventory (script: extract text per page, diff, map each differing line to an inventory row, report orphans); (7) every FALSE-UNDER-STACK row re-verified against its DEFERRED entry by reading the entry; (8) `uv run python -m glossary lint` per-rule counts not worse than base except the new rules at 0; (9) 20 random edited sentences read for grammar and meaning.
- [ ] Orchestrator: merge `terminology` into `pages-publishing` (`--no-ff`), run the three repo checks, log the outcome as DL-117.

## Out of scope

Pilot membership (Z's answer may change only the definition sentence in AGENTS.md 1.2 and `docs/references.md`); renaming skills or packages; re-running notebooks; editing `decisions/` evidence; closing stale upstream-issue wording (separate DEFERRED follow-up).

## Queued after OT-8 (requested by mzargham, 2026-10-03; NOT started, specify as its own contract when the terminology contracts clear)

**Contribution-policy revision.** The contribution sections, both in the notebooks and in the docs, must say that the
contributions we want are **keeping the tutorials current to the toolchain**, not adding new content. Existing content may be
refined, clarified or otherwise improved against the project's existing priorities:
1. conformance with the SysML v2 specifications (all three OMG PDFs: the SysML v2 language spec, the API and Services spec, KerML);
2. didactic clarity;
3. effective, demonstrative use of tools from the OpenSysML ecosystem.
An improvement is acceptable if it is **strictly dominant**: it makes at least one of these better without making any of them worse.

Scope to inventory when specified: `docs/contributor.md`, `docs/setup.md` (fork-and-exercise workflow), `README.md`, any "contribute"
text in chapter `index.md`/`conclusion.md` and notebook markdown cells, the exercise-pointer cells, and `AGENTS.md` where it states
contribution scope. Judgment items for the ACE: the exact "strictly dominant" test wording; how it reconciles with the
chapter-conclusion "what comes next" sentences and with `DEFERRED.md` (which tracks tool gaps); whether adding a chapter or
exercise is ever allowed. Edits fall under the same protections as the terminology pass (protected zones, markdown-only for
notebooks, guard checker, independent reviewer), and the contribution wording must use the OpenSysML convention (DL-116/DL-117).
