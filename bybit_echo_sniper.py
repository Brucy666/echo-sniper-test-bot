# bybit_echo_sniper.py
from bybit_feed import get_bybit_ohlcv
from echo_v_engine import detect_echo_vsplit
from discord_alert import send_discord_alert
from datetime import datetime
import pandas as pd

TIMEFRAMES = ["1h", "4h"]

def run_bybit_echo_sniper():
    print("[ECHO 🟣] Starting Bybit Echo Sniper...")

    tf_results = []

    for tf in TIMEFRAMES:
        print(f"[ECHO] Fetching {tf} data...")
        df = get_bybit_ohlcv("BTCUSDT", tf)
        if df is None or len(df) < 30:
            print(f"[ECHO] Skipping {tf}, not enough data.")
            continue

        result = detect_echo_vsplit(df)
        tf_results.append((tf, result))

    # Select strongest signal
    best = max(tf_results, key=lambda x: x[1]["strength"], default=None)

    if not best or best[1]["strength"] < 2.0:
        print("[ECHO] No valid Echo trap found.")
        return

    tf, signal = best
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    trap = {
        "symbol": "BTC/USDT",
        "exchange": "Bybit",
        "timestamp": timestamp,
        "entry_price": df["close"].iloc[-1],
        "score": signal["strength"],
        "confidence": signal["strength"],
        "trap_type": "Echo V Trap",
        "rsi_status": signal["status"],
        "vsplit_score": tf,
        "macro_vsplit": [],
        "macro_biases": []
    }

    print("[ECHO] Triggered Echo Signal:", trap)
    send_discord_alert(trap)

# Manual test
if __name__ == "__main__":
    run_bybit_echo_sniper()
