#!/usr/bin/env python3
"""Guard for the OpenSysML terminology revision (DL-116): did an edit stay on the editable surface?

Usage:
    uv run python scripts/check-terminology-edit.py --base <rev> [--head <rev>] [--repo <dir>]
                                                    [--allow GLOB ...]

`--head` defaults to the working tree (tracked changes against `--base` plus untracked files).
`--repo` may be any directory inside the repository; the repository root is resolved with git.
`--allow GLOB` (repeatable) exempts matching paths from rule (a) for this run only; `*` matches
across `/`, so `glossary/tests/*` covers the whole tree below it. A run with --allow is never
silent: the output starts with an `allow: ...` line, rule (a) lists each exempted violation as an
`info (a) exempted by --allow ...` line, and the final line reads `RESULT: PASS (with N --allow
exemption(s))`. The exit code is unchanged.

SELF: reviewers must run this checker from a pinned revision (the branch named `terminology`
after the guard merges), never from the branch under review, because an edit can change the checker
itself (scripts/ is a protected zone, with this checker's own files the only exemption).
Exit 0 only if every rule passes; exit 1 with one line per violation otherwise; exit 2 on a usage or
git error. Each rule prints PASS or FAIL. The checker judges no prose and edits nothing.

Rules (letters follow contract OT-2):
  (a) no protected zone changed: models/, decisions/judgment-records/, figures/, tests/, src/,
      scripts/, glossary/*.py, glossary/tests/, .github/, uv.lock, pyproject.toml, package.json,
      package-lock.json (any change at all), and decisions/ and docs/superpowers/ (new files only,
      except decisions/log.md, which may also grow by appended lines only); this checker's own two
      files are exempt
  (b) no notebook changed except the `source` of markdown cells (cell count, order, types, ids,
      metadata, code sources, outputs and execution counts compared as JSON)
  (c) protected tokens: per file, the multiset of matched token strings at base must be contained
      in the multiset at head (nothing removed or altered; adding a token is allowed and reported
      as an info line). Whole file; for notebooks code cells, except the issue references
      (OpenSysML#N, sysml-toolkit#N, toaster#N), which are read over all cells
  (d) every `## D-nnn` heading line in DEFERRED.md unchanged
  (e) the list of fenced code blocks in each changed .claude/skills/**/*.md file unchanged, and no
      change at all to a non-markdown file under .claude/skills/ (such files are executed by tests)
  (f) the set of skill directories and each SKILL.md `name:` frontmatter unchanged
  (g) no URL's occurrence count in a changed file decreases (additions are fine)
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

RULES: dict[str, str] = {
    "a": "protected zones unchanged",
    "b": "notebook edits limited to markdown cell source",
    "c": "protected tokens not removed or altered",
    "d": "DEFERRED.md D-nnn headings unchanged",
    "e": "skill fenced code blocks unchanged",
    "f": "skill directories and name: frontmatter unchanged",
    "g": "no URL occurrence removed from a changed file",
}

OWN_FILES = frozenset(
    {"scripts/check-terminology-edit.py", "tests/test_check_terminology_edit.py"}
)

# Zones governed by rule (a). `strict` zones allow no change at all; `new_ok` zones allow added files.
STRICT_PREFIXES = (
    "decisions/judgment-records/",
    "models/",
    "figures/",
    "tests/",
    "src/",
    "scripts/",
    ".github/",
    "glossary/tests/",
)
STRICT_FILES = ("uv.lock", "pyproject.toml", "package.json", "package-lock.json")
NEW_OK_PREFIXES = ("decisions/", "docs/superpowers/")

# Protected tokens, case-sensitive. Each regex captures the whole identifier, and rule (c) compares the
# matched strings, so changing an issue number or an API name is a change. `opensysml.` is the API-call
# token, so the domain opensysml.org (linked from the new stack definition) is not one; rule (g)
# covers it.
PROTECTED_TOKENS: dict[str, re.Pattern[str]] = {
    "import opensysml": re.compile(r"\bimport opensysml\b"),
    "opensysml.<name>": re.compile(r"\bopensysml\.(?!org\b)\w+(?:\.\w+)*"),
    "OPENSYSML_VERSION": re.compile(r"\bOPENSYSML_VERSION\b"),
    "OPENSYSML_GRPC_VERSION": re.compile(r"\bOPENSYSML_GRPC_VERSION\b"),
    "~/.opensysml": re.compile(r"~/\.opensysml\b"),
    "Open-MBEE/OpenSysML": re.compile(r"\bOpen-MBEE/OpenSysML\b"),
    "Open-MBEE/sysml-toolkit": re.compile(r"\bOpen-MBEE/sysml-toolkit\b"),
    "OpenSysML#NNN": re.compile(r"\bOpenSysML#\w+"),
    "sysml-toolkit#N": re.compile(r"\bsysml-toolkit#\w+"),
    "toaster#N": re.compile(r"\btoaster#\w+"),
    "opensysml-api": re.compile(r"\bopensysml-api\b"),
    "opensysml-query": re.compile(r"\bopensysml-query\b"),
}
# In notebooks these are read over all cells (they appear as markdown link text); the rest over code cells.
ISSUE_TOKENS = frozenset({"OpenSysML#NNN", "sysml-toolkit#N", "toaster#N"})

URL_RE = re.compile(r"https?://[^\s<>\"'`\\)\]}]+")
URL_TRAILING = ".,;:!?"
DEFERRED_HEADING_RE = re.compile(r"^## D-\d+.*$", re.MULTILINE)
FENCE_OPEN_RE = re.compile(r"^\s*(`{3,}|~{3,})")

SKILLS_DIR = ".claude/skills/"
APPEND_ONLY_FILE = "decisions/log.md"


class GitError(RuntimeError):
    pass


def _git(repo: Path, *args: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, check=False
    )
    if proc.returncode != 0:
        raise GitError(proc.stderr.decode("utf-8", "replace").strip() or "git failed")
    return proc.stdout


class Tree:
    """Read access to the files of one side of the comparison."""

    def __init__(self, repo: Path, rev: str | None) -> None:
        self.repo = repo
        self.rev = rev  # None means the working tree
        self._files: list[str] | None = None

    def read(self, path: str) -> bytes | None:
        if self.rev is None:
            target = self.repo / path
            return target.read_bytes() if target.is_file() else None
        try:
            return _git(self.repo, "show", f"{self.rev}:{path}")
        except GitError:
            return None

    def text(self, path: str) -> str | None:
        raw = self.read(path)
        return None if raw is None else raw.decode("utf-8", "replace")

    def files(self) -> list[str]:
        if self._files is None:
            if self.rev is None:
                out = _git(
                    self.repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard"
                )
                names = [n for n in out.decode("utf-8", "replace").split("\0") if n]
                self._files = sorted(n for n in set(names) if (self.repo / n).is_file())
            else:
                out = _git(self.repo, "ls-tree", "-r", "-z", "--name-only", self.rev)
                self._files = sorted(
                    n for n in out.decode("utf-8", "replace").split("\0") if n
                )
        return self._files


def changed_files(repo: Path, base: str, head: str | None) -> list[tuple[str, str]]:
    """(status, path) for each changed file; status is A, M or D. Renames count as D plus A."""
    args = ["diff", "--name-status", "--no-renames", "-z", base]
    if head is not None:
        args.append(head)
    parts = _git(repo, *args).decode("utf-8", "replace").split("\0")
    pairs = [
        (parts[i][:1], parts[i + 1]) for i in range(0, len(parts) - 1, 2) if parts[i]
    ]
    if head is None:
        out = _git(repo, "ls-files", "-z", "--others", "--exclude-standard")
        pairs += [("A", n) for n in out.decode("utf-8", "replace").split("\0") if n]
    return sorted(set(pairs), key=lambda p: (p[1], p[0]))


def zone_of(path: str) -> str | None:
    """'strict', 'new_ok' or None (outside the protected zones)."""
    if path in OWN_FILES:
        return None
    if path in STRICT_FILES or path.startswith(STRICT_PREFIXES):
        return "strict"
    if path.startswith("glossary/") and path.endswith(".py") and "/" not in path[len("glossary/"):]:
        return "strict"
    if path.startswith(NEW_OK_PREFIXES):
        return "new_ok"
    return None


def in_zone(path: str) -> bool:
    return zone_of(path) is not None or path in OWN_FILES


# ---------------------------------------------------------------------------------------------
# notebook helpers


def load_notebook(raw: bytes | None) -> dict | None:
    if raw is None:
        return None
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) and isinstance(data.get("cells"), list) else None


def _source_text(cell: dict) -> str:
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else str(src)


def notebook_code_text(nb: dict) -> str:
    return "\n".join(
        _source_text(c) for c in nb["cells"] if c.get("cell_type") == "code"
    )


def notebook_all_text(nb: dict) -> str:
    chunks: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, str):
            chunks.append(node)
        elif isinstance(node, list):
            if node and all(isinstance(x, str) for x in node):
                chunks.append("".join(node))
            else:
                for item in node:
                    walk(item)
        elif isinstance(node, dict):
            for value in node.values():
                walk(value)

    walk(nb)
    return "\n".join(chunks)


# ---------------------------------------------------------------------------------------------
# rules; each returns a list of violation strings "path: reason"


def is_append_only(old: str | None, new: str | None) -> bool:
    """True if every base line is kept, in order and unchanged, with lines only added at the end."""
    if old is None or new is None:
        return False
    old_lines, new_lines = old.splitlines(), new.splitlines()
    return new_lines[: len(old_lines)] == old_lines


def a_violation(status: str, path: str, base: Tree, head: Tree) -> str | None:
    """The rule (a) violation for one changed path, or None."""
    if path == APPEND_ONLY_FILE and status == "M":
        if not is_append_only(base.text(path), head.text(path)):
            return f"{path}: existing lines changed, deleted or inserted; append-only file"
        return None
    zone = zone_of(path)
    if zone == "strict":
        return f"{path}: protected zone changed ({status})"
    if zone == "new_ok" and status != "A":
        return f"{path}: protected zone changed ({status}); only new files are allowed"
    return None


def first_matching_glob(path: str, allow: Sequence[str]) -> str | None:
    return next((g for g in allow if fnmatch.fnmatchcase(path, g)), None)


def rule_a(
    changes: list[tuple[str, str]], base: Tree, head: Tree, allow: Sequence[str] = ()
) -> tuple[list[str], list[str]]:
    """(violations, info lines). Each violation waived by --allow is listed as an info line."""
    out, info = [], []
    for status, path in changes:
        violation = a_violation(status, path, base, head)
        if violation is None:
            continue
        glob = first_matching_glob(path, allow)
        if glob is None:
            out.append(violation)
        else:
            info.append(f"exempted by --allow '{glob}': {path} ({status})")
    return out, info


def rule_b(changes: list[tuple[str, str]], base: Tree, head: Tree) -> list[str]:
    out = []
    for status, path in changes:
        if not path.endswith(".ipynb") or status == "A":
            continue
        old = load_notebook(base.read(path))
        if status == "D":
            out.append(f"{path}: notebook deleted")
            continue
        new = load_notebook(head.read(path))
        if old is None or new is None:
            out.append(f"{path}: notebook is not readable JSON with a cells list")
            continue
        for key in sorted((set(old) | set(new)) - {"cells"}):
            if old.get(key) != new.get(key):
                out.append(f"{path}: notebook field '{key}' changed")
        if len(old["cells"]) != len(new["cells"]):
            out.append(
                f"{path}: cell count changed ({len(old['cells'])} -> {len(new['cells'])})"
            )
            continue
        for i, (oc, nc) in enumerate(zip(old["cells"], new["cells"])):
            if oc.get("cell_type") != nc.get("cell_type"):
                out.append(
                    f"{path}: cell {i} type changed ({oc.get('cell_type')} -> {nc.get('cell_type')})"
                )
                continue
            kind = oc.get("cell_type")
            ignore = {"source"} if kind == "markdown" else set()
            differing = sorted(
                k
                for k in (set(oc) | set(nc)) - ignore
                if oc.get(k) != nc.get(k)
            )
            if differing:
                out.append(f"{path}: {kind} cell {i} changed field(s) {', '.join(differing)}")
    return out


def notebook_sources_text(nb: dict) -> str:
    return "\n".join(_source_text(c) for c in nb["cells"])


def token_matches(path: str, raw: bytes | None) -> Counter[str]:
    """Multiset of matched protected-token strings in one file."""
    found: Counter[str] = Counter()
    if raw is None:
        return found
    text = code_text = raw.decode("utf-8", "replace")
    if path.endswith(".ipynb"):
        nb = load_notebook(raw)
        if nb is not None:
            text, code_text = notebook_sources_text(nb), notebook_code_text(nb)
    for name, rx in PROTECTED_TOKENS.items():
        source = text if name in ISSUE_TOKENS or not path.endswith(".ipynb") else code_text
        found.update(m.group(0) for m in rx.finditer(source))
    return found


def rule_c(
    changes: list[tuple[str, str]], base: Tree, head: Tree
) -> tuple[list[str], list[str]]:
    """(violations, info lines). Base tokens must all survive at head; additions are informational."""
    out, info = [], []
    for _status, path in changes:
        if in_zone(path):
            continue  # rule (a) governs these paths
        old = token_matches(path, base.read(path))
        new = token_matches(path, head.read(path))
        for token in sorted(old):
            if new[token] < old[token]:
                out.append(
                    f"{path}: token '{token}' removed or altered (count {old[token]} -> {new[token]})"
                )
        for token in sorted(new):
            if new[token] > old[token]:
                info.append(f"{path}: token '{token}' added (count {old[token]} -> {new[token]})")
    return out, info


def deferred_headings(text: str | None) -> list[str]:
    return DEFERRED_HEADING_RE.findall(text or "")


def rule_d(changes: list[tuple[str, str]], base: Tree, head: Tree) -> list[str]:
    if not any(path == "DEFERRED.md" for _s, path in changes):
        return []
    old = deferred_headings(base.text("DEFERRED.md"))
    new = deferred_headings(head.text("DEFERRED.md"))
    if old == new:
        return []
    out = []
    for line in old:
        if line not in new:
            out.append(f"DEFERRED.md: heading changed or removed: {line}")
    for line in new:
        if line not in old:
            out.append(f"DEFERRED.md: heading added or changed: {line}")
    if not out:
        out.append("DEFERRED.md: heading order or multiplicity changed")
    return out


def fenced_blocks(text: str | None) -> list[str]:
    """Fenced code blocks (fence lines included), in order. An unclosed fence runs to the end."""
    blocks: list[list[str]] = []
    current: list[str] | None = None
    fence = ""
    for line in (text or "").splitlines():
        if current is None:
            m = FENCE_OPEN_RE.match(line)
            if m:
                fence = m.group(1)
                current = [line]
        else:
            current.append(line)
            stripped = line.strip()
            if (
                stripped
                and set(stripped) == {fence[0]}
                and len(stripped) >= len(fence)
            ):
                blocks.append(current)
                current = None
    if current is not None:
        blocks.append(current)
    return ["\n".join(b) for b in blocks]


def rule_e(changes: list[tuple[str, str]], base: Tree, head: Tree) -> list[str]:
    out = []
    for status, path in changes:
        if not path.startswith(SKILLS_DIR):
            continue
        if not path.endswith(".md"):
            out.append(f"{path}: non-markdown skill file changed ({status})")
            continue
        old = fenced_blocks(base.text(path))
        new = fenced_blocks(head.text(path))
        if old != new:
            out.append(f"{path}: fenced code blocks changed ({len(old)} -> {len(new)} blocks)")
    return out


def skill_dirs(tree: Tree) -> set[str]:
    dirs = set()
    for name in tree.files():
        if name.startswith(SKILLS_DIR):
            parts = name[len(SKILLS_DIR):].split("/")
            if len(parts) >= 2:
                dirs.add(parts[0])
    return dirs


def skill_name(text: str | None) -> str | None:
    if not text:
        return None
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            return None
        m = re.match(r"name:\s*(.*?)\s*$", line)
        if m:
            return m.group(1).strip("'\"")
    return None


def rule_f(base: Tree, head: Tree) -> list[str]:
    out = []
    old_dirs, new_dirs = skill_dirs(base), skill_dirs(head)
    for d in sorted(old_dirs - new_dirs):
        out.append(f"{SKILLS_DIR}{d}: skill directory removed or renamed")
    for d in sorted(new_dirs - old_dirs):
        out.append(f"{SKILLS_DIR}{d}: skill directory added")
    for d in sorted(old_dirs & new_dirs):
        path = f"{SKILLS_DIR}{d}/SKILL.md"
        old, new = skill_name(base.text(path)), skill_name(head.text(path))
        if old != new:
            out.append(f"{path}: frontmatter name changed ({old!r} -> {new!r})")
    return out


def urls_in(path: str, raw: bytes | None) -> Counter[str]:
    """Occurrence count of each URL in one file."""
    if raw is None:
        return Counter()
    if path.endswith(".ipynb"):
        nb = load_notebook(raw)
        text = notebook_all_text(nb) if nb is not None else raw.decode("utf-8", "replace")
    else:
        text = raw.decode("utf-8", "replace")
    return Counter(u.rstrip(URL_TRAILING) for u in URL_RE.findall(text))


def rule_g(changes: list[tuple[str, str]], base: Tree, head: Tree) -> list[str]:
    out = []
    for status, path in changes:
        if status == "A" or in_zone(path):
            continue
        old, new = urls_in(path, base.read(path)), urls_in(path, head.read(path))
        for url in sorted(old):
            if new[url] < old[url]:
                out.append(f"{path}: URL count decreased ({old[url]} -> {new[url]}): {url}")
    return out


# ---------------------------------------------------------------------------------------------


def repo_root(path: Path) -> Path:
    """The repository root containing `path` (any directory inside the work tree)."""
    return Path(_git(path, "rev-parse", "--show-toplevel").decode("utf-8", "replace").strip())


def run_rules(
    repo: Path, base_rev: str, head_rev: str | None, allow: Sequence[str] = ()
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Run every rule; returns ({rule letter: violation lines}, {rule letter: info lines})."""
    repo = repo_root(repo)
    base, head = Tree(repo, base_rev), Tree(repo, head_rev)
    changes = changed_files(repo, base_rev, head_rev)
    a_violations, a_info = rule_a(changes, base, head, allow)
    c_violations, c_info = rule_c(changes, base, head)
    results = {
        "a": a_violations,
        "b": rule_b(changes, base, head),
        "c": c_violations,
        "d": rule_d(changes, base, head),
        "e": rule_e(changes, base, head),
        "f": rule_f(base, head),
        "g": rule_g(changes, base, head),
    }
    return results, {"a": a_info, "c": c_info}


