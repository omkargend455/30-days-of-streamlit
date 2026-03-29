import streamlit as st
import pandas as pd
import requests
from streamlit_tags import st_tags

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="Zero-Shot Classifier", layout="wide")

API_URL = "https://router.huggingface.co/hf-inference/models/valhalla/distilbart-mnli-12-3"

# 🔑 Replace with your token OR use secrets
API_KEY = st.secrets["API_KEY"]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ---------------- FUNCTION ---------------- #
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# ---------------- UI ---------------- #
st.title("🤗 Zero-Shot Text Classifier")

st.write("Classify multiple sentences into custom categories (no training required).")

# -------- LABEL INPUT -------- #
labels = st_tags(
    label="🏷️ Enter Labels (max 3)",
    text="Press enter to add",
    value=["Positive", "Negative"],
    suggestions=["Neutral", "Happy", "Angry", "Informational", "Transactional"],
    maxtags=3,
)

# -------- TEXT INPUT -------- #
text = st.text_area(
    "✍️ Enter sentences (one per line)",
    height=200,
    placeholder="Where is my order?\nI want to buy shoes\nHow to return item?"
)

# Process input
lines = list(dict.fromkeys(text.split("\n")))  # remove duplicates
lines = list(filter(None, lines))  # remove empty lines

# Limit for demo
MAX_LINES = 5
if len(lines) > MAX_LINES:
    st.warning(f"Only first {MAX_LINES} sentences will be processed")
    lines = lines[:MAX_LINES]

# ---------------- PROCESS ---------------- #
if st.button("🚀 Classify"):

    if not lines or not labels:
        st.warning("Please enter text and labels")

    else:
        results = []

        with st.spinner("Analyzing..."):

            for sentence in lines:
                output = query({
                    "inputs": sentence,
                    "parameters": {"candidate_labels": labels},
                    "options": {"wait_for_model": True}
                })

                # -------- RESPONSE HANDLING -------- #
                if isinstance(output, dict) and "labels" in output:
                    # Normal case
                    results.append({
                        "Text": sentence,
                        "Top Label": output["labels"][0],
                        "Confidence": round(output["scores"][0] * 100, 2)
                    })

                elif isinstance(output, list) and len(output) > 0:
                    # Sometimes returns list
                    first = output[0]
                    results.append({
                        "Text": sentence,
                        "Top Label": first.get("label", "Unknown"),
                        "Confidence": round(first.get("score", 0) * 100, 2)
                    })

                elif isinstance(output, dict) and "error" in output:
                    # API error
                    results.append({
                        "Text": sentence,
                        "Top Label": output["error"],
                        "Confidence": 0
                    })

                else:
                    # Unexpected response
                    results.append({
                        "Text": sentence,
                        "Top Label": "Unexpected response",
                        "Confidence": 0
                    })

        # Convert to DataFrame
        df = pd.DataFrame(results)

        # ---------------- OUTPUT ---------------- #
        st.subheader("📊 Results")
        st.dataframe(df, use_container_width=True)

        # ---------------- DOWNLOAD ---------------- #
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            data=csv,
            file_name="results.csv",
            mime="text/csv"
        )