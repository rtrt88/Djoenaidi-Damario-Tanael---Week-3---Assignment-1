# Djoenaidi-Damario-Tanael---Week-3---Assignment-1
A simple pipeline that turns raw scraped data (e.g. from CSV) into cleaned, validated records and a quality report.

What it does

Cleaning — Removes extra whitespace and HTML, normalizes encoding, standardizes dates, handles special characters.
Validation — Ensures required fields (title, content, url), valid URL format, and minimum content length.
Reporting — Produces validation and quality reports (valid/invalid counts, completeness, common failures).
Project layout

File	Purpose
cleaner.py	Data cleaning functions (whitespace, HTML, encoding, dates, special chars).
validator.py	Validation rules (required fields, URL format, content length).
csv_to_json.py	Converts bbc_news.csv → sample_data.json.
run_cleaning.py	Runs sample_data.json through cleaner → cleaned_output.json.
run_validation.py	Validates cleaned_output.json, writes validation_report.json.
generate_quality_report.py	Builds quality_report.txt (totals, valid/invalid, completeness, common failures).
Data flow

bbc_news.csv → csv_to_json.py → sample_data.json
sample_data.json → run_cleaning.py → cleaned_output.json
cleaned_output.json → run_validation.py → validation_report.json
cleaned_output.json → generate_quality_report.py → quality_report.txt
How to run

CSV → JSON
python csv_to_json.py
Reads bbc_news.csv, writes sample_data.json.

Clean
python run_cleaning.py
Cleans sample_data.json, writes cleaned_output.json.

Validate
python run_validation.py
Validates cleaned_output.json, writes validation_report.json.

Quality report
python generate_quality_report.py
Writes quality_report.txt (totals, valid/invalid, completeness per field, common validation failures).

Requirements

Python 3 with standard library only (re, html, unicodedata, datetime, urllib.parse, csv, json, collections).

Input data shape

Each record is a dict with at least:

title (text)
content (text)
url (valid URL string)
Optional date fields can be passed to the cleaner for ISO date standardization.
