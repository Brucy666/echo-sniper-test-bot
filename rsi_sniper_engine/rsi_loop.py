# rsi_sniper_engine/rsi_loop.py

import time
from rsi_bybit_sniper import run_rsi_sniper

def loop_rsi_sniper():
    print("[LOOP] 🧠 Starting RSI Sniper Loop...\n")
    while True:
        try:
            run_rsi_sniper()
        except Exception as e:
            print(f"[ERROR] RSI Sniper failed: {e}")
        print("[LOOP] ⏱ Sleeping 60 seconds...\n")
        time.sleep(60)

if __name__ == "__main__":
    loop_rsi_sniper()
