# echo_bybit_sniper.py

from bybit_feed import get_bybit_ohlcv
from echo_v_engine import detect_echo_signals
from echo_discord_alert import send_discord_alert
import time

def run_echo_bybit_sniper():
    print("[BYBIT SNIPER] ✅ Echo Bybit Sniper Activated")

    symbol = "BTCUSDT"
    timeframes = [
        ("1", "1m"), ("3", "3m"), ("5", "5m"),
        ("15", "15m"), ("30", "30m"), ("60", "1h"), ("240", "4h")
    ]

    tf_map = {}
    active_signals = []

    for interval, label in timeframes:
        print(f"[BYBIT FEED] ⏳ Fetching {label} data...")
        df = get_bybit_ohlcv(symbol=symbol, interval=interval)

        if df is None or df.empty:
            print(f"[BYBIT FEED] ⚠️ No OHLCV data for {label}")
            tf_map[label] = "No Data"
            continue

        print(f"[BYBIT FEED] ✅ Loaded {len(df)} rows for {symbol} @ {label}")
        signal = detect_echo_signals(df, tf_label=label)

        if signal:
            tf_map[label] = signal.get("type", "Signal")
            active_signals.append(signal)
        else:
            tf_map[label] = "No Signal"

    if active_signals:
        latest_signal = active_signals[-1]
        alert = {
            "symbol": symbol,
            "exchange": "Bybit",
            "bias": "above",
            "rsi_status": latest_signal["type"],
            "trap_type": latest_signal["type"],
            "entry_price": latest_signal.get("price", 0),
            "spoof_ratio": 0.22,
            "confidence": 7.2,
            "vsplit_score": "Above AVWAP",
            "trigger_tf": latest_signal.get("timeframe", "N/A"),
            "tf_map": tf_map
        }
        send_discord_alert(alert)
        print("[ECHO V] 🚀 Echo alert sent.")
    else:
        print("[ECHO V] ❌ No Echo signals detected.")

if __name__ == "__main__":
    while True:
        run_echo_bybit_sniper()
        print("[LOOP] 💤 Sleeping 60s...\n")
        time.sleep(60)
