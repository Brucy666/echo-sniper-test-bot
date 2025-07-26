# echo_v_engine.py (Multi-Timeframe + Divergence + Echo Grid)

import pandas as pd
import numpy as np

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def detect_echo_signals(df: pd.DataFrame, tf_label: str):
    if df is None or df.empty or len(df) < 20:
        print(f"[ECHO V] ❌ Not enough data for {tf_label}")
        return None

    df = df.copy()
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df["rsi"] = calculate_rsi(df["close"])
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    # Echo Sync-Up Signal
    echo_signal = None
    if prev["rsi"] < 50 and latest["rsi"] > 50 and latest["rsi"] > prev["rsi"]:
        echo_signal = {
            "timeframe": tf_label,
            "type": "Echo Sync Up",
            "rsi": round(latest["rsi"], 2),
            "price": float(latest["close"]),
            "rsi_status": "Echo Sync Up"
        }
        print(f"[ECHO V] ✅ Echo Sync Up detected on {tf_label}")

    # Hidden Bearish Divergence: price high, RSI lower
    price_highs = df["close"].rolling(10).max()
    rsi_highs = df["rsi"].rolling(10).max()
    
    if (
        df["close"].iloc[-1] >= price_highs.iloc[-2] and
        df["rsi"].iloc[-1] < df["rsi"].iloc[-2] and
        df["rsi"].iloc[-1] < rsi_highs.iloc[-2]
    ):
        echo_signal = {
            "timeframe": tf_label,
            "type": "Hidden Bearish Div",
            "rsi": round(latest["rsi"], 2),
            "price": float(latest["close"]),
            "rsi_status": "Hidden Bear Div"
        }
        print(f"[ECHO V] 🟥 Hidden Bearish Divergence on {tf_label}")

    # Hidden Bullish Divergence: price low, RSI higher
    price_lows = df["close"].rolling(10).min()
    rsi_lows = df["rsi"].rolling(10).min()

    if (
        df["close"].iloc[-1] <= price_lows.iloc[-2] and
        df["rsi"].iloc[-1] > df["rsi"].iloc[-2] and
        df["rsi"].iloc[-1] > rsi_lows.iloc[-2]
    ):
        echo_signal = {
            "timeframe": tf_label,
            "type": "Hidden Bullish Div",
            "rsi": round(latest["rsi"], 2),
            "price": float(latest["close"]),
            "rsi_status": "Hidden Bull Div"
        }
        print(f"[ECHO V] 🟩 Hidden Bullish Divergence on {tf_label}")

    return echo_signal

def build_echo_grid(rsi_value: float) -> str:
    if rsi_value > 60:
        return "⬆️ Rising"
    elif rsi_value < 40:
        return "⬇️ Falling"
    else:
        return "➖ Neutral"
