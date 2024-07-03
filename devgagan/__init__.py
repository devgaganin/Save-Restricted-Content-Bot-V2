from telethon.sync import TelegramClient
import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Define the clients
sexxx = Client("seex", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
plan = Client("plan", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
batch = Client("batch", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
stat = Client("stat", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
start = Client("start", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

clients = [sexxx, plan, batch, stat]

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

app = Client(
    ":gndmaraobsdk:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

async def start_clients():
    start_tasks = [client.start() for client in clients]
    try:
        await asyncio.gather(*start_tasks)
        print("All bots started ...")
    except Exception as e:
        print(f"Something went wrong: {e}")

async def stop_clients():
    stop_tasks = [client.stop() for client in clients]
    await asyncio.gather(*stop_tasks)
    print("All bots stopped ...")

async def madarchod_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await app.start()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name

async def main():
    await start_clients()
    await madarchod_bot()

# Run the main function
asyncio.run(main())
