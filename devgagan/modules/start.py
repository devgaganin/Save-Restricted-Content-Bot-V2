import pymongo
from devgagan import sex as gagan
from telethon import events, Button
from telethon.tl.types import DocumentAttributeVideo
import re
import logging
import pymongo
import sys
import math
import os
import time
from datetime import datetime as dt, timedelta
import json
import asyncio
from telethon.sync import TelegramClient
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

@gagan.on(events.NewMessage(pattern=f"^/start"))
async def start(event):
    """
    Command to start the bot
    """
    user_id = event.sender_id
    collection.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    buttons = [
        [Button.url("Join Channel", url="https://t.me/devggn")],
        [Button.url("Contact Me", url="https://t.me/ggnhere")],
    ]
    await gagan.send_file(
        event.chat_id,
        file=START_PIC,
        caption=TEXT,
        buttons=buttons
    )

@gagan.on(events.NewMessage(pattern=f"^/gcast"))
async def broadcast(event):
    if event.sender_id != OWNER_ID:
        return await event.respond("You are not authorized to use this command.")

    message = event.message.text.split(' ', 1)[1]
    for user_doc in collection.find():
        try:
            user_id = user_doc["user_id"]
            await gagan.send_message(user_id, message)
        except Exception as e:
            logger.error(f"Error sending message to user {user_id}: {str(e)}")

def get_registered_users():
    registered_users = []
    for user_doc in collection.find():
        registered_users.append((str(user_doc["user_id"]), user_doc.get("first_name", "")))
    return registered_users

# Function to save user IDs and first names to a text file
def save_user_ids_to_txt(users_info, filename):
    with open(filename, "w") as file:
        for user_id, first_name in users_info:
            file.write(f"{user_id}: {first_name}\n")

@gagan.on(events.NewMessage(incoming=True, pattern='/get'))
async def get_registered_users_command(event):
    # Check if the command is initiated by the owner
    if event.sender_id != OWNER_ID:
        return await event.respond("You are not authorized to use this command.")
    
    # Get all registered user IDs and first names
    registered_users = get_registered_users()

    # Save user IDs and first names to a text file
    filename = "registered_users.txt"
    save_user_ids_to_txt(registered_users, filename)

    # Send the text file
    await event.respond(file=filename, force_document=True)
    os.remove(filename)  # Remove the temporary file after sending

S = "/start"
START_PIC = "https://graph.org/file/1dfb96bd8f00a7c05f164.gif"
TEXT = "Send me the Link of any message of Restricted Channels to Clone it here.\nFor private channel's messages, send the Invite Link first.\n\n👉🏻 Execute /batch for bulk process upto 10K files range."


M = "/plan"
PREMIUM_PIC = "plan.png"
PRE_TEXT = """💰 **Premium Price**: Starting from $2 or 200 INR accepted via **__Amazon Gift Card__** (terms and conditions apply).
📥 **Download Limit**: Users can download up to 100 files in a single batch command.
🛑 **Batch**: You will get two modes /bulk and /batch.
   - Users are advised to wait for the process to automatically cancel before proceeding with any downloads or uploads.\n
📜 **Terms and Conditions**: For further details and complete terms and conditions, please send /terms.
"""

@gagan.on(events.NewMessage(pattern=f"^{M}"))
async def plan_command(event):
    # Creating inline keyboard with buttons
    buttons = [
        [Button.url("Send Gift Card Code", url="https://t.me/ttonehelpbot")]
    ]

    # Sending photo with caption and buttons
    await gagan.send_file(
        event.chat_id,
        file=PREMIUM_PIC,
        caption=PRE_TEXT,
        buttons=buttons
    )

T = "/terms"
TERM_PIC = "term.png"
TERM_TEXT = """📜 **Terms and Conditions** 📜\n
✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.
✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__
✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion and mood.
"""

@gagan.on(events.NewMessage(pattern=f"^{T}"))
async def term_command(event):
    # Creating inline keyboard with buttons
    buttons = [
        [Button.url("Query?", url="https://t.me/ttonehelpbot"),
         Button.url("Channel", url="https://telegram.dog/devggn")]
    ]

    # Sending photo with caption and buttons
    await gagan.send_file(
        event.chat_id,
        file=TERM_PIC,
        caption=TERM_TEXT,
        buttons=buttons
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

# Purchase premium for more website supported repo and /adl repo.

@gagan.on(events.NewMessage(pattern='/help'))
async def help_command(event):
    buttons = [[Button.url("REPO", url=REPO_URL)]]
    await event.respond(HELP_TEXT, buttons=buttons, link_preview=False)
