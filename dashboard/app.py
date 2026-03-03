import sys
import os
import time
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from scipy.fft import fft

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(layout="wide")
st.title("🌌 Real-Time Cosmic Ray Monitoring System")

# ---------- Initialize Data ----------

if "data" not in st.session_state:
    timestamps = pd.date_range(
        start=pd.Timestamp.now(),
        periods=200,
        freq="s"   # FIXED (lowercase s)
    )

    counts = 1500 + np.random.normal(0, 20, 200)
    pressure = 1010 + np.random.normal(0, 2, 200)

    st.session_state.data = pd.DataFrame({
        "timestamp": timestamps,
        "counts": counts,
        "pressure": pressure
    })

# ---------- Simulate Live Data ----------

new_row = pd.DataFrame({
    "timestamp": [pd.Timestamp.now()],
    "counts": [1500 + np.random.normal(0, 20)],
    "pressure": [1010 + np.random.normal(0, 2)]
})

st.session_state.data = pd.concat(
    [st.session_state.data, new_row]
).tail(300)

df = st.session_state.data.copy()

# ---------- Processing ----------

df["rolling_mean"] = df["counts"].rolling(20).mean()
df["rolling_std"] = df["counts"].rolling(20).std()

mean = df["counts"].mean()
std = df["counts"].std()
df["z_score"] = (df["counts"] - mean) / std
df["anomaly"] = np.abs(df["z_score"]) > 3

df["pressure_corrected"] = df["counts"] * (
    df["pressure"].mean() / df["pressure"]
)

fft_values = np.abs(fft(df["counts"].fillna(0)))

# ---------- Layout ----------

col1, col2 = st.columns(2)

# 1 Raw Counts
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df["timestamp"], y=df["counts"], mode="lines"))
fig1.update_layout(title="1️⃣ Raw Counts")
col1.plotly_chart(fig1, width="stretch")

# 2 Rolling Mean
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df["timestamp"], y=df["rolling_mean"], mode="lines"))
fig2.update_layout(title="2️⃣ Rolling Mean")
col2.plotly_chart(fig2, width="stretch")

# 3 Pressure Corrected
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df["timestamp"], y=df["pressure_corrected"], mode="lines"))
fig3.update_layout(title="3️⃣ Pressure Corrected Counts")
col1.plotly_chart(fig3, width="stretch")

# 4 Z-Score
fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=df["timestamp"], y=df["z_score"], mode="lines"))
fig4.update_layout(title="4️⃣ Z-Score")
col2.plotly_chart(fig4, width="stretch")

# 5 Anomalies
fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=df["timestamp"], y=df["counts"], mode="lines"))
anomalies = df[df["anomaly"]]
fig5.add_trace(go.Scatter(
    x=anomalies["timestamp"],
    y=anomalies["counts"],
    mode="markers"
))
fig5.update_layout(title="5️⃣ Anomaly Detection")
col1.plotly_chart(fig5, width="stretch")

# 6 Histogram
fig6 = go.Figure()
fig6.add_trace(go.Histogram(x=df["counts"]))
fig6.update_layout(title="6️⃣ Histogram of Counts")
col2.plotly_chart(fig6, width="stretch")

# 7 FFT Spectrum
fig7 = go.Figure()
fig7.add_trace(go.Scatter(y=fft_values))
fig7.update_layout(title="7️⃣ FFT Spectrum")
col1.plotly_chart(fig7, width="stretch")

# 8 Rolling Std Dev
fig8 = go.Figure()
fig8.add_trace(go.Scatter(x=df["timestamp"], y=df["rolling_std"], mode="lines"))
fig8.update_layout(title="8️⃣ Rolling Standard Deviation")
col2.plotly_chart(fig8, width="stretch")

# ---------- Controlled Auto Refresh ----------

time.sleep(2)
st.rerun()