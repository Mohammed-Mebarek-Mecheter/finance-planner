# utils/pdf_export.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd

def export_to_pdf(df: pd.DataFrame, filename: str):
    """
    Export a DataFrame to a PDF file.

    Parameters:
    - df (pd.DataFrame): The DataFrame to export.
    - filename (str): The filename for the exported PDF file.
    """
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.drawString(30, height - 40, "Financial Report")
    c.drawString(30, height - 60, "Generated using Financial Planning App")

    col_width = width / len(df.columns)
    row_height = 20
    x_offset = 30
    y_offset = height - 80

    for col_num, column in enumerate(df.columns):
        c.drawString(x_offset + col_num * col_width, y_offset, column)

    for row_num, row in df.iterrows():
        for col_num, cell in enumerate(row):
            c.drawString(x_offset + col_num * col_width, y_offset - (row_num + 1) * row_height, str(cell))

    c.save()
