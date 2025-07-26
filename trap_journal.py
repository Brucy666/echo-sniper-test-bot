# trap_journal.py
import os
import csv
from datetime import datetime

LOG_FILE = "logs/echo_sniper_traps.csv"

def log_echo_sniper_event(event: dict):
    os.makedirs("logs", exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "symbol", "exchange", "entry_price", "rsi",
            "vwap", "bias", "spoof_ratio", "score", "confidence",
            "rsi_status", "vsplit_score", "trap_type"
        ])

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": event.get("timestamp"),
            "symbol": event.get("symbol"),
            "exchange": event.get("exchange"),
            "entry_price": event.get("entry_price"),
            "rsi": event.get("rsi"),
            "vwap": event.get("vwap"),
            "bias": event.get("bias"),
            "spoof_ratio": event.get("spoof_ratio"),
            "score": event.get("score"),
            "confidence": event.get("confidence"),
            "rsi_status": event.get("rsi_status"),
            "vsplit_score": event.get("vsplit_score"),
            "trap_type": event.get("trap_type")
        })

    print(f"[📓] Echo Trap Logged: {event['exchange']} - {event['rsi_status']} @ {event['entry_price']}")
