"""Integrity checks for the glossary graph.

SHACL covers cardinality, datatype and pattern (shapes/). Everything that
relates one part of the graph to another lives here: the bipartite invariant,
orphans, the confirmation rule, the refinement rule, source rules, source
hashes, and drift of rendered gloss regions in documents.

`check` passes in a fresh worktree or CI where the gitignored source PDFs are
absent: hashes are verified only for files that are present, and absent ones
are warnings. `verify_sources` (the `verify-sources` command) requires them.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from pyshacl import validate
from rdflib import RDF, Graph, Literal, URIRef

from .graph import (
    KIND_ORDER,
    MAX_GLOSS,
    gloss_of,
    load_graph,
    load_shapes,
    load_vocabulary,
    primary,
    short_id,
    tutorial_definitions,
)
from .namespaces import GL, PACKAGE_DIR, REPO_DIR, TUTORIAL_SOURCE
from .render import GLOSS_RE, expected_gloss, target_files

# A confirmation or approval must come from a human. This is a guard against
# accidents, not a security control: the rule is enforced by review.
_AGENT_MARKERS = ("claude", "agent", "gpt", "bot", "assistant", "llm")


@dataclass(frozen=True)
class Finding:
    level: str  # "error" | "warning"
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.level.upper()} {self.code}: {self.message}"


def _err(code: str, msg: str) -> Finding:
    return Finding("error", code, msg)


def _warn(code: str, msg: str) -> Finding:
    return Finding("warning", code, msg)


def _shacl(graph: Graph, root: Path) -> list[Finding]:
    conforms, _rg, text = validate(
        graph, shacl_graph=load_shapes(root), ont_graph=load_vocabulary(root),
        inference="none", abort_on_first=False,
    )
    if conforms:
        return []
    msgs = sorted({m.strip() for m in re.findall(r"Message: (.+)", text)})
    return [_err("shacl", m) for m in msgs] or [_err("shacl", "shape violation (see pyshacl report)")]


def _node_type(graph: Graph, node: object) -> str | None:
    if (node, RDF.type, GL.Source) in graph:
        return "source"
    if (node, RDF.type, GL.Term) in graph:
        return "term"
    return None


def _bipartite(graph: Graph) -> list[Finding]:
    out = []
    for s, p, o in graph:
        if not isinstance(o, URIRef) or p == RDF.type:
            continue
        ts, to = _node_type(graph, s), _node_type(graph, o)
        if ts and ts == to:
            out.append(_err("bipartite", f"{short_id(s)} -[{short_id(p)}]-> {short_id(o)} links two "
                            f"{ts} nodes; only definition edges may connect sources and terms"))
    return out


def _orphans(graph: Graph) -> list[Finding]:
    out = []
    defined_terms = {graph.value(d, GL["term"]) for d in graph.subjects(RDF.type, GL.Definition)}
    defined_sources = {graph.value(d, GL.source) for d in graph.subjects(RDF.type, GL.Definition)}
    for t in graph.subjects(RDF.type, GL.Term):
        if t not in defined_terms:
            out.append(_err("orphan-term", f"term {short_id(t)} has no definition edge"))
    for s in graph.subjects(RDF.type, GL.Source):
        if s not in defined_sources:
            out.append(_err("orphan-source", f"source {short_id(s)} defines no term"))
    return out


def _is_agent(name: str) -> bool:
    low = name.lower()
    return any(m in low for m in _AGENT_MARKERS)


def _confirmation(graph: Graph) -> list[Finding]:
    out = []
    for d in graph.subjects(RDF.type, GL.Definition):
        status = graph.value(d, GL.status)
        who = graph.value(d, GL.confirmedBy)
        if status == GL.confirmed:
            if who is None:
                out.append(_err("confirmed-by", f"{short_id(d)} is confirmed but has no gl:confirmedBy"))
            elif _is_agent(str(who)):
                out.append(_err("confirmed-by", f"{short_id(d)} confirmedBy {who!s}: only a human confirms"))
        elif who is not None:
            out.append(_err("confirmed-by", f"{short_id(d)} has gl:confirmedBy but is not confirmed"))
    return out


def _tutorial_view(graph: Graph, root: Path) -> list[Finding]:
    out = []
    unresolved = []
    preview = tutorial_definitions(graph, root, include_proposed=True)
    confirmed = tutorial_definitions(graph, root)
    for t in sorted(graph.subjects(RDF.type, GL.Term)):
        label = short_id(t)
        for kind in KIND_ORDER:
            rows = [r for r in preview.get(t, []) if r["kind"] == kind]
            if len(rows) > 1:
                ids = ", ".join(short_id(r["def"]) for r in rows)
                out.append(_err("tutorial-definition", f"{label}: ambiguous {kind} definition ({ids}); set gl:preferred among same-source edges or adjust gl:rank"))
        row = primary(confirmed.get(t, []))
        if row is None:
            if graph.value(t, GL.loadBearing) == Literal(True):
                unresolved.append(label)
        elif gloss_of(graph, row["def"]) is None:
            out.append(_err("tutorial-definition", f"{label}: {short_id(row['def'])} has no gl:gloss and its text is over {MAX_GLOSS} characters"))
    if unresolved:
        out.append(_warn("tutorial-definition", f"{len(unresolved)} load-bearing term(s) have no confirmed definition yet"))
    return out


def _refinement(graph: Graph) -> list[Finding]:
    out = []
    for d in graph.subjects(RDF.type, GL.Definition):
        src = graph.value(d, GL.source)
        for prop in (GL.refines, GL.differsFrom):
            for target in graph.objects(d, prop):
                pname = "refines" if prop == GL.refines else "differsFrom"
                if src != TUTORIAL_SOURCE:
                    out.append(_err("refinement", f"{short_id(d)} uses gl:{pname} but is not a tutorial definition"))
                if graph.value(target, GL.source) == TUTORIAL_SOURCE:
                    out.append(_err("refinement", f"{short_id(d)} gl:{pname} another tutorial definition {short_id(target)}"))
                if prop == GL.differsFrom and graph.value(target, GL["term"]) != graph.value(d, GL["term"]):
                    out.append(_err("refinement", f"{short_id(d)} gl:differsFrom {short_id(target)}, which defines a different term; "
                                    "a departure is from the same term's canonical definition"))
        if (d, GL.differsFrom, None) in graph:
            who, note = graph.value(d, GL.approvedBy), graph.value(d, GL.approvalNote)
            if who is None or note is None:
                out.append(_err("unapproved-differs", f"{short_id(d)} differsFrom a canonical definition without gl:approvedBy and gl:approvalNote"))
            elif _is_agent(str(who)):
                out.append(_err("unapproved-differs", f"{short_id(d)} approvedBy {who!s}: only a human approves a departure"))
    return out


def _sources(graph: Graph) -> list[Finding]:
    out = []
    need = {
        GL.File: (GL.sha256, GL.localPath),
        GL.Video: (GL.url, GL.retrievedOn),
        GL.Repository: (GL.commit,),
    }
    for s in graph.subjects(RDF.type, GL.Source):
        kind = graph.value(s, GL.sourceKind)
        for prop in need.get(kind, ()):
            if graph.value(s, prop) is None:
                out.append(_err("source-fields", f"{short_id(s)} ({short_id(kind)}) needs gl:{str(prop).split('#')[1]}"))
    return out


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _hashes(graph: Graph, root: Path, *, require: bool) -> list[Finding]:
    out = []
    for s in graph.subjects(RDF.type, GL.Source):
        if graph.value(s, GL.sourceKind) != GL.File:
            continue
        rel, want = graph.value(s, GL.localPath), graph.value(s, GL.sha256)
        if rel is None or want is None:
            continue
        path = root / "sources" / "local" / str(rel)
        if not path.exists():
            out.append((_err if require else _warn)("source-absent",
                       f"{short_id(s)}: {rel} is not in glossary/sources/local/ (hash not verified)"))
        elif sha256_of(path) != str(want):
            out.append(_err("source-hash", f"{short_id(s)}: {rel} does not match its registered sha256"))
    return out


_WS = re.compile(r"\s+")
_PUNCT = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-",
                        "\u00ad": "", "\ufb01": "fi", "\ufb02": "fl", "\u00a0": " "})


def normalize(text: str) -> str:
    """Whitespace-, hyphenation- and quote-insensitive form for comparing an excerpt to a page."""
    t = text.translate(_PUNCT)
    t = re.sub(r"-\s*\n\s*", "", t)
    return _WS.sub(" ", t).strip().lower()


def pdf_page_text(path: Path, page: int) -> str | None:
    if shutil.which("pdftotext") is None:
        return None
    r = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(path), "-"],
                       capture_output=True, text=True, check=False)
    return r.stdout if r.returncode == 0 else None


def _quotes(graph: Graph, root: Path, *, require: bool) -> list[Finding]:
    """Verify each gl:quote occurs on its gl:pdfPage, for file sources whose original is present."""
    out = []
    for d in graph.subjects(RDF.type, GL.Definition):
        quote, page = graph.value(d, GL.quote), graph.value(d, GL.pdfPage)
        if quote is None or page is None:
            continue
        src = graph.value(d, GL.source)
        rel = graph.value(src, GL.localPath)
        if graph.value(src, GL.sourceKind) != GL.File or rel is None:
            continue
        path = root / "sources" / "local" / str(rel)
        if not path.exists():
            continue  # absence is reported by _hashes
        text = pdf_page_text(path, int(page))
        if text is None:
            out.append((_err if require else _warn)("quote-unchecked", f"{short_id(d)}: could not read PDF page {page} (pdftotext missing?)"))
        elif normalize(str(quote)) not in normalize(text):
            out.append(_err("quote-not-on-page", f"{short_id(d)}: quote not found on PDF page {page} of {rel}"))
    return out


def _markers(graph: Graph, repo: Path, root: Path) -> list[Finding]:
    out = []
    for f in target_files(repo):
        text = f.read_text(encoding="utf-8")
        for m in GLOSS_RE.finditer(text):
            term_key, inner = m.group("id"), m.group("body")
            want = expected_gloss(graph, term_key, root)
            rel = f.relative_to(repo)
            if want is None:
                out.append(_err("gloss-drift", f"{rel}: marker {term_key!r} has no confirmed tutorial definition"))
            elif inner != want:
                out.append(_err("gloss-drift", f"{rel}: marker {term_key!r} is stale; run `python -m glossary render`"))
    return out


def run_check(root: Path = PACKAGE_DIR, repo: Path = REPO_DIR) -> list[Finding]:
    graph = load_graph(root)
    findings = _shacl(graph, root)
    for fn in (_bipartite, _orphans, _confirmation, _refinement, _sources):
        findings += fn(graph)
    findings += _hashes(graph, root, require=False)
    findings += _quotes(graph, root, require=False)
    findings += _tutorial_view(graph, root)
    findings += _markers(graph, repo, root)
    return findings


def verify_sources(root: Path = PACKAGE_DIR) -> list[Finding]:
    g = load_graph(root)
    return _hashes(g, root, require=True) + _quotes(g, root, require=True)
