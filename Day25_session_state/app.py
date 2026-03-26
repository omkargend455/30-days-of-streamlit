import streamlit as st

st.title("Day 25 – Session State 🔁")

# ------------------------------
# Initialize session state
# ------------------------------
if "lbs" not in st.session_state:
    st.session_state.lbs = 0.0

if "kg" not in st.session_state:
    st.session_state.kg = 0.0


# ------------------------------
# Conversion functions
# ------------------------------
def lbs_to_kg():
    st.session_state.kg = st.session_state.lbs / 2.2046

def kg_to_lbs():
    st.session_state.lbs = st.session_state.kg * 2.2046


# ------------------------------
# UI
# ------------------------------
st.header("Input")

col1, col2 = st.columns(2)

with col1:
    st.number_input(
        "Pounds",
        key="lbs",
        on_change=lbs_to_kg
    )

with col2:
    st.number_input(
        "Kilograms",
        key="kg",
        on_change=kg_to_lbs
    )


# ------------------------------
# Output
# ------------------------------
st.header("Output")

st.write("Session State:")
st.json(st.session_state)


# ------------------------------
# Reset button
# ------------------------------
if st.button("Reset"):
    st.session_state.lbs = 0.0
    st.session_state.kg = 0.0