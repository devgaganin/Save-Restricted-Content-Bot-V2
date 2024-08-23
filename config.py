# devggn
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "29130580"))
API_HASH = getenv("API_HASH", "4c1d820023c16dfa5932e00527cb306c")
BOT_TOKEN = getenv("BOT_TOKEN", "7413856268:AAFppfr4ViRm1KOJYFgm1T0_0TEQCW2aJdE")
OWNER_ID = int(getenv("OWNER_ID", "7118187371"))
MONGODB_CONNECTION_STRING = getenv("MONGO_DB", "mongodb+srv://eraon8:d0DiBsv96iEW8JSb@rameshlal.errc5t2.mongodb.net/?retryWrites=true&w=majority&appName=Rameshlal")
LOG_GROUP = int(getenv("LOG_GROUP", "-4588997635"))
FORCESUB = getenv("FORCESUB", "resgif")
