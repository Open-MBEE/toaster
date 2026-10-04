# Contribution policy: final texts and rulings (ACE batch 3, DL-122): authoritative

Source: ACE batch-3 ruling of 2026-10-03 under Z's directive (see DL-122). Inventory: `inventory.md` (CT-1). Where this file and
the inventory differ, THIS FILE governs. Naming convention: DL-116/DL-117/DL-119.

## Canonical statements
**PS-1.** The contributions we want keep this tutorial current to its toolchain (the OpenSysML runtime, sysml-toolkit and the other pinned tools) and to the OMG SysML v2 specifications; we are not adding new content.

**PS-2.** Existing content may be refined, clarified or otherwise improved against three priorities: (1) conformance with the SysML v2 specifications (the OMG SysML v2 language, API and Services, and KerML specifications); (2) didactic clarity; (3) effective, demonstrative use of tools from the OpenSysML stack (the OpenSysML runtime and sysml-toolkit). An improvement is accepted only if it is strictly dominant: better on at least one of these and worse on none.

**PS-3.** New content is a new chapter, notebook, exercise, construct or analysis operation, model element, judgment record or glossary term, or a new learning outcome; none is accepted by pull request. Replacing a recorded workaround with the spec-anchored construct a newer tool release accepts is keeping current, not new content. A trade-off (better on one priority, worse on another) is not an improvement under this policy; propose it in an issue and Z decides.

