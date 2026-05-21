import pandas as pd
import plotly.express as px
import streamlit as st


def render_kpi_cards(summary: dict):
    st.subheader("KPI")

    totals = summary.get("totals", {})

    if not totals:
        st.info("Нет числовых показателей для KPI")
        return

    cols = st.columns(min(4, len(totals)))

    for i, (key, value) in enumerate(totals.items()):
        cols[i % len(cols)].metric(
            label=key,
            value=f"{value:,.0f}".replace(",", " ")
        )


def render_main_chart(df: pd.DataFrame):
    st.subheader("Основная визуализация")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    all_cols = df.columns.tolist()

    if df.empty:
        st.warning("Нет данных после применения фильтров")
        return

    if not numeric_cols:
        st.warning("Нет числовых колонок для построения графика")
        return

    chart_type = st.selectbox(
        "Тип графика",
        [
            "Столбчатый",
            "Линейный",
            "Круговая диаграмма",
            "Точечный",
        ],
    )

    x_col = st.selectbox("Ось X / категория", all_cols)
    y_col = st.selectbox("Ось Y / значение", numeric_cols)

    if chart_type == "Столбчатый":
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            text_auto=True,
            color_discrete_sequence=["#0071E3"],
        )

    elif chart_type == "Линейный":
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            markers=True,
            color_discrete_sequence=["#0071E3"],
        )

    elif chart_type == "Круговая диаграмма":
        pie_df = (
            df.groupby(x_col, as_index=False)[y_col]
            .sum()
            .sort_values(y_col, ascending=False)
        )

        fig = px.pie(
            pie_df,
            names=x_col,
            values=y_col,
            hole=0.45,
        )

    else:
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color_discrete_sequence=["#0071E3"],
        )

    fig.update_layout(
        height=460,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="#1D1D1F",
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E5E5E7",
            zeroline=False,
            tickformat="~s",
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
        ),
    )

    fig.update_traces(textfont_size=12)

    st.plotly_chart(fig, use_container_width=True)