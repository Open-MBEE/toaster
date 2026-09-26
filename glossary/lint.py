"""Lint learner-facing content against rules kept in data (lint_rules.toml).

Scope: markdown cells of chapters/**/*.ipynb, chapters/**/*.md and docs/**/*.md,
except docs/glossary.md (generated). Nothing else is scanned.
"""

from __future__ import annotations

import json
import re
import tomllib
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from .namespaces import PACKAGE_DIR

RULES_FILE = PACKAGE_DIR / "lint_rules.toml"
FIELDS = ("id", "regex", "message", "why", "severity", "scope")
SEVERITIES = ("error", "warn")
SCOPES = ("learner",)
EXCLUDED = ("docs/glossary.md",)


class LintConfigError(Exception):
    """The rules file or a baseline file is unusable (exit code 2)."""


@dataclass(frozen=True)
class Rule:
    id: str
    pattern: re.Pattern[str]
    message: str
    why: str
    severity: str
    scope: str


@dataclass(frozen=True)
class Hit:
    file: str
    cell: int | None
    line: int
    rule: str
    text: str
    severity: str


def load_rules(path: Path = RULES_FILE) -> list[Rule]:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as e:
        raise LintConfigError(f"cannot read rules file {path}: {e}") from e
    unknown = sorted(set(data) - {"rule"})
    if unknown:
        raise LintConfigError(f"unknown top-level key(s) {unknown} in {path} (only [[rule]] tables are allowed)")
    raw_rules = data.get("rule", [])
    if not isinstance(raw_rules, list) or not all(isinstance(r, dict) for r in raw_rules):
        raise LintConfigError(f"'rule' in {path} must be a list of [[rule]] tables")
    if not raw_rules:
        raise LintConfigError(f"no rules loaded from {path}; refusing to lint with zero rules")
    rules = []
    seen: set[str] = set()
    for i, raw in enumerate(raw_rules):
        name = raw.get("id") if isinstance(raw.get("id"), str) and raw.get("id") else f"#{i + 1}"
        for f in FIELDS:
            if f not in raw:
                raise LintConfigError(f"rule {name!r}: missing field {f!r}")
            if not isinstance(raw[f], str):
                raise LintConfigError(f"rule {name!r}: field {f!r} must be a string, got {type(raw[f]).__name__}")
        if not raw["id"]:
            raise LintConfigError(f"rule {name!r}: id must not be empty")
        if raw["id"] in seen:
            raise LintConfigError(f"rule {name!r}: duplicate rule id")
        seen.add(raw["id"])
        if not raw["regex"]:
            raise LintConfigError(f"rule {name!r}: regex must not be empty")
        if raw["severity"] not in SEVERITIES:
            raise LintConfigError(f"rule {name!r}: unknown severity {raw['severity']!r} (expected one of {SEVERITIES})")
        if raw["scope"] not in SCOPES:
            raise LintConfigError(f"rule {name!r}: unknown scope {raw['scope']!r} (expected one of {SCOPES})")
        try:
            pattern = re.compile(raw["regex"], re.IGNORECASE)
        except re.error as e:
            raise LintConfigError(f"rule {name!r}: regex does not compile: {e}") from e
        rules.append(Rule(raw["id"], pattern, raw["message"], raw["why"], raw["severity"], raw["scope"]))
    return rules


def _units(repo: Path):
    """Yield (relative path, cell index or None, text) for each learner-facing unit."""
    files = [p for pat in ("chapters/**/*.ipynb", "chapters/**/*.md", "docs/**/*.md") for p in repo.glob(pat)]
    for p in sorted(set(files)):
        rel = p.relative_to(repo).as_posix()
        if rel in EXCLUDED or ".ipynb_checkpoints" in p.parts:
            continue
        try:
            if p.suffix == ".ipynb":
                nb = json.loads(p.read_text(encoding="utf-8"))
                for i, cell in enumerate(nb.get("cells", [])):
                    if cell.get("cell_type") == "markdown":
                        src = cell.get("source", "")
                        yield rel, i, "".join(src) if isinstance(src, list) else src
            else:
                yield rel, None, p.read_text(encoding="utf-8")
        except (OSError, ValueError) as e:
            raise LintConfigError(f"cannot read {rel}: {e}") from e


def scan(repo: Path, rules: list[Rule]) -> list[Hit]:
    hits = []
    for rel, cell, text in _units(repo):
        for r in rules:
            for m in r.pattern.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                hits.append(Hit(rel, cell, line, r.id, m.group(0), r.severity))
    return hits


def _key(h: Hit | dict) -> tuple[str, str, str]:
    d = asdict(h) if isinstance(h, Hit) else h
    return d["file"], d["rule"], d["text"]


def write_baseline(path: Path, hits: list[Hit]) -> None:
    try:
        path.write_text(json.dumps([asdict(h) for h in hits], indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    except OSError as e:
        raise LintConfigError(f"cannot write baseline {path}: {e}") from e


def read_baseline(path: Path) -> Counter[tuple[str, str, str]]:
    """Baseline as a multiset of (file, rule, text) keys: duplicates count."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return Counter(_key(d) for d in data)
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise LintConfigError(f"cannot read baseline {path}: {e}") from e


def classify(hits: list[Hit], baseline: Counter[tuple[str, str, str]] | None) -> list[tuple[Hit, str | None]]:
    """A key is baselined only up to the number of times it appears in the baseline; further identical hits are new."""
    if baseline is None:
        return [(h, None) for h in hits]
    remaining = Counter(baseline)
    out: list[tuple[Hit, str | None]] = []
    for h in hits:
        k = _key(h)
        if remaining[k] > 0:
            remaining[k] -= 1
            out.append((h, "baselined"))
        else:
            out.append((h, "new"))
    return out


def exit_code(classified: list[tuple[Hit, str | None]]) -> int:
    return 1 if any(h.severity == "error" and status != "baselined" for h, status in classified) else 0


def summary(classified: list[tuple[Hit, str | None]], rules: list[Rule]) -> dict:
    per_rule = Counter(h.rule for h, _ in classified)
    return {
        "per_rule": {r.id: per_rule.get(r.id, 0) for r in rules},
        "total": len(classified),
        "errors": sum(1 for h, _ in classified if h.severity == "error"),
        "warnings": sum(1 for h, _ in classified if h.severity == "warn"),
        "new": sum(1 for _, s in classified if s == "new"),
        "baselined": sum(1 for _, s in classified if s == "baselined"),
    }


def format_hit(h: Hit, status: str | None) -> str:
    where = h.file + (f" cell {h.cell}" if h.cell is not None else "") + f" line {h.line}"
    return f"{where}: {h.rule} [{h.severity}] {h.text!r}" + (f" ({status})" if status else "")
