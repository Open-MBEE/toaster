# Pass 2, run 001: first end-to-end chain (2026-09-26)

Purpose: exercise subagent, orchestrator, ACE, Z on one real, low-risk task before designing more roles. Roles: `.claude/agents/orchestrator.md`, `layer-auditor.md`, `ace.md`, each with a pinned model. Contract: PASS2-001 (layer audit of `models/ch01-cumulative.sysml`).

## What ran

1. **Orchestrator** (this session, following `orchestrator.md`) created the worktree by hand from HEAD (`git worktree add ... -b audit/ch01`), wrote the contract (template `decisions/work-contract-template.md`), and launched the auditor cold on **Opus 5.5**, model pinned in the launch.
2. **Layer auditor** verified the premises (three did not hold), audited every element, wrote `decisions/audits/ch01-layer-audit.md`, and committed one file with a plain message. It did not fix anything and left contested calls as open questions with a recommended default.
3. **Orchestrator** checked the diff against the blast zone (one file, as contracted), integrated the commit (`171c4ef`), removed the worktree, and routed the open questions to the ACE.
4. **ACE** (**Fable 5.1**, pinned) ruled all five items (F-1 confirmed; OQ-1 narrowed; OQ-2 to OQ-4 confirmed the auditor's defaults; OQ-5 no action) and returned log-entry text. The orchestrator numbered and committed it as DL-018 to DL-022.
5. **Z**: one item came back to Z after the run. Z reviewed the logs and asked that ACE rulings rest on principles, not quotations; DL-019 (OQ-1) did not survive that test, was escalated, and Z ruled that the system-of-interest is the subject the layers describe (framework F7). DL-018 to DL-022 were rewritten in the new log format.

## Findings about the chain itself

- **It works.** The blast zone held, premises were checked and reported, the report separated findings from open questions, and the ACE's rulings each cite a numbered Z-statement.
- **The ACE never escalated in this run.** That is right only if each ruling truly rests on a Z-statement. DL-019 (OQ-1: is `ToastingSystem` functional or logical?) rests partly on the ACE's inference from Z-8 that a part def with no values reads as a design-space type. Z has not said that directly. It is flagged for Z's skim, and if Z disagrees the ACE's habit of extending Z-statements by inference is the thing to tighten in `ace-protocol`.
- **Launch mechanics.** The custom roles were run through a general-purpose agent told to read its role file, with the model pinned in the launch. The role files' `model` frontmatter was therefore not exercised as such. Whether Claude Code honors it when a role is launched by name needs one direct test before the roster grows.
- **The orchestrator was this session's persona, not a launched `--agent orchestrator` session.** The role file describes what it did, but the pinned model (Sonnet 5) was not what this session ran on.
- **Auditor's premises.** The contract's premises were guesses about Chapter 1; three did not hold, and the auditor said so. That is the behavior wanted.
- **Cost:** the auditor and ACE runs each used about 100k subagent tokens and 2 to 3 minutes.

## What the audit found (for Pass 4)

F-1 `cycleTime` is an emergent result entered as a choice (confirmed). F-2 `Heater` specializes no logical def and is unused. F-3 the whole system does not specialize the purpose type its subsystems specialize. F-4 chapter text disagrees with the model and itself ("physical architecture layer" versus "implementation-agnostic"; `Real` versus ISQ types; a stale abstract-modifier comment). These are recorded as inputs; nothing was edited.
