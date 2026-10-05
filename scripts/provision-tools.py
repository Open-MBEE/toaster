#!/usr/bin/env python3
"""Provision the pinned external tools into `.tools/` (or `--dest DIR`).

Downloads, for the current platform, the tools the tutorial shells out to, using the layout that
`toaster.tools` resolves:

    DIR/bin/sysmlv2        sysml-toolkit CLI
    DIR/bin/z3             Z3 solver (used by `sysmlv2 verify --solve`)
    DIR/plantuml.jar       PlantUML
    DIR/sysml.library/     SysML v2 standard library (sparse clone of SysML-v2-Release at a pinned commit)
    DIR/provisioned.json   what was installed from which pin, and the hashes of the installed files

Every download is checked against the sha256 in `scripts/tool-pins.json` before anything is installed:
all downloads are staged in a temporary directory outside DIR, so a mismatch leaves DIR untouched.
Re-running is idempotent: an item whose installed file still matches its pin is kept and not downloaded.

    uv run python scripts/provision-tools.py            # provision into <repo>/.tools
    uv run python scripts/provision-tools.py --check    # verify what is installed; exit 1 on any problem

Java is not provisioned (install a JRE; `scripts/check-tools.py` reports it).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PINS = Path(__file__).resolve().parent / "tool-pins.json"
MANIFEST_NAME = "provisioned.json"
ENV_VARS = ("SYSMLV2_BINARY", "SYSMLV2_LIB_DIR", "PLANTUML_JAR", "JAVA", "Z3")
_Z3_HINT = "install z3 via your package manager (brew install z3) and set Z3"
_SUPPORTED_OS = ("linux", "darwin")
_ARCH_NAMES = {"x86_64": "x86_64", "amd64": "x86_64", "arm64": "arm64", "aarch64": "arm64"}

Downloader = Callable[[str, Path], None]
LibraryFetcher = Callable[[str, str, Path], None]


# --- hashing, platform, pins -------------------------------------------------------------------


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sha256(path: Path, expected: str) -> None:
    """Raise `ValueError` unless the sha256 of `path` equals `expected` (case-insensitive)."""
    actual = sha256_of(path)
    if actual != expected.strip().lower():
        raise ValueError(f"sha256 mismatch for {path.name}: got {actual}, expected {expected}")


def tree_sha256(root: Path) -> str:
    """A digest of a directory: relative paths and file contents, in sorted order."""
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0")
        digest.update(sha256_of(path).encode() + b"\0")
    return digest.hexdigest()


def current_platform() -> tuple[str, str]:
    """`("linux"|"darwin", "x86_64"|"arm64")` for this machine; `ValueError` for anything else."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system not in _SUPPORTED_OS or machine not in _ARCH_NAMES:
        raise ValueError(f"unrecognised platform {system}-{machine}")
    return system, _ARCH_NAMES[machine]


def load_pins(path: Path) -> dict:
    """Read and structurally validate a pins file; `ValueError` names what is wrong."""
    pins = json.loads(Path(path).read_text())

    def need(cond: bool, what: str) -> None:
        if not cond:
            raise ValueError(f"{path}: {what}")

    def is_sha(value: Any) -> bool:
        return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)

    need(isinstance(pins, dict), "top level must be an object")
    for tool in ("sysmlv2", "z3"):
        entry = pins.get(tool)
        need(isinstance(entry, dict) and isinstance(entry.get("assets"), dict), f"{tool}.assets missing")
        for key, asset in entry["assets"].items():
            need(
                isinstance(asset, dict) and all(isinstance(asset.get(f), str) for f in ("url", "sha256", "member")),
                f"{tool}.assets.{key} needs url, sha256 and member",
            )
            need(is_sha(asset["sha256"]), f"{tool}.assets.{key}.sha256 must be 64 lowercase hex digits")
    plantuml = pins.get("plantuml")
    need(isinstance(plantuml, dict) and isinstance(plantuml.get("url"), str), "plantuml.url missing")
    need(is_sha(plantuml.get("sha256")), "plantuml.sha256 must be 64 lowercase hex digits")
    library = pins.get("library")
    need(
        isinstance(library, dict) and all(isinstance(library.get(f), str) for f in ("repo", "commit")),
        "library needs repo and commit",
    )
    return pins


