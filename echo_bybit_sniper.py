# echo_bybit_sniper.py (Final Version for Echo V)

from bybit_feed import get_bybit_ohlcv
from echo_v_engine import detect_echo_signals
from discord_alert import send_discord_alert
import time


def run_echo_bybit_sniper():
    print("[BYBIT SNIPER] ✅ Echo Bybit Sniper Activated")

    symbol = "BTCUSDT"
    timeframes = [
        ("1", "1m"), ("3", "3m"), ("5", "5m"), ("12", "12m"),
        ("15", "15m"), ("24", "24m"), ("30", "30m"), ("60", "1h"), ("240", "4h")
    ]

    signals = []

    for tf, label in timeframes:
        print(f"[BYBIT FEED] ⏳ Fetching {label} data...")
        df = get_bybit_ohlcv(symbol=symbol, interval=tf)

        if df is None or df.empty:
            print(f"[BYBIT FEED] ⚠️ No OHLCV data returned for {label}")
            continue

        print(f"[BYBIT FEED] ✅ Loaded {len(df)} OHLCV rows for {symbol} @ {label}")

        result = detect_echo_signals(df, label)
        if result:
            print(f"[ECHO V] ✅ {result['type']} detected on {label}")
            signals.append(result)
        else:
            print(f"[ECHO V] ❌ No signal on {label}")

    if not signals:
        print("[ECHO V] ❌ No Echo signals detected on any timeframe.")
        return

    alert_event = {
        "symbol": symbol,
        "exchange": "Bybit",
        "entry_price": 0,
        "rsi": signals[0]["rsi"],
        "spoof_ratio": 0.22,
        "confidence": 7.2,
        "trap_type": signals[0]["type"],
        "rsi_status": signals[0]["type"],
        "vsplit_score": "Above AVWAP",
        "bias": "above",
        "multi_signals": signals,
    }

    send_discord_alert(alert_event)
    print("[ECHO V] 🚀 Echo alert sent to Discord.")


if __name__ == "__main__":
    while True:
        print("[LOOP] 🌀 Starting Echo Sniper Loop...")
        run_echo_bybit_sniper()
        print("[LOOP] ⏳ Sleeping 60 seconds...\n")
        time.sleep(60)
