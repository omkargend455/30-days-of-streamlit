# 📊 YouTube Analytics Dashboard (Day 4)

An interactive YouTube channel analytics dashboard built with **Streamlit**, **Pandas**, and **Plotly**.

---

## 🚀 Features

- **Aggregate Metrics Mode**:
  - 6-month vs 12-month baseline performance metrics (Views, Likes, RPM, Watch Duration, Engagement Ratio, etc.).
  - Color-coded delta styling (green for growth, red for decline).
  - First 30-day benchmark percentiles (20th percentile, median, 80th percentile).
- **Individual Video Analysis Mode**:
  - Audience breakdown by geography (USA, India, Other) and subscription status.
  - Cumulative 30-day view trajectory compared against channel benchmark curves.

---

## 📁 Required CSV Files

The dashboard requires three CSV files to be uploaded via the sidebar:

| Input Field | Expected File Name | Description |
|---|---|---|
| **Aggregated Metrics By Video** | `Aggregated_Metrics_By_Video.csv` | Summary metrics per video (views, watch time, RPM, impressions, etc.) |
| **Metrics By Country & Subscriber Status** | `Aggregated_Metrics_By_Country_And_Subscriber_Status.csv` | Viewer location combined with subscription status |
| **Video Performance Over Time** | `Video_Performance_Over_Time.csv` | Daily time-series view counts for published videos |

---

## 🧪 Quick Start / Trial Run with Existing Data

Sample data is already included directly in this directory for immediate testing:

1. **Start the app:**
   ```bash
   streamlit run app.py
   ```
2. **Upload the sample CSV files:**
   In the left sidebar file uploaders, drag and drop the corresponding CSVs located in `Day04_Dashboard/`:
   - `Aggregated_Metrics_By_Video.csv`
   - `Aggregated_Metrics_By_Country_And_Subscriber_Status.csv`
   - `Video_Performance_Over_Time.csv`

Once all 3 files are uploaded, the dashboard will render automatically.

---

## 🌐 Downloading Sample Data from GitHub

If you or your users are running the deployed Streamlit Cloud app and need sample CSVs to test:

1. Download the files from the repository:
   - [Aggregated_Metrics_By_Video.csv](https://raw.githubusercontent.com/omkargend455/30-days-of-streamlit/main/Day04_Dashboard/Aggregated_Metrics_By_Video.csv)
   - [Aggregated_Metrics_By_Country_And_Subscriber_Status.csv](https://raw.githubusercontent.com/omkargend455/30-days-of-streamlit/main/Day04_Dashboard/Aggregated_Metrics_By_Country_And_Subscriber_Status.csv)
   - [Video_Performance_Over_Time.csv](https://raw.githubusercontent.com/omkargend455/30-days-of-streamlit/main/Day04_Dashboard/Video_Performance_Over_Time.csv)
2. Right-click each link and select **Save Link As...** to download them locally.
3. Upload them to the deployed Streamlit app sidebar.

*(Original sample data source: [Ken Jee's YouTube Analytics Dataset](https://github.com/Playing-with-data/youtube-analytics))*

---

## 🛠️ How to Export Your Own Data from YouTube Studio

To analyze your own channel:

1. Go to [YouTube Studio](https://studio.youtube.com/) and navigate to **Analytics**.
2. Click **Advanced Mode** (top-right corner).
3. Export each required dataset:
   - **Video Metrics:**
     - Select the **Video** tab.
     - Set the date range (e.g., Lifetime or Last 365 Days).
     - Click the **Export** icon (top right) $\rightarrow$ **Comma-separated values (.csv)**.
   - **Country & Subscriber Breakdown:**
     - Select the **Geography** tab.
     - Add a secondary dimension: select **Subscription status**.
     - Click **Export** $\rightarrow$ **CSV**.
   - **Performance Over Time:**
     - Select the time-series date view under Advanced Mode.
     - Click **Export** $\rightarrow$ **CSV**.
4. Rename and upload the exported files to the dashboard.
