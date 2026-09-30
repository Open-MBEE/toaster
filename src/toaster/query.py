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
    """``{id, requirement, subject, is_negated}`` for every satisfy (and verify) relationship.

    ``is_negated`` is True for ``assert not satisfy`` (a claim that the subject does NOT meet
    the requirement) and False otherwise, including for a ``verify`` objective, which has no
    ``subject`` to be negated about in the first place. Callers that need positive claims only
    (coverage: has anyone claimed this requirement is actually met) must check both ``subject``
    and ``is_negated``; a negative claim is real evidence about a candidate, not coverage of the
    requirement (``decisions/audits/ch06-layer-audit.md`` F-1, fixed PASS4-009 round 2).
    """
    idx = index or ApiIndex(model)
    return [{"id": e.get("qualifiedName"),
             "requirement": idx.qn(e["subsets"]) if "subsets" in e else None,
             "subject": idx.qn(e["subject"]) if "subject" in e else None,
             "is_negated": bool(e.get("isNegated", False))}
            for e in idx.of_type("SatisfyRequirementUsage")]


_REQUIREMENT_OWNER_TYPES = ("RequirementDefinition", "RequirementUsage")
_TIE_FIELDS = ("subsets", "redefines", "references")


def _nearest_requirement_owner(element: dict, idx: ApiIndex) -> str | None:
    """Walks ``element``'s own raw ``owner`` chain upward, inclusive of ``element`` itself, and
    returns the qualified name of the nearest ancestor whose ``@type`` is ``RequirementDefinition``
    or ``RequirementUsage``, or ``None`` if no ancestor (or ``element`` itself) is one."""
    seen: set[str] = set()
    current: dict | None = element
    while current is not None and current["@id"] not in seen:
        seen.add(current["@id"])
        if current.get("@type") in _REQUIREMENT_OWNER_TYPES:
            return current.get("qualifiedName") or current["@id"]
        owner_id = _ref(current["owner"]) if "owner" in current else None
        current = idx.by_id.get(owner_id) if owner_id else None
    return None


def requirement_ties(model: Any, target_qualified_name: str, index: ApiIndex | None = None) -> list[dict]:
    """Every element, anywhere in the model, whose own ``subsets``, ``redefines`` or ``references``
    property points directly at ``target_qualified_name``'s own id, as ``{tying_element, field,
    requirement}`` -- ``requirement`` is the nearest ancestor (walking the raw ``owner`` chain
    upward, inclusive of the tying element itself) whose own ``@type`` is ``RequirementDefinition``
    or ``RequirementUsage``, or ``None`` if the tie is not owned by a requirement at all.

    Broader than a bare ``SatisfyRequirementUsage.subsets`` membership test: SysML v2's own
    ``assert satisfy`` grammar requires a satisfy's ``subsets`` target to itself be a requirement
    usage (formal/2026-03-02 SS8.3), so a bare ``AssertConstraintUsage``'s own id can never appear
    there for any model that loads at all -- that check reports something guaranteed true by
    construction, not a finding. A requirement can still tie to such a constraint directly, most
    plainly by declaring its own ``require constraint c :> target;`` inside a ``requirement def``,
    which puts ``subsets`` on ``c`` itself (an element owned by the requirement, not a
    ``SatisfyRequirementUsage`` at all -- confirmed by construction, `decisions/next-passes.md`
    item 29, `decisions/log.md` DL-070). Confirmed empirically the same way for the other two
    fields: a ``ref altName references target;`` declared inside a requirement carries the tie via
    ``references`` instead of ``subsets``; a redefining usage (``:>>``/``redefines``) would carry it
    via ``redefines``. This is a general search over every element in the model, not specific to any
    one target id, so it works for any target a caller names, not only this tutorial's own
    ``deliveredEnergyBoundedBySupply``.
    """
    idx = index or ApiIndex(model)
    target = idx.by_qn.get(target_qualified_name)
    if target is None:
        return []
    target_id = target["@id"]
    out = []
    for element in idx.elements:
        for field in _TIE_FIELDS:
            if field in element and target_id in _raw_refs(element[field]):
                out.append({
                    "tying_element": element.get("qualifiedName") or element["@id"],
                    "field": field,
                    "requirement": _nearest_requirement_owner(element, idx),
                })
    return out


def tied_to_any_requirement(model: Any, target_qualified_name: str, index: ApiIndex | None = None) -> bool:
    """True if `requirement_ties` finds at least one match owned (directly or transitively) by a
    ``RequirementDefinition`` or ``RequirementUsage`` -- the honest, broader replacement for a bare
    ``SatisfyRequirementUsage.subsets``-only membership test (`decisions/next-passes.md` item 29,
    `decisions/log.md` DL-070), which can never be `True` for any loadable model and separately
    misses a genuine tie a requirement's own internal constraint can make directly."""
    idx = index or ApiIndex(model)
    return any(t["requirement"] is not None for t in requirement_ties(model, target_qualified_name, idx))


def perform_relationships(model: Any, index: ApiIndex | None = None) -> list[dict]:
    """``{performer, action}`` for each perform action usage: the owner performs the typed or referenced action."""
    idx = index or ApiIndex(model)
    out = []
    for e in idx.of_type("PerformActionUsage"):
        act = e.get("references") or (e.get("type") or [None])[0]
        out.append({"performer": idx.qn(e["owner"]), "action": idx.qn(act) if act else None})
    return out


