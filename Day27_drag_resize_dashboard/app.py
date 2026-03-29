import streamlit as st
import json
from pathlib import Path

# Streamlit Elements imports
from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo

# Page setup
st.set_page_config(layout="wide")

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.title("📊 Streamlit Dashboard")
    st.write("Draggable & Resizable Dashboard Example")

    media_url = st.text_input(
        "Enter YouTube URL",
        value="https://www.youtube.com/watch?v=vIQQR_yq-8I"
    )

# ---------------- SESSION STATE ---------------- #
if "data" not in st.session_state:
    # Load default JSON data
    st.session_state.data = Path("Day27_drag_resize_dashboard/data.json").read_text()

# ---------------- DASHBOARD LAYOUT ---------------- #
layout = [
    dashboard.Item("editor", 0, 0, 6, 3),
    dashboard.Item("chart", 6, 0, 6, 3),
    dashboard.Item("media", 0, 3, 12, 4),
]

# ---------------- MAIN DASHBOARD ---------------- #
with elements("dashboard"):

    with dashboard.Grid(layout, draggableHandle=".drag"):

        # ----------- CODE EDITOR ----------- #
        with mui.Card(key="editor", sx={"display": "flex", "flexDirection": "column"}):
            mui.CardHeader(title="🧑‍💻 Data Editor", className="drag")

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                editor.Monaco(
                    defaultValue=st.session_state.data,
                    language="json",
                    onChange=lazy(sync("data"))  # Prevent rerun on each keystroke
                )

            with mui.CardActions:
                mui.Button("Apply Changes", onClick=sync())

        # ----------- CHART ----------- #
        with mui.Card(key="chart", sx={"display": "flex", "flexDirection": "column"}):
            mui.CardHeader(title="📈 Bump Chart", className="drag")

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                try:
                    data = json.loads(st.session_state.data)

                    nivo.Bump(
                        data=data,
                        colors={"scheme": "spectral"},
                        lineWidth=3,
                        activeLineWidth=6,
                        inactiveOpacity=0.15,
                        pointSize=10,
                        margin={"top": 40, "right": 100, "bottom": 40, "left": 60},
                    )
                except Exception as e:
                    st.error("Invalid JSON data!")

        # ----------- MEDIA PLAYER ----------- #
        with mui.Card(key="media", sx={"display": "flex", "flexDirection": "column"}):
            mui.CardHeader(title="🎥 Media Player", className="drag")

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                media.Player(
                    url=media_url,
                    width="100%",
                    height="100%",
                    controls=True
                )