from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph
from typer.testing import CliRunner

from glossary.cli import app
from glossary.graph import load_graph, save_graph
from glossary.namespaces import PREFIXES
from glossary.serialize import canonical_turtle

runner = CliRunner()


def run(root: Path, *args: str, repo: Path | None = None):
    extra = ["--repo", str(repo)] if repo else []
    return runner.invoke(app, [*args, "--root", str(root), *extra])


def test_lookup_returns_every_edge_ordered_and_deterministic(root: Path) -> None:
    a = run(root, "lookup", "logical", "--json")
    b = run(root, "lookup", "logical", "--json")
    assert a.exit_code == 0 and a.output == b.output
    data = json.loads(a.output)
    assert [d["source"] for d in data["definitions"]] == ["Canon", "This tutorial", "Video"]
    tut = [d for d in data["definitions"] if d.get("tutorialDefinition") == "confirmed"]
    assert len(tut) == 1 and tut[0]["differsFrom"] == ["def-canon--logical"]


def test_lookup_accepts_id_or_label_and_reports_unknown(root: Path) -> None:
    assert run(root, "lookup", "term-logical").exit_code == 0
    assert run(root, "lookup", "LOGICAL").exit_code == 0
    assert run(root, "lookup", "nonsense").exit_code == 2


def test_compare_groups_by_source(root: Path) -> None:
    data = json.loads(run(root, "compare", "logical", "--json").output)
    assert set(data["sources"]) == {"Canon", "This tutorial", "Video"}


def test_terms_sources_where(root: Path) -> None:
    assert {t["id"] for t in json.loads(run(root, "terms", "--json").output)} == {"term-logical", "term-function"}
    assert len(json.loads(run(root, "sources", "--json").output)) == 3
    rows = json.loads(run(root, "where", "canon", "--json").output)
    assert {r["term"] for r in rows} == {"logical", "function"}


def test_stats_reports_density(root: Path) -> None:
    s = json.loads(run(root, "stats", "--json").output)
    assert (s["sources"], s["terms"], s["definitions"]) == (3, 2, 4)
    assert s["confirmed"] == 2 and s["proposed"] == 2
    assert s["density"] == round(4 / (3 * 2), 4)


def test_sparql_inline_and_named(root: Path) -> None:
    q = "PREFIX gl: <https://w3id.org/toaster/glossary#> SELECT ?t WHERE { ?t a gl:Term } ORDER BY ?t"
    assert len(json.loads(run(root, "sparql", q, "--json").output)) == 2
    assert run(root, "sparql", "terms").exit_code == 0


def test_check_exit_codes(root: Path, repo: Path, tmp_path: Path) -> None:
    assert run(root, "check", repo=repo).exit_code == 0
    bad = tmp_path / "bad"
    from .conftest import DEFS, make_root
    d = dict(DEFS)
    d["video"] = d["video"].replace('gl:locator "2:00" ;', "")
    assert run(make_root(bad, defs=d), "check", repo=repo).exit_code == 1


def test_render_dry_run_exit_code(root: Path, repo: Path) -> None:
    (repo / "AGENTS.md").write_text("<!-- gloss:logical -->stale<!-- /gloss -->")
    assert run(root, "render", "--dry-run", repo=repo).exit_code == 1
    assert run(root, "render", repo=repo).exit_code == 0
    assert run(root, "render", "--dry-run", repo=repo).exit_code == 0


def test_saved_turtle_is_canonical(root: Path, tmp_path: Path) -> None:
    g = load_graph(root)
    out = tmp_path / "out.ttl"
    save_graph(g, out)
    again = Graph().parse(out, format="turtle")
    assert canonical_turtle(again, prefixes=PREFIXES) == out.read_text()
