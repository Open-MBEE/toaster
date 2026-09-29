"""Diagram rendering helpers. WP-4 implements SysMLD exporter."""

import subprocess
from pathlib import Path
from typing import Any


def model_to_dot(
    model: Any,
    title: str = "model",
    elements: list | None = None,
    layout: dict | None = None,
) -> str:
    """Generate DOT source for the part hierarchy from model.query() elements,
    or from a pre-selected `elements` list (typically containment_subgraph()'s
    output) when the full, unscoped model is too large to be a legible
    structure diagram.

    `elements=None` (the default) draws every model.query() element, exactly
    as before this parameter existed -- still the right choice for a small
    model where "everything" is itself a legible view. `elements=[]` is a
    real, different, valid outcome (nothing in scope), not an error.

    `layout` carries presentation-only overrides that never change which
    elements or edges appear, only how they're drawn -- currently supports
    `{"rankdir": "TB"|"LR"|"BT"|"RL"}`; defaults to "TB" (unchanged).

    Nodes: PartDefinition (dashed border if abstract).
    Edges: composition (diamond arrowhead from owner to usage),
           typing (dashed open arrow from usage to its PartDefinition type).
    """
    layout = layout or {}
    rankdir = layout.get("rankdir", "TB")
    lines = [
        f'digraph "{title}" {{',
        f"  rankdir={rankdir};",
        '  graph [fontname="Helvetica"];',
        '  node [shape=box fontname="Helvetica"];',
        '  edge [fontname="Helvetica"];',
    ]
    source = model.query() if elements is None else elements
    for e in source:
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


def containment_subgraph(
    model: Any,
    root: str,
    *,
    relations: tuple[str, ...] = ("composition", "typing"),
    depth: int | None = None,
) -> list:
    """Elements reachable from `root` by the given relationship kinds, to
    `depth` hops (None = unbounded, 0 = the root only).

    "composition" follows owner->usage edges: the same ones model_to_dot()
    draws as diamond arrows (a PartUsage whose `owner` field is the current
    frontier element's own qualified name). "typing" follows a usage's own
    `type` field to its definition: the same ones model_to_dot() draws as
    dashed arrows. Each hop explores both requested relations for every
    element in the current frontier before advancing; an element discovered
    via composition on one hop has its own typing edge (if any) explored on
    the NEXT hop, not the same one.

    This queries model.query() fresh every call. It never reads or maintains
    a list of element names -- the selection is only ever as current as the
    model itself, so it cannot silently drift the way a hand-authored
    diagram-intent file can (see decisions/log.md DL-055).
    """
    valid_relations = {"composition", "typing"}
    for r in relations:
        if r not in valid_relations:
            raise ValueError(f"unknown relation kind: {r!r}")
    if depth is not None and depth < 0:
        raise ValueError(f"depth must be >= 0 or None, got {depth}")

    by_qname = {}
    for e in model.query():
        d = e.as_dict()
        qname = d.get("qualifiedName", d.get("@id", ""))
        by_qname[qname] = e

    if root not in by_qname:
        return []

    result = {root: by_qname[root]}
    frontier = {root}
    hops = 0
    while frontier and (depth is None or hops < depth):
        next_frontier = set()
        for qname in frontier:
            d = by_qname[qname].as_dict()
            if "composition" in relations:
                for other_qname, other_elem in by_qname.items():
                    if other_qname in result:
                        continue
                    other_d = other_elem.as_dict()
                    if (
                        other_d.get("@type") == "PartUsage"
                        and other_d.get("owner") == qname
                    ):
                        result[other_qname] = other_elem
                        next_frontier.add(other_qname)
            if "typing" in relations:
                part_type = d.get("type")
                if part_type and part_type in by_qname and part_type not in result:
                    result[part_type] = by_qname[part_type]
                    next_frontier.add(part_type)
        frontier = next_frontier
        hops += 1

    return list(result.values())


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


def build_interconnection_intent(model: Any, fqn: str, depth: int = 1) -> dict:
    """Extract interconnection data from model for a composite part or assembly.

    `depth` counts levels of part nesting (1 = fqn's own direct owned parts,
    the default and unchanged from before this parameter existed; 2 = those
    parts' own owned parts too; and so on) -- not raw traversal hops. Reaching
    one further nesting level costs a `typing` hop (a usage to its own type
    definition) plus a `composition` hop (that definition to its own owned
    usages): a usage's qualified name never itself owns anything, only its
    type does. So level N costs `2*N - 1` raw hops through
    containment_subgraph(relations=("composition", "typing")), except level 1,
    which is the root's own single composition hop. fqn itself is included in
    the traversal (containment_subgraph() always includes its root) but
    excluded from the returned parts list below, since fqn is the diagram's
    subject, not one of its own parts.

    Returns a dict with:
      title    — the qualified name
      parts    — list of {name, type} for owned PartUsage elements, to `depth`
                 levels of nesting
      flows    — list of {source, target} using sysx:sourceText from FlowUsage,
                 InterfaceUsage or ConnectionUsage ends (a connection whose ends
                 are ports is an interface, SysML v2 formal/2026-03-02 §7.14.1)
      allocs   — list of {source, target} using sysx:sourceText from AllocationUsage ends
    """
    import json as _json
    import warnings

    raw_depth = 2 * depth - 1 if depth >= 1 else 0
    expanded = containment_subgraph(
        model, fqn, relations=("composition", "typing"), depth=raw_depth
    )
    parts = []
    for e in expanded:
        d = e.as_dict()
        if d.get("@type") == "PartUsage" and d.get("qualifiedName", d.get("@id", "")) != fqn:
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
        if etype in ("FlowUsage", "InterfaceUsage", "ConnectionUsage"):
            flows.append({"source": src_text, "target": tgt_text})
        elif etype == "AllocationUsage":
            allocs.append({"source": src_text, "target": tgt_text})

    return {"title": fqn, "parts": parts, "flows": flows, "allocs": allocs}


def render_interconnection(intent: dict | str | Path, out: str | Path) -> None:
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

    def normalize(ref: str) -> str:
        """Collapse a qualified reference's leading segment to a known part's
        short name (e.g. 'Toaster::heating' -> 'heating') so an edge whose
        endpoint was written fully qualified reuses the same node the parts
        list already created, instead of drawing a duplicate box for the
        same model element."""
        segment = ref.split(".")[0]
        short = segment.rsplit("::", 1)[-1]
        return ref.replace(segment, short, 1) if short in part_names else ref

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
        src = normalize(str(flow.get("source", "")))
        tgt = normalize(str(flow.get("target", "")))
        src_part = src.split(".")[0]
        tgt_part = tgt.split(".")[0]
        if src_part in part_names and tgt_part in part_names:
            src_port = src.split(".")[1] if "." in src else ""
            tgt_port = tgt.split(".")[1] if "." in tgt else ""
            lbl = f"{src_port}→{tgt_port}" if src_port else ""
            lines.append(f'  "{src_part}" -> "{tgt_part}" [label="{lbl}" arrowhead=open];')
    for alloc in allocs:
        src = normalize(str(alloc.get("source", "")))
        tgt = normalize(str(alloc.get("target", "")))
        if src and tgt:
            lines.append(f'  "{src}" -> "{tgt}" [style=dashed label="allocate" arrowhead=open];')
    lines.append("}")

    render_dot("\n".join(lines), out)


def render_action_flow(model: Any, name: str, out: str | Path) -> None:
    """Render an action flow diagram for a named action def to SVG via PlantUML.

    WP-5 implements this using opensysml CLI + PlantUML.
    """
    raise NotImplementedError("render_action_flow: implement in WP-5")
