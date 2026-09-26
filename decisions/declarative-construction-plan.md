# Declarative Construction Architecture — Implementation Plan

**Status:** ACTIVE — DL-011 logged  
**Date:** 2026-09-25  
**Triggered by:** Z's direction: "the notebooks themselves are the code performing the build"  
**ACE review:** 2026-09-25 — 4 blocking + 5 minor findings corrected (see DL-011 for findings list)  
**Background context:** DL-008 moved model source to `models/chXX-cumulative.sysml` files;
Z identified that the cumulative files represent database *state* but not the *construction* process.
SysML v2 is declarative (like a database language); the tutorial should teach engineering by
having learners construct the model, not pull an already-built one.

---

## What changes

**Before:** Cell-02 in every notebook loads the full cumulative file silently. The cumulative files
are hand-authored source of truth.

**After:** Cell-02 in construct-introducing notebooks declares the new increment (via Editor API or
SysML string) and prints the reflection. The cumulative files become generated checkpoints.
Running the notebooks in sequence constructs the model.

---

## What stays the same

- The 7-cell template structure is preserved. Cell-02 gains construction code; no new cells added.
- The cumulative `.sysml` files remain in `models/` — they are now generated fixtures (checkpoints).
- Ch9–Ch10 analysis notebooks do not need construction cells (they query a finished model).
- The 5 gap construct notebooks already have notes pointing to toaster#9–#13. Their
  construction pattern is "print the SysML string declaration" — the string IS the declaration.
- Editor single-use rule: after `editor.apply()`, reload with `conn.load_from_content()` before
  constructing anything else. Cell-02 follows this: construct → `editor.apply()` → print →
  reload full cumulative.

---

## Scope

**Notebooks with construction cells (cell-02 updated): 13**

| Chapter | Notebooks | Count |
|---|---|---|
| Ch1 | nb01 (B), nb02 (A), nb03 (A), nb04 (A) | 4 |
| Ch2 | nb01 (B), nb02 (B) | 2 |
| Ch3 | nb01 (B), nb02 (A — pilot) | 2 |
| Ch4 | nb01 (A), nb02 (A) | 2 |
| Ch5 | nb02 (B), nb03 (A or B — probe first) | 2 |
| Ch7 | nb02 (A or B — probe first) | 1 |
| **Total** | | **13** |

**Explicitly excluded — no construction cells:**

| Notebooks | Reason |
|---|---|
| Ch2/nb03, Ch3/nb03, Ch4/nb03, Ch6/nb01–nb03 | Judgment or depth — no new SysML constructs |
| Ch5/nb01 | Navigation-only (model.find); no new SysML construct |
| Ch7/nb01, Ch7/nb03 | Sympy binding / param sweep — no new SysML construct |
| Ch8/nb01–nb03 | Analysis operations (verify_constraint, verify_satisfaction, stale detection) |
| Ch9/nb01–nb03, Ch10/nb01–nb03 | Query the finished model; no construction |

