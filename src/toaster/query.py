"""Model element queries over an OpenSysML v0.9.0 model.

Three surfaces, none of which sees everything (see the `opensysml-query` skill and decisions/probes.md):

- ``model.query()``: named elements only. Named allocations, connections and flows are visible.
- ``model.to_api_json().content``: everything, including unnamed connectors and every ``satisfy``.
  This module is the single place that reads it.
- ``Symbol.specializations``: the named specialization tree.

Helpers that need unnamed elements or connector ends go through ``ApiIndex``. When an upstream gap closes
(G1, decisions/log.md DL-015), only this module changes.
"""

from __future__ import annotations

import json
import warnings
from collections import defaultdict, deque
from typing import Any


def _constraint(prop: str, op: str, value: Any) -> dict:
    return {"@type": "PrimitiveConstraint", "property": prop, "operator": op,
            "value": value if isinstance(value, list) else [value]}


def query_by_type(model: Any, *types: str, scope: list[str] | None = None, select: list[str] | None = None) -> list:
    """Named elements whose @type is any of ``types`` (for example ``"PartDefinition"``)."""
    return model.query(scope=scope, select=select, where=_constraint("@type", "=", list(types)))


def find_requirements(model: Any) -> list:
    """All named RequirementUsage elements."""
    return query_by_type(model, "RequirementUsage")