# --- archives and downloads --------------------------------------------------------------------


def extract_member(archive: Path, member_suffix: str, dest: Path) -> Path:
    """Extract the single file in `archive` (.tar.gz/.tgz/.tar or .zip) whose path ends with `member_suffix`.

    `dest` is a directory (created if needed); the member is written to `dest / <its basename>`, keeping
    the permission bits recorded in the archive, and that path is returned. The match is on whole path
    components (`bin/z3` matches `z3-5.1.0-x64/bin/z3`, not `xbin/z3`). Nothing else in the archive is
    touched, and member names never choose where the file lands. `FileNotFoundError` if no file matches;
    `ValueError` if several do.
    """
    archive = Path(archive)
    suffix = member_suffix.lstrip("/")

    def matches(name: str) -> bool:
        return name == suffix or name.endswith("/" + suffix)

    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as zf:
            found = [i for i in zf.infolist() if not i.is_dir() and matches(i.filename)]
            _single(found, suffix, archive, lambda i: i.filename)
            info = found[0]
            mode = (info.external_attr >> 16) & 0o777
            return _write_member(zf.open(info), mode, dest, Path(info.filename).name)
    with tarfile.open(archive) as tf:
        found = [m for m in tf.getmembers() if m.isfile() and matches(m.name)]
        _single(found, suffix, archive, lambda m: m.name)
        member = found[0]
        stream = tf.extractfile(member)
        assert stream is not None
        return _write_member(stream, member.mode & 0o777, dest, Path(member.name).name)


def _single(found: list, suffix: str, archive: Path, name_of: Callable[[Any], str]) -> None:
    if not found:
        raise FileNotFoundError(f"no file ending with {suffix!r} in {archive.name}")
    if len(found) > 1:
        names = ", ".join(name_of(f) for f in found)
        raise ValueError(f"{suffix!r} is ambiguous in {archive.name}: {names}")


def _write_member(stream: Any, mode: int, dest: Path, name: str) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / name
    part = dest / (name + ".part")
    with stream, part.open("wb") as out:
        shutil.copyfileobj(stream, out)
    part.chmod(mode or 0o644)
    os.replace(part, target)
    return target


def download(url: str, dest: Path) -> None:
    """Stream `url` to `dest` (public https GET, no credentials)."""
    request = urllib.request.Request(url, headers={"User-Agent": "toaster-provision-tools"})
    with urllib.request.urlopen(request, timeout=120) as response, dest.open("wb") as out:
        shutil.copyfileobj(response, out)


def fetch_library(repo: str, commit: str, dest: Path) -> None:
    """Sparse-clone `repo` at `commit` and copy its `sysml.library` directory to `dest`."""
    with tempfile.TemporaryDirectory(prefix="sysml-library-") as tmp:
        clone = Path(tmp) / "clone"

        def git(*args: str, cwd: Path | None = None) -> str:
            done = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)
            return done.stdout.strip()

        git("clone", "--filter=blob:none", "--no-checkout", "--sparse", repo, str(clone))
        git("sparse-checkout", "set", "sysml.library", cwd=clone)
        git("checkout", commit, cwd=clone)
        head = git("rev-parse", "HEAD", cwd=clone)
        if head != commit:
            raise ValueError(f"library checkout is {head}, expected pinned commit {commit}")
        shutil.copytree(clone / "sysml.library", dest)


# --- plan: what to install for this platform ---------------------------------------------------


@dataclass(frozen=True)
class Item:
    name: str  # key in the manifest and in messages
    kind: str  # "archive" (extract one member), "file" (installed as downloaded), "git" (library)
    rel: str  # installed path relative to dest
    source: str  # pinned sha256 (archive, file) or commit (git)
    url: str = ""  # download URL, or repo URL for git
    member: str = ""  # archive member suffix
    executable: bool = False


