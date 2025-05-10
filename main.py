from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import os

app = FastAPI()

EXCEL_PATH = "data/capbudg.xls"

# Load and parse the Excel file at startup
def load_excel_tables():
    import pandas as pd
    import re

    xls = pd.ExcelFile(EXCEL_PATH)
    tables = {}

    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name, header=None)
        title_rows = []

        for idx in range(len(df) - 2):
            row = df.iloc[idx]
            next_rows = df.iloc[idx + 1:idx + 3]  # Look ahead 2 rows for structure
            non_empty_cells = row.dropna()

            if 1 <= len(non_empty_cells) <= 3:
                valid_titles = []
                for cell in non_empty_cells:
                    text = str(cell).strip()
                    if (
                        text.isupper()
                        and re.search(r"[A-Z]", text)
                        and not any(char.isdigit() for char in text)
                        and len(text.split()) <= 6
                    ):
                        valid_titles.append(text)

                if valid_titles:
                    # Now validate the structure below the title row
                    first_col = next_rows.iloc[:, 0].dropna().astype(str)
                    other_cols = next_rows.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")

                    if (
                        not first_col.empty
                        and other_cols.notna().sum().sum() >= 2  # At least 2 numeric values in next two rows
                    ):
                        title_rows.append((idx, valid_titles))

        # Extract tables
        for i in range(len(title_rows)):
            row_idx, table_names = title_rows[i]
            next_row_idx = title_rows[i + 1][0] if i + 1 < len(title_rows) else len(df)

            for name in table_names:
                cleaned_name = name.strip().title()
                if cleaned_name not in tables:
                    table_data = df.iloc[row_idx + 1:next_row_idx].dropna(how="all")
                    if not table_data.empty:
                        tables[cleaned_name] = table_data.reset_index(drop=True)

    return tables



tables_data = load_excel_tables()


@app.get("/list_tables")
def list_tables():
    return {"tables": list(tables_data.keys())}


@app.get("/get_table_details")
def get_table_details(table_name: str = Query(..., description="Name of the table to inspect")):
    if table_name not in tables_data:
        raise HTTPException(status_code=404, detail="Table not found")
    df = tables_data[table_name]
    row_names = df.iloc[:, 0].dropna().astype(str).tolist()
    return {
        "table_name": table_name,
        "row_names": row_names
    }


import math

@app.get("/row_sum")
def row_sum(
    table_name: str = Query(..., description="Name of the table"),
    row_name: str = Query(..., description="Name of the row to sum")
):
    # Check if the table exists
    if table_name not in tables_data:
        raise HTTPException(status_code=404, detail="Table not found")
    
    df = tables_data[table_name]
    
    # Ensure the first column is used for row names
    df.iloc[:, 0] = df.iloc[:, 0].astype(str)
    
    # Get the row using .loc for better readability and performance
    row = df.loc[df.iloc[:, 0] == row_name]
    
    # If row is empty, return an error
    if row.empty:
        raise HTTPException(status_code=404, detail="Row not found in the specified table")
    
    # Get all the values in that row (excluding the first column)
    raw_values = row.iloc[0, 1:]
    
    # Function to parse values into floats
    def parse_value(val):
        if isinstance(val, str):
            # Check if it's a percentage
            if '%' in val:
                try:
                    return float(val.strip().replace('%', ''))  # Remove '%' and convert to float
                except ValueError:
                    return None
            # Otherwise, attempt to directly convert to float
            try:
                return float(val)
            except ValueError:
                return None
        # Direct float conversion for non-string values
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    # Parse all values in the row
    parsed_values = [parse_value(v) for v in raw_values]
    
    # Filter out None or non-finite values (e.g., NaN, inf)
    safe_values = [v for v in parsed_values if v is not None and math.isfinite(v)]
    
    # Calculate the total sum
    total = sum(safe_values)

    return {
        "table_name": table_name,
        "row_name": row_name,
        "sum": float(total)
    }
