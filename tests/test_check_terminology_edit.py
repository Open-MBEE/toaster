"""Tests for scripts/check-terminology-edit.py, the protected-token diff checker (contract OT-2).

Every test builds a small git repository in tmp_path (git init, a base commit, a head commit), runs
the checker on base..head and asserts which rules pass and fail. Nothing here touches the network or
the real repository.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check-terminology-edit.py"
_spec = importlib.util.spec_from_file_location("check_terminology_edit", SCRIPT)
checker = importlib.util.module_from_spec(_spec)
sys.modules["check_terminology_edit"] = checker
_spec.loader.exec_module(checker)

ALL_RULES = tuple(checker.RULES)


# ---------------------------------------------------------------------------------------------
# fixture repository


def notebook(markdown: str = "Prose about OpenSysML.\n", code: str = "import opensysml\n", output: str = "ok\n") -> str:
    cells = [
        {"cell_type": "markdown", "id": "m1", "metadata": {}, "source": markdown.splitlines(keepends=True)},
        {
            "cell_type": "code",
            "id": "c1",
            "metadata": {"tags": ["x"]},
            "execution_count": 3,
            "source": code.splitlines(keepends=True),
            "outputs": [{"output_type": "stream", "name": "stdout", "text": [output]}],
        },
    ]
    nb = {"cells": cells, "metadata": {"kernelspec": {"name": "python3"}}, "nbformat": 4, "nbformat_minor": 5}
    return json.dumps(nb, indent=1) + "\n"


SKILL_MD = (
    "---\nname: demo\ndescription: A demo skill.\n---\n\n"
    "# Demo\n\nProse about OpenSysML.\n\n```python\nimport opensysml\nprint(1)\n```\n\nMore prose.\n"
)
DEFERRED = (
    "# Deferred work\n\nNote at the top.\n\n## D-001: First\n\nBody that names the runtime.\n\n"
    "## D-002: Second\n\nBody.\n"
)
SETUP = (
    "# Setup\n\nOpenSysML is used. See https://example.org/docs and https://example.org/other.\n\n"
    "Tracker: Open-MBEE/OpenSysML#12 and sysml-toolkit#4 and toaster#7.\n"
    "Package: opensysml.Model, `~/.opensysml`, OPENSYSML_VERSION, OPENSYSML_GRPC_VERSION,\n"
    "Open-MBEE/sysml-toolkit, opensysml-api, opensysml-query.\n"
)

BASE_FILES: dict[str, str] = {
    "models/a.sysml": "package A { part def P; }\n",
    "decisions/judgment-records/r1.json": '{"verdict": "ok"}\n',
    "decisions/log.md": "# Log\n\nDL-1\n",
    "decisions/notes.md": "# Notes\n",
    "figures/f.svg": "<svg/>\n",
    "tests/test_x.py": "def test_x():\n    pass\n",
    "src/s.py": "X = 1\n",
    "scripts/tool.py": "Y = 2\n",
    "uv.lock": "version = 1\n",
    "docs/superpowers/plan.md": "# Plan\n",
    "docs/setup.md": SETUP,
    "DEFERRED.md": DEFERRED,
    "chapters/ch01/nb.ipynb": notebook(),
    ".claude/skills/demo/SKILL.md": SKILL_MD,
    ".claude/skills/demo/ref.md": "# Ref\n\n```\nfoo\n```\n",
    ".claude/skills/demo/example.sysml": "package Demo { part def P; }\n",
    ".claude/skills/other/SKILL.md": "---\nname: other\ndescription: Other.\n---\n\nProse.\n",
}


def run(repo: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return done.stdout.strip()


def write_files(repo: Path, files: dict[str, str | None]) -> None:
    for name, content in files.items():
        target = repo / name
        if content is None:
            target.unlink()
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def commit(repo: Path, message: str) -> None:
    run(repo, "add", "-A")
    run(repo, "commit", "-q", "-m", message)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    run(tmp_path, "init", "-q")
    write_files(tmp_path, dict(BASE_FILES))
    commit(tmp_path, "base")
    return tmp_path


def check_change(repo: Path, changes: dict[str, str | None]) -> dict[str, list[str]]:
    """Apply `changes` (None deletes), commit, and run the checker on HEAD~1..HEAD."""
    write_files(repo, changes)
    commit(repo, "head")
    return checker.check(repo, "HEAD~1", "HEAD")


def failing(results: dict[str, list[str]]) -> set[str]:
    return {letter for letter, found in results.items() if found}


# ---------------------------------------------------------------------------------------------
# passes


def test_clean_prose_change_passes_every_rule(repo: Path) -> None:
    results = check_change(
        repo,
        {
            "docs/setup.md": SETUP.replace("OpenSysML is used.", "The OpenSysML runtime is used."),
            "chapters/ch01/nb.ipynb": notebook(markdown="Prose about the OpenSysML runtime.\n"),
            "DEFERRED.md": DEFERRED.replace("Note at the top.", "Terminology note, dated.\nNote at the top."),
            ".claude/skills/demo/SKILL.md": SKILL_MD.replace("Prose about OpenSysML.", "Prose about the runtime."),
        },
    )
    assert failing(results) == set(), results


def test_new_files_in_decisions_and_superpowers_are_allowed(repo: Path) -> None:
    results = check_change(
        repo,
        {
            "decisions/opensysml-terminology/inventory.md": "| row |\nimport opensysml\n",
            "docs/superpowers/plans/new.md": "# New\n",
        },
    )
    assert failing(results) == set(), results


def test_own_files_may_change_in_scripts_and_tests(repo: Path) -> None:
    results = check_change(
        repo,
        {
            "scripts/check-terminology-edit.py": "# checker\n",
            "tests/test_check_terminology_edit.py": "# tests\n",
        },
    )
    assert failing(results) == set(), results


def test_adding_the_domain_link_does_not_change_the_api_token_count(repo: Path) -> None:
    results = check_change(
        repo,
        {"docs/setup.md": SETUP + "The stack is described at https://opensysml.org/ and opensysml.org.\n"},
    )
    assert failing(results) == set(), results


def test_no_change_at_all_passes(repo: Path) -> None:
    write_files(repo, {"unrelated.txt": "x\n"})
    commit(repo, "head")
    assert failing(checker.check(repo, "HEAD~1", "HEAD")) == set()


# ---------------------------------------------------------------------------------------------
# rule (a)


@pytest.mark.parametrize(
    "path",
    [
        "models/a.sysml",
        "decisions/judgment-records/r1.json",
        "figures/f.svg",
        "tests/test_x.py",
        "src/s.py",
        "scripts/tool.py",
        "uv.lock",
        "decisions/notes.md",
        "docs/superpowers/plan.md",
    ],
)
def test_rule_a_fails_on_a_changed_protected_file(repo: Path, path: str) -> None:
    results = check_change(repo, {path: BASE_FILES[path] + "changed\n"})
    assert "a" in failing(results)
    assert any(path in line for line in results["a"])


@pytest.mark.parametrize(
    "path",
    ["models/new.sysml", "decisions/judgment-records/r2.json", "figures/g.svg", "src/new.py", "tests/test_new.py"],
)
def test_rule_a_fails_on_a_new_file_in_a_strict_zone(repo: Path, path: str) -> None:
    results = check_change(repo, {path: "x\n"})
    assert "a" in failing(results)


LOG = BASE_FILES["decisions/log.md"]  # "# Log\n\nDL-1\n"


def test_rule_a_allows_an_appended_log_entry(repo: Path) -> None:
    results = check_change(repo, {"decisions/log.md": LOG + "\n## DL-2\n\nNew entry.\n"})
    assert failing(results) == set(), results


def test_rule_a_allows_log_append_when_base_lacked_a_trailing_newline(repo: Path) -> None:
    write_files(repo, {"decisions/log.md": LOG.rstrip("\n")})
    commit(repo, "no trailing newline")
    results = check_change(repo, {"decisions/log.md": LOG + "DL-2\n"})
    assert failing(results) == set(), results


@pytest.mark.parametrize(
    "new",
    [
        "# Log\n\nDL-1 edited\n",  # edited existing line
        "# Log\n\nDL-0\n\nDL-1\n",  # line inserted in the middle
        "New first line\n# Log\n\nDL-1\n",  # line inserted at the start
        "# Log\n\n",  # last line deleted
        "# Log\nDL-1\n",  # blank line deleted
        "",  # emptied
    ],
)
def test_rule_a_fails_on_a_non_append_change_to_the_log(repo: Path, new: str) -> None:
    results = check_change(repo, {"decisions/log.md": new})
    assert failing(results) == {"a"}, results
    assert any("decisions/log.md" in line for line in results["a"])


def test_rule_a_append_exception_is_only_for_the_log(repo: Path) -> None:
    results = check_change(repo, {"DEFERRED.md": DEFERRED, "docs/superpowers/plan.md": "# Plan\nappended\n"})
    assert failing(results) == {"a"}, results


def test_rule_a_fails_on_a_deleted_log(repo: Path) -> None:
    results = check_change(repo, {"decisions/log.md": None})
    assert "a" in failing(results)


def test_rule_a_fails_on_a_deleted_decisions_file(repo: Path) -> None:
    results = check_change(repo, {"decisions/notes.md": None})
    assert "a" in failing(results)


def test_rule_a_fails_on_a_changed_judgment_record_even_with_prose_elsewhere(repo: Path) -> None:
    results = check_change(
        repo,
        {
            "decisions/judgment-records/r1.json": '{"verdict": "changed"}\n',
            "docs/setup.md": SETUP.replace("OpenSysML is used.", "The OpenSysML runtime is used."),
        },
    )
    assert failing(results) == {"a"}, results


# ---------------------------------------------------------------------------------------------
# rule (b)


def test_rule_b_fails_on_a_changed_code_cell(repo: Path) -> None:
    results = check_change(repo, {"chapters/ch01/nb.ipynb": notebook(code="import opensysml\nprint('x')\n")})
    assert "b" in failing(results)
    assert any("code cell 1" in line for line in results["b"])


def test_rule_b_fails_on_a_changed_output(repo: Path) -> None:
    results = check_change(repo, {"chapters/ch01/nb.ipynb": notebook(output="changed\n")})
    assert failing(results) == {"b"}, results
    assert any("outputs" in line for line in results["b"])


def test_rule_b_fails_on_changed_execution_count_id_and_metadata(repo: Path) -> None:
    base = json.loads(BASE_FILES["chapters/ch01/nb.ipynb"])
    for mutate in (
        lambda nb: nb["cells"][1].__setitem__("execution_count", 4),
        lambda nb: nb["cells"][1].__setitem__("id", "c9"),
        lambda nb: nb["cells"][1]["metadata"].__setitem__("tags", ["y"]),
        lambda nb: nb["cells"][0].__setitem__("id", "m9"),
        lambda nb: nb["cells"][0]["metadata"].__setitem__("k", 1),
        lambda nb: nb["metadata"].__setitem__("language_info", {"name": "python"}),
    ):
        nb = json.loads(json.dumps(base))
        mutate(nb)
        write_files(repo, {"chapters/ch01/nb.ipynb": json.dumps(nb, indent=1) + "\n"})
        assert checker.rule_b(
            checker.changed_files(repo, "HEAD", None),
            checker.Tree(repo, "HEAD"),
            checker.Tree(repo, None),
        ), mutate
        run(repo, "checkout", "--", "chapters/ch01/nb.ipynb")


def test_rule_b_fails_on_cell_count_and_order(repo: Path) -> None:
    nb = json.loads(BASE_FILES["chapters/ch01/nb.ipynb"])
    nb["cells"].append({"cell_type": "markdown", "id": "m2", "metadata": {}, "source": ["extra\n"]})
    results = check_change(repo, {"chapters/ch01/nb.ipynb": json.dumps(nb, indent=1) + "\n"})
    assert "b" in failing(results)
    assert any("cell count" in line for line in results["b"])

    nb = json.loads(BASE_FILES["chapters/ch01/nb.ipynb"])
    nb["cells"].reverse()
    results = check_change(repo, {"chapters/ch01/nb.ipynb": json.dumps(nb, indent=1) + "\n"})
    assert "b" in failing(results)


def test_rule_b_allows_markdown_source_only(repo: Path) -> None:
    results = check_change(repo, {"chapters/ch01/nb.ipynb": notebook(markdown="Entirely new prose.\n")})
    assert failing(results) == set(), results


def test_rule_b_ignores_whitespace_reformatting_of_the_json(repo: Path) -> None:
    compact = json.dumps(json.loads(BASE_FILES["chapters/ch01/nb.ipynb"]))
    results = check_change(repo, {"chapters/ch01/nb.ipynb": compact})
    assert failing(results) == set(), results


# ---------------------------------------------------------------------------------------------
# rule (c)


def test_rule_c_fails_when_a_token_is_removed(repo: Path) -> None:
    results = check_change(repo, {"docs/setup.md": SETUP.replace("Open-MBEE/OpenSysML#12", "the tracker")})
    assert "c" in failing(results)
    assert any("'Open-MBEE/OpenSysML'" in line for line in results["c"])
    assert any("'OpenSysML#12'" in line for line in results["c"])


def test_rule_c_fails_when_an_issue_number_changes(repo: Path) -> None:
    write_files(repo, {"docs/setup.md": SETUP + "See OpenSysML#590.\n"})
    commit(repo, "with 590")
    results = check_change(repo, {"docs/setup.md": SETUP + "See OpenSysML#591.\n"})
    assert failing(results) == {"c"}, results
    assert any("'OpenSysML#590' removed or altered" in line for line in results["c"])


def test_rule_c_fails_when_an_api_name_changes(repo: Path) -> None:
    write_files(repo, {"docs/setup.md": SETUP + "Call opensysml.load_model first.\n"})
    commit(repo, "with call")
    results = check_change(repo, {"docs/setup.md": SETUP + "Call opensysml.load first.\n"})
    assert failing(results) == {"c"}, results
    assert any("'opensysml.load_model'" in line for line in results["c"])


def test_rule_c_fails_on_a_lookalike_swap_even_with_a_genuine_token_added_elsewhere(repo: Path) -> None:
    write_files(repo, {"docs/setup.md": SETUP + "Call opensysml.load_model first.\nTracker OpenSysML#590.\n"})
    commit(repo, "with call")
    swapped = SETUP + "Call opensysml.load_modell first.\nTracker OpenSysML#590, OpenSysML#700.\n"
    results = check_change(repo, {"docs/setup.md": swapped})
    assert failing(results) == {"c"}, results
    assert any("'opensysml.load_model'" in line for line in results["c"])
    # the same count as before (3 api/issue tokens each side) would have passed a count comparison


@pytest.mark.parametrize(
    "old,new",
    [
        ("opensysml.Model", "opensysml_Model"),
        ("`~/.opensysml`", "`~/.cache`"),
        ("OPENSYSML_VERSION", "OPENSYSML_PIN"),
        ("OPENSYSML_GRPC_VERSION", "GRPC_PIN"),
        ("Open-MBEE/sysml-toolkit", "the toolkit repository"),
        ("sysml-toolkit#4", "sysml-toolkit issue 4"),
        ("toaster#7", "toaster issue 7"),
        ("opensysml-api", "the API skill"),
        ("opensysml-query", "the query skill"),
    ],
)
def test_rule_c_covers_each_protected_token(repo: Path, old: str, new: str) -> None:
    assert old in SETUP
    results = check_change(repo, {"docs/setup.md": SETUP.replace(old, new)})
    assert "c" in failing(results)


def test_rule_c_allows_an_added_token_and_reports_it_as_info(repo: Path) -> None:
    write_files(repo, {"docs/setup.md": SETUP + "Run `import opensysml` first.\n"})
    commit(repo, "head")
    results, all_info = checker.run_rules(repo, "HEAD~1", "HEAD")
    info = all_info["c"]
    assert failing(results) == set(), results
    # the base SETUP has no 'import opensysml', so the addition is the only info line
    assert info == ["docs/setup.md: token 'import opensysml' added (count 0 -> 1)"]
    done = run_cli(repo, "--base", "HEAD~1", "--head", "HEAD")
    assert done.returncode == 0
    assert "  info (c) docs/setup.md: token 'import opensysml' added" in done.stdout


def test_rule_c_allows_adding_the_runtime_tracker_reference(repo: Path) -> None:
    results = check_change(repo, {"docs/setup.md": SETUP + "the runtime's tracker (`Open-MBEE/OpenSysML#NNN`)\n"})
    assert failing(results) == set(), results


def test_rule_c_counts_notebook_code_cells_only(repo: Path) -> None:
    # An API token in notebook markdown prose is not protected: it may be added or removed. The same
    # token in a code cell is protected (rule (b) catches the code edit too).
    markdown_token = notebook(markdown="Call opensysml.load later.\n")
    results = check_change(repo, {"chapters/ch01/nb.ipynb": markdown_token})
    assert failing(results) == set(), results
    results = check_change(repo, {"chapters/ch01/nb.ipynb": notebook(markdown="Call the loader later.\n")})
    assert failing(results) == set(), results

    results = check_change(repo, {"chapters/ch01/nb.ipynb": notebook(code="print('x')\n")})
    assert {"b", "c"} <= failing(results)


def test_rule_c_reads_issue_references_over_all_notebook_cells(repo: Path) -> None:
    link_md = "See [toaster#19](https://example.org/t/19) and [OpenSysML#608](https://example.org/o/608).\n"
    write_files(repo, {"chapters/ch01/nb.ipynb": notebook(markdown=link_md)})
    commit(repo, "with link text")
    # removing the link text from a markdown cell fails, even though it is not a code cell
    results = check_change(repo, {"chapters/ch01/nb.ipynb": notebook(markdown="See the issues.\n")})
    assert failing(results) == {"c", "g"}, results  # (g): the link URLs went with the link text
    assert any("'toaster#19'" in line for line in results["c"])
    assert any("'OpenSysML#608'" in line for line in results["c"])
    # so does altering the number
    write_files(repo, {"chapters/ch01/nb.ipynb": notebook(markdown=link_md)})
    commit(repo, "restore link text")
    results = check_change(repo, {"chapters/ch01/nb.ipynb": notebook(markdown=link_md.replace("#608", "#609"))})
    assert failing(results) == {"c"}, results
    # leaving the link text alone while editing the prose passes
    write_files(repo, {"chapters/ch01/nb.ipynb": notebook(markdown=link_md)})
    commit(repo, "restore link text")
    results = check_change(repo, {"chapters/ch01/nb.ipynb": notebook(markdown="Also see [toaster#19](https://example.org/t/19) and [OpenSysML#608](https://example.org/o/608).\n")})
    assert failing(results) == set(), results


def test_rule_c_does_not_confuse_the_bare_name_with_a_token(repo: Path) -> None:
    results = check_change(repo, {"docs/setup.md": SETUP.replace("OpenSysML is used", "OpenSysML runtime is used")})
    assert failing(results) == set(), results


# ---------------------------------------------------------------------------------------------
# rule (d)


def test_rule_d_fails_on_a_changed_heading(repo: Path) -> None:
    results = check_change(repo, {"DEFERRED.md": DEFERRED.replace("## D-001: First", "## D-001: First (runtime)")})
    assert failing(results) == {"d"}, results


def test_rule_d_fails_on_a_removed_or_reordered_heading(repo: Path) -> None:
    results = check_change(repo, {"DEFERRED.md": DEFERRED.replace("## D-002: Second\n\nBody.\n", "")})
    assert "d" in failing(results)
    swapped = DEFERRED.replace("## D-001: First", "## D-00X").replace("## D-002: Second", "## D-001: First").replace(
        "## D-00X", "## D-002: Second"
    )
    results = check_change(repo, {"DEFERRED.md": swapped})
    assert "d" in failing(results)


def test_rule_d_allows_body_edits(repo: Path) -> None:
    results = check_change(repo, {"DEFERRED.md": DEFERRED.replace("Body that names the runtime.", "Body that names the OpenSysML runtime.")})
    assert failing(results) == set(), results


# ---------------------------------------------------------------------------------------------
# rules (e) and (f)


def test_rule_e_fails_on_a_changed_skill_code_fence(repo: Path) -> None:
    results = check_change(repo, {".claude/skills/demo/SKILL.md": SKILL_MD.replace("print(1)", "print(2)")})
    assert failing(results) == {"e"}, results


def test_rule_e_fails_on_a_changed_fence_in_a_reference_file(repo: Path) -> None:
    results = check_change(repo, {".claude/skills/demo/ref.md": "# Ref\n\n```\nbar\n```\n"})
    assert failing(results) == {"e"}, results


def test_rule_e_fails_on_a_removed_or_added_fence(repo: Path) -> None:
    results = check_change(repo, {".claude/skills/demo/SKILL.md": SKILL_MD + "\n```\nextra\n```\n"})
    assert "e" in failing(results)
    results = check_change(repo, {".claude/skills/demo/SKILL.md": SKILL_MD.replace("```python\nimport opensysml\nprint(1)\n```\n", "")})
    assert "e" in failing(results)


def test_rule_e_ignores_prose_around_the_fence(repo: Path) -> None:
    results = check_change(repo, {".claude/skills/demo/SKILL.md": SKILL_MD.replace("More prose.", "Different prose, same fence.")})
    assert failing(results) == set(), results


@pytest.mark.parametrize("change", ["modify", "delete", "add"])
def test_rule_e_fails_on_any_change_to_a_non_markdown_skill_file(repo: Path, change: str) -> None:
    path = ".claude/skills/demo/example.sysml"
    if change == "modify":
        changes = {path: BASE_FILES[path].replace("P;", "Q;")}
    elif change == "delete":
        changes = {path: None}
    else:
        changes = {".claude/skills/demo/extra.json": "{}\n"}
    results = check_change(repo, changes)
    assert failing(results) == {"e"}, results
    assert any("non-markdown" in line for line in results["e"])


def test_fenced_blocks_handles_tilde_fences_and_longer_fences() -> None:
    text = "a\n~~~\none\n~~~\n````\ntwo\n```\nstill two\n````\nz\n"
    assert checker.fenced_blocks(text) == ["~~~\none\n~~~", "````\ntwo\n```\nstill two\n````"]


def test_rule_f_fails_on_a_renamed_skill_directory(repo: Path) -> None:
    run(repo, "mv", ".claude/skills/other", ".claude/skills/renamed")
    commit(repo, "head")
    results = checker.check(repo, "HEAD~1", "HEAD")
    assert "f" in failing(results)
    assert any("removed or renamed" in line for line in results["f"])
    assert any("added" in line for line in results["f"])


def test_rule_f_fails_on_a_changed_name_frontmatter(repo: Path) -> None:
    results = check_change(repo, {".claude/skills/other/SKILL.md": "---\nname: other-renamed\ndescription: Other.\n---\n\nProse.\n"})
    assert failing(results) == {"f"}, results


def test_rule_f_allows_a_description_change(repo: Path) -> None:
    results = check_change(repo, {".claude/skills/other/SKILL.md": "---\nname: other\ndescription: The OpenSysML runtime.\n---\n\nProse.\n"})
    assert failing(results) == set(), results


# ---------------------------------------------------------------------------------------------
# rule (g)


def test_rule_g_fails_on_a_removed_url(repo: Path) -> None:
    results = check_change(repo, {"docs/setup.md": SETUP.replace(" and https://example.org/other", "")})
    assert failing(results) == {"g"}, results
    assert any("https://example.org/other" in line for line in results["g"])


def test_rule_g_fails_on_a_url_removed_from_a_notebook_markdown_cell(repo: Path) -> None:
    with_url = notebook(markdown="See https://example.org/nb for details.\n")
    write_files(repo, {"chapters/ch01/nb.ipynb": with_url})
    commit(repo, "add url")
    write_files(repo, {"chapters/ch01/nb.ipynb": notebook(markdown="See the page for details.\n")})
    commit(repo, "remove url")
    results = checker.check(repo, "HEAD~1", "HEAD")
    assert failing(results) == {"g"}, results


def test_rule_g_fails_when_one_of_two_identical_urls_is_removed(repo: Path) -> None:
    twice = SETUP + "Again: https://example.org/docs\n"
    write_files(repo, {"docs/setup.md": twice})
    commit(repo, "two occurrences")
    results = check_change(repo, {"docs/setup.md": SETUP})
    assert failing(results) == {"g"}, results
    assert any("count decreased (2 -> 1)" in line for line in results["g"])


def test_rule_g_allows_an_added_occurrence_or_url(repo: Path) -> None:
    results = check_change(repo, {"docs/setup.md": SETUP + "Again: https://example.org/docs and https://more.example/y\n"})
    assert failing(results) == set(), results


def test_rule_g_keeps_trailing_underscore_and_asterisk(repo: Path) -> None:
    write_files(repo, {"docs/setup.md": SETUP + "See https://example.org/a_ and https://example.org/b*\n"})
    commit(repo, "with odd urls")
    results = check_change(repo, {"docs/setup.md": SETUP + "See https://example.org/a and https://example.org/b\n"})
    assert failing(results) == {"g"}, results


def test_rule_g_allows_moving_or_adding_urls_and_trailing_punctuation(repo: Path) -> None:
    changed = SETUP.replace("https://example.org/docs and https://example.org/other.", "(https://example.org/other) then https://example.org/docs, and https://new.example/x.")
    results = check_change(repo, {"docs/setup.md": changed})
    assert failing(results) == set(), results


def test_fenced_blocks_recognise_any_indentation() -> None:
    text = "- item\n\n      ```python\n      x = 1\n      ```\n\ntext\n    ~~~\n    y\n    ~~~\n"
    assert checker.fenced_blocks(text) == [
        "      ```python\n      x = 1\n      ```",
        "    ~~~\n    y\n    ~~~",
    ]


def test_rule_e_fails_on_a_changed_deeply_indented_fence(repo: Path) -> None:
    indented = SKILL_MD + "\n- item\n\n      ```python\n      x = 1\n      ```\n"
    write_files(repo, {".claude/skills/demo/SKILL.md": indented})
    commit(repo, "indented fence")
    results = check_change(repo, {".claude/skills/demo/SKILL.md": indented.replace("x = 1", "x = 2")})
    assert failing(results) == {"e"}, results


# ---------------------------------------------------------------------------------------------
# strict zones added by ruling Q1, and --allow


@pytest.mark.parametrize(
    "path",
    [
        "glossary/lint.py",
        "glossary/tests/test_lint.py",
        "pyproject.toml",
        "package.json",
        "package-lock.json",
        ".github/workflows/ci.yml",
    ],
)
def test_rule_a_covers_the_q1_zones(repo: Path, path: str) -> None:
    results = check_change(repo, {path: "x = 1\n"})
    assert "a" in failing(results)
    assert any(path in line for line in results["a"])


def test_rule_a_does_not_cover_glossary_data_files(repo: Path) -> None:
    results = check_change(repo, {"glossary/lint_rules.toml": "[[rule]]\n", "glossary/README.md": "x\n"})
    assert "a" not in failing(results), results


def test_allow_exempts_matching_paths_from_rule_a_only(repo: Path) -> None:
    changes = {"glossary/tests/test_lint.py": "x = 1\n", "glossary/lint.py": "y = 1\n", "models/a.sysml": "z\n"}
    write_files(repo, changes)
    commit(repo, "head")
    results = checker.check(repo, "HEAD~1", "HEAD", allow=["glossary/tests/*"])
    assert [line.split(":")[0] for line in results["a"]] == ["glossary/lint.py", "models/a.sysml"]
    results = checker.check(repo, "HEAD~1", "HEAD", allow=["glossary/tests/*", "glossary/lint.py", "models/*"])
    assert failing(results) == set(), results


def test_allow_does_not_exempt_other_rules(repo: Path) -> None:
    results = checker.check(
        repo, "HEAD", None, allow=["DEFERRED.md"]
    )
    assert failing(results) == set()
    write_files(repo, {"DEFERRED.md": DEFERRED.replace("## D-001: First", "## D-001: Renamed")})
    results = checker.check(repo, "HEAD", None, allow=["DEFERRED.md"])
    assert failing(results) == {"d"}, results


def test_cli_allow_option_is_repeatable(repo: Path) -> None:
    write_files(repo, {"glossary/tests/test_lint.py": "x = 1\n", "glossary/lint.py": "y = 1\n"})
    commit(repo, "head")
    base_args = ("--base", "HEAD~1", "--head", "HEAD")
    assert run_cli(repo, *base_args).returncode == 1
    assert run_cli(repo, *base_args, "--allow", "glossary/tests/*").returncode == 1
    done = run_cli(repo, *base_args, "--allow", "glossary/tests/*", "--allow", "glossary/lint.py")
    assert done.returncode == 0, done.stdout
    assert "--allow" in run_cli(repo, "--help").stdout


def test_allow_is_never_silent(repo: Path) -> None:
    write_files(repo, {"glossary/tests/test_lint.py": "x = 1\n", "glossary/lint.py": "y = 1\n", "docs/setup.md": SETUP + "extra\n"})
    commit(repo, "head")
    base_args = ("--base", "HEAD~1", "--head", "HEAD")
    done = run_cli(repo, *base_args, "--allow", "glossary/tests/*", "--allow", "glossary/lint.py", "--allow", "unused/*")
    assert done.returncode == 0, done.stdout
    lines = done.stdout.splitlines()
    assert lines[0] == "allow: glossary/tests/*, glossary/lint.py, unused/*"
    assert "  info (a) exempted by --allow 'glossary/tests/*': glossary/tests/test_lint.py (A)" in lines
    assert "  info (a) exempted by --allow 'glossary/lint.py': glossary/lint.py (A)" in lines
    assert lines[-1] == "RESULT: PASS (with 2 --allow exemption(s))"
    # a glob that matches only non-violating paths waives nothing, so the result line stays plain
    done = run_cli(repo, *base_args, "--allow", "docs/*")
    assert "info (a)" not in done.stdout
    assert done.stdout.splitlines()[0] == "allow: docs/*"
    # a failing run still reports its waivers
    write_files(repo, {"models/a.sysml": "changed\n"})
    commit(repo, "more")
    done = run_cli(repo, "--base", "HEAD~2", "--head", "HEAD", "--allow", "glossary/*")
    assert done.returncode == 1
    assert done.stdout.splitlines()[-1] == "RESULT: FAIL (with 2 --allow exemption(s))"


def test_allow_star_cannot_hide_the_waiver(repo: Path) -> None:
    write_files(repo, {"models/a.sysml": "changed\n", "uv.lock": "version = 2\n"})
    commit(repo, "head")
    done = run_cli(repo, "--base", "HEAD~1", "--head", "HEAD", "--allow", "*")
    assert done.returncode == 0
    assert done.stdout.splitlines()[0] == "allow: *"
    assert "  info (a) exempted by --allow '*': models/a.sysml (M)" in done.stdout
    assert "  info (a) exempted by --allow '*': uv.lock (M)" in done.stdout
    assert done.stdout.splitlines()[-1] == "RESULT: PASS (with 2 --allow exemption(s))"


def test_nothing_extra_is_printed_without_allow(repo: Path) -> None:
    write_files(repo, {"docs/setup.md": SETUP.replace("OpenSysML is used.", "The OpenSysML runtime is used.")})
    commit(repo, "head")
    done = run_cli(repo, "--base", "HEAD~1", "--head", "HEAD")
    assert "allow" not in done.stdout and "info" not in done.stdout
    assert done.stdout.splitlines()[-1] == "RESULT: PASS"


def test_help_tells_reviewers_to_run_from_a_pinned_revision() -> None:
    assert "pinned revision" in checker.__doc__
    assert "SELF" in checker.__doc__


# ---------------------------------------------------------------------------------------------
# repository root resolution


def test_check_works_from_a_subdirectory(repo: Path) -> None:
    write_files(repo, {"models/a.sysml": "changed\n", "docs/setup.md": SETUP.replace("OpenSysML is used.", "The OpenSysML runtime is used.")})
    commit(repo, "head")
    sub = repo / "docs"
    results = checker.check(sub, "HEAD~1", "HEAD")
    assert failing(results) == {"a"}, results
    done = run_cli(sub, "--base", "HEAD~1", "--head", "HEAD")
    assert done.returncode == 1
    assert "models/a.sysml" in done.stdout


def test_working_tree_head_from_a_subdirectory(repo: Path) -> None:
    write_files(repo, {"docs/setup.md": SETUP.replace("Open-MBEE/OpenSysML#12", "the tracker"), "docs/untracked.md": "x\n"})
    results = checker.check(repo / "docs", "HEAD", None)
    assert failing(results) == {"c"}, results


# ---------------------------------------------------------------------------------------------
# head defaults to the working tree; CLI


def test_head_defaults_to_the_working_tree(repo: Path) -> None:
    write_files(repo, {"models/a.sysml": "changed\n", "docs/new.md": "x https://u.example/\n"})
    results = checker.check(repo, "HEAD", None)
    assert failing(results) == {"a"}, results
    assert any("models/a.sysml" in line for line in results["a"])
    run(repo, "checkout", "--", "models/a.sysml")
    assert failing(checker.check(repo, "HEAD", None)) == set()


def test_working_tree_deletion_of_a_file_with_tokens_and_urls_fails_c_and_g(repo: Path) -> None:
    (repo / "docs" / "setup.md").unlink()
    results = checker.check(repo, "HEAD", None)
    assert {"c", "g"} <= failing(results)


def run_cli(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_prints_pass_for_every_rule_and_exits_zero(repo: Path) -> None:
    write_files(repo, {"docs/setup.md": SETUP.replace("OpenSysML is used.", "The OpenSysML runtime is used.")})
    commit(repo, "head")
    done = run_cli(repo, "--base", "HEAD~1", "--head", "HEAD")
    assert done.returncode == 0, done.stdout + done.stderr
    lines = done.stdout.splitlines()
    assert [line.split()[0] for line in lines[:-1]] == ["PASS"] * len(ALL_RULES)
    assert lines[-1] == "RESULT: PASS"


def test_cli_prints_one_line_per_violation_and_exits_one(repo: Path) -> None:
    write_files(repo, {"models/a.sysml": "changed\n", "uv.lock": "version = 2\n"})
    commit(repo, "head")
    done = run_cli(repo, "--base", "HEAD~1", "--head", "HEAD")
    assert done.returncode == 1
    assert "FAIL (a) protected zones unchanged: 2 violation(s)" in done.stdout
    assert "  (a) models/a.sysml: protected zone changed (M)" in done.stdout
    assert "  (a) uv.lock: protected zone changed (M)" in done.stdout
    assert "PASS (b)" in done.stdout
    assert done.stdout.splitlines()[-1] == "RESULT: FAIL"


def test_cli_reports_an_unknown_revision_with_exit_two(repo: Path) -> None:
    done = run_cli(repo, "--base", "no-such-rev")
    assert done.returncode == 2
    assert "error" in done.stderr
