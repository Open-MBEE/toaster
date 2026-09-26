# Pass 2, run 004: generated glossary page, push-back and three reviews (2026-09-26)

Contract PASS2-006: `render` regenerates `docs/glossary.md` from the confirmed graph and `check` fails when the page is stale. Builder Sonnet 5, reviewer Opus 5.5 (different model), ACE Fable 5.1. Roles were launched by name for the later rounds; the model each reported matched its role file (builder `claude-sonnet-5`, reviewer `claude-opus-5-5`).

## How it went

1. **Round 1.** The builder delivered; all six acceptance checks passed by the orchestrator's re-run. Independent review: CANT_TELL (19 mutants, 18 killed; a survivor: `--dry-run` wrote the page), with a copyright question the reviewer could not settle.
2. **ACE triage.** Two questions ruled (the Tutorial entry is an attribution, not a source with a builder locator; drop "(PDF n)" from learner locators; the page shows every confirmed term). One escalated: near-verbatim canonical wording on a public page is a licence acceptance and a change to confirmed definitions. Z chose to accept short attributed wording (DL-026, DL-027).
3. **Push-back 1** (merge refused): builder-facing content on the learner page, decided changes not yet applied, and test gaps. The builder made exactly the required changes.
4. **Re-review: FAIL.** The reviewer found a real defect: "refines the sources above" was printed without checking which sources were above, so the learner page contradicted itself (logical architecture appeared to refine SEBoK while differing from it), and a test pinned it. This came from the push-back instruction the ACE and orchestrator had specified, not from the builder's departure from it.
5. **Push-back 2** (merge refused): name only the confirmed refined sources, from `gl:refines`; new tests including a Formal-kind fixture. Re-review PASS: every bridge entry independently verified against the graph (12 of 12), all named mutants killed.
6. **Integrated** by the orchestrator after re-running the checks: 119 tests pass, ruff clean, `render --dry-run` unchanged, no co-author trailers.

## What the chain showed

- **Merge gate and push-back earned their place.** Two refusals, both correct: the first removed builder-facing text from a learner page; the second removed a false statement that only the reviewer's independent check against the graph would have caught.
- **A decided wording can be wrong.** The ACE ruled "refines the sources above suffices where the refined edges are the term's own listed sources"; that was true in the case it looked at and false in general. Deriving output from the graph and verifying it against the graph, entry by entry, is what caught it. Reviews should check generated output against the data, not only against the spec text.
- **Escalation worked as designed**: the ACE ruled what the principles determined and escalated the licence acceptance that only Z can give, with a candidate, drafts and a gate.
- **Cost:** three reviews and three builder passes for a small feature. That is affordable for a learner-facing page; it is not a rate to apply to every change.

## Follow-ups (non-blocking, from the reviews)

- Tests: an unconfirmed other-term `gl:refines` target is not named; own-term de-duplication when two refined edges share a source.
- `differsFrom` notes do not filter by confirmed status (no real edge affected); a design call.
- Natural sort of locators (p. 3 before p. 20); escaping of labels containing commas or semicolons in the attribution.
- The Formal fixture source lives in `glossary/tests/test_render.py`, not conftest (adding it to conftest broke unrelated tests); acceptable.
- Formatting noise: an intermediate commit fails ruff; the head is clean. Future contracts should ask for lint-clean commits.
- The page depends on `docs/` existing (skipped silently otherwise; decided). It is in the site toc but the deploy job is still a placeholder, so nothing is public.
