# echo_logger.py

import os
import requests
from datetime import datetime

discord_log_webhook = os.getenv("DISCORD_ECHO_LOG_WEBHOOK")

def log_echo_cycle(symbol, timeframe_results):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    summary_lines = [f"**🔍 Echo V Scan Report**", f"Token: `{symbol}`", f"Time: `{timestamp}`", ""]

    for tf, result in timeframe_results.items():
        loaded = "✅" if result.get("data_loaded") else "⚠️"
        signal = result.get("signal", "None")
        signal_str = f"🔔 `{signal}`" if signal != "None" else "❌ No signal"
        summary_lines.append(f"{loaded} `{tf}` → {signal_str}")

    payload = {
        "username": "Echo Logger",
        "embeds": [
            {
                "title": "Echo Grid Scan Result",
                "description": "\n".join(summary_lines),
                "color": 0x5865F2,
                "footer": {"text": "Echo V Logging Engine"},
                "timestamp": datetime.utcnow().isoformat()
            }
        ]
    }

    if discord_log_webhook:
        try:
            requests.post(discord_log_webhook, json=payload)
            print("[LOGGER] 🧾 Echo scan log sent to Discord.")
        except Exception as e:
            print(f"[LOGGER ERROR] Failed to send log: {e}")
    else:
        print("[LOGGER WARNING] No Discord log webhook set.")
