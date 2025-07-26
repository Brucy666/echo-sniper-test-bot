# rsi_feed.py
import requests
import pandas as pd

def get_rsi_ohlcv(symbol="BTCUSDT", interval="1", limit=200):
    url = f"https://api.bybit.com/v5/market/kline?category=linear&symbol={symbol}&interval={interval}&limit={limit}"
    try:
        res = requests.get(url)
        data = res.json().get("result", {}).get("list", [])
        if not data:
            return None

        df = pd.DataFrame(data)
        df.columns = ["timestamp", "open", "high", "low", "close", "volume", "turnover"]
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(float), unit="ms")
        return df[["timestamp", "close"]]
    except Exception as e:
        print(f"[RSI FEED] ❌ Error fetching data: {e}")
        return None
