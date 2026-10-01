"""Tests for toaster.bootstrap.ensure_cli_binary() (Phase 2 Task 1)."""
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from toaster.bootstrap import ensure_cli_binary, _CLI_SUMS, _cli_cache_dir


def test_sha256_pins_cover_darwin_and_linux():
    """The pins this task's own implementation ships must cover at least the
    platforms this repo's own contributors actually use."""
    assert ("darwin", "amd64") in _CLI_SUMS
    assert ("darwin", "arm64") in _CLI_SUMS
    assert ("linux", "amd64") in _CLI_SUMS
    assert _CLI_SUMS[("darwin", "arm64")] == (
        "0129f277bd10c73ca09c7ce643cf7ae9b6b496250925d1a640ef1e2930340efb"
    )


def test_ensure_cli_binary_downloads_verifies_and_caches():
    """End-to-end: a real network call against the real pinned v0.9.0 release.
    This is the one test in this file that touches the network -- skip it only
    if explicitly offline, never silently."""
    path = ensure_cli_binary(version="v0.9.0")
    assert path.exists()
    assert path.is_file()
    result = subprocess.run([str(path), "-version"], capture_output=True, text=True, timeout=10)
    assert "sysml v0.9.0" in result.stdout
    assert "ee54ea03ea3ca8fb2c796ecda364adf748c40304" in result.stdout


def test_ensure_cli_binary_is_idempotent_and_skips_network_on_cache_hit():
    """A second call must return the same path without re-downloading -- verified
    by checking the cached file's own mtime is unchanged across the two calls."""
    first = ensure_cli_binary(version="v0.9.0")
    mtime_before = first.stat().st_mtime
    second = ensure_cli_binary(version="v0.9.0")
    assert second == first
    assert second.stat().st_mtime == mtime_before


def test_ensure_cli_binary_rejects_a_tampered_download(monkeypatch, tmp_path):
    """A SHA256 mismatch must raise, not silently install a wrong binary --
    simulated by pointing the cache dir at a scratch location and corrupting
    the pin table for this one test only.

    Corrupts the pin for THIS machine's own real platform (via
    opensysml.binary.detect_platform(), the same lookup ensure_cli_binary()
    itself performs), not a hardcoded ("darwin", "arm64") -- a hardcoded key
    would silently not test anything on a different platform (e.g. a Linux CI
    runner), since the code would look up and correctly verify against the
    real, uncorrupted hash for ITS OWN platform instead. Found by independent
    review (reviewer probe: flipping one byte of the real pin left the test
    passing on darwin-arm64 but silently installing an untampered binary when
    simulated on linux-amd64)."""
    import opensysml.binary as ob
    import toaster.bootstrap as bootstrap_mod

    this_platform = ob.detect_platform()
    monkeypatch.setattr(bootstrap_mod, "_cli_cache_dir", lambda: tmp_path)
    bad_sums = dict(bootstrap_mod._CLI_SUMS)
    bad_sums[this_platform] = "0" * 64
    monkeypatch.setattr(bootstrap_mod, "_CLI_SUMS", bad_sums)
    with pytest.raises(RuntimeError, match="sha256 mismatch"):
        ensure_cli_binary(version="v0.9.0")
    assert not (tmp_path / "sysml").exists()
