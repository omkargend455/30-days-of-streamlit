import streamlit as st
import requests

st.title("🎯 Bored API App (Improved)")

# ------------------------------
# Sidebar input
# ------------------------------
st.sidebar.header("Choose Activity Type")

activity_type = st.sidebar.selectbox(
    "Type",
    ["education", "recreational", "social", "diy", "charity",
     "cooking", "relaxation", "music", "busywork"]
)

# ------------------------------
# Cached API call
# ------------------------------
@st.cache_data
def fetch_activity(activity_type):
    url = f"http://www.boredapi.com/api/activity?type={activity_type}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

data = fetch_activity(activity_type)

# ------------------------------
# Layout
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    with st.expander("📘 About"):
        st.write(
            "Feeling bored? This app suggests activities using the Bored API."
        )

with col2:
    with st.expander("📦 Raw JSON"):
        st.write(data)

# ------------------------------
# Output
# ------------------------------
if "error" in data:
    st.error("API failed. Try again.")
else:
    st.header("💡 Suggested Activity")
    st.success(data["activity"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Participants", data["participants"])

    with col2:
        st.metric("Type", data["type"].capitalize())

    with col3:
        st.metric("Price", data["price"])

# ------------------------------
# Refresh button
# ------------------------------
if st.button("🔄 Get Another Idea"):
    st.cache_data.clear()