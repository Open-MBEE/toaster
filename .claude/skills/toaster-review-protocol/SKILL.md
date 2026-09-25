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

| Site | Kind | Hawkins ref |
|---|---|---|
| Assumption or context used for a claim | `asserted_context` | §3.2 |
| Child claims supporting a parent | `asserted_inference` | §3.1 |
| Evidence supporting a conclusion | `asserted_solution` | §3.3 |

## ReviewRecord required fields

```python
from toaster.evidence import ReviewRecord, hash_content

record = ReviewRecord(
    identifier="RR-001",
    kind="asserted_solution",
    claim="DeliveredEnergy >= 50000 J at nominal operating conditions",
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