def check(
    repo: Path, base_rev: str, head_rev: str | None, allow: Sequence[str] = ()
) -> dict[str, list[str]]:
    """Run every rule; maps rule letter to its violation lines (empty list means PASS)."""
    return run_rules(repo, base_rev, head_rev, allow)[0]


def render(
    results: dict[str, list[str]],
    info: dict[str, list[str]] | None = None,
    allow: Sequence[str] = (),
) -> str:
    info = info or {}
    lines = [f"allow: {', '.join(allow)}"] if allow else []
    for letter, desc in RULES.items():
        found = results[letter]
        if found:
            lines.append(f"FAIL ({letter}) {desc}: {len(found)} violation(s)")
            lines += [f"  ({letter}) {v}" for v in found]
        else:
            lines.append(f"PASS ({letter}) {desc}")
        lines += [f"  info ({letter}) {i}" for i in info.get(letter, [])]
    waived = len(info.get("a", []))
    suffix = f" (with {waived} --allow exemption(s))" if waived else ""
    lines.append("RESULT: " + ("FAIL" if any(results.values()) else "PASS") + suffix)
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        epilog="SELF: reviewers must run this checker from a pinned revision (the branch named "
        "'terminology' after the guard merges), not from the branch under review.",
    )
    parser.add_argument("--base", required=True, help="revision to compare against")
    parser.add_argument("--head", default=None, help="revision to check (default: working tree)")
    parser.add_argument(
        "--repo", default=".", help="a directory inside the repository (default: current)"
    )
    parser.add_argument(
        "--allow",
        action="append",
        default=[],
        metavar="GLOB",
        help="exempt paths matching GLOB (relative to the repository root; '*' matches across '/') "
        "from rule (a) for this run only; repeatable, e.g. --allow 'glossary/tests/*'",
    )
    args = parser.parse_args(argv)
    repo = Path(args.repo)
    try:
        repo = repo_root(repo)
        for rev in (args.base, args.head):
            if rev is not None:
                try:
                    _git(repo, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
                except GitError:
                    raise GitError(f"unknown revision: {rev}") from None
        results, info = run_rules(repo, args.base, args.head, args.allow)
    except (GitError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(render(results, info, args.allow))
    return 1 if any(results.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
