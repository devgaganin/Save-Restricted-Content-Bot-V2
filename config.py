# devgagan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "23011537"))
API_HASH = getenv("API_HASH", "cd59a9fc8cbdca6ae2b405f149cc3c8a")
BOT_TOKEN = getenv("BOT_TOKEN", "8014622953:AAEaabxjIg0Mat6ZxGmNwbuadVTmlpG-qEE")
OWNER_ID = list(map(int, getenv("OWNER_ID", "5389632871").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://sumitdevil54:zSHpTLijJYtP6J0C@cluster0.aqfm3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP = getenv("LOG_GROUP", "-1002378364423")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002341764297"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "0"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "500"))
