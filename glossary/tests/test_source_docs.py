"""The "Getting the source files" table in glossary/README.md must name every registered file source.

Adding a source, renaming its local file or re-hashing it without updating the README fails here, so
the table cannot drift from sources/sources.ttl.
"""

from __future__ import annotations

from rdflib import RDF

from glossary.graph import load_graph, short_id
from glossary.namespaces import GL, PACKAGE_DIR

README = PACKAGE_DIR / "README.md"


def _file_sources() -> list[tuple[str, str, str]]:
    g = load_graph()
    rows = []
    for s in g.subjects(RDF.type, GL.Source):
        if g.value(s, GL.sourceKind) != GL.File:
            continue
        rows.append((short_id(s), str(g.value(s, GL.localPath)), str(g.value(s, GL.sha256))[:12]))
    return sorted(rows)


def test_there_are_file_sources_to_document() -> None:
    assert len(_file_sources()) >= 7


def test_readme_table_names_every_file_source_and_hash_prefix() -> None:
    text = README.read_text(encoding="utf-8")
    assert "## Getting the source files" in text
    missing = []
    for sid, local_path, prefix in _file_sources():
        if f"`{local_path}`" not in text:
            missing.append(f"{sid}: filename {local_path}")
        if f"`{prefix}`" not in text:
            missing.append(f"{sid}: sha256 prefix {prefix}")
    assert missing == [], "glossary/README.md is out of date with sources.ttl:\n" + "\n".join(missing)
