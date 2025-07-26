# rsi_sniper_engine/bybit_feed.py

import requests
import pandas as pd
import time

BASE_URL = "https://api.bybit.com"
RETRIES = 3
SLEEP_BETWEEN_RETRIES = 1

def get_bybit_ohlcv(symbol: str = "BTCUSDT", interval: str = "1", limit: int = 200) -> pd.DataFrame:
    endpoint = "/v5/market/kline"
    url = f"{BASE_URL}{endpoint}"

    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
    }

    for attempt in range(RETRIES):
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if data.get("retCode") != 0 or "result" not in data or "list" not in data["result"]:
                print(f"[BYBIT FEED] ⚠️ Invalid response structure: {data}")
                return pd.DataFrame()

            ohlcv = data["result"]["list"]
            df = pd.DataFrame(ohlcv, columns=[
                "timestamp", "open", "high", "low", "close", "volume", "turnover"
            ])

            df = df.astype({
                "timestamp": "int64",
                "open": "float",
                "high": "float",
                "low": "float",
                "close": "float",
                "volume": "float",
                "turnover": "float",
            })

            df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
            df.set_index("timestamp", inplace=True)

            return df.sort_index()

        except Exception as e:
            print(f"[BYBIT FEED] ❌ Error fetching OHLCV data (attempt {attempt+1}): {e}")
            time.sleep(SLEEP_BETWEEN_RETRIES)

    print("[BYBIT FEED] ❌ Failed to fetch OHLCV after retries.")
    return pd.DataFrame()
