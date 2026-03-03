import sys
import os
import time
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import serial
from scipy.fft import fft

# CONFIGURE YOUR COM PORT HERE
COM_PORT = "COM5"      # <-- CHANGE THIS
BAUD_RATE = 9600       # <-- Confirm with device manual

st.set_page_config(layout="wide")
st.title("🌌 Real-Time Cosmic Ray Monitoring (USB Connected)")

# ---------- Initialize Serial ----------

@st.cache_resource
def init_serial():
    return serial.Serial(COM_PORT, BAUD_RATE, timeout=1)

try:
    ser = init_serial()
except Exception as e:
    st.error(f"Could not open serial port: {e}")
    st.stop()

# ---------- Initialize Session Data ----------

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["timestamp", "counts"]
    )

# ---------- Read From USB ----------

try:
    line = ser.readline().decode("utf-8").strip()

    if line:
        # If format is "COUNT:1523", modify parsing here
        count_value = float(line)

        new_row = pd.DataFrame({
            "timestamp": [pd.Timestamp.now()],
            "counts": [count_value]
        })

        st.session_state.data = pd.concat(
            [st.session_state.data, new_row]
        ).tail(500)

except Exception:
    pass  # Ignore corrupted serial reads

df = st.session_state.data.copy()

# ---------- Processing ----------

if not df.empty:

    df["rolling_mean"] = df["counts"].rolling(20).mean()
    df["rolling_std"] = df["counts"].rolling(20).std()

    mean = df["counts"].mean()
    std = df["counts"].std()
    df["z_score"] = (df["counts"] - mean) / std
    df["anomaly"] = np.abs(df["z_score"]) > 3

    fft_values = np.abs(fft(df["counts"].fillna(0)))

    col1, col2 = st.columns(2)

    # 1 Raw
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df["timestamp"], y=df["counts"], mode="lines"))
    fig1.update_layout(title="1️⃣ Raw Counts")
    col1.plotly_chart(fig1, width="stretch")

    # 2 Rolling Mean
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["timestamp"], y=df["rolling_mean"], mode="lines"))
    fig2.update_layout(title="2️⃣ Rolling Mean")
    col2.plotly_chart(fig2, width="stretch")

    # 3 Z-score
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df["timestamp"], y=df["z_score"], mode="lines"))
    fig3.update_layout(title="3️⃣ Z-Score")
    col1.plotly_chart(fig3, width="stretch")

    # 4 Anomalies
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=df["timestamp"], y=df["counts"], mode="lines"))
    anomalies = df[df["anomaly"]]
    fig4.add_trace(go.Scatter(
        x=anomalies["timestamp"],
        y=anomalies["counts"],
        mode="markers"
    ))
    fig4.update_layout(title="4️⃣ Anomaly Detection")
    col2.plotly_chart(fig4, width="stretch")

    # 5 Histogram
    fig5 = go.Figure()
    fig5.add_trace(go.Histogram(x=df["counts"]))
    fig5.update_layout(title="5️⃣ Histogram")
    col1.plotly_chart(fig5, width="stretch")

    # 6 FFT
    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(y=fft_values))
    fig6.update_layout(title="6️⃣ FFT Spectrum")
    col2.plotly_chart(fig6, width="stretch")

    # 7 Rolling Std
    fig7 = go.Figure()
    fig7.add_trace(go.Scatter(x=df["timestamp"], y=df["rolling_std"], mode="lines"))
    fig7.update_layout(title="7️⃣ Rolling Std Dev")
    col1.plotly_chart(fig7, width="stretch")

    # 8 Count Rate (per minute estimate)
    if len(df) > 60:
        rate = df["counts"].tail(60).mean()
    else:
        rate = df["counts"].mean()

    st.metric("8️⃣ Estimated Count Rate (Last 60 samples)", f"{rate:.2f}")

else:
    st.info("Waiting for detector data...")

# ---------- Refresh ----------

time.sleep(1)
st.rerun()