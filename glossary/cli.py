"""Command line for the glossary: SPARQL-backed lookups and integrity checks.

    uv run python -m glossary lookup mechanism
    uv run python -m glossary check
"""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rdflib import RDF, URIRef

from .check import run_check, verify_sources
from .graph import (
    KIND_ORDER,
    gloss_of,
    load_graph,
    local_status,
    primary,
    resolve_source,
    resolve_term,
    run_query,
    short_id,
    tutorial_definitions,
)
from .namespaces import GL, PACKAGE_DIR, REPO_DIR
from .render import render as render_files

app = typer.Typer(add_completion=False, no_args_is_help=True,
                  help="Sources, terms, and the definitions between them.")

RootOpt = typer.Option(PACKAGE_DIR, "--root", hidden=True, help="Glossary directory (tests point this at a fixture).")
RepoOpt = typer.Option(REPO_DIR, "--repo", hidden=True, help="Repository root holding documents with gloss markers.")
JsonOpt = typer.Option(False, "--json", help="Machine-readable output.")


def _emit(obj: object) -> None:
    typer.echo(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False))


def _die(msg: str) -> None:
    typer.echo(msg, err=True)
    raise typer.Exit(2)


def _term_or_die(graph, key: str) -> URIRef:
    term = resolve_term(graph, key)
    if term is None:
        _die(f"no term matching {key!r}; try `python -m glossary terms`")
    return term


KIND_LABEL = {"bridge": "tutorial", "conceptual": "idea", "formal": "formal semantics", "didactic": "story"}


def _def_view(row: dict, selected: dict | None = None) -> dict:
    out = {
        "id": short_id(row["def"]),
        "source": row["sourceLabel"],
        "edition": row["edition"],
        "status": local_status(row["status"]),
        "locator": row["locator"],
        "text": row["text"],
    }
    if selected:
        out["tutorialView"] = selected
    for key in ("quote", "gloss", "confirmedBy", "approvedBy"):
        if key in row:
            out[key] = row[key]
    if "refines" in row:
        out["refines"] = sorted(short_id(x) for x in row["refines"])
    if "differsFrom" in row:
        out["differsFrom"] = sorted(short_id(x) for x in row["differsFrom"])
    return out


def _marked_rows(g, root: Path, t: URIRef) -> list[dict]:
    """Definition rows for a term, marking the edge the tutorial-definition view selects."""
    sure = {short_id(r["def"]): r["kind"] for r in tutorial_definitions(g, root).get(t, [])}
    maybe = {short_id(r["def"]): r["kind"] for r in tutorial_definitions(g, root, include_proposed=True).get(t, [])}
    merged: dict[str, dict] = {}
    for r in run_query(g, root, "lookup", term=t):  # one row per refines/differsFrom target: merge them
        m = merged.setdefault(r["def"], {**r, "refines": set(), "differsFrom": set()})
        for k in ("refines", "differsFrom"):
            if k in r:
                m[k].add(r[k])
    rows = []
    for r in merged.values():
        i = short_id(r["def"])
        for k in ("refines", "differsFrom"):
            if not r[k]:
                del r[k]
        sel = ({"kind": sure[i], "state": "confirmed"} if i in sure
               else {"kind": maybe[i], "state": "preview"} if i in maybe else None)
        rows.append(_def_view(r, sel))
    return rows


@app.command()
def lookup(term: str, as_json: bool = JsonOpt, root: Path = RootOpt) -> None:
    """All definitions of TERM across sources, with locators and status."""
    g = load_graph(root)
    t = _term_or_die(g, term)
    rows = _marked_rows(g, root, t)
    label = str(g.value(t, GL.label))
    if as_json:
        _emit({"term": short_id(t), "label": label, "definitions": rows})
        return
    typer.echo(f"{label}  ({short_id(t)})  {len(rows)} definition(s)")
    for r in rows:
        v = r.get("tutorialView")
        mark = "" if not v else f"  <- tutorial view: {KIND_LABEL[v['kind']]}" + ("" if v["state"] == "confirmed" else " (if confirmed)")
        typer.echo(f"\n[{r['status']}] {r['source']} ({r['edition']}), {r['locator']}{mark}")
        typer.echo(f"  {r['text']}")
        if "quote" in r:
            typer.echo(f"  quote: \"{r['quote']}\"")
        if "refines" in r:
            typer.echo(f"  refines {', '.join(r['refines'])}")
        if "differsFrom" in r:
            typer.echo(f"  differsFrom {', '.join(r['differsFrom'])} (approved by {r.get('approvedBy', 'nobody')})")


