import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Day 24 – Streamlit Caching 🚀")

# ------------------------------
# Cached function
# ------------------------------
@st.cache_data
def load_data_cached():
    time.sleep(2)  # simulate slow task
    df = pd.DataFrame(
        np.random.rand(1000000, 5),
        columns=["A", "B", "C", "D", "E"]
    )
    return df


# ------------------------------
# Non-cached function
# ------------------------------
def load_data_normal():
    time.sleep(2)  # simulate slow task
    df = pd.DataFrame(
        np.random.rand(1000000, 5),
        columns=["A", "B", "C", "D", "E"]
    )
    return df


# ------------------------------
# Using cache
# ------------------------------
st.subheader("⚡ Using Cache")

start = time.time()
df1 = load_data_cached()
end = time.time()

st.write(df1.head())
st.success(f"Time taken: {end - start:.2f} seconds")


# ------------------------------
# Without cache
# ------------------------------
st.subheader("🐢 Without Cache")

start = time.time()
df2 = load_data_normal()
end = time.time()

st.write(df2.head())
st.warning(f"Time taken: {end - start:.2f} seconds")