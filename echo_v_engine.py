# echo_v_engine.py

import pandas as pd
import numpy as np

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def detect_echo_signals(df: pd.DataFrame, tf_label: str):
    """
    Detect echo signal for a given timeframe's OHLCV dataframe.
    Returns a signal dictionary if conditions are met, else None.
    """
    if df is None or df.empty or len(df) < 20:
        print(f"[ECHO V] ❌ Not enough data for {tf_label}")
        return None

    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df["rsi"] = calculate_rsi(df["close"])

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    signal = None

    # RSI sync condition (both above 50 and rising)
    if prev["rsi"] < 50 and latest["rsi"] > 50 and latest["rsi"] > prev["rsi"]:
        signal = {
            "timeframe": tf_label,
            "type": "Echo Sync Up",
            "rsi": round(latest["rsi"], 2),
            "rsi_status": "Echo Sync Up"
        }
        print(f"[ECHO V] ✅ Echo Sync Up detected on {tf_label}")

    return signal
