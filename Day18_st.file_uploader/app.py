import streamlit as st
import pandas as pd

st.title("Day 18 – File Uploader App 📁")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    # Preview
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # Shape
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Column selection
    st.subheader("📊 Select Column")
    column = st.selectbox("Choose column", df.columns)

    # Basic stats
    st.subheader("📈 Statistics")
    st.write(df.describe())

    # Simple visualization
    st.subheader("📉 Chart")
    st.bar_chart(df[column])

else:
    st.info("👆 Upload a CSV file to begin")