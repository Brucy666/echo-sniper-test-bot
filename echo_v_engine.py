# echo_v_engine.py (Upgraded with Echo Grid and Divergence Detection)

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
    if df is None or df.empty or len(df) < 20:
        print(f"[ECHO V] ❌ Not enough data for {tf_label}")
        return None

    df = df.copy()
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df["rsi"] = calculate_rsi(df["close"])

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    signal = None

    # Echo Sync-Up: RSI crosses 50 and rising
    if prev["rsi"] < 50 and latest["rsi"] > 50 and latest["rsi"] > prev["rsi"]:
        signal = {
            "timeframe": tf_label,
            "type": "Echo Sync Up",
            "rsi_status": "Above 50 Rising",
            "rsi": round(latest["rsi"], 2)
        }
        print(f"[ECHO V] ✅ Echo Sync Up detected on {tf_label}")

    # Hidden Bearish Divergence
    elif df["close"].iloc[-1] > df["close"].iloc[-4] and df["rsi"].iloc[-1] < df["rsi"].iloc[-4]:
        signal = {
            "timeframe": tf_label,
            "type": "Hidden Bear Div",
            "rsi_status": "Lower RSI on Higher High",
            "rsi": round(latest["rsi"], 2)
        }
        print(f"[ECHO V] 🟠 Hidden Bearish Div on {tf_label}")

    # Hidden Bullish Divergence
    elif df["close"].iloc[-1] < df["close"].iloc[-4] and df["rsi"].iloc[-1] > df["rsi"].iloc[-4]:
        signal = {
            "timeframe": tf_label,
            "type": "Hidden Bull Div",
            "rsi_status": "Higher RSI on Lower Low",
            "rsi": round(latest["rsi"], 2)
        }
        print(f"[ECHO V] 🟢 Hidden Bullish Div on {tf_label}")

    return signal

def build_echo_grid(results: list):
    if not results:
        return "None"

    summary = "\n🧭 **Multi-Timeframe Echo V**\n"
    for r in results:
        tf = r.get("timeframe", "N/A")
        typ = r.get("type", "-")
        rsi = r.get("rsi", "?")
        emoji = "🟢" if "Bull" in typ or "Sync" in typ else "🔴"
        summary += f"{emoji} `{tf}` → {typ} (RSI: {rsi})\n"
    return summary.strip()
