"""Loading, saving and querying the glossary graph.

Data lives in Turtle under the glossary directory: the source register, the
term nodes, and one file of definition edges per source. Every write goes
through save_graph, so a file on disk is always exactly what canonical_turtle
would produce from its own triples.
"""

from __future__ import annotations

from pathlib import Path

from rdflib import RDF, Graph, Literal, URIRef

from .namespaces import GL, GLID, PACKAGE_DIR, PREFIXES
from .serialize import canonical_turtle


def data_files(root: Path) -> list[Path]:
    files = [root / "sources" / "sources.ttl", root / "terms" / "terms.ttl"]
    files += sorted((root / "definitions").glob("*.ttl"))
    return [f for f in files if f.exists()]


def load_graph(root: Path = PACKAGE_DIR) -> Graph:
    g = Graph()
    for f in data_files(root):
        g.parse(f, format="turtle")
    return g


def load_vocabulary(root: Path = PACKAGE_DIR) -> Graph:
    g = Graph()
    for f in sorted((root / "vocabulary").glob("*.ttl")):
        g.parse(f, format="turtle")
    return g


def load_shapes(root: Path = PACKAGE_DIR) -> Graph:
    g = Graph()
    for f in sorted((root / "shapes").glob("*.shapes.ttl")):
        g.parse(f, format="turtle")
    return g


def save_graph(graph: Graph, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_turtle(graph, prefixes=PREFIXES), encoding="utf-8")


def query_text(root: Path, name: str) -> str:
    return (root / "queries" / f"{name}.rq").read_text(encoding="utf-8")


def run_query(graph: Graph, root: Path, name: str, **bindings: URIRef | Literal) -> list[dict]:
    """Run a named .rq file; return rows as plain dicts (unbound keys omitted)."""
    q = query_text(root, name)
    rows = graph.query(q, initBindings={k: v for k, v in bindings.items()})
    out = []
    for row in rows:
        out.append({str(k): _plain(v) for k, v in row.asdict().items()})
    return out


MAX_GLOSS = 240


def tutorial_definitions(graph: Graph, root: Path, *, include_proposed: bool = False) -> dict[URIRef, list[dict]]:
    """The tutorial-definition view: term -> the edge(s) chosen by citation order.

    One row per term is the norm; more than one is an ambiguity `check` reports. With include_proposed
    the view previews what it would be if every proposed edge were confirmed.
    """
    q = query_text(root, "tutorial_definitions")
    out: dict[URIRef, list[dict]] = {}
    for row in graph.query(q, initBindings={"includeProposed": Literal(include_proposed)}):
        out.setdefault(row.term, []).append({"def": row["def"], "source": row.source, "status": row.status})
    return out


def gloss_of(graph: Graph, definition: URIRef) -> str | None:
    """The one-line form: gl:gloss, else the text when it fits."""
    g = graph.value(definition, GL.gloss)
    if g is not None:
        return str(g)
    t = graph.value(definition, GL.text)
    return str(t) if t is not None and len(str(t)) <= MAX_GLOSS else None


def _plain(node: object) -> str | bool:
    if isinstance(node, Literal):
        return node.toPython() if isinstance(node.toPython(), bool) else str(node)
    return str(node)


def short_id(iri: object) -> str:
    """glid:term-mechanism -> term-mechanism; other IRIs are returned whole."""
    s = str(iri)
    return s.removeprefix(str(GLID))


def local_status(iri: object) -> str:
    s = str(iri)
    return s.removeprefix(str(GL))


def resolve_term(graph: Graph, key: str) -> URIRef | None:
    """Find a term by id (`term-mechanism` or `mechanism`) or by label, case-insensitively."""
    k = key.strip().lower()
    for term in graph.subjects(RDF.type, GL.Term):
        tid = short_id(term).lower()
        label = str(graph.value(term, GL.label) or "").lower()
        if k in (tid, tid.removeprefix("term-"), label):
            return term
    return None


def resolve_source(graph: Graph, key: str) -> URIRef | None:
    k = key.strip().lower()
    for src in graph.subjects(RDF.type, GL.Source):
        sid = short_id(src).lower()
        label = str(graph.value(src, GL.label) or "").lower()
        if k in (sid, sid.removeprefix("src-"), label):
            return src
    return None
