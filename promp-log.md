# Data cleaning and validation pipeline
_Exported on 05/02/2026 at 19:48:07 GMT+8 from Cursor (2.4.27)_

---

**User**

Build a data cleaning and validation pipeline that processes raw scraped data into clean, structured output.

By completing this assignment, you will:
- Implement data cleaning functions
- Create validation rules for data quality
- Handle missing and malformed data
- Generate quality metrics reports


Requirements
1. Data Cleaning 
Implement cleaning functions that:
- Remove extra whitespace and HTML artifacts
- Normalize text encoding
- Standardize date formats to ISO format
- Handle special characters appropriately

2. Data Validation 
Implement validation that:
- Checks for required fields (title, content, url)
- Validates URL format
- Checks content length minimums
- Flags invalid records with reasons

3. Quality Report 
Generate a report showing:
- Total records processed
- Valid vs. invalid counts
- Completeness percentage per field
- Common validation failures

Deliverables
Submit your repo url from Github containing:

1. `cleaner.py`- Data cleaning implementation 
2. `validator.py` - Validation implementation 
3. `sample_data.json` - Sample input data 
4. `cleaned_output.json` - Cleaned output
5. `quality_report.txt` - Generated quality report
6. `README.md` - Brief documentation (1 page max)
7. `prompt-log.md` - Your AI-assisted development process

Grading Rubric
Criterion	Points	Description
Data Cleaning	40	Working cleaning functions, handles edge cases
Data Validation	40	Comprehensive validation, clear error messages
Quality Report & Prompt Log	20	Insightful metrics plus documented AI-assisted process
Total: 100 points (5% of course grade)

Can you make the raw data based on the data cleaning and validation requirements above in json format.

---

**Cursor**


Creating sample raw JSON data that exercises the data-cleaning and validation pipeline.



I created `sample_data.json` with 16 raw records that cover your cleaning and validation needs.

### Records for data cleaning

| Scenario | Records |
|----------|---------|
| Extra whitespace | 1 (title), 3 (spacing), 15 (whitespace around fields) |
| HTML artifacts | 2 (`<p>`, `<strong>`, `<br/>`, `&nbsp;`, `&#8220;`, `<script>`) |
| Non-ISO dates | 2 (`Jan 15, 2024`), 3 (`15/01/2024`), 8 (`1/4/2024`), 12 (`yesterday`), 14 (`12/25/2024`) |
| Special characters | 5 (café, naïve, 日本語, © ® ™, em-dash) |
| HTML entities | 2, 16 (`&amp;`, `&lt;`, `&gt;`, `&quot;`, `&#39;`) |

### Records for validation

| Scenario | Records |
|----------|---------|
| Valid records | 1, 5, 10 |
| Missing required fields | 6 (empty URL), 7 (empty title), 11 (no title) |
| Invalid URL format | 8 (`not-a-valid-url`), 9 (`www.example.com` without protocol) |
| Content too short | 4 (`"Short"`) |
| Null/empty values | 13 (`content` and `author` null) |

### Record summary

- **1** – Valid, but with extra spaces and ISO date  
- **2** – HTML and date format issues  
- **3** – Extra spaces and DD/MM/YYYY date  
- **4** – Content below minimum length  
- **5** – Special characters and mixed encodings  
- **6** – Empty URL  
- **7** – Empty title  
- **8** – Invalid URL format  
- **9** – URL without protocol  
- **10** – Fully valid record  
- **11** – Missing title field  
- **12** – Invalid date string  
- **13** – Null content  
- **14** – US date format (MM/DD/YYYY)  
- **15** – Whitespace around many fields  
- **16** – HTML entities  

You can use this file to drive `cleaner.py`, `validator.py`, and the quality report.

---

**User**

Using @sample_data.json,
1. Data Cleaning 
Implement cleaning functions that:
- Remove extra whitespace and HTML artifacts
- Normalize text encoding
- Standardize date formats to ISO format
- Handle special characters appropriately
include the code in cleaner.py file.

---

**Cursor**


Implemented `cleaner.py` with the requested cleaning behavior. Summary:

### Functions

| Function | Purpose |
|----------|---------|
| `clean_whitespace()` | Trims leading/trailing spaces and collapses runs of whitespace into a single space |
| `remove_html_artifacts()` | Strips HTML tags (`<p>`, `<strong>`, `<script>`, etc.) and decodes entities (`&nbsp;`, `&#8220;`, `&amp;`) |
| `normalize_encoding()` | Removes BOM, null bytes, and normalizes Unicode to NFC |
| `handle_special_characters()` | Replaces em-dash/en-dash with ASCII dashes, strips control characters, keeps valid Unicode |
| `clean_text()` | Runs the full text pipeline (HTML → encoding → special chars → whitespace) |
| `parse_date()` | Parses multiple date formats and returns ISO `YYYY-MM-DD` (or `None` if unparseable) |
| `clean_record()` | Cleans a single record, including title, content, author, url, date |
| `clean_records()` | Cleans a list of records |

