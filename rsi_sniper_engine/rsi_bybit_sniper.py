# rsi_sniper_engine/rsi_bybit_sniper.py

from rsi_engine import calculate_rsi, detect_rsi_signal
from bybit_feed import get_bybit_ohlcv
from rsi_discord_alert import send_discord_alert
import time

def run_rsi_sniper():
    print("[RSI SNIPER] 🔍 Running RSI Sniper Engine")

    symbol = "BTCUSDT"
    interval = "15"  # 15m

    df = get_bybit_ohlcv(symbol=symbol, interval=interval)
    if df is None or df.empty:
        print("[BYBIT] ⚠️ No OHLCV data returned.")
        return

    print(f"[BYBIT] ✅ Loaded {len(df)} OHLCV rows for {symbol} @ {interval}m")

    df["rsi"] = calculate_rsi(df["close"])
    signal = detect_rsi_signal(df)

    if signal:
        alert = {
            "symbol": symbol,
            "exchange": "Bybit",
            "entry_price": df.iloc[-1]["close"],
            "rsi_value": df["rsi"].iloc[-1],
            "signal_type": signal,
            "confidence": 6.8,
            "timeframe": "15m"
        }

        send_discord_alert(alert)
        print("[RSI SNIPER] 🚀 Alert sent to Discord")
    else:
        print("[RSI SNIPER] ❌ No RSI signal detected")

    time.sleep(60)
