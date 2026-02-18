from telethon import TelegramClient, events
from server import update_message
import joblib, re, asyncio

api_id = 12345678
api_hash = "PASTE_API_HASH_HERE"

client = TelegramClient("session", api_id, api_hash)

model = joblib.load("spam_model.pkl")

current_chat = None   # <- dynamic channel


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


@client.on(events.NewMessage)
async def handler(event):
    global current_chat

    if current_chat is None:
        return

    # only listen to selected channel
    if event.chat and event.chat.username != current_chat:
        return

    message = event.raw_text
    cleaned = clean_text(message)
    prediction = model.predict([cleaned])[0]

    if prediction == 1:
        update_message(message, "SPAM")
    else:
        update_message(message, "NORMAL")


async def start_bot():
    await client.start()
    print("Bot running...")
    await client.run_until_disconnected()


def set_channel(username):
    global current_chat
    current_chat = username
    print("Now monitoring:", username)


if __name__ == "__main__":
    asyncio.run(start_bot())
