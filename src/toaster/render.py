"""Diagram rendering helpers. WP-4 implements SysMLD exporter."""

import subprocess
from pathlib import Path
from typing import Any


def model_to_dot(model: Any, title: str = "model") -> str:
    """Generate DOT source for the part hierarchy from model.query() elements.

    WP-1 probe result: opensysml v0.9.0 has no native render-form DOT.
    DOT is generated directly from model.query() output.

    Nodes: PartDefinition (dashed border if abstract).
    Edges: composition (diamond arrowhead from owner to usage),
           typing (dashed open arrow from usage to its PartDefinition type).
    """
    lines = [
        f'digraph "{title}" {{',
        "  rankdir=TB;",
        '  graph [fontname="Helvetica"];',
        '  node [shape=box fontname="Helvetica"];',
        '  edge [fontname="Helvetica"];',
    ]
    for e in model.query():
        d = e.as_dict()
        etype = d.get("@type", "")
        qname = d.get("qualifiedName", d.get("@id", ""))
        dname = d.get("declaredName") or d.get("name", "")
        is_abstract = d.get("isAbstract") == "true"

        if etype == "PartDefinition":
            style = 'style="dashed" ' if is_abstract else ""
            label = f"«abstract»\\n{dname}" if is_abstract else dname
            lines.append(f'  "{qname}" [{style}label="{label}"];')
        elif etype == "PartUsage":
            owner = d.get("owner", "")
            part_type = d.get("type", "")
            if owner:
                lines.append(
                    f'  "{owner}" -> "{qname}" [label="{dname}" arrowhead=diamond];'
                )
            if part_type:
                lines.append(
                    f'  "{qname}" -> "{part_type}" [style=dashed arrowhead=open];'
                )
    lines.append("}")
    return "\n".join(lines)


def render_dot(src: str | Path, out: str | Path) -> None:
    """Render a DOT source file or string to SVG via Graphviz."""
    src_path = Path(src) if isinstance(src, Path) else None
    if src_path and src_path.exists():
        subprocess.run(
            ["dot", "-Tsvg", str(src_path), "-o", str(out)],
            check=True,
        )
    else:
        subprocess.run(
            ["dot", "-Tsvg", "-o", str(out)],
            input=str(src),
            text=True,
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
