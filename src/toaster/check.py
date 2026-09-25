"""API-level verification wrappers. WP-4 implements these fully."""

from typing import Any


def evaluate_satisfaction(model: Any, symbol_id: str | None = None, engine: str | None = None) -> list:
    """Evaluate all assert satisfy assertions in the model."""
    return model.verify_satisfaction(symbol_id=symbol_id, engine=engine)


def verify_constraint(model: Any, name: str, subject: str | None = None, engine: str = "check") -> Any:
    """Verify a named constraint on the model."""
    return model.verify_constraint(name, subject=subject, engine=engine)
