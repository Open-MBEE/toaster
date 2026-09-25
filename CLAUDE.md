Read AGENTS.md first — it defines the file authority matrix, editing rules,
and escalation triggers. The short version: each agent role edits only its
assigned files, changes are committed after each logical unit, and reviewers
produce reports rather than edits.

Skills (.claude/skills/ directory):
- opensysml-api             — opensysml v0.9.0 interface (A2, A5)
- sysml-v2-toaster-model    — SysML v2 subset + model conventions (A3)
- toaster-recipe            — sub-notebook template + Tall three worlds (A4, A6)
- toaster-review-protocol   — Hawkins judgment record fields (A3)
- sysml-diagrams            — diagram pipelines + quality gates; DOT/SysMLD preferred (A2, A7)
- orchestrator-protocol     — WBS contract, loop rules, escalation triggers (A1)
- ace-protocol              — decision framework, Z's patterns, brief format (A8)
- myst-publication          — CI pipeline, MyST config, GitHub Pages (A2)
- tutorial-supporting-pages — docs/ pages structure and authoring rules (A4)
- skill-editor              — pre-edit gate, minimal-change rule, revert protocol (A8 only)
- tutorial-style-guide      — prose style, diagram aesthetics, code style (A3, A4, A6, A7)
- user-testing              — simulated learner protocol, personas, report format, ACE synthesis (A8, A9)
