"""
Quality report generator for scraped data pipeline.
Shows total records, valid/invalid counts, completeness per field, common validation failures.
"""

import json
from collections import Counter

from cleaner import clean_records
from validator import validate_records


FIELDS = ("title", "content", "url", "date", "author")


def _is_complete(value) -> bool:
    """True if field has a non-empty value."""
    if value is None:
        return False
    if not isinstance(value, str):
        return True
    return bool(value.strip())


def compute_completeness(records: list[dict]) -> dict[str, float]:
    """Compute completeness percentage per field."""
    total = len(records)
    if total == 0:
        return {f: 0.0 for f in FIELDS}
    counts = {}
    for field in FIELDS:
        complete = sum(1 for r in records if _is_complete(r.get(field)))
        counts[field] = round(100.0 * complete / total, 1)
    return counts


def compute_common_failures(invalid_results: list[dict]) -> list[tuple[str, int]]:
    """Count validation failure reasons and return sorted by frequency (desc)."""
    all_reasons = []
    for r in invalid_results:
        all_reasons.extend(r["reasons"])
    counts = Counter(all_reasons)
    return counts.most_common()


def generate_report(records: list[dict], output_path: str | None = None) -> str:
    """
    Load records, clean, validate, and generate quality report.
    If output_path given, writes report to file. Returns report text.
    """
    cleaned = clean_records(records)
    results = validate_records(cleaned)

    valid_count = sum(1 for r in results if r["valid"])
    invalid_count = len(results) - valid_count
    total = len(results)

    completeness = compute_completeness(cleaned)
    invalid_results = [r for r in results if not r["valid"]]
    common_failures = compute_common_failures(invalid_results)

    lines = [
        "=" * 50,
        "DATA QUALITY REPORT",
        "=" * 50,
        "",
        "RECORDS PROCESSED",
        "-" * 30,
        f"Total records: {total}",
        f"Valid: {valid_count}",
        f"Invalid: {invalid_count}",
        f"Valid rate: {round(100.0 * valid_count / total, 1) if total else 0}%",
        "",
        "COMPLETENESS PER FIELD",
        "-" * 30,
    ]

    for field in FIELDS:
        lines.append(f"  {field}: {completeness[field]}%")

    lines.extend([
        "",
        "COMMON VALIDATION FAILURES",
        "-" * 30,
    ])

    if common_failures:
        for reason, count in common_failures:
            lines.append(f"  [{count}x] {reason}")
    else:
        lines.append("  (none)")

    lines.append("")
    lines.append("=" * 50)

    report = "\n".join(lines)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)

    return report


def main():
    with open("sample_data.json", encoding="utf-8") as f:
        records = json.load(f)
    report = generate_report(records, "quality_report.txt")
    print(report)


if __name__ == "__main__":
    main()
