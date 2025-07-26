# bybit_feed.py

import requests
import pandas as pd

def get_bybit_ohlcv(symbol="BTCUSDT", interval="60", limit=200):
    url = "https://api.bybit.com/v5/market/kline"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("retCode") != 0:
            print(f"[BYBIT ERROR] retCode {data.get('retCode')}, msg: {data.get('retMsg')}")
            return None

        ohlcv = data.get("result", {}).get("list", [])
        if not ohlcv:
            print("[BYBIT FEED] ⚠️ No OHLCV data returned.")
            return None

        df = pd.DataFrame(ohlcv, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "turnover"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(float), unit="ms")
        df = df.sort_values("timestamp")
        df = df.astype({
            "open": float,
            "high": float,
            "low": float,
            "close": float,
            "volume": float
        })

        print(f"[BYBIT FEED] ✅ Loaded {len(df)} OHLCV rows for {symbol} @ {interval}")
        return df[["timestamp", "open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"[BYBIT ERROR] Exception fetching OHLCV: {e}")
        return None
