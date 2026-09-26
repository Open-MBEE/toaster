"""Generated gloss regions.

Documents carry one-line glosses of load-bearing terms between marker
comments:

    <!-- gloss:mechanism -->A prescribed input-to-output relation ...<!-- /gloss -->

The text between the markers is generated from the term's tutorialDefinition
(its gl:gloss) and is changed only by changing the glossary. `render` writes
it; `check` fails when it is stale or names a term with no confirmed
tutorialDefinition.
"""

from __future__ import annotations

import re
from pathlib import Path

from rdflib import Graph

from .graph import resolve_term
from .namespaces import GL, RENDER_TARGETS, REPO_DIR

GLOSS_RE = re.compile(r"<!-- gloss:(?P<id>[a-z0-9-]+) -->(?P<body>.*?)<!-- /gloss -->", re.DOTALL)


def target_files(repo: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in RENDER_TARGETS:
        files += sorted(repo.glob(pattern))
    return [f for f in files if f.is_file()]


def expected_gloss(graph: Graph, term_key: str) -> str | None:
    term = resolve_term(graph, term_key)
    if term is None:
        return None
    td = graph.value(term, GL.tutorialDefinition)
    if td is None or graph.value(td, GL.status) != GL.confirmed:
        return None
    gloss = graph.value(td, GL.gloss)
    return None if gloss is None else str(gloss)


def render(graph: Graph, repo: Path = REPO_DIR, *, write: bool = True) -> list[Path]:
    """Rewrite stale gloss regions. Returns the files that changed (or would change)."""
    changed: list[Path] = []
    for f in target_files(repo):
        text = f.read_text(encoding="utf-8")

        def sub(m: re.Match) -> str:
            want = expected_gloss(graph, m.group("id"))
            if want is None:
                return m.group(0)
            return f"<!-- gloss:{m.group('id')} -->{want}<!-- /gloss -->"

        new = GLOSS_RE.sub(sub, text)
        if new != text:
            changed.append(f)
            if write:
                f.write_text(new, encoding="utf-8")
    return changed