def requirement_coverage(model: Any, index: ApiIndex | None = None) -> list[dict]:
    """For each NAMED requirement usage: ``{requirement, satisfied_by, failed_by, covered}``.

    ``satisfied_by`` lists candidates with a real POSITIVE claim (``assert satisfy``);
    ``failed_by`` lists candidates with a real NEGATIVE claim (``assert not satisfy``) against
    the same requirement. ``covered`` means a genuine positive claim exists, not merely any claim:
    a negative claim is evidence a candidate fails the requirement, not evidence the requirement
    has been met, so it must never count as coverage (this function previously ignored polarity
    entirely and counted both the same way, reported live in
    ``decisions/audits/ch06-layer-audit.md`` and left unfixed until PASS4-009 round 2 found it
    again against the real ch08 model and fixed it here).

    The requirement list itself is restricted to NAMED requirement usages (``declaredName`` is
    not ``None``): a ``verification def``'s own ``objective { verify X; }`` block is exported as
    an unnamed ``RequirementUsage`` too (the objective's own auto-synthesized wrapper, not a
    design requirement anyone would check coverage on), and including it would report a bare
    bookkeeping artifact as an uncovered requirement.
    """
    idx = index or ApiIndex(model)
    positive: dict[str, list[str]] = defaultdict(list)
    negative: dict[str, list[str]] = defaultdict(list)
    for s in satisfy_relationships(model, idx):
        if not s["requirement"] or not s["subject"]:
            continue
        (negative if s["is_negated"] else positive)[s["requirement"]].append(s["subject"])
    reqs = sorted(
        e["qualifiedName"] for e in idx.of_type("RequirementUsage")
        if e.get("qualifiedName") and e.get("declaredName") is not None
    )
    return [
        {
            "requirement": r,
            "satisfied_by": sorted(positive.get(r, [])),
            "failed_by": sorted(negative.get(r, [])),
            "covered": bool(positive.get(r)),
        }
        for r in reqs
    ]


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


_RAW_SUPERTYPE_FIELDS = ("type", "subsets", "redefines", "specializes")


def _raw_refs(value: Any) -> list[str]:
    """Normalizes a raw API-JSON reference field to a list of ``@id``s. ``value`` may be a single dict
    ref (``{"@id": ...}``), a list of dict refs, a bare id string, or absent (``None``, normalized to
    ``[]``) -- confirmed empirically (2026-09-29, allocate-fix/task6): ``type`` is always a list even
    with one element; ``subsets``, ``redefines`` and ``specializes`` are each a single ref, never a list.
    """
    if value is None:
        return []
    if isinstance(value, list):
        return [_ref(v) for v in value]
    return [_ref(value)]


def supertypes_transitively_raw(
    model: Any, qualified_name: str, index: ApiIndex | None = None
) -> set[str]:
    """Everything ``qualified_name`` (transitively) specializes, is typed by, subsets, or redefines --
    walked directly over the raw API-JSON export's ``type``, ``subsets``, ``redefines`` and
    ``specializes`` reference fields, rather than through ``Symbol.specializations``
    (``specialization_graph``, the graph ``supertypes_transitively`` walks), which only sees NAMED
    elements (built from ``model.query(select=["name"])``).

    An allocation whose owner is anonymous, or a redefining usage with no declared name of its own (e.g.
    ``part redefines heater { ... }``, qualified name like ``P::Better::@0``), still carries these
    reference fields on its own raw element -- confirmed empirically (allocate-fix/task6, a second
    independent hardening round on `conformance._allocate_connector_end_accessibility`): a typed usage
    (``part x : B;``) carries ``"type": [{"@id": "P__B"}]`` (a list); a subsetted usage
    (``part y :> x;``) carries ``"subsets": {"@id": "P__x"}`` (a single ref); a redefining usage
    (``part redefines heater {...}`` or ``part :>> heater : Heater2 {...}``) carries
    ``"redefines": {"@id": "P__Toaster__heater"}`` (a single ref) even when the usage itself is
    completely unnamed; a Definition specializing another Definition (``part def B :> A;``) carries
    ``"specializes": {"@id": "P__A"}`` (a single ref). The walk follows all four fields at every hop, so
    a redefinition chain (a redefining usage whose own ``redefines`` target is itself a redefining usage)
    or a multi-level subsetting/specialization chain is fully covered, not just one hop.

    Confirmed empirically (same task) to reproduce ``supertypes_transitively``'s own results exactly on
    every named case it already handles: a Definition specializing another Definition, a plain Usage
    typed by a Definition (no ``:>`` at all), a subsetting Usage, and a two/three-level specialization
    chain. This is a strict extension of that graph to unnamed elements, not a different algorithm, so a
    caller needing an owner's transitive supertypes/types regardless of whether any element along the
    way is named should prefer this over ``supertypes_transitively``.
    """
    idx = index or ApiIndex(model)
    start = idx.by_qn.get(qualified_name)
    if start is None:
        return set()
    seen_ids: set[str] = set()
    todo = deque([start["@id"]])
    result: set[str] = set()
    while todo:
        current_id = todo.popleft()
        element = idx.by_id.get(current_id)
        if element is None:
            continue
        for field in _RAW_SUPERTYPE_FIELDS:
            for ref_id in _raw_refs(element.get(field)):
                if ref_id in seen_ids:
                    continue
                seen_ids.add(ref_id)
                todo.append(ref_id)
                target = idx.by_id.get(ref_id)
                if target and target.get("qualifiedName"):
                    result.add(target["qualifiedName"])
    return result


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
