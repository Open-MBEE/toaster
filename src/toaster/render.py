"""Diagram rendering helpers. WP-4 implements SysMLD exporter."""

import os
import re
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

    A `PartUsage` whose owner is a `RequirementDefinition`/`RequirementUsage`,
    or any other definition/usage kind that shares the same `subject`
    semantics -- `ConcernDefinition`/`ConcernUsage` (Concern specializes
    Requirement), `CaseDefinition`/`CaseUsage` and its own specializations
    `VerificationCaseDefinition`/`VerificationCaseUsage`,
    `UseCaseDefinition`/`UseCaseUsage`, `AnalysisCaseDefinition`/
    `AnalysisCaseUsage` -- is a declared `subject` (e.g. `requirement def
    TimelyToast { subject toaster : Toaster; ... }`, or equally `verification
    def TimelyToastTest { subject toaster : Toaster; ... }`), not real part
    composition. SysML v2 represents the subject binding as a `PartUsage`
    owned by the requirement/concern/case, but on every one of these kinds
    `subject` means the same thing: a reference/parameter binding, not
    ownership. Such a usage is skipped entirely (neither its composition edge
    nor its typing edge is drawn, and it does not appear in the diagram),
    since nothing else references it once the composition edge is gone.
    Every other owner kind (a real `PartDefinition` or `PartUsage`) is
    unaffected.

    This 12-member skip-set is not a claim that it is complete against the
    SysML v2 spec's full Requirement/Case family -- it is not (see below for
    confirmed gaps). What is confirmed: across this tutorial's own real
    fixtures (ch01 through ch10), every owner `@type` actually observed is
    one of `PartDefinition`, `PartUsage`, `Package`, `RequirementDefinition`,
    and `VerificationCaseDefinition` -- so only two of these 12 entries
    (`RequirementDefinition`, `VerificationCaseDefinition`) are subject-
    bearing owner kinds this tutorial's content currently exercises. The
    other 10 (`RequirementUsage`, the `Concern*`, `Case*`, `UseCase*`, and
    `AnalysisCase*` pairs) extend the skip-set to sibling kinds that share
    the same `subject` semantics by spec reasoning alone -- no real fixture
    in this tutorial exercises any of them today, so they are untested here,
    not confirmed unnecessary.

    Known, narrow limitation: only the direct subject-owned usage itself is
    skipped. A subject usage with its own further-nested parts (e.g.
    `requirement def R { subject t : T { part u : U; } }`) still leaks `u`
    as an orphan node, since nothing transitively owned by the subject usage
    is suppressed. No fixture in this tutorial exercises that case today, so
    it is recorded here rather than fixed.

    Separately, two more toolkit constructs carry their own `subject` and are
    confirmed NOT covered by `REQUIREMENT_OWNER_TYPES`: a `viewpoint def V {
    subject t : T; }` (a specialized requirement with its own `subject`)
    comes back from the toolkit as `@type` `ViewpointDefinition`/
    `ViewpointUsage`; a `satisfy requirement rq : R { subject t5 : T; }`
    relationship comes back as `@type` `SatisfyRequirementUsage`. Neither is
    in the skip-set, so each would still leak its subject as false
    composition. A third, related toolkit quirk: an `objective` nested inside
    a verification/analysis case def comes back as a plain `PartUsage` owned
    by the case (not a distinguishable requirement-family `@type` at all), so
    its own nested `subject` leaks too -- no type-list fix can catch that one,
    since nothing in the owner's `@type` distinguishes it from real
    composition. None of these three appear in any real fixture in this
    tutorial today, so -- per the same reasoning as the nested-subject-parts
    limitation above -- they are recorded here as a known gap, not fixed.
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
    # Built once per call (not per element): every model element keyed by its
    # own qualified name, so a PartUsage's `owner` string can be resolved to
    # the owning element's own `@type` -- model.query() is always callable on
    # `model` regardless of what `elements` was passed, since it queries the
    # model object fresh and does not depend on any prior scoping.
    by_qname = {}
    for e in model.query():
        od = e.as_dict()
        oqname = od.get("qualifiedName", od.get("@id", ""))
        by_qname[oqname] = od
    REQUIREMENT_OWNER_TYPES = {
        "RequirementDefinition",
        "RequirementUsage",
        "ConcernDefinition",
        "ConcernUsage",
        "CaseDefinition",
        "CaseUsage",
        "VerificationCaseDefinition",
        "VerificationCaseUsage",
        "UseCaseDefinition",
        "UseCaseUsage",
        "AnalysisCaseDefinition",
        "AnalysisCaseUsage",
    }

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
            owner_type = by_qname.get(owner, {}).get("@type", "")
            if owner_type in REQUIREMENT_OWNER_TYPES:
                continue
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

    If `fqn` names a usage (a part instance) rather than a definition, depth
    counts differently than the "1 = fqn's own direct owned parts" framing
    above: a usage's own qualified name never owns anything (only its type
    does, per containment_subgraph()'s semantics), so depth=1 from a usage
    root returns zero parts. This matches this function's behavior before
    `depth` existed (not a regression), and this tutorial's own call sites
    always root at a definition or assembly, never a bare usage.

    flows/allocs extraction below is unchanged by `depth` and stays
    model-wide (via model.to_api_json(), not scoped to the expanded parts
    set); its endpoint resolution and node-deduplication logic (see
    render_interconnection()'s `normalize()`) assumes the depth=1 case, where
    every part is a direct, unique owned child of `fqn`. At depth>1, a flow or
    allocation between two nested parts several levels deep can be drawn
    misleadingly (e.g. as a self-loop on their shared ancestor, since only the
    first path segment is resolved) or against a node that looks duplicated.
    Treat depth>1 diagrams' flows/allocs as exploratory until this is
    addressed; the `parts` list itself is not affected by this limitation.

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

    if depth is None or depth < 0:
        raise ValueError(f"depth must be an int >= 0, got {depth!r}")

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


def _apply_interconnection_layout_fixes(puml_text: str) -> str:
    """Presentation-only post-processing of sysml-toolkit's generated PlantUML source, applied
    before rendering: orientation and label wrapping only, never a change to which elements or
    edges appear (AGENTS.md: layout never carries engineering content).

    sysml-toolkit's own default PlantUML layout draws the connector between two ports as a
    straight diagonal line, which (confirmed by rendering and rasterizing the real Ch5 output)
    runs directly through the near box's own `<<part>>` stereotype and title text -- exactly
    the box label a reader needs to read. Inserting `skinparam linetype ortho` makes PlantUML
    route that connector in axis-aligned segments along box edges instead of a corner-cutting
    diagonal, which keeps it clear of both boxes' interiors.

    Separately, a port's own auto-generated label (e.g. `durationIn : ~DurationPort`) is wide
    enough, and close enough to the neighboring box, to overlap that box's own border in the
    unwrapped, single-line form (also confirmed by rendering the real output). Rewriting each
    port label's ` : ` to a line break (`durationIn` / `: ~DurationPort`, same text, same
    information) shrinks its rendered width enough to clear the border. Only `port "..."`
    declaration lines are rewritten -- a box's own title line (e.g. `"heating :
    HeatingSystem"`) is left on one line, since it already has the whole box's width to sit in
    and was never the defect being fixed.
    """
    if "\nskinparam linetype ortho" not in puml_text and "@startuml" in puml_text:
        puml_text = puml_text.replace("@startuml", "@startuml\nskinparam linetype ortho", 1)

    def _wrap_port_label(match: "re.Match[str]") -> str:
        return f'{match.group(1)}{match.group(2)}\\n: {match.group(3)}{match.group(4)}'

    return re.sub(
        r'(port\s+")([^"\n]*?) : ([^"\n]*?)(")',
        _wrap_port_label,
        puml_text,
    )


class ToolkitRenderError(Exception):
    """Raised when `render_toolkit_interconnection()` could not render: a given `binary`,
    `lib`, `plantuml_jar` or `java` path does not exist, or either subprocess (sysml-toolkit's
    `viz` CLI, or PlantUML) exited non-zero. Always names the offending path or command and
    includes the subprocess's own stderr, rather than letting a bare `FileNotFoundError` or a
    raw `subprocess.CalledProcessError` traceback surface to the caller."""


def render_toolkit_interconnection(
    src: str | Path,
    element: str,
    out: str | Path,
    *,
    lib: str | Path,
    binary: str | Path,
    plantuml_jar: str | Path,
    java: str | Path,
) -> None:
    """Render an interconnection view via sysml-toolkit's real `viz` CLI (not the in-house
    `render_interconnection()`), drawing real port names as their own boxes rather than
    folding port identity into a single edge label.

    Use this specifically when port identity itself is the chapter's own pedagogical point
    (e.g. a chapter introducing or exercising a conjugated port) -- the criterion stated in
    `.claude/skills/sysml-diagrams/SKILL.md`'s renderer-choice table and
    `.claude/skills/sysml-diagrams/references/recipes.md`'s interconnection recipe, confirmed
    on every real fixture tested (`decisions/diagram-study-real-fixtures.md`): sysml-toolkit
    draws port names like `durationIn`/`durationOut` as their own boxes inside the owning
    part, where the in-house `render_interconnection()` only draws one edge label
    (`durationInterface`) with no port identity at all. `render_interconnection()` stays the
    default everywhere else -- a chapter using interconnection only to show a connection or an
    allocation, where port identity is not itself the point, does not need this function's
    extra external-binary dependency.

    `src`: a SysML source file to load. `element`: the qualified name of the part whose
    interconnection view to draw (passed to `viz`'s own `--element`). `out`: the final SVG
    path.

    `lib`, `binary`, `plantuml_jar`, `java`: explicit paths to the sysml.library directory,
    the `sysmlv2` executable, the PlantUML jar, and a working `java` executable. All four are
    required keyword arguments -- none is ever resolved from an environment variable or
    searched on PATH (unlike `modelcheck.py`'s optional `lib`/`binary`, every path here must
    be passed explicitly). Each is checked, before either subprocess runs, against what this
    function actually needs it to be (`lib` a directory; `binary`/`java` an executable file;
    `plantuml_jar` a file) -- not merely `Path.exists()`, which an empty string or a directory
    passed as `binary` would still satisfy and then fail later as a raw `PermissionError` or
    `NotADirectoryError`. A path that fails its check raises `ToolkitRenderError` naming which
    argument and path, not a bare `FileNotFoundError` or another subprocess-level exception.

    Shells out to `sysmlv2 viz <src> --lib <lib> --view interconnection --element <element>
    -o <puml>`, applies presentation-only layout fixes to that generated PlantUML source (see
    `_apply_interconnection_layout_fixes()`), then to `java -Djava.awt.headless=true -jar
    <plantuml_jar> -tsvg <puml>`, which PlantUML writes next to `<puml>` as `<puml's
    stem>.svg`; that file is then moved to `out`. The intermediate `.puml` (post-layout-fix) is
    left on disk at `out` with its suffix replaced by `.puml` (not a randomized temp name) so a
    caller -- or a test checking for real port-name tokens, not just an exit code -- can read
    it after this function returns, matching `render_dot()`/`render_interconnection()`'s own
    "write real files, return None" style.
    """
    # Each path is checked against the real thing this function will actually try to do with
    # it (a directory to search, a file to hand to -jar, a file to execute), not just
    # Path.exists(): an empty string, a directory passed where a binary was expected, or a
    # non-executable file would otherwise pass an exists()-only check and then surface a raw
    # PermissionError or NotADirectoryError from the subprocess call below instead of this
    # function's own named ToolkitRenderError.
    for argname, path, check, what in (
        ("lib", lib, lambda p: p.is_dir(), "a directory"),
        ("binary", binary, lambda p: p.is_file() and os.access(p, os.X_OK), "an executable file"),
        ("plantuml_jar", plantuml_jar, lambda p: p.is_file(), "a file"),
        ("java", java, lambda p: p.is_file() and os.access(p, os.X_OK), "an executable file"),
    ):
        if not check(Path(path)):
            raise ToolkitRenderError(
                f"{argname}={path!r} is not {what} -- render_toolkit_interconnection() "
                f"requires each of lib/binary/plantuml_jar/java as an explicit, existing, "
                f"usable path; none is resolved from an environment variable or PATH"
            )

    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    puml_path = out_path.with_suffix(".puml")

    viz_command = [
        str(binary),
        "viz",
        str(src),
        "--lib",
        str(lib),
        "--view",
        "interconnection",
        "--element",
        element,
        "-o",
        str(puml_path),
    ]
    r = subprocess.run(viz_command, capture_output=True, text=True)
    if r.returncode != 0:
        raise ToolkitRenderError(
            f"`{' '.join(viz_command)}` exited {r.returncode}: "
            f"{r.stderr.strip() or '(no stderr)'}"
        )

    # Presentation-only layout fixes (orientation + label wrapping), applied to the generated
    # .puml before PlantUML renders it -- see _apply_interconnection_layout_fixes()'s own
    # docstring for why; never changes which elements or edges the file describes.
    puml_path.write_text(_apply_interconnection_layout_fixes(puml_path.read_text()))

    plantuml_svg_path = puml_path.with_suffix(".svg")
    plantuml_command = [
        str(java),
        "-Djava.awt.headless=true",
        "-jar",
        str(plantuml_jar),
        "-tsvg",
        str(puml_path),
    ]
    r = subprocess.run(plantuml_command, capture_output=True, text=True)
    if r.returncode != 0:
        raise ToolkitRenderError(
            f"`{' '.join(plantuml_command)}` exited {r.returncode}: "
            f"{r.stderr.strip() or '(no stderr)'}"
        )
    if not plantuml_svg_path.exists():
        raise ToolkitRenderError(
            f"`{' '.join(plantuml_command)}` exited 0 but did not produce the expected "
            f"SVG at {plantuml_svg_path}"
        )

    if plantuml_svg_path != out_path:
        plantuml_svg_path.replace(out_path)


def _render_opensysml_view(
    model: Any, name: str, out: str | Path, kind: str, *, binary: str | Path | None = None
) -> None:
    """Shared implementation for render_action_flow (kind="action") and
    render_state_flow (kind="state"): both use the identical OpenSysML CLI
    mechanism, differing only in the #kind: prefix.

    Serializes the ALREADY-LOADED model (model.to_sysml()) to a temp file and
    renders that, not the committed models/chXX-cumulative.sysml -- this
    renders exactly what the notebook's own model object represents, which
    may differ from disk in a notebook that applies an edit before rendering.
    """
    import subprocess
    import tempfile

    if binary is None:
        from toaster.bootstrap import ensure_cli_binary

        binary = ensure_cli_binary()
    binary = Path(binary)
    if not binary.exists():
        raise FileNotFoundError(f"sysml CLI binary not found at {binary}")

    out = Path(out)
    with tempfile.TemporaryDirectory() as tmp:
        src_path = Path(tmp) / "model.sysml"
        src_path.write_text(model.to_sysml().content)
        dot_path = Path(tmp) / "view.dot"
        subprocess.run(
            [str(binary), str(src_path), "-render", f"#{kind}:{name}",
             "-render-form", "dot", "-o", str(dot_path)],
            check=True, capture_output=True, text=True,
        )
        render_dot(dot_path, out)


def render_action_flow(
    model: Any, name: str, out: str | Path, *, binary: str | Path | None = None
) -> None:
    """Render an action-flow diagram for a named action def to SVG, via
    OpenSysML's own `-render #action:` CLI form (no in-house equivalent exists
    -- confirmed working on real content, decisions/diagram-study-real-fixtures.md).

    `binary=None` (default) provisions the CLI automatically via
    toaster.bootstrap.ensure_cli_binary(); pass an explicit path to pin a
    specific local build instead.
    """
    _render_opensysml_view(model, name, out, "action", binary=binary)


def render_state_flow(
    model: Any, name: str, out: str | Path, *, binary: str | Path | None = None
) -> None:
    """Render a state-transition diagram for a named state def to SVG, via
    OpenSysML's own `-render #state:` CLI form. Transition edges are labeled
    by their real trigger text (confirmed directly against Ch7's real Cycle
    state machine: `label="accept Start"`), so a renamed or mistyped trigger
    is visible in the figure, not just in printed diagnostics.

    `binary=None` (default) provisions the CLI automatically via
    toaster.bootstrap.ensure_cli_binary(); pass an explicit path to pin a
    specific local build instead.
    """
    _render_opensysml_view(model, name, out, "state", binary=binary)
