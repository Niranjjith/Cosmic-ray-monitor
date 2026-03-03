## Real-Time Cosmic Ray Monitoring System

This project is a **Streamlit-based dashboard for real-time cosmic ray monitoring and analysis**.  
It currently simulates detector data (counts and pressure) and demonstrates a full processing and visualization
pipeline that can be adapted to **real hardware-connected detectors**.

The app:

- **Streams time-series data** for cosmic-ray count rates and atmospheric pressure.
- **Performs online processing**, including rolling statistics, pressure correction, and anomaly detection.
- **Visualizes data** in multiple synchronized Plotly charts.
- **Supports spectral analysis** using FFT to highlight periodic components in the count rate.

---

### Features

- **Simulated detector stream**
  - Generates realistic-looking counts around a nominal rate.
  - Adds pressure measurements for barometric corrections.
  - Maintains a sliding time window of recent data.

- **Data processing**
  - Rolling mean and standard deviation of counts.
  - Z-score calculation and **3σ anomaly detection**.
  - Pressure-corrected counts to reduce barometric effects.
  - FFT spectrum of the count-rate time series.

- **Interactive dashboard**
  - Built with **Streamlit** and **Plotly** for rich, web-based visualization.
  - Eight key panels:
    1. Raw counts vs. time  
    2. Rolling mean of counts  
    3. Pressure-corrected counts  
    4. Z-score vs. time  
    5. Anomaly markers on the count-rate series  
    6. Histogram of counts  
    7. FFT amplitude spectrum  
    8. Rolling standard deviation  
  - Auto-refreshes on a short interval to emulate real-time monitoring.

---

### Project Structure (key parts)

- `dashboard/app.py` – main Streamlit dashboard:
  - Simulated data generation.
  - Processing logic (rolling stats, z-scores, anomalies, FFT).
  - Layout and plots.
- `requirements.txt` – Python dependencies.
- `venv/` – optional local virtual environment (not required if you use your own).

---

### Requirements

- **Python**: 3.9+ recommended  
- **OS**: Windows, macOS, or Linux

Python packages (also listed in `requirements.txt`):

- `pandas`
- `numpy`
- `matplotlib`
- `streamlit`
- `plotly`
- `scipy`

---

### Setup

From the project root (`cosmic-ray-monitor`):

```bash
# Optionally, create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate  # On macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

If you already have a virtual environment (as in this repo), you can reuse it by activating it and skipping creation.

---

### Running the Dashboard

From the project root, run:

```bash
streamlit run dashboard/app.py
```

This will:

- Start a local Streamlit server.
- Open your browser (or give you a localhost URL) with the **Real-Time Cosmic Ray Monitoring System** dashboard.
- Continuously update the plots as new simulated data points are generated.

You can stop the server with `Ctrl+C` in the terminal.

---

### Customizing for Real Detectors

To connect to a real detector instead of simulated data:

- Replace the **simulated data block** in `dashboard/app.py` with code that:
  - Reads counts and (optionally) pressure from your data source (serial port, TCP, files, etc.).
  - Appends them into the `st.session_state.data` DataFrame with a `timestamp` column.
- Keep the column names `timestamp`, `counts`, and `pressure` (or update the processing code accordingly).

The rest of the processing, anomaly detection, and visualization pipeline can remain unchanged.

---

### Development Notes

- The app uses `st.rerun()` with a short `time.sleep` to implement a **controlled auto-refresh loop**.
- For production or long-run deployments, you may:
  - Tune the refresh interval for your detector sampling rate.
  - Add logging, alerting (e.g., email/webhook on anomalies), or persistence to disk/database.

---

### License

Specify the license of your choice here (for example, MIT, GPL, or proprietary). If you are unsure,
MIT is a common permissive option:

```text
MIT License – Copyright (c) 2026
```

