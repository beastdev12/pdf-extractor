import pdfplumber
from openpyxl import Workbook
import tabula
import pandas as pd
import os
import camelot



def process_pdf(pdf_path):
    file_path = f"{pdf_path.replace('.pdf', '')}"
    excel_path = f"{file_path}.xlsx"

    # Try using Camelot first
    try:
        tables = camelot.read_pdf(pdf_path, flavor='stream', pages='all', strip_text='\n', encoding='utf-8', table_areas=None, **{'strict': False})
    except Exception as e:
        print(f"Camelot failed with error: {e}")
        tables = []

    # Create a list to store DataFrames
    dfs = [table.df for table in tables]

    # If no tables were found, try using pdfplumber or tabula
    if not dfs:
        # Try using pdfplumber
        print("Attempting to extract tables using pdfplumber...")
        by_pdfplumber(pdf_path, excel_path)

        # Optionally, try using tabula
        # by_tabula(pdf_path, file_path)

        return excel_path  # Return if tables are extracted

    # Concatenate all DataFrames
    final_df = pd.concat(dfs)

    # Save the DataFrame to Excel
    final_df.to_excel(excel_path, index=False)

    return excel_path



def by_pdfplumber(pdf_path, excel_path):
    with pdfplumber.open(pdf_path) as pdf:
        workbook = Workbook()
        sheet = workbook.active
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table:
                    sheet.append(row)
        #workbook.save(excel_path)

def by_tabula(pdf_path, file_path):

    dfs = tabula.read_pdf(pdf_path, pages='all')
    tabula.convert_into(pdf_path, f"{file_path}.csv", output_format="csv", pages='all')
    df = pd.read_csv(f"{file_path}.csv")
    df.to_excel(f"{file_path}.xlsx")
    os.remove(pdf_path)
    os.remove(f"{file_path}.csv")
