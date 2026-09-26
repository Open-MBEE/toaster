from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from glossary import lint
from glossary.cli import app

runner = CliRunner()


def nb(*cells: tuple[str, str], outputs: str = "") -> str:
    return json.dumps({"cells": [
        {"cell_type": t, "source": s.splitlines(keepends=True), "outputs": ([{"text": outputs}] if outputs else [])}
        for t, s in cells], "metadata": {}, "nbformat": 4, "nbformat_minor": 5})


def make_repo(tmp: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        p = tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return tmp


def hits_for(tmp: Path, text: str, rel: str = "docs/x.md") -> list[lint.Hit]:
    make_repo(tmp, {rel: text})
    return lint.scan(tmp, lint.load_rules())


def ids(hs: list[lint.Hit]) -> list[str]:
    return [h.rule for h in hs]


# (rule id, text that must hit, text that must not)
CASES = [
    ("tall-named", "See Tall's three worlds for this.", "Install the tall shelf; a tall seam of coal."),
    ("tall-named", "the Tall seam is the join", "Tallis is a surname; so is Metall; installation."),
    ("tall-named", "Tall is named alone", "Metall and Tallis"),
    ("tall-named", "the Three Worlds lens", "three or more worlds"),
    ("tall-named", "as in Tall (2020), the lens", "install (2020) and tall (2020) are not names"),
    ("concept-selection", "This is Concept Selection.", "concept and selection are separate; selection among alternatives"),
    ("concept-selection", "concept selection here", "concept selections and concept selectional"),
    ("sub-behavior", "each sub-behavior runs", "the behavior of the subsystem"),
    ("sub-behavior", "the sub-behaviors run", "the sub-behaviorial thing"),
    ("sub-behavior", "each Sub-Behaviour runs", "a sub behavior is not the hyphenated word"),
    ("stale-physical-layer", "the physical architecture layer", "the physical layer of the network architecture"),
    ("stale-physical-layer", "the physical architecture layers", "the physical layer of the network architecture"),
    ("stale-partition", "partitioned into implementation-agnostic parts", "partitioned into three layers"),
    ("stale-partition", "partitioned into implementation-agnostic parts", "The structure is implementation-agnostic."),
    ("stale-partition", "was partitioned into implementation-agnostic", "departitioned into implementation-agnostic"),
    ("accepted-disposition", "The disposition is accepted here.", "The reviewer accepted the invoice; a disposition is recorded."),
    ("accepted-disposition", "an accepted disposition", "accepted practice, and a disposition. One two three four five six accepted"),
]


@pytest.mark.parametrize(("rule", "hit", "miss"), CASES)
def test_rule_hits_and_near_misses(tmp_path: Path, rule: str, hit: str, miss: str) -> None:
    assert rule in ids(hits_for(tmp_path, hit))
    make_repo(tmp_path, {"docs/x.md": miss})
    assert rule not in ids(lint.scan(tmp_path, lint.load_rules()))


def test_severities_from_rules_file() -> None:
    sev = {r.id: r.severity for r in lint.load_rules()}
    assert sev["accepted-disposition"] == "warn"
    assert all(v == "error" for k, v in sev.items() if k != "accepted-disposition")


def test_hit_fields_md_and_notebook(tmp_path: Path) -> None:
    make_repo(tmp_path, {
        "chapters/ch/index.md": "line one\nuse sub-behavior here\n",
        "chapters/ch/a.ipynb": nb(("markdown", "intro"), ("code", "x = 'sub-behavior'"), ("markdown", "a\nb\nconcept selection")),
    })
    hs = {(h.file, h.cell, h.line, h.rule, h.text) for h in lint.scan(tmp_path, lint.load_rules())}
    assert hs == {("chapters/ch/index.md", None, 2, "sub-behavior", "sub-behavior"),
                  ("chapters/ch/a.ipynb", 2, 3, "concept-selection", "concept selection")}


def test_notebook_code_cells_and_outputs_ignored(tmp_path: Path) -> None:
    make_repo(tmp_path, {"chapters/ch/a.ipynb": nb(("code", "# sub-behavior\nx = 1"), ("markdown", "clean"), outputs="concept selection")})
    assert lint.scan(tmp_path, lint.load_rules()) == []


def test_scope_exclusions(tmp_path: Path) -> None:
    bad = "sub-behavior and concept selection\n"
    make_repo(tmp_path, {p: bad for p in (
        "AGENTS.md", "CLAUDE.md", "README.md", ".claude/skills/s/SKILL.md", "decisions/log.md", "glossary/README.md",
        "docs/glossary.md", "other/notes.md", "chapters/ch/notes.txt")})
    make_repo(tmp_path, {"chapters/ch/.ipynb_checkpoints/a-checkpoint.ipynb": nb(("markdown", bad))})
    assert lint.scan(tmp_path, lint.load_rules()) == []
    make_repo(tmp_path, {"docs/other.md": bad, "chapters/ch/deep/x.md": bad})
    assert {h.file for h in lint.scan(tmp_path, lint.load_rules())} == {"docs/other.md", "chapters/ch/deep/x.md"}


def test_cli_text_and_json_output_and_exit(tmp_path: Path) -> None:
    make_repo(tmp_path, {"docs/a.md": "sub-behavior\nThe disposition is accepted\n"})
    r = runner.invoke(app, ["lint", "--repo", str(tmp_path)])
    assert r.exit_code == 1
    assert "docs/a.md line 1: sub-behavior [error] 'sub-behavior'" in r.output
    assert "  sub-behavior  1" in r.output and "  accepted-disposition  1" in r.output and "  tall-named  0" in r.output
    assert "total 2 (1 error, 1 warn)" in r.output
    j = json.loads(runner.invoke(app, ["lint", "--json", "--repo", str(tmp_path)]).output)
    assert j["summary"]["per_rule"]["sub-behavior"] == 1 and len(j["hits"]) == 2
    assert {"file", "cell", "line", "rule", "text", "severity", "status"} <= set(j["hits"][0])
    assert all(h["status"] is None for h in j["hits"])


def test_warn_only_exits_zero_and_clean_exits_zero(tmp_path: Path) -> None:
    make_repo(tmp_path, {"docs/a.md": "The disposition is accepted\n"})
    assert runner.invoke(app, ["lint", "--repo", str(tmp_path)]).exit_code == 0
    make_repo(tmp_path, {"docs/a.md": "fine\n"})
    assert runner.invoke(app, ["lint", "--repo", str(tmp_path)]).exit_code == 0


def test_baseline_classification_and_exit_codes(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    base = tmp_path / "base.json"
    make_repo(repo, {"docs/a.md": "sub-behavior\n"})
    assert runner.invoke(app, ["lint", "--repo", str(repo), "--write-baseline", str(base)]).exit_code == 1
    assert json.loads(base.read_text())[0]["rule"] == "sub-behavior"
    r = runner.invoke(app, ["lint", "--repo", str(repo), "--baseline", str(base)])
    assert r.exit_code == 0 and "(baselined)" in r.output
    # line numbers do not matter
    make_repo(repo, {"docs/a.md": "\n\n\nsub-behavior\n"})
    assert runner.invoke(app, ["lint", "--repo", str(repo), "--baseline", str(base)]).exit_code == 0
    # a different matched text, another file, or another rule is new
    make_repo(repo, {"docs/a.md": "sub-behaviour\n"})
    r = runner.invoke(app, ["lint", "--repo", str(repo), "--baseline", str(base)])
    assert r.exit_code == 1 and "(new)" in r.output
    make_repo(repo, {"docs/a.md": "sub-behavior\n", "docs/b.md": "sub-behavior\n"})
    assert runner.invoke(app, ["lint", "--repo", str(repo), "--baseline", str(base)]).exit_code == 1
    make_repo(repo, {"docs/b.md": "fine\n"})
    j = json.loads(runner.invoke(app, ["lint", "--json", "--repo", str(repo), "--baseline", str(base)]).output)
    assert j["hits"][0]["status"] == "baselined" and j["summary"]["baselined"] == 1


def test_notebook_string_source_is_scanned(tmp_path: Path) -> None:
    doc = {"cells": [{"cell_type": "markdown", "source": "a\nuse sub-behavior here"}, {"cell_type": "code", "source": "sub-behavior"}]}
    make_repo(tmp_path, {"chapters/ch/a.ipynb": json.dumps(doc)})
    hs = lint.scan(tmp_path, lint.load_rules())
    assert [(h.cell, h.line, h.rule) for h in hs] == [(0, 2, "sub-behavior")]


def test_rule_id_is_part_of_baseline_key(tmp_path: Path) -> None:
    hit = lint.Hit("docs/a.md", None, 1, "rule-a", "foo", "error")
    other = lint.Hit("docs/a.md", None, 1, "rule-b", "foo", "error")
    base = tmp_path / "b.json"
    lint.write_baseline(base, [hit])
    cl = lint.classify([other, hit], lint.read_baseline(base))
    assert [s for _, s in cl] == ["new", "baselined"]


def test_baseline_is_count_based(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    base = tmp_path / "base.json"
    make_repo(repo, {"docs/a.md": "sub-behavior\n"})
    runner.invoke(app, ["lint", "--repo", str(repo), "--write-baseline", str(base)])
    make_repo(repo, {"docs/a.md": "sub-behavior\nsub-behavior\n"})
    r = runner.invoke(app, ["lint", "--repo", str(repo), "--baseline", str(base)])
    assert r.exit_code == 1 and "(new)" in r.output and "(baselined)" in r.output
    # baseline of two: two are fine, one is fine, zero is fine, three is new
    runner.invoke(app, ["lint", "--repo", str(repo), "--write-baseline", str(base)])
    assert runner.invoke(app, ["lint", "--repo", str(repo), "--baseline", str(base)]).exit_code == 0
    make_repo(repo, {"docs/a.md": "sub-behavior\n"})
    assert runner.invoke(app, ["lint", "--repo", str(repo), "--baseline", str(base)]).exit_code == 0
    make_repo(repo, {"docs/a.md": "clean\n"})
    assert runner.invoke(app, ["lint", "--repo", str(repo), "--baseline", str(base)]).exit_code == 0
    make_repo(repo, {"docs/a.md": "sub-behavior\n" * 3})
    assert runner.invoke(app, ["lint", "--repo", str(repo), "--baseline", str(base)]).exit_code == 1


def test_json_status_null_without_baseline_and_write_to_missing_dir(tmp_path: Path) -> None:
    make_repo(tmp_path / "r", {"docs/a.md": "sub-behavior\n"})
    r = runner.invoke(app, ["lint", "--repo", str(tmp_path / "r"), "--write-baseline", str(tmp_path / "nodir" / "b.json")])
    assert r.exit_code == 2 and "cannot write baseline" in r.output and "Traceback" not in r.output


def test_new_warning_does_not_fail_baseline_run(tmp_path: Path) -> None:
    base = tmp_path / "b.json"
    base.write_text("[]")
    make_repo(tmp_path / "r", {"docs/a.md": "an accepted disposition\n"})
    assert runner.invoke(app, ["lint", "--repo", str(tmp_path / "r"), "--baseline", str(base)]).exit_code == 0


def test_bad_baseline_is_exit_2(tmp_path: Path) -> None:
    base = tmp_path / "b.json"
    base.write_text("not json")
    assert runner.invoke(app, ["lint", "--repo", str(tmp_path), "--baseline", str(base)]).exit_code == 2
    assert runner.invoke(app, ["lint", "--repo", str(tmp_path), "--baseline", str(tmp_path / "missing.json")]).exit_code == 2


GOOD = {"id": "r", "regex": "foo", "message": "m", "why": "w", "severity": "error", "scope": "learner"}


def rules_file(tmp: Path, **over: str) -> Path:
    r = {**GOOD, **over}
    body = "\n".join(f"{k} = '''{v}'''" for k, v in r.items() if v is not None)
    p = tmp / "rules.toml"
    p.write_text("[[rule]]\n" + body + "\n")
    return p


@pytest.mark.parametrize(("over", "needle"), [
    ({"why": None}, "missing field 'why'"),
    ({"regex": None}, "missing field 'regex'"),
    ({"severity": "fatal"}, "unknown severity 'fatal'"),
    ({"scope": "everywhere"}, "unknown scope 'everywhere'"),
    ({"regex": "(unclosed"}, "does not compile"),
])
def test_rules_file_validation(tmp_path: Path, over: dict, needle: str) -> None:
    p = rules_file(tmp_path, **over)
    r = runner.invoke(app, ["lint", "--repo", str(tmp_path), "--rules", str(p)])
    assert r.exit_code == 2
    assert "rule 'r'" in r.output and needle in r.output


def test_valid_custom_rules_file_and_case_insensitive(tmp_path: Path) -> None:
    make_repo(tmp_path, {"docs/a.md": "a FOO here\n"})
    r = runner.invoke(app, ["lint", "--repo", str(tmp_path), "--rules", str(rules_file(tmp_path))])
    assert r.exit_code == 1 and "'FOO'" in r.output


@pytest.mark.parametrize(("body", "needle"), [
    ("[[rule]]\nid='r'\nregex=5\nmessage='m'\nwhy='w'\nseverity='error'\nscope='learner'\n", "field 'regex' must be a string"),
    ("[[rule]]\nid='r'\nregex='x'\nmessage=1\nwhy='w'\nseverity='error'\nscope='learner'\n", "field 'message' must be a string"),
    ("[[rule]]\nid=3\nregex='x'\nmessage='m'\nwhy='w'\nseverity='error'\nscope='learner'\n", "field 'id' must be a string"),
    ("rule = 5\n", "list of [[rule]] tables"),
    ("rule = [1, 2]\n", "list of [[rule]] tables"),
    ("", "no rules loaded"),
    ("[[rules]]\nid='r'\n", "unknown top-level key"),
    ("[[rule]]\nid='r'\nregex='x'\nmessage='m'\nwhy='w'\nseverity='error'\nscope='learner'\n" * 2, "duplicate rule id"),
    ("[[rule]]\nid='r'\nregex=''\nmessage='m'\nwhy='w'\nseverity='error'\nscope='learner'\n", "regex must not be empty"),
])
def test_rules_file_structural_errors(tmp_path: Path, body: str, needle: str) -> None:
    p = tmp_path / "rules.toml"
    p.write_text(body)
    r = runner.invoke(app, ["lint", "--repo", str(tmp_path), "--rules", str(p)])
    assert r.exit_code == 2 and needle in r.output and "Traceback" not in r.output
