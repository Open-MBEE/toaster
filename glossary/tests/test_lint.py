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
    ("tall-named", "the three-worlds lens", "a three world model"),
    ("tall-named", "the three worlds lens", "the threeworlds lens"),
    ("tall-named", "the Three  Worlds lens", "three-world and threeworlds"),
    ("tall-named", "the Tall lens", "xTall lens"),
    ("tall-named", "the three worlds lens", "rethree worlds lens"),
    ("tall-named", "the three worlds lens", "three worldsy lens"),
    ("tall-named", "the A-F construct", "a-f is not the abbreviation; neither is AF"),
    ("tall-named", "A-F, O-S, and E all appear", "the range a-f in lowercase does not count"),
    ("tall-named", "shows the O-S seam", "cross-section O S without a hyphen"),
    ("no-em-dash", "the model—loaded correctly", "the model, loaded correctly"),
    ("no-em-dash", "a fixed value—not a default", "a fixed value, not a default (a hyphen-only sentence)"),
    ("stale-physical-layer", "the physical architecture layers", "the physical architecture layersy"),
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
    # OT-7 guard rules: hit, and the sanctioned rewrite as the near miss
    ("opensysml-contrast-or-and", "OpenSysML or sysml-toolkit accepts it", "The OpenSysML runtime or sysml-toolkit accepts it"),
    ("opensysml-contrast-or-and", "OpenSysML and sysml-toolkit agree; also OpenSysML vs. sysml-toolkit", "the OpenSysML runtime and sysml-toolkit agree"),
    ("opensysml-contrast-or-and", "OpenSysML versus sysml-toolkit", "OpenSysML, the stack, includes sysml-toolkit"),
    ("opensysml-contrast-or-and", "neither OpenSysML nor sysml-toolkit; OpenSysML nor sysml-toolkit", "the OpenSysML runtime nor sysml-toolkit"),
    ("toolkit-and-opensysml", "sysml-toolkit or OpenSysML does it", "sysml-toolkit or the OpenSysML runtime does it"),
    ("toolkit-and-opensysml", "sysml-toolkit and OpenSysML agree", "sysml-toolkit and the OpenSysML runtime agree"),
    ("neither-opensysml", "Neither OpenSysML nor the pilot flags it", "Neither the OpenSysML runtime nor the pilot flags it"),
    ("not-opensysml", "this is not OpenSysML behavior", "this is not the OpenSysML runtime's behavior"),
    ("opensysml-capability", "OpenSysML cannot prove it", "the OpenSysML runtime cannot prove it"),
    ("opensysml-capability", "OpenSysML itself, OpenSysML alone, OpenSysML only, OpenSysML can't", "the OpenSysML runtime itself, alone, or only"),
    ("opensysml-capability", "OpenSysML does  not accept it; OpenSysML doesn't either", "the OpenSysML runtime does not accept it; sysml-toolkit doesn't"),
    ("opensysml-version", "OpenSysML v0.9.0 loads it", "the OpenSysML runtime accepts X; sysml-toolkit v0.9.1 rejects it"),
    ("opensysml-version", "OpenSysML v0.9.1", "OpenSysML runtime v0.9.0 and the stack OpenSysML v1"),
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


def test_baseline_key_includes_file(tmp_path: Path) -> None:
    base = tmp_path / "base.json"
    repo = tmp_path / "repo"
    # baseline is for the file scanned LAST, so a file-blind key would spend it on the wrong hit
    make_repo(repo, {"docs/b.md": "sub-behavior\n"})
    lint.write_baseline(base, lint.scan(repo, lint.load_rules()))
    make_repo(repo, {"docs/a.md": "sub-behavior\n"})
    cl = lint.classify(lint.scan(repo, lint.load_rules()), lint.read_baseline(base))
    assert {h.file: s for h, s in cl} == {"docs/a.md": "new", "docs/b.md": "baselined"}
    j = json.loads(runner.invoke(app, ["lint", "--json", "--repo", str(repo), "--baseline", str(base)]).output)
    assert {h["file"]: h["status"] for h in j["hits"]} == {"docs/a.md": "new", "docs/b.md": "baselined"}


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


def test_empty_rule_id_is_rejected(tmp_path: Path) -> None:
    r = runner.invoke(app, ["lint", "--repo", str(tmp_path), "--rules", str(rules_file(tmp_path, id=""))])
    assert r.exit_code == 2 and "id must not be empty" in r.output and "Traceback" not in r.output


def test_non_utf8_rules_file_is_exit_2(tmp_path: Path) -> None:
    p = tmp_path / "rules.toml"
    p.write_bytes(b"[[rule]]\nid='r'\nmessage='caf\xe9'\n")
    r = runner.invoke(app, ["lint", "--repo", str(tmp_path), "--rules", str(p)])
    assert r.exit_code == 2 and "rules.toml" in r.output and "Traceback" not in r.output


