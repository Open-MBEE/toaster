Read AGENTS.md first. Part 1 (Foundations) says what this tutorial teaches, which
sources define its terms, how the functional, logical and physical layers differ,
and how models are built and queried. Part 2 is the legacy roster and file
authority matrix (each role edits only its assigned files; changes are committed
after each logical unit; reviewers produce reports rather than edits). Where they
conflict, Part 1 governs.

Read order for a cold session: AGENTS.md Part 1, then the skills below that your
task touches (start with `architecture-layers` and `ace-protocol`), then the
glossary CLI for any term you are about to define or use:

    uv run python -m glossary lookup TERM      # every definition, by source, with locators
    uv run python -m glossary tutorial TERM    # the idea, formal semantics and story we use
    uv run python -m glossary check            # must pass before you commit glossary or gloss changes

Definitions come from the glossary, not from memory. Sources in citation order:
SEBoK (ideas), the OMG SysML v2 / API / KerML specs (formal semantics), Hawkins
2011 (judgment taxonomy), Åström and Murray with Sutton and Barto (mechanism and
policy only), Douglas (story and the toaster example). OpenSysML and sysml-toolkit
are toolchain, cited only to flag spec gaps.

Skills (.claude/skills/ directory):
- architecture-layers       — what / how / where boundary tests, spec idioms, per-layer audit checklist, source map
- opensysml-query           — the three query surfaces, tested recipes, what does not work and the workarounds
- tutorial-glossary         — using and extending the glossary knowledge graph
- opensysml-api             — opensysml v0.9.0 interface (A2, A5)
- sysml-v2-toaster-model    — SysML v2 subset + model conventions (A3)
- toaster-recipe            — sub-notebook template (A4, A6)
- toaster-review-protocol   — Hawkins judgment record fields (A3)
- sysml-diagrams            — diagram pipelines + quality gates; DOT/SysMLD preferred (A2, A7)
- orchestrator-protocol     — WBS contract, loop rules, escalation triggers (A1)
- ace-protocol              — the ACE: triage layer between the team and Z; decision framework, Z's patterns, brief format (A8)
- myst-publication          — CI pipeline, MyST config, GitHub Pages (A2)
- tutorial-supporting-pages — docs/ pages structure and authoring rules (A4)
- skill-editor              — pre-edit gate, minimal-change rule, revert protocol (A8 only)
- tutorial-style-guide      — prose style, diagram aesthetics, code style (A3, A4, A6, A7)
- user-testing              — simulated learner protocol, personas, report format, ACE synthesis (A8, A9)

Skills not yet updated for the Foundations (toaster-recipe, sysml-v2-toaster-model,
tutorial-style-guide, sysml-diagrams, orchestrator-protocol, user-testing) may
still carry the earlier framing; see decisions/next-passes.md. When a skill and
AGENTS.md Part 1 disagree, Part 1 governs.
