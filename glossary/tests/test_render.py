from __future__ import annotations

from pathlib import Path

from glossary.check import run_check
from glossary.graph import load_graph
from glossary.render import render

GLOSS = "Mechanisms carried by logical components."


def write(repo: Path, body: str) -> Path:
    f = repo / "AGENTS.md"
    f.write_text(body)
    return f


def test_stale_marker_is_an_error_and_render_fixes_it(root: Path, repo: Path) -> None:
    f = write(repo, "Logical: <!-- gloss:logical -->old text<!-- /gloss -->\n")
    assert any(x.code == "gloss-drift" for x in run_check(root, repo))
    changed = render(load_graph(root), repo, root)
    assert changed == [f]
    assert f.read_text() == f"Logical: <!-- gloss:logical -->{GLOSS}<!-- /gloss -->\n"
    assert not [x for x in run_check(root, repo) if x.level == "error"]


def test_render_is_idempotent(root: Path, repo: Path) -> None:
    write(repo, "<!-- gloss:logical -->x<!-- /gloss -->")
    render(load_graph(root), repo, root)
    assert render(load_graph(root), repo, root) == []


def test_marker_for_unconfirmed_term_is_an_error(root: Path, repo: Path) -> None:
    write(repo, "<!-- gloss:function -->whatever<!-- /gloss -->")
    assert any(x.code == "gloss-drift" for x in run_check(root, repo))


def test_marker_for_unknown_term_is_an_error(root: Path, repo: Path) -> None:
    write(repo, "<!-- gloss:nothing -->x<!-- /gloss -->")
    assert any(x.code == "gloss-drift" for x in run_check(root, repo))


def test_text_outside_markers_is_untouched(root: Path, repo: Path) -> None:
    body = "before <!-- gloss:logical -->x<!-- /gloss --> after\nno markers here\n"
    f = write(repo, body)
    render(load_graph(root), repo, root)
    assert f.read_text().startswith("before ") and f.read_text().endswith(" after\nno markers here\n")
