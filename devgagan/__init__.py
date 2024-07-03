#devggn

from telethon.sync import TelegramClient
import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

loop = asyncio.get_event_loop()

app = Client(
    ":gndmaraobsdk:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Define the clients
sexxx = Client("seex", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
plan = Client("plan", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
batch = Client("batch", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
stat = Client("stat", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
seer = Client("start", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

try:
    sexxx.start()
    print("Instance 1 started")
except Exception as e:
    print("Instance 1 not started")
try:
    plan.start()
    print("Instance 2 started")
except Exception as e:
    print("Instance 2 not started")
try:
    batch.start()
    print("Instance 3 started")
except Exception as e:
    print("Instance 3 not started")
try:
    stat.start()
    print("Instance 4 started")
except Exception as e:
    print("Instance 4 not started")
try:
    seer.start()
    print("Instance 5 started")
except Exception as e:
    print("Instance 5 was not started")


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


loop.run_until_complete(madarchod_bot())