def plan(pins: dict, platform_key: str) -> tuple[list[Item], list[str]]:
    """The items to provision for `platform_key`, and the problems that prevent that (empty if none)."""
    items: list[Item] = []
    problems: list[str] = []
    for tool, rel in (("sysmlv2", "bin/sysmlv2"), ("z3", "bin/z3")):
        assets = pins[tool]["assets"]
        asset = assets.get(platform_key)
        if asset is None:
            msg = f"{tool}: no pinned asset for {platform_key} (supported: {', '.join(sorted(assets))})"
            if tool == "z3":
                msg += f"; {_Z3_HINT}"
            problems.append(msg)
            continue
        items.append(Item(tool, "archive", rel, asset["sha256"], asset["url"], asset["member"], True))
    plantuml = pins["plantuml"]
    items.append(Item("plantuml", "file", "plantuml.jar", plantuml["sha256"], plantuml["url"]))
    library = pins["library"]
    items.append(Item("library", "git", "sysml.library", library["commit"], library["repo"]))
    if problems:
        keys = sorted({k for t in ("sysmlv2", "z3") for k in pins[t]["assets"]})
        problems.append(
            f"unsupported platform {platform_key}: supported keys are {', '.join(keys)}; "
            f"otherwise point to your own tools with the environment variables {', '.join(ENV_VARS)}"
        )
    return items, problems


# --- installed state ---------------------------------------------------------------------------


