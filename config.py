# devgaganin
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "20505904"))
API_HASH = getenv("API_HASH", "0e8475b59aeb2cbc4932b14e3823d826")
BOT_TOKEN = getenv("BOT_TOKEN", "7491331618:AAHVZMXjBSVeEbRVzt62rFKV-_VkA-rnp_4")
OWNER_ID = int(getenv("OWNER_ID", "1290716828"))
MONGODB_CONNECTION_STRING = getenv("MONGO_DB", "mongodb+srv://vipinlaptop845874:PgiJaT5IyaN5iMzg@cluster0.wigmd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP = int(getenv("LOG_GROUP", "1290716828"))
FORCESUB = getenv("FORCESUB", "-1002255977626")
DEFAULT_SESSION = getenv("DEFAULT_SESSION", "") # this is jkust to help if you dont want to force your bot user to login or if they not interested
