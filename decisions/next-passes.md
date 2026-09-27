# What comes after Pass 1: handoff record

This file declares what follows Pass 1 and what Pass 1 leaves as input. It records; it does not design. Z decides each item. Pass 1 (DL-015) produced: AGENTS.md Part 1 Foundations (role-agnostic) with the earlier roster kept as legacy Part 2; the glossary (`glossary/`); the skills `architecture-layers`, `opensysml-query`, `tutorial-glossary`; an updated `ace-protocol`, `skill-editor` and `opensysml-api`; the tested `src/toaster/query.py`; probe, gap and dry-run records.

## 1. The passes, in order (Z)

| Pass | Scope | Entry | Exit |
|---|---|---|---|
| 1 (this one) | Foundations, glossary, ACE definition, layer and query skills, handoff | Z's plan | DL-015 COMPLETE; Z has skimmed the ACE key and confirmed the glossary |
| 2. The agent system — **closed, see `decisions/pass2-close.md`** | Roles, responsibilities, protocols, skills, expertise, authority matrix; the orchestrator, subagents and their model assignments | Pass 1 exit | The roster and authority matrix are consistent with the Foundations; every role skill cites glossary ids; each role has a pinned model and a cold-start test |
| 3. Evaluation workflows | Simulated learners, layer audit, Tall-seam effectiveness, glossary `check` and skill-snippet tests in CI, prose lint against confirmed definitions | Pass 2 roster | Evaluations run on the pinned models and produce reports the ACE can triage |
| 4. Didactic content | Track B audit and rebuild of chapters and models, the recipe, SA-3 and SA-8 collisions, docs stubs, Ch9 and Ch10, staged conformance placement | Pass 3 | A chapter set that follows Part 1, with the staged model built explicit and implicit |

Each pass starts from the previous pass's output state.

## 2. Operating model the rebuild must implement (Z)

- **Subagents are independent actors.** Each runs in a *cold session* primed with its own identity and responsibilities, so no context bleeds between them. It works in a *private git worktree* and commits; the orchestrator integrates the commits. Create worktrees explicitly (`git worktree add <path> HEAD`); the harness's default isolation started from an older commit in the Pass 1 cold-start test (`decisions/cold-start.md`).
- **Accountability layering.** Z is the chief engineer. The **ACE** is accountable to Z for *triage*. The **orchestrator** is accountable for coordination. **Subagents** are accountable for narrowly scoped tasks.
- **Orchestrator:** very technical and project-manager oriented, mostly administrative. It coordinates subagent labor and makes no judgment calls. It escalates to the ACE whenever judgment is required, and routes subagents' local questions to the relevant parties, including other subagents, so information flows laterally as well as top-down.
- **Subagents:** do narrowly scoped work assigned by the orchestrator, deliver outputs to it, surface local questions to it, and are encouraged to escalate when unsure.
- **ACE (defined in Pass 1):** the triage layer that keeps Z from being spammed. Each triage ends in "rules and logs" or "escalates to Z and logs", with a concise request in Z's idiom. It rules only where Z's frameworks, principles and heuristics (`.claude/skills/ace-protocol/z-principles.md`) determine the answer, showing the reasoning; `z-model.md` holds the statements they were drawn from, as provenance. Only Z confirms glossary definitions, approves departures from a canonical source, and reopens an SA rule.
- **Escalation chain:** subagent to orchestrator to ACE to Z. Part 2 section 4 covers only the last two links.
- **Z preserves their own judgment over substantive decisions.** The ACE's rulings are recommendations Z can skim, and definitions the ACE or an agent edits are shown to Z (DL-017). Do not design any role that decides substantive questions on Z's behalf where the frameworks and principles do not determine the answer.

## 3. Model assignments (Z; per-role table is a Pass 2 decision)

Model choice is part of how a role is parameterized and must make sense for the role. Every role definition pins `model` and `effort`; an unpinned subagent silently inherits its parent's model. **Only the ACE runs on Fable 5.1** (`claude-fable-5-1`); other roles are mostly Sonnet 5 or Opus 5.5 depending on the role, and Haiku 4.5 can serve the novice learner (it should not have more capability than the learner it stands for). A role is tested on the model it will run on. **Authors and reviewers run on different models** (no same-model review, Z 2026-09-26): the reviewer role (Opus 5.5) reviews builders (Sonnet 5), and the orchestrator confirms the models differ before a task leaves `in-review`. Task states, `blocked` criteria and `wont-do` are in `decisions/task-states.md`. The Pass 1 cold-start test used Haiku 4.5, Sonnet 5 and Opus 5.5 as stand-ins and all passed. Today the repo has no `.claude/agents/` files and no assignments. The file pattern to reuse is in Z's `civic-ai-tools` repo (`.claude/agents/impl.md`, `cold-read.md`, an orchestrator session spawning implementers).

