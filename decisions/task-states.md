# Task states (coordination state machine)

A small state machine the orchestrator uses to track work and to phrase escalations to the ACE. The same vocabulary applies to conformance checks (`src/toaster/conformance.py`): `open`, `passed`, `failed`, `blocked`, `wont-do`.

## States

| State | Meaning | Required fields |
|---|---|---|
| `ready` | Contract written, worktree not yet made or work not started | contract id |
| `in-progress` | A subagent is working | role, model, worktree, branch |
| `in-review` | Author reported; an independent reviewer (a different model than the author) is checking | author model, reviewer role and model |
| `escalated` | Waiting on a judgment (ACE, or Z through the ACE) | question type, question, evidence, recommended default |
| `blocked` | Cannot proceed until a stated condition holds | `blocked_on`, `unblock_when`, `owner` |
| `done` | Acceptance checks pass, review passed, integrated | commit, checks run |
| `wont-do` | Dropped because something changed and it is no longer needed | reason, the change that removed the need, who ruled |

## Transitions

| From | To | Who | Condition |
|---|---|---|---|
| ready | in-progress | orchestrator | worktree created, model pinned, contract passed to a cold subagent |
| in-progress | in-review | orchestrator | author's report received, blast zone checked |
| in-review | done | orchestrator | reviewer passes, acceptance checks re-run by the orchestrator, commit integrated |
| in-review | in-progress | orchestrator | reviewer or checks found a defect (a new contract or a revision of the existing one) |
| any | escalated | orchestrator | a judgment is needed (see escalation language) |
| escalated | (previous state) | orchestrator | ACE ruled, or Z decided through the ACE |
| any | blocked | orchestrator | a condition outside this task must hold first |
| blocked | (previous state) | orchestrator | the `unblock_when` criterion is met and observed |
| ready, in-progress, blocked | wont-do | orchestrator proposes, ACE rules | a change made the task unnecessary (below) |

## Blocked: required criteria

A task is not `blocked` on "waiting". It records `blocked_on` (a task id, an answer from a named party, or an external event), `unblock_when` (a condition someone can observe or run, for example "OpenSysML issue closed and the probe script passes" or "Z answers DL-nnn"), and `owner` (who watches for it). Each state change out of `blocked` cites the observation that met the criterion. A blocked task with no checkable `unblock_when` is a defect in the record.

## Wont-do: required criteria

`wont-do` is a scope decision, not a failure. It records the reason, the specific change that removed the need (a decision, a merged commit, a tool fix), and who ruled. The orchestrator may propose it with evidence, and the ACE rules (the frameworks decide whether the need has actually gone). It goes to Z through the ACE if the task would drop something Z asked for, a learning outcome, or a confirmed definition. A `wont-do` task is kept in the record, not deleted, so the reasoning survives.

## Escalation language (orchestrator to ACE)

```
ESCALATE-TO-ACE
Type:        layer-call | definition | source-conflict | conformance-tier | sa-rule | licensing | scope-drop | unblock-dispute | other-judgment
Task:        <id and state>
Question:    <one sentence>
Evidence:    <paths, glossary ids, spec passages, test output>
Readings:    <the plausible answers, one line each>
Default:     <recommended answer>
```

`scope-drop` proposes `wont-do`; `unblock-dispute` is a disagreement about whether `unblock_when` is met. The ACE answers RULE or ESCALATE with the log entry (see `ace-protocol`); the orchestrator records the outcome and moves the task.

## Merge gate and push-back

The orchestrator owns the merge and may **refuse it**. A task does not leave `in-review` for `done` while any of these hold, and the orchestrator sends it back to `in-progress` with a push-back note:

- the diff touches paths outside the blast zone;
- the diff is noisy: unrelated reformatting, renames or edits that the task did not need (the author cleans it, the orchestrator does not);
- an open question is unresolved (the author or reviewer raised it and nobody has answered);
- a premise did not hold and the contract was not corrected;
- an acceptance check was not run or its output was not pasted, or the orchestrator's re-run disagrees;
- the reviewer's model is the same as the author's, or the review found a FAIL or a CANT_TELL;
- a gap is worked around without a record, or a commit carries a co-author trailer.

Push-back note, sent to the author:

```
PUSH-BACK
Task:      <id>
Refused:   <which merge-gate condition(s)>
Required:  <what must change, as checkable items: paths to revert, checks to re-run, the question that needs an answer and from whom>
Route:     <who answers an open question: the orchestrator, the ACE, another subagent, or Z through the ACE>
```

An open question is resolved by an answer recorded in the task, not by the author choosing: questions that need judgment go to the ACE in the `ESCALATE-TO-ACE` form and the task waits in `escalated` (or `blocked`, with an `unblock_when`). A task pushed back twice for the same reason goes to the ACE as an `other-judgment` (is the contract wrong?) instead of a third round. The orchestrator refuses to merge, but never fixes the work itself.

## Segregation: workspace, context, capability

Three boundaries keep roles independent, and each is controlled by a different mechanism:

- **Workspace** is controlled by **local git worktrees**: each task runs in its own worktree on its own branch, created by the orchestrator from a named base. A subagent writes only inside its worktree and its declared blast zone.
- **Context** is controlled by **instructions**: the role file and the work contract are everything a cold session receives. No conversation history crosses the boundary.
- **Capability** is controlled by the **pinned model** in the role file or the launch. Author and reviewer models differ.

## Independent review

Whoever reviews work runs on a different model than whoever authored it. The contract names the author's model and the reviewer's; the orchestrator confirms they differ before `in-review`, and if they do not, launches the reviewer on another pinned model. No role reviews its own output.
