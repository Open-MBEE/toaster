"""The committed glossary itself must always pass its own check."""

from __future__ import annotations

from glossary.check import run_check
from glossary.namespaces import GL, REPO_DIR


def test_namespace_term_is_the_property_iri() -> None:
    assert str(GL["term"]) == "https://w3id.org/toaster/glossary#term"


def test_committed_glossary_passes_check() -> None:
    errors = [f for f in run_check() if f.level == "error"]
    assert errors == [], "\n".join(map(str, errors))


def test_repo_dir_is_the_repository_root() -> None:
    assert (REPO_DIR / "pyproject.toml").exists()
