"""Persisted store for ReviewRecord: one JSON file per identifier under decisions/judgment-records/.

A judgment's content is authored once, where it was made (src/toaster/evidence.py's own
ReviewRecord, validated there); this module is the missing second half of that design -- save it,
then load it instead of retyping it in a later chapter. See
docs/superpowers/specs/2026-10-02-judgment-record-store-design.md.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from toaster.evidence import ReviewRecord

SCHEMA_VERSION = 1


def _default_store_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "decisions" / "judgment-records"


def save_record(record: ReviewRecord, store_dir: Path | None = None) -> Path:
    """Persist `record` as decisions/judgment-records/<identifier>.json. Returns the written path."""
    directory = store_dir or _default_store_dir()
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{record.identifier}.json"
    payload = {"schema_version": SCHEMA_VERSION, **asdict(record)}
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path


def load_record(identifier: str, store_dir: Path | None = None) -> ReviewRecord:
    """Load a previously-saved ReviewRecord by its own identifier."""
    directory = store_dir or _default_store_dir()
    data = json.loads((directory / f"{identifier}.json").read_text())
    data.pop("schema_version", None)
    return ReviewRecord(**data)


def records_citing(identifier: str, store_dir: Path | None = None) -> list[ReviewRecord]:
    """Every stored record whose own `premises` list names `identifier`."""
    directory = store_dir or _default_store_dir()
    out = []
    for path in sorted(directory.glob("*.json")):
        data = json.loads(path.read_text())
        if identifier in data.get("premises", []):
            data.pop("schema_version", None)
            out.append(ReviewRecord(**data))
    return out
