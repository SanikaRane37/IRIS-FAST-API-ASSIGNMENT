Sure! Below is a properly formatted version of the content you provided, using Markdown:

---

# IRIS-FAST-API-ASSIGNMENT

### Limitation Notice

Due to the current data extraction approach, if multiple tables are present on the same row or share overlapping row identifiers, the data may not be fetched or processed accurately. This limitation affects scenarios where visual layout merges or aligns different table contents horizontally, leading to ambiguous or incomplete row matching.

**Recommendation**: Ensure each table is structured independently and clearly separated to ensure accurate data retrieval.

### BASE URL

[http://localhost:9090/docs#/default/row\_sum\_row\_sum\_get](http://localhost:9090/docs#/default/row_sum_row_sum_get)

---

## Potential Improvements

### 1. Improved Excel File Parsing & Format Handling

* **Current Limitation**: The application is limited to `.xls` files, potentially excluding users with more modern `.xlsx` files.

* **Improvement**:

  * Consider auto-detecting file types, allowing the user to upload files without worrying about format compatibility.
  * Implement file validation to ensure that the uploaded file is a valid Excel format (or provide an option for CSV uploads as well).

### 2. Dynamic Table Detection and Flexible Parsing Logic

* **Current Limitation**: The application makes assumptions about table structure, like specific row lengths or numeric data following certain columns.

* **Improvement**:

  * Add more **dynamic detection algorithms** that can identify tables based on varied formats and user-defined patterns (e.g., headers in different columns).
  * Allow **customizable parsing rules** where users can specify which rows or columns should be considered as titles or data. This is especially helpful when working with inconsistent or unstructured tables.
  * Consider adding a **pre-processing step** that lets users inspect and adjust detected table structures before parsing, increasing flexibility.

---

## Missed Edge Cases

### 1. Empty or Corrupt Excel Files

* **Problem**: If an uploaded Excel file is empty, the current system doesn't return a user-friendly error message.

* **Solution**:

  * Detect when a file is empty and return a clear error message, such as **"Uploaded file is empty"**.
  * Handle **corrupt files** (e.g., incomplete or unsupported file formats) and notify users accordingly.

### 2. Non-Numeric Data in Rows Expected to Have Numbers

* **Problem**: The current implementation assumes that all values in a row (except the first column) should be numeric. Non-numeric data (e.g., text, special characters) may cause the summation to fail or return incorrect results.

* **Solution**:

  * Implement more **robust data parsing**, allowing text values (like "N/A" or "Error") to be ignored or flagged.
  * Handle **non-numeric cells** gracefully by skipping them or returning a specific error message.

### 3. Missing or Invalid Row Names

* **Problem**: If the row name specified by the user doesn't exist or is misspelled, the system will return a vague error without clarification.

* **Solution**:

  * Provide more specific error messages such as **"Row not found: \[row\_name]"** or suggest possible matches for rows when an exact match is not found.

### 4. Multiple Sheets in the Excel File

* **Problem**: The application assumes that all sheets are formatted the same way and processes them without distinguishing between sheets.

* **Solution**:

  * Add functionality to **select which sheet(s) to process** and ensure the user is informed if a sheet cannot be processed (e.g., missing table structures).

### 5. Inconsistent Row Structures

* **Problem**: The current approach assumes that all rows in a table follow the same structure.

* **Solution**:

  * Implement logic to detect **inconsistent row structures** and handle them, either by skipping or prompting users for clarification.

### 6. Malformed Table Names or Row Names

* **Problem**: If the table names or row names contain unexpected characters or formats (e.g., spaces or punctuation), they might not be parsed correctly.

* **Solution**:

  * Implement **sanitization** of input strings and allow for **case-insensitive matching** when searching for rows or tables.

### 7. Performance with Large Datasets

* **Problem**: Large Excel files may cause performance issues, particularly with extensive calculations or multiple table parsing.

* **Solution**:

  * Add **pagination** for large tables or provide options for **batch processing**. This will help prevent the server from being overwhelmed by massive datasets.

### 8. Handling Special Characters in Data

* **Problem**: Special characters like percentages (`%`), currency symbols (`$`), and commas (`,`) may not be parsed correctly and could lead to inaccurate results.

* **Solution**:

  * Implement global **data cleaning procedures** to remove or handle special characters during parsing. Ensure that such characters do not interfere with numeric calculations (e.g., handling percentages by converting to decimal form).

### 9. Data Privacy & Security

* **Problem**: The application does not currently provide any data security or privacy measures.

* **Solution**:

  * Ensure that uploaded files are processed securely.
  * Optionally, implement an **authentication system** to ensure that only authorized users can upload files or access specific endpoints.

### 10. Multiple Rows with the Same Name

* **Problem**: If there are multiple rows with the same name (due to inconsistent naming conventions), the current implementation might return incorrect results.

* **Solution**:

  * Provide clear **error handling** when duplicate rows are found or allow users to specify which row to process when there are multiple matches.


