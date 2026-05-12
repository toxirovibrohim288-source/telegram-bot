import re
from datetime import datetime
from telethon import TelegramClient, events

API_ID = int(__import__("os").environ.get("API_ID", 0))
API_HASH = __import__("os").environ.get("API_HASH", "")
BOT_TOKEN = __import__("os").environ.get("BOT_TOKEN", "")

PAYMENT_BOTS = [
    "PaymeBusinessNotifierBot",
    "clickuz",
    "ApelsinAssistantbot"
]

client = TelegramClient("session", API_ID, API_HASH)

payments = []

def extract_amount(text):
    match = re.findall(r'(\d[\d\s]*)', text)
    if not match:
        return None
    try:
        return float(max(match).replace(" ", ""))
    except:
        return None

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    username = getattr(sender, "username", "")

    if username not in PAYMENT_BOTS:
        return

    amount = extract_amount(event.raw_text)
    if not amount:
        return

    payments.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "service": username,
        "amount": amount
    })

    print("PAYMENT:", amount, "TOTAL:", sum(p["amount"] for p in payments))

async def main():
    print("BOT STARTED")
    await client.start()
    await client.run_until_disconnected()

client.loop.run_until_complete(main())
import os

print("API_ID:", os.environ.get("API_ID"))
print("API_HASH:", os.environ.get("API_HASH"))
