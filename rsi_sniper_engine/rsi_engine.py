# rsi_sniper_engine/rsi_engine.py

import pandas as pd

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def detect_rsi_signal(df: pd.DataFrame) -> str or None:
    rsi = df["rsi"]
    if len(rsi) < 2:
        return None

    latest = rsi.iloc[-1]
    prev = rsi.iloc[-2]

    if prev < 30 and latest > 30:
        return "RSI Bull Reversal"
    elif prev > 70 and latest < 70:
        return "RSI Bear Reversal"
    else:
        return None
