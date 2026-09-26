---
name: opensysml-query
description: Tested cookbook for interrogating a loaded SysML v2 model with OpenSysML v0.9.0 (three surfaces, what each sees, id formats, recipes, what does not work and the workaround). Snippets are executed by tests/test_skill_snippets.py.
---

# Querying a model (OpenSysML v0.9.0)

SysML v2 is declarative and database-like (AGENTS.md 1.4): we build a model, then ask it questions. There are three surfaces, and none of them sees everything. Pick by what you need to see. Results and dates are in `decisions/probes.md`; gap ids (G1 to G7) are in `decisions/log.md` DL-015.

| Surface | Sees | Does not see |
|---|---|---|
| `model.query(...)` (the API standard's Query: `scope`, `select`, `where`, `= > <`, `and`/`or`, `inverse`; no traversal) | **Named** elements of any metaclass, including named allocations, connections and flows | Unnamed `allocate`, `flow`, `connect`; every `satisfy`; metadata usages. A `perform action heat : X` appears as an `ActionUsage`. Inherited members are not expanded. |
| `json.loads(model.to_api_json().content)` | Everything, unnamed included, with qualified names and typed references | Nothing structural, but it is a flat list you must index yourself |
| `Symbol` (`model.find`, `model.get`, `.children`, `.specializations`, `.attributes`) | The named tree and its specialization edges | Unnamed elements |

`to_api_json()` returns a `Conversion` object: read `.content`, and suppress its experimental warning. Never hand `model.to_api_json()` to `json.loads` directly.

**Convention that makes queries easier:** name allocations, connections and flows in the model (`allocation apply2source allocate apply to source;`). Named ones become visible to `model.query()`. `satisfy` cannot be named, so use the JSON recipe.

## Setup used by every recipe

```python
import json, warnings
from collections import defaultdict, deque
from pathlib import Path
import opensysml

conn = opensysml.connect(version="v0.9.0")
model = conn.load_from_content(Path("models/ch08-cumulative.sysml").read_text(), strict=False)
assert model.ok

def pc(prop, op, value):
    return {"@type": "PrimitiveConstraint", "property": prop, "operator": op, "value": value if isinstance(value, list) else [value]}

def api_elements(m):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return json.loads(m.to_api_json().content)

els = api_elements(model)
by_id = {e["@id"]: e for e in els}
def ref(r): return r["@id"] if isinstance(r, dict) else r
def qn(r): return by_id.get(ref(r), {}).get("qualifiedName")   # never rebuild a name from an @id (see below)
def of_type(*t): return [e for e in els if e.get("@type") in t]
```

## Recipe 1: elements by type (named only)

```python
part_defs = model.query(where=pc("@type", "=", ["PartDefinition"]), select=["name"])
names = sorted(r.id for r in part_defs)          # ids are qualified names like ToasterDemo::Heater
assert "ToasterDemo::Heater" in names
abstract_ones = [r.id for r in model.query(where={"@type": "CompositeConstraint", "operator": "and", "constraint": [
    pc("@type", "=", ["PartDefinition"]), pc("isAbstract", "=", [True])]}, select=["name"])]
```

`QueryElement` has `.id`, `.type`, `.properties`, `.get(name, default)`, `.as_dict()`. `select` names the properties to return.

## Recipe 2: what specializes what (named elements, `Symbol`)

```python
def spec_edges():
    up, down = defaultdict(set), defaultdict(set)
    for r in model.query(select=["name"]):
        sym = model.get(r.id)
        for sp in sym.specializations:
            if sp.target_id:
                up[r.id].add(sp.target_id); down[sp.target_id].add(r.id)
    return up, down

def closure(start, edges):
    seen, todo = set(), deque([start])
    while todo:
        for n in edges.get(todo.popleft(), ()):
            if n not in seen:
                seen.add(n); todo.append(n)
    return seen

up, down = spec_edges()
realizers = closure("ToasterDemo::ToastingSystem", down)     # everything that (transitively) specializes it
assert "ToasterDemo::HeatingSystem" in realizers
```

This is how you find the concrete parts that realize an abstract logical part def. Specialization is *not* expanded for you: a part def that specializes an abstract one does not list the abstract one's members in `model.query`.

## Recipe 3: connectors, allocations and flows including unnamed (JSON)

```python
def end_path(end):
    """Path a connector end points at, e.g. ['ToasterDemo::BreadHandling::loader', 'ToasterDemo::BreadLoader::bread']."""
    rs = end.get("ownedReferenceSubsetting")
    if not rs:
        return []
    target = by_id[ref(by_id[ref(rs)]["referencedFeature"])]
    if "chainingFeature" in target:
        return [qn(c) for c in target["chainingFeature"]]
    return [target.get("qualifiedName")]

def connectors(*types):
    return [{"id": e.get("qualifiedName"), "type": e["@type"], "ends": [end_path(by_id[ref(r)]) for r in e.get("connectorEnd", [])]}
            for e in of_type(*types)]

flows = connectors("FlowUsage")
allocs = connectors("AllocationUsage")
assert flows and allocs
```

Each `ends` entry is a path; the first element is the owning feature, which lets you ask "is anything allocated *to* this component". To include inherited allocations, first expand the component with `closure(component, up)` from Recipe 2.

## Recipe 4: satisfy, perform (JSON only)

```python
def satisfies():
    return [{"id": e.get("qualifiedName"), "requirement": qn(e["subsets"]) if "subsets" in e else None,
             "subject": qn(e["subject"]) if "subject" in e else None} for e in of_type("SatisfyRequirementUsage")]

def performs():
    out = []
    for e in of_type("PerformActionUsage"):
        act = e.get("references") or (e.get("type") or [None])[0]
        out.append({"performer": qn(e["owner"]), "action": qn(act) if act else None})
    return out

assert satisfies()
```

`satisfy` and `verify` both appear as `SatisfyRequirementUsage`; the declared keyword distinguishes them. Coverage (which requirements have a satisfy, which subjects are verified) is a join of `satisfies()` with the requirement list from Recipe 1.

## Ids

The API JSON `@id` uses `__` for `::` and escapes `_` (`named_flow` becomes `named_5fflow`). Never rebuild a qualified name with `id.replace("__", "::")`. Look up `qualifiedName` in the element itself (`qn`), as above. Ids returned by `model.query` and `Symbol` are already qualified names.

## What does not work, and the workaround

| Problem | Workaround |
|---|---|
| `model.query` cannot see unnamed connectors, any `satisfy`, or metadata | Recipe 3 and 4 (JSON). Better: name connectors and allocations. |
| Named `perform` reports type `ActionUsage`, not `PerformActionUsage` | Query `ActionUsage`, or use Recipe 4. |
| `perform ToastBread;` where `ToastBread` is an action def | Rejected, and correct per spec 7.17.6. Write `perform action x : ToastBread;` or reference a usage. |
| Mismatched port types (a power port to a fuel port) are not diagnosed (G4) | Check port types yourself: read the two end features' `type` in the JSON and compare. |
| `import` across separately loaded sources does not resolve (G7) | Assemble by concatenation: join the SysML text yielded by the implicit modules and the chapter's explicit increment into one string and load that. Concatenation loses which source an element came from, so give implicit parts their own package (or a metadata marker) if provenance must stay queryable. |
| `conn.load(path)` exists but does not resolve imports either | Same workaround. |
| No `requirement_coverage` in `src/toaster/query.py` yet, and its allocation and satisfy helpers are being corrected in this pass | Use the recipes above until the corrected helpers land, then call those. |

The sysml-toolkit Python binding (`sysmlv2.Session.from_files`) does resolve imports across files and sees unnamed elements through `elements_of_metaclass`. It is toolchain, not a chapter dependency (see `decisions/probes.md`).

## Before you assert something works

Run it. The snippets above are executed by `tests/test_skill_snippets.py` against `models/ch08-cumulative.sysml`. When you add a recipe, add it here inside a `python` block so the test covers it.
