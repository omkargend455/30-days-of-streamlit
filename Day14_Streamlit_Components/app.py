import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html

st.title("Day 14 – Streamlit Components (Data Profiling)")

uploaded_file = st.file_uploader("Upload a CSV file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    profile = ProfileReport(df, explorative=True)

    st.subheader("Profiling Report")

    html(profile.to_html(), height=1000, scrolling=True)