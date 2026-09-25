"""Model element queries. WP-4 implements these fully."""

import json
from typing import Any


def find_requirements(model: Any) -> list:
    """Return all RequirementUsage elements in the model."""
    return model.query(
        where={
            "@type": "PrimitiveConstraint",
            "property": "@type",
            "operator": "=",
            "value": ["RequirementUsage"],
        }
    )


def find_allocations(model: Any) -> list:
    """Return all AllocationUsage elements in the model."""
    return model.query(
        where={
            "@type": "PrimitiveConstraint",
            "property": "@type",
            "operator": "=",
            "value": ["AllocationUsage"],
        }
    )


def get_satisfy_relationships(model: Any) -> list[dict]:
    """Return all SatisfyRequirementUsage elements.

    D-001: model.query() returns zero SatisfyRequirementUsage elements.
    Workaround: extract from model.to_api_json() filtered by @type.
    When D-001 is resolved upstream, only this function changes.
    """
    api_json = model.to_api_json()
    elements = json.loads(api_json) if isinstance(api_json, str) else api_json
    if isinstance(elements, dict):
        elements = elements.get("elements", list(elements.values()))
    return [e for e in elements if e.get("@type") == "SatisfyRequirementUsage"]
