import streamlit as st
import pandas as pd


def render_sidebar_filters(df: pd.DataFrame):
    st.sidebar.header("Фильтры")

    filters = {}

    for col in df.columns:
        if df[col].dtype == "object":
            values = df[col].dropna().unique().tolist()
            selected = st.sidebar.multiselect(col, values, default=values)
            filters[col] = selected

    return filters


def apply_filters(df: pd.DataFrame, filters: dict):
    filtered = df.copy()

    for col, values in filters.items():
        if values:
            filtered = filtered[filtered[col].isin(values)]

    return filtered