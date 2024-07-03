import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

loop = asyncio.get_event_loop()

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

async def start_clients():
    clients = [
        Client("seex", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN),
        Client("plan", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN),
        Client("batch", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN),
        Client("stat", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN),
        Client("start", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    ]

    try:
        for client in clients:
            await client.start()
            print(f"Instance {clients.index(client) + 1} started")
            await asyncio.sleep(10)
    except Exception as e:
        print(f"Instance {clients.index(client) + 1} not started: {e}")

async def madarchod_bot():
    async with Client(":gndmaraobsdk:", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
        global BOT_ID, BOT_NAME, BOT_USERNAME
        getme = await app.get_me()
        BOT_ID = getme.id
        BOT_USERNAME = getme.username
        BOT_NAME = f"{getme.first_name} {getme.last_name}" if getme.last_name else getme.first_name

# Run the event loop and tasks
loop.run_until_complete(asyncio.gather(start_clients(), madarchod_bot()))
