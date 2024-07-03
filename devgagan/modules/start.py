import pymongo
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import os
from devgagan import start as app
from config import MONGO_DB as MONGODB_CONNECTION_STRING, OWNER_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_NAME = "start_users"
COLLECTION_NAME = "registered_users_collection"

mongo_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

def load_registered_users():
    registered_users = set()
    for user_doc in collection.find():
        registered_users.add(user_doc["user_id"])
    return registered_users

def save_registered_users(registered_users):
    for user_id in registered_users:
        collection.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

REGISTERED_USERS = load_registered_users()

@app.on_message(filters.command("start"))
async def start(client, message):
    """
    Command to start the bot
    """
    user_id = message.from_user.id
    collection.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Join Channel", url="https://t.me/devggn")],
        [InlineKeyboardButton("Contact Me", url="https://t.me/ggnhere")]
    ])
    await message.reply_photo(
        START_PIC,
        caption=TEXT,
        reply_markup=buttons
    )

@app.on_message(filters.command("gcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    text = message.text.split(' ', 1)[1]
    for user_doc in collection.find():
        try:
            user_id = user_doc["user_id"]
            await client.send_message(user_id, text)
        except Exception as e:
            logger.error(f"Error sending message to user {user_id}: {str(e)}")

def get_registered_users():
    registered_users = []
    for user_doc in collection.find():
        registered_users.append((str(user_doc["user_id"]), user_doc.get("first_name", "")))
    return registered_users

def save_user_ids_to_txt(users_info, filename):
    with open(filename, "w") as file:
        for user_id, first_name in users_info:
            file.write(f"{user_id}: {first_name}\n")

@app.on_message(filters.command("get") & filters.user(OWNER_ID))
async def get_registered_users_command(client, message):
    registered_users = get_registered_users()
    filename = "registered_users.txt"
    save_user_ids_to_txt(registered_users, filename)
    await client.send_document(message.chat.id, filename)
    os.remove(filename)

S = "/start"
START_PIC = "https://graph.org/file/1dfb96bd8f00a7c05f164.gif"
TEXT = "Send me the Link of any message of Restricted Channels to Clone it here.\nFor private channel's messages, send the Invite Link first.\n\n👉🏻 Execute /batch for bulk process up to 10K files range."

M = "/plan"
PREMIUM_PIC = "plan.png"
PRE_TEXT = """💰 **Premium Price**: Starting from $2 or 200 INR accepted via **__Amazon Gift Card__** (terms and conditions apply).
📥 **Download Limit**: Users can download up to 100 files in a single batch command.
🛑 **Batch**: You will get two modes /bulk and /batch.
   - Users are advised to wait for the process to automatically cancel before proceeding with any downloads or uploads.\n
📜 **Terms and Conditions**: For further details and complete terms and conditions, please send /terms.
"""

@app.on_message(filters.command("plan"))
async def plan_command(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Send Gift Card Code", url="https://t.me/ttonehelpbot")]
    ])
    await message.reply_photo(
        PREMIUM_PIC,
        caption=PRE_TEXT,
        reply_markup=buttons
    )

T = "/terms"
TERM_PIC = "term.png"
TERM_TEXT = """📜 **Terms and Conditions** 📜\n
✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.
✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__
✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion and mood.
"""

@app.on_message(filters.command("terms"))
async def term_command(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Query?", url="https://t.me/ttonehelpbot"),
         InlineKeyboardButton("Channel", url="https://telegram.dog/devggn")]
    ])
    await message.reply_photo(
        TERM_PIC,
        caption=TERM_TEXT,
        reply_markup=buttons
    )

REPO_URL = "https://github.com/devgaganin/Save-Restricted-Content-Bot-Repo"

HELP_TEXT = """Here are the available commands:

➡️ /batch - to process link one by one iterating through single single message ids.

➡️ /dl - to download youtube videos.

➡️ /host - to download youtube videos.

➡️ /cancel - to cancel batches

➡️ /settings - to edit settings.

[GitHub Repository](%s)
""" % REPO_URL

@app.on_message(filters.command("help"))
async def help_command(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("REPO", url=REPO_URL)]
    ])
    await message.reply(HELP_TEXT, reply_markup=buttons, disable_web_page_preview=True)
