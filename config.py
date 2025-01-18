# devgagan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "24692763"))
API_HASH = getenv("API_HASH", "8e3840420e9d0895db3231d87c6d21a5")
BOT_TOKEN = getenv("BOT_TOKEN", "8005393579:AAES8sv0C5NMw_vDJSTHSicCfFvdlqjRCmA")
OWNER_ID = list(map(int, getenv("OWNER_ID", "6416816452").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://jihehod332:OM69Q4epgIEcN3xk@cluster0.qzw02.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP = getenv("LOG_GROUP", "-1002340534679")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002486629939"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "0"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "5000"))
WEBSITE_URL = getenv("WEBSITE_URL", "upshrink.com")
AD_API = getenv("AD_API", "")
STRING = getenv("STRING", None)
YT_COOKIES = getenv("YT_COOKIES", None)
INSTA_COOKIES = getenv("INSTA_COOKIES", None)
