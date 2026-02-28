import streamlit as st

st.header("st.button")

if st.button("Hello there"):
    st.write("Heyyyy")

else:
    st.write("Bye!")