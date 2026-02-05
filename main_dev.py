"""
Main pipeline: load sample data, clean, validate, write cleaned output and quality report.
"""

import json

from cleaner import clean_records
from validator import validate_records, split_valid_invalid
from quality_report import generate_report


def main():
    with open("sample_data.json", encoding="utf-8") as f:
        records = json.load(f)

    cleaned = clean_records(records)
    results = validate_records(cleaned)
    valid_records, _ = split_valid_invalid(results)

    with open("cleaned_output.json", "w", encoding="utf-8") as f:
        json.dump(valid_records, f, indent=2, ensure_ascii=False)

    generate_report(records, "quality_report.txt")


if __name__ == "__main__":
    main()
