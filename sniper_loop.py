# sniper_loop.py

import time
from echo_bybit_sniper import run_echo_bybit_sniper

print("[LOOP] 🔁 Starting Echo Sniper Loop...")

while True:
    try:
        print("[LOOP] → Running Bybit Echo Sniper...")
        run_echo_bybit_sniper()
    except Exception as e:
        print(f"[ERROR] Echo Sniper failed: {e}")

    print("[LOOP] ⏱️ Sleeping 60 seconds...\n")
    time.sleep(60)