def api_elements(model: Any) -> list[dict]:
    """The API JSON export as a list of element dicts (reads ``.content``; silences the experimental warning)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return json.loads(model.to_api_json().content)


def _ref(r: Any) -> Any:
    return r["@id"] if isinstance(r, dict) else r


class ApiIndex:
    """Index of the API-JSON export: the only route to unnamed connectors and to ``satisfy``."""

    def __init__(self, model: Any) -> None:
        self.elements = api_elements(model)
        self.by_id = {e["@id"]: e for e in self.elements}
        self.by_qn = {e["qualifiedName"]: e for e in self.elements if e.get("qualifiedName")}

    def qn(self, ref: Any) -> str | None:
        """Qualified name of a reference. Never rebuild it from an @id: ``_`` is escaped in ids."""
        return self.by_id.get(_ref(ref), {}).get("qualifiedName")

    def of_type(self, *types: str) -> list[dict]:
        return [e for e in self.elements if e.get("@type") in types]

    def end_path(self, end_ref: Any) -> list[str]:
        """Path a connector end points at, e.g. ['P::loader', 'P::BreadLoader::bread'], or ['P::a'] for a plain feature."""
        end = self.by_id[_ref(end_ref)]
        rs = end.get("ownedReferenceSubsetting")
        if not rs:
            return []
        target = self.by_id[_ref(self.by_id[_ref(rs)]["referencedFeature"])]
        if "chainingFeature" in target:
            return [self.qn(c) for c in target["chainingFeature"]]
        return [target.get("qualifiedName")]

    def type_names(self, feature_qn: str) -> list[str]:
        return [self.qn(t) for t in self.by_qn.get(feature_qn, {}).get("type", [])]


def find_connectors(model: Any, *types: str, index: ApiIndex | None = None) -> list[dict]:
    """``{id, type, ends}`` for each connector of the given metaclass names (unnamed included).

    ``ends`` is one path per connector end (see ``ApiIndex.end_path``). Metaclasses: ``AllocationUsage``,
    ``FlowUsage``, ``ConnectionUsage``, ``InterfaceUsage``.
    """
    idx = index or ApiIndex(model)
    return [{"id": e.get("qualifiedName"), "type": e["@type"],
             "ends": [idx.end_path(r) for r in e.get("connectorEnd", [])]} for e in idx.of_type(*types)]


def find_allocations(model: Any, index: ApiIndex | None = None) -> list[dict]:
    """All allocations, named or not, as ``{id, type, ends}``."""
    return find_connectors(model, "AllocationUsage", index=index)


def get_satisfy_relationships(model: Any) -> list[dict]:
    """Raw API-JSON elements of every SatisfyRequirementUsage (D-001: ``model.query`` returns none)."""
    return ApiIndex(model).of_type("SatisfyRequirementUsage")


def satisfy_relationships(model: Any, index: ApiIndex | None = None) -> list[dict]:
    """``{id, requirement, subject}`` for every satisfy (and verify) relationship."""
    idx = index or ApiIndex(model)
    return [{"id": e.get("qualifiedName"),
             "requirement": idx.qn(e["subsets"]) if "subsets" in e else None,
             "subject": idx.qn(e["subject"]) if "subject" in e else None}
            for e in idx.of_type("SatisfyRequirementUsage")]


def perform_relationships(model: Any, index: ApiIndex | None = None) -> list[dict]:
    """``{performer, action}`` for each perform action usage: the owner performs the typed or referenced action."""
    idx = index or ApiIndex(model)
    out = []
    for e in idx.of_type("PerformActionUsage"):
        act = e.get("references") or (e.get("type") or [None])[0]
        out.append({"performer": idx.qn(e["owner"]), "action": idx.qn(act) if act else None})
    return out


def requirement_coverage(model: Any, index: ApiIndex | None = None) -> list[dict]:
    """For each requirement usage: ``{requirement, satisfied_by, covered}``. Traceability for sign-off."""
    idx = index or ApiIndex(model)
    by_req: dict[str, list[str]] = defaultdict(list)
    for s in satisfy_relationships(model, idx):
        if s["requirement"] and s["subject"]:
            by_req[s["requirement"]].append(s["subject"])
    reqs = sorted(e["qualifiedName"] for e in idx.of_type("RequirementUsage") if e.get("qualifiedName"))
    return [{"requirement": r, "satisfied_by": sorted(by_req.get(r, [])), "covered": bool(by_req.get(r))} for r in reqs]


def specialization_graph(model: Any, kinds: set[str] | None = None) -> tuple[dict, dict]:
    """``(up, down)``: child to parents and parent to children over named elements (from ``Symbol.specializations``)."""
    up: dict[str, set[str]] = defaultdict(set)
    down: dict[str, set[str]] = defaultdict(set)
    for r in model.query(select=["name"]):
        sym = model.get(r.id)
        if sym is None:
            continue
        for sp in sym.specializations:
            if sp.target_id and (kinds is None or sp.kind in kinds):
                up[r.id].add(sp.target_id)
                down[sp.target_id].add(r.id)
    return up, down


def _closure(start: str, edges: dict) -> set[str]:
    seen: set[str] = set()
    todo = deque([start])
    while todo:
        for n in edges.get(todo.popleft(), ()):
            if n not in seen:
                seen.add(n)
                todo.append(n)
    return seen


def specializes_transitively(model: Any, qualified_name: str, kinds: set[str] | None = None) -> set[str]:
    """Everything that (transitively) specializes ``qualified_name``: the concrete realizers of an abstract part def."""
    return _closure(qualified_name, specialization_graph(model, kinds)[1])


def supertypes_transitively(model: Any, qualified_name: str, kinds: set[str] | None = None) -> set[str]:
    """Everything ``qualified_name`` (transitively) specializes."""
    return _closure(qualified_name, specialization_graph(model, kinds)[0])


def allocations_for(model: Any, qualified_name: str, inherit: bool = True, index: ApiIndex | None = None) -> list[dict]:
    """Allocations with ``qualified_name`` (or, with ``inherit``, any of its supertypes) at either end."""
    names = {qualified_name} | (supertypes_transitively(model, qualified_name) if inherit else set())
    return [a for a in find_allocations(model, index) if any(p and p[0] in names for p in a["ends"])]


def port_type_mismatches(model: Any, index: ApiIndex | None = None) -> list[dict]:
    """Staged project conformance check (AGENTS.md 1.9): connected ports whose declared types are unrelated.

    OpenSysML v0.9.0 accepts such a connection with no diagnostic (gap G4). Two ports are compatible when their
    types are equal or one specializes the other. Conjugated ports are not handled.
    """
    idx = index or ApiIndex(model)
    up, _ = specialization_graph(model)

    def related(a: str, b: str) -> bool:
        return a == b or a in _closure(b, up) or b in _closure(a, up)

    out = []
    for c in find_connectors(model, "ConnectionUsage", "InterfaceUsage", "FlowUsage", index=idx):
        ends = [p[-1] for p in c["ends"] if p]
        typed = [(e, idx.type_names(e)) for e in ends if idx.by_qn.get(e, {}).get("@type") == "PortUsage"]
        for i in range(len(typed)):
            for j in range(i + 1, len(typed)):
                (ea, ta), (eb, tb) = typed[i], typed[j]
                if ta and tb and not any(related(x, y) for x in ta for y in tb):
                    out.append({"connector": c["id"], "ends": [ea, eb], "types": [ta, tb]})
    return out
