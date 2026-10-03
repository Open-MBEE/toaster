"""Offline tests for scripts/provision-tools.py: tiny fake archives, a fake pins file, injected downloaders."""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import stat
import sys
import tarfile
import zipfile
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "provision-tools.py"
spec = importlib.util.spec_from_file_location("provision_tools", SCRIPT)
pt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = pt
spec.loader.exec_module(pt)
REAL_CURRENT_PLATFORM = pt.current_platform

REAL_PINS = SCRIPT.parent / "tool-pins.json"
KEY = "linux-x86_64"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_tar(path: Path, name: str, data: bytes, mode: int = 0o755) -> None:
    with tarfile.open(path, "w:gz") as tf:
        info = tarfile.TarInfo(name)
        info.size = len(data)
        info.mode = mode
        tf.addfile(info, io.BytesIO(data))
        other = tarfile.TarInfo("pkg-1/README.md")
        other.size = 2
        tf.addfile(other, io.BytesIO(b"hi"))


def make_zip(path: Path, name: str, data: bytes, mode: int = 0o755) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        info = zipfile.ZipInfo(name)
        info.external_attr = (stat.S_IFREG | mode) << 16
        zf.writestr(info, data)
        zf.writestr("pkg-1/LICENSE.txt", "x")


@pytest.fixture
def world(tmp_path, monkeypatch):
    """Fake release server: archives in tmp_path, a pins file naming them, and a counting downloader."""
    monkeypatch.setattr(pt, "current_platform", lambda: tuple(KEY.split("-")))
    blobs = tmp_path / "blobs"
    blobs.mkdir()
    make_tar(blobs / "toolkit.tar.gz", "pkg-1/sysmlv2", b"#!/bin/sh\necho sysmlv2 0.9.1\n")
    make_zip(blobs / "z3.zip", "pkg-1/bin/z3", b"#!/bin/sh\necho Z3 5.1.0\n")
    (blobs / "plantuml.jar").write_bytes(b"fake jar")
    pins = {
        "sysmlv2": {"version": "v0", "assets": {KEY: {
            "url": "https://example.test/toolkit.tar.gz",
            "sha256": sha((blobs / "toolkit.tar.gz").read_bytes()),
            "member": "pkg-1/sysmlv2"}}},
        "z3": {"version": "z3-0", "assets": {KEY: {
            "url": "https://example.test/z3.zip",
            "sha256": sha((blobs / "z3.zip").read_bytes()),
            "member": "pkg-1/bin/z3"}}},
        "plantuml": {"version": "v0", "url": "https://example.test/plantuml.jar",
                     "sha256": sha(b"fake jar")},
        "library": {"repo": "https://example.test/lib.git", "commit": "a" * 40},
    }
    pins_path = tmp_path / "pins.json"
    pins_path.write_text(json.dumps(pins))

    class Net:
        def __init__(self) -> None:
            self.downloads: list[str] = []
            self.library_fetches = 0

        def downloader(self, url: str, dest: Path) -> None:
            self.downloads.append(url)
            dest.write_bytes((blobs / url.rsplit("/", 1)[1]).read_bytes())

        def library(self, repo: str, commit: str, dest: Path) -> None:
            self.library_fetches += 1
            (dest / "Systems Library").mkdir(parents=True)
            (dest / "Systems Library" / "Requirements.sysml").write_text(commit)

    net = Net()

    def run(*extra: str, dest: Path | None = None) -> tuple[int, str]:
        out = io.StringIO()
        code = pt.main(
            ["--pins", str(pins_path), "--dest", str(dest or tmp_path / "dest"), *extra],
            out=out, downloader=net.downloader, library_fetcher=net.library,
        )
        return code, out.getvalue()

    return pins_path, pins, blobs, net, run, tmp_path / "dest"


# --- verify_sha256 -----------------------------------------------------------------------------


def test_verify_sha256_passes_and_fails(tmp_path):
    f = tmp_path / "f"
    f.write_bytes(b"abc")
    pt.verify_sha256(f, sha(b"abc"))
    pt.verify_sha256(f, sha(b"abc").upper())
    with pytest.raises(ValueError, match="mismatch"):
        pt.verify_sha256(f, sha(b"abd"))


