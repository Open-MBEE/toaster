"""Environment setup: verify tool versions and provision OpenSysML binary."""

import hashlib
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

_BINARY_DIR = Path(__file__).parent.parent.parent / ".opensysml"
_SUMS_FILE = Path(__file__).parent.parent.parent / "scripts" / "SHA256SUMS.txt"


def check_tool_versions() -> None:
    """Assert required CLI tools are present and print their versions."""
    tools = {
        "dot": ["-V"],
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


_CLI_SUMS = {
    ("darwin", "amd64"): "c4efdbcfd698ac9adb1ba64aca5adcd2d4caecf6299140da77eb9c2a8f1a4874",
    ("darwin", "arm64"): "0129f277bd10c73ca09c7ce643cf7ae9b6b496250925d1a640ef1e2930340efb",
    ("linux", "amd64"): "3e9a2070261cd08bd7363abf3a836c3adb5b92f488668548734bdce7b6bd8fa1",
    ("linux", "arm64"): "c74dbd818e1cf2aa082bf6f0c23759a661ed4af7b30e29959c2b8d9126162384",
    ("windows", "amd64"): "a95cc65062c7f7cd070d75c52adbba4763dfced950acc518e2b50aae0749a15b",
}


def _cli_cache_dir() -> Path:
    return Path.home() / ".opensysml" / "bin"


def ensure_cli_binary(version: str = "v0.9.0") -> Path:
    """Download, SHA256-verify, and cache OpenSysML's render-capable CLI binary.

    Distinct from opensysml.binary.ensure_binary(), which provisions the
    unrelated sysml-grpc SERVICE binary (no -render support at all, confirmed
    directly: `sysml-grpc -help` lists no -render flag). This provisions the
    separate `sysml-<os>-<arch>.tar.gz` asset the same v0.9.0 release also
    publishes, which does support -render (confirmed against the real pinned
    commit ee54ea03ea3ca8fb2c796ecda364adf748c40304).

    Cached at ~/.opensysml/bin/sysml, sibling to (but never overwriting)
    sysml-grpc's own cache in the same directory. A cache hit returns
    immediately with no network call.
    """
    import opensysml.binary as ob

    os_name, arch = ob.detect_platform()
    key = (os_name, arch)
    if key not in _CLI_SUMS:
        raise RuntimeError(
            f"No pinned sha256 for platform {os_name}-{arch}; "
            f"supported: {sorted(_CLI_SUMS)}"
        )

    cache_dir = _cli_cache_dir()
    target = cache_dir / ("sysml.exe" if os_name == "windows" else "sysml")
    if target.exists():
        return target

    cache_dir.mkdir(parents=True, exist_ok=True)
    asset_name = f"sysml-{os_name}-{arch}" + (".zip" if os_name == "windows" else ".tar.gz")
    url = (
        f"https://github.com/Open-MBEE/OpenSysML/releases/download/"
        f"{version}/{asset_name}"
    )
    archive_path = cache_dir / asset_name
    urllib.request.urlretrieve(url, archive_path)

    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    expected = _CLI_SUMS[key]
    if digest != expected:
        archive_path.unlink()
        raise RuntimeError(
            f"sha256 mismatch for {asset_name}: got {digest}, expected {expected} "
            f"-- refusing to install a binary that doesn't match the pinned release"
        )

    if os_name == "windows":
        import zipfile

        with zipfile.ZipFile(archive_path) as zf:
            zf.extractall(cache_dir)
        extracted = cache_dir / f"sysml-{os_name}-{arch}.exe"
    else:
        with tarfile.open(archive_path) as tf:
            tf.extractall(cache_dir)
        extracted = cache_dir / f"sysml-{os_name}-{arch}"

    extracted.rename(target)
    target.chmod(0o755)
    archive_path.unlink()
    return target


def provision(version: str = "v0.9.0") -> None:
    """Run full pre-flight: check tool versions then ensure binaries."""
    check_tool_versions()
    ensure_binary(version=version)
    ensure_cli_binary(version=version)
