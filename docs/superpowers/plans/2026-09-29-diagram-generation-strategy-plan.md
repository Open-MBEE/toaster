# Diagram Generation Strategy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

> **STATUS (2026-10-01, reconciliation pass): all 4 tasks DONE.** `containment_subgraph()`, `model_to_dot(elements=, layout=)`, and `build_interconnection_intent(depth=)` are all live in `src/toaster/render.py`; `decisions/diagram-tool-gaps.md` is seeded and has since grown past this plan's own Task 4 text (G-D001 is now marked RESOLVED there, not just documented). Every test this plan specifies exists and passes, plus extra hardening beyond what was planned (`tests/test_containment_subgraph.py` has 11 tests, not the 9 originally written here — two extra input-validation cases were added during implementation). The checkboxes below were never ticked when the work landed; this pass ticks them to match the actual, verified state (`uv run pytest tests/test_containment_subgraph.py tests/test_diagram_probe.py tests/test_interconnection.py -v`, all passing) rather than re-deriving or re-doing any of it.

**Goal:** Give `src/toaster/render.py` a query-driven content-selection layer (root + relationship kind + depth) that is separate from layout/presentation, so structure diagrams stop drawing every model element indiscriminately, and seed a dedicated register for rendering-tool gaps found along the way.

**Architecture:** One new function, `containment_subgraph()`, walks `model.query()`'s own `owner`/`type` fields from a root element by relationship kind, to a given depth, re-evaluated fresh against the live model every call. `model_to_dot()` gets an optional `elements` parameter (a pre-selected list, typically `containment_subgraph()`'s output) and a separate, optional `layout` parameter for presentation-only overrides. `build_interconnection_intent()` gets a `depth` parameter, implemented by reusing `containment_subgraph()` internally rather than duplicating traversal logic. A new file, `decisions/diagram-tool-gaps.md`, is seeded with the two rendering-tool gaps Phase 0 already found.

**Tech Stack:** Python (stdlib only for the new traversal logic), `opensysml` (already a dependency, used to load and query real fixture models in tests), Graphviz (already a dependency, unchanged).

**Spec:** [`docs/superpowers/specs/2026-09-29-diagram-generation-strategy-design.md`](../specs/2026-09-29-diagram-generation-strategy-design.md)

## Global Constraints

