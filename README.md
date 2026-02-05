# Djoenaidi-Damario-Tanael---Week-3---Assignment-1
## Data Cleaning and Validation Pipeline

A Python pipeline that processes raw scraped data into clean, structured output with validation and quality reporting.

## Overview

The pipeline loads JSON records, cleans text fields, validates required fields and formats, and produces:
- **cleaned_output.json** – valid records only, with normalized text and dates
- **quality_report.txt** – metrics on totals, completeness, and common validation failures

## Files

| File | Purpose |
|------|---------|
| `cleaner.py` | Removes whitespace/HTML, normalizes encoding, standardizes dates, handles special characters |
| `validator.py` | Checks required fields (title, content, url), URL format, content length minimums |
| `quality_report.py` | Generates quality metrics report |
| `main_dev.py` | Runs the full pipeline and writes output files |
| `sample_data.json` | Sample raw input data |

## Usage

```bash
python main_dev.py
```

Requires Python 3.10+. No external dependencies beyond the standard library.

## Pipeline Flow

1. **Load** – Read `sample_data.json`
2. **Clean** – Strip HTML tags and entities, collapse whitespace, normalize Unicode, convert dates to ISO (YYYY-MM-DD)
3. **Validate** – Ensure title/content/url exist and are non-empty; URL has http(s) scheme; content meets minimum length (20 chars)
4. **Output** – Write valid cleaned records to `cleaned_output.json`; generate `quality_report.txt`

## Data Cleaning

- Extra whitespace collapsed; leading/trailing spaces removed
- HTML tags and entities (`&nbsp;`, `&#8220;`, etc.) stripped and decoded
- Dates parsed from multiple formats (DD/MM/YYYY, MM/DD/YYYY, Jan 15 2024, ISO) → normalized to YYYY-MM-DD
- Em-dash/en-dash normalized; control characters removed

## Validation Rules

- **Required fields**: title, content, url (must be present and non-empty)
- **URL**: must start with `http://` or `https://` and have a host
- **Content**: minimum 20 characters

Invalid records are excluded from the output and listed in the quality report with failure reasons.
