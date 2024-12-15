# devgaganin
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "29226750"))
API_HASH = getenv("API_HASH", "e2772ee6aba52f15e72ac9684c38f54c")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = int(getenv("OWNER_ID", "7024606962"))
MONGODB_CONNECTION_STRING = getenv("MONGO_DB", "mongodb+srv://devilkumarali006:dtcsaYfS26Ceh9em@cluster0.ekho2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP = int(getenv("LOG_GROUP", "2467289478"))
FORCESUB = getenv("FORCESUB", "")
DEFAULT_SESSION = getenv("DEFAULT_SESSION", "") # this is jkust to help if you dont want to force your bot user to login or if they not interested
