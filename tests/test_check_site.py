"""Tests for scripts/check-site.py on tiny fixture trees. Offline; no build, no tools."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-site.py"
BASELINE = SCRIPT.parent / "site-baseline.json"
_spec = importlib.util.spec_from_file_location("check_site", SCRIPT)
cs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cs)

BASE = "/toaster"


def fig(mime: str = "image/svg+xml") -> dict:
    return {"type": "output", "children": [{"jupyter_data": {"data": {mime: "<svg/>"}}}]}


def write_content(content: Path, per_page: dict[str, int]) -> None:
    content.mkdir(parents=True, exist_ok=True)
    for name, n in per_page.items():
        tree = {"mdast": {"children": [fig() for _ in range(n)] + [{"jupyter_data": {"data": {"text/plain": "x"}}}]}}
        (content / f"{name}.json").write_text(json.dumps(tree))


def write_site(site: Path) -> None:
    (site / "build").mkdir(parents=True)
    (site / "ch01").mkdir()
    (site / "index.html").write_text(
        f'<html><a href="{BASE}/ch01/">c1</a><a href="{BASE}/ch01/">c1</a>'
        f'<link href="{BASE}/build/app.css"><script src="{BASE}/build/app.js"></script>'
        '<a href="https://example.org/x">e</a><a href="mailto:a@b.c">m</a><a href="#top">t</a>'
        f'<a href="{BASE}/ch01/#frag">f</a></html>'
    )
    (site / "ch01" / "index.html").write_text(f'<a href="{BASE}/">home</a>')
    (site / "build" / "app.css").write_text("body{}")
    (site / "build" / "app.js").write_text("1")


@pytest.fixture
def site(tmp_path: Path) -> Path:
    s = tmp_path / "html"
    write_site(s)
    return s


# check_log
def test_log_good():
    assert cs.check_log("building\nall done\n") == []


@pytest.mark.parametrize("marker", cs.LOG_MARKERS)
def test_log_fails_on_each_marker(marker):
    out = cs.check_log(f"ok\n{marker}: boom\n")
    assert len(out) == 1 and "line 2" in out[0]


def test_log_strips_ansi():
    assert cs.check_log("\x1b[31mAn exception occurred\x1b[0m during code execution\n")
    assert cs.check_log("An exception occ\x1b[1murred during code execution\n")


# check_figures
def test_figures_good(tmp_path):
    write_content(tmp_path / "c", {"a": 10, "b": 8, "empty": 0})
    assert cs.check_figures(tmp_path / "c", 18) == []


def test_figures_17_vs_18(tmp_path):
    write_content(tmp_path / "c", {"a": 10, "b": 7})
    out = cs.check_figures(tmp_path / "c", 18)
    assert len(out) == 1 and "17" in out[0] and "18" in out[0] and "a.json=10" in out[0]


def test_figures_nested_and_non_image_not_counted(tmp_path):
    c = tmp_path / "c"
    c.mkdir()
    (c / "p.json").write_text(json.dumps({"a": [{"b": {"jupyter_data": {"data": {"image/png": "x", "image/svg+xml": "y"}}}}]}))
    assert cs.check_figures(c, 1) == []
    (c / "q.json").write_text(json.dumps({"jupyter_data": {"data": {"text/html": "x"}}}))
    assert cs.check_figures(c, 1) == []


def test_figures_missing_or_empty_dir(tmp_path):
    assert cs.check_figures(tmp_path / "nope", 18)
    (tmp_path / "e").mkdir()
    assert cs.check_figures(tmp_path / "e", 18)


def test_figures_unreadable_json(tmp_path):
    write_content(tmp_path / "c", {"a": 18})
    (tmp_path / "c" / "bad.json").write_text("{not json")
    assert any("bad.json" in f for f in cs.check_figures(tmp_path / "c", 18))


def test_baseline_file():
    assert json.loads(BASELINE.read_text()) == {"figures": 18}


# check_leaks
def test_leaks_good(site):
    assert cs.check_leaks(site) == []


@pytest.mark.parametrize("s", ["/opt/homebrew", "/home/runner", "Documents/GitHub", "/Users/", "/var/folders"])
def test_leaks_each_default(site, s):
    (site / "ch01" / "leak.js").write_text(f"x = '{s}/bin'")
    out = cs.check_leaks(site)
    assert len(out) == 1 and "ch01/leak.js" in out[0] and s in out[0]


def test_leaks_extra_and_skip_binary(site):
    (site / "a.txt").write_text("secret-home-xyz")
    assert cs.check_leaks(site) == []
    assert cs.check_leaks(site, ["secret-home-xyz"])
    (site / "a.bin").write_bytes(b"\0\1/opt/homebrew")
    assert [f for f in cs.check_leaks(site) if "a.bin" in f] == []


# check_published_files
def test_published_good(site):
    assert cs.check_published_files(site) == []


@pytest.mark.parametrize("name", ["exercise-xyz.ipynb", "exercise01.md", "DEFERRED.md"])
def test_published_fails(site, name):
    (site / "build" / name).write_text("x")
    assert cs.check_published_files(site) == [f"build/{name}"]


def test_published_nested_and_outside_build_ignored(site):
    (site / "build" / "sub").mkdir()
    (site / "build" / "sub" / "exercise-a.ipynb").write_text("x")
    (site / "exercise-page.html").write_text("x")
    assert cs.check_published_files(site) == ["build/sub/exercise-a.ipynb"]


# check_links
def test_links_good(site):
    assert cs.check_links(site, BASE) == []
    assert cs.check_links(site, BASE + "/") == []


def test_links_broken(site):
    (site / "ch01" / "index.html").write_text(f'<a href="{BASE}/missing/">x</a><img src="{BASE}/build/gone.png">')
    out = cs.check_links(site, BASE)
    assert len(out) == 2 and all("ch01/index.html" in f for f in out)


def test_links_wrong_base(site):
    (site / "index.html").write_text('<a href="/other/ch01/">x</a><a href="/toasterx/ch01/">y</a><a href="/ch01/">z</a>')
    out = cs.check_links(site, BASE)
    assert len(out) == 3 and all("does not begin with base" in f for f in out)


def test_links_dir_without_index_is_broken(site):
    (site / "empty").mkdir()
    (site / "index.html").write_text(f'<a href="{BASE}/empty/">x</a>')
    assert len(cs.check_links(site, BASE)) == 1


def test_links_base_root_only(site):
    (site / "index.html").write_text(f'<a href="{BASE}">x</a><a href="{BASE}/">y</a>')
    assert cs.check_links(site, BASE) == []


# missing / empty inputs must fail
SITE_CHECKS = {
    "leaks": lambda d: cs.check_leaks(d),
    "published": lambda d: cs.check_published_files(d),
    "links": lambda d: cs.check_links(d, BASE),
}


@pytest.mark.parametrize("name", list(SITE_CHECKS))
def test_site_checks_fail_on_missing_dir(tmp_path, name):
    out = SITE_CHECKS[name](tmp_path / "nonexistent")
    assert len(out) == 1 and "nonexistent" in out[0]


@pytest.mark.parametrize("name", list(SITE_CHECKS))
def test_site_checks_fail_on_empty_dir(tmp_path, name):
    (tmp_path / "empty").mkdir()
    out = SITE_CHECKS[name](tmp_path / "empty")
    assert len(out) == 1 and "no index.html" in out[0] and "empty" in out[0]


@pytest.mark.parametrize("name", list(SITE_CHECKS))
def test_site_checks_fail_on_file_not_dir(tmp_path, name):
    (tmp_path / "f").write_text("x")
    assert SITE_CHECKS[name](tmp_path / "f")


def test_site_dir_without_root_index_fails(tmp_path):
    (tmp_path / "ch01").mkdir()
    (tmp_path / "ch01" / "index.html").write_text("<a href='/toaster/'>x</a>")
    assert all(SITE_CHECKS[n](tmp_path) for n in SITE_CHECKS)


@pytest.mark.parametrize("text", ["", "   \n\n"])
def test_log_empty_fails(text):
    assert cs.check_log(text) == ["log is empty"]


def test_links_zero_references_fails(tmp_path):
    s = tmp_path / "s"
    s.mkdir()
    (s / "index.html").write_text('<a href="https://example.org/">e</a><a href="#x">t</a><p>no refs</p>')
    out = cs.check_links(s, BASE)
    assert len(out) == 1 and "no root-relative references" in out[0]


# leak variants
@pytest.mark.parametrize(
    "text,form",
    [
        ('{"p": "\\/opt\\/homebrew\\/bin"}', "json-escaped"),
        ("see%2Fopt%2Fhomebrew%2Fbin", "percent-encoded"),
        ("see%2fopt%2fhomebrew", "percent-encoded"),
        ("a%2FUsers%2Fz", "percent-encoded"),
        ("Documents%2FGitHub", "percent-encoded"),
        ('"Documents\\/GitHub"', "json-escaped"),
        ("\\u002fvar\\u002ffolders", "unicode-escaped"),
    ],
)
def test_leaks_encoded_variants(site, text, form):
    (site / "ch01" / "enc.json").write_text(text)
    out = cs.check_leaks(site)
    assert out and all("ch01/enc.json" in f for f in out) and any(form in f for f in out)


def test_leaks_encoded_extra(site):
    (site / "x.json").write_text("p=%2Fsome%2Fcwd")
    assert cs.check_leaks(site) == []
    assert cs.check_leaks(site, ["/some/cwd"])


# link reference forms
def link_site(tmp_path: Path, body: str) -> Path:
    s = tmp_path / "ls"
    s.mkdir(parents=True)
    (s / "index.html").write_text(body)
    (s / "img.png").write_text("x")
    return s


def test_links_srcset_good_and_broken(tmp_path):
    s = link_site(tmp_path, f'<img srcset="{BASE}/img.png 1x, {BASE}/img.png 2x"><a href="{BASE}/">h</a>')
    assert cs.check_links(s, BASE) == []
    s = link_site(tmp_path / "b", f'<img srcset="{BASE}/img.png 1x, {BASE}/gone.png 2x, /bad/img.png 3x"><a href="{BASE}/">h</a>')
    out = cs.check_links(s, BASE)
    assert len(out) == 2 and any("gone.png" in f for f in out) and any("/bad/img.png" in f for f in out)


def test_links_meta_content(tmp_path):
    body = (
        f'<a href="{BASE}/">h</a><meta property="og:image" content="{BASE}/img.png">'
        '<meta name="description" content="not a path"><meta name="x" content="//cdn.example/x">'
    )
    assert cs.check_links(link_site(tmp_path, body), BASE) == []
    bad = f'<a href="{BASE}/">h</a><meta property="og:image" content="{BASE}/gone.png"><meta name="y" content="/other/img.png">'
    out = cs.check_links(link_site(tmp_path / "b", bad), BASE)
    assert len(out) == 2


def test_links_css_urls(tmp_path):
    good = (
        f'<a href="{BASE}/">h</a><div style="background:url({BASE}/img.png)"></div>'
        f"<style>.a{{background:url('{BASE}/img.png')}} .b{{background:url(\"{BASE}/img.png\")}} .c{{background:url(data:image/png;base64,AA==)}} .d{{background:url(https://e.org/x.png)}}</style>"
    )
    assert cs.check_links(link_site(tmp_path, good), BASE) == []
    bad = (
        f'<a href="{BASE}/">h</a><div style="background:url({BASE}/gone1.png)"></div>'
        f"<style>.a{{background:url('{BASE}/gone2.png')}} .b{{background:url(/wrong/img.png)}}</style>"
    )
    out = cs.check_links(link_site(tmp_path / "b", bad), BASE)
    assert len(out) == 3


# CLI
def run_cli(site, content, log, base=BASE, extra=()):
    return cs.main(["--site", str(site), "--content", str(content), "--log", str(log), "--base-url", base, "--baseline", str(BASELINE), *extra])


def test_cli_all_pass(site, tmp_path, capsys):
    write_content(tmp_path / "c", {"a": 18})
    (tmp_path / "log").write_text("fine\n")
    assert run_cli(site, tmp_path / "c", tmp_path / "log") == 0
    out = capsys.readouterr().out
    assert out.count("PASS") == 5 and "FAIL" not in out


def test_cli_fails_and_names_check(site, tmp_path, capsys):
    write_content(tmp_path / "c", {"a": 17})
    (tmp_path / "log").write_text("Jupyter server did not start\n")
    (site / "build" / "DEFERRED.md").write_text("x")
    assert run_cli(site, tmp_path / "c", tmp_path / "log", base="/wrong") == 1
    out = capsys.readouterr().out
    for name in ("check_log", "check_figures", "check_published_files", "check_links"):
        assert f"FAIL {name}" in out
    assert "PASS check_leaks" in out


def test_cli_missing_site_exits_1(tmp_path, capsys):
    write_content(tmp_path / "c", {"a": 18})
    (tmp_path / "log").write_text("fine\n")
    assert run_cli(tmp_path / "nonexistent", tmp_path / "c", tmp_path / "log") == 1
    out = capsys.readouterr().out
    for name in ("check_leaks", "check_published_files", "check_links"):
        assert f"FAIL {name}" in out
    assert "PASS check_log" in out and "PASS check_figures" in out


def test_cli_empty_site_exits_1(tmp_path):
    (tmp_path / "s").mkdir()
    write_content(tmp_path / "c", {"a": 18})
    (tmp_path / "log").write_text("fine\n")
    assert run_cli(tmp_path / "s", tmp_path / "c", tmp_path / "log") == 1


def test_cli_empty_log_exits_1(site, tmp_path, capsys):
    write_content(tmp_path / "c", {"a": 18})
    (tmp_path / "log").write_text("")
    assert run_cli(site, tmp_path / "c", tmp_path / "log") == 1
    assert "FAIL check_log" in capsys.readouterr().out


def test_cli_missing_log_exits_1(site, tmp_path):
    write_content(tmp_path / "c", {"a": 18})
    assert run_cli(site, tmp_path / "c", tmp_path / "nolog") == 1
