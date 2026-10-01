---
name: toaster-review-protocol
description: Hawkins et al. 2011 judgment record fields, three ACP types, two evidence paths, and ReviewRecord dataclass usage.
---

# Toaster Review Protocol

## Hawkins 2011 §§3.1–3.4 terms

- **Appropriateness** — correct for the application, context, and argument purpose
- **Sufficiency** — enough evidence to establish probable truth of the claim
- **Trustworthiness** — freedom from flaw, argued via process

## Three judgment sites and ACP kinds

| Site | Kind | Hawkins ref | `subject_ref` |
|---|---|---|---|
| Assumption or context used for a claim | `asserted_context` | §3.2 | required |
| Child claims supporting a parent | `asserted_inference` | §3.1 | required unless `premises` is non-empty |
| Evidence supporting a conclusion | `asserted_solution` | §3.3 | required |

## `subject_ref`: this tutorial's narrowed Assurance Claim Point

Hawkins' own Assurance Claim Point (ACP) is never free-floating: every confidence argument is
anchored to one specific, located assertion in the argument (Hawkins 2011, Sec. 3, p. 8 —
`glid:def-hawkins--assurance-claim-point`). `subject_ref` is this tutorial's own narrowed,
single-element analog: the one qualified name the record's `claim` is directly about, checkable
both from Python (`validate_record(record, model=model)` resolves it via `model.find()`) and from
the model's own side, via a real SysML metadata tag (SysML v2 formal/2026-03-02 §7.27.2,
MetadataDefinition):

```sysml
metadata def ReviewRecordRef {
    attribute identifier : ScalarValues::String;
}

metadata ac001Tag : ReviewRecordRef about nominal {
    identifier = "AC-001";
}
```

(the committed text in `models/ch02-cumulative.sysml`, built in
`chapters/ch02-requirements/03-judgment-context.ipynb`.)

The `about` clause binds the usage's inherited `annotatedElement` feature to the named subject — a
real, queryable model relationship, not a string a reader has to trust. `subject_ref` is required
for `asserted_context` and `asserted_solution`; for `asserted_inference` it may stay empty only
when `premises` is non-empty (the pure cross-record synthesis case — `AI-C10` is the one original
record that actually relies on this exemption rather than carrying a real anchor anyway; negative
controls such as `AI-C10-DRAFT` rely on it too). `src/toaster/query.py`'s `get_review_record_refs()` is the
model-to-Python direction: given a loaded model, it finds every `ReviewRecordRef` tag and what it's
about, independent of any notebook's own Python objects. `validate_record` cross-checks both
directions automatically whenever a `model` is passed and a tag already exists for that record's
own `identifier`.

## ReviewRecord required fields

```python
from toaster.evidence import ReviewRecord, hash_content

record = ReviewRecord(
    identifier="RR-001",
    kind="asserted_solution",
    claim="DeliveredEnergy >= 50000 J at nominal operating conditions",
    subject_ref="ToasterDemo::HeatGenerator::deliveredEnergy",
    model_ref="models/ch07-snapshot.sysml",
    content_hash=hash_content(open("models/ch07-snapshot.sysml").read()),
    scope="nominal operating envelope: P=800W, t=120s, eta=0.7",
    criteria="Q >= 50000 J",
    premises=["Q = eta * P * t (constant efficiency model)"],
    assumption_refs=["A-001: constant efficiency over cycle"],
    evidence_refs=["tests/fixtures/probe.sysml eval run 2026-09-25"],
    rationale="The energy model yields 67200 J at nominal conditions, exceeding the 50000 J threshold.",
    counterevidence="Real toasters have varying efficiency during warm-up. Claim is bounded to the defined operating envelope.",
    residual_uncertainties="User acceptance requires separate evidence; energy surrogate does not establish toast quality.",
    disposition="pending",           # always "pending" for worked examples (SA-7)
    dependency_freshness="current",
    engineering_conclusion="supported",
    record_kind="worked_example",    # always "worked_example" in this tutorial (SA-7)
)
```

## Why a judgment record is its own notebook content, not an aside