# --- ignore_code (OT-7) ---------------------------------------------------------------------

PLAIN = "plain-sub"
MASKED = "masked-sub"


def two_rule_file(tmp: Path) -> Path:
    base = "message = 'm'\nwhy = 'w'\nseverity = 'error'\nscope = 'learner'\n"
    p = tmp / "two.toml"
    p.write_text(
        f"[[rule]]\nid = '{PLAIN}'\nregex = 'foo'\n{base}\n"
        f"[[rule]]\nid = '{MASKED}'\nregex = 'foo'\nignore_code = true\n{base}")
    return p


def scan_two(tmp: Path, text: str, rel: str = "docs/x.md") -> list[lint.Hit]:
    make_repo(tmp, {rel: text})
    return lint.scan(tmp, lint.load_rules(two_rule_file(tmp)))


def test_ignore_code_skips_inline_span_for_masked_rule_only(tmp_path: Path) -> None:
    hs = scan_two(tmp_path, "see `foo` here\n")
    assert ids(hs) == [PLAIN]


@pytest.mark.parametrize("text", [
    "a ``foo`` b\n",
    "a ``x ` foo`` b\n",
    "a `foo\nbar` b\n",
    "```\nfoo\n```\n",
    "```python\nfoo\n```\n",
    "~~~\nfoo\n~~~\n",
    "   ```\nfoo\n   ```\n",
    "````\n```\nfoo\n```\n````\n",
    "```\nfoo\n",  # unclosed fence runs to the end
])
def test_ignore_code_masks_fences_and_spans(tmp_path: Path, text: str) -> None:
    assert ids(scan_two(tmp_path, text)) == [PLAIN]


@pytest.mark.parametrize("text", [
    "foo outside `code` foo\n",
    "a `foo\n\nbar` b\n",  # a span cannot cross a blank line
    "a `foo`` b\n",  # unequal backtick runs do not close
    "a `foo b\n",  # unclosed span is literal
    "~~~\ncode\n```\n~~~\nfoo\n",  # a ``` line does not close a ~~~ fence; the fence ended at ~~~
    "``` `\nfoo\n",  # backtick fence info string may not contain a backtick: not a fence
])
def test_ignore_code_does_not_over_mask(tmp_path: Path, text: str) -> None:
    got = ids(scan_two(tmp_path, text))
    assert MASKED in got


@pytest.mark.parametrize(("text", "visible"), [
    ("a `foo\r\n\r\nbar` b\r\n", "foo"),  # a span cannot cross a CRLF blank line
    ("a `x\r\n\r\nOpenSysML cannot` b\r\n", "OpenSysML cannot"),  # the probe: second paragraph stays visible
    ("a `x\r\n \t\r\nfoo` b\r\n", "foo"),  # whitespace-only CRLF blank line
])
def test_crlf_blank_line_stops_code_span(text: str, visible: str) -> None:
    masked = lint.mask_code(text)
    assert len(masked) == len(text) and visible in masked
    assert lint.mask_code(text.replace("\r\n", "\n")).count(visible) == 1  # same answer as LF


def test_crlf_notebook_cell_hit_after_paragraph_break_is_reported(tmp_path: Path) -> None:
    # Path.read_text() normalizes CRLF in .md files, but a notebook cell string keeps its \r\n
    text = "a `x\r\n\r\nOpenSysML cannot` b\r\n"
    make_repo(tmp_path, {"chapters/ch/a.ipynb": json.dumps({"cells": [{"cell_type": "markdown", "source": text}]})})
    hs = lint.scan(tmp_path, lint.load_rules())
    assert [(h.rule, h.cell, h.line) for h in hs] == [("opensysml-capability", 0, 3)]
    crlf_fence = "```\r\nfoo\r\n```\r\nfoo\r\n"
    make_repo(tmp_path, {"chapters/ch/a.ipynb": json.dumps({"cells": [{"cell_type": "markdown", "source": crlf_fence}]})})
    hs = lint.scan(tmp_path, lint.load_rules(two_rule_file(tmp_path)))
    assert [(h.rule, h.line) for h in hs if h.rule == MASKED] == [(MASKED, 4)]


def test_mask_preserves_length_and_line_structure() -> None:
    text = "a `x`\n```\ny\nz\n```\n~~~\nw\n~~~\nlast ``q `r`` end\r\nfoo\n"
    masked = lint.mask_code(text)
    assert len(masked) == len(text)
    assert [i for i, c in enumerate(masked) if c in "\r\n"] == [i for i, c in enumerate(text) if c in "\r\n"]
    assert "x" not in masked and "y" not in masked and "w" not in masked and "q" not in masked and "r" not in masked
    assert masked.endswith("foo\n") and masked.startswith("a ")