@app.command()
def compare(term: str, as_json: bool = JsonOpt, root: Path = RootOpt) -> None:
    """Definitions of TERM side by side, one block per source, showing refines and differsFrom."""
    g = load_graph(root)
    t = _term_or_die(g, term)
    rows = _marked_rows(g, root, t)
    by_source: dict[str, list[dict]] = {}
    for r in rows:
        by_source.setdefault(r["source"], []).append(r)
    if as_json:
        _emit({"term": short_id(t), "sources": by_source})
        return
    for source, defs in by_source.items():
        typer.echo(f"== {source}")
        for r in defs:
            rel = ""
            if "refines" in r:
                rel = f" [refines {', '.join(r['refines'])}]"
            if "differsFrom" in r:
                rel = f" [differsFrom {', '.join(r['differsFrom'])}]"
            typer.echo(f"  {r['locator']}: {r['text']}{rel}")


@app.command()
def terms(as_json: bool = JsonOpt, root: Path = RootOpt) -> None:
    """Every term, with its definition count."""
    g = load_graph(root)
    rows = run_query(g, root, "terms")
    sure = tutorial_definitions(g, root)
    view = [{"id": short_id(r["term"]), "label": r["label"], "definitions": int(r["definitions"]),
             "loadBearing": r.get("loadBearing") is True,
             "tutorialDefinition": (short_id(p["def"]) if (p := primary(sure.get(URIRef(r["term"]), []))) else None)}
            for r in rows]
    if as_json:
        _emit(view)
        return
    for r in view:
        flag = "*" if r["loadBearing"] else " "
        td = "T" if r["tutorialDefinition"] else " "
        typer.echo(f"{flag}{td} {r['definitions']:>2}  {r['label']}  ({r['id']})")


@app.command()
def tutorial(term: str = typer.Argument(None, help="One term, or omit for every term."),
             proposed: bool = typer.Option(False, "--proposed", help="Preview: include proposed edges, as if all were confirmed."),
             as_json: bool = JsonOpt, root: Path = RootOpt) -> None:
    """The tutorial-definition view: per term, the idea (conceptual), the formal semantics and the story (didactic), plus
    the tutorial's own refinement when there is one. Confirmed edges only unless --proposed."""
    g = load_graph(root)
    view = tutorial_definitions(g, root, include_proposed=proposed)
    keys = [_term_or_die(g, term)] if term else sorted(g.subjects(RDF.type, GL.Term), key=lambda x: str(g.value(x, GL.label)).lower())
    out = []
    for t in keys:
        rows = sorted(view.get(t, []), key=lambda r: KIND_ORDER.index(r["kind"]))
        out.append({"term": short_id(t), "label": str(g.value(t, GL.label)),
                    "definitions": [{"kind": r["kind"], "id": short_id(r["def"]), "source": str(g.value(r["source"], GL.label)),
                                     "status": local_status(r["status"]),
                                     "text": str(g.value(r["def"], GL.text)),
                                     "gloss": gloss_of(g, r["def"])} for r in rows]})
    if as_json:
        _emit(out)
        return
    for e in out:
        typer.echo(f"{e['label']}  ({e['term']})" + ("" if e["definitions"] else ": none confirmed"))
        for d in e["definitions"]:
            flag = "" if d["status"] == "confirmed" else " [proposed]"
            typer.echo(f"  {KIND_LABEL[d['kind']]:17s} {d['source']} ({d['id']}){flag}")
            typer.echo(f"      {d['gloss'] or d['text']}")


@app.command()
def sources(as_json: bool = JsonOpt, root: Path = RootOpt) -> None:
    """Every source, with its definition count."""
    g = load_graph(root)
    rows = run_query(g, root, "sources")
    view = [{"id": short_id(r["source"]), "label": r["label"], "edition": r["edition"],
             "kind": local_status(r["kind"]), "definitions": int(r["definitions"])} for r in rows]
    if as_json:
        _emit(view)
        return
    for r in view:
        typer.echo(f"{r['definitions']:>3}  {r['label']} ({r['edition']}, {r['kind']})  [{r['id']}]")