# --- extract_member ----------------------------------------------------------------------------


def test_extract_member_tar_by_suffix_keeps_exec_bit(tmp_path):
    archive = tmp_path / "a.tar.gz"
    make_tar(archive, "deep/dir/sysmlv2", b"binary", 0o755)
    out = pt.extract_member(archive, "dir/sysmlv2", tmp_path / "out")
    assert out == tmp_path / "out" / "sysmlv2"
    assert out.read_bytes() == b"binary"
    assert os.access(out, os.X_OK)
    assert not list((tmp_path / "out").glob("*.part"))


def test_extract_member_zip_by_suffix_keeps_exec_bit(tmp_path):
    archive = tmp_path / "a.zip"
    make_zip(archive, "z3-1/bin/z3", b"binary", 0o755)
    out = pt.extract_member(archive, "bin/z3", tmp_path / "out")
    assert out == tmp_path / "out" / "z3"
    assert os.access(out, os.X_OK)


def test_extract_member_does_not_invent_exec_bit(tmp_path):
    archive = tmp_path / "a.tar.gz"
    make_tar(archive, "d/data.txt", b"x", 0o644)
    assert not os.access(pt.extract_member(archive, "data.txt", tmp_path / "o"), os.X_OK)


def test_extract_member_missing_ambiguous_and_component_boundary(tmp_path):
    archive = tmp_path / "a.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("a/bin/z3", "1")
        zf.writestr("b/bin/z3", "2")
        zf.writestr("xbin/tool", "3")
    with pytest.raises(FileNotFoundError):
        pt.extract_member(archive, "nope", tmp_path / "o")
    with pytest.raises(ValueError, match="ambiguous"):
        pt.extract_member(archive, "bin/z3", tmp_path / "o")
    with pytest.raises(FileNotFoundError):
        pt.extract_member(archive, "bin/tool", tmp_path / "o")


# --- platform and pins -------------------------------------------------------------------------


@pytest.mark.parametrize(
    "system,machine,expected",
    [("Linux", "x86_64", ("linux", "x86_64")), ("Darwin", "arm64", ("darwin", "arm64")),
     ("Darwin", "x86_64", ("darwin", "x86_64")), ("Linux", "aarch64", ("linux", "arm64"))],
)
def test_current_platform(monkeypatch, system, machine, expected):
    monkeypatch.setattr(pt.platform, "system", lambda: system)
    monkeypatch.setattr(pt.platform, "machine", lambda: machine)
    assert pt.current_platform() == expected


def test_current_platform_rejects_unknown(monkeypatch):
    monkeypatch.setattr(pt.platform, "system", lambda: "Windows")
    with pytest.raises(ValueError):
        pt.current_platform()


def test_real_pins_file_is_valid_and_complete():
    pins = pt.load_pins(REAL_PINS)
    for tool in ("sysmlv2", "z3"):
        assert set(pins[tool]["assets"]) == {"linux-x86_64", "darwin-arm64", "darwin-x86_64"}
    assert pins["library"]["commit"] == "de1070ae8e79c21532b8004fc663d47b35d0e9fa"
    assert pins["plantuml"]["sha256"].startswith("5e1ecfa8")


def test_load_pins_rejects_bad_sha(tmp_path):
    bad = json.loads(REAL_PINS.read_text())
    bad["plantuml"]["sha256"] = "xyz"
    p = tmp_path / "p.json"
    p.write_text(json.dumps(bad))
    with pytest.raises(ValueError, match="plantuml.sha256"):
        pt.load_pins(p)


# --- provisioning ------------------------------------------------------------------------------


