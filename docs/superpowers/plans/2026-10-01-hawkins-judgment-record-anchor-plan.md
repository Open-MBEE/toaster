# Hawkins Judgment Record Anchor — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. In THIS repo, "subagent-driven" means dispatching through the existing `builder`/`reviewer` agent roles and `orchestrator-protocol`'s "Plan-driven non-chapter work" mechanism (one work contract per task below, builder in a private worktree, reviewer on a different model, orchestrator integrates), not a generic subagent loop — see that skill for the work-contract template and `decisions/task-states.md` for states.

**Goal:** Give every `ReviewRecord` a real, bidirectional, checkable anchor to the SysML model it judges — a new `subject_ref` field in Python paired with a new `metadata def ReviewRecordRef` tag in the model — retiring the recurring DL-075 seam escalation by giving judgment-record notebooks a concrete bridged connection to narrate instead of a choice between competing readings.

**Architecture:** Additive schema change (`subject_ref: str`) plus a cross-checkable model-side tag (SysML `metadata def`/`about`), joined by one new query helper (`get_review_record_refs`) built on the existing `to_api_json()` pattern. Every existing judgment-record notebook across Ch2–Ch10 is retrofitted: original-authoring records get a real `subject_ref` value and a matching model tag; reconstructions/ledgers carry the value forward in Python only; deliberate negative controls get a resolvable `subject_ref` added where needed so they keep demonstrating exactly one intended validation error.

**Tech Stack:** Python 3 dataclasses, OpenSysML v0.9.0 (`opensysml` package), pytest, Jupyter notebooks (`.ipynb`), SysML v2 text (`models/*.sysml`).

**Spec:** [`docs/superpowers/specs/2026-10-01-hawkins-judgment-record-anchor-design.md`](../specs/2026-10-01-hawkins-judgment-record-anchor-design.md) — this plan implements its Design sections 1–6. Executors should read both; where this plan gives an exact value or snippet, it is this plan's own refinement of the spec's stated intent (the spec itself flags per-record `subject_ref` values as "intent, not final strings" — this plan fixes them).

## Global Constraints

- OpenSysML version is pinned at `v0.9.0` throughout (`opensysml.connect(version="v0.9.0")`) — do not bump it as a side effect of this work.
- `record_kind` stays `"worked_example"` on every record in this tutorial (SA-7); `disposition` stays `"pending"`; never introduce `"accepted"`.
- `subject_ref` values must be real, `model.find()`-resolvable qualified names (verified empirically per task below), never invented placeholders.
- The `about` form for every `ReviewRecordRef` usage is the **explicit** form (`metadata x : ReviewRecordRef about <target> { ... }`), never the implicit nested form — confirmed in the spec's own probe (Verification item 6) and reconfirmed in this plan's own probe (Task 1) that only the explicit form populates `annotatedElement`.
- Every cumulative model file touched must still satisfy `model.ok == True` with zero diagnostics, and `uv run python scripts/check_construction.py --check` must exit 0 after every task that touches a construct-introducing notebook or a `models/*.sysml` file.
- No co-author trailers on commits (standing repo convention).
- Package name in every chapter's model is `ToasterDemo` — do not re-derive or guess a different root package.

## Review Focus

- **A judgment-record notebook that calls `validate_record(record)` without passing `model=`** must keep working exactly as before (the resolution and cross-representation checks are both gated on `model is not None`) — a reasonable reader would expect adding an optional parameter not to break existing single-argument calls. Task 1's tests pin this.
- **A `subject_ref` that doesn't resolve in the model** (typo, renamed element, wrong chapter's qualified name) must produce a clear, specific error naming the bad reference, not a silent pass or a raw `AttributeError`/`KeyError` from `model.find()`. Task 1's tests pin this.
- **An `asserted_inference` record with a non-empty `premises` list and an empty `subject_ref`** must validate with **zero** `subject_ref`-related errors (the Hawkins-grounded exemption) — a careless required-ness implementation could easily make this always-required and silently break `AI-C10`. Task 1's tests pin this explicitly as a positive case, not just the negative "premises also empty" case.
- **A `ReviewRecordRef` tag whose `about` target doesn't match the Python record's own `subject_ref`** (the drift the cross-representation check exists to catch) must be *caught*, not silently ignored — a reasonable implementer, focused on getting the resolution check working, might skip wiring the cross-representation check all the way through. Task 1's tests pin this with a deliberately mismatched fixture.
- **A negative-control record in an already-shipped notebook** (`AI-BAD`, the empty-identifier `"broken"` record, `AS-BAD`, `AS-PLACEHOLDER`, `AI-C10-DRAFT`) must keep demonstrating *exactly* the one validation failure its own markdown names, not silently gain a second, unrelated `subject_ref` error as a side effect of this change — the single most likely regression in this whole plan, because it's easy to add the new required-ness rule and forget every place it has a new blast radius. Task 8 and the negative-control sub-steps of Tasks 6/7/9 pin this by asserting the exact error list, not just "non-empty."

---

## File Structure

| File | Responsibility |
|---|---|
| `src/toaster/evidence.py` | `ReviewRecord` dataclass, `validate_record`, `check_stale` — gains `subject_ref` and the three new validation rules. Modified, not split (stays one small file). |
| `src/toaster/query.py` | Gains `get_review_record_refs(model, index=None)`, following the existing `ApiIndex`-based pattern (`get_satisfy_relationships`, `find_allocations`). Modified, not split. |
| `tests/test_evidence.py` | New/extended unit tests for `validate_record`'s new rules (may not exist yet — create if absent, following the existing `tests/` layout and `conftest.py` fixtures if any). |
| `tests/test_query.py` | New/extended unit tests for `get_review_record_refs` (may not exist yet — create if absent, matching the convention of existing query tests, e.g. `tests/test_requirement_ties.py` or similar, for fixture style). |
| `models/ch02-cumulative.sysml` through `models/ch08-cumulative.sysml`, `models/ch10-cumulative.sysml` | Gain `metadata def ReviewRecordRef { attribute identifier : String; }` (once, carried forward from Ch2) plus one `metadata ... : ReviewRecordRef about <subject> { identifier = "..."; }` usage per original-authoring record, carried forward from each record's origin chapter. |
| `chapters/ch02-requirements/03-judgment-context.ipynb`, `ch03-measures/01-moe-definition.ipynb`, `ch03-measures/03-threshold-judgment.ipynb`, `ch04-functional-decomp/03-completeness-check.ipynb`, `ch06-recursive-decomp/02-second-level.ipynb`, `ch06-recursive-decomp/03-stopping-judgment.ipynb`, `ch08-checking/02-violation-witness.ipynb`, `ch10-traceability-signoff/01-traceability-graph.ipynb` | Each gains a new first construction-zone narration group ("what is being claimed, and what, specifically, it is about") covering `subject_ref` plus the new metadata-usage fragment, and a rewritten seam cell per the spec's DL-075 resolution. |
| `chapters/ch08-checking/03-revision-flow.ipynb`, `ch09-coverage-sufficiency/02-evidence-completeness.ipynb`, `ch09-coverage-sufficiency/03-stale-detection.ipynb`, `ch10-traceability-signoff/02-judgment-synthesis.ipynb`, `ch10-traceability-signoff/03-engineering-signoff.ipynb` | Reconstructions/ledgers carry `subject_ref` forward in Python only (no new model tag); negative controls get a resolvable `subject_ref` added where needed to keep demonstrating exactly one error. |
| `scripts/check_construction.py` | Gains new registry entries for the 5 judgment notebooks that previously had no `TOASTER_INCREMENT` (Ch2/nb03, Ch3/nb03, Ch4/nb03, Ch6/nb03, Ch8/nb02) now that each introduces a real SysML fragment; existing entries for Ch3/nb01, Ch6/nb02, Ch10/nb01 gain the new fragment inside their existing `TOASTER_INCREMENT`. |
| `.claude/skills/toaster-review-protocol/SKILL.md` | New `subject_ref` row in the required-fields table and example; new section citing SysML v2 §7.27.2. |
| `.claude/skills/toaster-recipe/SKILL.md` | Judgment-record construction-zone pattern gains its new first group; nothing else changes. |
| `glossary/definitions/hawkins.ttl` | Gains the `gl:refines` edge from the tutorial's `subject_ref`/`ReviewRecordRef` convention to the existing `glid:def-hawkins--assurance-claim-point` term. |
| `decisions/log.md` | New DL entry recording this work and closing DL-075. |

---

## Task 1: Schema — `subject_ref` and the three new validation rules