## 3b. Working rules learned in Pass 1

Use query tools and direct lookups (glossary CLI, `model.query`, known file ranges) before grep or large loads; no co-author trailers in commits; record probes and corrections in the repo the same session (`decisions/probes.md`). These are also in the project memory and should become part of the role skills.

## 4. Audit findings that are the rebuild's inputs

**Authority and ownership gaps in the legacy roster (Part 2)**
- Chapter `index.md` and `conclusion.md` have no owner.
- Python `ReviewRecord` cells have no owner, and SysML fragments live in Python string cells, so the "SysML source cells versus Python code cells" split no longer holds.
- `DEFERRED.md` has no owner; `figures/` is missing and the matrix names a wrong `skills/` path.
- Part 2 has A8 unable to edit AGENTS.md and only A2 able to, while Part 1 makes alignment changes Z-initiated; the matrix also does not cover `glossary/`, `decisions/probes.md` or the new skills. A contributor outside the roster cannot tell whom to hand glossary proposals to (AGENTS.md 1.11 now says: through the orchestrator or the report).
- Part 2 mentions `DEVELOPMENT_PLAN.md`, which does not exist, and "8 modules".
- The orchestrator is "read only, never edits files", which conflicts with integrating commits (parked decision).
- Roles are keyed to artifact types (chapters, models, tests); the Foundations are keyed to layers and to the construct, analyze and judge loop.

**Skills not yet aligned with Part 1 (each carries the earlier framing)**: `toaster-recipe` (requires a named per-notebook "Tall seam" cell, which contradicts the rule that learner content never names it), `sysml-v2-toaster-model`, `tutorial-style-guide`, `sysml-diagrams` (its `references/environment.md` is missing and a Mermaid recipe contradicts SA-9), `orchestrator-protocol`, `user-testing` (personas for the new layers), `toaster-review-protocol`, `myst-publication`, `tutorial-supporting-pages`.

**Role-agnostic duty catalog** (duties, not roles, so the roster can be repartitioned): construct the model (explicit and implicit); query and analyze it; simulate; model check; judge and record evidence (Hawkins fields); layer-audit; steward the glossary; track spec gaps and issues; author prose; evaluate as a learner; review technically and didactically; curate and verify the implicit model parts; select, justify, render and check diagrams as views of the model; apply and report staged conformance checks; integrate commits and coordinate.

## 5. Diagram inventory (corrected 2026-09-26)

- **In force by decision:** Python-generated DOT from `model.query()` (`src/toaster/render.py::model_to_dot`, DL-002) rendered with Graphviz; SysMLD port-level interconnection; Matplotlib for quantitative figures (DL-001 removed Java from the required tools).
- **Described in `sysml-diagrams` but not in force:** Pilot Implementation `TREE` and `STATE` views (Java, the pilot JAR); OpenSysML to PlantUML action flow (no render CLI in v0.9.0); a Mermaid sequence recipe that SA-9 bans.
- **Available in sysml-toolkit v0.9.1, not in the skill:** `sysmlv2 viz` and `Session.to_plantuml` (seven views, `--color`, metadata stereotypes, `--show-inherited`, `--link-template`, cross-file name resolution), verified locally (`decisions/probes.md`). **Summary mode is not in the CLI or Python** (D-018); do not plan implicit-part collapse on the toolkit.
- **Provenance encoding candidates for implicit versus explicit parts:** distinct named packages (queryable, lost if not designed in), or a user-defined metadata marker (survives assembly; metadata is JSON-only to `model.query`).
- **Inputs, not fixed:** which renderers to standardize on, per-diagram-type guidance, and the `sysml-diagrams` contradictions.

## 6. Parked decisions (Z)

