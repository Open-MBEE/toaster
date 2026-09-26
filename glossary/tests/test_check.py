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


def _tiny_pdf(text: str) -> bytes:
    """A one-page PDF containing `text` (Helvetica), built by hand so no PDF library is needed."""
    stream = f"BT /F1 12 Tf 72 700 Td ({text}) Tj ET".encode()
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
            b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out, offsets = b"%PDF-1.4\n", []
    for n, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % n + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += b"".join(b"%010d 00000 n \n" % o for o in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    return out


def _pdf_root(tmp_path: Path, quote: str, page_text: str) -> Path:
    import hashlib
    import shutil

    import pytest

    if shutil.which("pdftotext") is None:
        pytest.skip("pdftotext not installed")
    pdf = _tiny_pdf(page_text)
    sources = SOURCES.replace(FILE_SHA_PLACEHOLDER, hashlib.sha256(pdf).hexdigest())
    root = make_root(tmp_path, sources=sources)
    (root / "sources" / "local" / "canon.txt").write_bytes(pdf)
    defs = root / "definitions" / "canon.ttl"
    defs.write_text(defs.read_text().replace('gl:locator "p. 5" ;', f'gl:locator "p. 5" ; gl:quote "{quote}" ; gl:pdfPage 1 ;'))
    return root


from .conftest import FILE_SHA as FILE_SHA_PLACEHOLDER  # noqa: E402


def test_quote_on_its_page_passes(tmp_path: Path, repo: Path) -> None:
    root = _pdf_root(tmp_path, "logical includes the functional view", "Canon says logical includes the functional view.")
    assert errors(root, repo) == []


def test_quote_not_on_its_page_fails(tmp_path: Path, repo: Path) -> None:
    root = _pdf_root(tmp_path, "something the source never says", "Canon says logical includes the functional view.")
    assert "quote-not-on-page" in errors(root, repo)
    assert "quote-not-on-page" in [f.code for f in verify_sources(root)]


def test_refines_may_narrow_another_terms_definition(tmp_path: Path, repo: Path) -> None:
    ok = dict(DEFS)
    ok["tutorial"] = ok["tutorial"].replace("gl:refines glid:def-video--logical", "gl:refines glid:def-canon--function")
    assert errors(make_root(tmp_path, defs=ok), repo) == []


def test_differs_from_must_be_the_same_term(tmp_path: Path, repo: Path) -> None:
    bad = dict(DEFS)
    bad["tutorial"] = bad["tutorial"].replace("gl:differsFrom glid:def-canon--logical", "gl:differsFrom glid:def-canon--function")
    assert "refinement" in errors(make_root(tmp_path, defs=bad), repo)
