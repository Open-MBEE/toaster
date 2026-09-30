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


# Round 1 (`subsets`/`redefines`/`references`) and round 2 (`referent`) each hardcoded one more
# named field and were each found, on independent review, to still miss real ties stored under yet
# another field name (round 3: `subject`/`supplier`/`sourceFeature`/`targetFeature`/`annotatedElement`/
# `function`, at minimum) -- enumerating field names does not converge, because any SysML v2
# relationship shape can carry a reference to an id under a name of its own. Round 3's fix (below)
# stops enumerating fields and scans EVERY field of EVERY element instead, keeping only genuine
# `{"@id": ...}`-shaped references (`_dict_refs`) and excluding just containment/self-identity
# bookkeeping (`_STRUCTURAL_FIELDS`) and the KerML `Membership`/`Specialization` relationship-object
# family (`_LINK_BOOKKEEPING_TYPES`, see its own docstring below).

# Fields that describe WHERE an element lives (`owner` and its siblings) or WHAT it owns
# (`owned*`/`member`/`membership`), never an incoming engineering tie -- confirmed empirically
# against `models/ch10-cumulative.sysml` and every fixture in this module's test suite
# (fix/ch10-widget-search, round 3): scanning any of these produces either a trivial self-match
# (``@id``) or a false "tie" from every container of a real tying element to that element. This is
# exactly why the owner chain is already walked UPWARD separately, in `_nearest_requirement_owner`,
# as a different kind of traversal, rather than being treated as an incoming tie here too.
_STRUCTURAL_FIELDS = frozenset({
    "@id",
    "owner", "owningNamespace", "owningRelationship", "owningMembership",
    "owningRelatedElement", "owningType", "owningClassifier", "owningFeature",
    "membershipOwningNamespace", "importOwningNamespace", "featuringType",
    "ownedRelationship", "ownedMembership", "ownedMember", "ownedMemberElement",
    "ownedRelatedElement", "ownedMemberFeature", "ownedFeature", "ownedFeatureMembership",
    "ownedImport", "ownedMemberParameter", "ownedConstraint", "ownedConcern",
    "ownedSpecialization", "ownedSubsetting", "ownedRedefinition", "ownedTyping",
    "ownedReferenceSubsetting", "ownedSubclassification", "ownedEndFeature",
    "ownedFeatureChaining", "ownedPortConjugator", "ownedObjectiveRequirement",
    "ownedResultExpression", "ownedSubjectParameter",
    "member", "membership",
})

# The full, closed set of KerML `Membership` and `Specialization` subtypes -- confirmed
# exhaustively via `javap` against the pinned OMG pilot jar's own class hierarchy
# (`org.omg.sysml.lang.sysml.*`, fix/ch10-widget-search round 3: every one of the jar's 184
# `org.omg.sysml.lang.sysml` interfaces was checked; exactly these 26 extend `Membership` or
# `Specialization`, directly or transitively, plus the two base types themselves -- 28 total --
# and none has a further subtype of its own). An element of one of these kinds exists purely to
# record, a second time and under a different accessor name (`memberElement`,
# `subsettedFeature`/`subsettingFeature`, `redefinedFeature`/`redefiningFeature`,
# `referencedFeature`/`referencingFeature`, `general`/`specific`, `relatedElement`...), a tie a
# "real", user-meaningful element already exposes directly through its own primary field (a
# `ConstraintUsage`'s own `subsets`, a `FeatureReferenceExpression`'s own `referent`, a
# `SatisfyRequirementUsage`'s own `subject`, ...): confirmed empirically for every construct this
# module's test suite covers -- every one still has its own, non-`Membership`/`Specialization`
# element exposing the same tie through the scan below, so skipping these produces no loss of
# coverage, only the removal of a same-tie duplicate under a synthetic id (e.g. `P__C1__c_ss0`)
# that no chapter or test would otherwise ever name. `Dependency` is deliberately NOT in this set,
# even though it, too, is a KerML `Relationship`: unlike `Membership`/`Specialization`, a
# `Dependency` is the ONE, PRIMARY element a `dependency ... from ... to ...;` statement produces
# (confirmed empirically: no second, synthetic element duplicates its own `supplier`/`client`), so
# excluding it would delete the only place that construct's tie is ever recorded.
_LINK_BOOKKEEPING_TYPES = frozenset({
    "Membership", "ActorMembership", "ElementFilterMembership", "EndFeatureMembership",
    "FeatureMembership", "FeatureValue", "FramedConcernMembership", "ObjectiveMembership",
    "OwningMembership", "ParameterMembership", "RequirementConstraintMembership",
    "RequirementVerificationMembership", "ReturnParameterMembership", "StakeholderMembership",
    "StateSubactionMembership", "SubjectMembership", "TransitionFeatureMembership",
    "VariantMembership", "ViewRenderingMembership",
    "Specialization", "ConjugatedPortTyping", "CrossSubsetting", "FeatureTyping",
    "Redefinition", "ReferenceSubsetting", "Subclassification", "Subsetting",
})


