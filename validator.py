"""
Data validation for scraped records.
Checks required fields, URL format, content length. Flags invalid records with reasons.
"""

import re
from urllib.parse import urlparse
from typing import Any


MIN_CONTENT_LENGTH = 20
REQUIRED_FIELDS = ("title", "content", "url")
URL_SCHEMES = ("http", "https")


def _is_empty(value: Any) -> bool:
    """True if value is None, empty string, or whitespace-only."""
    if value is None:
        return True
    if not isinstance(value, str):
        return True
    return not value.strip()


def validate_required_fields(record: dict) -> list[str]:
    """Check that required fields (title, content, url) exist and are non-empty."""
    reasons = []
    for field in REQUIRED_FIELDS:
        if field not in record:
            reasons.append(f"missing required field: {field}")
        elif _is_empty(record[field]):
            reasons.append(f"empty required field: {field}")
    return reasons


def validate_url_format(url: Any) -> list[str]:
    """Validate URL has http/https scheme and valid structure."""
    reasons = []
    if url is None:
        return ["url is null"]
    s = str(url).strip()
    if not s:
        return ["url is empty"]
    try:
        parsed = urlparse(s)
    except Exception:
        reasons.append("url is malformed")
        return reasons
    if parsed.scheme not in URL_SCHEMES:
        reasons.append("url must start with http:// or https://")
    if not parsed.netloc:
        reasons.append("url has no host")
    return reasons


def validate_content_length(content: Any, min_len: int = MIN_CONTENT_LENGTH) -> list[str]:
    """Check content meets minimum length."""
    reasons = []
    if content is None:
        return [f"content is null"]
    s = str(content).strip()
    if len(s) < min_len:
        reasons.append(f"content too short (min {min_len} chars, got {len(s)})")
    return reasons


def validate_record(record: dict, min_content_length: int = MIN_CONTENT_LENGTH) -> tuple[bool, list[str]]:
    """
    Validate a single record. Returns (is_valid, list of failure reasons).
    """
    reasons = []

    reasons.extend(validate_required_fields(record))
    reasons.extend(validate_content_length(record.get("content"), min_content_length))

    url = record.get("url")
    if url is not None and not _is_empty(url):
        reasons.extend(validate_url_format(url))

    is_valid = len(reasons) == 0
    return is_valid, reasons


def validate_records(records: list[dict], min_content_length: int = MIN_CONTENT_LENGTH) -> list[dict]:
    """
    Validate records. Returns list of validation results:
    [{"record": record, "valid": bool, "reasons": [...], "index": int}, ...]
    """
    results = []
    for i, record in enumerate(records):
        is_valid, reasons = validate_record(record, min_content_length)
        results.append({
            "record": record,
            "valid": is_valid,
            "reasons": reasons,
            "index": i,
        })
    return results


def split_valid_invalid(results: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Split validation results into valid and invalid lists.
    Returns (valid_records, invalid_results_with_reasons).
    """
    valid = [r["record"] for r in results if r["valid"]]
    invalid = [r for r in results if not r["valid"]]
    return valid, invalid
