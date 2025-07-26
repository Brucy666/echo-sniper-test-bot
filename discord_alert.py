# discord_alert.py

import requests
from datetime import datetime
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_ECHO_WEBHOOK")

def format_discord_alert(event: dict) -> dict:
    symbol = event.get("symbol", "N/A")
    exchange = event.get("exchange", "Unknown")
    price = event.get("entry_price", 0)
    rsi = event.get("rsi", "N/A")
    spoof = event.get("spoof_ratio", 0)
    confidence = event.get("confidence", 0)
    trap_type = event.get("trap_type", "N/A")
    status = event.get("rsi_status", "None")
    tf_score = event.get("vsplit_score", "None")
    bias = event.get("bias", "Unknown")
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    bias_emoji = "📈" if bias.lower() == "above" else "📉"
    spoof_emoji = "🟢" if spoof < 0.3 else "🟠" if spoof < 0.6 else "🔴"
    brain = "🧠" if confidence > 7 else "⚠️" if confidence > 4 else "❓"

    return {
        "username": "Echo Sniper Bot",
        "embeds": [
            {
                "title": f"🎯 Echo Trap Triggered",
                "color": 0x00ffae if bias.lower() == "above" else 0xff5555,
                "fields": [
                    {"name": "Token", "value": f"`{symbol}`", "inline": True},
                    {"name": "Exchange", "value": f"`{exchange}`", "inline": True},
                    {"name": "Bias", "value": f"{bias_emoji} `{bias}`", "inline": True},
                    {"name": "RSI Signal", "value": f"`{status}`", "inline": True},
                    {"name": "Trap Type", "value": f"`{trap_type}`", "inline": True},
                    {"name": "Spoof Ratio", "value": f"{spoof_emoji} `{spoof:.2f}`", "inline": True},
                    {"name": "Entry Price", "value": f"`{price}`", "inline": True},
                    {"name": "VWAP Status", "value": f"`{tf_score}`", "inline": True},
                    {"name": "Confidence", "value": f"{brain} `{confidence}/10`", "inline": True},
                    {"name": "Timestamp", "value": f"`{timestamp}`", "inline": False}
                ],
                "footer": {"text": "Echo AI V Engine"}
            }
        ]
    }

def send_discord_alert(event: dict):
    if not DISCORD_WEBHOOK:
        print("[❌] No Discord webhook set.")
        return

    payload = format_discord_alert(event)
    headers = {"Content-Type": "application/json"}

    try:
        res = requests.post(DISCORD_WEBHOOK, json=payload, headers=headers)
        if res.status_code in [200, 204]:
            print("[✓] Echo alert sent to Discord.")
        else:
            print(f"[!] Discord alert failed: {res.status_code}, {res.text}")
    except Exception as e:
        print(f"[!] Discord send error: {e}")