def _dict_refs(value: Any) -> list[str]:
    """Every ``@id`` found in ``value`` where ``value`` is itself a ``{"@id": ...}``-shaped dict, or
    a list containing such dicts. Shares ``_raw_refs``'s single-dict-vs-list normalization (the field
    the field-agnostic scan below reads may hold one reference or several), but additionally drops
    any non-dict item: a bare string field (``declaredName``, ``qualifiedName``, ``elementId``, an
    enum like ``direction``) is never a genuine reference no matter what string it happens to hold,
    so it is dropped here rather than risked on a coincidental match -- confirmed empirically that no
    real reference field in the API-JSON export ever uses a bare string shape instead of ``{"@id":
    ...}`` (fix/ch10-widget-search round 3). ``_raw_refs`` keeps bare strings (a legitimate shape for
    its own callers, which read fields -- ``type``, ``subsets``, ``redefines``, ``specializes`` --
    already known to be dict-shaped in practice), so this is a separate, stricter helper rather than
    a change to it.
    """
    items = value if isinstance(value, list) else [value]
    return [item["@id"] for item in items if isinstance(item, dict) and "@id" in item]


# Direct metaclass parent, confirmed via `javap` (fix/ch10-widget-search round 3): each of these
# five is a genuine SUBTYPE of `RequirementDefinition` or `RequirementUsage` in the pinned
# metamodel, not a lookalike sharing only a name -- `ConcernDefinition`/`ViewpointDefinition` extend
# `RequirementDefinition`; `ConcernUsage`/`ViewpointUsage`/`SatisfyRequirementUsage` extend
# `RequirementUsage`. The same javap scan that produced `_LINK_BOOKKEEPING_TYPES` (every one of the
# metamodel's 184 own interfaces) confirms these five are the COMPLETE set: no other interface
# extends `RequirementDefinition`/`RequirementUsage`, and none of the five has a further subtype of
# its own.
_REQUIREMENT_METACLASS_PARENTS: dict[str, tuple[str, ...]] = {
    "ConcernDefinition": ("RequirementDefinition",),
    "ViewpointDefinition": ("RequirementDefinition",),
    "ConcernUsage": ("RequirementUsage",),
    "ViewpointUsage": ("RequirementUsage",),
    "SatisfyRequirementUsage": ("RequirementUsage",),
}


