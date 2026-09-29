"""The real-fixture mutation-control test: change one real element, re-render,
diff. This is the exact check that caught SysMLD's silent staleness on the
original toy fixture (see check_sysmld_mutation.py); it runs here for every
tool that rendered a mutable view, not just the ones expected to pass."""
from scripts.diagram_study.harness import svgs_differ


def mutation_control_result(tool: str, baseline_svg: bytes, mutated_svg: bytes) -> dict:
    if not baseline_svg:
        raise ValueError(f"{tool}: baseline render is empty — cannot run a meaningful mutation-control comparison")
    changed = svgs_differ(baseline_svg, mutated_svg)
    return {
        "tool": tool,
        "baseline_rendered": True,
        "svg_changed": changed,
        "verdict": "reflects the mutation" if changed else "STALE: picture unchanged after a real model edit",
    }
