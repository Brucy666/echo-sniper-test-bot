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
        print(f"[BYBIT FEED] ⏳ Fetching {tf_label} data...")

        df = get_bybit_ohlcv(symbol=symbol, interval=tf)

        if df is None or df.empty:
            print(f"[BYBIT FEED] ⚠️ No OHLCV data returned for {tf_label}")
            continue

        print(f"[BYBIT FEED] ✅ Loaded {len(df)} OHLCV rows for {symbol} @ {tf_label}")

        signal = detect_echo_signals(df, tf_label)
        if signal:
            echo_results.append(signal)
        else:
            print(f"[ECHO V] ❌ No signal on {tf_label}")

    # If we got any echo signal, send the strongest (or latest)
    if echo_results:
        latest_signal = echo_results[-1]  # Could enhance with priority scoring later

        alert = {
            "symbol": symbol,
            "exchange": "Bybit",
            "entry_price": df.iloc[-1]["close"],
            "rsi": latest_signal.get("rsi", 50),
            "spoof_ratio": 0.18,  # Sim placeholder
            "confidence": 7.5,    # Sim placeholder
            "trap_type": "RSI Split",  # Sim placeholder
            "rsi_status": latest_signal.get("type", "Echo"),
            "vsplit_score": "Above AVWAP",  # Sim placeholder
            "bias": "above"
        }

        send_discord_alert(alert)
        print("[ECHO V] 🚀 Echo alert sent to Discord")
    else:
        print("[ECHO V] ❌ No Echo signals detected on any timeframe.")


if __name__ == "__main__":
    while True:
        run_echo_bybit_sniper()
        print("[LOOP] ⏳ Sleeping 60 seconds...\n")
        time.sleep(60)