def load_manifest(dest: Path) -> dict:
    try:
        data = json.loads((dest / MANIFEST_NAME).read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def problem_with(dest: Path, manifest: dict, item: Item) -> str | None:
    """Why `item` is not correctly installed under `dest`, or None if it is."""
    path = dest / item.rel
    if not (path.exists() or path.is_symlink()):
        return f"missing: {path}"
    if item.kind == "file":
        if not path.is_file():
            return f"not a file: {path}"
        try:
            verify_sha256(path, item.source)
        except ValueError as exc:
            return str(exc)
        return None
    entry = manifest.get(item.name)
    if not isinstance(entry, dict):
        return f"{item.rel} is not recorded in {MANIFEST_NAME} (not provisioned by this script)"
    if entry.get("source") != item.source:
        return f"installed from {entry.get('source')}, pinned {item.source}"
    if item.kind == "git":
        if not (path / "Systems Library").is_dir():
            return f"{path} has no 'Systems Library' directory"
        if tree_sha256(path) != entry.get("installed_sha256"):
            return f"{path} differs from what was installed"
        return None
    if not path.is_file():
        return f"not a file: {path}"
    if sha256_of(path) != entry.get("installed_sha256"):
        return f"sha256 of {path} differs from what was installed"
    if item.executable and not os.access(path, os.X_OK):
        return f"{path} is not executable"
    return None


# --- commands ----------------------------------------------------------------------------------


def _say(out: TextIO, text: str = "") -> None:
    print(text, file=out)


def _exports(dest: Path, out: TextIO) -> None:
    _say(out)
    _say(out, "Resolved paths (toaster.tools finds these under .tools/ automatically; to use another --dest, export):")
    for var, rel in (
        ("SYSMLV2_BINARY", "bin/sysmlv2"),
        ("Z3", "bin/z3"),
        ("PLANTUML_JAR", "plantuml.jar"),
        ("SYSMLV2_LIB_DIR", "sysml.library"),
    ):
        _say(out, f"export {var}={shlex.quote(str(dest / rel))}")
    _say(out, "Java is not provisioned: install a JRE and put `java` on PATH (or export JAVA=/path/to/java).")


def check_command(dest: Path, pins: dict, platform_key: str, out: TextIO) -> int:
    items, problems = plan(pins, platform_key)
    for line in problems:
        _say(out, f"FAIL {line}")
    manifest = load_manifest(dest)
    bad = len(problems)
    for item in items:
        reason = problem_with(dest, manifest, item)
        if reason:
            bad += 1
            _say(out, f"FAIL {item.name}: {reason}")
        else:
            _say(out, f"ok   {item.name}: {dest / item.rel}")
    if bad:
        _say(out, f"{bad} problem(s). Fix with: uv run python scripts/provision-tools.py --dest {shlex.quote(str(dest))}")
        return 1
    _exports(dest, out)
    return 0


def provision_command(
    dest: Path,
    pins: dict,
    platform_key: str,
    out: TextIO,
    downloader: Downloader = download,
    library_fetcher: LibraryFetcher = fetch_library,
) -> int:
    items, problems = plan(pins, platform_key)
    if problems:
        for line in problems:
            _say(out, f"error: {line}")
        return 2
    manifest = load_manifest(dest)
    todo = [i for i in items if problem_with(dest, manifest, i)]
    for item in items:
        if item not in todo:
            _say(out, f"kept      {item.name}: {dest / item.rel} (matches pin)")
    staged: dict[str, Path] = {}
    # Stage everything in a temporary directory outside dest: a failure leaves dest untouched.
    with tempfile.TemporaryDirectory(prefix="provision-tools-") as tmp_name:
        tmp = Path(tmp_name)
        try:
            for item in todo:
                _say(out, f"fetching  {item.name}: {item.url}")
                if item.kind == "git":
                    staging = tmp / "library" / "sysml.library"
                    library_fetcher(item.url, item.source, staging)
                    if not (staging / "Systems Library").is_dir():
                        raise ValueError("fetched library has no 'Systems Library' directory")
                    staged[item.name] = staging
                    continue
                archive = tmp / f"{item.name}-download"
                downloader(item.url, archive)
                verify_sha256(archive, item.source)
                if item.kind == "file":
                    staged[item.name] = archive
                else:
                    staged[item.name] = extract_member(archive, item.member, tmp / f"{item.name}-staged")
        except (ValueError, OSError, tarfile.TarError, zipfile.BadZipFile, subprocess.CalledProcessError) as exc:
            _say(out, f"error: {exc}")
            _say(out, f"nothing was installed under {dest}")
            return 1
        dest.mkdir(parents=True, exist_ok=True)
        for item in todo:
            target = dest / item.rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if item.kind == "git":
                if target.exists() or target.is_symlink():
                    shutil.rmtree(target)
                shutil.move(str(staged[item.name]), target)
                installed = tree_sha256(target)
            else:
                part = target.with_name(target.name + ".part")
                shutil.move(str(staged[item.name]), part)
                if item.executable:
                    part.chmod(part.stat().st_mode | 0o755)
                os.replace(part, target)
                installed = sha256_of(target)
            manifest[item.name] = {"source": item.source, "installed": item.rel, "installed_sha256": installed}
            _say(out, f"installed {item.name}: {target}")
    (dest / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    _exports(dest, out)
    return 0


def main(
    argv: list[str] | None = None,
    *,
    out: TextIO | None = None,
    downloader: Downloader = download,
    library_fetcher: LibraryFetcher = fetch_library,
) -> int:
    out = out or sys.stdout
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dest", type=Path, default=REPO_ROOT / ".tools", help="install directory (default: <repo>/.tools)")
    parser.add_argument("--check", action="store_true", help="verify installed files against the pins; exit 1 on any problem")
    parser.add_argument("--pins", type=Path, default=DEFAULT_PINS, help="pins file (default: scripts/tool-pins.json)")
    args = parser.parse_args(argv)
    try:
        pins = load_pins(args.pins)
    except (OSError, ValueError) as exc:
        _say(out, f"error: cannot read pins: {exc}")
        return 2
    try:
        platform_key = "-".join(current_platform())
    except ValueError as exc:
        keys = sorted({k for t in ("sysmlv2", "z3") for k in pins[t]["assets"]})
        _say(
            out,
            f"error: {exc}; supported keys are {', '.join(keys)}; "
            f"otherwise point to your own tools with the environment variables {', '.join(ENV_VARS)} "
            f"({_Z3_HINT})",
        )
        return 2
    dest = args.dest.expanduser().resolve()
    if args.check:
        return check_command(dest, pins, platform_key, out)
    return provision_command(dest, pins, platform_key, out, downloader, library_fetcher)


if __name__ == "__main__":
    sys.exit(main())
