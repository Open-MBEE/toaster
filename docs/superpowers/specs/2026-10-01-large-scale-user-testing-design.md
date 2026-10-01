# Design: large-scale user testing — the persona × modality grid, and an interviewing interpretive layer

**Status:** draft, written at Z's direction; not yet reviewed
**Author:** session design work with Z, 2026-10-01
**Related:** `.claude/skills/user-testing/SKILL.md`, `.claude/skills/ace-protocol/SKILL.md`, `.claude/agents/simulated-learner.md`, `.claude/agents/ace.md`, `.claude/agents/orchestrator.md`, decisions/log.md DL-075 through DL-083 (the existing single-modality user-testing battery this design extends, not replaces)

## Why this exists

Tonight's own ad hoc testing (browser-rendered book, README accuracy, one exercise notebook run by hand) found real bugs in about twenty minutes of directed looking — three rendering bugs, three documentation inaccuracies, a missing LICENSE, an incomplete CI pipeline, and an exercise-scaffolding inconsistency that would confuse a first-time learner. All of that was one session, one perspective, testing mostly one modality (the rendered book) end to end and two others (README, one exercise) only glancingly. Z's ask is to make that kind of finding *systematic* rather than incidental: before this tutorial goes in front of real outside users across GitHub, GitHub Pages, and a local clone, run the same kind of close reading **deliberately, at scale, across who's reading and where they're reading it**, and turn whatever it finds into a short, prioritized, actionable list — not a pile of forty raw reports Z has to read personally.

This repo already has most of the machinery this needs. `user-testing` already defines three learner personas with pinned models matched to their claimed capability, a fixed execution checklist, and a fixed report format. `ace-protocol` already defines a triage layer — the ACE — whose entire job is "resolve only what truly needs Z and nothing that wastes Z's time," ruling where principles determine the answer and escalating a concise, Z-idiom brief otherwise. What's missing is two things: **the grid** (today's `user-testing` tests exactly one modality — a learner reading chapter notebooks from a local checkout — and has no persona-specific coverage of the other two places a real user actually encounters this project), and **the interview step** (today's ACE synthesis reads finished, static reports; it cannot go back and ask a specific sub-agent a clarifying follow-up before ruling, the way a human running a usability study would ask a participant "what did you expect to happen there?").

## The grid

### Personas (unchanged from `user-testing`, reused as-is)

| Persona | Model | Stands in for |
|---|---|---|
| **Novice** | Haiku 4.5 | A reader with no prior SysML/MBSE background, Python-literate |
| **SE Practitioner** | Sonnet 5 | A systems engineer with no SysML v2 background, judging whether modeling choices are defensible |
| **Returning Learner** | Sonnet 5 | Someone who already completed earlier chapters, now starting fresh content |

No new persona is introduced. Z's own model-matching rule (`decisions/next-passes.md` §3, carried into `user-testing`: a simulated novice should not have more capability than the learner it stands for) applies identically here.

### Modalities (new — this is what the grid actually adds)

| Modality | What a real user does | What existing coverage there is today |
|---|---|---|
| **M1 — GitHub repo** | Lands on `github.com/Open-MBEE/toaster` from a search result, a link, or a colleague's recommendation. Reads the README, skims the file tree, maybe checks "Releases" or "Issues," decides whether to clone it. | None. Tonight's README fixes were my own ad hoc read, not a persona-structured test. |
| **M2 — GitHub Pages (rendered book)** | Opens the deployed book in a browser, reads chapters, maybe searches, maybe switches to mobile or dark mode, never opens a terminal. | None structured; tonight's browser sweep was thorough but was me, not a persona, and found technical-rendering bugs more than "does this make sense" judgments. |
| **M3 — Local clone, reading the chapters** | Follows `docs/setup.md`, runs `uv sync --locked`, opens chapter notebooks in Jupyter, reads and re-runs cells. | This is what `user-testing` already covers end to end — reuse its existing checklist and report format for this modality unchanged. |
| **M4 — Local clone, doing an exercise** | Having read a chapter, opens the matching `exercises/ch{N}/exercise.ipynb`, tries to fill it in using only what the chapter taught. | None. `user-testing`'s own checklist explicitly scopes to chapter notebooks; exercises are excluded from CI and from today's testing battery by design. Tonight's own finding (Ch1's exercise fails gracefully, Ch8's crashes with an unexplained `AssertionError`) came from me running two exercises by hand, not from persona testing. |

### Which cells are worth running

Not every persona × modality cell carries equal signal, and running all twelve blindly would waste budget on cells where the persona dimension doesn't actually change what's found. Scope the first run to the cells below; treat the rest as available, not default.

| | M1: GitHub repo | M2: GitHub Pages | M3: Local, chapters | M4: Local, exercise |
|---|---|---|---|---|
| **Novice** | run | run | run (existing coverage, re-point at a fresh checkout) | run |
| **SE Practitioner** | — (low persona-differentiation for a README skim; skip unless M1 is re-run after major content changes) | run | run | run |
| **Returning Learner** | — (the persona's own definition, "starting this chapter fresh," doesn't map onto M1 at all) | run | run | run |

That's **nine cells**, not twelve — M1 gets one persona (Novice, the persona a README's clarity matters most for; a practitioner or returning learner reading a README is not meaningfully different from a novice reading one, so testing it three times would just burn budget for the same finding repeated). This keeps the first run inside this session's own stated default workflow-size guideline (medium, under ten agents) without the orchestrator needing to ask for an exception.

