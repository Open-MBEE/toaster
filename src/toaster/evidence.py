"""Engineering review records. WP-6 completes validate_record and check_stale."""

import hashlib
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class ReviewRecord:
    identifier: str
    kind: Literal["asserted_context", "asserted_inference", "asserted_solution"]
    claim: str
    model_ref: str
    content_hash: str
    scope: str
    criteria: str
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


def validate_record(r: ReviewRecord) -> list[str]:
    """Return a list of field-level validation errors (empty = valid). WP-6 stub."""
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
    return errors


def check_stale(r: ReviewRecord, current_content: str) -> bool:
    """Return True if the record's content_hash no longer matches current_content."""
    return r.content_hash != hash_content(current_content)
