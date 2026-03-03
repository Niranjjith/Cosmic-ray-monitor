import numpy as np
from scipy.fft import fft

def detect_anomalies(df, threshold=3):
    mean = df["counts"].mean()
    std = df["counts"].std()

    df["z_score"] = (df["counts"] - mean) / std
    df["anomaly"] = np.abs(df["z_score"]) > threshold

    return df


def compute_fft(df):
    counts = df["counts"].values
    fft_values = fft(counts)
    return np.abs(fft_values)