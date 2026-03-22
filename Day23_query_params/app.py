import streamlit as st

st.title("Day 23 – Query Params (Interactive)")

# --- 1. Get current query params ---
params = st.query_params

# Default values
default_name = params.get("name", "Guest")
default_city = params.get("city", "Unknown")

# --- 2. User input ---
st.sidebar.header("Enter Details")

name = st.sidebar.text_input("Enter your name", default_name)
city = st.sidebar.text_input("Enter your city", default_city)

# --- 3. Update URL dynamically ---
st.query_params["name"] = name
st.query_params["city"] = city

# --- 4. Display output ---
st.subheader("Output")
st.write(f"Hello **{name}** from **{city}** 👋")

# --- 5. Show current URL state ---
st.subheader("Current URL Params")
st.write(dict(st.query_params))