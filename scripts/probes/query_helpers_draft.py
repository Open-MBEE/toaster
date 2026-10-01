"""Proposed helpers for src/toaster/query.py (scratch, verified against ch08-cumulative.sysml)."""
import json, warnings
from collections import defaultdict, deque

def _pc(prop, op, value, inverse=False):
    return {"@type": "PrimitiveConstraint", "property": prop, "operator": op,
            "value": value if isinstance(value, list) else [value], "inverse": inverse}

def query_by_type(model, *types, scope=None, select=None):
    """Named elements whose @type is any of `types` (e.g. 'PartDefinition')."""
    return model.query(scope=scope, select=select, where=_pc("@type", "=", list(types)))

def api_elements(model):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return json.loads(model.to_api_json().content)

def _id(ref):
    return ref["@id"] if isinstance(ref, dict) else ref

class ApiIndex:
    """Index of the API-JSON export; the only route to unnamed connectors/satisfy."""
    def __init__(self, model):
        self.els = api_elements(model)
        self.by = {e["@id"]: e for e in self.els}
    def qn(self, ref):
        """Qualified name of an API-JSON @id (None for synthetic pend/pchain/_rs nodes).
        Never rebuild it with id.replace('__','::'): '_' is escaped ('named_flow' -> 'named_5fflow')."""
        return self.by.get(_id(ref), {}).get("qualifiedName")
    def of_type(self, *types):
        return [e for e in self.els if e.get("@type") in types]
    def end_path(self, end_ref):
        """Qualified-name path a connector end points at: ['ToasterDemo::BreadHandling::loader',
        'ToasterDemo::BreadLoader::bread'] for `loader.bread`, or ['X::a'] for a plain feature."""
        end = self.by[_id(end_ref)]
        rs = end.get("ownedReferenceSubsetting")
        if not rs:
            return []
        target = self.by[_id(self.by[_id(rs)]["referencedFeature"])]
        if "chainingFeature" in target:
            return [self.qn(c) for c in target["chainingFeature"]]
        return [target.get("qualifiedName")]
    def connector_ends(self, e):
        return [self.end_path(r) for r in e.get("connectorEnd", [])]

def _connectors(idx, *types):
    out = []
    for e in idx.of_type(*types):
        out.append({"id": e.get("qualifiedName"), "type": e["@type"], "ends": idx.connector_ends(e)})
    return out

def find_connectors(model, *types, idx=None):
    """[{id, type, ends:[path,...]}] for unnamed+named AllocationUsage/FlowUsage/ConnectionUsage..."""
    return _connectors(idx or ApiIndex(model), *types)

def satisfy_relationships(model, idx=None):
    """[{id, requirement, subject}] from SatisfyRequirementUsage (assert satisfy / verify)."""
    idx = idx or ApiIndex(model)
    return [{"id": e.get("qualifiedName"), "requirement": idx.qn(e["subsets"]) if "subsets" in e else None,
             "subject": idx.qn(e["subject"]) if "subject" in e else None,
             "keyword": e.get("sysx:declaredKeyword", e.get("sysx:declaredPrefix"))}
            for e in idx.of_type("SatisfyRequirementUsage")]

def perform_relationships(model, idx=None):
    """[{performer, action}] from PerformActionUsage (owner performs typed/referenced action)."""
    idx = idx or ApiIndex(model)
    out = []
    for e in idx.of_type("PerformActionUsage"):
        act = e.get("references") or (e.get("type") or [None])[0]
        out.append({"performer": idx.qn(e["owner"]), "action": idx.qn(act) if act else None, "id": e.get("qualifiedName")})
    return out

def spec_graph(model, kinds=None):
    """(up, down): dict id -> set(id). Edges child->parent from Symbol.specializations
    (kinds: specializes, typing, subsets, redefines). Only named elements."""
    up, down = defaultdict(set), defaultdict(set)
    for r in model.query(select=["name"]):
        s = model.get(r.id)
        if s is None:
            continue
        for sp in s.specializations:
            if sp.target_id and (kinds is None or sp.kind in kinds):
                up[r.id].add(sp.target_id); down[sp.target_id].add(r.id)
    return up, down

def _closure(start, edges):
    seen, q = set(), deque([start])
    while q:
        for n in edges.get(q.popleft(), ()):
            if n not in seen:
                seen.add(n); q.append(n)
    return seen

def specializes_transitively(model, fqn, kinds=None):
    """Everything that (transitively) specializes fqn."""
    return _closure(fqn, spec_graph(model, kinds)[1])

def supertypes_transitively(model, fqn, kinds=None):
    """Everything fqn (transitively) specializes."""
    return _closure(fqn, spec_graph(model, kinds)[0])

def allocations_for(model, fqn, inherit=True, idx=None):
    """Allocations whose either end is fqn (or, if inherit, any supertype of fqn)."""
    names = {fqn} | (supertypes_transitively(model, fqn) if inherit else set())
    out = []
    for a in find_connectors(model, "AllocationUsage", idx=idx):
        if any(p and p[0] in names for p in a["ends"]):
            out.append(a)
    return out
