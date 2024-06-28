
#Join @devggn

import sys
from pyrogram import Client
from telethon.sync import TelegramClient
import uvloop
from config import API_ID, API_HASH, BOT_TOKEN, SESSION

uvloop.install()

bot = TelegramClient('premiumrepo', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
userbot = Client("gaganrepo",api_id=API_ID,api_hash=API_HASH,session_string=SESSION)

try:
    userbot.start()
except BaseException:
    print("Your Session expired please re add that... thanks @devggn.")
    sys.exit(1)

Bot = Client(
    "ggnbot",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)    

try:
    Bot.start()
except Exception as e:
    sys.exit(1)