def test_provision_installs_layout_and_prints_exports(world):
    _, _, _, net, run, dest = world
    code, out = run()
    assert code == 0, out
    assert os.access(dest / "bin" / "sysmlv2", os.X_OK)
    assert os.access(dest / "bin" / "z3", os.X_OK)
    assert (dest / "plantuml.jar").read_bytes() == b"fake jar"
    assert (dest / "sysml.library" / "Systems Library" / "Requirements.sysml").is_file()
    for var in ("SYSMLV2_BINARY", "Z3", "PLANTUML_JAR", "SYSMLV2_LIB_DIR"):
        assert f"export {var}=" in out
    assert len(net.downloads) == 3 and net.library_fetches == 1


def test_wrong_sha_fails_before_anything_is_installed(world):
    pins_path, pins, _, _, run, dest = world
    # the jar is last in download order: sysmlv2 and z3 download fine first, then the bad pin fires.
    pins["plantuml"]["sha256"] = "0" * 64
    pins_path.write_text(json.dumps(pins))
    code, out = run()
    assert code != 0
    assert "mismatch" in out
    assert "nothing was installed" in out
    assert not dest.exists() or not any(dest.iterdir())


def test_wrong_sha_on_existing_dest_leaves_it_untouched(world):
    pins_path, pins, _, _, run, dest = world
    dest.mkdir()
    (dest / "keep.txt").write_text("mine")
    pins["sysmlv2"]["assets"][KEY]["sha256"] = "1" * 64
    pins_path.write_text(json.dumps(pins))
    assert run()[0] != 0
    assert sorted(p.name for p in dest.iterdir()) == ["keep.txt"]


def test_second_run_downloads_nothing(world):
    _, _, _, net, run, _ = world
    assert run()[0] == 0
    net.downloads.clear()
    fetches = net.library_fetches
    code, out = run()
    assert code == 0
    assert net.downloads == [] and net.library_fetches == fetches
    assert out.count("kept") == 4


def test_tampered_binary_is_replaced_on_rerun(world):
    _, _, _, net, run, dest = world
    run()
    (dest / "bin" / "z3").write_bytes(b"tampered")
    net.downloads.clear()
    assert run()[0] == 0
    assert net.downloads == ["https://example.test/z3.zip"]
    assert b"Z3 5.1.0" in (dest / "bin" / "z3").read_bytes()


# --- --check -----------------------------------------------------------------------------------


def test_check_exit_codes(world):
    _, _, _, net, run, dest = world
    assert run("--check")[0] == 1  # absent
    run()
    assert run("--check")[0] == 0
    (dest / "plantuml.jar").write_bytes(b"other")
    code, out = run("--check")
    assert code == 1 and "plantuml" in out and "mismatch" in out
    run()
    (dest / "bin" / "sysmlv2").write_bytes(b"tampered")
    assert run("--check")[0] == 1
    run()
    (dest / "bin" / "z3").unlink()
    assert run("--check")[0] == 1
    run()
    (dest / "sysml.library" / "Systems Library" / "Requirements.sysml").write_text("changed")
    assert run("--check")[0] == 1
    assert net.downloads  # sanity: the fake downloader was the only network path


def test_check_downloads_nothing(world):
    _, _, _, net, run, _ = world
    run()
    net.downloads.clear()
    run("--check")
    assert net.downloads == []


# --- unsupported platform ------------------------------------------------------------------------


def test_unsupported_platform_lists_keys_and_env_vars(world, monkeypatch):
    _, _, _, net, run, dest = world
    monkeypatch.setattr(pt, "current_platform", lambda: ("linux", "arm64"))
    code, out = run()
    assert code == 2
    assert "linux-arm64" in out and "linux-x86_64" in out
    for var in pt.ENV_VARS:
        assert var in out
    assert "brew install z3" in out
    assert net.downloads == [] and not dest.exists()


def test_unrecognised_machine_message(world, monkeypatch):
    _, _, _, net, run, dest = world
    monkeypatch.setattr(pt, "current_platform", REAL_CURRENT_PLATFORM)
    monkeypatch.setattr(pt.platform, "system", lambda: "Windows")
    code, out = run()
    assert code == 2
    assert "unrecognised platform" in out and "linux-x86_64" in out and "SYSMLV2_BINARY" in out
    assert net.downloads == [] and not dest.exists()
