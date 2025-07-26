# echo_discord_alert.py

import requests
from datetime import datetime
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_ECHO_WEBHOOK")

def format_tf_map(tf_map: dict) -> str:
    lines = ["**Timeframe Overview**"]
    for tf, signal in tf_map.items():
        if "Hidden Bull" in signal:
            icon = "🟢"
        elif "Hidden Bear" in signal:
            icon = "🟠"
        elif "Sync" in signal:
            icon = "✅"
        elif "No Signal" in signal:
            icon = "🔍"
        else:
            icon = "❓"
        lines.append(f"{tf:<4} {icon} {signal}")
    return "\n".join(lines)

def format_discord_alert(event: dict) -> dict:
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    return {
        "username": "Echo Sniper Bot",
        "embeds": [
            {
                "title": "🎯 Echo Signal Detected",
                "color": 0x00ffae,
                "fields": [
                    {"name": "Symbol", "value": event.get("symbol", "N/A"), "inline": True},
                    {"name": "Exchange", "value": event.get("exchange", "N/A"), "inline": True},
                    {"name": "Bias", "value": f"📈 {event.get('bias', '')}", "inline": True},
                    {"name": "Signal", "value": event.get("rsi_status", "None"), "inline": True},
                    {"name": "Trap Type", "value": event.get("trap_type", "N/A"), "inline": True},
                    {"name": "Spoof Ratio", "value": f"🟢 {event.get('spoof_ratio', 0):.2f}", "inline": True},
                    {"name": "Entry Price", "value": str(event.get("entry_price", 0)), "inline": True},
                    {"name": "VWAP Zone", "value": event.get("vsplit_score", "N/A"), "inline": True},
                    {"name": "Confidence", "value": f"🧠 {event.get('confidence', 0)}/10", "inline": True},
                    {"name": "Time", "value": timestamp, "inline": False},
                    {"name": "Timeframe Overview", "value": format_tf_map(event.get("tf_map", {})), "inline": False}
                ],
                "footer": {"text": "Echo V Multi-Timeframe AI Engine"}
            }
        ]
    }

def send_discord_alert(event: dict):
    if not DISCORD_WEBHOOK:
        print("[❌] Missing webhook.")
        return

    try:
        payload = format_discord_alert(event)
        headers = {"Content-Type": "application/json"}
        response = requests.post(DISCORD_WEBHOOK, json=payload, headers=headers)

        if response.status_code in [200, 204]:
            print("[✓] Discord alert sent.")
        else:
            print(f"[!] Discord error: {response.status_code} {response.text}")
    except Exception as e:
        print(f"[!] Alert send failed: {e}")