**Files:**
- Modify: `src/toaster/evidence.py` (whole file is 55 lines; this task rewrites the dataclass and `validate_record`)
- Modify/Create: `tests/test_evidence.py`

**Interfaces:**
- Consumes: nothing new (pure stdlib + the existing `ReviewRecord`/`hash_content`/`check_stale`).
- Produces: `ReviewRecord.subject_ref: str` (new field); `validate_record(r: ReviewRecord, model: Any | None = None) -> list[str]` (new optional second parameter — existing single-argument call sites must be unaffected). Task 2 and every later task that calls `validate_record(record, model)` or constructs a `ReviewRecord(..., subject_ref=...)` depends on this exact signature.

**Why `model_ref`, `content_hash`, `scope`, `criteria` also gain `= ""` defaults:** Python dataclasses require every field after the first field with a default to also have one. Inserting `subject_ref: str = ""` right after `claim` (matching the spec's own code snippet, for readability — the ACP-analog field reads naturally next to `claim`) means every field after it needs a default too. This is a mechanical side effect, not a design change: no caller in this repo currently constructs a `ReviewRecord` without passing `model_ref`/`content_hash`/`scope`/`criteria` explicitly (grep confirms this in Task 6's verification step), so no behavior changes for any existing record.

- [ ] **Step 1: Write the failing tests**

Create or extend `tests/test_evidence.py`:

```python
import pytest
import opensysml

from toaster.evidence import ReviewRecord, validate_record, hash_content


def _base_kwargs(**overrides):
    kwargs = dict(
        identifier="RR-TEST",
        kind="asserted_solution",
        claim="Test claim.",
        model_ref="models/test.sysml",
        content_hash="deadbeef",
        scope="test scope",
        criteria="test criteria",
        rationale="test rationale",
        counterevidence="test counterevidence",
    )
    kwargs.update(overrides)
    return kwargs


def test_subject_ref_defaults_empty():
    r = ReviewRecord(**_base_kwargs())
    assert r.subject_ref == ""


def test_subject_ref_required_for_asserted_context_without_model():
    r = ReviewRecord(**_base_kwargs(kind="asserted_context"))
    errors = validate_record(r)
    assert any("subject_ref" in e for e in errors)


def test_subject_ref_required_for_asserted_solution_without_model():
    r = ReviewRecord(**_base_kwargs(kind="asserted_solution"))
    errors = validate_record(r)
    assert any("subject_ref" in e for e in errors)


def test_subject_ref_may_be_empty_for_asserted_inference_with_premises():
    r = ReviewRecord(**_base_kwargs(kind="asserted_inference", premises=["some premise"]))
    errors = validate_record(r)
    assert not any("subject_ref" in e for e in errors)


def test_subject_ref_required_for_asserted_inference_without_premises():
    r = ReviewRecord(**_base_kwargs(kind="asserted_inference", premises=[]))
    errors = validate_record(r)
    assert any("subject_ref" in e for e in errors)
    # the pre-existing premises rule must still also fire -- this is a real double-error case
    assert any("premise" in e for e in errors)


def test_validate_record_without_model_arg_still_works():
    # Existing call sites across the repo call validate_record(record) with one argument.
    r = ReviewRecord(**_base_kwargs(subject_ref="ToasterDemo::anything"))
    errors = validate_record(r)  # no model= passed
    assert errors == []


_FIXTURE = """
package ToasterDemo {
    part def Widget {
        attribute flag : ScalarValues::Boolean;
    }
    part target : Widget;

    metadata def ReviewRecordRef {
        attribute identifier : ScalarValues::String;
    }

    metadata rrTag : ReviewRecordRef about target {
        identifier = "RR-TEST";
    }
}
"""


@pytest.fixture
def loaded_model():
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_FIXTURE, strict=False)
    assert model.ok, model.diagnostics
    yield model
    conn.close()


def test_subject_ref_resolution_check_passes_for_real_element(loaded_model):
    r = ReviewRecord(**_base_kwargs(subject_ref="ToasterDemo::target"))
    errors = validate_record(r, model=loaded_model)
    assert errors == []


def test_subject_ref_resolution_check_fails_for_unresolvable_element(loaded_model):
    r = ReviewRecord(**_base_kwargs(subject_ref="ToasterDemo::doesNotExist"))
    errors = validate_record(r, model=loaded_model)
    assert any("doesNotExist" in e for e in errors)


def test_cross_representation_check_passes_when_tag_matches(loaded_model):
    r = ReviewRecord(**_base_kwargs(identifier="RR-TEST", subject_ref="ToasterDemo::target"))
    errors = validate_record(r, model=loaded_model)
    assert errors == []


def test_cross_representation_check_fails_when_tag_disagrees(loaded_model):
    # Same identifier as the model's own rrTag, but a DIFFERENT subject_ref -- this is the
    # drift the cross-representation check exists to catch.
    r = ReviewRecord(**_base_kwargs(identifier="RR-TEST", subject_ref="ToasterDemo::Widget"))
    errors = validate_record(r, model=loaded_model)
    assert any("RR-TEST" in e and "Widget" in e for e in errors)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_evidence.py -v`
Expected: collection error or failures — `subject_ref` doesn't exist yet, `validate_record` doesn't accept `model=`.

- [ ] **Step 3: Implement**

Replace `src/toaster/evidence.py` in full:

```python
"""Engineering review records. WP-6 completes validate_record and check_stale."""

import hashlib
from dataclasses import dataclass, field
from typing import Any, Literal

from toaster.query import get_review_record_refs


@dataclass
class ReviewRecord:
    identifier: str
    kind: Literal["asserted_context", "asserted_inference", "asserted_solution"]
    claim: str
    subject_ref: str = ""
    model_ref: str = ""
    content_hash: str = ""
    scope: str = ""
    criteria: str = ""
    premises: list[str] = field(default_factory=list)
    assumption_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    rationale: str = ""
    counterevidence: str = ""
    residual_uncertainties: str = ""
    disposition: Literal["pending", "accepted", "rejected"] = "pending"
    dependency_freshness: Literal["current", "stale"] = "current"
    engineering_conclusion: Literal["supported", "refuted", "undetermined"] = "undetermined"
    record_kind: Literal["worked_example", "actual_review"] = "worked_example"


def hash_content(s: str) -> str:
    """Return SHA-256 hex digest of a string."""
    return hashlib.sha256(s.encode()).hexdigest()


def validate_record(r: ReviewRecord, model: Any | None = None) -> list[str]:
    """Return a list of field-level validation errors (empty = valid).

    `subject_ref` is this tutorial's narrowed analog of Hawkins' Assurance Claim Point
    (`toaster-review-protocol` SS, SysML v2 formal/2026-03-02 SS7.27.2): the one model
    element this specific judgment is about. Required for `asserted_context` and
    `asserted_solution`; for `asserted_inference` it may stay empty only when `premises`
    is non-empty (the pure cross-record synthesis case, e.g. `AI-C10`).

    When `model` is given and `subject_ref` is set, two further checks run: that
    `subject_ref` resolves in the model, and that any `ReviewRecordRef` metadata tag
    already present for this record's own `identifier` agrees with `subject_ref` (catching
    drift between the Python record and the model tag if they are ever edited independently).
    """
    errors = []
    if not r.identifier:
        errors.append("identifier is empty")
    if not r.claim:
        errors.append("claim is empty")
    if not r.rationale:
        errors.append("rationale is empty")
    if not r.counterevidence:
        errors.append("counterevidence is empty")
    if r.record_kind == "actual_review":
        errors.append("record_kind must be 'worked_example' in this tutorial (SA-7)")
    if r.kind == "asserted_inference" and not r.premises:
        errors.append("asserted_inference requires at least one premise (Hawkins §3.1)")

    if not r.subject_ref:
        if r.kind in ("asserted_context", "asserted_solution"):
            errors.append(
                f"subject_ref is empty (required for {r.kind})"
            )
        elif r.kind == "asserted_inference" and not r.premises:
            errors.append(
                "subject_ref is empty (required for asserted_inference with no premises)"
            )
    elif model is not None:
        if model.find(r.subject_ref) is None:
            errors.append(f"subject_ref {r.subject_ref!r} does not resolve in the model")
        else:
            tags = {t["identifier"]: t["annotated_element"] for t in get_review_record_refs(model)}
            tagged = tags.get(r.identifier)
            if tagged is not None and tagged != r.subject_ref:
                errors.append(
                    f"ReviewRecordRef tag for {r.identifier!r} is about {tagged!r}, "
                    f"but subject_ref is {r.subject_ref!r}"
                )
    return errors


def check_stale(r: ReviewRecord, current_content: str) -> bool:
    """Return True if the record's content_hash no longer matches current_content."""
    return r.content_hash != hash_content(current_content)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_evidence.py -v`
