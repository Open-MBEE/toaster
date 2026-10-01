"""Namespaces and paths for the glossary, in one place so nothing drifts."""

from __future__ import annotations

from pathlib import Path

from rdflib import Namespace

# NB: rdflib Namespace has a .term() method, so the property gl:term must be written GL["term"], never GL.term.
GL = Namespace("https://w3id.org/toaster/glossary#")
GLID = Namespace("https://w3id.org/toaster/glossary/id/")

PREFIXES = {
    "gl": str(GL),
    "glid": str(GLID),
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_DIR = PACKAGE_DIR.parent

# The source that holds this tutorial's own refinements (see check.py).
TUTORIAL_SOURCE = GLID["src-tutorial"]

# Files that may carry rendered gloss regions (see render.py).
RENDER_TARGETS = ("AGENTS.md", "CLAUDE.md", ".claude/skills/**/SKILL.md")
