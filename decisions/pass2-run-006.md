# Pass 2, run 006: parallel layer audits of Ch2 to Ch5 (2026-09-26)

Contract PASS2-008 (four tasks, A to D): layer-audit the elements each of Ch2 to Ch5 adds. Four `layer-auditor` runs (Opus 5.5, launched by name) in four private worktrees, in parallel; then two spot reviews by Sonnet 5 (a different model) of the Ch5 and Ch3 reports' factual and tool claims; then one batched triage by the ACE (Fable 5.1) of the ten consolidated questions.

## What ran

1. **Fan-out.** Four worktrees from HEAD, four contracts differing only in chapter, focus and context (Ch3: MoE/MoP labeling; Ch4: `ApplyHeat` mixing; Ch5: allocation, perform, the lint hit). All four tasks `in-progress` at once; each committed one file inside its blast zone (verified per branch, no trailers), and the orchestrator integrated the four reports.
2. **Independent verification.** Spot reviewers re-ran the reports' claims: 7 of 7 (Ch3) and 6 of 6 (Ch5) confirmed, including the headline tool claim (sysml-toolkit with the library rejects Ch5's definition-level allocate while OpenSysML accepts it) and one extension (the false-satisfy pattern also occurs in Ch6 to Ch8).
3. **Consolidation.** About 40 open questions and findings from four reports were merged into ten questions by type (cross-chapter duplicates merged; for example the `ApplyHeat` equality question arrived from three chapters) and sent to the ACE as one `ESCALATE-TO-ACE` batch. The ACE ruled all ten (DL-030 to DL-039); none was escalated to Z. The findings became `decisions/pass4-backlog.md` (eleven themes) and three new gap entries (D-019 to D-021) with two unfiled bug drafts.

## What the chain showed

- **Fan-out worked.** Four parallel auditors produced consistent, comparable reports; identifiers continued across reports so the log had no collisions; the cross-chapter questions surfaced as duplicates the orchestrator could merge. Cost: about 155k subagent tokens per audit (about 7 minutes each, run concurrently), 80k per spot review, 180k for the ACE batch.
- **Batching mattered.** Sending the ACE one consolidated batch by type, not 40 questions, produced rulings that reference each other (DL-030 to DL-039) and none that contradict.
- **The ACE escalated nothing, again.** Six rulings extend principles to new kinds of case (DL-030, DL-032, DL-033, DL-034, DL-037, DL-039) and each says so. One of them (DL-039 part 1) changes the meaning of a ruling of Z's (DL-025); the orchestrator flagged it as pending Z rather than accepting it. A ruling that revises a Z decision should escalate; the `ace-protocol` skill does not yet say so.
- **Audits surfaced tool gaps a chapter run never would**: definition-level allocate and item-typed part usages, both accepted by OpenSysML (one also by the toolkit). The audit method (compare the model with an independent checker, not only reload it) is worth keeping.
- **Auditors' premises again failed informatively**: "Chapter 3 introduces MoE and MoP" and "Chapter 5 introduces the logical-to-physical architecture" did not hold.

## Follow-ups

Second audit wave (Ch6 to Ch10); the ace-protocol clause on rulings that amend a Z decision; the language-gap guard and the "satisfaction claims evaluated" check (builder contracts, after Z's decision on DL-039); the predecessor check for cumulative fixtures and the missing import in Ch4 nb03 (small builder contracts).

## Z's read-back (2026-09-27)

Z accepted DL-039's reading of DL-025 (language conformance is defined by the spec, not by `model.ok`; a known spec violation blocks a project check with a checkable unblock criterion, and the tutorial supplies a language-gap guard with negative controls until upstream fixes the hole). Z confirmed the six flagged extensions (DL-030, 032, 033, 034, 037, 039) as matching Z's own judgment; they are recorded as Z's rulings, not merely unobjected-to ACE inferences. **Correction (2026-09-27, found by the Ch6 and Ch8 layer audits):** this entry, `pass4-backlog.md` and `z-principles.md`'s "Confirmed extensions" section originally cited these six one number off for four of them (033/034/035/038 instead of 032/033/034/037); `decisions/log.md`'s own headers were always correct and are authoritative. The confirmed *content* is unaffected — only the citations were wrong, now fixed in all three files.