**5 gap construct notebooks (gap notes already added in prior session):**
Ch1/nb01 (abstract part def, toaster#9), Ch2/nb01 (require constraint, toaster#11),
Ch2/nb02 (attribute :>>, toaster#10), Ch3/nb01 (assert satisfy, toaster#12),
Ch5/nb02 (allocate, toaster#13)

---

## Construction cell convention (all 13 notebooks — all Pattern B)

**Phase 2 pilot finding (2026-09-25):** The Editor API produces bare declarations only
(no bodies, no `default =` form, calc/action/item defs without inputs or expressions).
All 13 construction notebooks use Pattern B (SysML string fragments) until the Editor API
reaches full spec coverage. See DEFERRED.md D-004 through D-010 for the gap registry.

### Structural rule: code factored as if we had the API calls

**The construction cell structure must mirror exactly what Pattern A would look like if the
Editor API were fully implemented.** One named fragment variable per element = one future
`editor.add_*()` call. When the API matures, replace each string with the corresponding
call; everything else stays the same.

### TOASTER_INCREMENT convention

`TOASTER_INCREMENT` = the **new declarations introduced by this notebook only** (not the full
cumulative model). It is assembled from the individual fragment variables at the end of the
construction zone and printed as the reflection.

### Construction zone structure

For a notebook introducing multiple elements (e.g., part def + two attributes):

```
[code cell]     ONE fragment variable declared + printed   ← mirrors one editor.add_*() call
[markdown cell] narration for that element
[code cell]     NEXT fragment variable + printed            ← mirrors next editor.add_*() call
[markdown cell] narration
...
[code cell]     TOASTER_INCREMENT assembled from fragments
                print(TOASTER_INCREMENT)                    ← reflection: the full increment
                load ch0X-cumulative.sysml; assert model.ok ← load for subsequent cells
```

### Fragment naming convention

Fragment variable names mirror the element being declared:
- `PART_DEF`, `HEATER_DEF`, `TOASTING_SYSTEM_DEF` — part definitions
- `POWER_ATTR`, `CYCLE_ATTR` — attribute declarations
- `HEATER_USAGE`, `CONTROL_USAGE` — part usages (composition)
- `TIMELY_REQ`, `DELIVERED_ENERGY_CALC` — requirement/calc usages

### Example: single-element notebook (Ch1/nb01 — abstract part def)

```python
from pathlib import Path
import opensysml
from toaster.report import format_diagnostics

conn = opensysml.connect(version="v0.9.0")

# abstract modifier not yet supported in Editor API — toaster#9 / OpenSysML#595
# spec: SysML v2 formal/2026-03-02 §7.3.3 (PartDefinition — AbstractClassifier)
TOASTING_SYSTEM_DEF = """\
abstract part def ToastingSystem {
    doc /* Any system that converts electrical energy into thermal energy
         for food preparation. */
}
"""
print(TOASTING_SYSTEM_DEF)

TOASTER_INCREMENT = TOASTING_SYSTEM_DEF
source = Path("../../models/ch01-cumulative.sysml").read_text()
model = conn.load_from_content(source, strict=False)
assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
```

### Example: multi-element notebook (Ch1/nb02 — part def + attributes)

```python
from pathlib import Path
import opensysml
from toaster.report import format_diagnostics

conn = opensysml.connect(version="v0.9.0")

# Part def shell — editor.add_part_def(owner='ToasterDemo', name='Heater') when API ships
HEATER_DEF = "part def Heater {"
print(HEATER_DEF)

# Power attribute — editor.add_attribute(owner=..., name='power', type=..., default=...) when API ships
# default = modifier not yet supported — toaster#N / OpenSysML#N
# spec: KerML formal/2026-03-02 §9.4.2 (FeatureValue — default keyword)
POWER_ATTR = "    attribute power : ISQ::PowerValue default = 800.0 [SI::W];"
print(POWER_ATTR)

# Cycle time attribute
CYCLE_ATTR = "    attribute cycleTime : ISQ::DurationValue default = 120.0 [SI::s];"
print(CYCLE_ATTR)

# Assembly — mirrors editor.apply() new-member output
TOASTER_INCREMENT = f"""\
{HEATER_DEF}
{POWER_ATTR}
{CYCLE_ATTR}
}}
"""
print(TOASTER_INCREMENT)

source = Path("../../models/ch01-cumulative.sysml").read_text()
model = conn.load_from_content(source, strict=False)
assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
```

### Fragment size rule

Each fragment variable: ≤5 lines of SysML, ideally 1–3 lines. If a fragment is longer,
it should be split into multiple fragment variables (one per logical sub-element). The
`TOASTER_INCREMENT` assembly may be longer but must be derivable from its named parts.

---

## Ordering: DL-011 logged BEFORE Phase 0

The architectural decision log entry is the authorization for the whole intervention. It must
precede all skill updates and implementation. It is logged immediately (see `decisions/log.md`
DL-011 entry), not at Phase 1e as the original draft had it.

---

## Phase 0 — Skill updates (FIRST — no implementation until complete)

Skills are the team's shared operating model. Agents must have correct guidance before
implementing; an incorrect skill propagates to every future session.

### 0a. `opensysml-api` — add Editor API section

Add after the "Connection" section:

```
## Editor API (programmatic construction)

model.edit() → Editor

# Structural
editor.add_part_def(owner, name, specializes=[], doc=None)
editor.add_part(owner, name, type=None, specializes=[])
editor.add_attribute(owner, name, type=None, default=None, multiplicity=None)
editor.add_member(owner, kind, name, ...)  # for kinds not covered by typed helpers

# Calculation
editor.add_calc_def(owner, name, inputs=[], return_type=None, expression=None)

# Item / state (confirm via probe before using)
editor.add_item_def(owner, name, ...)
editor.add_member(owner, kind="state def", name=...)

editor.apply() → EditResult
str(result)  # FULL MODEL including all prior + new declarations (not just the new member)

Editor single-use rule: editor is bound to one model hash.
After editor.apply(), must call conn.load_from_content(str(result)) before editing further.

Gap constructs — do NOT attempt these kinds; use Pattern B (SysML string) instead:
  abstract part def → toaster#9 / OpenSysML#595
  attribute :>>      → toaster#10 / OpenSysML#596
  require constraint → toaster#11 / OpenSysML#597
  assert satisfy     → toaster#12 / OpenSysML#598
  allocate           → toaster#13 / OpenSysML#599
```

### 0b. `sysml-v2-toaster-model` — add construction cell patterns

Add a "Construction cell patterns" section with Pattern A and Pattern B verbatim (from this plan).
Add TOASTER_INCREMENT convention including the Pattern A/B distinction. Note which constructs
use Pattern A vs Pattern B.

| Construct | Pattern | Chapter/Notebook |
|---|---|---|
| abstract part def | B (gap — toaster#9) | Ch1/nb01 |
| part def + attribute | A | Ch1/nb02 |
| :> specialization | A | Ch1/nb03 |
| part usage (composition) | A | Ch1/nb04 |
| requirement def + require constraint | B (gap — toaster#11) | Ch2/nb01 |
| attribute :>> override | B (gap — toaster#10) | Ch2/nb02 |
| requirement usage + assert satisfy | B (gap — toaster#12) | Ch3/nb01 |
| calc def | A | Ch3/nb02 |
| action def | A | Ch4/nb01 |
| item def | A | Ch4/nb02 |
| allocate | B (gap — toaster#13) | Ch5/nb02 |
| flow | A (if probe confirms) or B | Ch5/nb03 |
| state | A (if probe confirms) or B | Ch7/nb02 |

### 0c. `toaster-recipe` — update cell-02 description

Current: "Model increment — full cumulative SysML string (SA-2); conn.load_from_content(…); assert model.ok"

Replace with:
```
| 2 | Code | **Model increment** — two-phase: (1) declare the increment (Pattern A: Editor API
returning full model; Pattern B: SysML string for gap constructs); assign to TOASTER_INCREMENT;
print as reflection. (2) load full chapter cumulative from models/chXX-cumulative.sysml;
assert model.ok. Not all cell-02s have TOASTER_INCREMENT — see scope table. |
```

A6 checklist update: "TOASTER_INCREMENT is assigned and printed in cell-02 of construct-introducing
notebooks (13 total — see scope table). Judgment, depth, navigation, analysis, and param-sweep
notebooks do not assign TOASTER_INCREMENT."

### 0d. `tutorial-style-guide` — add construction cell rules

Append to code style section:
```
Construction cells (cell-02, construct-introducing notebooks only):
- TOASTER_INCREMENT is the required variable name.
  Pattern A: full model after editor.apply(). Pattern B: new SysML fragment only.
- Print TOASTER_INCREMENT immediately after assignment — this IS the reflection.
- For Pattern A: base = model state immediately before this notebook's declarations.
- For Pattern B: state the gap issue number in a comment above the string.
- conn.close() at the end of the last code cell (cell-04), never inside cell-02.
```

---

## Phase 0e — Probe `flow` and `state` Editor API support — COMPLETE (2026-09-25)

**Results:**

| Construct | Probe result | Pattern | DEFERRED entry |
|---|---|---|---|
| `flow X.port to Y.port` | `IllegalMemberKindError kind "flow"` | **B** | D-009 / toaster#14 |
| `state def Cycle` (bare) | Succeeds — adds `state def Cycle;` | A (bare only) | — |
| `state usage` (sub-state) | `IllegalMemberKindError kind "state usage"` | **B** | D-010 / toaster#15 |
| `transition` usage | `IllegalMemberKindError kind "transition"` | **B** | D-010 / toaster#15 |

**Conclusion:**
- Ch5/nb03 (`flow`): Pattern B — gap D-009 confirmed.
- Ch7/nb02 (full state machine): Pattern B — bare `state def` via Pattern A is insufficient; the tutorial
  construct needs sub-states + transitions, which are both gaps (D-010).

Editor method list (from `dir(editor)`): `add_assoc, add_attribute, add_attribute_def, add_behavior,
add_calc, add_calc_def, add_class, add_classifier, add_datatype, add_feature, add_function,
add_interaction, add_item, add_item_def, add_member, add_metaclass, add_package, add_part,
add_part_def, add_port, add_port_def, add_predicate, add_struct, applied, apply, delete, move,
operations, rename, set_value`

No `add_state`, `add_flow`, `add_transition` exist. All 7 gap constructs now confirmed.

**Updated: all 13 construct cells now have a confirmed Pattern assignment. Phase 1 may proceed.**

---

## Phase 1 — Test infrastructure (SECOND — defines acceptance criteria)

All checkpoint infrastructure must exist before any notebook is modified. This is TDD.

### 1a. `pyproject.toml` — add checkpoint marker

```toml
[tool.pytest.ini_options]
markers = [
  "checkpoint: verify notebook construction cells are consistent with committed fixtures",
]
addopts = "-m 'not checkpoint'"
```

`pytest` (default): skips checkpoint tests — learners who fork and edit won't see confusing
fixture-mismatch failures.  
`pytest -m checkpoint` (CI): runs checkpoint tests explicitly.

### 1b. `tests/test_model_checkpoints.py` — fixture consistency tests

```python
import subprocess
import pytest

@pytest.mark.checkpoint
def test_fixture_consistency():
    """Run construction cells and verify fixtures are consistent."""
    result = subprocess.run(
        ["python", "scripts/check_construction.py", "--check"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Construction inconsistency:\n{result.stdout}\n{result.stderr}"

@pytest.mark.checkpoint
@pytest.mark.parametrize("chapter", range(1, 9))
def test_chapter_fixture(chapter):
    result = subprocess.run(
        ["python", "scripts/check_construction.py", "--check", f"--chapter={chapter}"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
```

### 1c. `scripts/check_construction.py` — verification script

**Revised scope (B-ACE-3 fix):** The script VERIFIES consistency between notebook construction
cells and committed fixtures. It does NOT reconstruct cumulative files from scratch by
concatenating TOASTER_INCREMENT values (which is impossible given Pattern A/B incompatibility).

**Design:**

For each Chapter 1–8, for each construct-introducing notebook (in order):
1. Parse the notebook JSON and extract cell-02 source.
2. Identify whether it is Pattern A (`editor.apply()` path) or Pattern B (string fragment path)
   by checking for `editor.` in the source.
3. Execute cell-02 using `exec()` in a prepared namespace (conn already open, correct CWD,
   base model loaded). Capture `TOASTER_INCREMENT`.
4. Validation:
   - **Pattern A**: load `TOASTER_INCREMENT` via `conn.load_from_content()`; assert `model.ok`.
     For the LAST Pattern A notebook in the chapter: compare against the committed
     `models/chXX-cumulative.sysml` (normalize whitespace before comparing).
   - **Pattern B**: wrap `TOASTER_INCREMENT` in a minimal package with standard imports;
     load via `conn.load_from_content()`; assert `model.ok` (validates the fragment parses).
5. Exit 1 and report any failures.

`--check` mode is the only mode — the script never writes to `models/`. The `// GENERATED FIXTURE`
header on cumulative files is the signal that they SHOULD be kept in sync by running this script,
but the script itself is read-only.

**Note on `regenerate` mode (deferred):** A future enhancement could add `--regenerate` to
actually write updated cumulative files using the last Pattern A TOASTER_INCREMENT per chapter.
Deferred until after Phase 5 confirms the construction cells are stable.

### 1d. Update cumulative file headers

Add to the top of each `models/chXX-cumulative.sysml`:
```
// GENERATED FIXTURE — do not edit directly.
// Run: python scripts/check_construction.py --check   (to verify)
// Source: notebook cell-02 TOASTER_INCREMENT in each chapter's construct-introducing notebooks.
```

### 1e. Commit infrastructure (before pilot)

Commit: `test: checkpoint test infrastructure + fixture headers`

Files: `pyproject.toml`, `tests/test_model_checkpoints.py`, `scripts/check_construction.py`,
all 8 `models/chXX-cumulative.sysml` headers.

---

## Phase 2 — Pilot (one notebook end-to-end before rollout)

**Pilot target:** Ch3/nb02 (`calc def DeliveredEnergy`) — Editor API supports this construct;
it has a clear reflection (full model including DeliveredEnergy); existing tests exercise it;
ch02-cumulative.sysml is the natural base.

### 2a. Implement construction cell in Ch3/nb02

Apply Pattern A to cell-02. Load ch02-cumulative.sysml as base. Add `editor.add_calc_def(...)`.
Assign `TOASTER_INCREMENT = str(editor.apply())`. Print. Keep existing cells 3–7 intact.

### 2b. Verify checkpoint test passes

```
pytest -m checkpoint tests/test_model_checkpoints.py::test_chapter_fixture[3]
```

Must be GREEN before proceeding.

### 2c. ACE or Z review of pilot

The pilot's printed `TOASTER_INCREMENT` is the first example of the reflection pattern.
Confirm the output is pedagogically clear (shows the full canonical model — is that too much?
Should it print only the new section? Resolve before rolling out to all 13 notebooks).

If the full model is too verbose: switch to printing only the new member text (extracted as
`str(editor.apply())` minus the base). This is a judgment call that must be made here.

---

## Phase 3 — Code (scripts finalization + any src/toaster/ changes)

Phase 3 exists primarily as a verification gate after the pilot:

- Confirm `scripts/check_construction.py` works correctly for both Pattern A and B based on
  the pilot result.
- Review whether any `src/toaster/` module changes are needed (none expected — the Editor API
  is called directly from notebook cells).
- If Phase 2c reveals the full-model reflection is too verbose, implement the extraction approach
  here before rolling out to 13 notebooks.

If Phase 2 resolves cleanly with no code changes needed, Phase 3 is a sign-off checkpoint only.

---

## Phase 4 — Notebook rollout (13 notebooks, chapter by chapter)

Apply construction cells in this order. Within each chapter, do all notebooks before moving on.
After each chapter batch, run `pytest -m checkpoint --chapter=N` before starting Ch(N+1).

| Batch | Notebook | Construct | Pattern | Gate |
|---|---|---|---|---|
| Ch1 | nb01 | abstract part def | B | — |
| Ch1 | nb02 | part def + attribute | A | base = Ch1/nb01 fragment in preamble |
| Ch1 | nb03 | :> specialization | A | base = Ch1/nb02 TOASTER_INCREMENT |
| Ch1 | nb04 | part usage (composition) | A | base = Ch1/nb03 TOASTER_INCREMENT |
| checkpoint | | | | `pytest -m checkpoint --chapter=1` GREEN |
| Ch2 | nb01 | requirement def + require constraint | B | — |
| Ch2 | nb02 | attribute :>> override | B | — |
| checkpoint | | | | `pytest -m checkpoint --chapter=2` GREEN |
| Ch3 | nb01 | requirement usage + assert satisfy | B | — |
| Ch3 | nb02 | calc def | A | **already done in pilot** |
| checkpoint | | | | `pytest -m checkpoint --chapter=3` GREEN |
| Ch4 | nb01 | action def | A | base = ch03-cumulative.sysml |
| Ch4 | nb02 | item def | A | base = Ch4/nb01 TOASTER_INCREMENT |
| checkpoint | | | | `pytest -m checkpoint --chapter=4` GREEN |
| Ch5 | nb02 | allocate | B | — |
| Ch5 | nb03 | flow | B | D-009 confirmed 2026-09-25 |
| checkpoint | | | | `pytest -m checkpoint --chapter=5` GREEN |
| Ch7 | nb02 | state machine | B | D-010 confirmed 2026-09-25 |
| checkpoint | | | | `pytest -m checkpoint --chapter=7` GREEN |

**Ch6, Ch8–Ch10:** No construction cells. Do not modify.

---

## Phase 5 — Simulated user testing + ACE synthesis + remediations (LAST)

Run the full A9 simulated learner battery after ALL 13 construction cells are in place.

### 5a. Test battery

Three persona agents per batch. Cover all 10 chapters.
- L-Novice: Ch1–Ch3 (construction cells are most visible here)
- L-SE Practitioner: Ch4–Ch6 + Ch9
- L-Returning Learner: Ch7–Ch8 + Ch10

**Focus question for this batch:** "Does cell-02's construction code make the declarative
nature of SysML v2 visible? Is the reflection output (printed TOASTER_INCREMENT) meaningful?
Does the two-phase structure (construct then load) cause confusion or add clarity?"

### 5b. ACE synthesis

ACE handles corroborated blocking issues inline. Non-blocking findings logged.
Any finding that affects the construction cell pattern across multiple chapters escalates to Z
before ACE attempts a fix.

### 5c. Remediations

Apply fixes. If remediations touch more than 3 notebooks, re-run the user test battery on the
affected chapters before closing.

### 5d. DL entry

Log as DL-012 (or whichever number follows after any interim DL entries).

---

## Acceptance criteria (plan complete when ALL are met)

- [ ] DL-011 logged (before Phase 0)
- [ ] All 4 skills updated (Phase 0a–d)
- [ ] Phase 0e probe complete; flow and state constructs confirmed as Pattern A or B; skill updated
- [ ] `pyproject.toml` has `checkpoint` marker + `addopts` (Phase 1a)
- [ ] `tests/test_model_checkpoints.py` exists with `@pytest.mark.checkpoint` tests (Phase 1b)
- [ ] `scripts/check_construction.py` exists; `--check` mode exits 0 on clean repo (Phase 1c)
- [ ] All `models/chXX-cumulative.sysml` have `// GENERATED FIXTURE` header (Phase 1d)
- [ ] Pilot (Ch3/nb02) checkpoint test GREEN (Phase 2)
- [ ] Phase 2c review complete; reflection verbosity resolved (Phase 2c)
- [ ] All 13 construct-introducing notebooks have Pattern A or B in cell-02 (Phase 4)
- [ ] Per-chapter checkpoint gates all GREEN (Phase 4)
- [ ] Simulated user test battery complete; remediations applied (Phase 5)
- [ ] DL-012 logged (Phase 5)

---

## What Z asked for and what was added

Z specified: skill updates → tests → code → notebooks → user testing + ACE

Added steps not in Z's original list:
1. **Phase 0a–0d are separate skill sub-steps** — each skill has a specific section to update
2. **Phase 0e — flow/state Editor API probes** — explicit GATE before Ch5/nb03 and Ch7/nb02;
   do not assume Pattern A or B for these two constructs without probing
3. **TOASTER_INCREMENT Pattern A/B distinction** — Pattern A = full model; Pattern B = fragment;
   this distinction affects the regenerate script design and must be in skills before rollout
4. **Pilot step (Phase 2)** — test the pattern end-to-end on one notebook before rolling out
5. **Phase 2c reflection verbosity review** — `editor.apply()` returns the full model which may
   be long; decide before rollout whether to print the full model or extract only the new member
6. **Phase 3 as sign-off gate** — not a heavy code phase; exists to catch Phase 2c fallout
7. **Ch1 base model convention (B-ACE-4)** — Ch1 has no ch00-cumulative; Pattern A cells chain
   on the previous notebook's TOASTER_INCREMENT within the chapter
8. **`scripts/check_construction.py` scope narrowed (B-ACE-3)** — verifies consistency only;
   does not reconstruct from scratch (impossible given Pattern A/B TOASTER_INCREMENT mismatch)
9. **Per-chapter checkpoint gates explicitly in Phase 4 table** — not just a note; listed as
   explicit BLOCKED/checkpoint rows that agents cannot skip

## ACE review findings log (all handled by ACE, 2026-09-25)

| ID | Severity | Finding | Fix |
|---|---|---|---|
| B-ACE-1 | Blocking | Phase 0b table listed `attribute :>>` as Ch2/nb01; it is Ch2/nb02 | Fixed in Phase 0b table |
| B-ACE-2 | Blocking | Scope said 18 notebooks; Phase 4 table implied 13 | Fixed scope section |
| B-ACE-3 | Blocking | `editor.apply()` returns full model, not new member (probed); regenerate script design invalid | Revised TOASTER_INCREMENT convention + script scope |
| B-ACE-4 | Blocking | Ch1 base model undefined; no ch00-cumulative | Added convention in Pattern A section |
| N-ACE-1 | Minor | Ch5/nb01 mislabeled "analysis"; it is navigation | Fixed in scope table |
| N-ACE-2 | Minor | Phase 3 was hollow; no clear purpose | Clarified as sign-off gate |
| N-ACE-3 | Minor | Ch7/nb01 in scope header but excluded in Phase 4 | Fixed scope section |
| N-ACE-4 | Minor | flow/state probes had no explicit gate | Added Phase 0e as explicit GATE |
| N-ACE-5 | Minor | DL-011 positioned mid-Phase-1; should precede all phases | Moved to ordering note before Phase 0 |
