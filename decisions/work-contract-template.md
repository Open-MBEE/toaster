# Work contract template

The orchestrator writes one per task and passes it, with the subagent's role file, to a cold session. It carries no conversation history: the subagent works from the repository and this contract alone.

```
CONTRACT <id> | <date>
Role:           <.claude/agents/<role>.md>, model <explicit id>, effort <level>
Reviewer:       <role>, model <explicit id, and different from the author's model>
State:          <ready | in-progress | in-review | escalated | blocked | done | wont-do>, per decisions/task-states.md
Task:           <one paragraph, what to produce>
Context:        <where to look: paths, glossary term ids, decision records>
Non-goals:      <what the subagent must not do or change>
Blast zone:     <the only paths it may write, on branch <name> in worktree <absolute path>>
Acceptance:     <binary criteria, each with a runnable check>
Premises:       <claims in this contract the subagent must verify against the repository at HEAD, not trust>
Questions to:   the orchestrator (who routes to the ACE, another subagent, or an owner)
Report:         branch and commit, model run on, results of every check, everything flagged and not fixed,
                every premise that did not hold
```

Merge gate: the orchestrator may refuse to merge (out-of-zone or noisy diff, unresolved open question, unmet premise, unrun check, same-model or failed review) and returns the task with a PUSH-BACK note; see decisions/task-states.md.

Rules: the author and the reviewer run on different models (no role reviews its own output); a blocked task records `blocked_on`, `unblock_when` and `owner`; the worktree is created by the orchestrator (`git worktree add <path> -b <branch> <base>`); the model is pinned in the launch; commits are plain, with no co-author trailers; the subagent does not merge or push.
