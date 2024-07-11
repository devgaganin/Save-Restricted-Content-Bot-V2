
#Join @devggn

import sys
from pyrogram import Client
from telethon.sync import TelegramClient
import uvloop
from config import API_ID, API_HASH, BOT_TOKEN

bot = TelegramClient('premiumrepo', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

Bot = Client(
    "ggnbot",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH,
    workers=10,
    sleep_threshold=20,
    max_concurrent_transmissions=8
    
)    

try:
    Bot.start()
except Exception as e:
    sys.exit(1)

modi = Client(
    "modibot",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
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
    workers=10,
    sleep_threshold=20,
    max_concurrent_transmissions=8
)    

try:
    sigma.start()
except Exception as e:
    sys.exit(1)

sex = TelegramClient('sexrepo', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
