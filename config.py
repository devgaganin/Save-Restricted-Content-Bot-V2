# devggn
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "28316155"))
API_HASH = getenv("API_HASH", "e3499ac331a8df93997c1680366f2327")
BOT_TOKEN = getenv("BOT_TOKEN", "7298768567:AAHFNglR8exFNN9TDA_rpb8vKiaHaVhw9U8")
OWNER_ID = int(getenv("OWNER_ID", "7473115116"))
MONGODB_CONNECTION_STRING = getenv("MONGO_DB", "mongodb+srv://dustofappearance678:g1ETBVtzGV9ZcPJK@cluster0.bkxjy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP = int(getenv("LOG_GROUP", "-1002183779903"))
FORCESUB = getenv("FORCESUB", "forcesubscribe2")
