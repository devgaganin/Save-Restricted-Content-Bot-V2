# devggn
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "19748984"))
API_HASH = getenv("API_HASH", "2141e30f96dfbd8c46fbb5ff4b197004")
BOT_TOKEN = getenv("BOT_TOKEN", "7012175450:AAHEdufYSZUkRBYt7antQjjcGD7fW1SusqQ")
OWNER_ID = int(getenv("OWNER_ID", "7065117445"))
MONGODB_CONNECTION_STRING = getenv("MONGO_DB", "mongodb+srv://forward:forward@cluster0.xowzpr4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP = int(getenv("LOG_GROUP", "-1001878947221"))
# SESSION = getenv("PYROGRAM_V2_SESSION", "")
FORCESUB = getenv("FORCESUB", "save_restricted_content_bots")