def _is_requirement_owner_type(type_name: str | None) -> bool:
    """True if ``type_name`` (an element's own raw ``@type``) is ``RequirementDefinition``/
    ``RequirementUsage`` or a genuine metaclass SUBTYPE of either -- walked via the same generic
    reachability closure (``_closure``) this module already uses for a model's OWN specialization
    graph (``supertypes_transitively``), just seeded from the metamodel's fixed class hierarchy
    (``_REQUIREMENT_METACLASS_PARENTS``) instead of a model's instance-level ``subsets``/
    ``redefines``/``specializes`` graph -- reusing that one mechanism rather than inventing a second,
    parallel way to walk supertypes. Replaces the old exact ``@type in ("RequirementDefinition",
    "RequirementUsage")`` string match, which missed every one of ``ConcernDefinition``/
    ``ConcernUsage``/``ViewpointDefinition``/``ViewpointUsage``/``SatisfyRequirementUsage`` -- real
    metamodel subtypes, not lookalikes (round 3 review). In particular, a bare ``satisfy r by
    lemma;``'s own ``SatisfyRequirementUsage`` element is now recognized as its own nearest
    requirement (the same inclusive-walk rule ``_nearest_requirement_owner`` already applies to a
    bare ``requirement r :> lemma;``), with no need to walk any further up its owner chain at all.
    """
    if type_name is None:
        return False
    if type_name in ("RequirementDefinition", "RequirementUsage"):
        return True
    return bool({"RequirementDefinition", "RequirementUsage"} & _closure(type_name, _REQUIREMENT_METACLASS_PARENTS))


def _nearest_requirement_owner(element: dict, idx: ApiIndex) -> str | None:
    """Walks ``element``'s own raw ``owner`` chain upward, inclusive of ``element`` itself, and
    returns the qualified name of the nearest ancestor whose ``@type`` is ``RequirementDefinition``/
    ``RequirementUsage`` or a genuine metaclass subtype of either (``_is_requirement_owner_type``),
    or ``None`` if no ancestor (or ``element`` itself) is one."""
    seen: set[str] = set()
    current: dict | None = element
    while current is not None and current["@id"] not in seen:
        seen.add(current["@id"])
        if _is_requirement_owner_type(current.get("@type")):
            return current.get("qualifiedName") or current["@id"]
        owner_id = _ref(current["owner"]) if "owner" in current else None
        current = idx.by_id.get(owner_id) if owner_id else None
    return None


