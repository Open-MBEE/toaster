# Inventory B: the binding surface (CONTRACT OT-1b)

Read-only inventory for the OpenSysML terminology revision. Base commit `1649785` on branch `term/inv-b` (before this file). Convention and classes: `docs/superpowers/plans/2026-10-03-opensysml-terminology-plan.md` (normative convention, protected zones, OT-1b, OT-6); DL-116 (`decisions/log.md` line 1592); `decisions/opensysml-terminology/website-review.md`. No file other than this one was edited.

## Method

1. `grep -i opensysml` per file over the scoped surface; every matching **line** is one row (one row can carry several phrases on the same line; the replacement column then lists each, or the note does).
2. Each line was read in context and classified. A line whose only matches are protected tokens (package `opensysml`, `import opensysml`, `opensysml.` calls, `opensysml-api`/`opensysml-query`, `Open-MBEE/OpenSysML`, `OpenSysML#NNN`, `OPENSYSML_*`, URLs, file names such as `adapters/opensysml.py`) is auto-classified KEEP-ID (script: strip those tokens, test whether `opensysml` remains). Every line that retains a bare prose use was classified by hand.
3. Capability claims were classified against the DEFERRED entry that holds the probe results: FALSE-UNDER-STACK (sysml-toolkit v0.9.1 differs, so the bare-subject sentence is false if OpenSysML includes the toolkit), SAME (toolkit behaves the same), UNPROBED (the entry has no toolkit result). The class column carries the primary class, then `;` and the truth class.
4. The ACE paragraph for AGENTS.md 1.2/1.7/1.9 and the CLAUDE.md sources line is **not in the repository** (DL-116 Decision (4) says "wording in the ACE report, quoted in the plan"; the plan quotes only the normative convention). Those DEFINE rows are composed from the normative convention and marked "ACE wording to confirm".
5. Extra DEFERRED/skill sentences that conflate the runtime with sysml-toolkit without the token "OpenSysML" are listed in "Related bare-tool sentences" below; they are outside the line-count check.

Class vocabulary used (plan classes plus one): KEEP-ID, KEEP-STACK, RUNTIME, TOOLKIT, BOTH, DEFINE, AMBIGUOUS, and **KEEP-BODY** (new sub-class of KEEP: a DEFERRED body sentence outside the gap sentence, where DL-116 (3) permits "runtime" insertions only in the gap sentence; the dated top note carries the reading rule; an optional edit is given in the note).

## Machine check (lines matching /opensysml/i = rows)

Command per file: `grep -ci opensysml FILE`. Result at base `1649785`: every file below has lines == rows, 0 duplicates listed, and the set of files with matches under `AGENTS.md CLAUDE.md DEFERRED.md .claude glossary` equals the set below (asserted by the generator).

