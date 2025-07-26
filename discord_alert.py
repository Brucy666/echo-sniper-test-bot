# discord_alert.py

import requests
from datetime import datetime
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_ECHO_WEBHOOK")

def format_discord_alert(event: dict) -> dict:
    symbol = event.get("symbol", "N/A")
    price = event.get("entry_price", 0)
    vwap = event.get("vwap", 0)
    rsi = event.get("rsi", 0)
    spoof = event.get("spoof_ratio", 0)
    score = event.get("score", 0.0)
    confidence = event.get("confidence", 0.0)
    reasons = event.get("reasons", "None")
    echo_signal = event.get("echo_signal", "None")
    echo_multi_tf = event.get("multi_tf_echo", "None")
    timestamp = event.get("timestamp", datetime.utcnow().isoformat())

    return {
        "username": "Echo V Alert",
        "embeds": [
            {
                "title": f"📉 {symbol} – KuCoin Test",
                "color": 0x00ffaa,
                "fields": [
                    {"name": "Entry Price", "value": f"`{price}`", "inline": True},
                    {"name": "VWAP", "value": f"`{vwap}`", "inline": True},
                    {"name": "RSI", "value": f"`{rsi}`", "inline": True},
                    {"name": "Spoof Ratio", "value": f"`{spoof}`", "inline": True},
                    {"name": "Echo V Signal", "value": f"{echo_signal}", "inline": True},
                    {"name": "Score", "value": f"`{score}`", "inline": True},
                    {"name": "Confidence", "value": f"`{confidence}`", "inline": True},
                    {"name": "Reasons", "value": f"{reasons}", "inline": False},
                    {"name": "📡 Multi-Timeframe Echo V", "value": f"{echo_multi_tf}", "inline": False},
                    {"name": "🕒", "value": f"`{timestamp}`", "inline": False}
                ]
            }
        ]
    }

def send_discord_alert(event: dict):
    if not DISCORD_WEBHOOK:
        print("[x] Discord webhook not set")
        return

    try:
        payload = format_discord_alert(event)
        res = requests.post(DISCORD_WEBHOOK, json=payload)
        if res.status_code == 204:
            print("[✓] Discord alert sent.")
        else:
            print(f"[x] Discord response error: {res.status_code}")
    except Exception as e:
        print(f"[x] Discord exception: {e}")
