import pymongo
from .. import bot as gagan
from .. import LOG_GROUP, MONGODB, OWNER_ID
from telethon import events, Button
from pyrogram import Client, filters
from telethon.tl.types import DocumentAttributeVideo
from multiprocessing import Process, Manager
import re
from decouple import config
import pymongo
import sys
from pyrogram.types import Message
from mutagen.easyid3 import EasyID3
import math
import os
import yt_dlp
import time
from datetime import datetime as dt, timedelta
import json
import asyncio
import cv2
from yt_dlp import YoutubeDL
from telethon.sync import TelegramClient
from .. import Bot as app
from main.plugins.helpers import screenshot
from pyrogram import Client, filters
import subprocess

# MONGODB_CONNECTION_STRING = "mongodb+srv://ggn:ggn@ggn.upuljx5.mongodb.net/?retryWrites=true&w=majority&appName=ggn"
# OWNER_ID = 7065117445 # edit this
# LOG_GROUP = -1001878947221 # edit this

MDB = "mongodb+srv://ggn:ggn@ggn.upuljx5.mongodb.net/?retryWrites=true&w=majority&appName=ggn"
MONGODB_CONNECTION_STRING = config("MONGODB", default=MDB)
# MongoDB database name and collection name
DB_NAME = "start_users"
COLLECTION_NAME = "registered_users_collection"

# Establish a connection to MongoDB
mongo_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

# Function to load registered user IDs from the MongoDB collection
def load_registered_users():
    registered_users = set()
    for user_doc in collection.find():
        registered_users.add(user_doc["user_id"])
    return registered_users

# Function to save registered user IDs to the MongoDB collection
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
    # Save the sender ID in the database
    collection.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    # Creating inline keyboard with one button
    buttons = [
        [Button.url("Join Channel", url="https://t.me/devggn")],
        [Button.url("Contact Me", url="https://t.me/ggnhere")],
    ]
    # Sending photo with caption and buttons
    await gagan.send_file(
        event.chat_id,
        file=START_PIC,
        caption=TEXT,
        buttons=buttons
    )


@gagan.on(events.NewMessage(pattern=f"^/broadcast"))
async def broadcast(event):
    """
    Command to broadcast message to all users
    """
    if event.sender_id != OWNER_ID:
        return await event.respond("You are not authorized to use this command.")

    if len(event.message.text.split(' ', 1)) < 2:
        return await event.respond("Please provide a message to broadcast.")

    message = event.message.text.split(' ', 1)[1]
    users = list(collection.find())
    total_users = len(users)
    progress_message = await event.respond(f"Starting broadcast to {total_users} users...")

    for index, user_doc in enumerate(users):
        try:
            user_id = user_doc["user_id"]
            await gagan.send_message(user_id, message)
        except Exception as e:
            logger.error(f"Error sending message to user {user_id}: {str(e)}")

        if (index + 1) % 100 == 0:
            await progress_message.edit(f"Broadcasting... {index + 1}/{total_users} users processed.")
            time.sleep(2)  # Sleep for 2 seconds after every 100 users

    await progress_message.edit(f"Broadcast completed. Total users: {total_users}")

def thumbnail(chat_id):
    return f'{chat_id}.jpg' if os.path.exists(f'{chat_id}.jpg') else f'thumb.jpg'
    
# Function to load registered user IDs and first names from the MongoDB collection
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

# Command to get the list of registered users with their first names
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

@gagan.on(events.NewMessage(func=lambda event: event.photo))
async def save_photo_as_thumbnail(event):
    user_id = event.sender_id
    gagan_client = event.client

    # Download and save the photo as the thumbnail
    temp_path = await gagan_client.download_media(event.media)
    if os.path.exists(f'{user_id}.jpg'):
        os.remove(f'{user_id}.jpg')
    os.rename(temp_path, f'./{user_id}.jpg')

    await event.respond('Thumbnail saved successfully!')

@gagan.on(events.NewMessage(pattern='/remthumb'))
async def remove_thumbnail(event):
    user_id = event.sender_id
    gagan_client = event.client
    try:
        os.remove(f'{user_id}.jpg')
        await event.respond('Thumbnail removed successfully!')
    except FileNotFoundError:
        await event.respond("No thumbnail found to remove.")


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

REPO_URL = "https://github.com/devgaganin/Save-Restricted-Content-Bot-Repo/"

