# echo_bybit_sniper.py (Multi-Timeframe Grid w/ Safe Alert)

from bybit_feed import get_bybit_ohlcv
from echo_v_engine import detect_echo_signals
from discord_alert import send_discord_alert
import time


def run_echo_bybit_sniper():
    print("[BYBIT SNIPER] ✅ Echo Bybit Sniper Activated")

    symbol = "BTCUSDT"
    timeframes = ["1", "3", "5", "12", "15", "24", "30", "60", "240"]

    for tf in timeframes:
        tf_label = f"{tf}m" if tf not in ["60", "240"] else ("1h" if tf == "60" else "4h")

        print(f"[BYBIT FEED] ⏳ Fetching {tf_label} data...")
        df = get_bybit_ohlcv(symbol=symbol, interval=tf)

        if df is None or df.empty:
            print(f"[BYBIT FEED] ⚠️ No OHLCV data returned for {tf_label}")
            continue

        print(f"[BYBIT FEED] ✅ Loaded {len(df)} OHLCV rows for {symbol} @ {tf_label}")

        signals = detect_echo_signals(df, tf_label=tf_label)

        if not signals:
            print(f"[ECHO V] ❌ No signal on {tf_label}")
            continue

        for signal in signals:
            print(f"[ECHO V] ✅ Echo {signal.get('rsi_status', '?')} detected on {tf_label}")

            # Safe defaults for missing alert fields
            safe_signal = {
                "symbol": symbol,
                "exchange": "Bybit",
                "entry_price": signal.get("entry_price", 0),
                "rsi": signal.get("rsi", 0),
                "spoof_ratio": signal.get("spoof_ratio", 0),
                "confidence": signal.get("confidence", 0),
                "trap_type": signal.get("trap_type", "Unknown"),
                "rsi_status": signal.get("rsi_status", "Unknown"),
                "vsplit_score": signal.get("vsplit_score", "Unknown"),
                "bias": signal.get("bias", "Unknown")
            }

            send_discord_alert(safe_signal)
            print(f"[ECHO V] 🚀 Alert sent for {tf_label}")


if __name__ == "__main__":
    while True:
        run_echo_bybit_sniper()
        print("[LOOP] ⏳ Sleeping 60 seconds...\n")
        time.sleep(60)
