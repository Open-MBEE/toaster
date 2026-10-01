---
name: skill-editor
description: Pre-edit gate, blast-radius assessment, minimal-change rule, post-edit check, and revert protocol for editing .claude/skills/ files.
---

# Skill Editor

Load this skill before editing any `.claude/skills/**/*.md` file.

## Step 1 — Pre-edit gate

Before touching any file:
- Identify which archetypes load the target skill and which WPs are currently in-flight using those archetypes.
- If a WP is mid-loop (developer has delivered; reviewer has not finished): defer until the loop closes.
- Write the DL log entry **first**, status `PENDING`, with the intended change in one sentence and the current text of the section being changed captured verbatim (revert record).

**Z-directed alignment pass.** When Z has directed an alignment pass, the DL entry that records Z's direction (with the plan it follows) satisfies the escalate-to-Z gates in Step 2 for the edits it names. The pre-edit DL entry is still written first, and the revert record may point to the commit that precedes the first edit (`git show <commit>:<path>`) instead of pasting the text. This is a one-off Z override, not a change to file authority, and it ends with the pass.

**Generated regions are exempt from this gate.** Text between `<!-- gloss:ID -->` and `<!-- /gloss -->` markers is generated from the glossary by `uv run python -m glossary render`. It is changed only by changing the glossary, which is itself logged and confirmed by Z. Never edit it by hand.

## Step 2 — Blast-radius assessment

| Question | If yes |
|---|---|
| Does this change affect more than one archetype's primary skill? | Escalate to Z |
| Does this remove a prohibition or "must never do" clause? | Escalate to Z |
| Does this add a capability not in the original WP-0 design? | Escalate to Z |
| Does this change `sysml-v2-toaster-model`'s construct list? | Escalate to Z |
| Does this affect a learning outcome? | Escalate to Z |

## Step 3 — Minimal change rule

- Change only what is incorrect or ambiguous.
- Do not restructure sections, rename headings, or reorder rules.
- If more than ~20% of the skill's content would change: stop and escalate.

## Step 4 — Post-edit check

- Re-read the modified section and the two adjacent sections.
- Confirm no adjacent rule is accidentally weakened or contradicted.
- Confirm no skill you touched contradicts AGENTS.md Part 1 or a confirmed glossary definition (`uv run python -m glossary check`; search the skill for the terms you changed). When a skill and Part 1 disagree, Part 1 governs, and the skill is the thing to fix.
- Update the DL entry to `COMPLETE` with a one-sentence summary of what changed and why.

## Revert protocol

If the change makes things worse (CANT_TELL or FAIL citing the modified guidance, or a developer reports contradiction):
- Read the DL entry's captured verbatim section.
- Restore it exactly.
- Update the DL entry: `Path: Reverted on [date], reason: [one sentence]`.

## What ACE can fix unilaterally

- Incorrect API shape or return type in `opensysml-api`
- Missing example for a construct already in scope
- Tighter prohibition derived from an observed error pattern
- Clarification of an ambiguous rule that a developer demonstrably misread
- "Common mistake" note where a CANT_TELL or FAIL reveals a recurring pattern

## What ACE must never do

- Edit skills without first writing the DL pre-edit entry
- Make a change mid-loop
- Make more than one logical change per session
- Remove or weaken an existing prohibition without Z's explicit direction
