# utils/export.py

import pandas as pd

def export_to_csv(df: pd.DataFrame, filename: str):
    """
    Export a DataFrame to a CSV file.

    Parameters:
    - df (pd.DataFrame): The DataFrame to export.
    - filename (str): The filename for the exported CSV file.
    """
    df.to_csv(filename, index=False)