The model is computable: `model.eval(...)` and the conformance checks tell you whether a claim
holds. That is not the same as the model being interpretable — knowing a claim evaluates True or
False does not by itself tell a reader whether the claim was the right one to check, whether enough
was checked to trust it, or what would have to be true for the check to be wrong. A `ReviewRecord`
is where that second layer lives: it states, in the reader's terms, what appropriateness,
sufficiency and trustworthiness look like for this specific claim (Hawkins 2011 §§3.1-3.4). A
notebook that builds one is teaching that layer as directly as a construction-zone cell teaches a
SysML construct, and deserves the same narrated, one-idea-at-a-time treatment, not a single
dense call that a reader skims past to get to the printed validation result.

## Judgment record construction zone

Build a `ReviewRecord` the same way a construction-zone notebook builds a model fragment: name each
group of fields, narrate what it's for, print it, then assemble. Group by the question each part of
Hawkins' taxonomy is answering, not by the dataclass's field order:

```
[markdown] narration: what is being claimed, and what, specifically, it is about
[code]     claim = "..."
           subject_ref = "ToasterDemo::..."
           model_ref = "..."
[markdown] narration: what standard the claim is checked against (appropriateness)
[code]     scope = "..."
           criteria = "..."
[markdown] narration: what's being taken as given
[code]     premises = [...]
           assumption_refs = [...]
[markdown] narration: what supports the claim, and how (sufficiency)
[code]     evidence_refs = [...]
           rationale = "..."
[markdown] narration: what could be wrong, and what's still open (trustworthiness) —
           counterevidence and residual_uncertainties are never blank; a record that
           hides its own weak points is not more trustworthy, it is less checkable
[code]     counterevidence = "..."
           residual_uncertainties = "..."
[markdown] narration: assembling the record from the named parts above
[code]     record = ReviewRecord(identifier=..., kind=..., claim=claim, subject_ref=subject_ref,
               model_ref=model_ref, content_hash=hash_content(source), scope=scope, criteria=criteria,
               premises=premises, assumption_refs=assumption_refs,
               evidence_refs=evidence_refs, rationale=rationale,
               counterevidence=counterevidence,
               residual_uncertainties=residual_uncertainties,
               disposition="pending", dependency_freshness="current",
               engineering_conclusion=..., record_kind="worked_example")
           errors = validate_record(record)
           print(f"Validation errors: {errors}")
```

Five groups, five narration cells, matching the model-fragment construction zone's pacing rule (no
two code cells adjacent). Each `print`ed group is the record's own reflection, the same role a
printed `TOASTER_INCREMENT` plays for a model fragment.

**Size limit:** `toaster-recipe`'s ≤600 words / ≤50 lines budget is sized for a notebook whose main
content is one model construct. A notebook whose construct is a judgment record may exceed it — the
fields Hawkins' taxonomy requires are the content, not overhead around it — provided the words spent
are the record's own claim, criteria, evidence, rationale and challenge, not restated narration
about the tutorial's own process.

## Two evidence paths

| Path | Use when | Call |
|---|---|---|
| Model checking | Discrete/logical property: "does this constraint hold?" | `model.verify_constraint(name, subject=..., engine="check")` |
| Python simulation | Continuous/parametric: "does this quantity satisfy this requirement across a range?" | sympy → lambdify → numpy grid → matplotlib |

## Canonical simulation pattern (Ch7)

```python
import sympy as sp
import numpy as np

P, t, eta = sp.symbols('P t eta', positive=True)
Q_sym = P * t * eta                          # mirrors calc def DeliveredEnergy
Q_fn = sp.lambdify([P, t, eta], Q_sym, 'numpy')

P_vals = np.linspace(500, 1200, 50)
Q_vals = Q_fn(P_vals, 120.0, 0.7)

# Evidence check — reference value independently calculated
assert abs(float(Q_fn(800.0, 120.0, 0.7)) - 67200.0) < 1.0
```

## Rules

- `record_kind` must always be `"worked_example"` (SA-7). The acceptance discussion goes in `rationale` as teaching narrative; `disposition` stays `"pending"`.
- `counterevidence` must be non-empty. A5 will report CANT_TELL if this field is blank.
- `dependency_freshness` becomes `"stale"` when `model_ref` content hash no longer matches. Use `check_stale(record, current_content)`.
- `disposition = "accepted"` is forbidden in this tutorial.

**Reference:** `ADCS-lifecycle-demo/traceability/attestation.py` for appropriateness/sufficiency structure.
