# Join @devggn

import sys
import asyncio
from pyrogram import Client, compose
from telethon.sync import TelegramClient
# import uvloop
from config import API_ID, API_HASH, BOT_TOKEN

device = "Telegram Android 10.11.1"
# uvloop.install()

# Telethon client setup
bot = TelegramClient('premiumrepo', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
sex = TelegramClient('ssswewew', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


modi = Client(
    "modibot",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH,
    device_model=device,
    sleep_threshold=20,
    max_concurrent_transmissions=10
)    

try:
    modi.start()
except Exception as e:
    sys.exit(1)

sigma = Client(
    "sigma",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH,
    device_model=device,
    sleep_threshold=20,
    max_concurrent_transmissions=10
)    

try:
    sigma.start()
except Exception as e:
    sys.exit(1)

# List of additional Pyrogram clients
Bot = []

# Create multiple additional Pyrogram clients
for i in range(1, 4):
    client_name = f"bot{i}"
    client = Client(
        client_name,
        bot_token=BOT_TOKEN,
        api_id=int(API_ID),
        api_hash=API_HASH,
        device_model=device,
        workers=50,
        sleep_threshold=20,
        max_concurrent_transmissions=10
    )
    
    # Append client to the list
    clients.append(client)

# Define async function to run the clients
async def run_clients():
    try:
        await compose(clients)
    except Exception as e:
        sys.exit(1)

# Run the async function in the main script
def run_additional_clients():
    asyncio.run(run_clients())
    
