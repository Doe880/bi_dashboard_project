import streamlit as st
from components.auth import check_auth
from utils.data_loader import load_data
from utils.metrics import build_summary_metrics
from components.filters import render_sidebar_filters, apply_filters
from components.charts import render_kpi_cards, render_main_chart

st.set_page_config(layout="wide")

check_auth()

df, meta = load_data("data/GeekBrains – Pivot.csv")

st.title("📊 BI Панель (Pivot данные)")

filters = render_sidebar_filters(df)
df_filtered = apply_filters(df, filters)

summary = build_summary_metrics(df_filtered)

render_kpi_cards(summary)

render_main_chart(df_filtered)

st.subheader("Данные")
st.dataframe(df_filtered, use_container_width=True)