Expected: all PASS.

- [ ] **Step 5: Run the full existing suite to confirm no regression**

Run: `uv run pytest -q`
Expected: same pass count as before this task, plus the new tests — zero new failures. (If any existing test constructs a bare `ReviewRecord(...)` and calls `validate_record` with one argument, it must still pass unchanged — this is the Review Focus item above.)

- [ ] **Step 6: Commit**

```bash
git add src/toaster/evidence.py tests/test_evidence.py
git commit -m "Add subject_ref to ReviewRecord: the tutorial's Assurance Claim Point analog"
```

---

## Task 2: Query helper — `get_review_record_refs`

**Files:**
- Modify: `src/toaster/query.py`
- Modify/Create: `tests/test_query.py`

**Interfaces:**
- Consumes: `ApiIndex`, `_ref` (already defined in `query.py`).
- Produces: `get_review_record_refs(model: Any, index: ApiIndex | None = None) -> list[dict]`, each dict shaped `{"tag": <qualified name of the metadata usage>, "identifier": <str>, "annotated_element": <qualified name or None>}`. Task 1's `evidence.py` imports and calls this function — Task 1 and Task 2 can be built in parallel (neither's tests depend on the other being merged first), but both must land before any notebook task (3 onward) that calls `validate_record(record, model=...)` against a real `ReviewRecordRef` tag.

This task's exact JSON shapes were confirmed empirically against OpenSysML v0.9.0 (not assumed) with this probe, which any implementer should feel free to re-run to double-check before writing code:

```python
import json, warnings
import opensysml

conn = opensysml.connect(version="v0.9.0")
source = """
package P {
    part def Widget { attribute flag : ScalarValues::Boolean; }
    part target : Widget;
    metadata def ReviewRecordRef { attribute identifier : ScalarValues::String; }
    metadata tag1 : ReviewRecordRef about target { identifier = "X-1"; }
}
"""
model = conn.load_from_content(source, strict=False)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    content = json.loads(model.to_api_json().content)
for e in content:
    if e["@type"] in ("MetadataUsage", "ReferenceUsage", "LiteralString"):
        print(e["@type"], e.get("qualifiedName"), e.get("@id"), {k: v for k, v in e.items() if k in ("type", "annotatedElement", "value", "declaredName", "ownedMember")})
conn.close()
```

Confirmed shapes (do not re-derive, these are facts about v0.9.0, not design choices):
- A `MetadataUsage` element has `type: [{"@id": "<MetadataDefinition id>"}]` (a list) and `annotatedElement: [{"@id": "<target id>"}]` (**also a list**, even for one target — this tutorial's convention is exactly one target per tag, per the spec's "singular, not a list" decision, so take the first).
- The usage's own `identifier` attribute is itself a separate element reachable via the usage's `ownedMember` list: the member whose `declaredName == "identifier"` is a `ReferenceUsage` whose own `value` field is `{"@id": "<LiteralString id>"}`; that `LiteralString` element's own `value` field is the actual Python string (e.g. `"X-1"`).

- [ ] **Step 1: Write the failing test**

Create or extend `tests/test_query.py`:

```python
import opensysml

from toaster.query import get_review_record_refs


_FIXTURE_ONE_TAG = """
package ToasterDemo {
    part def Widget { attribute flag : ScalarValues::Boolean; }
    part target : Widget;
    metadata def ReviewRecordRef { attribute identifier : ScalarValues::String; }
    metadata rrTag : ReviewRecordRef about target { identifier = "RR-001"; }
}
"""

_FIXTURE_NO_TAGS = """
package ToasterDemo {
    part def Widget { attribute flag : ScalarValues::Boolean; }
    part target : Widget;
}
"""


def _load(source):
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(source, strict=False)
    assert model.ok, model.diagnostics
    return conn, model


def test_get_review_record_refs_finds_one_tag():
    conn, model = _load(_FIXTURE_ONE_TAG)
    try:
        refs = get_review_record_refs(model)
        assert len(refs) == 1
        assert refs[0]["identifier"] == "RR-001"
        assert refs[0]["annotated_element"] == "ToasterDemo::target"
    finally:
        conn.close()


def test_get_review_record_refs_empty_when_no_tags():
    conn, model = _load(_FIXTURE_NO_TAGS)
    try:
        assert get_review_record_refs(model) == []
    finally:
        conn.close()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_query.py -v`
Expected: FAIL — `get_review_record_refs` not defined.

- [ ] **Step 3: Implement**

Add to `src/toaster/query.py`, directly after `get_satisfy_relationships` (keeps the two `to_api_json()`-based helpers adjacent):

```python
def get_review_record_refs(model: Any, index: ApiIndex | None = None) -> list[dict]:
    """Every ``ReviewRecordRef`` metadata tag in the model: ``{tag, identifier, annotated_element}``.

    The model-to-Python direction of this tutorial's narrowed Assurance Claim Point anchor
    (``toaster-review-protocol``, SysML v2 formal/2026-03-02 SS7.27.2): given a loaded model,
    find every judgment-record tag and the one subject it names, independent of any
    notebook's own Python objects. Takes the first ``annotatedElement`` only, matching this
    tutorial's one-tag-one-subject convention (a tag with more than one is a modeling error
    this tutorial's own notebooks never produce, not a shape this helper tries to generalize).
    """
    idx = index or ApiIndex(model)
    out = []
    for e in idx.of_type("MetadataUsage"):
        type_qns = {idx.qn(t) for t in e.get("type", [])}
        if not any(qn and qn.endswith("::ReviewRecordRef") for qn in type_qns):
            continue
        annotated = [idx.qn(a) for a in e.get("annotatedElement", [])]
        identifier_value = None
        for member_ref in e.get("ownedMember", []):
            member = idx.by_id.get(_ref(member_ref))
            if member and member.get("declaredName") == "identifier":
                literal = idx.by_id.get(_ref(member.get("value")))
                if literal is not None:
                    identifier_value = literal.get("value")
        out.append({
            "tag": e.get("qualifiedName"),
            "identifier": identifier_value,
            "annotated_element": annotated[0] if annotated else None,
        })
    return out
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_query.py -v`
Expected: PASS.

- [ ] **Step 5: Run the full suite**

Run: `uv run pytest -q`
Expected: no regressions.

- [ ] **Step 6: Commit**

```bash
git add src/toaster/query.py tests/test_query.py
git commit -m "Add get_review_record_refs: model-to-Python direction of the judgment-record anchor"
```

---

## Task 3: The `ReviewRecordRef` construct, introduced once in Chapter 2 (`AC-001`)

**Depends on:** Task 1, Task 2 (must be merged first — `validate_record(record, model=...)` and the metadata tag it cross-checks must both exist).

**Files:**
- Modify: `models/ch02-cumulative.sysml`, `models/ch03-cumulative.sysml`, `models/ch04-cumulative.sysml`, `models/ch05-cumulative.sysml`, `models/ch06-cumulative.sysml`, `models/ch07-cumulative.sysml`, `models/ch08-cumulative.sysml`, `models/ch10-cumulative.sysml` (every cumulative file from Ch2 onward — each is a self-contained full snapshot, not an import chain, so the definition text is carried forward by copy into every later file, the same convention every other reusable construct in this tutorial already follows)
- Modify: `chapters/ch02-requirements/03-judgment-context.ipynb`
- Modify: `scripts/check_construction.py` (new registry entry — this notebook currently has no `TOASTER_INCREMENT`)

**Exact SysML text to add** (once, inside the `ToasterDemo` package body, placed immediately after `package ToasterDemo {`):

```sysml
metadata def ReviewRecordRef {
    attribute identifier : ScalarValues::String;
}
```

**`AC-001`'s own usage** (add immediately after `nominal`'s own declaration in every cumulative file ch02 onward — `nominal` already exists in `ch02-cumulative.sysml`, confirmed present):

```sysml
metadata ac001Tag : ReviewRecordRef about nominal {
    identifier = "AC-001";
}
```

