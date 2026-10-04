# Contribution policy: amendments after the final gate (ACE batch 5, DL-128): authoritative

Governs over final-texts.md / final-texts-2.md where they differ. All edits are exact-text substitutions: locate by OLD TEXT,
exactly one match, else STOP and report. Files: `docs/contributor.md` and `.github/PULL_REQUEST_TEMPLATE.md` only. No URL is
added or removed (rule g); `AGENTS.md` is unchanged.

## B1 (docs/contributor.md, "Keep current")
Step 1, LAST sentence:
- before: ... and the `opensysml.connect(version=...)` calls in `scripts/check_conformance.py` and `scripts/check_construction.py`, together.
- after: ... and every `opensysml.connect(version=...)` call in `scripts/check_conformance.py`, `scripts/check_construction.py`, `chapters/`, `exercises/` and `tests/` (`git grep -n 'connect(version=' -- src scripts chapters exercises tests`), together. Code cells, stored outputs and `models/` are protected during editorial passes, not during a bump: the notebooks are re-executed and their outputs regenerate (step 3). `scripts/probes/` and `scripts/diagram_study/` are dated probes and keep the version they probed.

Step 5, the parenthetical grep and the sentence after it:
- before: re-check chapter prose and `DEFERRED.md` entries that state a version (`git grep -n 'v0\.9\.[01]' -- chapters DEFERRED.md`): a statement re-probed under the new release takes the new version; one not re-probed keeps the version it was probed against.
- after: re-check the prose, tests and `DEFERRED.md` entries that state a version (`git grep -n 'v0\.9\.[01]' -- chapters exercises tests DEFERRED.md`): a test or fixture that pins the version moves with it; a statement re-probed under the new release takes the new version; one not re-probed keeps the version it was probed against.

## B2
`docs/contributor.md`, "How a change is built and reviewed" step 3, first line:
- before: 3. Run `uv run python -m glossary lint` before committing prose; run the pacing check in
- after: 3. Before committing prose, check that `uv run python -m glossary lint` reports no hit the base branch does not (it is not a CI gate and exits 1 on pre-existing hits: run `--write-baseline base.json` on the base, then `--baseline base.json` on your branch, which exits 1 only on a new error); run the pacing check in
(the rest of step 3 unchanged; keep the page's wrapping style where the new text lengthens the line.)

`.github/PULL_REQUEST_TEMPLATE.md`, last Protections bullet:
- before: - [ ] `TOASTER_REQUIRE_TOOLS=1 uv run pytest tests/ glossary/tests/` and `uv run python -m glossary lint` pass locally
- after: - [ ] `TOASTER_REQUIRE_TOOLS=1 uv run pytest tests/ glossary/tests/` passes locally, and `uv run python -m glossary lint` reports no hit the base branch does not (it is not a CI gate; see the contributor guide)

## n2 (harmonise to "worse on none")
- `docs/contributor.md` "Improve what is here": `State in the pull request which priority improves and the evidence, and for each of the other two why it is not worse;` -> `State in the pull request which priority improves and the evidence, and why the change is worse on none of the three;`
- `.github/PULL_REQUEST_TEMPLATE.md`: `Not worse on each of the others (one line each, with how you checked):` -> `Not worse on any priority (one line each, with how you checked):`

## n1 (recorded, no edit)
"How a change is built and reviewed" step 2 carries the run instruction for `scripts/check_construction.py --check --chapter=N`
(registered construction zones executed, each TOASTER_INCREMENT and the cumulative fixture loaded; an existing
CONSTRUCTION_NOTEBOOKS entry is edited only if its stubs change; new entries are for new notebooks, which are not accepted),
added in CT-2 after the guard's rule (g) caught the dropped URL (ACE batch-3 follow-up).
