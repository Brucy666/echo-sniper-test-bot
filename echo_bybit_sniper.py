# echo_bybit_sniper.py

import time
from bybit_feed import get_multi_ohlcv
from echo_v_engine import get_multi_tf_echo_signals


def run_echo_bybit_sniper():
    print("[BYBIT SNIPER] 🟡 Running Echo V Analysis for Bybit...")

    symbol = "BTC/USDT"
    timeframes = ["1m", "5m", "15m", "1h", "4h"]

    # Pull historical candles for all timeframes
    tf_data_map = {}
    for tf in timeframes:
        ohlcv = get_multi_ohlcv(symbol, tf)
        if ohlcv is not None:
            tf_data_map[tf] = ohlcv
        else:
            print(f"[BYBIT ERROR] Failed to fetch {tf} data for {symbol}")

    # Run Echo V logic
    try:
        echo_results = get_multi_tf_echo_signals(tf_data_map)
        for tf, result in echo_results.items():
            print(f"[ECHO ✅] {symbol} {tf} → {result}")
    except Exception as e:
        print(f"[ECHO ERROR] Failed to calculate Echo signals: {e}")
