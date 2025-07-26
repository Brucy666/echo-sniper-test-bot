# bybit_feed.py
# Pulls historical OHLCV data for multi-timeframe Echo RSI engine

import requests
import pandas as pd
import time

BASE_URL = "https://api.bybit.com"

BYBIT_INTERVAL_MAP = {
    "1m": "1",
    "5m": "5",
    "15m": "15",
    "1h": "60",
    "4h": "240"
}


def get_bybit_ohlcv(symbol="BTCUSDT", interval="1m", limit=200):
    try:
        bybit_interval = BYBIT_INTERVAL_MAP.get(interval)
        if not bybit_interval:
            print(f"[BYBIT FEED] ❌ Unsupported interval: {interval}")
            return None

        url = f"{BASE_URL}/v5/market/kline"
        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": bybit_interval,
            "limit": limit
        }

        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json().get("result", {}).get("list", [])

        if not data:
            print("[BYBIT FEED] ⚠️ No OHLCV data returned.")
            return None

        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "turnover"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(float), unit="ms")
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)

        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"[BYBIT FEED ERROR] {e}")
        return None


if __name__ == "__main__":
    df = get_bybit_ohlcv(interval="4h")
    print(df.tail())
