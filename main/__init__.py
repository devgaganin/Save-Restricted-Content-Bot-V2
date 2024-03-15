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
SESSION = "BQHDMOUAruOqUO0grRRxIyGzuWfE2jbicJKq1WHgHAKK5ouLl3iG1Sa_ia3AaVm0WmcCXx0SPIVQXzZonVTBlmJYzqLtbe7j3oUwNUebD1QVwzZOGddgZz00FmFyOupXZ98D4sTOWMc5G90V9UTD_sLh9kBiEED3rfl2HF05UvUcXsKN63ip_Vj36N695ED-geqOV0zMLmMzj0Cr2kiJ1qoT4KRXLnLpnrVIqaj4LqmqDsYiu7w6Mc4zlxKCjOcItR4wZ6H6idogNV_gVMU84sy8s2d0I3XvWwJycfhaNWEKLxREFKwUNf32k-yGcR739V2YcmH4zQiynLT_Ci-DVBnbRvsNxwAAAAGlHSMFAA" #config("SESSION", default=None)
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
