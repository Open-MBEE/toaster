from toaster.evidence import ReviewRecord, check_stale, hash_content
from toaster.judgment_store import load_record, records_citing, save_record


def _sample_record(identifier="AC-TEST", premises=None):
    return ReviewRecord(
        identifier=identifier,
        kind="asserted_context",
        claim="A test claim.",
        subject_ref="ToasterDemo::Toaster",
        model_ref="ToasterDemo::Toaster",
        content_hash=hash_content("some model text"),
        scope="A test scope.",
        criteria="A test criterion.",
        premises=premises or [],
        assumption_refs=["AS-TEST-ASSUMPTION"],
        evidence_refs=["some evidence"],
        rationale="A test rationale.",
        counterevidence="A test counterevidence.",
        residual_uncertainties="A test residual uncertainty.",
        disposition="pending",
        dependency_freshness="current",
        engineering_conclusion="undetermined",
        record_kind="worked_example",
    )


def test_save_record_writes_one_json_file_per_identifier(tmp_path):
    record = _sample_record()
    path = save_record(record, store_dir=tmp_path)
    assert path == tmp_path / "AC-TEST.json"
    assert path.exists()


def test_round_trip_save_then_load_returns_equal_record(tmp_path):
    record = _sample_record()
    save_record(record, store_dir=tmp_path)
    loaded = load_record("AC-TEST", store_dir=tmp_path)
    assert loaded == record


def test_records_citing_finds_a_record_whose_premises_names_the_identifier(tmp_path):
    origin = _sample_record(identifier="AC-ORIGIN")
    citing = _sample_record(identifier="AI-CITING", premises=["AC-ORIGIN"])
    unrelated = _sample_record(identifier="AS-UNRELATED")
    save_record(origin, store_dir=tmp_path)
    save_record(citing, store_dir=tmp_path)
    save_record(unrelated, store_dir=tmp_path)

    citers = records_citing("AC-ORIGIN", store_dir=tmp_path)

    assert [r.identifier for r in citers] == ["AI-CITING"]


def test_loaded_record_still_works_with_check_stale(tmp_path):
    record = _sample_record()
    save_record(record, store_dir=tmp_path)
    loaded = load_record("AC-TEST", store_dir=tmp_path)

    assert check_stale(loaded, "some model text") is False
    assert check_stale(loaded, "different model text") is True
