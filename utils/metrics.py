import pandas as pd


def build_summary_metrics(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include="number").columns

    totals = df[numeric_cols].sum().to_dict()

    return {
        "rows_total": len(df),
        "columns_total": len(df.columns),
        "totals": totals,
    }