from pathlib import Path
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data(path: str):
    file_path = Path(path)

    # авто-определение разделителя
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except:
        df = pd.read_csv(file_path, encoding="cp1251", sep=";")

    # очистка колонок
    df.columns = df.columns.str.strip()

    # очистка значений
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("\xa0", " ")
                .str.strip()
            )

    meta = {
        "file_name": file_path.name,
        "rows": df.shape[0],
        "cols": df.shape[1],
    }

    return df, meta