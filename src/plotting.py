import matplotlib.pyplot as plt

def plot_time_series(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["counts"], label="Raw Counts")

    if "rolling_mean" in df.columns:
        plt.plot(df["timestamp"], df["rolling_mean"], label="Rolling Mean")

    if "anomaly" in df.columns:
        anomalies = df[df["anomaly"]]
        plt.scatter(anomalies["timestamp"],
                    anomalies["counts"],
                    color="red",
                    label="Anomaly")

    plt.xlabel("Time")
    plt.ylabel("Cosmic Ray Counts")
    plt.title("Cosmic Ray Intensity vs Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()