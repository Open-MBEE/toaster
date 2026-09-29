"""Reusable render/run helpers for the Phase 0 real-fixture diagram study.
Generalizes the original study's run_study.py (run(), render()) from one
fixture to a (tool, view, element, model) table over real chapter models.
"""
import hashlib
import subprocess
import time
from pathlib import Path


def build_render_command(
    tool: str, view: str, element: str, model_path: Path, source_path: Path, tools: dict
) -> list[str]:
    if tool == "opensysml-puml":
        return [tools["opensysml"], str(model_path), "-render", f"#{view}:{element}",
                "-render-form", "plantuml", "-o", str(source_path)]
    if tool == "opensysml-dot":
        return [tools["opensysml"], str(model_path), "-render", f"#{view}:{element}",
                "-render-form", "dot", "-o", str(source_path)]
    if tool == "toolkit":
        return [tools["toolkit"], "viz", str(model_path), "--view", view,
                "--element", element, "-o", str(source_path)]
    if tool == "pilot":
        # args: library, model, element, view, dest-svg (see PilotRender.java)
        return [tools["java"], "-Djava.awt.headless=true", "-cp", tools["pilot_jar"],
                tools["pilot_render_class"], tools["pilot_library"], str(model_path),
                element, view, str(source_path)]
    raise ValueError(f"unknown tool: {tool!r}")


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def svgs_differ(before: bytes, after: bytes) -> bool:
    return before != after


def run_and_log(name: str, cmd: list[str], out_dir: Path, env: dict | None = None) -> subprocess.CompletedProcess:
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic()
    result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=120)
    elapsed = round(time.monotonic() - t0, 3)
    (out_dir / f"{name}.log").write_text(
        f"$ {' '.join(cmd)}\nexit_code={result.returncode} elapsed_seconds={elapsed}\n\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}\n"
    )
    return result
