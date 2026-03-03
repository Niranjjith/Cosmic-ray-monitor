def apply_rolling_average(df, window=30):
    df["rolling_mean"] = df["counts"].rolling(window=window).mean()
    return df


def pressure_correction(df):
    if "pressure" in df.columns:
        mean_pressure = df["pressure"].mean()
        df["pressure_corrected"] = df["counts"] * (mean_pressure / df["pressure"])
    return df