def requirement_ties(model: Any, target_qualified_name: str, index: ApiIndex | None = None) -> list[dict]:
    """Every element, anywhere in the model, whose own field -- ANY field, not a fixed named list --
    holds a genuine ``{"@id": ...}``-shaped reference to ``target_qualified_name``'s own id, as
    ``{tying_element, field, requirement}`` -- ``requirement`` is the nearest ancestor (walking the
    raw ``owner`` chain upward, inclusive of the tying element itself) whose own ``@type`` is
    ``RequirementDefinition``/``RequirementUsage`` or a genuine metaclass subtype of either
    (``ConcernDefinition``, ``ConcernUsage``, ``ViewpointDefinition``, ``ViewpointUsage``,
    ``SatisfyRequirementUsage`` -- confirmed via ``javap`` against the pinned OMG pilot jar to be the
    complete set), or ``None`` if the tie is not owned by a requirement at all.

    This is round 3's fix (fix/ch10-widget-search): rounds 1 and 2 each hardcoded one more named
    field (``subsets``/``redefines``/``references``, then ``referent``) and each was found, on
    independent review, to still miss a real tie stored under yet another field name -- most
    seriously, the chapter's OWN idiom for a genuine tie, ``assert satisfy r by lemma;`` (field
    ``subject`` on the ``SatisfyRequirementUsage`` itself), plus ``dependency ... to lemma;`` (field
    ``supplier``), ``allocate lemma to t;`` (field ``sourceFeature``), ``bind x = lemma;`` (field
    ``targetFeature``), ``metadata M about lemma;`` (field ``annotatedElement``), and an invocation
    expression naming the constraint as a function (field ``function``). Enumerating field names
    does not converge -- there is always one more SysML v2 relationship shape that can carry a
    reference to an id -- so this scans every field of every element instead, keeping only genuine
    dict-shaped references (``_dict_refs``) and excluding only: containment/self-identity bookkeeping
    (``_STRUCTURAL_FIELDS`` -- ``@id`` itself, and the ``owner``/``owned*``/``member``/``membership``
    family, exactly the fields ``_nearest_requirement_owner`` already walks as a SEPARATE traversal,
    never an incoming tie); and the KerML ``Membership``/``Specialization`` relationship-object
    family (``_LINK_BOOKKEEPING_TYPES``), which exists only to record a tie a second time, under a
    different accessor name, that a "real" element (a ``ConstraintUsage``'s own ``subsets``, a
    ``FeatureReferenceExpression``'s own ``referent``, a ``SatisfyRequirementUsage``'s own
    ``subject``, ...) already exposes directly -- confirmed empirically for every construct this
    module's test suite covers, so excluding them costs no coverage, only removes a same-tie
    duplicate under an id no chapter or test would otherwise name.

    Reproduces every prior round's own positive controls unchanged (a general field-agnostic scan is
    a strict superset of a fixed field list), and is still honestly, explicitly scoped: it does NOT
    chase a transitive chain through an intermediate constraint that is itself not owned by any
    requirement (e.g. ``constraint mid :> target;`` sitting outside any requirement, with a
    requirement's own constraint then subsetting ``mid``) -- a direct-reference scan has no reason to
    follow a second hop through an element that is not itself requirement-owned, and this is
    confirmed to remain the one, named scope limit after this round's redesign, not a newly
    discovered one. This is a general search over every element in the model, not specific to any
    one target id, so it works for any target a caller names, not only this tutorial's own
    ``deliveredEnergyBoundedBySupply``.

    Raises ``KeyError`` if ``target_qualified_name`` does not resolve to a real element in the
    model, rather than silently reporting an empty result for a typo'd or renamed target (the same
    "passes for the wrong reason" shape the original bug had, just at a different layer).
    """
    idx = index or ApiIndex(model)
    target = idx.by_qn.get(target_qualified_name)
    if target is None:
        raise KeyError(
            f"requirement_ties: {target_qualified_name!r} does not resolve to any element in the model"
        )
    target_id = target["@id"]
    out = []
    for element in idx.elements:
        if element["@id"] == target_id or element.get("@type") in _LINK_BOOKKEEPING_TYPES:
            continue
        for field, value in element.items():
            if field in _STRUCTURAL_FIELDS:
                continue
            if target_id in _dict_refs(value):
                out.append({
                    "tying_element": element.get("qualifiedName") or element["@id"],
                    "field": field,
                    "requirement": _nearest_requirement_owner(element, idx),
                })
    return out


def tied_to_any_requirement(model: Any, target_qualified_name: str, index: ApiIndex | None = None) -> bool:
    """True if `requirement_ties` finds at least one match owned (directly or transitively) by a
    ``RequirementDefinition``/``RequirementUsage`` or a genuine metaclass subtype of either
    (``ConcernDefinition``, ``ConcernUsage``, ``ViewpointDefinition``, ``ViewpointUsage``,
    ``SatisfyRequirementUsage`` -- ``_is_requirement_owner_type``) -- the honest, broader replacement
    for a bare ``SatisfyRequirementUsage.subsets``-only membership test (`decisions/next-passes.md`
    item 29, `decisions/log.md` DL-070), which can never be `True` for any loadable model and
    separately misses a genuine tie a requirement's own internal constraint, a bare
    `require`/`assume` reference, a `dependency`/`allocate`/`bind`/`metadata` statement, or the
    chapter's own `assert satisfy ... by ...` idiom, can each make directly. Raises ``KeyError`` (via
    `requirement_ties`) if `target_qualified_name` does not resolve to a real element in the model."""
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
    with one element; ``subsets``, ``redefines`` and ``specializes`` are each usually a single ref, but
    ``subsets`` (at least) is exported as a LIST when a constraint subsets more than one thing (e.g.
    ``require constraint c :> other, target;`` -- confirmed empirically, fix/ch10-widget-search round
    2), so callers must handle both shapes; this function already does.
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