- **SA-2** (full stage model per chapter): Z ruled the assembled model made legible through diagrams satisfies it; the SA-2 wording needs updating for explicit and implicit construction.
- **SA-3** (energy model `Q = eta P t`) and **SA-8** (one construct per notebook) will collide with the content pass.
- **SA-7** versus the Ch10 sign-off framing (no "accepted" dispositions).
- **The Tall seam**: the recipe requirement contradicts the rule; the recipe rewrite belongs to Pass 4 and evaluation of the seam to Pass 3.
- **`docs/references.md`** lacks SEBoK, Åström and Murray, Sutton and Barto (and says a 6-part Douglas series while the playlist lists 5, to verify). **`docs/glossary.md`** is a stub with a wrong H1; the new glossary will regenerate it (`render` support is planned, not built).
- **Orchestrator integration authority**; **ownership of implicit versus explicit constructions and of the diagrams that make them legible**; **A10's remit** (Ch5 and Ch6 authority).
- **DL-204 (Z ruled A, 2026-09-26):** learners meet each kind of emergence where its value is first obtained: simple at the roll-up (Ch5/6), weak at the first simulation of a functional intent (Ch7), strong at sign-off (Ch10); one sentence each, no separate section. Chapter placement is finalized in Pass 4.
- **Where each staged conformance check first applies** (for example port types), and the wording that reports it "open" (Z-27).
- **Douglas timestamp** for the tongs-and-flamethrower story is unverified.
- **Backup branch** `backup/pass1-before-trailer-strip` (local; holds the pre-rewrite commits) awaits Z's word to delete.
- **Audit backlog:** the Ch1 to Ch5 audits are consolidated in `decisions/pass4-backlog.md` (eleven themes; Ch6 to Ch10 not yet audited). ACE rulings DL-030 to DL-039 constrain the re-derivation.
- **Pass 2 chain runs 001 to 006** (`decisions/pass2-run-00N.md`) established: roles (`orchestrator`, `layer-auditor`, `builder`, `reviewer`, `ace`), task states, the merge gate and push-back, and independent review on a different model. Open follow-ups from run 004 are listed there.
- **Filing the gap issues** (`decisions/gap-issue-drafts.md`) awaits Z's review; nothing is filed.
- **Definitions edited at Z's direction:** mechanism approved as written by Z (2026-09-26). MoE and MoP: Z asked for a clearer, SEBoK-compatible, less overloaded wording that makes the measure measurable (a unit and a means of collecting data); the redraft (toast evenness for MoE, power efficiency for MoP) was applied on Z's answer and is recorded in DL-017.

## 7. Content pass (Pass 4) inputs, as candidates the audit will confirm or drop

Start with an audit, not an edit: run the `architecture-layers` per-layer checklist on every chapter's elements and record each one's layer under the confirmed definitions; then decide what to relabel, split, move or add.
1. Relabel Ch1, Ch4, Ch5, Ch6 prose to the aligned vocabulary (OQ-1, the def/usage forward reference, and OQ-3, the "inspired by" hedge, remain; OQ-2 is resolved by the definitions).
2. Restate `ApplyHeat` with flows and an energy-balance inequality; move `efficiency` out as a MoP of the mechanism; replace settable performance attributes such as `cycleTime` with prescribed parameters plus derived results, so the satisfy check tests emergent behavior against intent.
3. Show function, logical component, concrete part with `perform action x : ActionDef`, ports and interfaces, named `allocate`, and abstract-to-concrete specialization (Ch5).
4. Define MoE, MoP and TPM with the derivation chain explicit, and state each MoE/MoP split with its justification (the toast timing case is a candidate narrative example, Z-26).
5. Make Ch6's stopping judgment test the leaf criterion (concrete, interfaced, verified).
6. Restructure for explicit and implicit construction: implicit parts as Python modules with a declared dependency order yielding SysML source; per-chapter explicit increments and a stage manifest; extend `scripts/check_construction.py` to assemble and verify each stage; choose the provenance encoding and the diagrams that make implicit parts legible.
7. Rename Ch3's MoE/MoP-labeled files and update `myst.yml` and `scripts/check_construction.py`; fill in Ch9 and Ch10 and the missing snapshot models.
8. Stage the project conformance checks (port types, flows accounted, coverage) with negative controls and "open" reporting.

## 8. What Pass 1 did not test

The ACE on a question Z has said nothing about beyond DL-204, and on a routed escalation from a real subagent; roles other than the ACE; the evaluation workflows; any chapter content.
