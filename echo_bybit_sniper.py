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
        print(f"[BYBIT FEED] 📡 Fetching {tf_label} data...")

        df = get_bybit_ohlcv(symbol=symbol, interval=tf)

        if df is None or df.empty:
            print(f"[BYBIT FEED] ⚠️ No data returned for {tf_label}")
            continue

        print(f"[BYBIT FEED] ✅ Loaded {len(df)} OHLCV rows for {symbol} @ {tf_label}")

        # Run Echo detection
        signal = detect_echo_signals(df, tf_label)
        if signal:
            print(f"[ECHO] 🟢 Signal detected on {tf_label}: {signal['rsi_status']}")
            signal["symbol"] = symbol
            signal["exchange"] = "Bybit"
            signal["entry_price"] = df.iloc[-1]["close"]
            signal["tf"] = tf_label
            send_discord_alert(signal)
            echo_results.append(signal)
        else:
            print(f"[ECHO] ⚪ No signal on {tf_label}")

    if not echo_results:
        print("[ECHO] ❌ No Echo signals detected on any timeframe.")


if __name__ == "__main__":
    while True:
        run_echo_bybit_sniper()
        print("[LOOP] ⏳ Sleeping 60 seconds...\n")
        time.sleep(60)
