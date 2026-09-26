# Declarative Construction Architecture — Implementation Plan

**Status:** APPROVED — pending DL entry  
**Date:** 2026-09-25  
**Triggered by:** Z's direction: "the notebooks themselves are the code performing the build"  
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

**Notebooks with construction cells (cell-02 updated):** 18  
  Ch1: nb01–nb04 (4); Ch2: nb01–nb02 (2); Ch3: nb01–nb02 (2); Ch4: nb01–nb02 (2);  
  Ch5: nb01–nb03 (3); Ch7: nb01–nb02 (2); Ch8: nb01–nb02 (2) — nb03 is analysis

**Notebooks with no construction cell needed:**  
  Ch2/nb03, Ch3/nb03, Ch4/nb03, Ch6/nb01–nb03 (judgment + depth — no new constructs),  
  Ch8/nb03 (stale detection — analysis), Ch9/nb01–nb03, Ch10/nb01–nb03

**5 gap construct notebooks (already have notes; just need the print pattern added):**  
  Ch1/nb01 (abstract part def, toaster#9), Ch2/nb01 (require constraint, toaster#11),  
  Ch2/nb02 (attribute :>>, toaster#10), Ch3/nb01 (assert satisfy, toaster#12),  
  Ch5/nb02 (allocate, toaster#13)

---

## Cell-02 patterns

### Pattern A — Editor API construct

```python
from pathlib import Path
import opensysml
from toaster.report import format_diagnostics

conn = opensysml.connect(version="v0.9.0")

# Load base (previous chapter's cumulative) for construction
base = conn.load_from_content(
    Path("../../models/ch02-cumulative.sysml").read_text(), strict=False
)
assert base.ok

# Declare the increment via Editor API
editor = base.edit()
editor.add_calc_def(
    owner="ToasterDemo",
    name="DeliveredEnergy",
    inputs=[("power", "ISQ::PowerValue"),
            ("duration", "ISQ::DurationValue"),
            ("efficiency", "MeasurementReferences::DimensionOneValue")],
    return_type="ISQ::EnergyValue",
    expression="power * duration * efficiency",
)
increment = editor.apply()
TOASTER_INCREMENT = str(increment)   # exportable for regenerate_fixtures.py
print(TOASTER_INCREMENT)             # reflection: validated canonical SysML from the service

# Load full cumulative for subsequent cells
source = Path("../../models/ch03-cumulative.sysml").read_text()
model = conn.load_from_content(source, strict=False)
assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
```

### Pattern B — Gap construct (Editor API not yet supported)

```python
from pathlib import Path
import opensysml
from toaster.report import format_diagnostics

conn = opensysml.connect(version="v0.9.0")

# Declare the increment as SysML notation
# Editor API does not yet support the abstract modifier — see toaster#9 / OpenSysML#595
TOASTER_INCREMENT = """\
abstract part def ToastingSystem {
    doc /* The top-level concept: any system that converts electrical energy
         into thermal energy for food preparation. */
}
"""
print(TOASTER_INCREMENT)   # reflection: the declaration itself

# Load full cumulative for subsequent cells
source = Path("../../models/ch01-cumulative.sysml").read_text()
model = conn.load_from_content(source, strict=False)
assert model.ok, f"Model failed: {format_diagnostics(model.diagnostics)}"
```

**Key convention:** `TOASTER_INCREMENT` is the machine-readable export used by
`regenerate_fixtures.py`. Every construct-introducing cell-02 must assign to it.

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

# Item / state (when confirmed)
editor.add_item_def(owner, name, ...)
editor.add_member(owner, kind="state def", name=...)

editor.apply() → EditResult
str(result)  # canonical validated SysML text from the gRPC service

Editor single-use rule: editor is bound to one model hash.
After editor.apply(), must call conn.load_from_content(str(result)) before editing further.

Gap constructs — do NOT attempt these kinds in add_member(); use Pattern B instead:
  abstract part def → toaster#9 / OpenSysML#595
  attribute :>>      → toaster#10 / OpenSysML#596
  require constraint → toaster#11 / OpenSysML#597
  assert satisfy     → toaster#12 / OpenSysML#598
  allocate           → toaster#13 / OpenSysML#599
```

### 0b. `sysml-v2-toaster-model` — add construction cell patterns

Add a "Construction cell patterns" section with Pattern A and Pattern B verbatim (from this plan).
Add `TOASTER_INCREMENT` convention. Note which constructs use Pattern A vs Pattern B.

| Construct | Pattern | Chapter |
|---|---|---|
| abstract part def | B (gap — toaster#9) | Ch1/nb01 |
| part def + attribute | A | Ch1/nb02 |
| :> specialization | A | Ch1/nb03 |
| part usage (composition) | A | Ch1/nb04 |
| attribute :>> | B (gap — toaster#10) | Ch2/nb01 |
| requirement def + require constraint | B (gap — toaster#11) | Ch2/nb01 |
| requirement usage + assert satisfy | B (gap — toaster#12) | Ch3/nb01 |
| calc def | A | Ch3/nb02 |
| action def | A | Ch4/nb01 |
| item def | A | Ch4/nb02 |
| allocate | B (gap — toaster#13) | Ch5/nb02 |
| flow | A (if supported) or B | Ch5/nb03 |
| state | A (if supported) or B | Ch7/nb02 |

### 0c. `toaster-recipe` — update cell-02 description

Current: "Model increment — full cumulative SysML string (SA-2); conn.load_from_content(…); assert model.ok"

Replace with:
```
| 2 | Code | **Model increment** — two-phase: (1) declare the increment (Pattern A: Editor API;
Pattern B: SysML string for gap constructs); assign to TOASTER_INCREMENT; print as reflection.
(2) load full cumulative from models/chXX-cumulative.sysml; assert model.ok. |
```

A6 checklist update: "TOASTER_INCREMENT is assigned and printed in cell-02 (construct-introducing
notebooks only); not required in judgment, depth, or analysis notebooks."

### 0d. `tutorial-style-guide` — add construction cell rules

Append to code style section:
```
Construction cells (cell-02, construct-introducing notebooks):
- TOASTER_INCREMENT is the required variable name for the new declaration text.
- Print TOASTER_INCREMENT immediately after it is assigned — this IS the reflection.
- For Pattern A: base model loads from the PREVIOUS chapter's cumulative (not current).
- For Pattern B: state the gap issue number in a comment above the string.
- conn.close() remains at the end of the last code cell (cell-04 or equivalent), not inside cell-02.
```

---

## Phase 1 — Test infrastructure (SECOND — defines acceptance criteria)

All checkpoint infrastructure must exist before any notebook is modified. This is TDD.

### 1a. `pyproject.toml` — add checkpoint marker

```toml
[tool.pytest.ini_options]
markers = [
  "checkpoint: compare notebook-constructed increments to committed fixtures",
]
addopts = "-m 'not checkpoint'"
```

`pytest` (default): skips checkpoint tests. Learners who fork and edit their notebooks won't see
confusing fixture-mismatch failures.  
`pytest -m checkpoint` (CI): runs checkpoint tests explicitly.

### 1b. `tests/test_model_checkpoints.py` — fixture comparison tests

```python
import subprocess
import pytest

@pytest.mark.checkpoint
def test_fixture_freshness():
    """Regenerate cumulative files in memory and assert no drift from committed versions."""
    result = subprocess.run(
        ["python", "scripts/regenerate_fixtures.py", "--check"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Fixture drift:\n{result.stdout}\n{result.stderr}"
```

Additional tests (one per chapter) for finer-grained CI output:
```python
@pytest.mark.checkpoint
@pytest.mark.parametrize("chapter", range(1, 9))
def test_chapter_fixture(chapter):
    result = subprocess.run(
        ["python", "scripts/regenerate_fixtures.py", "--check", f"--chapter={chapter}"],
        ...
    )
    assert result.returncode == 0
```

### 1c. `scripts/regenerate_fixtures.py` — extraction + regeneration script

**Design:** For each notebook in Ch1–Ch8 (in chapter/notebook order):
1. Parse the notebook JSON and find cell-02.
2. Extract the cell source and execute it in a restricted kernel (no notebook runtime needed —
   just `exec()` in a dict namespace; imports and `conn` must be set up first).
3. Capture `TOASTER_INCREMENT` from the namespace.
4. Accumulate: `ch(N)_text = ch(N-1)_text + "\n" + TOASTER_INCREMENT`
5. Wrap in `package ToasterDemo { ... }` and write to `models/chXX-cumulative.sysml`.

`--check` mode: compare generated content to committed files; exit 1 if any differ.

The script header that every notebook cell-02 depends on (the package wrapper, imports) is defined
once in the script and injected before the notebook cell code runs.

### 1d. Update cumulative file headers

Add to the top of each `models/chXX-cumulative.sysml` after regeneration:
```
// GENERATED FIXTURE — do not edit directly.
// Run: python scripts/regenerate_fixtures.py
// Source: notebook cell-02 TOASTER_INCREMENT in each chapter's notebooks (in order).
```

### 1e. DL entry for the architectural decision

Log DL-011 in `decisions/log.md` before Phase 2 begins:
- Path: Escalated to Z / approved
- Decision: declarative construction architecture (this plan)
- Files: this plan document + all phases
- Rationale: Z's "notebooks are the construction code" direction; SysML v2 is declarative

---

## Phase 2 — Pilot (one notebook end-to-end before rollout)

**Pilot target:** Ch3/nb02 (`calc def DeliveredEnergy`) — Editor API supports this construct;
it has a clear, verifiable reflection (canonical calc def SysML); existing tests exercise it.

### 2a. Implement construction cell in Ch3/nb02

Apply Pattern A to cell-02. Assign `TOASTER_INCREMENT`. Print reflection via `editor.apply()`.
Keep existing cells 3–7 intact.

### 2b. Verify checkpoint test passes

```
pytest -m checkpoint tests/test_model_checkpoints.py::test_chapter_fixture[3]
```

Must be GREEN before proceeding.

### 2c. Verify regenerate_fixtures works

```
python scripts/regenerate_fixtures.py --chapter=3
```

`models/ch03-cumulative.sysml` should regenerate to match the committed file. If it diverges,
investigate before proceeding to rollout.

### 2d. ACE or Z review of pilot

The pilot output (printed `TOASTER_INCREMENT` in cell-02) is the first example of the
"reflection" pattern. Confirm it is pedagogically clear before rolling out to all 18 notebooks.
If the reflection output is opaque or verbose, adjust before rollout.

---

## Phase 3 — Code (scripts + any src/toaster/ changes)

### 3a. `scripts/regenerate_fixtures.py` — full implementation

Fully implement based on the design in Phase 1c. Pilot in Phase 2 will have already validated
the core extraction logic for one notebook.

### 3b. `src/toaster/` — minimal changes expected

Review after pilot. The Editor API is called directly from notebook cells; no new `src/toaster/`
module is expected. If any utility is needed (e.g., a helper to set up the base model for
construction), add it here — but do not add until the pilot reveals a concrete need.

---

## Phase 4 — Notebook rollout (18 notebooks, chapter by chapter)

Apply construction cells in this order. Within each chapter, do all notebooks before moving on —
the cumulative files build on each other.

| Batch | Notebooks | Constructs | Pattern |
|---|---|---|---|
| Ch1 | nb01 | abstract part def | B (gap note already added) |
| Ch1 | nb02 | part def + attribute | A |
| Ch1 | nb03 | :> specialization | A |
| Ch1 | nb04 | part usage (composition) | A |
| Ch2 | nb01 | requirement def + require constraint | B (gap note already added) |
| Ch2 | nb02 | attribute :>> override | B (gap note already added) |
| Ch3 | nb01 | requirement usage + assert satisfy | B (gap note already added) |
| Ch3 | nb02 | calc def | A — **already done in pilot** |
| Ch4 | nb01 | action def | A |
| Ch4 | nb02 | item def | A |
| Ch5 | nb01 | concept selection (model.find nav) | no TOASTER_INCREMENT — analysis |
| Ch5 | nb02 | allocate | B (gap note already added) |
| Ch5 | nb03 | flow | A or B — probe first |
| Ch6 | nb01–nb03 | depth (no new constructs) | no TOASTER_INCREMENT |
| Ch7 | nb01 | sympy binding (no new SysML) | no TOASTER_INCREMENT |
| Ch7 | nb02 | state machine | A or B — probe first |
| Ch7 | nb03 | param sweep | no TOASTER_INCREMENT |
| Ch8 | nb01 | invariant check | no TOASTER_INCREMENT |
| Ch8 | nb02 | violation witness | no TOASTER_INCREMENT |

**Ch9–Ch10:** No construction cells. These query the finished model. Do not modify.

**After each chapter batch:** run `pytest -m checkpoint --chapter=N` before starting Ch(N+1).

**Two constructs to probe before rolling out:**
- `flow X.port to Y.port` (Ch5/nb03): check if `editor.add_member(kind="flow", ...)` works
- `state def` + `transition` (Ch7/nb02): check if `editor.add_member(kind="state def", ...)` works

Probe by running a minimal test in an interactive session. Document results in DEFERRED.md
(add D-009/D-010 if gaps) or confirm Pattern A in the skill if the Editor supports them.

---

## Phase 5 — Simulated user testing + ACE synthesis + remediations (LAST)

Run the full A9 simulated learner battery after ALL notebook construction cells are in place.
This is the same protocol used in DL-003 through DL-010.

### 5a. Test battery

Three persona agents per batch. Cover all 10 chapters. Suggested assignments:
- L-Novice: Ch1–Ch3 (construction cells are most visible here)
- L-SE Practitioner: Ch4–Ch6 + Ch9
- L-Returning Learner: Ch7–Ch8 + Ch10

Focus question for this batch: "Does the construction cell (cell-02) make the declarative
nature of SysML v2 visible? Is the reflection output (printed TOASTER_INCREMENT) meaningful?
Does the two-phase cell-02 (construct then load) cause confusion?"

### 5b. ACE synthesis

ACE handles corroborated blocking issues inline (per DL-00x protocol). Non-blocking findings
logged. Any finding that affects the construction cell pattern across multiple chapters escalates
to Z before ACE attempts a fix.

### 5c. Remediations

Apply fixes. If remediations touch more than 3 notebooks, re-run the user test battery on the
affected chapters before closing.

### 5d. DL entry

Log the checkpoint as DL-012 (or whichever number follows).

---

## Acceptance criteria (plan complete when ALL are met)

- [ ] All 4 skills updated (Phase 0)
- [ ] `pyproject.toml` has `checkpoint` marker + `addopts` (Phase 1a)
- [ ] `tests/test_model_checkpoints.py` exists with `@pytest.mark.checkpoint` tests (Phase 1b)
- [ ] `scripts/regenerate_fixtures.py` exists and `--check` mode exits 0 on clean repo (Phase 1c)
- [ ] All `models/chXX-cumulative.sysml` have `// GENERATED FIXTURE` header (Phase 1d)
- [ ] DL-011 logged (Phase 1e)
- [ ] Pilot (Ch3/nb02) checkpoint test GREEN (Phase 2)
- [ ] All 18 construct-introducing notebooks have Pattern A or B in cell-02 (Phase 4)
- [ ] `TOASTER_INCREMENT` assigned and printed in each construction cell (Phase 4)
- [ ] `pytest -m checkpoint` GREEN for Ch1–Ch8 (Phase 4)
- [ ] Simulated user test battery complete, remediations applied (Phase 5)
- [ ] DL-012 logged (Phase 5)

---

## What Z asked for and what was added

Z specified: skill updates → tests → code → notebooks → user testing + ACE

Added steps not in Z's original list:
1. **Phase 0a–0d are separate skill sub-steps** — each skill has a specific target section to update
2. **`TOASTER_INCREMENT` variable convention** — required for `regenerate_fixtures.py` to work;
   must be established in skills (0b) before notebooks (Phase 4)
3. **Pilot step (Phase 2)** — test the pattern end-to-end on one notebook before rolling out to 18
4. **DL-011 entry (Phase 1e)** — document the architectural decision before implementation begins
5. **`flow` and `state` Editor API probes (Phase 4 note)** — two constructs not yet tested; probe
   before assuming Pattern A or B
6. **Ch9–Ch10 explicitly excluded** — analysis-only notebooks; no construction cells needed
7. **Ch5/nb01 and Ch6/nb01–nb03 explicitly excluded** — navigation-only or depth-only notebooks
8. **Per-chapter checkpoint gates** (after each batch, run checkpoint before moving on)
9. **Connection lifecycle detail** — editor single-use rule documented in Pattern A; base model
   loads from previous chapter, full cumulative loads at the end
