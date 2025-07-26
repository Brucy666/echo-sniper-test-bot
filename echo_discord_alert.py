# echo_discord_alert.py (Upgraded with Safe TF Map Display)

import requests
from datetime import datetime
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_ECHO_WEBHOOK")

def format_tf_overview(tf_map):
    lines = ["\n🧠 **Echo V Timeframe Map**"]

    if not isinstance(tf_map, dict) or not tf_map:
        lines.append("_Unavailable_")
        return "\n".join(lines)

    for tf, signal in tf_map.items():
        if signal == "None":
            lines.append(f"`{tf:<4}`