def test_masking_leaves_line_numbers_and_text_unchanged(tmp_path: Path) -> None:
    text = "line1 `foo`\n```\nfoo\nfoo\n```\nline6 foo and `x`\n"
    hs = scan_two(tmp_path, text)
    plain = [h.line for h in hs if h.rule == PLAIN]
    masked = [h for h in hs if h.rule == MASKED]
    assert plain == [1, 3, 4, 6]
    assert [(h.line, h.text) for h in masked] == [(6, "foo")]


def test_masked_rule_in_notebook_markdown_cell(tmp_path: Path) -> None:
    make_repo(tmp_path, {"chapters/ch/a.ipynb": nb(("markdown", "intro\n\nuse `foo` then foo\n"))})
    hs = lint.scan(tmp_path, lint.load_rules(two_rule_file(tmp_path)))
    assert [(h.rule, h.cell, h.line) for h in hs if h.rule == MASKED] == [(MASKED, 0, 3)]
    assert [h.line for h in hs if h.rule == PLAIN] == [3, 3]


def test_default_rules_hit_sets_ignore_code_false_for_existing_rules() -> None:
    flags = {r.id: r.ignore_code for r in lint.load_rules()}
    existing = ("tall-named", "no-em-dash", "concept-selection", "sub-behavior",
                "stale-physical-layer", "stale-partition", "accepted-disposition")
    assert all(flags[i] is False for i in existing)
    new = [i for i in flags if i not in existing]
    assert len(new) == 6 and all(flags[i] for i in new)
    assert all(r.severity == "error" and "AGENTS.md 1.2" in r.why and "DL-116" in r.why
               for r in lint.load_rules() if r.id in new)


def test_existing_rule_still_sees_code_text(tmp_path: Path) -> None:
    # existing rules are not masked: an em-dash inside backticks is still reported
    assert "no-em-dash" in ids(hits_for(tmp_path, "see `a\u2014b` here\n"))


@pytest.mark.parametrize("value", ["'yes'", "1", "[true]", "'true'"])
def test_non_bool_ignore_code_is_exit_2(tmp_path: Path, value: str) -> None:
    p = tmp_path / "rules.toml"
    p.write_text("[[rule]]\nid='r'\nregex='x'\nmessage='m'\nwhy='w'\nseverity='error'\nscope='learner'\n"
                 f"ignore_code={value}\n")
    r = runner.invoke(app, ["lint", "--repo", str(tmp_path), "--rules", str(p)])
    assert r.exit_code == 2 and "field 'ignore_code' must be a boolean" in r.output and "Traceback" not in r.output


def test_bool_ignore_code_accepted_and_default_false(tmp_path: Path) -> None:
    base = "message='m'\nwhy='w'\nseverity='error'\nscope='learner'\n"
    p = tmp_path / "rules.toml"
    p.write_text(f"[[rule]]\nid='a'\nregex='x'\n{base}\n[[rule]]\nid='b'\nregex='x'\nignore_code=false\n{base}\n"
                 f"[[rule]]\nid='c'\nregex='x'\nignore_code=true\n{base}")
    assert [r.ignore_code for r in lint.load_rules(p)] == [False, False, True]


def test_docs_superpowers_is_not_scanned(tmp_path: Path) -> None:
    bad = "sub-behavior and concept selection\n"
    make_repo(tmp_path, {"docs/superpowers/specs/s.md": bad, "docs/superpowers/plans/deep/p.md": bad})
    assert lint.scan(tmp_path, lint.load_rules()) == []
    make_repo(tmp_path, {"docs/superpowers.md": bad, "docs/superpowersx/y.md": bad, "chapters/superpowers/z.md": bad})
    assert {h.file for h in lint.scan(tmp_path, lint.load_rules())} == {
        "docs/superpowers.md", "docs/superpowersx/y.md", "chapters/superpowers/z.md"}


def test_guard_rules_ignore_code_in_markdown_but_not_prose(tmp_path: Path) -> None:
    # the protected stored-output pattern: a code span quoting a bare name is not reported
    make_repo(tmp_path, {"docs/a.md": "The output reads `OpenSysML cannot do it` verbatim.\n```\nOpenSysML v0.9.0\n```\n"})
    assert lint.scan(tmp_path, lint.load_rules()) == []
    make_repo(tmp_path, {"docs/a.md": "OpenSysML cannot do it, and OpenSysML v0.9.0 is old.\n"})
    assert ids(lint.scan(tmp_path, lint.load_rules())) == ["opensysml-capability", "opensysml-version"]


def test_guard_rules_sanctioned_sentence_passes(tmp_path: Path) -> None:
    ok = "the OpenSysML runtime accepts X; sysml-toolkit v0.9.1 rejects it\n"
    assert hits_for(tmp_path, ok) == []