**PL-1 (learner-facing, appended to ch10 conclusion.md "What comes next" after "...never made for them.").** If you come back to this repository, the contribution it wants is keeping it current to its toolchain and to the SysML v2 specifications, not extending it; the [contributor guide](#what-we-accept) says what that means.

(NOTE for the builder: `#what-we-accept` is a label in docs/contributor.md; chapter pages are separate pages, so use the correct cross-page form that MyST resolves in this repo: check how other chapter pages link to docs pages, e.g. `../../docs/contributor.md#what-we-accept`, and verify the built link resolves; report the form used.)

## AGENTS.md (Z-directed; this change is recorded by DL-122): insert after §1.11 (the paragraph ending before the `---` that follows it), a new section, verbatim:

```
## 1.12 What contributions we want

The contributions we want keep this tutorial current to its toolchain (the OpenSysML runtime, sysml-toolkit and the other pinned tools) and to the OMG SysML v2 specifications; we are not adding new content. Existing content may be refined, clarified or otherwise improved against three priorities: (1) conformance with the SysML v2 specifications (the OMG SysML v2 language, API and Services, and KerML specifications, §1.2); (2) didactic clarity; (3) effective, demonstrative use of tools from the OpenSysML stack (the OpenSysML runtime and sysml-toolkit). An improvement is accepted only if it is strictly dominant: better on at least one of these and worse on none. A trade-off is not an improvement under this rule; it is proposed in an issue and Z decides.

New content is a new chapter, notebook, exercise, construct or analysis operation, model element, judgment record or glossary term, or a new learning outcome; none is accepted by pull request. Replacing a recorded workaround with the spec-anchored construct a newer tool release accepts is keeping current (§1.9), not new content. Added text or cells count as improvement only where the learner's task gets harder without them (the earn-its-place test, `.claude/skills/ace-protocol/z-principles.md` P4; the pacing rule in `tutorial-style-guide`; SA-8). The reviewer-facing test is in `docs/contributor.md`, and the pull-request template asks for it.
```
No change to §1.11, Part 2 head, or Part 2 §5. (If the file's section numbering/heading style differs, match it; report.)

## docs/contributor.md
1. Insert as the NEW FIRST SECTION after the intro paragraph (after line 5), before `## Who is Z`:

```
(what-we-accept)=
## What we accept

The contributions we want keep this tutorial current to its toolchain (the OpenSysML runtime, sysml-toolkit and the other pinned tools) and to the OMG SysML v2 specifications; we are not adding new content. Existing content may be refined, clarified or otherwise improved against three priorities: (1) conformance with the SysML v2 specifications (the OMG SysML v2 language, API and Services, and KerML specifications); (2) didactic clarity; (3) effective, demonstrative use of tools from the OpenSysML stack (the OpenSysML runtime and sysml-toolkit). An improvement is accepted only if it is strictly dominant: better on at least one of these and worse on none. The binding statement is [`AGENTS.md`](https://github.com/Open-MBEE/toaster/blob/main/AGENTS.md) §1.12.

- **Keep current.** Bump a pin in `pyproject.toml`/`uv.lock`, `package.json`/`package-lock.json` or [`scripts/tool-pins.json`](https://github.com/Open-MBEE/toaster/blob/main/scripts/tool-pins.json) and regenerate the outputs ([below](#keep-current)); retire a workaround whose [`DEFERRED.md`](https://github.com/Open-MBEE/toaster/blob/main/DEFERRED.md) resolution condition a new release meets, updating that entry's status line and the comment cell at the workaround (headings stay: they are linked anchors); re-check a clause that a new edition of one of the three OMG specifications changed. Reporting drift is a contribution too: open an issue naming the tool and version (or the specification edition), the chapter and cell, and the spec clause. Upstream issues are filed by the project itself, after Z has reviewed the text (`AGENTS.md` §1.9).
- **Improve what is here.** State in the pull request which priority improves and the evidence, and for each of the other two why it is not worse; the pull-request template asks for exactly this. Adding text or a cell counts as improving only if the learner's task gets harder without it, and the pacing rule and the one-construct-per-notebook rule still apply. An independent reviewer on a different model checks the statement; what the reviewer cannot tell goes to the ACE. A trade-off (better on one priority, worse on another) is not an improvement under this policy: open an issue and Z decides.
- **Not accepted by pull request.** A new chapter, notebook, exercise, construct or analysis operation, model element, judgment record or glossary term, or a new learning outcome. Replacing a recorded workaround with the spec-anchored construct a newer tool release accepts is keeping current, not new content. If you think the tutorial needs something new, open an issue first; only Z decides that, and a glossary term is confirmed only by Z.
```
("Who is Z" follows and names the handle. Because "Z" first appears in this new section, write "mzargham (Z)" at that FIRST "Z" mention on the page per DL-112 (first mention on published pages) and keep the later text.)

2. C-02 (about lines 48-52, the paragraph starting "If you want to extend a chapter ..."): replace the paragraph with:
```
If you want to keep a chapter current, clarify a definition, or review didactic content, the harness
tools above are built for exactly that — start at `CLAUDE.md`'s own read order rather than
improvising a workflow from scratch. The sections below cover the maintenance tasks directly; none
of them require running an agent, but all of them follow conventions the harness itself enforces
(the recipe's pacing rule, the layer boundary tests, the review gate), and every change passes the
test in [What we accept](#what-we-accept).
```
(Locate by text; the old sentence "extend a chapter" must exist exactly once; if the wording around it differs from this description, STOP and report.)

3. C-04 (about lines 88-98, the section "## Update a dependency and regenerate outputs"): replace heading and steps with:
```
(keep-current)=
## Keep current: update a dependency or tool pin and regenerate outputs

1. Change the version in `pyproject.toml` (Python), `package.json` (Node) or
   [`scripts/tool-pins.json`](https://github.com/Open-MBEE/toaster/blob/main/scripts/tool-pins.json)
   (the `sysmlv2` binary, Z3, the PlantUML jar and the standard-library commit, with their sha256
   hashes), then `uv lock` / `npm install` to update the lockfile, or
   `uv run python scripts/provision-tools.py` to re-provision `.tools/`.
2. Run `TOASTER_REQUIRE_TOOLS=1 uv run pytest tests/ glossary/tests/` and
   `uv run python scripts/check-tools.py`
   ([`check-tools.py` on GitHub](https://github.com/Open-MBEE/toaster/blob/main/scripts/check-tools.py)).
3. Rebuild the local preview (`uv run npx mystmd start --execute`) and spot-check a chapter that
   exercises the changed dependency; a version bump in `opensysml` or `sympy` can change
   printed output even when no test fails.
4. Re-read the `DEFERRED.md` entries that name the bumped tool. If the new release meets an
   entry's resolution condition, retire the workaround, update the entry's status line and the
   comment cell at the workaround (do not rename the heading), and recompute the `content_hash`
   of any judgment record the model change touches ([below](#change-a-model-element)). A release
   that breaks something gets a new entry, not a silently dropped demonstration.
5. Commit the lockfile or the pins alongside the version change; never bump a version without
   regenerating and committing what matches it. Update the version strings in
   `docs/setup.md`, `docs/reproducibility.md` and `AGENTS.md` §1.2 in the same change.
```
(Keep any existing anchor/label that other pages link to: the old heading's slug was `update-a-dependency-and-regenerate-outputs`; grep for inbound references; if any exists, keep a `(update-a-dependency-and-regenerate-outputs)=` label too.)

4. C-05 (about lines 100-113, "## Add a new chapter"): replace with:
```
## How a change is built and reviewed

New chapters are not accepted ([What we accept](#what-we-accept)); the rules that governed
building the existing ones govern every change to them:

1. `toaster-recipe`'s sub-notebook skeleton and `architecture-layers`' boundary tests bind any
   model element a change touches; both are binding, not stylistic suggestions.
2. Each cumulative fixture (`models/chNN-cumulative.sysml`) must keep containing everything the
   previous chapter's fixture has; see
   [`tests/test_predecessor_containment.py`](https://github.com/Open-MBEE/toaster/blob/main/tests/test_predecessor_containment.py) for how that invariant is checked.
3. Run `uv run python -m glossary lint` before committing prose; run the pacing check in
   `tutorial-style-guide` (consecutive code cells with no markdown between them) on every
   notebook you touched.
4. Get an independent review on a different model than whoever authored the change, per
   `decisions/task-states.md`'s merge gate.
```
(Keep the old heading's slug label if anything links to it; the existing content of that section that is not captured here must be reconciled: read the section first; if it contains steps not covered above that are still correct for CHANGING existing chapters, keep them under the new heading; if it describes adding a chapter only, drop them. Report what you dropped.)

5. C-06 (after about line 119, the start of the "Change a model element" section): insert one sentence before its numbered list:
```
A model change is accepted only as keeping current (a workaround retired) or as a strictly
dominant improvement ([What we accept](#what-we-accept)); either way:
```
C-07 unchanged.

## README.md
- ~L46: `exercises/  — parallel exercise notebooks (fork and work here)` -> `exercises/  — parallel exercise notebooks (work them in your own fork)`
- ~L57-58: `See [docs/contributor.md](docs/contributor.md) if you want to understand how the tutorial is actually built, tested, and reviewed, or to contribute to it yourself.` -> `See [docs/contributor.md](docs/contributor.md) to understand how the tutorial is built, tested and reviewed, and what contributions it wants: keeping it current to its toolchain (the OpenSysML runtime, sysml-toolkit and the other pinned tools) and to the OMG SysML v2 specifications, not adding new content.`
(Match the file's actual wrapping; locate by text.)

## docs/setup.md
- Heading `## Fork and exercise` is kept. After the paragraph that says the workspaces are blank (about L183) append:
```
Your fork is where your exercise work lives; it is not a contribution path. If, while working, you
find the tutorial out of date against a newer release of the OpenSysML runtime, sysml-toolkit or the
OMG specifications, that is the contribution this tutorial wants: see the
[contributor guide](#what-we-accept).
```
(setup.md and contributor.md are separate pages: use the in-site link form that resolves, e.g. `contributor.md#what-we-accept` or the `contributor` page ref; verify on the built page.)
- N4 (about L149): `**sysml-toolkit** does what the OpenSysML runtime cannot yet: prove that a constraint holds for every` -> `**sysml-toolkit** does what the OpenSysML runtime's Python binding cannot yet: prove that a constraint holds for every`

## chapters (markdown only)
- `chapters/ch10-traceability-signoff/conclusion.md` "## What comes next": append PL-1 after "...never made for them."
- N5 `chapters/ch07-execution/02-state-traces.ipynb` markdown cell `cell-23`: `The tutorial's own guard does: \`language_gap_findings\` flags` -> `The tutorial's own guard catches it: \`language_gap_findings\` flags` (nothing else changes).
- N6 `chapters/ch03-measures/03-threshold-judgment.ipynb` markdown cell `cell-03` (the cell discussing the file; NOT `968c7318`): append
  > Its `doc` comment's note `not yet supported in OpenSysML v0.9.0` predates this tutorial's component naming and refers to the OpenSysML runtime v0.9.0, which does not accept the formal `#verificationMethod` metadata; notebook 04 explains ([toaster#19](https://github.com/Open-MBEE/toaster/issues/19)).
  The quoted phrase stays in backticks (the lint rule has ignore_code). Code cells and models are untouched. NOTE: `toaster#19` link text is a protected token: ADDING it is fine.

## Skills (CT-3, ACE only; DL-122 is the pre-edit record; revert record = commit preceding the first skill edit)
`.claude/skills/tutorial-supporting-pages/SKILL.md`:
- L17: `| \`docs/contributor.md\` | Maintainer guide (4 update scenarios) |` -> `| \`docs/contributor.md\` | Maintainer guide ("What we accept" policy, then 4 maintenance scenarios) |`
- L19-32 template block: add after item 4, inside the fence: `5. Your fork is where your exercise work lives; it is not a contribution path (see the contributor guide).` (Nothing else in the block changes.)
- L48-53 ->
```
## Contributor guide — 4 required scenarios

The guide opens with "What we accept" (AGENTS.md §1.12: keep current to the toolchain and the
specifications; strictly dominant improvements; no new content), then:

1. Keep current: update a dependency or tool pin and regenerate outputs
2. How a change is built and reviewed
3. Change a model element and review stale judgment records
4. Run the full CI pipeline locally
```
- L59-64: add bullet `- Write a contributor scenario that invites a new chapter, notebook, exercise, model element or glossary term (AGENTS.md §1.12)`.

## CT-3b (separate ACE session, own pre-edit DL-123): `.claude/skills/sysml-diagrams/SKILL.md`
- L18 cell 3 -> `Confirmed against real chapter content (Ch4's \`ToastBread\`, Ch6's \`ApplyHeat\`): exit 0 and the control sequence is drawn, but the CLI's DOT omits the actions' declared typed flows (D-037); the caption must say so. No in-house action-flow renderer exists yet.`
- L19 cell 3 first sentence -> `The real-fixture study ran this against Ch7's real \`Cycle\` state machine: both OpenSysML runtime render forms exit 0 and draw the states and transitions, but the \`do\` activity label omits the performed action's name (D-037); the caption must say so.`
(Locate by text; the surrounding table cells and fences stay.)

## CT-4 (.github, lint)
New file `.github/PULL_REQUEST_TEMPLATE.md`:
```
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

- [ ] No new chapter, notebook, exercise, construct or analysis operation, model element, judgment record or glossary term
- [ ] `models/`, judgment records, stored outputs and `DEFERRED.md` headings unchanged, or the change says why and recomputes `content_hash`
- [ ] `TOASTER_REQUIRE_TOOLS=1 uv run pytest tests/ glossary/tests/` and `uv run python -m glossary lint` pass locally
```
`glossary/lint.py`: reject unknown per-rule keys: `unknown = sorted(set(raw) - set(FIELDS) - set(OPTIONAL_BOOL_FIELDS))` -> `LintConfigError(f"rule {name!r}: unknown field(s) {unknown}")` (adapt names to the actual code), a test in `glossary/tests/test_lint.py`, and "unknown rule field" in the README's exit-2 list. Acceptance: `uv run pytest glossary/tests/` passes; lint counts equal to base.

## N-items ruled (no edit unless listed above)
N1: recorded retroactively (glossary/README.md edit accurate; no revert). N2: no edit. N3, N8: no action. N7 leftovers (stored-output label `OpenSysML itself`, "this toolchain's Z3 backend" in code/outputs, "the pilot itself stays toolchain", D-019 body, D-034 Resolution): left.

## Reviewer checklist (strictly dominant)
| Priority | "Worse" means | Verified by | Evidence |
|---|---|---|---|
| (1) Conformance with the three OMG specifications | model or notebook text violating a normative clause; a spec-anchored construct replaced by a tool idiom; a conformance check or its negative control dropped or weakened; a staged check's status changed without its stated condition | reviewer (different model); the Pilot Implementation's behavior is the baseline where a clause is ambiguous (AGENTS 1.2) | clause citation; `uv run python scripts/check_conformance.py`; strict load under the pinned runtime; always-on guards still fire on their negative controls |
| (2) Didactic clarity | longer or denser without passing P4's test; a second construct or operation in a sub-notebook (SA-8); a lens named to learners (1.10); a check presented as proof or a disposition "accepted" (1.6, SA-7); pacing rule broken; a figure whose omissions are no longer stated | reviewer; a simulated-learner checkpoint (`user-testing`) when the change alters what a learner does or sees beyond wording | the proposer's P4 statement; pacing-check output; learner report where required; figure recipe and caption |
| (3) Demonstrative use of the OpenSysML stack | a construct described as working but not run under the pinned version (P5); a new workaround without DEFERRED entry, issue draft and comment cell (1.9); a tool demonstration removed; meaning moved from the model into Python (F4) | CI (`TOASTER_REQUIRE_TOOLS=1`, `myst build --strict`, `check-site.py`); reviewer re-runs the touched notebook | executed outputs; DEFERRED entries touched; `check-tools.py` output |

Decision rule: PASS needs one evidenced "better" (improvements) or an evidenced currency event (keep-current), plus all three evidenced "not worse" lines. Any "worse" -> not accepted (trade-offs go to Z by issue). CANT_TELL or a protected zone touched -> ACE. Ties with no currency event -> churn, declined.
