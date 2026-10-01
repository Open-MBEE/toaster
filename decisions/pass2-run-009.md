# Pass 2, run 009: layer audits of Ch6-Ch8, and a citation-integrity finding (2026-09-27)

Contract PASS2-011 (originally scoped Ch6-Ch10). Three `layer-auditor` runs (Opus 5.5), two spot reviews (Sonnet 5), one ACE batch (Fable 5.1).

## Scope correction, before launch

Ch9 and Ch10 turned out to be entirely stub notebooks (no model content, no cumulative fixture — every notebook's model cell is a literal `# stub` placeholder). Rather than audit empty chapters, the orchestrator dropped those two worktrees before launch and recorded the finding in `pass4-backlog.md`'s Coverage section. Caught by reading the chapter directories, not by an auditor.

## What ran

1. Three parallel audits (Ch6, Ch7, Ch8), same pattern as run 006, with the conformance CLI (run 008) used as a diagnostic tool inside the audits rather than re-derived by hand.
2. Two spot reviews of the most load-bearing new tool claims: Ch7's state-machine trigger-resolution gap, Ch8's "adds zero model elements" claim. Both required an explicit model override (`model: "sonnet"`) on the Agent call — the `reviewer` role file's own default (Opus 5.5) collided with the audit author's model this time, since both are auditor output. Both first-attempt launches correctly self-detected the collision and stopped without reviewing, per the role file's own instruction, rather than silently reviewing same-model. Both PASSED on the second launch, all claims confirmed.
3. One ACE batch of ten consolidated questions. Nine ruled, one escalated to Z (DL-046: does a pre-alignment decision, DL-006, still stand against a stated Part 1 learning outcome — AGENTS.md 1.1 item 5, model checking beside simulation).

## The citation-integrity finding

All three Ch6-8 auditors independently flagged, unprompted, that `z-principles.md`'s "Confirmed extensions" section and `pass4-backlog.md` cited the wrong DL numbers for several of run 006's rulings (an orchestrator transcription error when logging the batch and asking Z to confirm — `decisions/log.md`'s own headers were always correct). Verified against the log and fixed in nine places across three files (commit `6995a84`) before continuing the audit work. The confirmed *content* was unaffected; only the numbers pointing to it were wrong.

This is the clearest evidence yet that independent, differently-scoped auditors reading the same corpus catch things a single reviewer pass would miss — three separate auditors, given different chapters and different explicit instructions, all noticed the same latent error on their own.

## What the chain showed

- **Model-collision self-detection worked as designed.** The reviewer role file's instruction to stop rather than silently review same-model output held under a case the orchestrator hadn't anticipated (auditor-vs-auditor, not the usual builder-vs-reviewer pairing). Process lesson recorded: when reviewing auditor output (or any role whose default model isn't the counterpart being reviewed), the orchestrator must pass an explicit `model` override on the Agent call rather than relying on the reviewer role file's own default.
- **New tool gap found:** state-machine trigger names are not resolved by OpenSysML at all (D-023) — a more severe hole than the port-type or allocation gaps, since a typo produces no signal whatsoever, not even a wrong answer.
- **A real chapter-scope surprise:** Chapter 8, titled "Constraint Checking," adds nothing to the model and performs no formal model checking — everything in it is Python claim evaluation on fixed values, already covered by the DL-039 false-satisfy pattern. This is now Z's decision (DL-046): whether that's a defect against Part 1's own learning outcomes, or whether the earlier SA-6 scoping decision should stand.

## Backlog and gap register updated

`decisions/pass4-backlog.md` sections 12-15 (Ch6, Ch7, Ch8 findings, and the citation-integrity process note); Coverage section corrected for the Ch9/Ch10 stub finding. `DEFERRED.md` D-023 (trigger resolution, no draft issue yet — needs a spec citation not yet located).

## For Z

One escalation, DL-046 (see decisions/log.md): does DL-006 still stand, or does Chapter 8 need to deliver actual model checking per AGENTS.md 1.1 item 5? The ACE's default is B (deliver it), gated by a probe showing OpenSysML v0.9.0 can actually answer a "holds" question with a formal engine — unproven today, every form tried was declined.

Two mechanical follow-ups, not blocking: set `applies_from` for `satisfaction-claims-evaluated` to Chapter 3 in the registry (DL-048, small builder contract); three flagged extensions (DL-040, DL-044, DL-045) await Z's skim before being added to the confirmed-extensions list.
