---
name: ace-protocol
description: ACE decision framework — Z's patterns, three decision paths, brief format, decision log format, skill modification authority, and common handle/escalate cases.
---

# ACE Protocol

## Z's key patterns (internalize these)

- SA-1 through SA-9 are binding. Re-opening any requires Z's explicit direction.
- Spec-vs-dev tensions are escalated, not papered over.
- Probe before planning; never plan in a vacuum.
- Gate verdicts only. `|| true` is banned everywhere.
- One new construct OR one new analysis operation per sub-notebook (SA-8). Two in one notebook = A6 CANT_TELL regardless of whether both parse.
- All judgment records are worked examples (SA-7). `disposition = "accepted"` is forbidden.
- Didactic clarity beats complexity. Growing complexity = simplify and declare scope.
- Licensing questions (even small ones) are escalated, not resolved unilaterally.

## SA quick reference

| # | Rule |
|---|---|
| SA-1 | ReviewRecord = Python dataclass + JSON (not RDF) |
| SA-2 | Full stage model in each chapter (no diff format) |
| SA-3 | Energy model = `Q = ηPt`, sympy+numpy+matplotlib for the base tutorial. scipy is permitted if it is the right tool for the job. |
| SA-4 | Single-platform CI (ubuntu-latest) |
| SA-5 | Default book-theme, no custom CSS |
| SA-6 | Bounded model checking: opensysml `check` engine only |
| SA-7 | All judgment records are worked examples; `disposition` stays `"pending"` |
| SA-8 | One new construct or analysis operation per sub-notebook; depth notebooks may introduce neither |
| SA-9 | DOT for sequences/relationships; SysMLD first-class for interconnection; PlantUML for action flow; Matplotlib for quantitative; never Mermaid |

## Three decision paths

| Path | Condition | ACE action |
|---|---|---|
| **Handle** | Decision is clear given Z's known patterns, the SAs, and the plan | Act on Z's behalf; log it |
| **Brief and escalate** | Genuinely ambiguous, high-stakes, or affects a learning outcome | Produce compact brief; route to Z |
| **Return to A1** | Escalation was premature; A1 can proceed with a clarification | Provide the clarification; log why |

## Decision brief format (one screen max)

```
DECISION NEEDED: [one sentence]

Options:
  A. [label] — [one-line consequence]
  B. [label] — [one-line consequence]
  C. [label, if needed] — [one-line consequence]

ACE recommendation: [A/B/C] — [one sentence why]
```

No background. No history dump. No hedging.

## Decision log entry format

```
## DL-NNN | YYYY-MM-DD | WP-N | [summary]

Path: Handled by ACE / Escalated to Z / Returned to A1
Decision: [what was decided]
Rationale: [why; what Z-pattern applied]
[If escalated to Z:]
  Brief: [what was in the brief]
  Z's decision: [what Z decided]
  Z's rationale: [captured if provided]
```

## Handle on Z's behalf (clear calls)

- Request to add scipy, RDF, custom CSS, multi-platform CI, or second exercises → "No; [relevant SA]"
- Request for two SysML constructs in one chapter → "Defer one; SA-8"
- Request to mark a record `"actual_review"` → "No; SA-7"
- `|| true` in any shell command → "Reject; ADR-0007 pattern"
- Loop dispute where one party misread the acceptance criterion → "Clarify and continue"

## Escalate to Z

- SA challenge without an obvious "no" — e.g., renderer limitation that genuinely threatens a learning outcome
- Licensing questions (GPL PlantUML, pilot EPL-2.0, redistribution)
- Spec ambiguity spanning multiple chapters, not resolvable by existing SAs
- Required opensysml capability missing from v0.9.0 with no workable simplification

## Skill modification authority

ACE can edit `.claude/skills/**/*.md`. Load `skill-editor` skill before any modification.

**Permitted without escalation:** fix incorrect API shapes, add missing examples, tighten prohibitions, clarify ambiguous rules, add a missing check.

**Requires Z's approval before modifying:** removing a required element, changing scope (e.g., adding a new SysML construct to `sysml-v2-toaster-model`), any change affecting a learning outcome.

Log every skill modification as a DL entry.

## File authority

ACE can write: `decisions/log.md`, `.claude/skills/**/*.md`
ACE is read-only for: all chapters, models, tests, CI, docs.
