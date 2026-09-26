from __future__ import annotations

from pathlib import Path

from glossary.check import run_check, verify_sources

from .conftest import DEFS, PREFIX, SOURCES, TERMS, make_root


def errors(root: Path, repo: Path) -> list[str]:
    return [f.code for f in run_check(root, repo) if f.level == "error"]


def test_valid_fixture_passes(root: Path, repo: Path) -> None:
    assert errors(root, repo) == []


def test_missing_locator_fails_shacl(tmp_path: Path, repo: Path) -> None:
    bad = dict(DEFS)
    bad["video"] = bad["video"].replace('gl:locator "2:00" ;', "")
    assert "shacl" in errors(make_root(tmp_path, defs=bad), repo)


def test_quote_too_long_fails_shacl(tmp_path: Path, repo: Path) -> None:
    bad = dict(DEFS)
    bad["video"] = bad["video"].replace("gl:status gl:proposed .", f'gl:quote "{"x" * 301}" ; gl:status gl:proposed .')
    assert "shacl" in errors(make_root(tmp_path, defs=bad), repo)


def test_bipartite_violation_fails(tmp_path: Path, repo: Path) -> None:
    terms = TERMS + "\nglid:term-logical gl:label \"logical\" .\nglid:term-function gl:related glid:term-logical .\n"
    assert "bipartite" in errors(make_root(tmp_path, terms=terms), repo)


def test_orphan_term_fails(tmp_path: Path, repo: Path) -> None:
    terms = TERMS + '\nglid:term-lonely a gl:Term ; gl:label "lonely" .\n'
    assert "orphan-term" in errors(make_root(tmp_path, terms=terms), repo)


def test_orphan_source_fails(tmp_path: Path, repo: Path) -> None:
    sources = SOURCES + PREFIX.replace("@prefix", "@prefix", 0) + (
        '\nglid:src-idle a gl:Source ; gl:label "Idle" ; gl:edition "1" ; gl:sourceKind gl:Repository ; gl:commit "x" .\n')
    assert "orphan-source" in errors(make_root(tmp_path, sources=sources), repo)


def test_tutorial_definition_must_be_confirmed(tmp_path: Path, repo: Path) -> None:
    bad = dict(DEFS)
    bad["tutorial"] = bad["tutorial"].replace("gl:status gl:confirmed ; gl:confirmedBy \"Z\" ;", "gl:status gl:proposed ;")
    assert "tutorial-definition" in errors(make_root(tmp_path, defs=bad), repo)


def test_tutorial_definition_needs_gloss(tmp_path: Path, repo: Path) -> None:
    bad = dict(DEFS)
    bad["tutorial"] = bad["tutorial"].replace('gl:gloss "Mechanisms carried by logical components." ;', "")
    assert "tutorial-definition" in errors(make_root(tmp_path, defs=bad), repo)


def test_confirmed_by_agent_rejected(tmp_path: Path, repo: Path) -> None:
    bad = dict(DEFS)
    bad["canon"] = bad["canon"].replace('gl:confirmedBy "Z"', 'gl:confirmedBy "Claude"')
    assert "confirmed-by" in errors(make_root(tmp_path, defs=bad), repo)


def test_confirmed_requires_confirmed_by(tmp_path: Path, repo: Path) -> None:
    bad = dict(DEFS)
    bad["canon"] = bad["canon"].replace(' ;\n    gl:confirmedBy "Z" .', " .")
    assert "confirmed-by" in errors(make_root(tmp_path, defs=bad), repo)


def test_unapproved_differs_fails(tmp_path: Path, repo: Path) -> None:
    bad = dict(DEFS)
    bad["tutorial"] = bad["tutorial"].replace('gl:approvedBy "Z" ; gl:approvalNote "DL-015, 2026-09-26" .', ".")
    bad["tutorial"] = bad["tutorial"].replace("glid:def-video--logical ;\n    .", "glid:def-video--logical .")
    assert "unapproved-differs" in errors(make_root(tmp_path, defs=bad), repo)


def test_refines_only_from_tutorial_source(tmp_path: Path, repo: Path) -> None:
    bad = dict(DEFS)
    bad["video"] = bad["video"].replace("gl:status gl:proposed .", "gl:status gl:proposed ; gl:refines glid:def-canon--logical .")
    assert "refinement" in errors(make_root(tmp_path, defs=bad), repo)


def test_video_source_needs_url_and_date(tmp_path: Path, repo: Path) -> None:
    bad = SOURCES.replace('gl:url "https://example.org/v" ; ', "")
    assert "source-fields" in errors(make_root(tmp_path, sources=bad), repo)


def test_absent_source_file_warns_but_passes(tmp_path: Path, repo: Path) -> None:
    root = make_root(tmp_path, with_file=False)
    findings = run_check(root, repo)
    assert not [f for f in findings if f.level == "error"]
    assert any(f.code == "source-absent" and f.level == "warning" for f in findings)


def test_hash_mismatch_fails(tmp_path: Path, repo: Path) -> None:
    root = make_root(tmp_path)
    (root / "sources" / "local" / "canon.txt").write_bytes(b"tampered")
    assert "source-hash" in errors(root, repo)


def test_verify_sources_requires_the_files(tmp_path: Path) -> None:
    assert [f.code for f in verify_sources(make_root(tmp_path, with_file=False))] == ["source-absent"]
    assert verify_sources(make_root(tmp_path / "again")) == []
