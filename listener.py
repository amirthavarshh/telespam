from telethon import TelegramClient, events

# 🔐 Replace with your own values
api_id = 24541791

api_hash = "199d4a2fe10f292214cf25784cada04d"

client = TelegramClient("session", api_id, api_hash)


@client.on(events.NewMessage)
async def new_message_listener(event):
    sender = await event.get_sender()
    print("\nNew Message Received")
    print("User:", sender.id)
    print("Text:", event.raw_text)


print("Listening for messages...")

client.start()
client.run_until_disconnected()
