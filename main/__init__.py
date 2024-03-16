#Join me at telegram @dev_gagan

from pyrogram import Client

from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from decouple import config
import logging, time, sys

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)


# variables
API_ID = "26075120" #config("API_ID", default=None, cast=int)
API_HASH = "1fda88a5d1de46058a4791c78bce198e" #config("API_HASH", default=None)
BOT_TOKEN = "6978714575:AAE_XolEbhZQjzX69QHDOBR6ZddX96og5e8" #config("BOT_TOKEN", default=None)
SESSION = "BQGN3_AABGE0s1j8mc-Y99z9exMOLbaxQ5NGoCAiLGCY2ClePhzqs-3BEk1IzHaSKp3FxIWTaR5v-ahEDUITzIbJgcP1jEPTSdJF9zDPxnW2NTPz2VsBQ6UHH3dAIlWUDSOG9MSQUp-esfAXxg8pLRSW6smf7I_ihDU4YVUFCgbSIuD7jKW9w6i2CCsQwqRSVbBHEz8qrP1ViJINBzjTbtZj0QmdC4VKLz9Ae1pR9X5fDhbM1nAvfBVcwZ627rXmYN-nxfbHIq5CnflIkLhr2TxGlOIR5cvV1sz_KGABdDvi9FygrnjR2obQQmkCyxjVbLI-vQHRbaY08pT-TuOoU5p0ocqlrgAAAAGlHSMFAA" #config("SESSION", default=None)
FORCESUB = "save_restricted_content_bots" #config("FORCESUB", default=None)
AUTH = "6964148334" #config("AUTH", default=None)
SUDO_USERS = []

if len(AUTH) != 0:
    SUDO_USERS = {int(AUTH.strip()) for AUTH in AUTH.split()}
else:
    SUDO_USERS = set()

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 

#userbot = Client(
#    session_name=SESSION, 
#    api_hash=API_HASH, 
#    api_id=API_ID)
userbot = Client("myacc",api_id=API_ID,api_hash=API_HASH,session_string=SESSION)

try:
    userbot.start()
except BaseException:
    print("Your session expired please re add that... thanks @dev_gagan.")
    sys.exit(1)

Bot = Client(
    "SaveRestricted",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)    

try:
    Bot.start()
except Exception as e:
    #print(e)
    logger.info(e)
    sys.exit(1)