## Sandboxing

Every cell's sub-agent is dispatched the way this session's own builder/reviewer agents already were tonight: a cold session, no shared context with any other cell, given only its own work contract. The specific sandboxing mechanism differs by modality, because the modalities have genuinely different blast radii:

- **M3 and M4 (local clone)** need a **private git worktree** (`isolation: "worktree"` on the `Agent` tool call, the same mechanism tonight's fifteen builder contracts used) — a real, independent checkout, so a persona's experience reflects a genuinely fresh `git clone`, not an environment already polluted by whatever this session has been doing to the working directory. This also means M3/M4 agents can be dispatched **before** any fix from this testing round lands, to test the actual current released state, and then **again** after fixes land, as a regression check — the same before/after discipline this session used all night for its own retrofit work.
- **M2 (GitHub Pages)** needs the **built, served site**, not a worktree — either the already-running local `myst start --execute` preview this session has open (serving what's on the current branch) or, once Task 7 of the CI/CD plan produces a real built static export, that export served locally under the `/toaster` path. The sub-agent needs the Browser tools (`mcp__Claude_Browser__*`), not a worktree; its "sandbox" is that it gets its own fresh tab and no memory of any other cell's findings.
- **M1 (GitHub repo)** needs **only read access to the repository as a visitor would see it on GitHub itself** — either the live `github.com/Open-MBEE/toaster` page (if public visibility and the current state are what's being tested) or, more usefully for testing *this branch's own proposed changes before they're merged*, a rendered preview of this branch's README and file tree. A worktree isn't wrong here, just unnecessary; a read-only checkout of the branch under test is sufficient.

Every sub-agent, regardless of modality, is **named and kept addressable** after it reports — this is the one sandboxing requirement that's new relative to tonight's builder/reviewer pattern, and it's what makes the interview step (below) possible at all. Launch every cell's agent with a stable, descriptive name (not left to auto-naming) so the interpretive layer can address it by name in `SendMessage` later without having to hunt through `ListAgents` output to recover an opaque ID.

## The record: what each cell actually produces

Each sub-agent produces two things, not one: the existing narrative report `user-testing` already specifies (unchanged format: EXECUTION RESULTS / NARRATIVE OBSERVATIONS / STRUCTURAL CHECKS / OVERALL, extended per modality below), and a **structured findings list** the interpretive layer can process without re-reading full prose for every cell.

### Structured findings list (new)

Every finding a sub-agent reports — not just blocking ones — gets one row:

```
{
  "cell": "M2-novice",
  "finding_id": "M2-novice-01",
  "severity": "blocking | friction | confusing | cosmetic | positive",
  "location": "exact URL, file path, or notebook cell reference",
  "quote": "the exact text or exact behavior observed, never a paraphrase",
  "expected": "what the persona expected to happen or find, in one sentence",
  "actual": "what actually happened, in one sentence"
}
```

This is a deliberate narrowing of `user-testing`'s existing "blocking / minor / cosmetic" triage (which is the *synthesizer's* vocabulary, applied after the fact) down to what a reporting sub-agent can say about its own experience without having to judge severity itself — `severity` here is the sub-agent's own first-pass guess, explicitly re-judged by the interpretive layer, not binding. `positive` is included deliberately: a synthesis that only sees problems can't tell "this chapter has no issues" from "no one tested this chapter," and this session's own feedback memory (`[[feedback-durable-learnings]]`-style discipline, record from success and failure both) applies here the same as it does to any other kind of review.

### Modality-specific additions to the existing report format

- **M1 (GitHub repo):** add a "First five minutes" narrative section — what did the persona read, in what order, and at what point (if any) did they decide to clone it or give up. This is the one modality where *sequence* (what's read first) matters as much as content accuracy.
- **M2 (GitHub Pages):** add the same execution-results table `user-testing` already specifies for chapter notebooks (model.ok, bad.ok, printed output), since the rendered book's code cells carry real executed output the persona should be able to verify against what the prose claims — a persona finding the printed `Validation errors: []` and the prose's claim that it's clean disagree is exactly the kind of finding this grid exists to catch.
- **M3 (local, chapters):** unchanged from `user-testing` today.
- **M4 (exercises):** add an explicit **first-run-unmodified** execution result (run the exercise exactly as cloned, before attempting to fill in anything) separately from the persona's own attempt at filling it in — tonight's own Ch1-vs-Ch8 scaffolding-inconsistency finding depended on exactly this distinction (what happens before any input, not just what happens after a good-faith attempt), and a report that only covers the attempted fill-in would miss that class of finding entirely.

## The interpretive layer

**This is the existing ACE, not a new role.** `ace-protocol`'s own stated job — triage layer, rules where Z's principles determine the answer, escalates a concise brief otherwise, logs either way — is already the right shape for "consume the records and synthesize findings toward a concrete recommendation." What's added is a new capability the ACE does not have today: **the interview step**, inserted between "read every cell's structured findings" and "triage and rule or escalate."

### Synthesis protocol (extends `user-testing`'s existing ACE synthesis protocol, modality-grid version)

1. **Collect.** Read every cell's structured findings list and narrative report. Do not read full narrative prose for every row before triage — use the structured list as the index, and open full prose only for rows that need it (this keeps the ACE's own context budget bounded even at nine cells).
2. **Cluster.** Group findings that are really the same underlying issue seen from different cells — tonight's own README inaccuracies, for instance, would plausibly surface independently from an M1 Novice *and* an M3 Returning Learner re-reading setup instructions; these are one finding with two pieces of corroborating evidence, not two findings.
3. **Interview — the new step.** For any finding where the structured record is ambiguous, where severity is unclear, or where two cells' findings appear to conflict, the ACE sends a targeted follow-up message to the specific sub-agent that reported it, by name (`SendMessage` to the cell's own agent name, established at dispatch per the Sandboxing section above — this works because `SendMessage` "resumes it from its transcript" even for an agent that has already completed and reported). Ask one narrow, concrete question per message — "quote the exact sentence that confused you," "did you actually click that link, or assume it was broken," "what would you have expected to see instead" — the same discipline this session's own reviewer agents already used when probing a builder's self-report rather than trusting it at face value. This is not optional polish: a structured finding with `severity: "confusing"` and no interview is a guess about how bad it is; the same finding after one targeted follow-up is evidence.
4. **Triage**, using `user-testing`'s existing blocking/friction/confusing/cosmetic classification, now informed by interview answers where they were needed: for each cluster, classify severity, decide Rule or Escalate exactly as `ace-protocol` already specifies (can the frameworks and principles in `z-principles.md` determine what to do about this, or does it genuinely need Z's own judgment — a design question, a scope question, a taste question the ACE cannot resolve from principles alone).
5. **Synthesize a recommendation, not a report.** The deliverable is not "here are forty findings" — it is a short, prioritized list: what's already fixed (with evidence), what the ACE is ruling on directly and fixing or dispatching a builder contract for, what's being escalated to Z with a concise Z-idiom brief per finding, and what's explicitly out of scope for this round (recorded, not dropped — the same "known gaps, not silently fixed" discipline DL-084 already modeled tonight). Log it as a DL entry the same shape as `ace-protocol` already specifies, with one addition: a `Grid coverage:` line naming exactly which cells ran, so a future reader knows what this synthesis did and did not see.

