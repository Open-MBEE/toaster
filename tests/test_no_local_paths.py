"""Guard: nothing shippable names a developer's home directory, Homebrew prefix or checkout path.

Tools are found through `toaster.tools` (an argument, an environment variable, `.tools/`, then PATH),
never through a path baked into a notebook, a module, a test or a script. This test fails if any of
the forbidden strings below reappears in

  (a) a code cell of any notebook under chapters/ or exercises/, or
  (b) any .py file under src/, tests/ or scripts/, or
  (c) a markdown cell, or a stored output (stream text, text/plain, application/json, SVG text), of
      any notebook under chapters/ or exercises/, or
  (d) a published docs page: docs/**/*.md except docs/superpowers/ (plans and specs that myst.yml's
      toc does not build).

The allowlist is exactly: this file and the site-gate pair scripts/check-site.py and
tests/test_check_site.py (all three have to spell the strings out: they are the scanners and their
fixtures), and the one line in src/toaster/bootstrap.py that builds the `.opensysml` cache directory
under the user's home (`Path.home()` and `".opensysml"` on the same line; a cache location, not a tool
location).
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN = ("Path.home()", "/opt/homebrew", "Documents/GitHub", "/Users/", "/home/")

THIS_FILE = Path(__file__).resolve()
SPELLS_THE_STRINGS = {
    THIS_FILE,
    (ROOT / "scripts" / "check-site.py").resolve(),
    (ROOT / "tests" / "test_check_site.py").resolve(),
}
BOOTSTRAP = ROOT / "src" / "toaster" / "bootstrap.py"
BOOTSTRAP_ALLOWED_MARKER = '".opensysml"'


def _is_bootstrap_cache_line(line: str) -> bool:
    # Another line in bootstrap.py also mentions ".opensysml" but names no forbidden string; the
    # allowlist is the one line that does (the home-directory cache location).
    return BOOTSTRAP_ALLOWED_MARKER in line and "Path.home()" in line


def find_forbidden(text: str) -> list[str]:
    """The forbidden strings present in `text` (in FORBIDDEN order, each once)."""
    return [needle for needle in FORBIDDEN if needle in text]


def find_forbidden_in_py(path: Path, text: str) -> list[str]:
    """As `find_forbidden`, for a .py file, honouring the allowlist."""
    if path.resolve() in SPELLS_THE_STRINGS:
        return []
    if path.resolve() == BOOTSTRAP:
        text = "\n".join(
            line for line in text.splitlines() if not _is_bootstrap_cache_line(line)
        )
    return find_forbidden(text)


def _text(value) -> str:
    return "".join(value) if isinstance(value, list) else str(value)


def _output_texts(output: dict):
    """The text a stored output would show a reader, one string per kind that carries text."""
    if "text" in output:  # stream
        yield "stream", _text(output["text"])
    data = output.get("data", {})
    if "text/plain" in data:
        yield "text/plain", _text(data["text/plain"])
    if "application/json" in data:
        yield "application/json", json.dumps(data["application/json"])
    if "image/svg+xml" in data:
        yield "image/svg+xml", _text(data["image/svg+xml"])


def _notebooks(root: Path):
    for top in ("chapters", "exercises"):
        for nb in sorted((root / top).rglob("*.ipynb")):
            if ".ipynb_checkpoints" in nb.parts:
                continue
            yield nb, json.loads(nb.read_text(encoding="utf-8")).get("cells", [])


def _notebook_cases(root: Path):
    for nb, cells in _notebooks(root):
        for index, cell in enumerate(cells):
            if cell.get("cell_type") != "code":
                continue
            yield pytest.param(
                _text(cell.get("source", "")), id=f"{nb.relative_to(root).as_posix()}::cell-{index}"
            )


def _markdown_cases(root: Path):
    for nb, cells in _notebooks(root):
        for index, cell in enumerate(cells):
            if cell.get("cell_type") != "markdown":
                continue
            yield pytest.param(
                _text(cell.get("source", "")),
                id=f"{nb.relative_to(root).as_posix()}::markdown-{index}",
            )


def _output_cases(root: Path):
    for nb, cells in _notebooks(root):
        for index, cell in enumerate(cells):
            for n, output in enumerate(cell.get("outputs", [])):
                for kind, text in _output_texts(output):
                    yield pytest.param(
                        text,
                        id=f"{nb.relative_to(root).as_posix()}::cell-{index}::output-{n}::{kind}",
                    )


def _docs_cases(root: Path):
    for md in sorted((root / "docs").rglob("*.md")):
        if "superpowers" in md.relative_to(root / "docs").parts:
            continue
        yield pytest.param(md, id=md.relative_to(root).as_posix())


def _python_cases(root: Path):
    for top in ("src", "tests", "scripts"):
        for py in sorted((root / top).rglob("*.py")):
            if any(part in (".venv", "__pycache__") for part in py.parts):
                continue
            yield pytest.param(py, id=py.relative_to(root).as_posix())


@pytest.mark.parametrize("source", list(_notebook_cases(ROOT)))
def test_notebook_code_cell_names_no_local_path(source):
    assert find_forbidden(source) == []


@pytest.mark.parametrize("source", list(_markdown_cases(ROOT)))
def test_notebook_markdown_cell_names_no_local_path(source):
    assert find_forbidden(source) == []


@pytest.mark.parametrize("text", list(_output_cases(ROOT)))
def test_notebook_stored_output_names_no_local_path(text):
    assert find_forbidden(text) == []


@pytest.mark.parametrize("path", list(_docs_cases(ROOT)))
def test_published_docs_page_names_no_local_path(path):
    assert find_forbidden(path.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize("path", list(_python_cases(ROOT)))
def test_python_file_names_no_local_path(path):
    text = path.read_text(encoding="utf-8")
    assert find_forbidden_in_py(path, text) == []


# --- the scanner itself ----------------------------------------------------------------------------


@pytest.mark.parametrize("needle", FORBIDDEN)
def test_scanner_flags_each_forbidden_string(needle):
    assert find_forbidden(f"x = '{needle}foo'") == [needle]


def test_scanner_passes_clean_text():
    assert find_forbidden("from toaster.tools import resolve_sysmlv2\n") == []


def test_allowlist_covers_exactly_the_bootstrap_cache_line():
    allowed = 'return Path.home() / ".opensysml" / "bin"\n'
    assert find_forbidden_in_py(BOOTSTRAP, allowed) == []
    other = allowed + 'other = Path.home() / "elsewhere"\n'
    assert find_forbidden_in_py(BOOTSTRAP, other) == ["Path.home()"]
    assert find_forbidden_in_py(ROOT / "src" / "toaster" / "other.py", allowed) == [
        "Path.home()"
    ]


def test_bootstrap_has_exactly_one_allowlisted_line():
    lines = [
        line
        for line in BOOTSTRAP.read_text(encoding="utf-8").splitlines()
        if _is_bootstrap_cache_line(line)
    ]
    assert len(lines) == 1


def test_output_scanner_reads_every_text_carrying_kind():
    outputs = [
        {"output_type": "stream", "text": ["a\n", "b\n"]},
        {"output_type": "display_data", "data": {"text/plain": "p", "image/png": "AAAA"}},
        {"output_type": "execute_result", "data": {"application/json": {"k": "/home/x"}}},
        {"output_type": "display_data", "data": {"image/svg+xml": ["<svg>", "</svg>"]}},
    ]
    seen = [(kind, text) for out in outputs for kind, text in _output_texts(out)]
    assert seen == [
        ("stream", "a\nb\n"),
        ("text/plain", "p"),
        ("application/json", '{"k": "/home/x"}'),
        ("image/svg+xml", "<svg></svg>"),
    ]
    assert find_forbidden(seen[2][1]) == ["/home/"]
