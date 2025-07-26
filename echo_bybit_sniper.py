# echo_bybit_sniper.py (Full Echo Grid + Discord Summary)

from bybit_feed import get_bybit_ohlcv
from echo_v_engine import detect_echo_signals
from discord_alert import send_discord_alert
import time


def run_echo_bybit_sniper():
    print("[BYBIT SNIPER] ✅ Echo Bybit Sniper Activated")

    symbol = "BTCUSDT"
    timeframes = ["1", "3", "5", "12", "15", "24", "30", "60", "240"]
    tf_labels = {
        "1": "1m", "3": "3m", "5": "5m", "12": "12m", "15": "15m",
        "24": "24m", "30": "30m", "60": "1h", "240": "4h"
    }

    echo_signals = []
    rsi_status_summary = {}

    for tf in timeframes:
        tf_label = tf_labels[tf]
        print(f"[BYBIT FEED] ⏳ Fetching {tf_label} data...")

        df = get_bybit_ohlcv(symbol=symbol, interval=tf)
        if df is None or df.empty:
            print(f"[BYBIT FEED] ⚠️ No OHLCV data returned for {tf_label}")
            rsi_status_summary[tf_label] = "❓"
            continue

        print(f"[BYBIT FEED] ✅ Loaded {len(df)} OHLCV rows for {symbol} @ {tf_label}")

        signal = detect_echo_signals(df, tf_label)
        if signal:
            echo_signals.append(signal)
            status = signal.get("type", "Unknown")
            if "Bear" in status:
                rsi_status_summary[tf_label] = "🔻"
            elif "Bull" in status:
                rsi_status_summary[tf_label] = "🔼"
            elif "Sync" in status:
                rsi_status_summary[tf_label] = "⏸"
            else:
                rsi_status_summary[tf_label] = "✅"
        else:
            print(f"[ECHO V] ❌ No signal on {tf_label}")
            rsi_status_summary[tf_label] = "❌"

    if echo_signals:
        signal = echo_signals[-1]
        summary_lines = [f"{tf}: {status}" for tf, status in rsi_status_summary.items()]
        summary_text = "\n".join(summary_lines)

        signal_event = {
            "symbol": symbol,
            "exchange": "Bybit",
            "entry_price": signal.get("price", 0),
            "rsi": signal.get("rsi", 0),
            "spoof_ratio": 0.22,
            "confidence": 7.2,
            "trap_type": signal.get("type", "Unknown"),
            "rsi_status": signal.get("type", "N/A"),
            "vsplit_score": "Above AVWAP",
            "bias": "above",
            "tf_summary": summary_text
        }

        send_discord_alert(signal_event)
        print("[ECHO V] 🚀 Echo alert sent to Discord.")
    else:
        print("[ECHO V] ❌ No Echo signals detected on any timeframe.")


if __name__ == "__main__":
    while True:
        run_echo_bybit_sniper()
        print("[LOOP] ⏳ Sleeping 60 seconds...\n")
        time.sleep(60)
