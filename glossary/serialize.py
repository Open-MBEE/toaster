"""Canonical, byte-deterministic Turtle serialization.

Same house pattern as sysmlv2-testing: every node is a minted IRI (no blank
nodes), so a fully sorted writer is a sufficient canonical form. Identical
triples give byte-identical files regardless of insertion order, which is
what makes diffs and reviews local and the determinism test possible.
"""

from __future__ import annotations

import re
from collections import defaultdict

from rdflib import RDF, Graph, URIRef
from rdflib.namespace import NamespaceManager
from rdflib.term import Node

_PARSE_SAFE_LOCAL = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.\-]*$")


def canonical_turtle(graph: Graph, *, prefixes: dict[str, str]) -> str:
    nm = NamespaceManager(Graph(), bind_namespaces="none")
    for pfx, ns in prefixes.items():
        nm.bind(pfx, ns, override=True, replace=True)

    def n3(node: Node) -> str:
        rendered = node.n3(nm)
        if isinstance(node, URIRef) and not rendered.startswith("<"):
            local = rendered.partition(":")[2]
            if not (_PARSE_SAFE_LOCAL.match(local) and not local.endswith(".")):
                return f"<{node}>"
        return rendered

    def pred_key(pred: Node) -> tuple[int, str]:
        return (0, "") if pred == RDF.type else (1, n3(pred))

    grouped: dict[Node, dict[Node, set[Node]]] = defaultdict(lambda: defaultdict(set))
    for s, p, o in graph:
        grouped[s][p].add(o)

    lines: list[str] = [f"@prefix {pfx}: <{ns}> ." for pfx, ns in sorted(prefixes.items())]
    lines.append("")
    for subject in sorted(grouped, key=n3):
        predicates = grouped[subject]
        clauses: list[str] = []
        for pred in sorted(predicates, key=pred_key):
            pred_str = "a" if pred == RDF.type else n3(pred)
            objects = ",\n        ".join(n3(o) for o in sorted(predicates[pred], key=n3))
            clauses.append(f"    {pred_str} {objects}")
        lines.append(f"{n3(subject)}\n" + " ;\n".join(clauses) + " .")
        lines.append("")
    return "\n".join(lines)