### Why this stays inside the ACE's existing authority, not a new one

`ace-protocol`'s file-authority section already scopes the ACE to `decisions/log.md` and `.claude/skills/**/*.md`, read-only everywhere else. Nothing in this design asks the ACE to write chapter content, models, or CI config directly — ruled findings that need a content fix still go through the normal pipeline (`ace-protocol`: "the ACE does not edit repository files... the orchestrator dispatches a builder/author-role work contract to make the change and a reviewer to confirm it"). The interview step changes *what evidence the ACE has before it rules*, not *what the ACE is allowed to do with a ruling*.

## What this design does not do

- It does not replace `user-testing`'s existing single-modality (M3-only) battery or its persona definitions — it extends both.
- It does not propose running all nine cells on every future change; it scopes *this* first run to nine cells and leaves the full twelve-cell grid, plus a repeat-after-fixes regression pass, as a documented option, not a standing requirement.
- It does not change `ace-protocol`'s accountability model, file authority, or rule/escalate test — only its synthesis protocol gains one new step.
- It does not specify a UI or dashboard for the interview transcripts; they live in each sub-agent's own transcript, addressable by name, the same as every other agent this session has dispatched tonight.

## Open items for the implementation plan, not resolved by this design

- Exact dispatch order and parallelism: M3/M4 cells share a blast zone only with each other (separate worktrees avoid file conflicts entirely, unlike tonight's Hawkins-plan builder contracts, which shared cumulative-model files) — likely safe to run fully parallel, but should be confirmed rather than assumed.
- Whether M2's sub-agents test against the *current dev-server preview* (fast, available now) or wait for the CI/CD plan's real static build under `/toaster` (more representative of the actual deployed experience, but blocked on that plan's own Task 2/6) — a sequencing decision between this design and the CI/CD plan, not resolved here.
- The exact DL-entry numbering and whether a grid-testing battery gets its own `decisions/user-testing-grid/` directory (mirroring the existing `decisions/user-testing/` convention) or reuses it with a modality suffix on each filename.
- Whether `simulated-learner`'s own agent definition needs a modality parameter added to its work contract (currently only `(persona, chapter)`), or whether modality is better expressed as an entirely separate contract field the orchestrator fills in per cell.
