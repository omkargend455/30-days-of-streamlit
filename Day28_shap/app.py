import streamlit as st
from streamlit_shap import st_shap
import shap
import xgboost
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

st.set_page_config(layout="wide")

# ---------------- LOAD DATA ---------------- #
@st.cache_data
def load_data():
    X, y = shap.datasets.adult()
    y = pd.Series(y, name="Target")  # ✅ Convert to Pandas Series
    return X, y

# ---------------- LOAD MODEL ---------------- #
@st.cache_resource
def load_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    d_train = xgboost.DMatrix(X_train, label=y_train)
    d_test = xgboost.DMatrix(X_test, label=y_test)

    params = {
        "eta": 0.01,
        "objective": "binary:logistic",
        "subsample": 0.5,
        "base_score": float(np.mean(y_train)),
        "eval_metric": "logloss",
        "n_jobs": -1,
    }

    model = xgboost.train(
        params,
        d_train,
        num_boost_round=10,
        evals=[(d_test, "test")],
        verbose_eval=False
    )

    return model

# ---------------- UI ---------------- #
st.title("📊 SHAP Explainability Dashboard")

with st.expander("ℹ️ About"):
    st.write("This app explains ML predictions using SHAP values.")

# ---------------- DATA ---------------- #
st.header("📁 Dataset")

X, y = load_data()
X_display, y_display = shap.datasets.adult(display=True)

st.write("Shape of dataset:", X.shape)

with st.expander("View Features"):
    st.dataframe(X.head())

with st.expander("View Target"):
    st.dataframe(y.head())  # ✅ Now works perfectly

# ---------------- MODEL ---------------- #
st.header("🤖 Model Training")

model = load_model(X, y)
st.success("Model trained successfully!")

# ---------------- SHAP ---------------- #
st.header("🔍 SHAP Explainability")

explainer = shap.Explainer(model, X)
shap_values = explainer(X)

# -------- WATERFALL -------- #
with st.expander("📉 Waterfall Plot"):
    st_shap(shap.plots.waterfall(shap_values[0]), height=300)

# -------- BEESWARM -------- #
with st.expander("🐝 Beeswarm Plot"):
    st_shap(shap.plots.beeswarm(shap_values), height=300)

# -------- FORCE PLOT -------- #
explainer_tree = shap.TreeExplainer(model)
shap_vals = explainer_tree.shap_values(X)

with st.expander("⚡ Force Plot"):
    st.subheader("Single Prediction")
    st_shap(
        shap.force_plot(
            explainer_tree.expected_value,
            shap_vals[0, :],
            X_display.iloc[0, :]
        ),
        height=200
    )

    st.subheader("Multiple Predictions")
    st_shap(
        shap.force_plot(
            explainer_tree.expected_value,
            shap_vals[:100],
            X_display.iloc[:100]
        ),
        height=400
    )