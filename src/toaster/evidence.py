"""Engineering review records. WP-6 completes validate_record and check_stale."""

import hashlib
from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class ReviewRecord:
    identifier: str
    kind: Literal["asserted_context", "asserted_inference", "asserted_solution"]
    claim: str
    subject_ref: str = ""
    model_ref: str = ""
    content_hash: str = ""
    scope: str = ""
    criteria: str = ""
    premises: list[str] = field(default_factory=list)
    assumption_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    rationale: str = ""
    counterevidence: str = ""
    residual_uncertainties: str = ""
    disposition: Literal["pending", "accepted", "rejected"] = "pending"
    dependency_freshness: Literal["current", "stale"] = "current"
    engineering_conclusion: Literal["supported", "refuted", "undetermined"] = "undetermined"
    record_kind: Literal["worked_example", "actual_review"] = "worked_example"


def hash_content(s: str) -> str:
    """Return SHA-256 hex digest of a string."""
    return hashlib.sha256(s.encode()).hexdigest()


def validate_record(r: ReviewRecord, model: Any | None = None) -> list[str]:
    """Return a list of field-level validation errors (empty = valid).

    `subject_ref` is this tutorial's narrowed analog of Hawkins' Assurance Claim Point
    (`toaster-review-protocol`, SysML v2 formal/2026-03-02 §7.27.2): the one model
    element this specific judgment is about. Required for `asserted_context` and
    `asserted_solution`; for `asserted_inference` it may stay empty only when `premises`
    is non-empty (the pure cross-record synthesis case, e.g. `AI-C10`).

    When `model` is given and `subject_ref` is set, two further checks run: that
    `subject_ref` resolves in the model, and that any `ReviewRecordRef` metadata tag
    already present for this record's own `identifier` agrees with `subject_ref` (catching
    drift between the Python record and the model tag if they are ever edited independently).
    """
    errors = []
    if not r.identifier:
        errors.append("identifier is empty")
    if not r.claim:
        errors.append("claim is empty")
    if not r.rationale:
        errors.append("rationale is empty")
    if not r.counterevidence:
        errors.append("counterevidence is empty")
    if r.record_kind == "actual_review":
        errors.append("record_kind must be 'worked_example' in this tutorial (SA-7)")
    if r.kind == "asserted_inference" and not r.premises:
        errors.append("asserted_inference requires at least one premise (Hawkins §3.1)")

    if not r.subject_ref:
        if r.kind in ("asserted_context", "asserted_solution"):
            errors.append(
                f"subject_ref is empty (required for {r.kind})"
            )
        elif r.kind == "asserted_inference" and not r.premises:
            errors.append(
                "subject_ref is empty (required for asserted_inference with no premises)"
            )
    elif model is not None:
        if model.find(r.subject_ref) is None:
            errors.append(f"subject_ref {r.subject_ref!r} does not resolve in the model")
        else:
            from toaster.query import get_review_record_refs

            tags = {t["identifier"]: t["annotated_element"] for t in get_review_record_refs(model)}
            tagged = tags.get(r.identifier)
            if tagged is not None and tagged != r.subject_ref:
                errors.append(
                    f"ReviewRecordRef tag for {r.identifier!r} is about {tagged!r}, "
                    f"but subject_ref is {r.subject_ref!r}"
                )
    return errors


def check_stale(r: ReviewRecord, current_content: str) -> bool:
    """Return True if the record's content_hash no longer matches current_content."""
    return r.content_hash != hash_content(current_content)
