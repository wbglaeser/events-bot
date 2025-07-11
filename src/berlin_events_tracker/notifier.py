# src/berlin_events_tracker/notifier.py

import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

# Load from .env in development; in prod make sure env vars are set
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")
API_URL   = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def _send_message(text: str) -> None:
    """Low-level: send a Markdown message to your chat."""
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram credentials missing; skipping notification.")
        return

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    resp = requests.post(API_URL, json=payload)
    if not resp.ok:
        print(f"❌ Telegram send failed [{resp.status_code}]: {resp.text}")

def notify_new_events(added_events: List[Dict]) -> None:
    """
    Formats a list of added events and sends them as one Telegram message.
    Each event dict must have: 'title', 'link', and 'termin'.
    """
    if not added_events:
        return

    lines = ["*Neue Events hinzugefügt:*"]
    for ev in added_events:
        title = ev.get("title", "–")
        link  = ev.get("link", "")
        date  = ev.get("termin", "")
        # Markdown link: [text](url)
        lines.append(f"• [{title}]({link}) am {date}")

    message = "\n".join(lines)
    _send_message(message)