| file | lines matching | rows | of which in code fences |
|---|---|---|---|
| `AGENTS.md` | 6 | 6 | 0 |
| `CLAUDE.md` | 3 | 3 | 0 |
| `DEFERRED.md` | 69 | 69 | 0 |
| `glossary/sources/notes/reading-notes.md` | 1 | 1 | 0 |
| `.claude/agents/layer-auditor.md` | 1 | 1 | 0 |
| `.claude/agents/orchestrator.md` | 1 | 1 | 0 |
| `.claude/skills/ace-protocol/SKILL.md` | 2 | 2 | 0 |
| `.claude/skills/ace-protocol/z-model.md` | 1 | 1 | 0 |
| `.claude/skills/architecture-layers/SKILL.md` | 3 | 3 | 0 |
| `.claude/skills/opensysml-api/SKILL.md` | 20 | 20 | 7 |
| `.claude/skills/opensysml-query/SKILL.md` | 6 | 6 | 2 |
| `.claude/skills/orchestrator-protocol/SKILL.md` | 1 | 1 | 0 |
| `.claude/skills/skill-editor/SKILL.md` | 1 | 1 | 0 |
| `.claude/skills/sysml-diagrams/SKILL.md` | 7 | 7 | 0 |
| `.claude/skills/sysml-diagrams/references/recipes.md` | 6 | 6 | 0 |
| `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 24 | 24 | 0 |
| `.claude/skills/toaster-recipe/SKILL.md` | 4 | 4 | 4 |
| `.claude/skills/tutorial-glossary/SKILL.md` | 1 | 1 | 0 |
| `.claude/skills/tutorial-style-guide/SKILL.md` | 2 | 2 | 1 |
| `.claude/skills/tutorial-supporting-pages/SKILL.md` | 1 | 1 | 0 |
| **total** | **160** | **160** | **14** |

Count-only groups (not rowed; all KEEP, at base `1649785`, `grep -rIli` files / `grep -rIhi` lines):

| group | files | lines | class |
|---|---|---|---|
| `decisions/**` (dated evidence, append-only; DL-116 reading rule) | 93 | 451 | KEEP |
| `docs/superpowers/**` (plans/specs; protected) | 14 | 160 | KEEP |
| `src/**` (protected, incl. comments) | 8 | 43 | KEEP |
| `scripts/**` (protected, incl. comments) | 9 | 42 | KEEP |
| `tests/**` (protected) | 18 | 86 | KEEP |

(`decisions/**` includes the plan-adjacent `decisions/opensysml-terminology/website-review.md`; adding this inventory file changes the `decisions/**` counts by +1 file; and `docs/superpowers/plans/2026-10-03-opensysml-terminology-plan.md` carries 23 lines of the 160.) `glossary/**` has exactly one match, rowed above (`glossary/sources/notes/reading-notes.md:35`); `glossary/README.md`, `docs/glossary.md` and `glossary/definitions/*.ttl` have **0** mentions of OpenSysML (the plan's expectation of ttl mentions did not materialise: nothing to KEEP or fix). `.claude/agents/*.md`: 2 matches, both `opensysml-query` (KEEP-ID).

## Class totals (primary class)

| class | rows |
|---|---|
| KEEP-ID | 94 |
| RUNTIME | 50 |
| DEFINE | 5 |
| KEEP-BODY | 5 |
| AMBIGUOUS | 3 |
| BOTH | 2 |
| KEEP-STACK | 1 |
| **total** | **160** |

Truth classes (capability claims, any primary class): FALSE-UNDER-STACK 16, SAME 11, UNPROBED 27.

### Per-file primary-class counts

| file | AMBIGUOUS | BOTH | DEFINE | KEEP-BODY | KEEP-ID | KEEP-STACK | RUNTIME |
|---|---|---|---|---|---|---|---|
| `AGENTS.md` | 0 | 0 | 4 | 0 | 2 | 0 | 0 |
| `CLAUDE.md` | 0 | 0 | 1 | 0 | 2 | 0 | 0 |
| `DEFERRED.md` | 1 | 1 | 0 | 5 | 35 | 0 | 27 |
| `glossary/sources/notes/reading-notes.md` | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| `.claude/agents/layer-auditor.md` | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| `.claude/agents/orchestrator.md` | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| `.claude/skills/ace-protocol/SKILL.md` | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| `.claude/skills/ace-protocol/z-model.md` | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| `.claude/skills/architecture-layers/SKILL.md` | 0 | 0 | 0 | 0 | 3 | 0 | 0 |
| `.claude/skills/opensysml-api/SKILL.md` | 0 | 0 | 0 | 0 | 19 | 0 | 1 |
| `.claude/skills/opensysml-query/SKILL.md` | 0 | 1 | 0 | 0 | 3 | 0 | 2 |
| `.claude/skills/orchestrator-protocol/SKILL.md` | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| `.claude/skills/skill-editor/SKILL.md` | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| `.claude/skills/sysml-diagrams/SKILL.md` | 0 | 0 | 0 | 0 | 0 | 0 | 7 |
| `.claude/skills/sysml-diagrams/references/recipes.md` | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 0 | 0 | 0 | 0 | 21 | 0 | 3 |
| `.claude/skills/toaster-recipe/SKILL.md` | 0 | 0 | 0 | 0 | 4 | 0 | 0 |
| `.claude/skills/tutorial-glossary/SKILL.md` | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| `.claude/skills/tutorial-style-guide/SKILL.md` | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| `.claude/skills/tutorial-supporting-pages/SKILL.md` | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

## Skills: prose, fences, frontmatter, executed snippets

There are **15** skill directories (the plan and CLAUDE.md say 14; `ace-protocol`, `architecture-layers`, `myst-publication`, `opensysml-api`, `opensysml-query`, `orchestrator-protocol`, `skill-editor`, `sysml-diagrams`, `sysml-v2-toaster-model`, `toaster-recipe`, `toaster-review-protocol`, `tutorial-glossary`, `tutorial-style-guide`, `tutorial-supporting-pages`, `user-testing`). Reference files: `ace-protocol/z-model.md`, `z-principles.md`, `architecture-layers/example-layers.sysml`, `sysml-diagrams/references/recipes.md`.

| file | total lines | lines inside code fences (incl. fence lines) | prose lines | OpenSysML lines | in fences | in prose |
|---|---|---|---|---|---|---|
| `.claude/skills/ace-protocol/SKILL.md` | 159 | 25 | 134 | 2 | 0 | 2 |
| `.claude/skills/ace-protocol/z-model.md` | 39 | 0 | 39 | 1 | 0 | 1 |
| `.claude/skills/ace-protocol/z-principles.md` | 62 | 0 | 62 | 0 | 0 | 0 |
| `.claude/skills/architecture-layers/SKILL.md` | 96 | 0 | 96 | 3 | 0 | 3 |
| `.claude/skills/architecture-layers/example-layers.sysml` | 45 | 0 | 45 | 0 | 0 | 0 |
| `.claude/skills/myst-publication/SKILL.md` | 75 | 25 | 50 | 0 | 0 | 0 |
| `.claude/skills/opensysml-api/SKILL.md` | 155 | 76 | 79 | 20 | 7 | 13 |
| `.claude/skills/opensysml-query/SKILL.md` | 182 | 111 | 71 | 6 | 2 | 4 |
| `.claude/skills/orchestrator-protocol/SKILL.md` | 72 | 0 | 72 | 1 | 0 | 1 |
| `.claude/skills/skill-editor/SKILL.md` | 65 | 0 | 65 | 1 | 0 | 1 |
| `.claude/skills/sysml-diagrams/SKILL.md` | 79 | 0 | 79 | 7 | 0 | 7 |
| `.claude/skills/sysml-diagrams/references/recipes.md` | 167 | 52 | 115 | 6 | 0 | 6 |
| `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 192 | 29 | 163 | 24 | 0 | 24 |
| `.claude/skills/toaster-recipe/SKILL.md` | 229 | 55 | 174 | 4 | 4 | 0 |
| `.claude/skills/toaster-review-protocol/SKILL.md` | 193 | 90 | 103 | 0 | 0 | 0 |
| `.claude/skills/tutorial-glossary/SKILL.md` | 61 | 8 | 53 | 1 | 0 | 1 |
| `.claude/skills/tutorial-style-guide/SKILL.md` | 121 | 11 | 110 | 2 | 1 | 1 |
| `.claude/skills/tutorial-supporting-pages/SKILL.md` | 65 | 12 | 53 | 1 | 0 | 1 |
| `.claude/skills/user-testing/SKILL.md` | 160 | 28 | 132 | 0 | 0 | 0 |

(Fence counts include the ``` delimiter lines.)

### Frontmatter `name:` / `description:` lines (line 2 / line 3 of each SKILL.md)

`name:` values equal the directory names and must not change (plan: protected; checker rule f). Lines carrying OpenSysML: `opensysml-api` line 2 (`name: opensysml-api`, KEEP-ID) and line 3 (`description: opensysml v0.9.0 interface — ...`, KEEP-ID by plan OT-6); `opensysml-query` line 2 (`name:`, KEEP-ID) and line 3 (`description: ... with OpenSysML v0.9.0 ...`, RUNTIME, DL-116 item 3 says it becomes "the OpenSysML runtime v0.9.0"). The other 13 skills' `name:`/`description:` lines carry no match. Note `opensysml-query` line 3 ends "Snippets are executed by tests/test_skill_snippets.py."; that clause stays.

### Snippets executed by `tests/test_skill_snippets.py` (skill edits cannot touch these)

1. `.claude/skills/architecture-layers/example-layers.sysml` (whole file, 45 lines, loaded by `test_architecture_layers_example_loads` and `test_opensysml_query_perform_recipe_on_layers_example`). Not a SKILL.md; it has no OpenSysML mention.
2. Every ```` ```python ```` block in `.claude/skills/opensysml-query/SKILL.md` (`python_blocks()` matches a fence line equal to ```` ```python ````), executed in order by `test_opensysml_query_recipes_run_against_ch08`. There are 6 blocks at lines **22-45** (setup; block 0, includes `import opensysml` line 26 and `opensysml.connect(version="v0.9.0")` line 28), **49-55** (block 1), **61-82** (block 2), **88-107** (block 3), **113-126** (block 4, the perform recipe, re-run by `test_opensysml_query_perform_recipe_on_layers_example`), **134-157** (block 5, port-type recipe; used by `test_port_type_conformance_recipe_catches_mismatch_and_accepts_specialization`, blocks 0-2, 3 (split at `flows = `), 5 (split at `assert port_type_mismatches()`)). Everything between those line ranges (including prose lines 129-133 and the paragraph at line 132) is editable prose; the fences themselves and the code inside them are not.
3. No other skill file has code executed by that test. Other fences (opensysml-api lines 11-15, 28, 125, 132; toaster-recipe 55-87; tutorial-style-guide 89; sysml-diagrams/references/recipes.md) are documentation snippets; they are still protected by the plan (checker rule e compares all fenced blocks), but only items 1 and 2 are executed.

## DEFERRED.md: headings and the proposed dated note

DEFERRED.md has 69 matching lines: **13 heading lines (KEEP-ID, byte-identical)** — D-017 (232), D-019 (260), D-020 (269), D-023 (296), D-024 (325), D-026 (342), D-032 (837), D-033 (856), D-034 (865), D-035 (876), D-036 (885), D-037 (894), D-038 (908) — and 56 body lines. Note that headings `## D-004` appears twice in the file (lines 42 and 172); neither carries OpenSysML. Headings are not edited; their GitHub anchors are linked from published pages.

Proposed text of the ONE dated terminology note for the top of DEFERRED.md (insert after the `# Deferred work` heading, before `## D-001`; no heading is touched):

> **Terminology note (2026-10-03, DL-116).** OpenSysML (opensysml.org) is the open-source SysML v2 tool stack; this tutorial uses two of its components, the OpenSysML runtime (Go; `Open-MBEE/OpenSysML`; Python package `opensysml`; pinned v0.9.0) and sysml-toolkit (Rust; `sysmlv2`; pinned v0.9.1). Entries written before this note use a bare "OpenSysML" (and "opensysml") to mean **the OpenSysML runtime**; read them that way. Where an entry records a different result for sysml-toolkit, the entry's own text governs: for D-017, D-019, D-023, D-034, D-035 and D-036 the heading names the runtime's behavior only, and the body states what sysml-toolkit v0.9.1 does. Headings are unchanged because their anchors are linked from published pages.

This wording is composed from DL-116 and the convention; the ACE should confirm. It deliberately lists D-035 (heading says "OpenSysML and the pilot both reject it", but sysml-toolkit warns) in addition to the five entries DL-116 item 7 names; D-037 and D-038 are UNPROBED (runtime-specific CLI/export) and need no listing.

## Truth-class findings

**FALSE-UNDER-STACK** (bare-subject runtime claim contradicted by the toolkit result in the cited entry):
- `AGENTS.md:127` (DEFINE): D-017 line 236: "sysml-toolkit v0
- `DEFERRED.md:232` (KEEP-ID): Heading text is false under the umbrella: line 236 "sysml-toolkit v0
- `DEFERRED.md:260` (KEEP-ID): Line 262: "sysml-toolkit v0
- `DEFERRED.md:262` (RUNTIME): Gap sentence; the following sentence already names sysml-toolkit v0
- `DEFERRED.md:296` (KEEP-ID): Line 298: "sysml-toolkit v0
- `DEFERRED.md:323` (RUNTIME): "OpenSysML itself" is a banned pattern; D-023 line 298 shows sysml-toolkit v0
- `DEFERRED.md:865` (KEEP-ID): Line 867: "sysml-toolkit v0
- `DEFERRED.md:867` (RUNTIME): Same line also: "only OpenSysML silently tolerates it" -> "only the OpenSysML runtime silently tolerates it"; "OpenSysML alone is the outlier" -> "the OpenSysML runtime is the outlier" (drops the bann
- `DEFERRED.md:872` (RUNTIME): Banned pattern "OpenSysML alone"; edit warranted even though a Resolution line
- `DEFERRED.md:876` (KEEP-ID): Heading says OpenSysML rejects it; line 878: "sysml-toolkit v0
- `DEFERRED.md:878` (RUNTIME): Same line also: "there, OpenSysML alone was the outlier tolerating something the other two correctly rejected" -> "there, the OpenSysML runtime was the outlier 
- `DEFERRED.md:880` (RUNTIME): Workaround line; the sentence is exactly the one contrasting with toolkit behavior, so the bare name would now include the toolkit
- `DEFERRED.md:881` (RUNTIME): Resolution line, but it asserts a behavior the toolkit lacks (D-035 line 878)
- `DEFERRED.md:885` (KEEP-ID): Line 887: "sysml-toolkit v0
- `DEFERRED.md:887` (RUNTIME): Same line also: "likely OpenSysML being too permissive" -> "likely the OpenSysML runtime being too permissive"
- `DEFERRED.md:890` (RUNTIME): Resolution line; the contrast "OpenSysML (not sysml-toolkit

**AMBIGUOUS** (needs the ACE; options in the row table): `DEFERRED.md:852`, `.claude/skills/ace-protocol/SKILL.md:63`, `.claude/skills/ace-protocol/z-model.md:21`. Also pending Z (not a row): whether the OMG SysML v2 Pilot Implementation is inside "OpenSysML" (DL-116 item 2, default out; the AGENTS.md 1.2 replacement holds under either answer).

Items DL-116 item 7 did not list, found here: D-035 heading (FALSE-UNDER-STACK), D-037 and D-038 headings/bodies (UNPROBED), D-026/D-027 bodies (UNPROBED), D-003/D-004 (UNPROBED). D-024 and D-020/D-032 are SAME or already contrast both tools.

## Related bare-tool sentences (no "OpenSysML" token; outside the count)

These say "the tool" or similar about a runtime-only or both-tools behavior; the convention ("a claim true of one component names that component") applies if a later pass widens scope:
- `.claude/skills/architecture-layers/SKILL.md:47` "Mismatched port types are **not diagnosed** by the tool (gap G4, ...)" and `:71` "The tool will not diagnose it." (D-014: SAME; both tools accept it).
- `DEFERRED.md` D-019 body (line 263): "The tool rejects `perform ToastBread;` naming a definition (G2)" (runtime behavior; sentence already inside the D-019 gap text).
- `AGENTS.md:147` Gap-tracking rule "where the tool is at fault" (generic; no change).

## Row table

Columns: row id; file; locator (`line` of the file; `F` = inside a code fence); quoted text (verbatim from that line; multi-line quote joined with ⏎); class (`primary; truth`); proposed replacement (with the convention rule it applies in the note column, merged into the replacement cell as "Note:").

| row | file | locator | quoted text (verbatim) | class | proposed replacement |
|---|---|---|---|---|---|
| B-001 | `AGENTS.md` | 43 | **Toolchain, not sources.** OpenSysML, sysml-toolkit, the Pilot Implementation and the like execute the specs. | DEFINE | **Toolchain, not sources.** OpenSysML (opensysml.org), the open-source SysML v2 tool stack, is toolchain: this tutorial uses two of its components, named by role, **the OpenSysML runtime** (Go; repo `Open-MBEE/OpenSysML`; Python package `opensysml`; pinned v0.9.0) and **sysml-toolkit** (Rust; `sysmlv2` binary; pinned v0.9.1). The OMG SysML v2 Pilot Implementation (EPL-2.0) is the conformance baseline and is always named as such. They execute the specs. Note: ACE wording to confirm: the exact DL-116 ACE paragraph is not in the repo (only the Decision (4) summary and the plan's normative convention). This replacement is composed from the convention; the sentence is written so it holds whether the Pilot is in or out of OpenSysML (DL-116 item 2, pending Z). Rest of the paragraph ("They are cited only to flag a spec gap (§1.9), never to define a term.") unchanged. Part 1 governs: orchestrator reads final text before merge. |
| B-002 | `AGENTS.md` | 127 | OpenSysML v0.9.0 does not resolve `import` across separately loaded sources. | DEFINE; FALSE-UNDER-STACK | The OpenSysML runtime v0.9.0 does not resolve `import` across separately loaded sources (sysml-toolkit v0.9.1 does, D-017). Note: D-017 line 236: "sysml-toolkit v0.9.1 resolves the same imports across files (`sysmlv2 check base.sysml chapter.sysml`, `Session.from_files`)". Convention: contrasts name both components. ACE wording to confirm (1.7 bullet wording not in repo). The rest of the bullet (assemble by concatenation, gap G7) unchanged. |
| B-003 | `AGENTS.md` | 137 |  chapter notebook (recipes and limits are in the `opensysml-query` skill): | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-004 | `AGENTS.md` | 139 | 1. `model.query()` in OpenSysML: the API Query | DEFINE | 1. `model.query()` in the OpenSysML runtime: the API Query Note: Convention: a claim about one component's API names it. `model.query()` is the runtime's Python API; the sysml-toolkit binding is the fourth surface (AGENTS.md line 143, no change). ACE wording to confirm. |
| B-005 | `AGENTS.md` | 145 | (OpenSysML v0.9.0 accepts a power port connected to a fuel port; the KerML 1.1 spec searched has no validation constraint for it) | DEFINE; SAME | (the OpenSysML runtime v0.9.0 and sysml-toolkit v0.9.1 both accept a power port connected to a fuel port; the KerML 1.1 spec searched has no validation constraint for it) Note: D-014 lines 192-194: runtime accepts with ok=True; "sysml-toolkit v0.9.1 `check` and `lint` (default rules) accept it too". Truth class SAME. Convention: versions attach to component names; DL-116 item 7 default is runtime-only wording ("the OpenSysML runtime v0.9.0 accepts"); the both-components form is offered because D-014 probed both. ACE wording to confirm which. |
| B-006 | `AGENTS.md` | 266 | Never invent opensysml API shapes not in the adapter file. | KEEP-ID | (no change) Note: Lowercase `opensysml` is the Python package name (protected token class: package names). |
| B-007 | `CLAUDE.md` | 19 | policy only), Douglas (story and the toaster example). OpenSysML and sysml-toolkit ⏎ are toolchain, cited only to flag spec gaps. | DEFINE | policy only), Douglas (story and the toaster example). The OpenSysML runtime and sysml-toolkit (components of OpenSysML, opensysml.org) ⏎ are toolchain, cited only to flag spec gaps. Note: Spans CLAUDE.md lines 19-20 (match is on line 19). ACE wording to confirm (the "CLAUDE.md sources line" wording is not in the repo). Alternative if the stack is to be named: "OpenSysML (its runtime and sysml-toolkit) and the Pilot Implementation are toolchain". |
| B-008 | `CLAUDE.md` | 26 | - opensysml-query           — the three query surfaces, tested recipes, | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-009 | `CLAUDE.md` | 28 | - opensysml-api             — opensysml v0.9.0 interface (A2, A5) | KEEP-ID | (no change) Note: Skill list entry: skill name and its frontmatter description (unchanged per DL-116/plan OT-6: description uses the package name). Optional: none. |
| B-010 | `DEFERRED.md` | 5 | urn `SatisfyRequirementUsage` elements (Open-MBEE/OpenSysML#TBD). | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-011 | `DEFERRED.md` | 12 | ips, update `get_satisfy_relationships()` and the opensysml-api skill. | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-012 | `DEFERRED.md` | 13 | **Upstream issue:** Open-MBEE/OpenSysML#590 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-013 | `DEFERRED.md` | 29 | `ISQ::DimensionOneValue` is not defined in opensysml v0.9.0 (Open-MBEE/OpenSysML#TBD). | RUNTIME; UNPROBED | `ISQ::DimensionOneValue` is not defined in the OpenSysML runtime v0.9.0 (`opensysml`; Open-MBEE/OpenSysML#TBD). Note: Gap sentence. D-003 has no sysml-toolkit result, so UNPROBED. Version attaches to the component name (convention). |
| B-014 | `DEFERRED.md` | 35 | **Resolution:** When `ISQ::DimensionOneValue` and `SI::one` ship in opensysml: | RUNTIME; UNPROBED | **Resolution:** When `ISQ::DimensionOneValue` and `SI::one` ship in the OpenSysML runtime: Note: Resolution line restating the gap; optional. If the Resolution rule (gap sentence only) is applied strictly, class becomes KEEP-BODY. |
| B-015 | `DEFERRED.md` | 39 | **Upstream issue:** Open-MBEE/OpenSysML#594 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-016 | `DEFERRED.md` | 50 | **Upstream issue:** Open-MBEE/OpenSysML#595 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-017 | `DEFERRED.md` | 62 | **Upstream issue:** Open-MBEE/OpenSysML#596 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-018 | `DEFERRED.md` | 73 | **Upstream issue:** Open-MBEE/OpenSysML#597 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-019 | `DEFERRED.md` | 85 | **Upstream issue:** Open-MBEE/OpenSysML#598 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-020 | `DEFERRED.md` | 97 | **Upstream issue:** Open-MBEE/OpenSysML#599 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-021 | `DEFERRED.md` | 111 | **Upstream issue:** Open-MBEE/OpenSysML#601 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-022 | `DEFERRED.md` | 123 | **Upstream issue:** Open-MBEE/OpenSysML#602 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-023 | `DEFERRED.md` | 139 | **Upstream issue:** Open-MBEE/OpenSysML#603 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-024 | `DEFERRED.md` | 154 | **Upstream issue:** Open-MBEE/OpenSysML#604 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-025 | `DEFERRED.md` | 169 | **Upstream issue:** Open-MBEE/OpenSysML#605 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-026 | `DEFERRED.md` | 179 | In OpenSysML v0.9.0 this raises "expected a body member" and `ok=False`. | RUNTIME; UNPROBED | In the OpenSysML runtime v0.9.0 this raises "expected a body member" and `ok=False`. Note: D-004 (VerificationMethodKind): no toolkit result in the entry. Gap sentence. |
| B-027 | `DEFERRED.md` | 187 | **Upstream issue:** Open-MBEE/OpenSysML#608 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-028 | `DEFERRED.md` | 192 | OpenSysML v0.9.0 accepts `connect outlet.o to torch.fuelIn` | RUNTIME; SAME | The OpenSysML runtime v0.9.0 accepts `connect outlet.o to torch.fuelIn` Note: D-014 line 193: "sysml-toolkit v0.9.1 `check` and `lint` (default rules) accept it too". Minimal insertion of "The ... runtime" in the gap sentence; the next sentence already names the toolkit. |
| B-029 | `DEFERRED.md` | 199 | ort_type_mismatches(model)` (tested; recipe 5 in `opensysml-query`), applied from the | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-030 | `DEFERRED.md` | 207 | Probed 2026-09-26 (OpenSysML v0.9.0): named `allocation`, `connection` and `flow` are visible to `model.query()`; | RUNTIME; UNPROBED | Probed 2026-09-26 (the OpenSysML runtime v0.9.0): named `allocation`, `connection` and `flow` are visible to `model.query()`; Note: D-015 is about the runtime's `model.query()` API; no toolkit comparison in the entry. |
| B-031 | `DEFERRED.md` | 214 | Related: OpenSysML#590 (closed 2026-09-26). A maintainer said anonymous elemen | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-032 | `DEFERRED.md` | 218 | **Upstream issue:** filed 2026-09-27, [OpenSysML#643](https://github.com/Open-MBEE/OpenSysML/issues/643) | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-033 | `DEFERRED.md` | 229 | **Upstream issue:** filed 2026-09-27, [OpenSysML#644](https://github.com/Open-MBEE/OpenSysML/issues/644) | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-034 | `DEFERRED.md` | 232 | ## D-017: `import` across separately loaded sources does not resolve in OpenSysML (gap G7) | KEEP-ID; FALSE-UNDER-STACK | (heading protected; byte-identical) Note: Heading text is false under the umbrella: line 236 "sysml-toolkit v0.9.1 resolves the same imports across files". Reading rule in the dated top note must cover it. DL-116 item 7 lists D-017. |
| B-035 | `DEFERRED.md` | 244 | Re-test when OpenSysML changes. | KEEP-BODY | (no change) Note: Resolution sentence. Option if edited: "Re-test when the OpenSysML runtime changes." |
| B-036 | `DEFERRED.md` | 245 | **Upstream issue:** filed 2026-09-27, [OpenSysML#645](https://github.com/Open-MBEE/OpenSysML/issues/645) (fi | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-037 | `DEFERRED.md` | 260 | ## D-019: OpenSysML accepts an allocate between definitions (language conformance hole) | KEEP-ID; FALSE-UNDER-STACK | (heading protected; byte-identical) Note: Line 262: "sysml-toolkit v0.9.1 with the standard library rejects it". DL-116 item 7 lists D-019. |
| B-038 | `DEFERRED.md` | 262 | OpenSysML v0.9.0 loads `allocate ApplyHeat to HeatingSystem;` | RUNTIME; FALSE-UNDER-STACK | The OpenSysML runtime v0.9.0 loads `allocate ApplyHeat to HeatingSystem;` Note: Gap sentence; the following sentence already names sysml-toolkit v0.9.1 rejecting it. |
| B-039 | `DEFERRED.md` | 265 | **Resolution:** upstream fix in OpenSysML; re-test with `scripts/probes`. | KEEP-BODY | (no change) Note: Resolution/non-gap sentence; DL-116 (3) permits "runtime" only in the sentence stating the gap; the dated top note carries the reading rule. Option if edited: "upstream fix in the OpenSysML runtime". |
| B-040 | `DEFERRED.md` | 266 | **Upstream issue:** filed 2026-09-27, [OpenSysML#646](https://github.com/Open-MBEE/OpenSysML/issues/646) (ci | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-041 | `DEFERRED.md` | 269 | ## D-020: Neither OpenSysML nor sysml-toolkit reports a part usage typed only by an item definition | KEEP-ID; SAME | (heading protected; byte-identical) Note: Line 271: runtime ok=True and "passes sysml-toolkit v0.9.1 `check --lib`". Heading uses the banned pattern "Neither OpenSysML nor" but is protected; true as stated only if OpenSysML is read as the runtime (reading rule). DL-116 item 7: D-020 is toolkit-same. |
| B-042 | `DEFERRED.md` | 271 | loads with `ok=True` in OpenSysML v0.9.0 and passes sysml-toolkit v0.9.1 `check --lib` | RUNTIME; SAME | loads with `ok=True` in the OpenSysML runtime v0.9.0 and passes sysml-toolkit v0.9.1 `check --lib` Note: Gap sentence; contrast already names both tools. |
| B-043 | `DEFERRED.md` | 275 | **Upstream issue:** filed 2026-09-27, [OpenSysML#647](https://github.com/Open-MBEE/OpenSysML/issues/647) and | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-044 | `DEFERRED.md` | 296 | ## D-023: OpenSysML does not resolve state-machine transition trigger names | KEEP-ID; FALSE-UNDER-STACK | (heading protected; byte-identical) Note: Line 298: "sysml-toolkit v0.9.1 does resolve these names and warns on broken references". DL-116 item 7 lists D-023. |
| B-045 | `DEFERRED.md` | 323 | loads with `ok=True` (OpenSysML itself does not catch it) | RUNTIME; FALSE-UNDER-STACK | loads with `ok=True` (the OpenSysML runtime does not catch it) Note: "OpenSysML itself" is a banned pattern; D-023 line 298 shows sysml-toolkit v0.9.1 resolves trigger names. Same-entry note, gap sentence. |
| B-046 | `DEFERRED.md` | 325 | ## D-024: RETRACTED — OpenSysML v0.9.0's Python binding cannot ask a "holds" question (sysml-toolkit can) | KEEP-ID; SAME | (heading protected; byte-identical) Note: Heading already contrasts the runtime's binding with sysml-toolkit; true as stated under the convention (bare name = runtime in this entry). |
| B-047 | `DEFERRED.md` | 327 | it checked only OpenSysML. `sysmlv2 verify --solve` | RUNTIME; SAME | it checked only the OpenSysML runtime. `sysmlv2 verify --solve` Note: Same line also has "OpenSysML's own gap (its Python binding is evaluate-only) still stands as a fact" -> "the OpenSysML runtime's own gap (its Python binding is evaluate-only)". Truth: line 327 itself says sysml-toolkit does `verify --solve`; the original claim "no tool in the toolchain" was the retracted false-under-stack-style error. Two replacements, one row. |
| B-048 | `DEFERRED.md` | 336 | (b) OpenSysML's Python binding gains a way to pose a holds/outcomes question to its own `check`/`smt` engines (D-024's original ask, still true as a fact about OpenSysML even though it is no longer blocking) | RUNTIME; SAME | (b) the OpenSysML runtime's Python binding gains a way to pose a holds/outcomes question to its own `check`/`smt` engines (D-024's original ask, still true as a fact about the OpenSysML runtime even though it is no longer blocking) Note: Resolution line, but it restates a capability gap and (a) in the same sentence names sysml-toolkit; the bare name would now read as including the toolkit. Optional; KEEP-BODY if the strict rule is applied. |
| B-049 | `DEFERRED.md` | 342 | ## D-026: OpenSysML treats an implicit and an explicit-but-spec-identical `[0..*]` multiplicity differently for an `in` parameter reachable through a nested action step | KEEP-ID; UNPROBED | (heading protected; byte-identical) Note: No sysml-toolkit result anywhere in D-026 (lines 342-546, grep toolkit: none). UNPROBED. |
| B-050 | `DEFERRED.md` | 346 | OpenSysML v0.9.0 can evaluate the model. | RUNTIME; UNPROBED | The OpenSysML runtime v0.9.0 can evaluate the model. Note: Line starts "OpenSysML v0.9.0 can evaluate the model." Gap sentence. |
| B-051 | `DEFERRED.md` | 408 | **The mechanism this evidence actually supports:** OpenSysML v0.9.0 gives a | RUNTIME; UNPROBED | **The mechanism this evidence actually supports:** The OpenSysML runtime v0.9.0 gives a Note: Wrapped sentence (continues on 409). Replace "OpenSysML v0.9.0 gives a" with "the OpenSysML runtime v0.9.0 gives a" (lower-case after the bold lead-in). |
| B-052 | `DEFERRED.md` | 581 | since two OpenSysML surfaces (load, and the API-JSON conversion this | RUNTIME; UNPROBED | since two OpenSysML runtime surfaces (load, and the API-JSON conversion this Note: D-027 (lines 547-599): load and API-JSON conversion are runtime surfaces; no toolkit result. |
| B-053 | `DEFERRED.md` | 837 | ## D-032: OpenSysML accepts an allocate connector end that reaches into another type's nested feature by qualified name, with no featuring context to make it accessible (GUARDED) | KEEP-ID; SAME | (heading protected; byte-identical) Note: Line 839: "sysml-toolkit v0.9.1 accepts it too". DL-116 item 7: toolkit-same. |
| B-054 | `DEFERRED.md` | 839 | OpenSysML v0.9.0 loads `allocate <expr> to <Def>::<usage>;` | RUNTIME; SAME | The OpenSysML runtime v0.9.0 loads `allocate <expr> to <Def>::<usage>;` Note: Gap sentence; same sentence continues "sysml-toolkit v0.9.1 accepts it too". |
| B-055 | `DEFERRED.md` | 845 | OpenSysML accepted it with zero findings, the pilot rejected it. | RUNTIME; UNPROBED | the OpenSysML runtime accepted it with zero findings, the pilot rejected it. Note: Probe of a specific fixture against the runtime and the pilot only; no toolkit result for this fixture. Lower-case "the" mid-sentence after the semicolon. |
| B-056 | `DEFERRED.md` | 849 | The underlying OpenSysML/sysml-toolkit acceptance-without-diagnostic gap itself remains open upstream | BOTH; SAME | The underlying acceptance-without-diagnostic gap in the OpenSysML runtime and sysml-toolkit itself remains open upstream Note: D-032 line 839 shows both accept. "OpenSysML/sysml-toolkit" reads as parent/child under the new meaning. Convention: contrasts/conjunctions name both components. Edit sits in a status sentence, not the heading. |
| B-057 | `DEFERRED.md` | 852 | **Resolution:** upstream fix in both OpenSysML and sysml-toolkit; re-test with `scripts/probes`. | AMBIGUOUS | Option A (leave, KEEP-BODY): the top note's reading rule says a bare name before DL-116 means the runtime. Option B: "**Resolution:** upstream fix in both the OpenSysML runtime and sysml-toolkit; re-test with `scripts/probes`." Note: Banned pattern "OpenSysML and sysml-toolkit" in a Resolution line (outside the gap sentence, so outside DL-116 (3) permission). Needs the ACE. |
| B-058 | `DEFERRED.md` | 856 | ## D-033: OpenSysML's `eval()` does not simplify a product against a `DimensionOneUnit` factor, or fold an SI base-unit expansion back into its derived-unit symbol | KEEP-ID; UNPROBED | (heading protected; byte-identical) Note: No sysml-toolkit comparison in D-033 (lines 856-863). `eval()` is a runtime Python API. UNPROBED (DL-116 item 7 agrees). |
| B-059 | `DEFERRED.md` | 858 | OpenSysML DOES normally resolve a `kg⋅m²⋅s⁻²` base-unit product | RUNTIME; UNPROBED | The OpenSysML runtime DOES normally resolve a `kg⋅m²⋅s⁻²` base-unit product Note: Gap sentence. Quote is the start of the sentence inside a long line (line 858). |
| B-060 | `DEFERRED.md` | 860 | with a note that OpenSysML's own printed output shows an unsimplified unit expression | RUNTIME; UNPROBED | with a note that the OpenSysML runtime's own printed output shows an unsimplified unit expression Note: Workaround line describing what chapters/ch07 index.md and nb01 cells 14, 17, 18 say; those learner-surface markdown cells are covered by OT-1a/OT-3B and must carry the same wording. |
| B-061 | `DEFERRED.md` | 861 | **Resolution:** upstream fix in OpenSysML's `eval()`/`Quantity`/`Unit` display logic | KEEP-BODY | (no change) Note: Resolution/non-gap sentence; DL-116 (3) permits "runtime" only in the sentence stating the gap; the dated top note carries the reading rule. Names the runtime's own `eval()` API, so the bare name is unambiguous; option: "the OpenSysML runtime's". |
| B-062 | `DEFERRED.md` | 865 | ## D-034: `filter` is a reserved word in the real SysML v2 grammar; OpenSysML alone accepts it as a bare feature name with no diagnostic | KEEP-ID; FALSE-UNDER-STACK | (heading protected; byte-identical) Note: Line 867: "sysml-toolkit v0.9.1 correctly REJECTS bare `filter` too ... only OpenSysML silently tolerates it". "OpenSysML alone" is false under the umbrella. DL-116 item 7 lists D-034. |
| B-063 | `DEFERRED.md` | 867 | loads with `model.ok == True` and zero diagnostics in OpenSysML v0.9.0. | RUNTIME; FALSE-UNDER-STACK | loads with `model.ok == True` and zero diagnostics in the OpenSysML runtime v0.9.0. Note: Same line also: "only OpenSysML silently tolerates it" -> "only the OpenSysML runtime silently tolerates it"; "OpenSysML alone is the outlier" -> "the OpenSysML runtime is the outlier" (drops the banned "alone"). Three replacements, one row. |
| B-064 | `DEFERRED.md` | 872 | **Resolution:** upstream fix in OpenSysML alone (diagnose a reserved-word-as-identifier collision at parse time, matching sysml-toolkit's and the pilot's own behavior) | RUNTIME; FALSE-UNDER-STACK | **Resolution:** upstream fix in the OpenSysML runtime (diagnose a reserved-word-as-identifier collision at parse time, matching sysml-toolkit's and the pilot's own behavior) Note: Banned pattern "OpenSysML alone"; edit warranted even though a Resolution line. Truth: D-034 line 867 shows toolkit rejects. |
| B-065 | `DEFERRED.md` | 876 | ## D-035: sysml-toolkit reports an `assert satisfy`/`assert not satisfy` naming an undeclared requirement as a warning, not an error; OpenSysML and the pilot both reject it outright | KEEP-ID; FALSE-UNDER-STACK | (heading protected; byte-identical) Note: Heading says OpenSysML rejects it; line 878: "sysml-toolkit v0.9.1 ... reports `warning: unresolved reference 'missingReq'` and exits 0". False if OpenSysML includes the toolkit. NOT listed in DL-116 item 7 (omission to flag). |
| B-066 | `DEFERRED.md` | 878 | confirmed correct against OpenSysML v0.9.0 (`bad.ok == False`) | RUNTIME; FALSE-UNDER-STACK | confirmed correct against the OpenSysML runtime v0.9.0 (`bad.ok == False`) Note: Same line also: "there, OpenSysML alone was the outlier tolerating something the other two correctly rejected" -> "there, the OpenSysML runtime was the outlier ...". Caution: that sentence cites D-032 as an "OpenSysML alone" case but D-032 line 839 says sysml-toolkit accepts too (pre-existing inconsistency in the entry; do not fix, flag). |
| B-067 | `DEFERRED.md` | 880 | assert against OpenSysML's behavior only, matching the pattern real Chapter 9 notebook 01 already uses (`bad.ok == False`) | RUNTIME; FALSE-UNDER-STACK | assert against the OpenSysML runtime's behavior only, matching the pattern real Chapter 9 notebook 01 already uses (`bad.ok == False`) Note: Workaround line; the sentence is exactly the one contrasting with toolkit behavior, so the bare name would now include the toolkit. |
| B-068 | `DEFERRED.md` | 881 | matching OpenSysML's and the pilot's own behavior) | RUNTIME; FALSE-UNDER-STACK | matching the OpenSysML runtime's and the pilot's own behavior) Note: Resolution line, but it asserts a behavior the toolkit lacks (D-035 line 878). |
| B-069 | `DEFERRED.md` | 885 | ## D-036: the `connector` keyword (a KerML-only construct) is accepted in a `.sysml` file by OpenSysML; sysml-toolkit and the pilot both correctly reject it there | KEEP-ID; FALSE-UNDER-STACK | (heading protected; byte-identical) Note: Line 887: "sysml-toolkit v0.9.1 rejects every one at parse time". DL-116 item 7 lists D-036. |
| B-070 | `DEFERRED.md` | 887 | OpenSysML v0.9.0 loads each cleanly (`model.ok == True`, no diagnostics) | RUNTIME; FALSE-UNDER-STACK | The OpenSysML runtime v0.9.0 loads each cleanly (`model.ok == True`, no diagnostics) Note: Same line also: "likely OpenSysML being too permissive" -> "likely the OpenSysML runtime being too permissive". |
| B-071 | `DEFERRED.md` | 890 | file an upstream issue against OpenSysML (not sysml-toolkit/the pilot) | RUNTIME; FALSE-UNDER-STACK | file an upstream issue against the OpenSysML runtime (`Open-MBEE/OpenSysML`; not sysml-toolkit or the pilot) Note: Resolution line; the contrast "OpenSysML (not sysml-toolkit...)" would be false under the umbrella. Never counts the pilot among the stack tools. |
| B-072 | `DEFERRED.md` | 894 | ## D-037: OpenSysML's own `-render` CLI drops real content from both action-flow and state diagrams | KEEP-ID; UNPROBED | (heading protected; byte-identical) Note: Runtime-specific CLI (`opensysml -render`); no sysml-toolkit `viz` comparison in D-037 (D-018 covers `sysmlv2 viz` separately). UNPROBED; not in DL-116 item 7 (omission to flag). |
| B-073 | `DEFERRED.md` | 896 | both shell out to OpenSysML's own `-render '#action:...' -render-form dot` / `-render '#state:...' -render-form dot` CLI | RUNTIME; UNPROBED | both shell out to the OpenSysML runtime's own `-render '#action:...' -render-form dot` / `-render '#state:...' -render-form dot` CLI Note: Gap sentence. |
| B-074 | `DEFERRED.md` | 901 | (OpenSysML's `-render` CLI) | RUNTIME; UNPROBED | (the OpenSysML runtime's `-render` CLI) Note: Gap sentence. |
| B-075 | `DEFERRED.md` | 904 | either an upstream fix in OpenSysML's own `-render` CLI | KEEP-BODY | (no change) Note: Resolution/non-gap sentence; DL-116 (3) permits "runtime" only in the sentence stating the gap; the dated top note carries the reading rule. Names the runtime's own CLI; option: "the OpenSysML runtime's own `-render` CLI". |
| B-076 | `DEFERRED.md` | 908 | ## D-038: OpenSysML's API-JSON export has no structural `subjectParameter` key on `RequirementDefinition`; Ch10 reads each candidate feature's own `sysx:sourceText` instead | KEEP-ID; UNPROBED | (heading protected; byte-identical) Note: Runtime API-JSON export; no toolkit result in D-038. UNPROBED; not in DL-116 item 7 (omission to flag). |
| B-077 | `DEFERRED.md` | 910 | The API-JSON export OpenSysML v0.9.0 produces carries no `subjectParameter` key | RUNTIME; UNPROBED | The API-JSON export the OpenSysML runtime v0.9.0 produces carries no `subjectParameter` key Note: Gap sentence. |
| B-078 | `DEFERRED.md` | 913 | **Resolution:** upstream fix in OpenSysML's API-JSON export | KEEP-BODY | (no change) Note: Resolution/non-gap sentence; DL-116 (3) permits "runtime" only in the sentence stating the gap; the dated top note carries the reading rule. Names the runtime's own export; option: "the OpenSysML runtime's API-JSON export". |
| B-079 | `glossary/sources/notes/reading-notes.md` | 35 | - OpenSysML, sysml-toolkit and the Pilot Implementation are toolchain, cited only to flag spec gaps. They define no terms. | RUNTIME | - The OpenSysML runtime, sysml-toolkit (both components of OpenSysML) and the Pilot Implementation are toolchain, cited only to flag spec gaps. They define no terms. Note: Under the umbrella the original list names the parent and a child in parallel. Not a glossary term and not a .ttl; `uv run python -m glossary check` must still pass. Mirrors AGENTS.md line 43 wording; ACE wording to confirm. |
| B-080 | `.claude/agents/layer-auditor.md` | 12 | ery the model with the recipes in `.claude/skills/opensysml-query/SKILL.md` or `toaster.query`, and read known files by | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-081 | `.claude/agents/orchestrator.md` | 36 |  the glossary CLI, `model.query`, the recipes in `opensysml-query`, and direct reads of known files and ranges. | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-082 | `.claude/skills/ace-protocol/SKILL.md` | 63 | \| SA-6 \| Bounded model checking: opensysml `check` engine only \| | AMBIGUOUS | Option A: "\| SA-6 \| Bounded model checking: the OpenSysML runtime's `check` engine only \|". Option B: leave (dated scope decision SA-6) and add a note that `sysmlv2 verify --solve` (sysml-toolkit) is used via toaster.modelcheck per D-024/D-025. Note: SA-6 is a dated scope decision that predates D-024 (sysml-toolkit v0.9.1 `verify --solve` via Z3 now in use). Rewriting changes what a scope decision says. ACE (author of the skill) should rule. |
| B-083 | `.claude/skills/ace-protocol/SKILL.md` | 132 | - Required opensysml capability missing from v0.9.0 with no workable simplification | RUNTIME | - Required OpenSysML runtime capability missing from v0.9.0 with no workable simplification Note: Escalation trigger; version attaches to the runtime. Optional: "and no sysml-toolkit alternative". |
| B-084 | `.claude/skills/ace-protocol/z-model.md` | 21 | - Z-12. OpenSysML and other implementations are toolchain, cited only to flag spec gaps. | AMBIGUOUS | Option A: "- Z-12. The OpenSysML runtime, sysml-toolkit and the Pilot Implementation are toolchain, cited only to flag spec gaps." Option B: leave as Z's recorded position (z-model records Z's positions; Z-12 is cited by DL-116 provenance) and rely on the reading rule. Note: z-model entries are Z's positions with ids cited in DL-116 ("z-model Z-12"). Editing the wording of a numbered Z position is the ACE's/Z's call. Skill prose, ACE-edited in OT-6. |
| B-085 | `.claude/skills/architecture-layers/SKILL.md` | 47 | rmance check (AGENTS.md 1.9) and use recipe 5 in `opensysml-query`, with a negative control. \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-086 | `.claude/skills/architecture-layers/SKILL.md` | 71 | el port)? Apply the port-type conformance check (`opensysml-query` recipe 5) from the point the connection is declared  | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-087 | `.claude/skills/architecture-layers/SKILL.md` | 95 | \| Tool behavior \| `decisions/probes.md`, `opensysml-query` \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-088 | `.claude/skills/opensysml-api/SKILL.md` | 2 | name: opensysml-api | KEEP-ID | (no change) Note: Frontmatter `name:` line; protected. |
| B-089 | `.claude/skills/opensysml-api/SKILL.md` | 3 | description: opensysml v0.9.0 interface — correct method names, return shapes, limitations, and the D-001 encapsulation rule. | KEEP-ID | (no change) Note: Plan OT-6: "`opensysml-api` description stays (\"opensysml v0.9.0 interface\" uses the package name)". Frontmatter line. |
| B-090 | `.claude/skills/opensysml-api/SKILL.md` | 6 | # OpenSysML v0.9.0 API | RUNTIME | # The OpenSysML runtime v0.9.0 API Note: H1 (not frontmatter). Version attaches to a component name. Not covered by DL-116 explicit wording; derived from the convention. |
| B-091 | `.claude/skills/opensysml-api/SKILL.md` | 11 (F) | import opensysml | KEEP-ID | (no change) Note: Inside a code fence. |
| B-092 | `.claude/skills/opensysml-api/SKILL.md` | 12 (F) | import opensysml.binary | KEEP-ID | (no change) Note: Inside a code fence. |
| B-093 | `.claude/skills/opensysml-api/SKILL.md` | 14 (F) | opensysml.binary.ensure_binary(version="v0.9.0") | KEEP-ID | (no change) Note: Inside a code fence. |
| B-094 | `.claude/skills/opensysml-api/SKILL.md` | 15 (F) | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) Note: Inside a code fence. |
| B-095 | `.claude/skills/opensysml-api/SKILL.md` | 28 (F) | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) Note: Inside a code fence. |
| B-096 | `.claude/skills/opensysml-api/SKILL.md` | 75 | \| `abstract part def` \| toaster#9 / OpenSysML#595 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-097 | `.claude/skills/opensysml-api/SKILL.md` | 76 | \| `attribute :>>` redefinition \| toaster#10 / OpenSysML#596 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-098 | `.claude/skills/opensysml-api/SKILL.md` | 77 | \| `require constraint { ... }` \| toaster#11 / OpenSysML#597 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-099 | `.claude/skills/opensysml-api/SKILL.md` | 78 | \| `assert satisfy R by P` \| toaster#12 / OpenSysML#598 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-100 | `.claude/skills/opensysml-api/SKILL.md` | 79 | \| `allocate X to Y` \| toaster#13 / OpenSysML#599 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-101 | `.claude/skills/opensysml-api/SKILL.md` | 80 | \| `flow X.port to Y.port` \| toaster#14 / OpenSysML#TBD \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-102 | `.claude/skills/opensysml-api/SKILL.md` | 81 |  usage` (sub-state) + `transition` \| toaster#15 / OpenSysML#TBD \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-103 | `.claude/skills/opensysml-api/SKILL.md` | 111 | ted in Pass 1, see `tests/test_query.py` and the `opensysml-query` skill). | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-104 | `.claude/skills/opensysml-api/SKILL.md` | 125 (F) | satisfy, and metadata are invisible here; see the opensysml-query skill. | KEEP-ID | (no change) Note: Inside a code fence. |
| B-105 | `.claude/skills/opensysml-api/SKILL.md` | 132 (F) | helpers in src/toaster/query.py or the recipes in opensysml-query | KEEP-ID | (no change) Note: Inside a code fence. |
| B-106 | `.claude/skills/opensysml-api/SKILL.md` | 152 | `OPENSYSML_VERSION` (preferred), `OPENSYSML_GRPC_VERSION` (upstream fa | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-107 | `.claude/skills/opensysml-api/SKILL.md` | 154 | **Reference:** `sysmlv2-testing/adapters/opensysml.py` — authoritative; probed 2026-09-25 against v0.9.0. | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-108 | `.claude/skills/opensysml-query/SKILL.md` | 2 | name: opensysml-query | KEEP-ID | (no change) Note: Frontmatter `name:` line; protected. |
| B-109 | `.claude/skills/opensysml-query/SKILL.md` | 3 | description: Tested cookbook for interrogating a loaded SysML v2 model with OpenSysML v0.9.0 | RUNTIME | description: Tested cookbook for interrogating a loaded SysML v2 model with the OpenSysML runtime v0.9.0 Note: DL-116 item 3: "description and H1 say \"the OpenSysML runtime v0.9.0\"". Frontmatter `description:` line (editable; `name:` line 2 is not). |
| B-110 | `.claude/skills/opensysml-query/SKILL.md` | 6 | # Querying a model (OpenSysML v0.9.0) | RUNTIME | # Querying a model (the OpenSysML runtime v0.9.0) Note: H1; DL-116 item 3. |
| B-111 | `.claude/skills/opensysml-query/SKILL.md` | 26 (F) | import opensysml | KEEP-ID | (no change) Note: Inside an executed ```python block (tests/test_skill_snippets.py). |
| B-112 | `.claude/skills/opensysml-query/SKILL.md` | 28 (F) | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) Note: Inside an executed ```python block (tests/test_skill_snippets.py). |
| B-113 | `.claude/skills/opensysml-query/SKILL.md` | 132 | OpenSysML accepts a connection between ports of unrelated types with no diagnostic (gap G4 | BOTH; SAME | The OpenSysML runtime v0.9.0 and sysml-toolkit v0.9.1 both accept a connection between ports of unrelated types with no diagnostic (gap G4 Note: D-014 lines 192-194 (toolkit `check`/`lint` accept it too). Prose paragraph between code fences (lines 113-126 and 134-157 are executed blocks; line 132 is outside them). |
| B-114 | `.claude/skills/orchestrator-protocol/SKILL.md` | 37 | - Required construct unavailable in opensysml==0.9.0 | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-115 | `.claude/skills/skill-editor/SKILL.md` | 53 | - Incorrect API shape or return type in `opensysml-api` | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-116 | `.claude/skills/sysml-diagrams/SKILL.md` | 16 | rendering a single root via OpenSysML's `#tree:` form only shows that root's own direct features | RUNTIME; UNPROBED | rendering a single root via the OpenSysML runtime's `#tree:` form only shows that root's own direct features Note: Runtime `-render` CLI. Table cell. |
| B-117 | `.claude/skills/sysml-diagrams/SKILL.md` | 18 | \| OpenSysML CLI, `-render #action:element -render-form dot` → Graphviz SVG \| | RUNTIME; UNPROBED | \| OpenSysML runtime CLI, `-render #action:element -render-form dot` → Graphviz SVG \| Note: Table cell. |
| B-118 | `.claude/skills/sysml-diagrams/SKILL.md` | 19 | \| OpenSysML CLI, `-render #state:element -render-form dot` → Graphviz SVG \| | RUNTIME; UNPROBED | \| OpenSysML runtime CLI, `-render #state:element -render-form dot` → Graphviz SVG \| Note: Same line also: "100% success across both OpenSysML render forms" -> "both OpenSysML runtime render forms". |
| B-119 | `.claude/skills/sysml-diagrams/SKILL.md` | 20 | \| OpenSysML sequence query → DOT → Graphviz SVG \| | RUNTIME; UNPROBED | \| OpenSysML runtime sequence query → DOT → Graphviz SVG \| Note: Same line also has the command `opensysml -render-form dot` inside backticks: KEEP-ID (executable name). |
| B-120 | `.claude/skills/sysml-diagrams/SKILL.md` | 56 | - **OpenSysML CLI (`-render-form dot`)** — action flow and state views | RUNTIME; UNPROBED | - **OpenSysML runtime CLI (`-render-form dot`)** — action flow and state views |
| B-121 | `.claude/skills/sysml-diagrams/SKILL.md` | 62 | found opensysml had no native DOT or render-form CLI | RUNTIME; UNPROBED | found the OpenSysML runtime had no native DOT or render-form CLI Note: Same line also: "the earlier finding about OpenSysML's CLI itself no longer holds" -> "the earlier finding about the OpenSysML runtime's CLI no longer holds" (drops "itself"). |
| B-122 | `.claude/skills/sysml-diagrams/SKILL.md` | 64 | For action flow and state: OpenSysML's own `-render` CLI, not a custom Python renderer | RUNTIME; UNPROBED | For action flow and state: the OpenSysML runtime's own `-render` CLI, not a custom Python renderer |
| B-123 | `.claude/skills/sysml-diagrams/references/recipes.md` | 9 | is the pinned OpenSysML CLI; `model.sysml` is the chapter-generated snapshot. | RUNTIME | is the pinned OpenSysML runtime CLI; `model.sysml` is the chapter-generated snapshot. Note: Prose (line 9 of the file; not in a code fence). |
| B-124 | `.claude/skills/sysml-diagrams/references/recipes.md` | 74 | the way OpenSysML's own interconnection export does | RUNTIME | the way the OpenSysML runtime's own interconnection export does |
| B-125 | `.claude/skills/sysml-diagrams/references/recipes.md` | 83 | ## Action flow — OpenSysML | RUNTIME | ## Action flow — OpenSysML runtime Note: Heading in a reference file; no anchors inbound known (not a protected heading). |
| B-126 | `.claude/skills/sysml-diagrams/references/recipes.md` | 100 | ## State transition — OpenSysML | RUNTIME | ## State transition — OpenSysML runtime |
| B-127 | `.claude/skills/sysml-diagrams/references/recipes.md` | 110 | 100% success across both OpenSysML render forms | RUNTIME | 100% success across both OpenSysML runtime render forms |
| B-128 | `.claude/skills/sysml-diagrams/references/recipes.md` | 119 | ## Sequence — OpenSysML and Mermaid | RUNTIME | ## Sequence — OpenSysML runtime and Mermaid |
| B-129 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 8 | ## Confirmed construct subset (opensysml v0.9.0) | RUNTIME; UNPROBED | ## Confirmed construct subset (the OpenSysML runtime, `opensysml` v0.9.0) Note: "Confirmed" = probed against the runtime only; no toolkit result for the subset. |
| B-130 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 29 | This metadata construct does not parse in OpenSysML v0.9.0 | RUNTIME; UNPROBED | This metadata construct does not parse in the OpenSysML runtime v0.9.0 Note: D-004 (VerificationMethodKind) has no toolkit result. Token `OpenSysML#608` on the same line: KEEP-ID. |
| B-131 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 78 | ## ISQ/SI unit typing — confirmed in opensysml v0.9.0 | RUNTIME; UNPROBED | ## ISQ/SI unit typing — confirmed in the OpenSysML runtime v0.9.0 |
| B-132 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 133 | and opensysml edit.py. All five constructs parse correctly | KEEP-ID | (no change) Note: "opensysml edit.py" names a file in the Python package (file/package name). |
| B-133 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 138 | \| D-004 \| `abstract part def` \| Ch1 \| OpenSysML#595 \| `conn.load_from_content()` \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-134 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 139 | \| D-005 \| `attribute :>>` redefinition \| Ch2 \| OpenSysML#596 \| `conn.load_from_content()` \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-135 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 140 | \| D-006 \| `require constraint { ... }` \| Ch2 \| OpenSysML#597 \| `conn.load_from_content()` \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-136 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 141 | \| D-007 \| `assert satisfy R by P` \| Ch3 \| OpenSysML#598 \| `conn.load_from_content()` \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-137 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 142 | \| D-008 \| `allocate X to Y` \| Ch5 \| OpenSysML#599 \| `conn.load_from_content()` \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-138 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 143 | \| D-009 \| `flow X.port to Y.port` \| Ch5 \| OpenSysML#601 \| `conn.load_from_content()` \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-139 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 144 | -010 \| `state` + sub-states + transitions \| Ch7 \| OpenSysML#602 \| `conn.load_from_content()` \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-140 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 145 | 1 \| `attribute` with `default =` modifier \| Ch1 \| OpenSysML#603 \| `conn.load_from_content()` \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-141 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 146 |  \| `calc def` body (inputs + return expr) \| Ch3 \| OpenSysML#604 \| `conn.load_from_content()` \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-142 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 147 | \| `action def` body (params + sequencing) \| Ch4 \| OpenSysML#605 \| `conn.load_from_content()` \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-143 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 173 | \| `abstract part def` \| Ch1/nb01 \| toaster#9 / OpenSysML#595 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-144 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 174 | ute` (with `default =`) \| Ch1/nb02 \| toaster#16 / OpenSysML#603 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-145 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 177 |  + `require constraint` \| Ch2/nb01 \| toaster#11 / OpenSysML#597 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-146 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 178 | attribute :>>` override \| Ch2/nb02 \| toaster#10 / OpenSysML#596 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-147 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 179 | sage + `assert satisfy` \| Ch3/nb01 \| toaster#12 / OpenSysML#598 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-148 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 180 |  body (inputs + return) \| Ch3/nb02 \| toaster#17 / OpenSysML#604 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-149 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 181 |  `action def` with body \| Ch4/nb01 \| toaster#18 / OpenSysML#605 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-150 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 183 | \| `allocate` \| Ch5/nb02 \| toaster#13 / OpenSysML#599 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-151 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 184 | \| `flow` \| Ch5/nb03 \| toaster#14 / OpenSysML#601 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-152 | `.claude/skills/sysml-v2-toaster-model/SKILL.md` | 185 | b-states + transitions) \| Ch7/nb02 \| toaster#15 / OpenSysML#602 \| | KEEP-ID | (no change) Note: Protected token (package/skill name, repo or issue reference, URL, or env var). |
| B-153 | `.claude/skills/toaster-recipe/SKILL.md` | 55 (F) | import opensysml | KEEP-ID | (no change) Note: Inside a code fence. |
| B-154 | `.claude/skills/toaster-recipe/SKILL.md` | 58 (F) | conn = opensysml.connect(version="v0.9.0") | KEEP-ID | (no change) Note: Inside a code fence. |
| B-155 | `.claude/skills/toaster-recipe/SKILL.md` | 60 (F) | abstract modifier not yet supported — toaster#9 / OpenSysML#595 | KEEP-ID | (no change) Note: Inside a code fence. |
| B-156 | `.claude/skills/toaster-recipe/SKILL.md` | 87 (F) | fault = modifier not yet supported — toaster#16 / OpenSysML#603 | KEEP-ID | (no change) Note: Inside a code fence. |
| B-157 | `.claude/skills/tutorial-glossary/SKILL.md` | 43 | Implementations (OpenSysML, sysml-toolkit) are toolchain, not sources. | RUNTIME | Implementations (the OpenSysML runtime, sysml-toolkit, the Pilot Implementation) are toolchain, not sources. Note: Parent and child listed in parallel under the umbrella reading; mirrors AGENTS.md 1.2. |
| B-158 | `.claude/skills/tutorial-style-guide/SKILL.md` | 86 | add a comment citing the toaster issue + OpenSysML issue + spec section | RUNTIME | add a comment citing the toaster issue + the tracker issue of the component at fault (the runtime's `Open-MBEE/OpenSysML#NNN` or `Open-MBEE/sysml-toolkit#N`) + spec section Note: Convention: the runtime's tracker is `Open-MBEE/OpenSysML#NNN`; "OpenSysML issue" now ambiguous. Line 89 (in a code fence) is KEEP-ID. |
| B-159 | `.claude/skills/tutorial-style-guide/SKILL.md` | 89 (F) | abstract modifier not yet supported — toaster#9 / OpenSysML#595 | KEEP-ID | (no change) Note: Inside a code fence. |
| B-160 | `.claude/skills/tutorial-supporting-pages/SKILL.md` | 15 | \| `docs/references.md` \| Citations: Brian Douglas video, Hawkins 2011, opensysml, mystmd \| | KEEP-STACK | \| `docs/references.md` \| Citations: Brian Douglas video, Hawkins 2011, OpenSysML (the stack definition and links), mystmd \| Note: Lower-case "opensysml" here names the references section, which per the plan becomes the stack definition (OT-4). Optional capitalisation/clarification. |
