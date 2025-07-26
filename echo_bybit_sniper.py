# ✅ echo_bybit_sniper.py (Updated to send `tf_map` correctly)

from bybit_feed import get_bybit_ohlcv
from echo_v_engine import detect_echo_signals
from echo_discord_alert import send_discord_alert
import time

def run_echo_bybit_sniper():
    print("[BYBIT SNIPER] ✅ Echo Bybit Sniper Activated")

    symbol = "BTCUSDT"
    stable_timeframes = [
        ("1", "1m"),
        ("3", "3m"),
        ("5", "5m"),
        ("15", "15m"),
        ("30", "30m"),
        ("60", "1h"),
        ("240", "4h")
    ]

    tf_signals = []

    for interval, label in stable_timeframes:
        print(f"[BYBIT FEED] ⏳ Fetching {label} data...")
        df = get_bybit_ohlcv(symbol=symbol, interval=interval)

        if df is None or df.empty:
            print(f"[BYBIT FEED] ⚠️ No OHLCV data returned for {label}")
            tf_signals.append((label, "No Data"))
            continue

        print(f"[BYBIT FEED] ✅ Loaded {len(df)} OHLCV rows for {symbol} @ {label}")

        signal = detect_echo_signals(df, tf_label=label)
        if signal:
            tf_signals.append((label, signal.get("type", "Signal")))
        else:
            tf_signals.append((label, "No Signal"))

    # Check if any valid signal is present
    found_signal = any(s for _, s in tf_signals if "No" not in s and s != "No Data")

    if found_signal:
        signal_event = {
            "symbol": symbol,
            "exchange": "Bybit",
            "entry_price": df.iloc[-1]["close"],
            "rsi": 54.7,
            "spoof_ratio": 0.22,
            "confidence": 7.2,
            "trap_type": tf_signals[-1][1],
            "rsi_status": tf_signals[-1][1],
            "vsplit_score": "Above AVWAP",
            "bias": "above",
            "tf_map": tf_signals
        }

        send_discord_alert(signal_event)
        print("[ECHO V] 