(Use the short name `nominal`, not `ToasterDemo::nominal`, inside the `about` clause — the usage sits inside the same package, matching this repo's existing convention of short names inside a package body, e.g. how `TimelyToast::toaster` is written elsewhere. The qualified name `ToasterDemo::nominal` is what `subject_ref` and `model.find()` use from *outside* the package, in Python.)

- [ ] **Step 1: Add the definition and first usage to `models/ch02-cumulative.sysml`**

Insert the two SysML blocks above at the stated locations. Run:

```bash
uv run python - <<'EOF'
from pathlib import Path
import opensysml
conn = opensysml.connect(version="v0.9.0")
source = Path("models/ch02-cumulative.sysml").read_text()
model = conn.load_from_content(source, strict=False)
assert model.ok, model.diagnostics
print("ok")
conn.close()
EOF
```
Expected: `ok`, no diagnostics.

- [ ] **Step 2: Carry both blocks forward into every later cumulative file**

For each of `models/ch03-cumulative.sysml` through `models/ch08-cumulative.sysml` and `models/ch10-cumulative.sysml`: add the identical `metadata def ReviewRecordRef { ... }` block and the identical `ac001Tag` usage (targeting `nominal`, which already exists in every one of these files — confirmed by the Chapter 2 survey that `nominal`/`slow` persist unchanged through every later chapter). Re-run the same load-and-assert check against each file in turn, substituting the path.

- [ ] **Step 3: Add the construction zone to `chapters/ch02-requirements/03-judgment-context.ipynb`**

Per `toaster-recipe`'s construction-zone pattern and `toaster-review-protocol`'s updated judgment-record construction zone (Task 10 writes the skill text this follows — read that section of the spec now, since the skill edit and this notebook edit describe the same pattern): insert a new **first** named group, before the existing `claim`/`model_ref` group, narrating "what is being claimed, and what, specifically, it is about":

```python
# what is being claimed, and what, specifically, it is about
subject_ref = "ToasterDemo::nominal"
AC001_TAG = """\
metadata ac001Tag : ReviewRecordRef about nominal {
    identifier = "AC-001";
}
"""
print(AC001_TAG)
```

Followed by a markdown cell narrating that this fragment is the same text now committed in `models/ch02-cumulative.sysml`, and that loading the cumulative model (the existing `model.ok` cell, unchanged) is what makes this a real, checkable tag rather than an assertion the reader has to trust.

Add `subject_ref=subject_ref` to the existing `ReviewRecord(...)` call's keyword arguments (alongside `claim=claim`, `model_ref=model_ref`, etc.), and change the existing `errors = validate_record(context_record)` call to `errors = validate_record(context_record, model=model)` (the notebook's own `model` variable, already loaded by the existing cell 2 pattern).

**Rewrite the seam cell** to narrate the bridged connection per the spec's DL-075 resolution: one sentence addressing that the tagged SysML text (printed above), the tool that loads and cross-checks both the Python record and the model tag, and a result showing they agree, are three things the reader has just watched connect — e.g. (adapt to the notebook's own voice, but keep this shape): "The tag printed above is now part of the loaded model, and `validate_record` confirms the Python record and the model's own tag agree about what AC-001 is actually about." Do not name Tall or "the three worlds" (AGENTS.md 1.10, unchanged rule).

- [ ] **Step 4: Register the notebook in `scripts/check_construction.py`**

Add a new entry to the registry (alongside the existing Ch2 entries at the file's current lines ~80–95) for `chapters/ch02-requirements/03-judgment-context.ipynb`, with `context_stubs` providing the minimal stub `nominal` needs to parse in isolation (follow the existing stub style used by the neighboring Ch2 entries — e.g. a bare `part nominal;` stub, adjusted to whatever minimal form the existing entries use for referencing a prior-notebook element). Run:

```bash
uv run python scripts/check_construction.py --check
```
Expected: exit 0.

- [ ] **Step 5: Run the full notebook and the full suite**

Execute the notebook's cells top to bottom (or via the repo's existing notebook-execution check, if one exists — check `myst.yml`/CI config for how notebooks are normally executed) and confirm no errors. Then:

```bash
uv run pytest -q
```
Expected: no regressions.

- [ ] **Step 6: Commit**

```bash
git add models/ch02-cumulative.sysml models/ch03-cumulative.sysml models/ch04-cumulative.sysml models/ch05-cumulative.sysml models/ch06-cumulative.sysml models/ch07-cumulative.sysml models/ch08-cumulative.sysml models/ch10-cumulative.sysml chapters/ch02-requirements/03-judgment-context.ipynb scripts/check_construction.py
git commit -m "Introduce ReviewRecordRef metadata def; tag AC-001's real subject (nominal)"
```

---

## Task 4: Retrofit Chapter 3 — `AC-C03`, `AS-C03`

**Depends on:** Task 3 (must be merged first — shares the same 6 cumulative files ch03/04/05/06/07/08/10, sequenced to avoid merge conflicts with Tasks 5–9 below, which touch the same files).

**Subjects:** both records are about the same element, `ToasterDemo::timely` (the `TimelyToast` requirement usage), confirmed present from `models/ch03-cumulative.sysml` onward.

**Files:**
- Modify: `models/ch03-cumulative.sysml` through `models/ch08-cumulative.sysml`, `models/ch10-cumulative.sysml` (carry forward from Ch3)
- Modify: `chapters/ch03-measures/01-moe-definition.ipynb` (`AC-C03`; this notebook is **already registered** in `check_construction.py` with its own `TOASTER_INCREMENT` — extend it, do not create a new registry entry)
- Modify: `chapters/ch03-measures/03-threshold-judgment.ipynb` (`AS-C03`; **not yet registered** — add a new entry)
- Modify: `scripts/check_construction.py`

