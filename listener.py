from server import update_message
from telethon import TelegramClient, events
import joblib
import re

# ---------- TELEGRAM API ----------
api_id = 24541791
api_hash = "199d4a2fe10f292214cf25784cada04d"

client = TelegramClient("session", api_id, api_hash)

# ---------- LOAD AI MODEL ----------
model = joblib.load("spam_model.pkl")


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


# ---------- MESSAGE LISTENER ----------
@client.on(events.NewMessage)
async def new_message_listener(event):
    message = event.raw_text
    cleaned = clean_text(message)

    prediction = model.predict([cleaned])[0]

    if prediction == 1:
        print("SPAM:", message)
        update_message(message, "SPAM")
    else:
        print("NORMAL:", message)
        update_message(message, "NORMAL")


client.start()
client.run_until_disconnected()