@app.command()
def where(source: str, as_json: bool = JsonOpt, root: Path = RootOpt) -> None:
    """The terms SOURCE defines."""
    g = load_graph(root)
    s = resolve_source(g, source)
    if s is None:
        _die(f"no source matching {source!r}; try `python -m glossary sources`")
    rows = run_query(g, root, "where", source=s)
    view = [{"term": r["label"], "id": short_id(r["term"]), "locator": r["locator"],
             "status": local_status(r["status"])} for r in rows]
    if as_json:
        _emit(view)
        return
    for r in view:
        typer.echo(f"[{r['status']}] {r['term']}  {r['locator']}")


@app.command()
def stats(as_json: bool = JsonOpt, root: Path = RootOpt) -> None:
    """N sources, M terms, D definitions, and the density D / (N x M)."""
    g = load_graph(root)
    src = run_query(g, root, "sources")
    trm = run_query(g, root, "terms")
    n, m = len(src), len(trm)
    d = sum(int(r["definitions"]) for r in src)
    confirmed = sum(1 for r in run_query(g, root, "lookup_all") if local_status(r["status"]) == "confirmed")
    out = {"sources": n, "terms": m, "definitions": d, "confirmed": confirmed,
           "proposed": d - confirmed, "density": round(d / (n * m), 4) if n and m else 0.0}
    if as_json:
        _emit(out)
        return
    typer.echo(f"N={n} sources, M={m} terms, D={d} definitions (confirmed {confirmed}, proposed {d - confirmed}); "
               f"density D/(N*M) = {out['density']}")


@app.command()
def sparql(query: str, as_json: bool = JsonOpt, root: Path = RootOpt) -> None:
    """Run a query: a name in queries/, a path to a .rq file, or inline SPARQL text."""
    g = load_graph(root)
    named = root / "queries" / f"{query}.rq"
    path = Path(query)
    if named.exists():
        text = named.read_text(encoding="utf-8")
    elif path.suffix == ".rq" and path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = query
    if "ORDER BY" not in text.upper():
        typer.echo("note: no ORDER BY; row order is not guaranteed", err=True)
    result = g.query(text)
    rows = [{str(k): str(v) for k, v in r.asdict().items()} for r in result]
    if as_json:
        _emit(rows)
        return
    for r in rows:
        typer.echo("\t".join(f"{k}={v}" for k, v in r.items()))


@app.command()
def check(as_json: bool = JsonOpt, root: Path = RootOpt, repo: Path = RepoOpt) -> None:
    """Validate the graph and rendered glosses. Exits 1 on any error; passes without the source PDFs."""
    findings = run_check(root, repo)
    errors = [f for f in findings if f.level == "error"]
    if as_json:
        _emit({"ok": not errors, "findings": [f.__dict__ for f in findings]})
    else:
        for f in findings:
            typer.echo(str(f))
        typer.echo("glossary check: " + ("FAILED" if errors else "ok")
                   + f" ({len(errors)} error(s), {len(findings) - len(errors)} warning(s))")
    raise typer.Exit(1 if errors else 0)


@app.command("verify-sources")
def verify_sources_cmd(as_json: bool = JsonOpt, root: Path = RootOpt) -> None:
    """Verify every registered source hash against glossary/sources/local/ (needs the originals)."""
    findings = verify_sources(root)
    if as_json:
        _emit({"ok": not findings, "findings": [f.__dict__ for f in findings]})
    else:
        for f in findings:
            typer.echo(str(f))
        typer.echo("verify-sources: " + ("FAILED" if findings else "ok"))
    raise typer.Exit(1 if findings else 0)


@app.command("render")
def render_cmd(dry_run: bool = typer.Option(False, "--dry-run", help="List files that would change; exit 1 if any."),
               root: Path = RootOpt, repo: Path = RepoOpt) -> None:
    """Write tutorial glosses between <!-- gloss:ID --> markers in AGENTS.md, CLAUDE.md and skills."""
    changed = render_files(load_graph(root), repo, root, write=not dry_run)
    for f in changed:
        typer.echo(("would change " if dry_run else "updated ") + str(f.relative_to(repo)))
    if not changed:
        typer.echo("render: nothing to change")
    raise typer.Exit(1 if (dry_run and changed) else 0)
