# test_sniper_loop.py
import time
from bybit_echo_sniper import run_bybit_echo_sniper

print("[LOOP TEST 🤖] 🚀 Starting Test Echo Sniper Loop...")

while True:
    print("\n[LOOP TEST] 🔁 New Scan Cycle — Echo Test Bot")

    try:
        run_bybit_echo_sniper()
    except Exception as e:
        print(f"[ERROR] Echo Sniper Exception: {e}")

    print("[LOOP TEST] ⏱️ Sleeping for 60 seconds...\n")
    time.sleep(60)