### Supported date formats

- `2024-01-15`, `2024-03-10T14:30:00`, `2024-02-05T09:00:00Z`
- `15/01/2024` (DD/MM/YYYY)
- `12/25/2024`, `1/4/2024` (MM/DD/YYYY)
- `Jan 15, 2024`, `Feb 5, 2024`

Unparseable values (e.g. `"yesterday"`) produce `None`.

### Usage

```python
from cleaner import clean_records

with open("sample_data.json") as f:
    import json
    records = json.load(f)
cleaned = clean_records(records)
```

---

**User**

Using @sample_data.json,
2. Data Validation
Implement validation that:
- Checks for required fields (title, content, url)
- Validates URL format
- Checks content length minimums
- Flags invalid records with reasons
include the code in validator.py.

---

**Cursor**


`validator.py` includes the requested validation logic. Summary:

### Functions

| Function | Purpose |
|----------|---------|
| `validate_required_fields()` | Ensures `title`, `content`, and `url` exist and are non-empty |
| `validate_url_format()` | Checks `http://` or `https://` scheme and a valid host |
| `validate_content_length()` | Enforces a minimum content length (default 20 chars) |
| `validate_record()` | Runs all checks and returns `(is_valid, reasons)` |
| `validate_records()` | Validates a list and returns per-record results |
| `split_valid_invalid()` | Splits results into valid records and invalid results with reasons |

### Validation rules

- **Required fields**: `title`, `content`, `url` must be present and non-empty (no null/whitespace)
- **URL format**: Must use `http://` or `https://` and have a host (e.g. `not-a-valid-url`, `www.example.com` without protocol are rejected)
- **Content length**: At least 20 characters (configurable via `min_content_length`)

### Example failure messages

- `"missing required field: title"`
- `"empty required field: url"`
- `"url must start with http:// or https://"`
- `"url has no host"`
- `"content too short (min 20 chars, got 5)"`

### Usage

```python
from validator import validate_records, split_valid_invalid

with open("sample_data.json") as f:
    import json
    records = json.load(f)

results = validate_records(records)
valid_records, invalid_results = split_valid_invalid(results)

for inv in invalid_results:
    print(f"Record {inv['index']}: {inv['reasons']}")
```

---

**User**

Using @sample_data.json 
3. Quality Report 
Generate a report showing:
- Total records processed
- Valid vs. invalid counts
- Completeness percentage per field
- Common validation failures

include the code in quality_report.py.

---

**Cursor**


`quality_report.py` is implemented and run successfully. Here’s what it does:

### Functions

| Function | Purpose |
|----------|---------|
| `compute_completeness()` | Computes % of records with a non-empty value per field |
| `compute_common_failures()` | Counts validation reasons and sorts them by frequency |
| `generate_report()` | Cleans data, validates, builds report, and can save to a file |
| `main()` | Loads `sample_data.json`, generates report, writes `quality_report.txt` |

### Report contents

1. **Records processed**: Total count, valid and invalid counts, valid rate (%).
2. **Completeness per field**: Percentage of records with non-empty values for `title`, `content`, `url`, `date`, `author`.
3. **Common validation failures**: Validation reasons with counts, ordered by frequency.

### Flow

1. Load `sample_data.json`
2. Clean records with `clean_records()`
3. Validate records with `validate_records()`
4. Compute completeness and failure stats
5. Format and write the report to `quality_report.txt`

### Usage

```bash
python quality_report.py
```

The report is both printed and saved to `quality_report.txt`. On the sample data, it reports 16 records, 9 valid and 7 invalid (56.2% valid rate), with completeness and failure breakdowns.

---

**User**

create a main_dev.py file that runs the cleaner.py, validator.py, and quantity_report.py and generates a cleaned output of the sample_data.json in the file cleaned_output.json and a qualiy_report.txt.

---

**Cursor**


`main_dev.py` is in place and running correctly. It does the following:

1. **Load** `sample_data.json`
2. **Clean** records with `clean_records` from `cleaner.py`
3. **Validate** with `validate_records` from `validator.py`
4. **Write valid records** to `cleaned_output.json` (9 records)
5. **Generate quality report** and save it to `quality_report.txt`

### Usage

```bash
python main_dev.py
```

### Output files

- **cleaned_output.json** – Only valid, cleaned records (title, content, url, date, author with whitespace and HTML removed, dates normalized)
- **quality_report.txt** – Quality report with total/valid/invalid counts, completeness per field, and common validation failures

