# devggn
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "21857983"))
API_HASH = getenv("API_HASH", "e469e84c943ce3b8b056eb6a296f2c67")
BOT_TOKEN = getenv("BOT_TOKEN", "7289060685:AAEfteCWvdrQoNZ2JPstVPnBv9Rql_iaLBA")
OWNER_ID = list(map(int, getenv("OWNER_ID", "833465134").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://yogesh:vFojzRVGQQKWNmoj@master.2cdyk37.mongodb.net/?retryWrites=true&w=majority&appName=MASTER")
LOG_GROUP = getenv("LOG_GROUP", "-1002233879412")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002221310765"))
