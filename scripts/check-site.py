#!/usr/bin/env python3
"""Release gate for the built site: log, figures, host-path leaks, published files, internal links.

Usage:
    uv run python scripts/check-site.py --site _build/html --content _build/site/content \
        --log build.log --base-url /toaster [--baseline scripts/site-baseline.json]

Exit 0 only if every check passes. Each check function returns a list of failure
strings (empty means pass). Thresholds come from the baseline file, never from here.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Sequence
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

LOG_MARKERS = (
    "An exception occurred during code execution",
    "Could not load Jupyter session manager",
    "Jupyter server did not start",
)
LEAK_STRINGS = (
    "/home/runner",
    "/opt/homebrew",
    "Documents/GitHub",
    "/Users/",
    "/var/folders",
)
PUBLISHED_PREFIXES = ("exercise", "DEFERRED")

ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b[@-Z\\-_]")


def check_log(log_text: str) -> list[str]:
    """Fail on any line carrying a code-execution or Jupyter-session failure marker."""
    if not log_text.strip():
        return ["log is empty"]
    failures = []
    for lineno, line in enumerate(ANSI_RE.sub("", log_text).splitlines(), start=1):
        for marker in LOG_MARKERS:
            if marker in line:
                failures.append(f"log line {lineno}: {line.strip()}")
                break
    return failures


def _count_images(node: object) -> int:
    n = 0
    if isinstance(node, dict):
        jd = node.get("jupyter_data")
        if isinstance(jd, dict):
            data = jd.get("data")
            if isinstance(data, dict) and any(str(k).startswith("image/") for k in data):
                n += 1
        for v in node.values():
            n += _count_images(v)
    elif isinstance(node, list):
        for v in node:
            n += _count_images(v)
    return n


def figure_counts(content_dir: Path) -> tuple[dict[str, int], list[str]]:
    """Per-page image-output counts from <content_dir>/*.json, plus read errors."""
    counts: dict[str, int] = {}
    errors: list[str] = []
    for path in sorted(content_dir.glob("*.json")):
        try:
            counts[path.name] = _count_images(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError) as exc:
            errors.append(f"unreadable page JSON {path.name}: {exc}")
    return counts, errors


def check_figures(content_dir: Path, expected: int) -> list[str]:
    """Fail unless the total number of image output nodes equals the baseline."""
    content_dir = Path(content_dir)
    if not content_dir.is_dir():
        return [f"content directory not found: {content_dir}"]
    counts, errors = figure_counts(content_dir)
    failures = list(errors)
    if not counts:
        failures.append(f"no page JSON found in {content_dir}")
    total = sum(counts.values())
    if total != expected:
        per_page = ", ".join(f"{name}={n}" for name, n in counts.items() if n) or "none"
        failures.append(f"figure count {total} != baseline {expected} (per page: {per_page})")
    return failures


def _is_text(data: bytes) -> bool:
    """grep -I semantics: a NUL byte means binary."""
    return b"\0" not in data


def site_problem(site_dir: Path) -> str | None:
    """A message if site_dir is not a built site (not a directory, or no index.html), else None."""
    site_dir = Path(site_dir)
    if not site_dir.is_dir():
        return f"site directory not found: {site_dir}"
    if not (site_dir / "index.html").is_file():
        return f"site directory has no index.html (empty or not a built site): {site_dir}"
    return None


def needle_variants(needle: str) -> list[tuple[str, str]]:
    """(form, text) pairs: the raw string, its JSON-escaped form and its percent-encoded forms."""
    pct = quote(needle, safe="")
    forms = [
        ("raw", needle),
        ("json-escaped", needle.replace("\\", "\\\\").replace("/", "\\/")),
        ("unicode-escaped", needle.replace("/", "\\u002f")),
        ("unicode-escaped", needle.replace("/", "\\u002F")),
        ("percent-encoded", pct),
        ("percent-encoded", re.sub(r"%[0-9A-F]{2}", lambda m: m.group().lower(), pct)),
    ]
    seen: set[str] = set()
    out = []
    for form, text in forms:
        if text not in seen:
            seen.add(text)
            out.append((form, text))
    return out


def check_leaks(site_dir: Path, extra: Sequence[str] = ()) -> list[str]:
    """Fail if any text file under the site contains a host path or an extra string.

    Each needle is also matched in its JSON-escaped and percent-encoded forms.
    """
    site_dir = Path(site_dir)
    problem = site_problem(site_dir)
    if problem:
        return [problem]
    needles = [s for s in (*LEAK_STRINGS, *extra) if s]
    needles = list(dict.fromkeys(needles))
    encoded = [(n, form, text.encode("utf-8")) for n in needles for form, text in needle_variants(n)]
    failures = []
    for path in sorted(site_dir.rglob("*")):
        if not path.is_file():
            continue
        try:
            data = path.read_bytes()
        except OSError as exc:
            failures.append(f"unreadable {path.relative_to(site_dir)}: {exc}")
            continue
        if not _is_text(data):
            continue
        hit: set[tuple[str, str]] = set()
        for needle, form, raw in encoded:
            if (needle, form) not in hit and raw in data:
                hit.add((needle, form))
                suffix = "" if form == "raw" else f" ({form} form)"
                failures.append(f"{path.relative_to(site_dir)} contains {needle!r}{suffix}")
    return failures


def check_published_files(site_dir: Path) -> list[str]:
    """Fail if <site>/build/ holds exercise* or DEFERRED* files."""
    problem = site_problem(site_dir)
    if problem:
        return [problem]
    build = Path(site_dir) / "build"
    if not build.is_dir():
        return []
    return [
        f"build/{p.relative_to(build)}"
        for p in sorted(build.rglob("*"))
        if p.is_file() and p.name.startswith(PUBLISHED_PREFIXES)
    ]


CSS_URL_RE = re.compile(r"""url\(\s*(?:"([^"]*)"|'([^']*)'|([^)\s'"]*))\s*\)""", re.IGNORECASE)


def _css_urls(css: str) -> list[str]:
    return [next(g for g in m.groups() if g is not None).strip() for m in CSS_URL_RE.finditer(css)]


class _RefParser(HTMLParser):
    """Collect href/src, srcset candidates, meta content values and CSS url() references."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[str] = []
        self._in_style = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "style":
            self._in_style = True
        for name, value in attrs:
            if not value:
                continue
            value = value.strip()
            if name in ("href", "src"):
                self.refs.append(value)
            elif name in ("srcset", "imagesrcset"):
                for candidate in value.split(","):
                    parts = candidate.split()
                    if parts:
                        self.refs.append(parts[0])
            elif name == "content" and tag == "meta" and value.startswith("/"):
                self.refs.append(value)
            elif name == "style":
                self.refs.extend(_css_urls(value))

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self._in_style = False

    def handle_data(self, data: str) -> None:
        if self._in_style:
            self.refs.extend(_css_urls(data))


def _normalize_base(base_url: str) -> str:
    return base_url.rstrip("/")


def check_links(site_dir: Path, base_url: str) -> list[str]:
    """Every root-relative href/src must carry the base URL and resolve inside the site."""
    site_dir = Path(site_dir)
    problem = site_problem(site_dir)
    if problem:
        return [problem]
    base = _normalize_base(base_url)
    failures = []
    checked = 0
    for page in sorted(site_dir.rglob("*.html")):
        parser = _RefParser()
        try:
            parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        except Exception as exc:  # html.parser is lenient, but report rather than crash
            failures.append(f"{page.relative_to(site_dir)}: unparseable ({exc})")
            continue
        rel_page = page.relative_to(site_dir)
        for ref in parser.refs:
            if not ref.startswith("/") or ref.startswith("//"):
                continue  # http(s)://, mailto:, #-only, relative and protocol-relative are out of scope
            checked += 1
            path = unquote(urlsplit(ref).path)
            if base and not (path == base or path.startswith(base + "/")):
                failures.append(f"{rel_page}: {ref} does not begin with base {base}")
                continue
            local = path[len(base):].lstrip("/")
            target = site_dir / local if local else site_dir
            if target.is_file() or (target.is_dir() and (target / "index.html").is_file()):
                continue
            failures.append(f"{rel_page}: {ref} not found in site")
    if checked == 0:
        failures.append(f"no root-relative references found to check under {site_dir}")
    return failures


def _report(name: str, failures: list[str]) -> bool:
    if failures:
        print(f"FAIL {name} ({len(failures)})")
        for item in failures:
            print(f"  {item}")
        return False
    print(f"PASS {name}")
    return True


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", type=Path, required=True, help="built HTML directory, e.g. _build/html")
    ap.add_argument("--content", type=Path, required=True, help="page JSON directory, e.g. _build/site/content")
    ap.add_argument("--log", type=Path, required=True, help="captured build log")
    ap.add_argument("--base-url", required=True, help="site base URL, e.g. /toaster")
    ap.add_argument(
        "--baseline",
        type=Path,
        default=Path(__file__).resolve().parent / "site-baseline.json",
        help="JSON file with the expected figure count",
    )
    args = ap.parse_args(argv)

    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    expected = int(baseline["figures"])
    try:
        log_text = args.log.read_text(encoding="utf-8", errors="replace")
        log_failures = check_log(log_text)
    except OSError as exc:
        log_failures = [f"cannot read log {args.log}: {exc}"]
    extra = [str(Path.home()), str(Path.cwd())]

    results = [
        _report("check_log", log_failures),
        _report("check_figures", check_figures(args.content, expected)),
        _report("check_leaks", check_leaks(args.site, extra)),
        _report("check_published_files", check_published_files(args.site)),
        _report("check_links", check_links(args.site, args.base_url)),
    ]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
