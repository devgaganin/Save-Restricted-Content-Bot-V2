# devggn
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = int(getenv("OWNER_ID", ""))
MONGODB_CONNECTION_STRING = getenv("MONGODB_CONNECTION_STRING", "mongodb+srv://ggn:ggn@ggn.upuljx5.mongodb.net/?retryWrites=true&w=majority&appName=ggn")
LOG_GROUP = int(getenv("LOG_GROUP", ""))
SESSION = getenv("SESSION", "")
FORCESUB = getenv("FORCESUB", "")
