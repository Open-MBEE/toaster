"""Diagram rendering helpers. WP-4 implements SysMLD exporter."""

import json
import subprocess
from pathlib import Path
from typing import Any


def render_dot(src: str | Path, out: str | Path) -> None:
    """Render a DOT source file to SVG."""
    subprocess.run(
        ["dot", "-Tsvg", str(src), "-o", str(out)],
        check=True,
    )


def render_sysmld(intent: str | Path, out: str | Path) -> None:
    """Render a SysMLD intent JSON file to SVG via sysmld CLI."""
    sysmld_file = Path(str(out).replace(".svg", ".sysmld"))
    subprocess.run(["sysmld", "interconnection", str(intent)], check=True)
    subprocess.run(["sysmld", "render", str(sysmld_file)], check=True)


def render_action_flow(model: Any, name: str, out: str | Path) -> None:
    """Render an action flow diagram for a named action def to SVG via PlantUML."""
    puml_path = Path(str(out).replace(".svg", ".puml"))
    # opensysml CLI renders to plantuml; java renders to SVG
    import opensysml  # type: ignore[import]
    # WP-4 implements the CLI call; stub raises to surface missing impl
    raise NotImplementedError("render_action_flow: implement in WP-4 using opensysml CLI")


def build_interconnection_intent(model: Any, fqn: str) -> dict:
    """Build SysMLD intent dict from model for the given qualified name. WP-4."""
    raise NotImplementedError("build_interconnection_intent: implement in WP-4")
