from pathlib import Path
from typing import List
import fitz  # PyMuPDF
import pandas as pd
from schema import JBIEntry
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment

def extract_text_from_pdf(pdf_path: Path) -> str:
    with fitz.open(pdf_path) as doc:
        return "\n".join(page.get_text() for page in doc)

def save_results_to_excel(data, output_path: str):
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False)

    # Excel mit openpyxl laden und anpassen
    workbook = load_workbook(output_path)
    sheet = workbook.active

    # Spaltenbreite setzen und Zeilenumbruch aktivieren
    for i, col in enumerate(df.columns, 1):
        col_letter = get_column_letter(i)
        sheet.column_dimensions[col_letter].width = 40  # Spaltenbreite

        for cell in sheet[col_letter]:
            cell.alignment = Alignment(wrap_text=True, vertical="top")  # Zeilenumbruch + oben ausrichten

    workbook.save(output_path)