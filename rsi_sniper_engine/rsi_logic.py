# rsi_sniper_engine/rsi_logic.py

import pandas as pd
import numpy as np

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = -delta.clip(upper=0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def detect_rsi_divergence(df: pd.DataFrame, tf_label: str):
    if df is None or df.empty or len(df) < 30:
        print(f"[RSI LOGIC] ⚠️ Insufficient data for {tf_label}")
        return None

    df = df.copy()
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['rsi'] = calculate_rsi(df['close'])

    recent = df.iloc[-5:]
    latest = recent.iloc[-1]

    # Regular Bearish Divergence: Price Higher High, RSI Lower High
    if df['close'].iloc[-1] > df['close'].iloc[-5] and df['rsi'].iloc[-1] < df['rsi'].iloc[-5]:
        return {
            "signal": "Regular Bear Div",
            "rsi": round(df['rsi'].iloc[-1], 2),
            "price": round(df['close'].iloc[-1], 2),
            "timeframe": tf_label
        }

    # Hidden Bullish Divergence: Price Higher Low, RSI Lower Low
    if df['close'].iloc[-1] > df['close'].iloc[-3] and df['rsi'].iloc[-1] < df['rsi'].iloc[-3]:
        return {
            "signal": "Hidden Bull Div",
            "rsi": round(df['rsi'].iloc[-1], 2),
            "price": round(df['close'].iloc[-1], 2),
            "timeframe": tf_label
        }

    return None
