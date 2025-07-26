# echo_bybit_sniper.py (Full Echo Grid)

from bybit_feed import get_bybit_ohlcv
from echo_v_engine import detect_echo_signals
from discord_alert import send_discord_alert
import time

def run_echo_bybit_sniper():
    print("[BYBIT SNIPER] ✅ Echo Bybit Sniper Activated")

    symbol = "BTCUSDT"
    timeframes = ["1", "3", "5", "12", "15", "24", "30", "60", "240"]  # 9 TFs total

    echo_results = []

    for tf in timeframes:
        tf_label = f"{tf}m" if tf not in ["60", "240"] else ("1h" if tf == "60" else "4h")
        print(f"[BYBIT FEED] 🔄 Fetching {tf_label} data...")

        df = get_bybit_ohlcv(symbol=symbol, interval=tf)
        if df is None or len(df) < 20:
            print(f"[BYBIT FEED] ⚠️ Skipping {tf_label}, not enough data.")
            continue

        echo = detect_echo_signals(df)
        if echo["status"] != "None":
            echo_results.append(f"{tf_label}: {echo['status']} ({echo['strength']})")

    if echo_results:
        signal = {
            "symbol": symbol,
            "exchange": "Bybit",
            "entry_price": round(float(df['close'].iloc[-1]), 2),
            "rsi": 0,
            "spoof_ratio": 0.0,
            "confidence": round(len(echo_results) * 1.5, 1),
            "trap_type": "Echo V Engine",
            "rsi_status": echo_results[0].split(": ")[1].split(" (")[0],
            "vsplit_score": f"{len(echo_results)} TFs active",
            "bias": "above" if "Bull" in echo_results[0] or "Up" in echo_results[0] else "below"
        }

        print("[ECHO 🔍] Signals detected:")
        for line in echo_results:
            print(f" → {line}")
        send_discord_alert(signal)
    else:
        print("[ECHO 🔍] No signals detected.")

if __name__ == "__main__":
    while True:
        run_echo_bybit_sniper()
        print("[LOOP] ⏳ Sleeping 60 seconds...\n")
        time.sleep(60)
