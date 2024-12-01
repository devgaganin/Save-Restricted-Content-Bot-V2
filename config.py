# devgagan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "21567814"))
API_HASH = getenv("API_HASH", "cd7dc5431d449fd795683c550d7bfb7e")
BOT_TOKEN = getenv("BOT_TOKEN", "7649708076:AAE-4tGnslvR8cmk7J5OuRuRlEHqsZpzWYc")
OWNER_ID = list(map(int, getenv("OWNER_ID", "21567814").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://krishna931074:4L2TsfrwBSOu3sxB@cluster0.2p4co.mongodb.net/")
LOG_GROUP = getenv("LOG_GROUP", "")
CHANNEL_ID = int(getenv("CHANNEL_ID", ""))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "0"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "500"))
