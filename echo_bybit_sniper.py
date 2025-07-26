# echo_bybit_sniper.py (Final Echo V - Multi-TF Map Enabled)

from bybit_feed import get_bybit_ohlcv
from echo_v_engine import detect_echo_signals
from discord_alert import send_discord_alert
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
    latest_price = 0
    last_valid_signal = "No Signal"

    for interval, label in stable_timeframes:
        print(f"[BYBIT FEED] ⏳ Fetching {label} data...")
        df = get_bybit_ohlcv(symbol=symbol, interval=interval)

        if df is None or df.empty:
            print(f"[BYBIT FEED] ⚠️ No OHLCV data returned for {label}")
            tf_signals.append((label, "No Data"))
            continue

        print(f"[BYBIT FEED] ✅ Loaded {len(df)} OHLCV rows for {symbol} @ {label}")
        latest_price = df.iloc[-1]["close"]

        signal = detect_echo_signals(df, tf_label=label)
        if signal:
            signal_type = signal.get("type", "Signal")
            tf_signals.append((label, signal_type))
            last_valid_signal = signal_type
            print(f"[ECHO V] ✅ {signal_type} detected on {label}")
        else:
            tf_signals.append((label, "No Signal"))
            print(f"[ECHO V] ❌ No signal on {label}")

    # Alert trigger condition
    found_signal = any(s for _, s in tf_signals if "No" not in s and "Data" not in s)

    if found_signal:
        signal_event = {
            "symbol": symbol,
            "exchange": "Bybit",
            "entry_price": latest_price,
            "rsi": 54.7,
            "spoof_ratio": 0.22,
            "confidence": 7.2,
            "trap_type": last_valid_signal,
            "rsi_status": last_valid_signal,
            "vsplit_score": "Above AVWAP",
            "bias": "above",
            "tf_map": dict(tf_signals)
        }

        send_discord_alert(signal_event)
        print("[ECHO V] 🚀 Echo alert sent to Discord.")
    else:
        print("[ECHO V] ❌ No Echo signals detected on any timeframe.")

if __name__ == "__main__":
    while True:
        run_echo_bybit_sniper()
        print("[LOOP] 🕒 Sleeping 60 seconds...\n")
        time.sleep(60)
