# echo_bybit_sniper.py

from bybit_feed import get_bybit_ohlcv
from discord_alert import send_discord_alert
import time


def run_echo_bybit_sniper():
    print("[BYBIT SNIPER] 🧠 Echo Bybit Sniper Activated")

    # Example: fetch data from Bybit (symbol and timeframe are hardcoded for testing)
    try:
        df = get_bybit_ohlcv("BTC/USDT", "1h")
        if df is not None and not df.empty:
            print("[BYBIT SNIPER] ✅ Fetched 1H OHLCV data from Bybit")

            # Simulated test logic for now:
            event = {
                "symbol": "BTC/USDT",
                "exchange": "Bybit",
                "entry_price": df.iloc[-1]["close"],
                "rsi": 34.2,
                "spoof_ratio": 0.12,
                "trap_type": "RSI-V",
                "rsi_status": "V-Split",
                "vsplit_score": "1H: V-Wave",
                "confidence": 8.5,
                "bias": "above"
            }
            send_discord_alert(event)
        else:
            print("[BYBIT SNIPER] ⚠️ No data returned from Bybit feed")

    except Exception as e:
        print(f"[BYBIT SNIPER ERROR] {e}")


if __name__ == "__main__":
    while True:
        run_echo_bybit_sniper()
        time.sleep(60)
