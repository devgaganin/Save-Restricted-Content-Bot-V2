# devggn
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "25373179"))
API_HASH = getenv("API_HASH", "e7cbea9f7469ee49c17ce48e2afd79b3")
BOT_TOKEN = getenv("BOT_TOKEN", "7737656716:AAGC1clgqNOJq0jwRgiAzyaOk5I3xtUyuLc")
OWNER_ID = list(map(int, getenv("OWNER_ID", "6689545604").split()))
MONGO_DB = getenv("MONGO_DB", "")
LOG_GROUP = getenv("LOG_GROUP", "-1002392553444")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002309682734"))
