"""Formatted output helpers. WP-5 completes format_coverage_table and format_signoff_document."""

from typing import Any


def format_diagnostics(diags: list) -> str:
    """Format a list of opensysml diagnostic objects as a readable string."""
    if not diags:
        return "(no diagnostics)"
    lines = []
    for d in diags:
        sev = getattr(d, "severity", "?")
        msg = getattr(d, "message", str(d))
        line = getattr(d, "start_line", None)
        loc = f" (line {line})" if line is not None else ""
        lines.append(f"  [{sev}]{loc} {msg}")
    return "\n".join(lines)


def format_coverage_table(reqs: list, satisfies: list) -> str:
    """Return a text table of requirements vs. satisfy relationships. WP-5."""
    raise NotImplementedError("format_coverage_table: implement in WP-5")


def format_signoff_document(model: Any, records: list, meta: dict) -> str:
    """Assemble the sign-off document from model data and review records. WP-5."""
    raise NotImplementedError("format_signoff_document: implement in WP-5")
