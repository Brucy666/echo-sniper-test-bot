# rsi_sniper_engine/rsi_discord_alert.py

import requests
import os
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_RSI_WEBHOOK")

def send_discord_alert(alert):
    embed = {
        "title": "📈 RSI Signal Detected",
        "color": 0x3498db,
        "fields": [
            {"name": "Symbol", "value": f"`{alert['symbol']}`", "inline": True},
            {"name": "Exchange", "value": f"`{alert['exchange']}`", "inline": True},
            {"name": "Signal Type", "value": f"`{alert['signal_type']}`", "inline": True},
            {"name": "RSI", "value": f"`{alert['rsi_value']:.2f}`", "inline": True},
            {"name": "Entry Price", "value": f"`{alert['entry_price']}`", "inline": True},
            {"name": "TF", "value": f"`{alert['timeframe']}`", "inline": True},
            {"name": "Confidence", "value": f"🧠 `{alert['confidence']}/10`", "inline": True},
            {"name": "Time", "value": f"`{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}`", "inline": False}
        ],
        "footer": {"text": "RSI Sniper Engine"}
    }

    payload = {
        "username": "RSI Sniper Bot",
        "embeds": [embed]
    }

    try:
        res = requests.post(DISCORD_WEBHOOK, json=payload)
        if res.status_code in [200, 204]:
            print("[✓] RSI alert sent.")
        else:
            print(f"[!] Discord error: {res.status_code}")
    except Exception as e:
        print(f"[!] Discord exception: {e}")
