import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")

# ======================================================
# Helper functions
# ======================================================
def style_negative(v):
    try:
        return "color:red;" if v < 0 else None
    except:
        return None

def style_positive(v):
    try:
        return "color:green;" if v > 0 else None
    except:
        return None

def audience_simple(code):
    if code == "US":
        return "USA"
    elif code == "IN":
        return "India"
    else:
        return "Other"

# ======================================================
# Sidebar – Upload CSV files
# ======================================================
st.sidebar.header("📂 Upload YouTube CSV Files")

file_agg = st.sidebar.file_uploader(
    "Aggregated Metrics By Video", type="csv"
)

file_country = st.sidebar.file_uploader(
    "Metrics By Country & Subscriber Status", type="csv"
)

file_time = st.sidebar.file_uploader(
    "Video Performance Over Time", type="csv"
)

if not all([file_agg, file_country, file_time]):
    st.info("⬅️ Upload all required CSV files to continue")
    st.stop()

# ======================================================
# Load & clean data (CACHE)
# ======================================================
@st.cache_data
def load_data(file_agg, file_country, file_time):

    # -------- Aggregated video metrics --------
    df_agg = pd.read_csv(file_agg).iloc[1:, :]

    df_agg.columns = [
        'Video','Video title','Video publish time','Comments added','Shares',
        'Dislikes','Likes','Subscribers lost','Subscribers gained',
        'RPM(USD)','CPM(USD)','Average % viewed','Average view duration',
        'Views','Watch time (hours)','Subscribers',
        'Your estimated revenue (USD)','Impressions','Impressions ctr(%)'
    ]

    # Mixed date formats FIX
    df_agg['Video publish time'] = pd.to_datetime(
        df_agg['Video publish time'],
        format="mixed",
        errors="coerce"
    )

    # Duration → seconds
    df_agg['Average view duration'] = pd.to_timedelta(
        df_agg['Average view duration'],
        errors="coerce"
    )

    df_agg['Avg_duration_sec'] = df_agg['Average view duration'].dt.total_seconds()

    # Derived metrics
    df_agg['Engagement_ratio'] = (
        (df_agg['Comments added'] + df_agg['Shares'] +
         df_agg['Dislikes'] + df_agg['Likes']) /
        df_agg['Views'].replace(0, np.nan)
    )

    df_agg['Views / sub gained'] = (
        df_agg['Views'] / df_agg['Subscribers gained'].replace(0, np.nan)
    )

    # -------- Country / subscriber data --------
    df_country = pd.read_csv(file_country)

    # -------- Time series data --------
    df_time = pd.read_csv(file_time)

    df_time['Date'] = pd.to_datetime(
        df_time['Date'],
        format="mixed",
        errors="coerce"
    )

    return df_agg, df_country, df_time


df_agg, df_country, df_time = load_data(
    file_agg, file_country, file_time
)

# ======================================================
# Merge time-series with publish dates
# ======================================================
df_time = df_time.merge(
    df_agg[['Video', 'Video publish time']],
    left_on="External Video ID",
    right_on="Video",
    how="left"
)

df_time['days_published'] = (
    df_time['Date'] - df_time['Video publish time']
).dt.days

# ======================================================
# Benchmark curves (first 30 days)
# ======================================================
last_12mo = df_agg['Video publish time'].max() - pd.DateOffset(months=12)

df_time_yr = df_time[df_time['Video publish time'] >= last_12mo]

views_days = (
    df_time_yr
    .pivot_table(
        index='days_published',
        values='Views',
        aggfunc=[
            np.median,
            lambda x: np.percentile(x, 80),
            lambda x: np.percentile(x, 20)
        ]
    )
    .reset_index()
)

views_days.columns = [
    'days_published',
    'median_views',
    '80pct_views',
    '20pct_views'
]

views_days = views_days[views_days['days_published'].between(0, 30)]

views_cumulative = views_days.copy()
views_cumulative.iloc[:, 1:] = views_cumulative.iloc[:, 1:].cumsum()

# ======================================================
# UI MODE
# ======================================================
mode = st.sidebar.selectbox(
    "Dashboard Mode",
    ["Aggregate Metrics", "Individual Video Analysis"]
)

# ======================================================
# Aggregate Metrics
# ======================================================
if mode == "Aggregate Metrics":
    st.title("📊 YouTube Aggregate Metrics")

    metrics = [
        'Views','Likes','Subscribers','Shares','Comments added',
        'RPM(USD)','Average % viewed','Avg_duration_sec',
        'Engagement_ratio','Views / sub gained'
    ]

    date_6 = df_agg['Video publish time'].max() - pd.DateOffset(months=6)
    date_12 = df_agg['Video publish time'].max() - pd.DateOffset(months=12)

    med_6 = df_agg[df_agg['Video publish time'] >= date_6][metrics].median()
    med_12 = df_agg[df_agg['Video publish time'] >= date_12][metrics].median()

    cols = st.columns(5)
    for i, m in enumerate(metrics):
        delta = (med_6[m] - med_12[m]) / med_12[m]
        cols[i % 5].metric(m, round(med_6[m], 2), f"{delta:.2%}")

    df_diff = df_agg.copy()
    df_diff[metrics] = (df_diff[metrics] - med_12) / med_12

    df_display = df_diff[['Video title'] + metrics].copy()

    numeric_cols = df_display.select_dtypes(include=[np.number]).columns

    st.dataframe(
        df_display
        .style
        .applymap(style_negative, subset=numeric_cols)
        .applymap(style_positive, subset=numeric_cols)
        .format("{:.1%}", subset=numeric_cols),
        use_container_width=True
    )

# ======================================================
# Individual Video Analysis
# ======================================================
else:
    st.title("🎬 Individual Video Analysis")

    video = st.selectbox(
        "Select Video",
        df_agg['Video title'].dropna().unique()
    )

    # Audience breakdown
    sub_df = df_country[df_country['Video Title'] == video].copy()
    sub_df['Country'] = sub_df['Country Code'].apply(audience_simple)

    fig1 = px.bar(
        sub_df,
        x="Views",
        y="Is Subscribed",
        color="Country",
        orientation="h",
        title="Audience Breakdown"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Time comparison
    video_time = df_time[df_time['Video title'] == video]
    first_30 = video_time[video_time['days_published'].between(0, 30)]

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=views_cumulative['days_published'],
        y=views_cumulative['20pct_views'],
        name="20th Percentile",
        line=dict(dash="dash")
    ))

    fig2.add_trace(go.Scatter(
        x=views_cumulative['days_published'],
        y=views_cumulative['median_views'],
        name="Median",
        line=dict(dash="dash")
    ))

    fig2.add_trace(go.Scatter(
        x=views_cumulative['days_published'],
        y=views_cumulative['80pct_views'],
        name="80th Percentile",
        line=dict(dash="dash")
    ))

    fig2.add_trace(go.Scatter(
        x=first_30['days_published'],
        y=first_30['Views'].cumsum(),
        name="Current Video",
        line=dict(width=4)
    ))

    fig2.update_layout(
        title="First 30 Days View Comparison",
        xaxis_title="Days Since Published",
        yaxis_title="Cumulative Views"
    )

    st.plotly_chart(fig2, use_container_width=True)