HELP_TEXT = """Here are the available commands:

➡️ /fwd - Setup forward process from public channels or private channels (your bot must be admin in private channels to clone). Follow the on-screen instructions for setup.

➡️ /bulk - to process link one by one iterating through single single message ids.

➡️ /batch - to process multiple links at once by taking start link, iterating though multple message ids.

➡️ /addsession - Save materials by logging in to your own account using the bot. To generate a session, use @stringprsnlbot. Make sure you trust the source to generate the session. 

```Use: /addsession YOURSESSION ```

➡️ /logout - Logout if you have recently added a session and want to use the bot in normal mode.

➡️ /delete - Delete words from filenames and captions if you don't want them to appear. These words should be added on the cloud and saved permanently. You don't have authorization to remove that blacklist. 

```Use: /delete word(s)/sentence(s)``` .

➡️ /setrename - Add a rename tag in the filename you save. 

```Use: /setrename RENAMETAGWORD``` 

This will add RENAMETAGWORD to your filenames automatically in batch time and set it permanently for you (until reboot).

➡️ /setchat - Forward messages directly to a groupID, channelID (with -100), or user (they must have started the bot) bot must be admin in channel or group. 

```Use: /setchat channelD```

No need to add -100 in the userid.

➡️ /setcaption - Add your own caption.

```Use: /setcaption CAPTION_TEXT```

➡️ /remthumb - Delete your thumbnail.

➡️ /cancel - Cancel ongoing batch process.

➡️ /host - host your own Save Restricted Bot with all features available in this bot.

```Use: /host BOT_TOKEN SESSION```

➡️ /unhost - to unhost the hosted bots (remember this will unhost both bot at once if you hosted both bots)

➡️ /plan - View our plan details.

➡️ /terms - View our premium terms.

➡️ /dl - download video from multiple sites.

➡️ /set - This command is used to set custom batch size, base timer, threshold limit, increase timer value. Parameters are

b = batch_size (only useful for /batch this will decide how many links will process at once)
bt = base_timer (this sets the initial sleep timer for batch command)
l = timer_increase_threshold (this sets the number of files after which the timer value will be increased)
t = increase_timer_value (this sets the timer value to increase i.e after every threshold processing limit)

```Use : /set b bt l t```

Note: To set your custom thumbnail just sent photo/image without anycommand or else.

[GitHub Repository](%s)
""" % REPO_URL


@gagan.on(events.NewMessage(pattern='/help'))
async def help_command(event):
    """
    Command to display help message
    """
    # Creating inline keyboard with a button linking to the GitHub repository
    buttons = [[Button.url("REPO", url=REPO_URL)]]

    # Sending the help message with the GitHub repository button
    await event.respond(HELP_TEXT, buttons=buttons, link_preview=False)


# Function to get video info including duration
def get_youtube_video_info(url):
    ydl_opts = {'quiet': True, 'skip_download': True}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        if not info_dict:
            return None
        return {
            'title': info_dict.get('title', 'Unknown Title'),
            'duration': info_dict.get('duration', 0),  # Duration in seconds
        }

@app.on_message(filters.command("dl", prefixes="/"))
async def youtube_dl_command(_, message):
    # Check if the command has an argument (YouTube URL)
    if len(message.command) > 1:
        youtube_url = message.command[1]
        
        # Send initial message indicating downloading
        progress_message = await message.reply("Fetching video info...")

        try:
            # Fetch video info using yt-dlp
            video_info = get_youtube_video_info(youtube_url)
            if not video_info:
                await progress_message.edit_text("Failed to fetch video info.")
                return

            # Check if video duration is greater than 3 hours (10800 seconds)
            if video_info['duration'] > 10800:
                await progress_message.edit_text("Video duration exceeds 3 hours. Not allowed.")
                return
            
            await progress_message.edit_text("Downloading video...")

            # Safe file naming
            original_file = f"{video_info['title'].replace('/', '_').replace(':', '_')}.mp4"
            thumbnail_path = f"{video_info['title'].replace('/', '_').replace(':', '_')}.jpg"

            # Download video
            ydl_opts = {
                'format': 'best',
                'outtmpl': original_file,  # Output file template
                'noplaylist': True,  # Disable downloading playlists
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])  # Start downloading the video

            # Check if the original file exists before renaming
            if not os.path.exists(original_file):
                await progress_message.edit_text("Failed to download video.")
                return

            # Edit the progress message to indicate uploading
            await progress_message.edit_text("Uploading video...")

            # Get video metadata
            metadata = video_metadata(original_file)
            caption = f"{video_info['title']}\n\n__**Powered by [Advance Content Saver Bot](https://t.me/advance_content_saver_bot)**__"  # Set caption to the title of the video
            
            # Send the video file and thumbnail
            ggn = message.chat.id
            k = thumbnail(ggn)
            await app.send_video(
                chat_id=message.chat.id,
                video=original_file,
                caption=caption,
                thumb=k,
                width=metadata['width'],
                height=metadata['height'],
                duration=metadata['duration'],
            )

            # Clean up downloaded files
            os.remove(original_file)
            # os.remove(thumbnail_path)

            # Delete the progress message after sending video
            await progress_message.delete()

        except Exception as e:
            await progress_message.edit_text(f"An error occurred: {str(e)}")

    else:
        await message.reply("Please provide a YouTube URL after /dl.")

def video_metadata(file):
    vcap = cv2.VideoCapture(f'{file}')
    width = round(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = round(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vcap.get(cv2.CAP_PROP_FPS)
    frame_count = vcap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = round(frame_count / fps)
    return {'width': width, 'height': height, 'duration': duration}
