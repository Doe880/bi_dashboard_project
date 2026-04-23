import pandas as pd
import plotly.express as px
import streamlit as st


def render_kpi_cards(summary: dict):
    st.subheader("KPI")

    cols = st.columns(min(4, len(summary["totals"])))

    for i, (key, value) in enumerate(summary["totals"].items()):
        cols[i % len(cols)].metric(key, int(value))


def render_main_chart(df: pd.DataFrame):
    st.subheader("Основная визуализация")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        st.warning("Нет числовых колонок")
        return

    x_col = st.selectbox("Ось X", df.columns)
    y_col = st.selectbox("Ось Y", numeric_cols)

    fig = px.bar(df, x=x_col, y=y_col)
    st.plotly_chart(fig, use_container_width=True)