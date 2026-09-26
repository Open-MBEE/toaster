"""Fixture glossaries built in tmp dirs, so tests never depend on the real seed."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import pytest

PKG = Path(__file__).resolve().parents[1]

PREFIX = """@prefix gl: <https://w3id.org/toaster/glossary#> .
@prefix glid: <https://w3id.org/toaster/glossary/id/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
"""

FILE_BYTES = b"canonical source bytes"
FILE_SHA = hashlib.sha256(FILE_BYTES).hexdigest()

SOURCES = PREFIX + f"""
glid:src-canon a gl:Source ; gl:label "Canon" ; gl:edition "1" ; gl:sourceKind gl:File ;
    gl:rank 1 ; gl:sha256 "{FILE_SHA}" ; gl:localPath "canon.txt" .
glid:src-video a gl:Source ; gl:label "Video" ; gl:edition "P3" ; gl:sourceKind gl:Video ;
    gl:rank 8 ; gl:url "https://example.org/v" ; gl:retrievedOn "2026-09-26"^^xsd:date .
glid:src-tutorial a gl:Source ; gl:label "This tutorial" ; gl:edition "test" ; gl:sourceKind gl:Repository ;
    gl:rank 0 ; gl:commit "abc123" .
"""

TERMS = PREFIX + """
glid:term-logical a gl:Term ; gl:label "logical" ; gl:loadBearing true .
glid:term-function a gl:Term ; gl:label "function" ; gl:loadBearing true .
"""

DEFS = {
    "canon": PREFIX + """
glid:def-canon--logical a gl:Definition ; gl:source glid:src-canon ; gl:term glid:term-logical ;
    gl:text "Canon says logical includes the functional view." ; gl:locator "p. 5" ; gl:status gl:confirmed ;
    gl:confirmedBy "Z" .
glid:def-canon--function a gl:Definition ; gl:source glid:src-canon ; gl:term glid:term-function ;
    gl:text "A transformation of inputs to outputs." ; gl:locator "p. 9" ; gl:status gl:proposed .
""",
    "video": PREFIX + """
glid:def-video--logical a gl:Definition ; gl:source glid:src-video ; gl:term glid:term-logical ;
    gl:text "Who is responsible for the functions." ; gl:locator "2:00" ; gl:status gl:proposed .
""",
    "tutorial": PREFIX + """
glid:def-tutorial--logical a gl:Definition ; gl:source glid:src-tutorial ; gl:term glid:term-logical ;
    gl:text "Mechanisms carried by components." ; gl:gloss "Mechanisms carried by logical components." ;
    gl:locator "AGENTS.md" ; gl:status gl:confirmed ; gl:confirmedBy "Z" ;
    gl:differsFrom glid:def-canon--logical ; gl:refines glid:def-video--logical ;
    gl:approvedBy "Z" ; gl:approvalNote "DL-015, 2026-09-26" .
""",
}


def make_root(tmp: Path, *, sources: str = SOURCES, terms: str = TERMS, defs: dict | None = None,
              with_file: bool = True) -> Path:
    root = tmp / "glossary"
    for d in ("vocabulary", "shapes", "queries"):
        shutil.copytree(PKG / d, root / d)
    (root / "sources" / "local").mkdir(parents=True)
    (root / "terms").mkdir()
    (root / "definitions").mkdir()
    (root / "sources" / "sources.ttl").write_text(sources)
    (root / "terms" / "terms.ttl").write_text(terms)
    for name, text in (DEFS if defs is None else defs).items():
        (root / "definitions" / f"{name}.ttl").write_text(text)
    if with_file:
        (root / "sources" / "local" / "canon.txt").write_bytes(FILE_BYTES)
    return root


@pytest.fixture
def root(tmp_path: Path) -> Path:
    return make_root(tmp_path)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    return r
