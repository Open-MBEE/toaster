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
    """Render a DOT source file or string to SVG via Graphviz.

    capture_output=True routes stderr through a pipe, preventing gRPC's
    fork-detection messages from reaching the notebook's stderr stream.
    Real graphviz errors are still surfaced via CalledProcessError.
    """
    src_path = Path(src) if isinstance(src, Path) else None
    if src_path and src_path.exists():
        r = subprocess.run(
            ["dot", "-Tsvg", str(src_path), "-o", str(out)],
            capture_output=True,
        )
    else:
        r = subprocess.run(
            ["dot", "-Tsvg", "-o", str(out)],
            input=str(src),
            text=True,
            capture_output=True,
        )
    if r.returncode != 0:
        raise subprocess.CalledProcessError(r.returncode, "dot", stderr=r.stderr)


def build_interconnection_intent(model: Any, fqn: str) -> dict:
    """Extract interconnection data from model for a composite part or assembly.

    Returns a dict with:
      title    — the qualified name
      parts    — list of {name, type} for owned PartUsage elements
      flows    — list of {source, target} using sysx:sourceText from FlowUsage ends
      allocs   — list of {source, target} using sysx:sourceText from AllocationUsage ends
    """
    import json as _json
    import warnings

    # Owned parts via model.query() PartUsage
    parts = []
    for e in model.query():
        d = e.as_dict()
        if d.get("@type") == "PartUsage" and d.get("owner") == fqn:
            parts.append({
                "name": d.get("declaredName") or d.get("name", ""),
                "type": (d.get("type") or "").split("::")[-1],
            })

    flows: list[dict] = []
    allocs: list[dict] = []

    # FlowUsage and AllocationUsage via to_api_json (experimental)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        raw = model.to_api_json().content
    data = _json.loads(raw)
    by_id = {e["@id"]: e for e in data if "@id" in e}

    for elem in data:
        etype = elem.get("@type", "")
        ends = elem.get("connectorEnd", [])
        if len(ends) != 2:
            continue
        src_text = by_id.get(ends[0]["@id"], {}).get("sysx:sourceText", "")
        tgt_text = by_id.get(ends[1]["@id"], {}).get("sysx:sourceText", "")
        if not (src_text and tgt_text):
            continue
        if etype == "FlowUsage":
            flows.append({"source": src_text, "target": tgt_text})
        elif etype == "AllocationUsage":
            allocs.append({"source": src_text, "target": tgt_text})

    return {"title": fqn, "parts": parts, "flows": flows, "allocs": allocs}


def render_sysmld(intent: dict | str | Path, out: str | Path) -> None:
    """Render an interconnection intent dict (or JSON file) to SVG via Graphviz DOT.

    SysMLD CLI is a pilot visualizer and not a build dependency; this function
    implements the same semantics using DOT/Graphviz, which is already required.
    """
    import json as _json

    if isinstance(intent, (str, Path)) and Path(intent).exists():
        with open(intent) as f:
            data = _json.load(f)
    else:
        data = intent  # type: ignore[assignment]

    title = str(data.get("title", "interconnection")).split("::")[-1]
    parts = data.get("parts", [])
    flows = data.get("flows", [])
    allocs = data.get("allocs", [])
    part_names = {p["name"] for p in parts}

    lines = [
        f'digraph "{title}" {{',
        "  rankdir=LR;",
        f'  label="{title}";',
        "  labelloc=t;",
        '  graph [fontname="Helvetica"];',
        '  node [shape=box fontname="Helvetica" style=filled fillcolor=white];',
        '  edge [fontname="Helvetica"];',
    ]
    for p in parts:
        label = f'{p["name"]}\\n:{p["type"]}' if p.get("type") else p["name"]
        lines.append(f'  "{p["name"]}" [label="{label}"];')
    for flow in flows:
        src = str(flow.get("source", ""))
        tgt = str(flow.get("target", ""))
        src_part = src.split(".")[0]
        tgt_part = tgt.split(".")[0]
        if src_part in part_names and tgt_part in part_names:
            src_port = src.split(".")[1] if "." in src else ""
            tgt_port = tgt.split(".")[1] if "." in tgt else ""
            lbl = f"{src_port}→{tgt_port}" if src_port else ""
            lines.append(f'  "{src_part}" -> "{tgt_part}" [label="{lbl}" arrowhead=open];')
    for alloc in allocs:
        src = str(alloc.get("source", ""))
        tgt = str(alloc.get("target", ""))
        if src and tgt:
            lines.append(f'  "{src}" -> "{tgt}" [style=dashed label="allocate" arrowhead=open];')
    lines.append("}")

    render_dot("\n".join(lines), out)


def render_action_flow(model: Any, name: str, out: str | Path) -> None:
    """Render an action flow diagram for a named action def to SVG via PlantUML.

    WP-5 implements this using opensysml CLI + PlantUML.
    """
    raise NotImplementedError("render_action_flow: implement in WP-5")
