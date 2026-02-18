from server import update_message
from telethon import TelegramClient, events
import joblib
import re

api_id = 12345678
api_hash = "PASTE_API_HASH_HERE"

client = TelegramClient("session", api_id, api_hash)

model = joblib.load("spam_model.pkl")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


@client.on(events.NewMessage)
async def new_message_listener(event):
    print("MESSAGE EVENT TRIGGERED")

    message = event.raw_text
    cleaned = clean_text(message)

    prediction = model.predict([cleaned])[0]

    if prediction == 1:
        print("SPAM:", message)
        update_message(message, "SPAM")
    else:
        print("NORMAL:", message)
        update_message(message, "NORMAL")


print("AI Spam Detector Running...")

client.start()
client.run_until_disconnected()
