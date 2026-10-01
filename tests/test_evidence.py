import pytest
import opensysml

from toaster.evidence import ReviewRecord, validate_record, hash_content


def _base_kwargs(**overrides):
    kwargs = dict(
        identifier="RR-TEST",
        kind="asserted_solution",
        claim="Test claim.",
        model_ref="models/test.sysml",
        content_hash="deadbeef",
        scope="test scope",
        criteria="test criteria",
        rationale="test rationale",
        counterevidence="test counterevidence",
    )
    kwargs.update(overrides)
    return kwargs


def test_subject_ref_defaults_empty():
    r = ReviewRecord(**_base_kwargs())
    assert r.subject_ref == ""


def test_subject_ref_required_for_asserted_context_without_model():
    r = ReviewRecord(**_base_kwargs(kind="asserted_context"))
    errors = validate_record(r)
    assert any("subject_ref" in e for e in errors)


def test_subject_ref_required_for_asserted_solution_without_model():
    r = ReviewRecord(**_base_kwargs(kind="asserted_solution"))
    errors = validate_record(r)
    assert any("subject_ref" in e for e in errors)


def test_subject_ref_may_be_empty_for_asserted_inference_with_premises():
    r = ReviewRecord(**_base_kwargs(kind="asserted_inference", premises=["some premise"]))
    errors = validate_record(r)
    assert not any("subject_ref" in e for e in errors)


def test_subject_ref_required_for_asserted_inference_without_premises():
    r = ReviewRecord(**_base_kwargs(kind="asserted_inference", premises=[]))
    errors = validate_record(r)
    assert any("subject_ref" in e for e in errors)
    # the pre-existing premises rule must still also fire -- this is a real double-error case
    assert any("premise" in e for e in errors)


def test_validate_record_without_model_arg_still_works():
    # Existing call sites across the repo call validate_record(record) with one argument.
    r = ReviewRecord(**_base_kwargs(subject_ref="ToasterDemo::anything"))
    errors = validate_record(r)  # no model= passed
    assert errors == []


_FIXTURE = """
package ToasterDemo {
    part def Widget {
        attribute flag : ScalarValues::Boolean;
    }
    part target : Widget;

    metadata def ReviewRecordRef {
        attribute identifier : ScalarValues::String;
    }

    metadata rrTag : ReviewRecordRef about target {
        identifier = "RR-TEST";
    }
}
"""


@pytest.fixture
def loaded_model():
    conn = opensysml.connect(version="v0.9.0")
    model = conn.load_from_content(_FIXTURE, strict=False)
    assert model.ok, model.diagnostics
    yield model
    conn.close()


def test_subject_ref_resolution_check_passes_for_real_element(loaded_model):
    r = ReviewRecord(**_base_kwargs(subject_ref="ToasterDemo::target"))
    errors = validate_record(r, model=loaded_model)
    assert errors == []


def test_subject_ref_resolution_check_fails_for_unresolvable_element(loaded_model):
    r = ReviewRecord(**_base_kwargs(subject_ref="ToasterDemo::doesNotExist"))
    errors = validate_record(r, model=loaded_model)
    assert any("doesNotExist" in e for e in errors)


def test_cross_representation_check_passes_when_tag_matches(loaded_model):
    r = ReviewRecord(**_base_kwargs(identifier="RR-TEST", subject_ref="ToasterDemo::target"))
    errors = validate_record(r, model=loaded_model)
    assert errors == []


def test_cross_representation_check_fails_when_tag_disagrees(loaded_model):
    # Same identifier as the model's own rrTag, but a DIFFERENT subject_ref -- this is the
    # drift the cross-representation check exists to catch.
    r = ReviewRecord(**_base_kwargs(identifier="RR-TEST", subject_ref="ToasterDemo::Widget"))
    errors = validate_record(r, model=loaded_model)
    assert any("RR-TEST" in e and "Widget" in e for e in errors)
