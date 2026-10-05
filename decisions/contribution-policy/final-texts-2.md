# Contribution policy: amendments after the CT-2 review (ACE batch 4, DL-124): authoritative

Governs over `final-texts.md` where they differ. AGENTS.md §1.12 stays UNCHANGED. All docs edits are to `docs/contributor.md`
unless stated; locate every edit by OLD TEXT (line numbers approximate), exactly one match, else STOP and report.

## F1 (substantive)
**"Keep current" step 1: replace the whole step with:**
```
1. Change the version in `pyproject.toml` (Python), `package.json` (Node) or
   [`scripts/tool-pins.json`](https://github.com/Open-MBEE/toaster/blob/main/scripts/tool-pins.json)
   (the `sysmlv2` binary, Z3 and the PlantUML jar with their sha256 hashes, and the
   standard-library commit), then `uv lock` / `npm install` to update the lockfile, or
   `uv run python scripts/provision-tools.py` to re-provision `.tools/`. The OpenSysML runtime
   binary is pinned separately from the `opensysml` package: change the `version="v0.9.0"`
   defaults in `src/toaster/bootstrap.py` (and its `_CLI_SUMS` hashes) and
   `src/toaster/connect.py`, and the `opensysml.connect(version=...)` calls in
   `scripts/check_conformance.py` and `scripts/check_construction.py`, together.
```
(Also carries Q3.) **Step 5: replace the whole step with:**
```
5. Commit the lockfile or the pins alongside the version change; never bump a version without
   regenerating and committing what matches it. Update the version strings in
   `docs/setup.md`, `docs/reproducibility.md` and `AGENTS.md` §1.2 in the same change, and
   re-check chapter prose and `DEFERRED.md` entries that state a version
   (`git grep -n 'v0\.9\.[01]' -- chapters DEFERRED.md`): a statement re-probed under the new
   release takes the new version; one not re-probed keeps the version it was probed against.
```
## F2
- "Keep current" bullet: `updating that entry's status line and the comment cell at the workaround (headings stay: they are linked anchors)` -> `adding a dated status line to that entry (or updating the one it has), updating the comment cell at the workaround, and leaving the heading as it is (headings are linked anchors)`
- step 4 of "Keep current": `retire the workaround, update the entry's status line and the comment cell at the workaround (do not rename the heading)` -> `retire the workaround, add a dated status line to the entry (or update the one it has), update the comment cell at the workaround (do not rename the heading)`
## F3
- `If you think the tutorial needs something new, open an issue first; only Z decides that, and a glossary term is confirmed only by Z.` -> `If you think the tutorial needs something new, open an issue; only Z decides that, and a glossary term is confirmed only by Z.` (AGENTS.md §1.12 unchanged; default: no exception clause.)
## F4 (three one-word edits)
- `An independent reviewer on a different model checks the statement` -> `An independent reviewer on a different AI model checks the statement`
- `(always on different models, never the same one reviewing its own work)` -> `(always on different AI models, never the same one reviewing its own work)`
- `Get an independent review on a different model than whoever authored the change` -> `Get an independent review on a different AI model than whoever authored the change`
## Q1: no text added (1.3 and 1.11 already govern). Default: not added.
## Q2: insert after the third bullet of "What we accept" ("Not accepted by pull request"), before `## Who is Z`:
```
The reviewer applies this test. A pull request passes when one "better" line (or, for keeping
current, the currency event) and all three "not worse" lines are evidenced; any "worse" means the
change is not accepted; what the reviewer cannot tell goes to the ACE.

| Priority | "Worse" means | Verified by, with what evidence |
|---|---|---|
| (1) Spec conformance | Text or model violating a normative clause of one of the three specifications; a spec-anchored construct replaced by a tool idiom; a conformance check or its negative control dropped or weakened | Reviewer: the clause citation, `uv run python scripts/check_conformance.py`, a strict load under the pinned runtime; the OMG SysML v2 Pilot Implementation is the baseline where a clause is ambiguous |
| (2) Didactic clarity | Longer or denser without the learner's task getting harder without it; a second construct or operation in one sub-notebook; a check presented as proof; the pacing rule broken; a figure whose omissions are no longer stated | Reviewer: the pull request's statement, the pacing check, and a simulated-learner checkpoint when the change alters what a learner does or sees beyond wording |
| (3) Tool use | A construct described as working but not run under the pinned version; a new workaround without a `DEFERRED.md` entry and comment cell; a tool demonstration removed; meaning moved from the model into Python | CI (`TOASTER_REQUIRE_TOOLS=1`, `myst build --strict`, `scripts/check-site.py`) and the reviewer re-running the touched notebook; the executed outputs and the `DEFERRED.md` entries touched |
```
## EXTRA (a): `.github/PULL_REQUEST_TEMPLATE.md`, Protections, first bullet
`- [ ] No new chapter, notebook, exercise, construct or analysis operation, model element, judgment record or glossary term` -> `- [ ] No new chapter, notebook, exercise, construct or analysis operation, model element, judgment record, glossary term or learning outcome`
## EXTRA (b) (CT-6, ACE): `.claude/skills/sysml-diagrams/references/recipes.md`
- ~L92-94 before: `Confirmed directly against real chapter content (\`decisions/diagram-study-real-fixtures.md\`;` / `Ch6's \`ApplyHeat\` action, exit 0, real action-flow notation). No in-house action-flow renderer` / `exists yet. Expected output: the declared actions, initial/final nodes, and successions. Check`
  after: `Confirmed against real chapter content (\`decisions/diagram-study-real-fixtures.md\`; Ch4's \`ToastBread\` and Ch6's \`ApplyHeat\` actions, exit 0): the control sequence is drawn, but the CLI's DOT omits the actions' declared typed flows (D-037); the caption must say so. No in-house action-flow renderer exists yet. Expected output: the declared actions, initial/final nodes, and successions, without flow pins. Check` (rest of the paragraph unchanged; keep the file's line wrapping)
- ~L109-111 before: `Confirmed directly against real chapter content (\`decisions/diagram-study-real-fixtures.md\`):` / `100% success across both OpenSysML runtime render forms on Ch7's real \`Cycle\` state machine, and the` / `mutation-control test (retargeting a transition) correctly changes the rendered output. Show`
  after: `Run against real chapter content (\`decisions/diagram-study-real-fixtures.md\`): both OpenSysML runtime render forms exit 0 on Ch7's real \`Cycle\` state machine and draw its states and transitions, but the \`do\` activity label omits the performed action's name (D-037); the caption must say so. The mutation-control test (retargeting a transition) correctly changes the rendered output. Show` (rest unchanged)

## CORRECTION recorded after CT-6 (ACE editor, DL-125 amended): the EXTRA (b) action-flow paragraph, as APPLIED
The batch-4 EXTRA (b) action-flow text cited `decisions/diagram-study-real-fixtures.md` as confirming the Ch4/Ch6 renders; that study (L52) did not rerun the action-flow view and DL-057's probe did. The text actually applied (commit d14bc6a) is:

Confirmed against real chapter content (Ch4's `ToastBread` and Ch6's `ApplyHeat` actions, exit 0: `figures/ch04-toastbread-flow.svg`, `figures/ch06-applyheat-flow.svg`, DEFERRED.md D-037; the real-fixture study, `decisions/diagram-study-real-fixtures.md`, did not rerun the action-flow view, the DL-057 probe did): the control sequence is drawn, but the CLI's DOT omits the actions' declared typed flows (D-037); the caption must say so. No in-house action-flow renderer exists yet. Expected output: the declared actions, initial/final nodes, and successions, without flow pins. Check (rest of the paragraph unchanged)

The state-transition paragraph was applied exactly as in EXTRA (b). Follow-up note (not edited; decisions/ is append-only history): `decisions/diagram-survey.md` L185 says "Phase 0 confirms this exact element already renders cleanly on real content" for Ch6's `ApplyHeat` action-flow; the fixture study (L52) and DL-057 (L735) say Phase 0 did not test action-flow.

## CT-5 addenda (micro-ruling, DL-127)
- docs/contributor.md, "Improve what is here" bullet: `goes to the ACE.` -> `goes to the ACE (the project's triage role, described below).` (first use only; the table lead-in keeps the bare second use; no label or URL).
- README.md ~L52: `decisions/  — ACE decision log` -> `decisions/  — decision log (rulings and escalations)`.