**Exact SysML text** (add to `models/ch03-cumulative.sysml` onward, after `timely`'s own declaration):

```sysml
metadata acC03Tag : ReviewRecordRef about timely {
    identifier = "AC-C03";
}

metadata asC03Tag : ReviewRecordRef about timely {
    identifier = "AS-C03";
}
```

(Two separate tags, same subject — Hawkins' own model allows more than one ACP to be about the same located element; nothing here requires one tag per subject, only one subject per tag.)

- [ ] **Step 1:** Add both blocks to `models/ch03-cumulative.sysml`; verify `model.ok` via the same load-and-assert snippet as Task 3 Step 1 (substitute the path and expect both `acC03Tag` and `asC03Tag` to resolve via `model.find("ToasterDemo::acC03Tag")` / `model.find("ToasterDemo::asC03Tag")`).
- [ ] **Step 2:** Carry both blocks forward into `models/ch04-cumulative.sysml` through `ch08-cumulative.sysml` and `ch10-cumulative.sysml`; verify each.
- [ ] **Step 3:** In `ch03-measures/01-moe-definition.ipynb`: extend the existing `TOASTER_INCREMENT` construction zone with the `acC03Tag` fragment (print it as its own named step, same pattern as Task 3 Step 3); add `subject_ref="ToasterDemo::timely"` to the `AC-C03` `ReviewRecord(...)` call; change its `validate_record(...)` call to pass `model=model`; rewrite its seam cell per the DL-075 resolution language (same shape as Task 3 Step 3's seam rewrite, adapted to this notebook's own subject).
- [ ] **Step 4:** In `ch03-measures/03-threshold-judgment.ipynb`: add a new construction-zone group (this notebook has no existing `TOASTER_INCREMENT` — follow Task 3 Step 3's full pattern, not the "extend" pattern) with the `asC03Tag` fragment; add `subject_ref="ToasterDemo::timely"` to the `AS-C03` call; `model=model` on `validate_record`; rewrite the seam cell.
- [ ] **Step 5:** Update `scripts/check_construction.py`: extend the existing Ch3/`01-moe-definition.ipynb` entry's expected `TOASTER_INCREMENT` content; add a new entry for `03-threshold-judgment.ipynb` with a minimal `timely` stub. Run `uv run python scripts/check_construction.py --check` — expect exit 0.
- [ ] **Step 6:** `uv run pytest -q` — no regressions.
- [ ] **Step 7:** Commit:
```bash
git add models/ch03-cumulative.sysml models/ch04-cumulative.sysml models/ch05-cumulative.sysml models/ch06-cumulative.sysml models/ch07-cumulative.sysml models/ch08-cumulative.sysml models/ch10-cumulative.sysml chapters/ch03-measures/01-moe-definition.ipynb chapters/ch03-measures/03-threshold-judgment.ipynb scripts/check_construction.py
git commit -m "Retrofit AC-C03/AS-C03 with subject_ref and ReviewRecordRef tags (both about timely)"
```

---

## Task 5: Retrofit Chapter 4 — `AI-C04`

**Depends on:** Task 4 (serialized — same shared cumulative files).

**Subject:** `ToasterDemo::ApplyHeat`.

**Files:**
- Modify: `models/ch04-cumulative.sysml` through `models/ch08-cumulative.sysml`, `models/ch10-cumulative.sysml`
- Modify: `chapters/ch04-functional-decomp/03-completeness-check.ipynb` (not yet registered — new entry)
- Modify: `scripts/check_construction.py`

**Exact SysML text** (after `ApplyHeat`'s own declaration):

```sysml
metadata aiC04Tag : ReviewRecordRef about applyHeat {
    identifier = "AI-C04";
}
```

Confirm the correct short name to use in `about`: the Ch4 survey found both a top-level `ApplyHeat` (an action def) and `ToastBread::applyHeat` (a nested performed usage). `AI-C04`'s existing `model_ref` is `ToasterDemo::ApplyHeat` (the definition/top-level usage, not the nested one) — use `ApplyHeat` in the `about` clause to match, and set `subject_ref="ToasterDemo::ApplyHeat"` in Python to match exactly.

- [ ] **Step 1:** Add the block to `models/ch04-cumulative.sysml`; verify.
- [ ] **Step 2:** Carry forward into `ch05` through `ch08`, `ch10` cumulative files; verify each.
- [ ] **Step 3:** In `ch04-functional-decomp/03-completeness-check.ipynb`: add the construction-zone group (new `TOASTER_INCREMENT`, following Task 3 Step 3's pattern); `subject_ref="ToasterDemo::ApplyHeat"` on the `AI-C04` call; `model=model` on `validate_record`; rewrite the seam cell.
- [ ] **Step 4:** Register the notebook in `check_construction.py` with a minimal `ApplyHeat` stub. `uv run python scripts/check_construction.py --check` — exit 0.
- [ ] **Step 5:** `uv run pytest -q` — no regressions.
- [ ] **Step 6:** Commit:
```bash
git add models/ch04-cumulative.sysml models/ch05-cumulative.sysml models/ch06-cumulative.sysml models/ch07-cumulative.sysml models/ch08-cumulative.sysml models/ch10-cumulative.sysml chapters/ch04-functional-decomp/03-completeness-check.ipynb scripts/check_construction.py
git commit -m "Retrofit AI-C04 with subject_ref and ReviewRecordRef tag (about ApplyHeat)"
```

---

## Task 6: Retrofit Chapter 6 — `AC-C06`, `AS-C06`, `AI-C06`, and its `AI-BAD` negative control

**Depends on:** Task 5 (serialized).

**Subjects:**
- `AC-C06` → `ToasterDemo::heatGenerationReq`
- `AS-C06` → `ToasterDemo::ResistanceCoil`
- `AI-C06` → `ToasterDemo::HeatingAssembly::heatGen`

**Files:**
- Modify: `models/ch06-cumulative.sysml` through `models/ch08-cumulative.sysml`, `models/ch10-cumulative.sysml`
- Modify: `chapters/ch06-recursive-decomp/02-second-level.ipynb` (`AC-C06`, `AS-C06`; **already registered** with an existing `TOASTER_INCREMENT` — extend it)
- Modify: `chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb` (`AI-C06` original authoring, plus `AI-BAD` negative control; not yet registered — new entry)
- Modify: `scripts/check_construction.py`

**Exact SysML text** (after each subject's own declaration in `models/ch06-cumulative.sysml`):

```sysml
metadata acC06Tag : ReviewRecordRef about heatGenerationReq {
    identifier = "AC-C06";
}

metadata asC06Tag : ReviewRecordRef about ResistanceCoil {
    identifier = "AS-C06";
}
```

And, for `AI-C06` (also lands in `ch06-cumulative.sysml`, since `HeatingAssembly::heatGen` already exists there per the survey):

```sysml
metadata aiC06Tag : ReviewRecordRef about HeatingAssembly::heatGen {
    identifier = "AI-C06";
}
```

- [ ] **Step 1:** Add all three blocks to `models/ch06-cumulative.sysml`; verify `model.ok` and that `model.find("ToasterDemo::acC06Tag")`, `...asC06Tag`, `...aiC06Tag` all resolve.
- [ ] **Step 2:** Carry all three forward into `ch07`, `ch08`, `ch10` cumulative files; verify each.
- [ ] **Step 3:** In `ch06-recursive-decomp/02-second-level.ipynb`: extend the existing `TOASTER_INCREMENT` with the `acC06Tag` and `asC06Tag` fragments (two more named steps in the existing construction zone, each its own print+narration); add `subject_ref="ToasterDemo::heatGenerationReq"` to the `AC-C06` call and `subject_ref="ToasterDemo::ResistanceCoil"` to the `AS-C06` call; `model=model` on both `validate_record` calls; rewrite both seam cells if this notebook has one seam cell per record, or the one shared seam cell if it has only one — follow whatever structure the notebook already has, updating every seam cell present.
- [ ] **Step 4:** In `ch06-recursive-decomp/03-stopping-judgment.ipynb`:
  - Add the construction-zone group (new `TOASTER_INCREMENT`) with the `aiC06Tag` fragment; `subject_ref="ToasterDemo::HeatingAssembly::heatGen"` on the `AI-C06` call; `model=model` on its `validate_record` call; rewrite its seam cell.
  - **`AI-BAD` fix (Review Focus item):** this notebook's `AI-BAD` negative control has `premises=[]` and currently no `subject_ref`. Under the new rule, `asserted_inference` with empty premises AND empty `subject_ref` now produces **two** errors (the pre-existing premises error, plus the new subject_ref-required error) where the notebook's own markdown currently asserts exactly one. Add `subject_ref="ToasterDemo::HeatingAssembly::heatGen"` to the `AI-BAD` construction (reusing `AI-C06`'s real subject — `AI-BAD` is demonstrating the premises rule specifically, not the subject_ref rule, so giving it a real, resolvable subject keeps that demonstration singular). Verify by running `validate_record(ai_bad_record, model=model)` and confirming the result is exactly `["asserted_inference requires at least one premise (Hawkins §3.1)"]`, not two entries. Update the notebook's own markdown/printed-assertion text if it states an exact error list, so it still matches.
- [ ] **Step 5:** Register `03-stopping-judgment.ipynb` in `check_construction.py` with a minimal `HeatingAssembly`/`heatGen` stub; extend the existing `02-second-level.ipynb` entry's expected content. `uv run python scripts/check_construction.py --check` — exit 0.
- [ ] **Step 6:** `uv run pytest -q` — no regressions.
- [ ] **Step 7:** Commit:
```bash
git add models/ch06-cumulative.sysml models/ch07-cumulative.sysml models/ch08-cumulative.sysml models/ch10-cumulative.sysml chapters/ch06-recursive-decomp/02-second-level.ipynb chapters/ch06-recursive-decomp/03-stopping-judgment.ipynb scripts/check_construction.py
git commit -m "Retrofit AC-C06/AS-C06/AI-C06 with subject_ref and tags; fix AI-BAD's new double-error"
```

---

## Task 7: Retrofit Chapter 8 — `AS-C08` (original) and its revision-flow reconstruction + negative control

**Depends on:** Task 6 (serialized).

**Subject:** `ToasterDemo::deliveredEnergyBoundedBySupply`.

**Files:**
- Modify: `models/ch08-cumulative.sysml`, `models/ch10-cumulative.sysml`
- Modify: `chapters/ch08-checking/02-violation-witness.ipynb` (original authoring; not yet registered — new entry)
- Modify: `chapters/ch08-checking/03-revision-flow.ipynb` (reconstruction of `AS-C08` + an empty-identifier negative control — no new model tag needed here, Python-only)
- Modify: `scripts/check_construction.py`

**Exact SysML text** (after `deliveredEnergyBoundedBySupply`'s own declaration in `ch08-cumulative.sysml`):

```sysml
metadata asC08Tag : ReviewRecordRef about deliveredEnergyBoundedBySupply {
    identifier = "AS-C08";
}
```

- [ ] **Step 1:** Add the block to `models/ch08-cumulative.sysml`; verify.
- [ ] **Step 2:** Carry forward into `models/ch10-cumulative.sysml`; verify.
- [ ] **Step 3:** In `ch08-checking/02-violation-witness.ipynb`: add the construction-zone group with the `asC08Tag` fragment; `subject_ref="ToasterDemo::deliveredEnergyBoundedBySupply"` on the `AS-C08` call; `model=model` on `validate_record`; rewrite the seam cell.
- [ ] **Step 4:** In `ch08-checking/03-revision-flow.ipynb` (no new model tag — this notebook only reconstructs and tests staleness, per the design's retrofit table rule that reconstructions carry `subject_ref` forward in Python only):
  - Add `subject_ref="ToasterDemo::deliveredEnergyBoundedBySupply"` to the rebuilt `AS-C08` record.
  - **Empty-identifier negative control fix (Review Focus item):** this notebook's `identifier=""` "broken" record (`kind="asserted_solution"`) currently has no `subject_ref` either. Under the new rule it would newly gain a second error (`subject_ref is empty`) alongside the intended `identifier is empty`. Add `subject_ref="ToasterDemo::deliveredEnergyBoundedBySupply"` to this record too, so it keeps demonstrating exactly `["identifier is empty"]`. Verify directly: `validate_record(broken_record, model=model) == ["identifier is empty"]`.
- [ ] **Step 5:** Register `02-violation-witness.ipynb` in `check_construction.py` with a minimal `deliveredEnergyBoundedBySupply` stub. `uv run python scripts/check_construction.py --check` — exit 0.
- [ ] **Step 6:** `uv run pytest -q` — no regressions.
- [ ] **Step 7:** Commit:
```bash
git add models/ch08-cumulative.sysml models/ch10-cumulative.sysml chapters/ch08-checking/02-violation-witness.ipynb chapters/ch08-checking/03-revision-flow.ipynb scripts/check_construction.py
git commit -m "Retrofit AS-C08 with subject_ref and tag; fix revision-flow's negative control"
```

---

## Task 8: Retrofit Chapter 9 reconstructions and negative controls (no new model tags — Ch9 has no cumulative model of its own)

**Depends on:** Task 7 (needs `AS-C06`'s and `AS-C08`'s real subject_ref values already decided, which Tasks 6/7 fix; Ch9's own notebooks load `ch08-cumulative.sysml` directly, confirmed by the survey — no Ch9 cumulative file exists, so this task touches no `models/*.sysml` file at all).

**Files:**
- Modify: `chapters/ch09-coverage-sufficiency/02-evidence-completeness.ipynb`
- Modify: `chapters/ch09-coverage-sufficiency/03-stale-detection.ipynb`

**Values to carry forward (Python only, matching each record's origin chapter exactly):**
- `AS-C06` → `subject_ref="ToasterDemo::ResistanceCoil"`
- `AS-C08` → `subject_ref="ToasterDemo::deliveredEnergyBoundedBySupply"`

**Negative controls needing a resolvable `subject_ref` added, each to preserve its own single-intended-error demonstration (Review Focus item — the same regression class as Task 6/7):**

| Notebook | Record | Current intended error | Fix |
|---|---|---|---|
| `02-evidence-completeness.ipynb` | `AS-BAD` (`kind="asserted_solution"`, `counterevidence=""`) | `["counterevidence is empty"]` | Add `subject_ref="ToasterDemo::ResistanceCoil"` |
| `02-evidence-completeness.ipynb` | `AS-PLACEHOLDER` (`kind="asserted_solution"`, all fields non-empty but weak — demonstrates **zero** errors despite weak content) | `[]` | Add `subject_ref="ToasterDemo::ResistanceCoil"` — without this, the record would newly gain `["subject_ref is empty (required for asserted_solution)"]`, silently breaking the notebook's own point that validation passes despite weak content |
| `03-stale-detection.ipynb` | empty-identifier `"broken"` record (`kind="asserted_solution"`) | `["identifier is empty"]` | Add `subject_ref="ToasterDemo::deliveredEnergyBoundedBySupply"` |

- [ ] **Step 1:** In `02-evidence-completeness.ipynb`: add `subject_ref` to the rebuilt `AS-C06` and `AS-C08` records (matching their origin-chapter values); add `subject_ref` to `AS-BAD` and `AS-PLACEHOLDER` per the table above. Update any `validate_record(...)` call in this notebook that doesn't already pass `model=model` to do so (needed for the resolution check to actually run against a real model — confirm the notebook already loads `model` via its existing cell 2; if it does not load a model at all currently, keep calling `validate_record(record)` without `model=` for this notebook, since the required-ness check alone, not resolution, is what's being demonstrated — check which is the case before deciding).
- [ ] **Step 2:** Verify each exact error list by running the notebook's own cells (or an equivalent standalone script) and asserting:
  - `validate_record(as_bad)` (or `..., model=model`) `== ["counterevidence is empty"]`
  - `validate_record(as_placeholder, ...) == []`
- [ ] **Step 3:** In `03-stale-detection.ipynb`: same `AS-C06`/`AS-C08` carry-forward; add `subject_ref` to the empty-identifier `"broken"` record per the table; verify `validate_record(broken, ...) == ["identifier is empty"]`.
- [ ] **Step 4:** `uv run pytest -q` — no regressions. (No `check_construction.py` change needed — neither notebook introduces a new SysML construct.)
- [ ] **Step 5:** Commit:
```bash
git add chapters/ch09-coverage-sufficiency/02-evidence-completeness.ipynb chapters/ch09-coverage-sufficiency/03-stale-detection.ipynb
git commit -m "Carry subject_ref forward in Ch9 reconstructions; fix negative controls' new double-errors"
```

---

## Task 9: Retrofit Chapter 10 — `AC-C10` (original), the judgment ledger, `AI-C10` exemption check, and its two negative controls

**Depends on:** Task 8 (serialized — shares `models/ch10-cumulative.sysml` with every earlier task; also needs `AC-C06`/`AS-C06`/`AI-C06`/`AS-C08` subject_ref values already fixed by Tasks 6/7).

**Subject:** `AC-C10` → `ToasterDemo::EnergyConservationReq`.

**Files:**
- Modify: `models/ch10-cumulative.sysml`
- Modify: `chapters/ch10-traceability-signoff/01-traceability-graph.ipynb` (`AC-C10` original authoring; **already registered** in `check_construction.py` with its own `TOASTER_INCREMENT` from the earlier energy-tie work — extend it)
- Modify: `chapters/ch10-traceability-signoff/02-judgment-synthesis.ipynb` (ledger reconstructions of `AS-C06`/`AS-C08`/`AI-C06`, plus `AI-BAD` negative control — no new model tag, Python-only)
- Modify: `chapters/ch10-traceability-signoff/03-engineering-signoff.ipynb` (`AI-C10` original authoring — confirm the exemption applies; `AI-C10-DRAFT` negative control — confirm whether it needs a fix)
- Modify: `scripts/check_construction.py`

**Exact SysML text** (after `EnergyConservationReq`'s own declaration in `models/ch10-cumulative.sysml` — this is the last cumulative file, so no further carry-forward is needed):

```sysml
metadata acC10Tag : ReviewRecordRef about EnergyConservationReq {
    identifier = "AC-C10";
}
```

- [ ] **Step 1:** Add the block to `models/ch10-cumulative.sysml`; verify `model.ok` and `model.find("ToasterDemo::acC10Tag")`.
- [ ] **Step 2:** In `ch10-traceability-signoff/01-traceability-graph.ipynb`: extend the existing `TOASTER_INCREMENT` with the `acC10Tag` fragment; `subject_ref="ToasterDemo::EnergyConservationReq"` on the `AC-C10` call; `model=model` on its `validate_record` call; rewrite its seam cell.
- [ ] **Step 3:** In `ch10-traceability-signoff/02-judgment-synthesis.ipynb` (no new model tag):
  - Carry forward `subject_ref` for the rebuilt `AS-C06` (`"ToasterDemo::ResistanceCoil"`), `AS-C08` (`"ToasterDemo::deliveredEnergyBoundedBySupply"`), `AI-C06` (`"ToasterDemo::HeatingAssembly::heatGen"`).
  - **`AI-BAD` fix** (same regression class as Task 6): this notebook's own `AI-BAD` (`premises=[]`, no `subject_ref`) would newly gain a second error. Add `subject_ref="ToasterDemo::HeatingAssembly::heatGen"` (reusing `AI-C06`'s subject, same reasoning as Task 6). Verify `validate_record(ai_bad, ...) == ["asserted_inference requires at least one premise (Hawkins §3.1)"]`.
- [ ] **Step 4:** In `ch10-traceability-signoff/03-engineering-signoff.ipynb`:
  - **`AI-C10` exemption check:** read the notebook's own existing `premises` list for the `AI-C10` record (the survey found it cites `AS-C06`/`AS-C08`/`AI-C06`/`AC-C10` plus coverage findings as prose premises — confirm this list is non-empty as currently written). If non-empty (expected), `AI-C10` needs **no** `subject_ref` change at all — leave it exactly as the spec's retrofit table states (exempt). Run `validate_record(ai_c10_record, model=model)` and confirm no `subject_ref`-related error appears, and that this matches the pre-existing behavior (zero new errors introduced).
  - **`AI-C10-DRAFT` check:** this negative control's intended error is `counterevidence=""`. Check whether its own `premises` list is already non-empty (it is described as "a draft of the synthesis record built below," implying it shares the same premises). If `premises` is non-empty, no fix is needed (the exemption already covers it — confirm by running `validate_record` and checking the result is exactly `["counterevidence is empty"]`). If `premises` turns out to be empty in this draft (unlike the final `AI-C10`), add `subject_ref="ToasterDemo::EnergyConservationReq"` to it so it keeps demonstrating exactly one error, the same fix pattern as every other negative control in this plan.
- [ ] **Step 5:** Extend the existing `01-traceability-graph.ipynb` registry entry in `check_construction.py` with the `acC10Tag` fragment. `uv run python scripts/check_construction.py --check` — exit 0.
- [ ] **Step 6:** `uv run pytest -q` — no regressions. Also run `uv run python scripts/check_construction.py --check` one final time across all chapters (not just `--chapter=10`) to confirm every earlier task's cumulative-file edits still hold together.
- [ ] **Step 7:** Commit:
```bash
git add models/ch10-cumulative.sysml chapters/ch10-traceability-signoff/01-traceability-graph.ipynb chapters/ch10-traceability-signoff/02-judgment-synthesis.ipynb chapters/ch10-traceability-signoff/03-engineering-signoff.ipynb scripts/check_construction.py
git commit -m "Retrofit AC-C10 with subject_ref and tag; carry ledger values forward; confirm AI-C10 exemption"
```

---

## Task 10: `toaster-review-protocol` skill update

**Depends on:** Task 3 (wants a real, landed example to cite — can run in parallel with Tasks 4–9 once Task 3 is merged, since it touches no `models/*.sysml` or chapter file).

**Files:**
- Modify: `.claude/skills/toaster-review-protocol/SKILL.md`

**Note:** this is a skill edit — per `skill-editor`, follow its pre-edit gate (DL-PENDING-then-COMPLETE, blast-radius table, minimal-change rule) even though this plan already specifies the exact diff; `skill-editor`'s process is still the required wrapper for making the edit, not a substitute for having one.

- [ ] **Step 1:** In the `## ReviewRecord required fields` example (current lines 24–46), add `subject_ref` to the constructor call, immediately after `claim=...`:

```python
record = ReviewRecord(
    identifier="RR-001",
    kind="asserted_solution",
    claim="DeliveredEnergy >= 50000 J at nominal operating conditions",
    subject_ref="ToasterDemo::deliveredEnergy",
    model_ref="models/ch07-snapshot.sysml",
    ...
```

- [ ] **Step 2:** Add a new section immediately after `## Three judgment sites and ACP kinds` (current lines 14–20), before `## ReviewRecord required fields`:

```markdown
## `subject_ref`: this tutorial's narrowed Assurance Claim Point

Hawkins' own Assurance Claim Point (ACP) is never free-floating: every confidence argument is
anchored to one specific, located assertion in the argument (Hawkins 2011, Sec. 3, p. 8 —
`glid:def-hawkins--assurance-claim-point`). `subject_ref` is this tutorial's own narrowed,
single-element analog: the one qualified name the record's `claim` is directly about, checkable
both from Python (`validate_record(record, model=model)` resolves it via `model.find()`) and from
the model's own side, via a real SysML metadata tag (SysML v2 formal/2026-03-02 SS7.27.2):

```sysml
metadata def ReviewRecordRef {
    attribute identifier : String;
}

metadata ac001Tag : ReviewRecordRef about nominal {
    identifier = "AC-001";
}
```

The `about` clause binds the usage's inherited `annotatedElement` feature to the named subject — a
real, queryable model relationship, not a string a reader has to trust. `subject_ref` is required
for `asserted_context` and `asserted_solution`; for `asserted_inference` it may stay empty only
when `premises` is non-empty (the pure cross-record synthesis case — `AI-C10` is the one record in
this tutorial that uses this exemption). `src/toaster/query.py`'s `get_review_record_refs()` is the
model-to-Python direction: given a loaded model, it finds every `ReviewRecordRef` tag and what it's
about, independent of any notebook's own Python objects. `validate_record` cross-checks both
directions automatically whenever a `model` is passed and a tag already exists for that record's
own `identifier`.
```

- [ ] **Step 3:** Update the `## Three judgment sites and ACP kinds` table (current lines 14–20) — add a column noting the required-ness rule:

```markdown
| Site | Kind | Hawkins ref | `subject_ref` |
|---|---|---|---|
| Assumption or context used for a claim | `asserted_context` | §3.2 | required |
| Child claims supporting a parent | `asserted_inference` | §3.1 | required unless `premises` is non-empty |
| Evidence supporting a conclusion | `asserted_solution` | §3.3 | required |
```

- [ ] **Step 4:** Update the `## Judgment record construction zone` group listing (current lines 60–95) to show the new first group:

```markdown
[markdown] narration: what is being claimed, and what, specifically, it is about
[code]     claim = "..."
           subject_ref = "ToasterDemo::..."
           model_ref = "..."
```

- [ ] **Step 5:** Verify the skill file still renders correctly (no broken markdown/code-fence nesting) by reading it back in full after editing.

- [ ] **Step 6:** Commit:
```bash
git add .claude/skills/toaster-review-protocol/SKILL.md
git commit -m "toaster-review-protocol: document subject_ref as this tutorial's ACP analog"
```

---

## Task 11: `toaster-recipe` skill update

**Depends on:** none of the other tasks strictly, but make this edit alongside or after Task 10 so both skill files stay consistent with each other in the same sitting.

**Files:**
- Modify: `.claude/skills/toaster-recipe/SKILL.md`

- [ ] **Step 1:** In the `## Judgment record notebooks` section (current lines ~117–121), add one sentence pointing at the new first construction-zone group:

```markdown
A notebook that builds a `ReviewRecord` (an `asserted_context`, `asserted_inference` or
`asserted_solution` judgment) uses `toaster-review-protocol`'s own construction-zone pattern for
it, not one dense call: name each group of fields, narrate what it's for, print it, then assemble.
The first group now names the record's own subject (`subject_ref`) alongside its `claim`, and
builds the matching `ReviewRecordRef` metadata-tag fragment the same way a model-increment cell
builds any other named fragment (`toaster-review-protocol` SS"subject_ref"). The size limits below
are relaxed for this content (see that skill for the exact grouping and why).
```

- [ ] **Step 2:** Add one sentence to the "Tall's three worlds" seam-cell guidance (current lines ~107–111, the "For the author's own reference" mapping) noting that a judgment-record notebook's seam cell now narrates a bridged connection, not a choice between readings — this closes DL-075:

```markdown
**Judgment-record notebooks specifically:** the seam cell narrates one bridged connection — the
tagged SysML text (the subject plus its `ReviewRecordRef` usage), the tool that loads it and
cross-checks both the Python record and the model tag, and a result showing they agree
(`validate_record` plus `get_review_record_refs`) — not a choice between the model's own
construct/tool/result triad and the record's own fields/`validate_record`/result triad
(`decisions/log.md` DL-075, retired by this convention).
```

- [ ] **Step 3:** Verify the skill file still renders correctly.

- [ ] **Step 4:** Commit:
```bash
git add .claude/skills/toaster-recipe/SKILL.md
git commit -m "toaster-recipe: judgment-record construction zone narrates subject_ref; closes DL-075"
```

---

## Task 12: Glossary — `gl:refines` edge

**Depends on:** none (can run any time; independent file).

**Files:**
- Modify: `glossary/definitions/hawkins.ttl`

**Exact edit:** the `glid:def-hawkins--assurance-claim-point` term already exists (confirmed present, lines 61–70 of the current file) and is already `gl:confirmed`. Add a new tutorial-side definition edge immediately after it, in the same file, following this file's own existing style (each definition block separated by a blank line):

```turtle
glid:def-tutorial--subject-ref
    a gl:Definition ;
    gl:confirmedBy "Z" ;
    gl:locator "src/toaster/evidence.py ReviewRecord.subject_ref; models/*.sysml ReviewRecordRef" ;
    gl:refines glid:def-hawkins--assurance-claim-point ;
    gl:source glid:src-tutorial ;
    gl:status gl:confirmed ;
    gl:term glid:term-assurance-claim-point ;
    gl:text "This tutorial's own narrowed analog of an Assurance Claim Point: a single, checkable qualified name a judgment record is directly about, anchored on both the Python side (subject_ref) and the model side (a ReviewRecordRef metadata tag), without importing GSN's argument-graph apparatus." .
```

Before writing this, check `glossary/sources/sources.ttl` for the exact id this tutorial uses as its own source (the design spec and CLAUDE.md both describe "this tutorial" as source N=9 in the glossary's own register) — use whatever id is actually registered there (likely `glid:src-tutorial`, but confirm, don't guess) rather than inventing a new one.

Also check `glossary/terms/terms.ttl` for whether `glid:term-assurance-claim-point` already exists as a `Term` node (it should, since the Definition edge already references it) — if for some reason it does not, this task must also add the `Term` node itself, following the existing style in that file.

- [ ] **Step 1:** Confirm the exact `gl:source` id for "this tutorial" in `glossary/sources/sources.ttl`.
- [ ] **Step 2:** Confirm `glid:term-assurance-claim-point` exists in `glossary/terms/terms.ttl`.
- [ ] **Step 3:** Add the `gl:refines` edge above (with the confirmed source id) to `glossary/definitions/hawkins.ttl`.
- [ ] **Step 4:** Run the glossary's own check:
```bash
uv run python -m glossary check
```
Expected: exits 0.
- [ ] **Step 5:** Run `uv run python -m glossary lookup "assurance claim point"` and confirm the output now shows both the Hawkins edge and the new tutorial `gl:refines` edge.
- [ ] **Step 6:** Commit:
```bash
git add glossary/definitions/hawkins.ttl
git commit -m "Glossary: tie subject_ref/ReviewRecordRef to Hawkins' Assurance Claim Point"
```

---

## Task 13: Close DL-075; record this work

**Depends on:** Task 9 (the retrofit must be complete and verified before this entry can honestly describe it as done).

**Files:**
- Modify: `decisions/log.md`

- [ ] **Step 1:** Append a new DL entry (check the current highest DL number at the time this task runs — it was `DL-083` as of this plan's writing, so this is very likely `DL-084`, but confirm with `grep -o "^## DL-[0-9]*" decisions/log.md | sort -t- -k2 -n | tail -1` before writing the number) in this repo's standard format (Path/Decision/Principles applied/Reasoning/Determined/Extension/Provenance), recording:
  - **Path:** the Hawkins-anchor design (`docs/superpowers/specs/2026-10-01-hawkins-judgment-record-anchor-design.md`) and this plan were implemented in full: `subject_ref` added to `ReviewRecord`; `ReviewRecordRef` metadata construct introduced in Ch2 and carried through every later cumulative model; `get_review_record_refs()` added; every original-authoring judgment record (`AC-001`, `AC-C03`, `AS-C03`, `AI-C04`, `AC-C06`, `AS-C06`, `AI-C06`, `AS-C08`, `AC-C10`) retrofitted with a real, resolvable `subject_ref` and a matching model tag; every reconstruction/ledger carries the value forward; every negative control that would otherwise have gained an unintended second validation error was fixed to keep demonstrating exactly its own one intended failure; `toaster-review-protocol` and `toaster-recipe` updated; the glossary's existing `assurance-claim-point` term now has a `gl:refines` edge from this tutorial's own convention.
  - **This closes DL-075.** State explicitly: the recurring judgment-record seam escalation (nine persona reports and ten ACE syntheses converging on it) is retired because judgment-record notebooks no longer face a choice between the model's own construct/tool/result triad and the record's own fields/`validate_record`/result triad — the seam cell now narrates one bridged connection (the tagged SysML text, the tool that loads and cross-checks both representations, and a result showing they agree), which is a concrete instance of AGENTS.md 1.10's requirement, not a judgment call between readings.
  - **Provenance:** cite the spec and this plan by path; note the primary-source read of Hawkins et al. 2011 and the live OpenSysML v0.9.0 probe that grounded the design before any code was written.

- [ ] **Step 2:** If `decisions/log.md` has a "status: open" marker or similar on the original DL-075 entry, update it to point at the new closing entry (follow whatever convention this file already uses for cross-referencing a later entry that resolves an earlier one — check a few existing examples in the file before writing this).

- [ ] **Step 3:** Commit:
```bash
git add decisions/log.md
git commit -m "DL-0NN: close DL-075 -- Hawkins judgment records now anchored to the model"
```

---

## Task 14: Full verification sweep

**Depends on:** every prior task.

- [ ] **Step 1:** Full test suite:
```bash
uv run pytest -q
```
Expected: all pass, no regressions from the baseline recorded before Task 1 (`411 passed, 7 deselected` plus `7 passed` under `-m checkpoint`, per the most recent PR description — the new tests from Tasks 1–2 add to this count, nothing should be removed from it).

- [ ] **Step 2:** Construction consistency, across every chapter, not just the ones this plan touched:
```bash
uv run python scripts/check_construction.py --check
```
Expected: exit 0.

- [ ] **Step 3:** Glossary:
```bash
uv run python -m glossary check
```
Expected: exit 0 (same pre-existing source-PDF-absent warnings as before this plan, no new errors).

- [ ] **Step 4:** Every cumulative model loads cleanly end to end (not just the ones with new content — a regression in an untouched file would mean a carry-forward step accidentally touched the wrong file):
```bash
uv run python - <<'EOF'
from pathlib import Path
import opensysml
conn = opensysml.connect(version="v0.9.0")
for n in ["02", "03", "04", "05", "06", "07", "08", "10"]:
    source = Path(f"models/ch{n}-cumulative.sysml").read_text()
    model = conn.load_from_content(source, strict=False)
    assert model.ok, f"ch{n}: {model.diagnostics}"
    print(f"ch{n}: ok")
conn.close()
EOF
```

- [ ] **Step 5:** Cross-representation agreement, across every original-authoring record, in one pass:
```bash
uv run python - <<'EOF'
from pathlib import Path
import opensysml
from toaster.query import get_review_record_refs

conn = opensysml.connect(version="v0.9.0")
source = Path("models/ch10-cumulative.sysml").read_text()  # the last file has every tag
model = conn.load_from_content(source, strict=False)
assert model.ok

refs = {r["identifier"]: r["annotated_element"] for r in get_review_record_refs(model)}
expected = {
    "AC-001": "ToasterDemo::nominal",
    "AC-C03": "ToasterDemo::timely",
    "AS-C03": "ToasterDemo::timely",
    "AI-C04": "ToasterDemo::ApplyHeat",
    "AC-C06": "ToasterDemo::heatGenerationReq",
    "AS-C06": "ToasterDemo::ResistanceCoil",
    "AI-C06": "ToasterDemo::HeatingAssembly::heatGen",
    "AS-C08": "ToasterDemo::deliveredEnergyBoundedBySupply",
    "AC-C10": "ToasterDemo::EnergyConservationReq",
}
for identifier, subject in expected.items():
    assert refs.get(identifier) == subject, f"{identifier}: expected {subject}, got {refs.get(identifier)}"
print("all 9 tags agree:", sorted(expected))
conn.close()
EOF
```

- [ ] **Step 6:** Contradiction sweep — grep for stale references to the pre-retrofit state:
```bash
grep -rn "validate_record(record)\s*$\|validate_record(r)\s*$" chapters/ --include=*.ipynb
```
Review every hit by hand: a bare one-argument `validate_record` call on an `asserted_context`/`asserted_solution` record, or an `asserted_inference` record with empty premises, is a sign a retrofit step in Tasks 4–9 was missed (it would now report a `subject_ref`-required error that no markdown cell explains).

- [ ] **Step 7:** Report results. No commit for this task (verification only) unless a fix is needed, in which case fix forward with its own commit and re-run this task's steps.

---

## Execution Notes for Whoever (or Whatever) Runs This Overnight

- **Tasks 1 and 2 may run in parallel** (independent files, no shared blast zone).
- **Tasks 3 through 9 must run strictly in series**, even though the records themselves don't logically depend on each other, because every one of them edits the same shared set of `models/chNN-cumulative.sysml` files — parallel branches would conflict at integration. This is exactly the "shared blast zone forces serial dispatch" case `orchestrator-protocol` already describes.
- **Tasks 10, 11, and 12 may run in parallel with Tasks 4–9** (and with each other) once Task 3 is merged — they touch skill files and the glossary only, no shared cumulative-model blast zone.
- **Task 13 depends on Task 9** (needs the retrofit done to describe truthfully) but not on Tasks 10–12.
- **Task 14 depends on everything.**
- Each task above is sized to be one `builder`/`reviewer` work contract under `orchestrator-protocol`'s "Plan-driven non-chapter work" mechanism. Route escalations (a stub that won't validate, a qualified name that doesn't resolve as expected, a negative control whose exact current field values don't match what this plan assumed) through the normal chain — builder to orchestrator to ACE — rather than guessing past them; the ACE rules or escalates to Z per its own protocol, and logs either way.
