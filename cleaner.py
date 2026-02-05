"""
Data cleaning functions for scraped data.
Removes whitespace/HTML artifacts, normalizes encoding, standardizes dates, handles special characters.
"""

import html
import re
import unicodedata
from datetime import datetime
from typing import Any


def clean_whitespace(text: str) -> str:
    """Remove extra whitespace: strip edges and collapse runs of whitespace to single space."""
    if text is None or not isinstance(text, str):
        return ""
    return " ".join(text.split())


def remove_html_artifacts(text: str) -> str:
    """Remove HTML tags and decode HTML entities."""
    if text is None or not isinstance(text, str):
        return ""
    # Remove HTML tags
    no_tags = re.sub(r"<[^>]+>", " ", text)
    # Decode HTML entities
    decoded = html.unescape(no_tags)
    return decoded


def normalize_encoding(text: str) -> str:
    """Normalize text encoding: ensure valid UTF-8 and NFC normalization for consistent Unicode."""
    if text is None or not isinstance(text, str):
        return ""
    # Replace common encoding errors
    replacements = [
        ("\ufeff", ""),  # BOM
        ("\x00", ""),    # Null byte
    ]
    result = text
    for old, new in replacements:
        result = result.replace(old, new)
    # NFC normalization for consistent representation (e.g. é as single char)
    return unicodedata.normalize("NFC", result)


def handle_special_characters(text: str) -> str:
    """Handle special characters: normalize em-dash, strip control characters, preserve valid Unicode."""
    if text is None or not isinstance(text, str):
        return ""
    result = []
    for char in text:
        cat = unicodedata.category(char)
        if cat.startswith("C"):  # Control, format, surrogate
            if char in ("\n", "\r", "\t"):
                result.append(" ")
            continue
        if char == "—":  # Em-dash
            result.append(" - ")
        elif char == "–":  # En-dash
            result.append("-")
        else:
            result.append(char)
    return "".join(result)


def clean_text(text: str) -> str:
    """
    Full text cleaning: HTML removal, entity decode, whitespace, encoding, special chars.
    """
    if text is None or not isinstance(text, str):
        return ""
    t = remove_html_artifacts(text)
    t = normalize_encoding(t)
    t = handle_special_characters(t)
    t = clean_whitespace(t)
    return t


def parse_date(raw: Any) -> str | None:
    """
    Parse various date formats and return ISO format (YYYY-MM-DD) or None if unparseable.
    """
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None

    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%B %d, %Y",   # January 15, 2024
        "%b %d, %Y",   # Jan 15, 2024
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # Try flexible patterns
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if m:
        month, day, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= month <= 12 and 1 <= day <= 31:
            try:
                dt = datetime(year, month, day)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass

    return None


def clean_record(record: dict) -> dict:
    """
    Clean a single record. Returns a new dict with cleaned fields.
    Does not remove records; validation handles that.
    """
    out = {}
    for key, value in record.items():
        if key == "date":
            parsed = parse_date(value)
            out[key] = parsed if parsed else (str(value).strip() if value is not None else None)
        elif key in ("title", "content", "author") and value is not None:
            out[key] = clean_text(str(value))
        elif key == "url" and value is not None:
            out[key] = clean_whitespace(str(value))
        else:
            out[key] = value
    return out


def clean_records(records: list[dict]) -> list[dict]:
    """Clean a list of records."""
    return [clean_record(r) for r in records]

if __name__ == "__main__":
    print("Hello, World! This is the cleaner module. ")