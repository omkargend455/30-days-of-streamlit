import streamlit as st
from datetime import time, datetime

st.header("st.slider")

# Ex 1

st.subheader("Slider")

age = st.slider("How old are you?", 0, 130, 25)
st.write("I'm", age , "years old")

# Ex 2
st.subheader("Range slider")

values = st.slider(
    "Select a range of values",
    0.0, 100.0, (25.0, 75.0))
st.write("Values:", values)