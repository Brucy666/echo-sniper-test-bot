# echo_bybit_sniper.py

from bybit_feed import get_bybit_ohlcv
from discord_alert import send_discord_alert
import time


def run_echo_bybit_sniper():
    print("[BYBIT SNIPER] ✅ Echo Bybit Sniper Activated")

    # Retrieve OHLCV data
    df = get_bybit_ohlcv(symbol="BTCUSDT", interval="60")  # 60 = 1 hour candles

    if df is None or df.empty:
        print("[BYBIT SNIPER] ⚠️ No data returned from Bybit feed")
        return

    # --- Echo analysis logic goes here ---
    # For now, we'll simulate a signal trigger for testing
    latest_candle = df.iloc[-1]
    price = latest_candle["close"]

    # Simulated signal
    signal_event = {
        "symbol": "BTCUSDT",
        "exchange": "Bybit",
        "entry_price": price,
        "rsi": 54.2,
        "spoof_ratio": 0.18,
        "confidence": 7.5,
        "trap_type": "RSI Split",
        "rsi_status": "Echo Sync Up",
        "vsplit_score": "Above AVWAP",
        "bias": "above"
    }

    send_discord_alert(signal_event)
    print("[BYBIT SNIPER] 🚀 Echo alert sent")


if __name__ == "__main__":
    while True:
        run_echo_bybit_sniper()
        print("[LOOP] ⏳ Sleeping 60 seconds...\n")
        time.sleep(60)