- No new dependency is added — pure Python plus what `render.py` already imports.
- `containment_subgraph()` only queries the model; it never mutates it and never writes a file.
- `model_to_dot(model, title)` called exactly as before (no `elements`, no `layout`) must produce byte-for-byte the same DOT source as before this plan — existing callers and `tests/test_diagram_probe.py` are not touched and must keep passing unmodified.
- `build_interconnection_intent(model, fqn)` called exactly as before (no `depth`) must behave exactly as before — all 9 existing tests in `tests/test_interconnection.py` must keep passing unmodified, and Ch5's shipped notebook (`chapters/ch05-architecture/03-interfaces.ipynb`), which calls it with no `depth` argument, is not touched by this plan.
- Presentation/layout parameters never carry engineering content (AGENTS.md's diagrams-as-scientific-plots principle) — a `layout` override changes only how the selected graph is drawn, never which elements or edges appear.
- No chapter notebook, no Phase 1 per-chapter survey work, and no upstream issue filing happens in this plan — all explicitly out of scope per the spec's Non-goals.

## Review Focus

- A `root` that doesn't exist in `model.query()` at all (a typo, or a qualified name from the wrong fixture) — `containment_subgraph()` must return an empty list cleanly, never raise `KeyError`. Task 1's tests cover this.
- `depth=0` — must mean "the root only, zero hops of traversal," not "unbounded" and not "empty." Task 1 defines and tests this explicitly, since the spec never pins the boundary value down.
- A containment cycle (implausible in a well-formed model, but the traversal must not hang the notebook it runs in if one exists) — Task 1's algorithm tracks visited elements by qualified name and must provably terminate; tested directly, not just assumed safe by construction.
- `model_to_dot(model, elements=[])` — an explicitly empty selection is a real, valid outcome ("nothing in scope"), distinct from `elements=None` ("everything in scope, the old default"). Task 2 tests both are handled and produce different output.
- `build_interconnection_intent(model, fqn, depth=2)` reaching into a sub-part's own nested composition — the real Ch5/Ch6/Ch8 fixtures don't have a part with its own nested `part` members deep enough to exercise this, so Task 3 uses a small synthetic fixture (matching the file's own existing convention of hand-written sources for exactly this kind of unit test) to prove multi-level recursion actually works, not just that it doesn't crash on fixtures that happen to be flat.

---

## Task 1: `containment_subgraph()` — query-driven element selection

**Files:**
- Modify: `src/toaster/render.py` (add the function after `model_to_dot`, before `render_dot`)
- Test: `tests/test_containment_subgraph.py` (new)

**Interfaces:**
- Produces: `containment_subgraph(model, root: str, *, relations: tuple[str, ...] = ("composition", "typing"), depth: int | None = None) -> list` — returns a list of the same `QueryElement` objects `model.query()` itself returns (each has `.as_dict()`, matching `model_to_dot()`'s and `build_interconnection_intent()`'s existing element-handling pattern), so it composes directly as input to Task 2's `model_to_dot(elements=...)` and Task 3's `build_interconnection_intent`.

**Semantics, pinned precisely (this is what the tests below check):** each traversal hop processes every element currently in the frontier and, for each one, follows both requested relation kinds — `"composition"`: find every `PartUsage` whose `owner` field equals the frontier element's own qualified name; `"typing"`: if the frontier element itself has a `type` field, follow it to that definition. Everything found is added to the result and becomes next hop's frontier; hop count then increments. `depth=None` runs until no new elements are found (the frontier goes empty). `depth=0` returns just `[root's own element]` with zero hops run. A root not present in `model.query()` returns `[]`.

- [x] **Step 1: Write the failing tests, grounded in the real Ch6 fixture**

```python
# tests/test_containment_subgraph.py
"""Tests for containment_subgraph() (diagram generation strategy, Task 1)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from toaster.render import containment_subgraph

REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="module")
def ch06_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch06-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok, f"Ch6 fixture failed to load: {model.diagnostics}"
    yield model
    conn.close()


def _qnames(elements):
    return {e.as_dict().get("qualifiedName", e.as_dict().get("@id", "")) for e in elements}


def test_unknown_root_returns_empty_list(ch06_model):
    result = containment_subgraph(ch06_model, "ToasterDemo::NoSuchElement")
    assert result == []


def test_depth_zero_returns_only_the_root(ch06_model):
    result = containment_subgraph(ch06_model, "ToasterDemo::Toaster", depth=0)
    assert _qnames(result) == {"ToasterDemo::Toaster"}


def test_toaster_reaches_direct_composition_and_typing_at_depth_two(ch06_model):
    # depth=1: Toaster's own composition children (heating, control).
    # depth=2: each child's typing target (HeatingSystem, ControlSystem) --
    # a node discovered via composition has its own typing edge explored on
    # the NEXT hop, per this function's pinned semantics.
    result = containment_subgraph(ch06_model, "ToasterDemo::Toaster", depth=2)
    names = _qnames(result)
    assert "ToasterDemo::Toaster" in names
    assert "ToasterDemo::Toaster::heating" in names
    assert "ToasterDemo::Toaster::control" in names
    assert "ToasterDemo::HeatingSystem" in names
    assert "ToasterDemo::ControlSystem" in names


def test_toaster_never_reaches_heatgen_at_any_depth(ch06_model):
    """The real finding from Phase 0's own review: Toaster::heating is typed
    by the abstract HeatingSystem, not the concrete HeatingAssembly that owns
    heatGen -- there is no composition or typing edge connecting them, so no
    depth value reaches heatGen from this root. This is the required
    negative-case test, not an optional one."""
    result = containment_subgraph(ch06_model, "ToasterDemo::Toaster", depth=None)
    names = _qnames(result)
    assert "ToasterDemo::HeatingAssembly::heatGen" not in names
    assert "ToasterDemo::HeatGenerator" not in names
    # Confirm the traversal actually terminated (returned, didn't hang) and
    # found the expected, smaller set -- not an accidentally-empty result.
    assert "ToasterDemo::Toaster" in names
    assert "ToasterDemo::HeatingSystem" in names


def test_heating_assembly_reaches_heatgen_at_depth_one(ch06_model):
    """The positive case: rooting directly at the definition that owns
    heatGen reaches it in exactly one composition hop."""
    result = containment_subgraph(ch06_model, "ToasterDemo::HeatingAssembly", depth=1)
    names = _qnames(result)
    assert "ToasterDemo::HeatingAssembly" in names
    assert "ToasterDemo::HeatingAssembly::heatGen" in names
    # HeatGenerator (heatGen's own type) is a second hop, not reached at depth=1.
    assert "ToasterDemo::HeatGenerator" not in names


def test_heating_assembly_reaches_heatgen_type_at_depth_two(ch06_model):
    result = containment_subgraph(ch06_model, "ToasterDemo::HeatingAssembly", depth=2)
    names = _qnames(result)
    assert "ToasterDemo::HeatGenerator" in names


def test_composition_only_excludes_typing_targets(ch06_model):
    result = containment_subgraph(
        ch06_model, "ToasterDemo::Toaster", relations=("composition",), depth=None
    )
    names = _qnames(result)
    assert "ToasterDemo::Toaster::heating" in names
    assert "ToasterDemo::HeatingSystem" not in names


def test_no_infinite_loop_on_a_flat_leaf_root(ch06_model):
    """A root with no composition children and no type field (a leaf) must
    terminate immediately, not hang."""
    result = containment_subgraph(ch06_model, "ToasterDemo::Bread", depth=None)
    assert _qnames(result) == {"ToasterDemo::Bread"}


CYCLE_SOURCE = """
package CycleTest {
    part def A { part b : B; }
    part def B { part a : A; }
}
"""


def test_no_infinite_loop_on_a_genuine_mutual_reference_cycle():
    """A (real, if unusual) mutual type reference -- A contains a part typed
    B, B contains a part typed back to A -- must not loop back to the root
    forever. This is the actual Review Focus case: a leaf root proves the
    stop condition fires when there's nothing left to find; this proves it
    fires when the SAME element would otherwise be rediscovered forever."""
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(CYCLE_SOURCE, strict=False)
    assert model.ok, f"Cycle model failed: {model.diagnostics}"
    result = containment_subgraph(model, "CycleTest::A", depth=None)
    conn.close()
    names = {e.as_dict().get("qualifiedName", e.as_dict().get("@id", "")) for e in result}
    assert names == {"CycleTest::A", "CycleTest::A::b", "CycleTest::B", "CycleTest::B::a"}
```

- [x] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_containment_subgraph.py -v`
Expected: FAIL with `ImportError: cannot import name 'containment_subgraph'`

- [x] **Step 3: Implement `containment_subgraph()` in `src/toaster/render.py`**, inserted immediately after `model_to_dot()`'s closing `return "\n".join(lines)` line and before `def render_dot`:

```python
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
```

- [x] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_containment_subgraph.py -v`
Expected: PASS (9 tests)

- [x] **Step 5: Run the full suite to confirm no regression**

Run: `uv run pytest -q`
Expected: all previously-passing tests still pass, plus the 8 new ones.

- [x] **Step 6: Commit**

```bash
git add src/toaster/render.py tests/test_containment_subgraph.py
git commit -m "Add containment_subgraph(): query-driven element selection by root, relation kind, and depth"
```

## Task 2: `model_to_dot()` — `elements` and `layout` parameters

**Files:**
- Modify: `src/toaster/render.py:8-48` (`model_to_dot`)
- Test: `tests/test_diagram_probe.py` (extend with new tests; existing 2 tests stay unmodified)

**Interfaces:**
- Consumes: `containment_subgraph()`'s return value (Task 1) as the typical `elements` argument.
- Produces: `model_to_dot(model, title="model", elements=None, layout=None) -> str` — the `elements`/`layout` signature every later chapter notebook that wants a scoped structure diagram will call.

- [x] **Step 1: Write the failing tests**

```python
# tests/test_diagram_probe.py -- ADD these to the existing file, do not remove
# the existing test_model_to_dot_structure / test_render_dot_produces_svg.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from toaster.render import containment_subgraph, model_to_dot

REPO_ROOT = Path(__file__).parent.parent


def test_model_to_dot_default_behavior_unchanged():
    """elements=None, layout=None must produce byte-for-byte the same output
    as before this plan -- the existing, unmodified test above already pins
    the shape of this output; this test pins that passing the new parameters'
    default values changes nothing."""
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_SRC, strict=False)
    assert model.ok
    without_new_params = model_to_dot(model, title="ToasterProbe")
    with_defaults_explicit = model_to_dot(
        model, title="ToasterProbe", elements=None, layout=None
    )
    assert without_new_params == with_defaults_explicit
    conn.close()


def test_model_to_dot_elements_scopes_the_output():
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_SRC, strict=False)
    assert model.ok
    scoped = containment_subgraph(model, "ToasterProbe::Toaster", depth=1)
    dot = model_to_dot(model, title="ToasterProbe", elements=scoped)
    assert "ToasterProbe::Toaster" in dot
    conn.close()


def test_model_to_dot_empty_elements_list_is_a_valid_empty_diagram():
    """elements=[] means 'nothing in scope' -- a real, different outcome from
    elements=None ('everything'), not an error and not silently the same
    as the default."""
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_SRC, strict=False)
    assert model.ok
    dot = model_to_dot(model, title="Empty", elements=[])
    assert "digraph" in dot
    assert "ToasterProbe::Toaster" not in dot
    conn.close()


def test_model_to_dot_excludes_unreachable_elements_on_real_ch08_fixture():
    """The real problem this plan exists to fix: on Ch8's real, larger model,
    scoping to Toaster's own containment excludes the unrelated test-fixture
    islands (nominal, slow, rated, weak, heatGenCheck, TimelyToast) that made
    the unscoped diagram unreadably wide."""
    conn = opensysml.connect(version="v0.9.0")
    src = (REPO_ROOT / "models" / "ch08-cumulative.sysml").read_text()
    model = conn.load_from_content(src, strict=False)
    assert model.ok
    scoped = containment_subgraph(model, "ToasterDemo::Toaster", depth=2)
    dot = model_to_dot(model, title="Ch8 scoped", elements=scoped)
    assert "ToasterDemo::Toaster::heating" in dot
    for excluded in ("ToasterDemo::nominal", "ToasterDemo::slow", "ToasterDemo::rated",
                     "ToasterDemo::weak", "ToasterDemo::heatGenCheck"):
        assert excluded not in dot
    conn.close()


def test_model_to_dot_layout_rankdir_override():
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_SRC, strict=False)
    assert model.ok
    default_dot = model_to_dot(model, title="ToasterProbe")
    lr_dot = model_to_dot(model, title="ToasterProbe", layout={"rankdir": "LR"})
    assert "rankdir=TB" in default_dot
    assert "rankdir=LR" in lr_dot
    assert "rankdir=TB" not in lr_dot
    conn.close()
```

- [x] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_diagram_probe.py -v`
Expected: the 5 new tests FAIL (`TypeError: model_to_dot() got an unexpected keyword argument 'elements'`); the 2 existing tests still PASS.

- [x] **Step 3: Modify `model_to_dot()` in `src/toaster/render.py:8-48`**

Replace the full function with:

```python
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
```

Note this keeps the composition/typing edge lines exactly as before; the only behavioral change is which elements `source` iterates over and the `rankdir` line, both no-ops at their default values.

- [x] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_diagram_probe.py -v`
Expected: PASS (7 tests: the original 2 plus the 5 new ones)

- [x] **Step 5: Run the full suite**

Run: `uv run pytest -q`
Expected: no regressions.

- [x] **Step 6: Commit**

```bash
git add src/toaster/render.py tests/test_diagram_probe.py
git commit -m "model_to_dot(): add elements and layout parameters, default behavior unchanged"
```

## Task 3: `build_interconnection_intent()` — `depth` parameter

**A real bug caught by testing against actual execution, not just design:** the obvious first attempt — call `containment_subgraph(..., relations=("composition",))` — never reaches a second level of nesting at all, at any depth value. Verified directly: a usage's own qualified name never "owns" anything; only its *type* does, so reaching a usage's nested sub-parts requires a `typing` hop (usage → its type definition) before the next `composition` hop (that definition → its own owned usages) can find anything. This is the exact same "wrong root chosen" shape Phase 0 already found between `Toaster::heating` and `heatGen`, one level removed. Verified empirically (see the plan's own derivation): with both relations active, reaching part-nesting level `N` costs `2N - 1` raw traversal hops (level 1 = 1 hop; level 2 = 3 hops; level 3 = 5 hops), because each additional nesting level costs one `typing` hop plus one `composition` hop, except the first level, which only needs the initial `composition` hop from the root itself. `depth` below is "levels of part nesting" (the intuitive unit a notebook author reasons about), translated internally to raw hops — never raw hops directly.

**Files:**
- Modify: `src/toaster/render.py:75-123` (`build_interconnection_intent`)
- Test: `tests/test_interconnection.py` (extend; existing 9 tests stay unmodified)

**Interfaces:**
- Consumes: `containment_subgraph()` (Task 1), called internally with `relations=("composition", "typing")` (both — composition alone cannot reach a second nesting level, see above) and `depth=2*depth-1` (the raw-hop translation derived above).
- Produces: `build_interconnection_intent(model, fqn, depth=1)` — `depth=1` (the default) is exactly today's behavior (direct owned parts only, confirmed: `2*1-1 == 1` raw hop, the same single composition hop the current code already does); `depth=2` reaches one further level of nested sub-parts (their own composition children); `depth=3` one further level again.

- [x] **Step 1: Write the failing test, using a small synthetic 3-level fixture**

The real Ch5/Ch6/Ch8 fixtures don't have a part with its own nested `part` members deep enough to exercise `depth=2` meaningfully (per this plan's Review Focus) — add a synthetic source alongside the file's existing ones (`FLOW_SOURCE`, `ALLOC_SOURCE`), matching that established convention:

```python
# tests/test_interconnection.py -- ADD alongside the existing module-level sources

NESTED_SOURCE = """
package ToasterDemo {
    private import ScalarValues::*;
    item def Signal;
    part def Inner {
        part sensor : Signal;
    }
    part def Outer {
        part inner : Inner;
    }
    part def Top {
        part outer : Outer;
    }
}
"""


@pytest.fixture(scope="module")
def nested_model():
    import opensysml

    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(NESTED_SOURCE, strict=False)
    assert model.ok, f"Nested model failed: {model.diagnostics}"
    yield model
    conn.close()


def test_default_depth_is_unchanged_direct_parts_only(nested_model):
    intent = build_interconnection_intent(nested_model, "ToasterDemo::Top")
    names = {p["name"] for p in intent["parts"]}
    assert names == {"outer"}


def test_depth_two_reaches_nested_composition(nested_model):
    intent = build_interconnection_intent(nested_model, "ToasterDemo::Top", depth=2)
    names = {p["name"] for p in intent["parts"]}
    assert "outer" in names
    assert "inner" in names


def test_depth_three_reaches_the_full_chain(nested_model):
    intent = build_interconnection_intent(nested_model, "ToasterDemo::Top", depth=3)
    names = {p["name"] for p in intent["parts"]}
    assert names == {"outer", "inner", "sensor"}
```

- [x] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_interconnection.py -v -k "depth"`
Expected: `test_default_depth_is_unchanged_direct_parts_only` passes already (current behavior matches `depth=1`'s intended meaning); `test_depth_two_reaches_nested_composition` and `test_depth_three_reaches_the_full_chain` FAIL (`TypeError: build_interconnection_intent() got an unexpected keyword argument 'depth'`).

- [x] **Step 3: Modify `build_interconnection_intent()` in `src/toaster/render.py:75-123`**

Replace the parts-extraction block (lines 89-97 of the current file) with a depth-aware version, and add the `depth` parameter to the signature:

```python
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
```

- [x] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_interconnection.py -v`
Expected: PASS (12 tests: the original 9 plus the 3 new ones)

- [x] **Step 5: Run the full suite**

Run: `uv run pytest -q`
Expected: no regressions.

- [x] **Step 6: Commit**

```bash
git add src/toaster/render.py tests/test_interconnection.py
git commit -m "build_interconnection_intent(): add depth parameter, reusing containment_subgraph(), default behavior unchanged"
```

## Task 4: `decisions/diagram-tool-gaps.md` — seed the gap-tracking register

**Files:**
- Create: `decisions/diagram-tool-gaps.md`

**Interfaces:**
- Produces: the register file itself, the format later entries (from Phase 1's survey or future probes) will follow.

- [x] **Step 1: Write `decisions/diagram-tool-gaps.md`**

```markdown
# Diagram tool gaps

A living register of confirmed capability gaps and bugs in rendering tools
considered for this tutorial's diagrams, distinct from `DEFERRED.md` (which
stays scoped, per `decisions/log.md` `DL-055`, to gaps in constructs or
dependencies this tutorial actually adopts). Both entries below are about
tools this tutorial does **not** adopt -- see `decisions/diagram-study-real-fixtures.md`
and `docs/superpowers/specs/2026-09-29-diagram-generation-strategy-design.md`
for why. They're recorded here so the findings aren't lost, and so a drafted
upstream issue (`decisions/gap-issue-drafts.md`'s existing discipline: draft,
hold for Z's review, file only on instruction) has a durable source to draw
from once a gap's picture is complete enough to be worth filing.

## G-D001: OMG pilot rejects qualified-name `allocate` targets

- **Tool / version:** OMG SysML v2 Pilot Implementation, release `2026-08`, `jupyter-sysml-kernel-0.62.0`.
- **Symptom:** every real-fixture render attempt (all 4 fixtures, all view types tried) fails with `ERROR:Must be an accessible feature (use dot notation for nesting)`, pointing at an `allocation ... allocate X::y to Z::w;` statement -- e.g. `models/ch05-cumulative.sysml:111`, `allocation heatAllocation allocate ToastBread::applyHeat to Toaster::heating;`.
- **Root cause:** the pilot's name-resolution check rejects a qualified-name (`::`-separated) reference on either side of an `allocate` statement; not established whether this is a pilot limitation or a real question about the tutorial's own `allocate` syntax against the spec (open, not resolved here).
- **Evidence:** `decisions/diagram-study-real-fixtures/evidence/ch05-tree-pilot-emit.log` and the equivalent log for every other fixture/view combination (all show the identical error).
- **Adoption-blocking?** Moot -- the pilot is not adopted for this tutorial (see the tool-selection table in `docs/superpowers/specs/2026-09-29-diagram-generation-strategy-design.md`); this entry exists to inform the pilot's own developers, not to justify a workaround for use here.
- **Status:** documented, not drafted. No issue drafted yet.

## G-D002: SysMLD/sysml2d indexer mis-tracks brace scope on ordinary real syntax

- **Tool / version:** `sysml2d` (SysMLD), pinned commit `1af88250d355f4e218f6653ef934e93ac8319cd6`.
- **Symptom:** `sysmld.model_index.build_model_index()` cannot resolve any correctly-qualified real element name from either of Ch5's or Ch7's real fixture models -- only a truncated, package-prefix-dropped form resolves (e.g. `Toaster` resolves, `ToasterDemo::Toaster` does not).
- **Root cause:** the indexer pops a scope frame (`package_stack`/`def_stack`) on any source line starting with `}`, regardless of whether a tracked keyword (`package`, `part def`, `state def`, and a few behavior kinds) opened that specific brace. Both real fixtures contain an untracked brace pair inside `action def ApplyHeat` (a multi-line `doc` annotation, and an `assert constraint balance { ... }` body) whose closing braces pop frames early, eventually popping the outer `package ToasterDemo { ... }` frame itself before later elements are indexed.
- **Evidence:** `decisions/diagram-study-real-fixtures/evidence/sysmld-indexer-probe.json` (the `idx.has(...)` checks, both a true positive on the truncated form and a false negative on the correct form); `decisions/log.md` `DL-055` and its addendum (the full ACE ruling and independent review that confirmed this root cause against the pinned source directly).
- **Adoption-blocking?** Moot -- SysMLD is not adopted for this tutorial and was already only "not adopted" per the original toy-fixture study, kept in Phase 0's rerun for comparison completeness only. This entry exists to inform sysml2d's own developers.
- **Status:** documented, not drafted. No issue drafted yet.
```

- [x] **Step 2: Confirm the file exists and both entries are present**

Run: `test -f decisions/diagram-tool-gaps.md && grep -c "^## G-D" decisions/diagram-tool-gaps.md`
Expected: file exists; count is `2`.

- [x] **Step 3: Commit**

```bash
git add decisions/diagram-tool-gaps.md
git commit -m "Seed decisions/diagram-tool-gaps.md with Phase 0's two rendering-tool findings (pilot allocate-target rejection, SysMLD indexer bug)"
```

---

## Self-Review Notes

**Spec coverage:** every numbered item in the spec's "Decisions already made" that requires new code (2, 3, part of 4) maps to Task 1-3; the gap register (decision 4) maps to Task 4; decision 1 (tool-selection table) and decision 5 (Phase 1 implication) require no code and are not re-implemented here, matching the spec's own Non-goals ("Phase 1's actual per-chapter survey is not run by this spec"). Decision 6 (the rename/skill-doc correction) was already applied before this spec was written (`DL-057`, commit `6ed75bf`) and is not repeated here.

**Type/interface consistency:** `containment_subgraph()`'s return type (a list of the same element objects `model.query()` returns) is used identically by `model_to_dot(elements=...)` (Task 2) and internally by `build_interconnection_intent(depth=...)` (Task 3) — both call `.as_dict()` on each element the same way `containment_subgraph()`'s own implementation does.

**Known, explicit non-goal carried from the spec, not re-litigated here:** the `sysml-toolkit`-vs-`render_interconnection()` per-chapter choice, any chapter notebook content, Phase 1's survey, and upstream issue filing are all out of scope, matching the spec's own Non-goals section exactly.
