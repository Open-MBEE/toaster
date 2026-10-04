<!-- docs/contributor.md "What we accept" (AGENTS.md 1.12): this tutorial accepts changes that keep it
current and strictly dominant improvements to existing content. It is not adding new content. -->

## What this change is (tick one)

- [ ] Keeps current: pin or dependency bump / workaround retired (DEFERRED entry D-___) / spec-edition re-check / drift fix
- [ ] Improves what is here (fill in the next section)

## Strictly dominant (improvements only)

Better on (name it, with evidence):
- [ ] (1) Spec conformance — clause(s): ___ ; check run: ___
- [ ] (2) Didactic clarity — what gets harder for the learner without this change: ___ ; pacing check: ___
- [ ] (3) Tool use — construct or operation run under the pinned versions: ___

Not worse on each of the others (one line each, with how you checked):
- (1) ___
- (2) ___
- (3) ___

## Protections

- [ ] No new chapter, notebook, exercise, construct or analysis operation, model element, judgment record, glossary term or learning outcome
- [ ] `models/`, judgment records, stored outputs and `DEFERRED.md` headings unchanged, or the change says why and recomputes `content_hash`
- [ ] `TOASTER_REQUIRE_TOOLS=1 uv run pytest tests/ glossary/tests/` and `uv run python -m glossary lint` pass locally
