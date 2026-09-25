"""Environment setup: verify tool versions and provision OpenSysML binary."""

import hashlib
import subprocess
import sys
from pathlib import Path

_BINARY_DIR = Path(__file__).parent.parent.parent / ".opensysml"
_SUMS_FILE = Path(__file__).parent.parent.parent / "scripts" / "SHA256SUMS.txt"


def check_tool_versions() -> None:
    """Assert required CLI tools are present and print their versions."""
    tools = {
        "dot": ["-V"],
        "java": ["-version"],
    }
    missing = []
    for tool, args in tools.items():
        try:
            result = subprocess.run(
                [tool] + args, capture_output=True, text=True, timeout=10
            )
            version_line = (result.stdout or result.stderr).splitlines()[0]
            print(f"{tool}: {version_line}")
        except FileNotFoundError:
            missing.append(tool)
    if missing:
        raise RuntimeError(f"Missing required tools: {missing}")


def ensure_binary(version: str = "v0.9.0") -> None:
    """Download and verify the OpenSysML binary for the current platform."""
    import opensysml.binary  # type: ignore[import]

    opensysml.binary.ensure_binary(version=version)


def provision(version: str = "v0.9.0") -> None:
    """Run full pre-flight: check tool versions then ensure binary."""
    check_tool_versions()
    ensure_binary(version=version)
