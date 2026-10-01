from pathlib import Path
import pandas as pd


def load_and_prepare_data(file_path: str | Path) -> pd.DataFrame:
    """
    Load coffee sales data from CSV and add derived date fields.
    """
    df = pd.read_csv(file_path)

    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.quarter

    return df
