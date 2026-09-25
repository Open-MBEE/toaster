---
name: opensysml-api
description: opensysml v0.9.0 interface — correct method names, return shapes, limitations, and the D-001 encapsulation rule.
---

# OpenSysML v0.9.0 API

## Connection

```python
import opensysml
import opensysml.binary

opensysml.binary.ensure_binary(version="v0.9.0")
conn = opensysml.connect(version="v0.9.0")
model = conn.load_from_content(source, strict=False)   # CORRECT — not conn.loads() or conn.load()
conn.close()
```

`model.ok` → bool. `model.diagnostics` → list of objects with `.severity`, `.message`, `.start_line`, `.start_column`, `.end_line`, `.end_column`.

## Evaluation and execution

```python
result = model.eval("ToasterDemo::DeliveredEnergy(800.0, 120.0, 0.7)")
float(result)    # cast — raw return is not a plain float

trace = model.execute_state(subject="ToasterDemo::Cycle", events=["Start", "Finish"])
# returns {"states_visited": [...]}

verdict = model.verify_constraint("ToasterDemo::TimelyToast", subject="ToasterDemo::nominal", engine="check")
# engine values: "check", "ir"
```

## Satisfaction and coverage (Ch9–10)

```python
verdicts = model.verify_satisfaction()          # list of Verdict(kind, element, holds, error)
ok = model.satisfied()                          # bool

# D-001: model.query() returns ZERO SatisfyRequirementUsage elements.
# CORRECT workaround — call this function, never repeat the workaround in notebooks:
from toaster.query import get_satisfy_relationships
satisfies = get_satisfy_relationships(model)    # list of dicts with @type, subsets, subject
```

`get_satisfy_relationships()` is the single point of the `to_api_json()` workaround.
When D-001 is resolved upstream, only that function changes.

## Model query (Ch9–10)

```python
reqs = model.query(where={
    "@type": "PrimitiveConstraint",
    "property": "@type",
    "operator": "=",
    "value": ["RequirementUsage"],
})
# QueryElement: .id, .type, .properties, .get(name, default), .as_dict()
# Also queryable: AllocationUsage, ActionUsage, PartUsage, RequirementDefinition
```

## Structured export

```python
model.to_sysml()      # roundtrip SysML text — safe, not experimental
model.to_api_json()   # OMG SysML v2 API JSON — experimental (fires warning); use only via get_satisfy_relationships()
# model.to_turtle()   — do NOT use in tutorial notebooks
```

## Symbol navigation

```python
sym = model.find("ToasterDemo::Heater")    # Symbol | None (by short name or FQN)
sym = model.get("ToasterDemo::Heater")     # Symbol — raises if not found
ns  = model.root                           # root namespace Symbol
```

## What does NOT exist

- `conn.loads()`, `conn.load()` — these methods do not exist
- OSLC queries — no OSLC client in v0.9.0; `model.query()` is the SysML v2 API Query protocol
- `render_document`, `run_document_query` — require model-internal `DocumentQueries::Document` elements; don't use in tutorial notebooks

## Environment variables

`OPENSYSML_VERSION` (preferred), `OPENSYSML_GRPC_VERSION` (upstream fallback)

**Reference:** `sysmlv2-testing/adapters/opensysml.py` — authoritative; probed 2026-09-25 against v0.9.0.
