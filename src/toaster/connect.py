"""Connection lifecycle: open and close an OpenSysML session."""

from contextlib import contextmanager
from typing import Generator

import opensysml  # type: ignore[import]


@contextmanager
def opensysml_session(version: str = "v0.9.0") -> Generator:
    """Context manager that yields an open opensysml connection."""
    conn = opensysml.connect(version=version)
    try:
        yield conn
    finally:
        conn.close()
