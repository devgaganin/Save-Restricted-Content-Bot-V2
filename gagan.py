from pyrogram import Client, filters
import re
import pymongo
import sys
import math
import os
import time
from datetime import datetime as dt
import json
import asyncio
import cv2
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from pyrogram.errors import InviteHashInvalid, InviteHashExpired, ChatAdminRequired, UserAlreadyParticipant
from pyrogram.errors import FloodWait, RPCError


# Your API ID, API HASH, and String Session fill these
API_ID = 1234
API_HASH = ""
STRING_SESSION = ""
BOT_TOKEN = ""
MONGODB_CONNECTION_STRING = ""
OWNER_ID = 12345

# Create a Pyrogram Client
app = Client(
    name="gagan",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)

userbot = Client("myacc", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

@userbot.on_message(filters.command("nice") & filters.reply)
async def src_file(_, message):
    # Check if the replied message has any media
    await message.delete()
    if message.reply_to_message and message.reply_to_message.media:
        # Download the media
        file_path = await userbot.download_media(message.reply_to_message)

        # Send the downloaded media to yourself based on its type
        if message.reply_to_message.photo:
            await userbot.send_photo('me', file_path)
        elif message.reply_to_message.video:
            await userbot.send_video('me', file_path)
        elif message.reply_to_message.document:
            await userbot.send_document('me', file_path)
        else:
            await userbot.send_message('me', "Unsupported file type.")

        # Delete the downloaded file
        os.remove(file_path)
    else:
        # If the replied message does not contain any media, inform the user
        await message.reply_text("Please reply to a message containing media to save it.")
try:
    userbot.start()
except BaseException:
    print("Your session expired please re add that... thanks @dev_gagan.")
    sys.exit(1)


# MongoDB database name and collection name
DB_NAME = "pyrosrc"
COLLECTION_NAME = "pyrosrc"

mongo_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

# Dictionary to store user caption preferences
user_caption_preferences = {}

video_extensions = ['mkv', 'mp4', 'webm', 'avi', 'mov', 'flv', 'wmv', 'm4v', 'mpg', 'mpeg', 'mpe', 'mpv', '3gp', '3g2', 'ts', 'mts', 'm2ts', 'f4v', 'f4p', 'f4a', 'f4b', 'ogv', 'vob', 'rm', 'rmvb', 'divx', 'xvid', 'asf', 'mxf', 'm1v', 'm2v', 'dv', 'svi', 'mjpg', 'mjpeg', 'ogm', 'dat', 'qt', 'yuv', 'vcd', 'h264', 'h265', 'm2p', 'mp2', 'mpv2', 'scm', 'tod', 'trp', 'vdr', 'vp6', 'vp7', 'vro', 'wtv', 'xesc']

# State variables
batch_start_link = {}
batch_message_count = {}
batch_current_count = {}
batch_in_progress = {}

user_chat_ids = {}
user_rename_preferences = {}

# Function to save user to MongoDB
def save_user_to_db(user_id, first_name):
    if not collection.find_one({"user_id": user_id}):
        collection.insert_one({"user_id": user_id, "first_name": first_name})

# Function to get registered users from MongoDB
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


async def set_rename_command(user_id, custom_rename_tag):
    # Update the user_rename_preferences dictionary
    user_rename_preferences[str(user_id)] = custom_rename_tag

def get_user_rename_preference(user_id):
    # Retrieve the user's custom renaming tag if set, or default to '@pyrosrcbot'
    return user_rename_preferences.get(str(user_id), '@pyrosrcbot')

async def set_chat_id(client, message):
    try:
        chat_id = int(message.text.split(" ", 1)[1])
        user_chat_ids[message.from_user.id] = chat_id
        await message.reply_text("Chat ID set successfully!")
    except (IndexError, ValueError):
        await message.reply_text("Invalid chat ID!")

@app.on_message(filters.command("setchat"))
async def set_chat_id_handler(client, message):
    await set_chat_id(client, message)

@app.on_message(filters.command("setrename"))
async def set_rename_command_handler(client, message):
    # Parse the custom rename tag from the command
    command_parts = message.text.split(' ')
    if len(command_parts) < 2:
        await message.reply_text("Please provide a custom rename tag!")
        return

    custom_rename_tag = ' '.join(command_parts[1:])

    # Call the function to set the custom rename tag
    await set_rename_command(message.from_user.id, custom_rename_tag)
    await message.reply_text(f"Custom rename tag set to: {custom_rename_tag}")

# Function to load delete words for a user from MongoDB
def load_delete_words(user_id):
    try:
        words_data = collection.find_one({"_id": user_id})
        if words_data:
            return set(words_data.get("delete_words", []))
        else:
            return set()
    except Exception as e:
        print(f"Error loading delete words: {e}")
        return set()

# Function to save delete words for a user to MongoDB
def save_delete_words(user_id, delete_words):
    try:
        collection.update_one(
            {"_id": user_id},
            {"$set": {"delete_words": list(delete_words)}},
            upsert=True
        )
    except Exception as e:
        print(f"Error saving delete words: {e}")

# Function to set custom caption preference for a user
async def set_caption_command(user_id, custom_caption):
    user_caption_preferences[str(user_id)] = custom_caption
    # You can optionally save this preference to MongoDB if needed

# Function to get user's custom caption preference
def get_user_caption_preference(user_id):
    return user_caption_preferences.get(str(user_id), '')

@app.on_message(filters.command("start"))
async def start(_, message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    # Save the user to MongoDB
    save_user_to_db(user_id, first_name)

    gagan_text = (
        "Welcome to Advance SRC Bot [Pyrogram V2 Based]\n\n"
        "Send me the Link of any message of Restricted Channels to Clone it here. For private channel's messages, send the Invite Link first.\n\n"
        "Send /help to know how to use this bot."
    )

    # Create the join button
    join_button = InlineKeyboardButton(
        text="Join Channel",
        url="https://t.me/save_restricted_content_bots"
    )

    photo_path = "https://graph.org/file/4e80dc2f4f6f2ddadb4d2.jpg"
    # Create inline keyboard markup with the button
    reply_markup = InlineKeyboardMarkup([[join_button]])

    # Reply to the user with the additional text and the button
    await message.reply_photo(photo_path, caption=gagan_text, reply_markup=reply_markup)

@app.on_message(filters.command("get"))
async def get_registered_users_command(_, message):
    # Check if the command is initiated by the owner
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("You are not authorized to use this command.")
    
    # Get all registered user IDs and first names
    registered_users = get_registered_users()

    # Save user IDs and first names to a text file
    filename = "registered_users.txt"
    save_user_ids_to_txt(registered_users, filename)

    # Send the text file
    await message.reply_document(filename)
    os.remove(filename)  # Remove the temporary file after sending

@app.on_message(filters.command("gcast") & filters.reply)
async def broadcast_message(_, message):
    # Check if the command is initiated by the owner
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("You are not authorized to use this command.")
    
    # Get all registered user IDs
    registered_users = get_registered_users()

    # Broadcast the replied message to all registered users
    for user_id, _ in registered_users:
        try:
            if message.reply_to_message.photo:
                await app.send_photo(user_id, message.reply_to_message.photo.file_id, caption=message.reply_to_message.caption)
            elif message.reply_to_message.video:
                await app.send_video(user_id, message.reply_to_message.video.file_id, caption=message.reply_to_message.caption)
            elif message.reply_to_message.document:
                await app.send_document(user_id, message.reply_to_message.document.file_id, caption=message.reply_to_message.caption)
            elif message.reply_to_message.text:
                await app.send_message(user_id, message.reply_to_message.text)
            await asyncio.sleep(1)  # Delay of 1 second to avoid flood
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

def thumbnail(chat_id):
    return f'{chat_id}.jpg' if os.path.exists(f'{chat_id}.jpg') else f'thumb.jpg'

# Define a handler for the /help command
@app.on_message(filters.command("help"))
async def start(_, message):
    await message.delete()
    additional_text = (
        "Welcome to Advance SRC Bot [Pyrogram V2 Based]\n\n"
        "How to use?\n"
        "1) Join: Send `InviteLink` to add the bot to your channel (not needed for public channels).\n\n"
        "2) Batch: Send \n`/batch firstpostlink range`, \nwhere range is the number of messages you want to process in a batch (max 100).\n\n"
        "3) Don't have a link? Add your session using \n`/addsession SESSION`.\n\n"
        "4) Delete: Send \n`/delete WORD`\nto delete words/sentence from caption\n\n"
        "5) Custom Caption: Send `/setcaption CAPTIONTEXT`\n\n"
        "6) How to generate session?\n\n"
        "--- Generate SESSION from @stringprsnlbot or from any where you trust and after that send \n`/addsession SESSION`\n\n"
        "6) Custom Thumbnail: Send a photo to bot and reply **/setthumb** to that photo\n\n"
        "__Note: It does not reply to a single message link; you must always send the /batch command and can process up to 1000 messages at once.__\n\n"
        "**__Powered by Team SPY__**"
    )

    # Create the join button
    join_button = InlineKeyboardButton(
        text="Join Channel",
        url="https://t.me/devggn"
    )

    # Create inline keyboard markup with the button
    reply_markup = InlineKeyboardMarkup([[join_button]])

    # Reply to the user with the additional text and the button
    await message.reply_text(additional_text, reply_markup=reply_markup)


@app.on_message(filters.command("setcaption"))
async def setcaption_command_handler(_, message):
    user_id = message.from_user.id
    custom_caption = ' '.join(message.command[1:])
    
    if not custom_caption:
        await message.reply_text("Please provide a custom caption.")
        return
    
    await set_caption_command(user_id, custom_caption)
    await message.reply_text(f"Custom caption set to: {custom_caption}")

# /delete command handler (to add words to delete list)
@app.on_message(filters.command("delete"))
async def delete_command_handler(_, message):
    user_id = message.from_user.id
    words_to_delete = message.command[1:]
    
    if not words_to_delete:
        await message.reply_text("Please provide word(s) to delete!")
        return
    
    user_delete_words = load_delete_words(user_id)
    
    for word in words_to_delete:
        user_delete_words.add(word)
    
    save_delete_words(user_id, user_delete_words)
    
    await message.reply_text(f"Word(s) added to your list of words to delete: {', '.join(words_to_delete)}")


user_sessions = {}

@app.on_message(filters.command('addsession') & filters.private)
async def add_session_command_handler(client, message):
    """
    Command to add user session
    """
    # Parse the user session string from the command
    try:
        _, user_session = message.text.split(' ', 1)  # Split only once to capture the session string
    except ValueError:
        return await message.reply_text("Invalid /addsession command. Use /addsession SESSION_STRING.")

    # Store the session string for the user (identified by sender_id)
    sender_id = message.from_user.id
    user_sessions[sender_id] = user_session
    await message.reply_text("Session string added successfully.")


@app.on_message(filters.command("logout"))
async def del_session_command_handler(client, message):
    """
    Command to delete user session
    """
    # Get the sender ID
    sender_id = message.from_user.id

    # Check if the user has a session
    if sender_id in user_sessions:
        # Delete the session
        del user_sessions[sender_id]
        await message.reply_text("Session string deleted successfully.")
    else:
        await message.reply_text("No session found for the user.")

# Define a command handler for /setthumb

@app.on_message(filters.command("setthumb") & filters.reply)
async def save_file(_, message):
    # Check if the replied message has any media
    await message.delete()
    if message.reply_to_message and message.reply_to_message.media:
        # Check if the media is a photo
        if message.reply_to_message.photo:
            # Download the photo
            file_path = await app.download_media(message.reply_to_message)

            # Get the chat ID (user's ID)
            chat_id = message.chat.id

            # Construct the filename using the chat ID
            filename = f"{chat_id}.jpg"

            # Check if the file already exists
            if os.path.exists(filename):
                # Remove the existing file
                os.remove(filename)

            os.rename(file_path, filename)

            # Respond with a success message
            await message.reply(f"Thumbnail saved successfully...")
        else:
            await message.reply("The replied media is not a photo.")
    else:
        await message.reply("No media found in the replied message.")

@app.on_message(filters.command("remthumb"))
async def remove_thumbnail(_, message):
    await message.delete()
    chat_id = message.chat.id
    filename = f"{chat_id}.jpg"
    
    if os.path.exists(filename):
        os.remove(filename)
        await message.reply("Thumbnail removed successfully.")
    else:
        await message.reply("No thumbnail found to remove.")


# Define a handler for the /cancel command
@app.on_message(filters.command("cancel"))
async def cancel_command_handler(_, message):
    await message.delete()
    chat_id = message.chat.id

    # Check if batch processing is ongoing for this user
    if chat_id in batch_in_progress and batch_in_progress[chat_id]:
        # Clear batch processing state for this user
        batch_in_progress[chat_id] = False  # Set batch_in_progress to False to stop further processing

        await message.reply_text("Batch processing canceled.")
    else:
        await message.reply_text("No active batch processing to cancel.")

@app.on_message(filters.command("batch"))
async def batch_command_handler(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text[len("/batch"):].strip()

    # Check if batch processing is ongoing for this user
    if chat_id in batch_in_progress and batch_in_progress[chat_id]:
        await message.reply_text("Batch processing is already ongoing. Wait for it to finish or cancel.")
        return

    # Parse the provided parameters
    params = text.split()
    if len(params) != 2:
        await message.reply_text("Invalid parameters. Please use '/batch postlink number_of_messages'.")
        return

    post_link = params[0]
    try:
        num_messages = int(params[1])
    except ValueError:
        await message.reply_text("Invalid number of messages. Please provide a valid integer.")
        return

    # Check the maximum number of messages unless it's the OWNER
    if user_id != OWNER_ID and num_messages > 100:
        await message.reply_text("Limit is 100. Purchase Premium to go beyond limits...")
        return

    # Validate the post link format
    if not (post_link.startswith('https://t.me/') or post_link.startswith('https://t.me/c/')):
        await message.reply_text("Invalid starting post link. Please provide a valid link.")
        return

    # Start batch processing
    await handle_batch_processing(client, message, post_link, num_messages)

async def handle_batch_processing(client, message, start_link, num_messages):
    chat_id = message.chat.id

    # Ensure batch setup is complete
    batch_start_link[chat_id] = start_link
    batch_message_count[chat_id] = num_messages
    batch_current_count[chat_id] = 0
    batch_in_progress[chat_id] = True

    try:
        if start_link.startswith('https://t.me/c/'):
            match = re.match(r'https://t.me/c/(\d+)(/\d+)?/(\d+)', start_link)
            if match:
                private_chat_id = int(match.group(1))
                private_chat_id = f'-100{private_chat_id}'
                private_chat_id = int(private_chat_id)
                post_id = int(match.group(3))

                for i in range(num_messages):
                    message_id = post_id + i

                    await handle_private_channel_post_link(client, message, private_chat_id, message_id)

                    # Check if batch processing needs to be canceled
                    if not batch_in_progress[chat_id]:
                        # await message.reply_text("Batch processing canceled.")
                        return

                # Reset batch variables after completion
                batch_start_link[chat_id] = None
                batch_message_count[chat_id] = 0
                batch_current_count[chat_id] = 0
                batch_in_progress[chat_id] = False

                # Send completion message
                await message.reply_text("Task Completed.")
            else:
                await message.reply_text("Invalid private channel link.")
        else:
            match = re.match(r'https://t.me/([^/]+)/(\d+)', start_link)
            if match:
                chat_username = match.group(1)
                start_message_id = int(match.group(2))

                for i in range(num_messages):

                    message_link = f"https://t.me/{chat_username}/{start_message_id + i}"
                    await handle_telegram_post_link(client, message, message_link)

                    # Check if batch processing needs to be canceled
                    if not batch_in_progress[chat_id]:
                        # await message.reply_text("Batch processing canceled.")
                        return

                # Reset batch variables after completion
                batch_start_link[chat_id] = None
                batch_message_count[chat_id] = 0
                batch_current_count[chat_id] = 0
                batch_in_progress[chat_id] = False

                # Send completion message
                await message.reply_text("Task Completed.")
            else:
                await message.reply_text("Invalid starting post link.")
    except Exception as e:
        print(f"Error during batch processing: {e}")
        await message.reply_text("Error occurred during batch processing. Please try again later.")


async def handle_telegram_post_link(_, message, post_link):
    chat_id = message.chat.id

    match = re.match(r'https://t.me/([^/]+)/(\d+)', post_link)
    if match:
        chat_username = match.group(1)
        message_id = int(match.group(2))

        # Fetch the message using get_messages
        try:
            msg = await app.get_messages(chat_username, message_id)
        except Exception as e:
            await message.reply_text(f"Error fetching message: {e}")
            return

        # Retrieve custom caption preference
        custom_caption = get_user_caption_preference(chat_id)
        original_caption = msg.caption if msg.caption else ''
        final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"

        # Handle deletion of words from caption based on user preferences
        delete_words = load_delete_words(chat_id)
        for word in delete_words:
            final_caption = final_caption.replace(word, '')

        # Clean up final caption formatting
        final_caption = re.sub(r'\s{2,}', ' ', final_caption.strip())
        final_caption = re.sub(r'\n{2,}', '\n', final_caption)
        
        # Construct the final caption with custom text if provided
        caption = f"{final_caption}\n__**{custom_caption}**__" if custom_caption else f"{final_caption}\n\n__**Powered by [PYRO SRC (β)](https://t.me/pyrosrcbot)**__"
        gagan = message.chat.id
        hanuman = user_chat_ids.get(gagan, gagan)

        # Handle different message types and send them to the current chat
        if msg.text:
            await app.copy_message(hanuman, chat_username, message_id, caption=caption)
        elif msg.photo:
            await app.send_photo(hanuman, msg.photo.file_id, caption=caption)
        elif msg.video:
            await app.send_video(hanuman, msg.video.file_id, caption=caption)
        elif msg.animation:
            await app.send_animation(hanuman, msg.animation.file_id, caption=caption)
        elif msg.sticker:
            await app.send_sticker(hanuman, msg.sticker.file_id)
        elif msg.voice:
            await app.send_voice(hanuman, msg.voice.file_id, caption=caption)
        elif msg.audio:
            await app.send_audio(hanuman, msg.audio.file_id, caption=caption)
        elif msg.document:
            await app.send_document(hanuman, msg.document.file_id, caption=caption)
        elif msg.video_note:
            await app.send_video_note(hanuman, msg.video_note.file_id)
        elif msg.media_group_id:
            media_group = await app.get_media_group(chat_username, message_id)
            media_group_files = [await media.download() for media in media_group]
            await app.send_media_group(hanuman, media_group_files, caption=caption)
        else:
            None

        sleep_message = await message.reply_text("Sleeping for 2 seconds...")
        await asyncio.sleep(5)
        await sleep_message.delete()

        # Update current message count for batch processing
        batch_current_count[chat_id] += 1

        # Check if batch processing needs to be canceled
        if not batch_in_progress[chat_id]:
            # await message.reply_text("Batch processing canceled.")
            return

        # Continue with the next message in batch if not completed
        if batch_current_count[chat_id] < batch_message_count[chat_id]:
            next_message_id = message_id + 1
            next_post_link = f"https://t.me/{chat_username}/{next_message_id}"
            await handle_telegram_post_link(_, message, next_post_link)
    else:
        await message.reply_text("Invalid Telegram post link.")

def TimeFormatter(milliseconds) -> str:
    milliseconds = int(milliseconds) * 1000
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)}d, " if days else "")
        + (f"{str(hours)}h, " if hours else "")
        + (f"{str(minutes)}m, " if minutes else "")
        + (f"{str(seconds)}s, " if seconds else "")
        + (f"{str(milliseconds)}ms, " if milliseconds else "")
    )
    return tmp[:-2]

#--------------------------------------------
def humanbytes(size):
    size = int(size)
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {Dic_powerN[n]}B"


FINISHED_PROGRESS_STR = "🟢"
UN_FINISHED_PROGRESS_STR = "🔴"
DOWNLOAD_LOCATION = "/downloads"

async def progress_for_pyrogram(current, total, bot, ud_type, progress_message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        status = f"{DOWNLOAD_LOCATION}/status.json"
        if os.path.exists(status):
            with open(status, 'r+') as f:
                statusMsg = json.load(f)
                if not statusMsg["running"]:
                    bot.stop_transmission()
        speed = current / diff
        elapsed_time = round(diff) * 1
        time_to_completion = round((total - current) / speed) * 1
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "**{0}{1}** \n".format(
            ''.join(FINISHED_PROGRESS_STR for _ in range(math.floor(percentage / 10))),
            ''.join(UN_FINISHED_PROGRESS_STR for _ in range(10 - math.floor(percentage / 10))),
        )

        tmp = progress + "**\n__Completed__:** {0} of {1}\n**__Speed__**: {2}/s\n**__Time__**: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            text = f"{ud_type}\n {tmp}"
            if progress_message.text != text or progress_message.caption != text:
                if not progress_message.photo:
                    await progress_message.edit_text(text=f"{ud_type}\n {tmp}")
                else:
                    await progress_message.edit_caption(caption=f"{ud_type}\n {tmp}")
        except Exception as e:
            print(f"Error updating progress: {e}")


# Define hhmmss, screenshot, and video_metadata functions
def hhmmss(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

async def screenshot(video, duration, sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    time_stamp = hhmmss(int(duration) / 2)
    out = dt.now().isoformat("_", "seconds") + ".jpg"
    cmd = ["ffmpeg",
           "-ss",
           f"{time_stamp}",
           "-i",
           f"{video}",
           "-frames:v",
           "1",
           f"{out}",
           "-y"
          ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if os.path.isfile(out):
        return out
    else:
        return None

def video_metadata(file):
    vcap = cv2.VideoCapture(f'{file}')
    width = round(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = round(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vcap.get(cv2.CAP_PROP_FPS)
    frame_count = vcap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = round(frame_count / fps)
    return {'width': width, 'height': height, 'duration': duration}

# Main function
async def handle_private_channel_post_link(_, message, chat_id, message_id):
    try:
        sender = message.chat.id
        user_session = user_sessions.get(sender)
        session_name = f"{chat_id}_app"
        
        if user_session:
            user_bot = Client(
                session_name,
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=user_session
            )
            await user_bot.start()
            msg = await user_bot.get_messages(chat_id, message_id)
        else:
            msg = await userbot.get_messages(chat_id, message_id)

        custom_caption = get_user_caption_preference(message.chat.id)
        original_caption = msg.caption if msg.caption else ''
        final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"

        delete_words = load_delete_words(message.chat.id)
        for word in delete_words:
            final_caption = final_caption.replace(word, '')

        final_caption = re.sub(r'\s{2,}', ' ', final_caption.strip())
        final_caption = re.sub(r'\n{2,}', '\n', final_caption)

        caption = f"{final_caption}\n__**{custom_caption}**__" if custom_caption else f"{final_caption}\n\n__**Powered by [PYRO SRC (β)](https://t.me/pyrosrcbot)**__"

        progress_message = await message.reply_text("Processing...")

        start_time = time.time()
        gagan = message.chat.id
        hanuman = user_chat_ids.get(gagan, gagan)
        
        async def send_media(media_type, file, caption, metadata=None):
            try:
                sender = message.chat.id
                thumb_path = None
                if media_type == "video":
                    thumb_path = await screenshot(file, metadata['duration'], sender)

                if media_type == "photo":
                    await app.send_photo(hanuman, file, caption=caption, progress=progress_for_pyrogram, progress_args=(app, "Uploading Photo\n", progress_message, start_time))
                elif media_type == "video":
                    await app.send_video(hanuman, file, caption=caption, thumb=thumb_path, width=metadata['width'], height=metadata['height'], duration=metadata['duration'], progress=progress_for_pyrogram, progress_args=(app, "Uploading Video\n", progress_message, start_time))
                elif media_type == "animation":
                    await app.send_animation(hanuman, file, caption=caption, progress=progress_for_pyrogram, progress_args=(app, "Uploading Animation\n", progress_message, start_time))
                elif media_type == "sticker":
                    await app.send_sticker(hanuman, file, progress=progress_for_pyrogram, progress_args=(app, "Uploading Sticker\n", progress_message, start_time))
                elif media_type == "voice":
                    await app.send_voice(hanuman, file, caption=caption, progress=progress_for_pyrogram, progress_args=(app, "Uploading Voice\n", progress_message, start_time))
                elif media_type == "audio":
                    await app.send_audio(hanuman, file, caption=caption, progress=progress_for_pyrogram, progress_args=(app, "Uploading Audio\n", progress_message, start_time))
                elif media_type == "document":
                    x = message.chat.id
                    k = thumbnail(x)
                    await app.send_document(hanuman, file, caption=caption, thumb=k, progress=progress_for_pyrogram, progress_args=(app, "Uploading Document\n", progress_message, start_time))
                elif media_type == "video_note":
                    await app.send_video_note(hanuman, file, progress=progress_for_pyrogram, progress_args=(app, "Uploading Video Note\n", progress_message, start_time))
                # await progress_message.delete()
            except Exception as e:
                await progress_message.edit_text(f"Error sending {media_type}: {e}")

        if msg.text:
            await app.send_message(hanuman, msg.text)
            await progress_message.delete()
        else:
            media_type = ""
            if msg.photo:
                media_type = "photo"
            elif msg.video:
                media_type = "video"
            elif msg.animation:
                media_type = "animation"
            elif msg.sticker:
                media_type = "sticker"
            elif msg.voice:
                media_type = "voice"
            elif msg.audio:
                media_type = "audio"
            elif msg.document:
                media_type = "document"
            elif msg.video_note:
                media_type = "video_note"

            if media_type:
                if user_session:
                    file = await user_bot.download_media(msg, progress=progress_for_pyrogram, progress_args=(app, f"Downloading {media_type.capitalize()}\n", progress_message, start_time))
                    await user_bot.stop()
                else:
                    file = await userbot.download_media(msg, progress=progress_for_pyrogram, progress_args=(app, f"Downloading {media_type.capitalize()}\n", progress_message, start_time))
                
                custom_rename_tag = get_user_rename_preference(message.chat.id)
                last_dot_index = str(file).rfind('.')
                if last_dot_index != -1 and last_dot_index != 0:
                    original_file_name = str(file)[:last_dot_index]
                    file_extension = str(file)[last_dot_index + 1:]
                else:
                    original_file_name = str(file)
                    file_extension = 'mp4'
                
                delete_words = load_delete_words(message.chat.id)
                for word in delete_words:
                    original_file_name = original_file_name.replace(word, "")
                
                new_file_name = original_file_name + " " + custom_rename_tag + "." + file_extension
                os.rename(file, new_file_name)
                file = new_file_name
                if file_extension.lower() in video_extensions:
                    media_type = "video"
                    metadata = video_metadata(file)
                else:
                    metadata = None

                await send_media(media_type, file, caption, metadata)
                os.remove(file)
            elif msg.media_group_id:
                if user_session:
                    media_group = await user_bot.get_media_group(chat_id, message_id)
                    await user_bot.stop()
                else:
                    media_group = await userbot.get_media_group(chat_id, message_id)
                media_group_files = [await media.download(progress=progress_for_pyrogram, progress_args=(app, "Downloading Media Group\n", progress_message, start_time)) for media in media_group]
                await app.send_media_group(hanuman, media_group_files, caption=caption, progress=progress_for_pyrogram, progress_args=(app, "Uploading Media Group\n", progress_message, start_time))
                # await progress_message.delete()

            await progress_message.delete()
            sleep_message = await message.reply_text("Sleeping for 2 seconds before processing next message...")
            await asyncio.sleep(5)
            await sleep_message.delete()

        batch_current_count[message.chat.id] += 1

        if not batch_in_progress[message.chat.id]:
            return

        if batch_current_count[message.chat.id] < batch_message_count[message.chat.id]:
            next_message_id = message_id + 1
            await handle_private_channel_post_link(_, message, chat_id, next_message_id)
    except Exception as e:
        await message.reply_text(f"Error processing post: {e}")

async def handle_private_link(_, message, chat_id, message_id):
    try:
        sender = message.chat.id
        user_session = user_sessions.get(sender)
        session_name = f"{chat_id}_app"

        if user_session:
            user_bot = Client(
                session_name,
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=user_session
            )
            await user_bot.start()
            msg = await user_bot.get_messages(chat_id, message_id)
        else:
            msg = await userbot.get_messages(chat_id, message_id)

        custom_caption = get_user_caption_preference(message.chat.id)
        original_caption = msg.caption if msg.caption else ''
        final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"

        delete_words = load_delete_words(message.chat.id)
        for word in delete_words:
            final_caption = final_caption.replace(word, '')

        final_caption = re.sub(r'\s{2,}', ' ', final_caption.strip())
        final_caption = re.sub(r'\n{2,}', '\n', final_caption)

        caption = f"{final_caption}\n__**{custom_caption}**__" if custom_caption else f"{final_caption}\n\n__**Powered by [PYRO SRC (β)](https://t.me/pyrosrcbot)**__"

        progress_message = await message.reply_text("Processing...")

        start_time = time.time()
        gagan = message.chat.id
        hanuman = user_chat_ids.get(gagan, gagan)

        async def send_media(media_type, file, caption, metadata=None):
            try:
                sender = message.chat.id
                thumb_path = None
                if media_type == "video":
                    thumb_path = await screenshot(file, metadata['duration'], sender)

                if media_type == "photo":
                    await app.send_photo(hanuman, file, caption=caption, progress=progress_for_pyrogram, progress_args=(app, "Uploading Photo\n", progress_message, start_time))
                elif media_type == "video":
                    await app.send_video(hanuman, file, caption=caption, thumb=thumb_path, width=metadata['width'], height=metadata['height'], duration=metadata['duration'], progress=progress_for_pyrogram, progress_args=(app, "Uploading Video\n", progress_message, start_time))
                elif media_type == "animation":
                    await app.send_animation(hanuman, file, caption=caption, progress=progress_for_pyrogram, progress_args=(app, "Uploading Animation\n", progress_message, start_time))
                elif media_type == "sticker":
                    await app.send_sticker(hanuman, file, progress=progress_for_pyrogram, progress_args=(app, "Uploading Sticker\n", progress_message, start_time))
                elif media_type == "voice":
                    await app.send_voice(hanuman, file, caption=caption, progress=progress_for_pyrogram, progress_args=(app, "Uploading Voice\n", progress_message, start_time))
                elif media_type == "audio":
                    await app.send_audio(hanuman, file, caption=caption, progress=progress_for_pyrogram, progress_args=(app, "Uploading Audio\n", progress_message, start_time))
                elif media_type == "document":
                    x = message.chat.id
                    k = thumbnail(x)
                    await app.send_document(hanuman, file, caption=caption, thumb=k, progress=progress_for_pyrogram, progress_args=(app, "Uploading Document\n", progress_message, start_time))
                elif media_type == "video_note":
                    await app.send_video_note(hanuman, file, progress=progress_for_pyrogram, progress_args=(app, "Uploading Video Note\n", progress_message, start_time))
                await progress_message.delete()
            except Exception as e:
                await progress_message.edit_text(f"Error sending {media_type}: {e}")

        if msg.text:
            await app.send_message(hanuman, msg.text)
            await progress_message.delete()
        else:
            media_type = ""
            if msg.photo:
                media_type = "photo"
            elif msg.video:
                media_type = "video"
            elif msg.animation:
                media_type = "animation"
            elif msg.sticker:
                media_type = "sticker"
            elif msg.voice:
                media_type = "voice"
            elif msg.audio:
                media_type = "audio"
            elif msg.document:
                media_type = "document"
            elif msg.video_note:
                media_type = "video_note"

            if media_type:
                if user_session:
                    file = await user_bot.download_media(msg, progress=progress_for_pyrogram, progress_args=(app, f"Downloading {media_type.capitalize()}\n", progress_message, start_time))
                    await user_bot.stop()
                else:
                    file = await userbot.download_media(msg, progress=progress_for_pyrogram, progress_args=(app, f"Downloading {media_type.capitalize()}\n", progress_message, start_time))
                
                custom_rename_tag = get_user_rename_preference(message.chat.id)
                last_dot_index = str(file).rfind('.')
                if last_dot_index != -1 and last_dot_index != 0:
                    original_file_name = str(file)[:last_dot_index]
                    file_extension = str(file)[last_dot_index + 1:]
                else:
                    original_file_name = str(file)
                    file_extension = 'mp4'
                
                delete_words = load_delete_words(message.chat.id)
                for word in delete_words:
                    original_file_name = original_file_name.replace(word, "")
                
                new_file_name = original_file_name + " " + custom_rename_tag + "." + file_extension
                os.rename(file, new_file_name)
                file = new_file_name

                # Check file extension and change media_type to "video" if it matches video extensions
                if file_extension.lower() in video_extensions:
                    media_type = "video"
                    metadata = video_metadata(file)
                else:
                    metadata = None

                await send_media(media_type, file, caption, metadata)
                os.remove(file)
            elif msg.media_group_id:
                if user_session:
                    media_group = await user_bot.get_media_group(chat_id, message_id)
                    await user_bot.stop()
                else:
                    media_group = await userbot.get_media_group(chat_id, message_id)
                media_group_files = [await media.download(progress=progress_for_pyrogram, progress_args=(app, "Downloading Media Group\n", progress_message, start_time)) for media in media_group]
                await app.send_media_group(hanuman, media_group_files, caption=caption, progress=progress_for_pyrogram, progress_args=(app, "Uploading Media Group\n", progress_message, start_time))
                await progress_message.delete()

    except Exception as e:
        pass

# Define the on_message handler for t.me/c links
@app.on_message(filters.regex(r'https://t\.me/c/\d+/\d+') & ~filters.me)
async def handle_t_me_c_links(client, message):
    match_c = re.match(r'https://t\.me/c/(\d+)/(\d+)', message.text)
    if match_c:
        try:
            chat_id_str = match_c.group(1)
            chat_id = int(f"-100{chat_id_str}")  # Applying -100 prefix for channel ids
            message_id = int(match_c.group(2))
            await handle_private_link(client, message, chat_id, message_id)
        except Exception as e:
            await message.reply_text(f"Error processing t.me/c link: {e}")

# Define the on_message handler for t.me links
@app.on_message(filters.regex(r'^https://t\.me/[^/]+/\d+') & ~filters.me)
async def handle_telegram_public_link(app, message):
    # Check if the link is valid and starts with 't.me/' but not 't.me/c'
    match = re.match(r'^https://t\.me/([^/]+)/(\d+)$', message.text)
    if match and not message.text.startswith('t.me/c'):
        try:
            chat_username = match.group(1)
            message_id = int(match.group(2))
            
            # Fetch the message using get_messages
            msg = await app.get_messages(chat_username, message_id)
            custom_caption = get_user_caption_preference(message.chat.id)
            original_caption = msg.caption if msg.caption else ''
            final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
            delete_words = load_delete_words(message.chat.id)
            for word in delete_words:
                final_caption = final_caption.replace(word, '')
            final_caption = re.sub(r'\s{2,}', ' ', final_caption.strip())
            final_caption = re.sub(r'\n{2,}', '\n', final_caption)
            caption = f"{final_caption}\n__**{custom_caption}**__" if custom_caption else f"{final_caption}\n\n__**Powered by [PYRO SRC (β)](https://t.me/pyrosrcbot)**__"
            gagan = message.chat.id
            hanuman = user_chat_ids.get(gagan, gagan)
            # Handle the message based on its type
            if msg.photo:                
                await app.send_photo(hanuman, msg.photo.file_id, caption=caption)
            elif msg.video:                
                await app.send_video(hanuman, msg.video.file_id, caption=caption)
            elif msg.animation:                
                await app.send_animation(hanuman, msg.animation.file_id, caption=caption)
            elif msg.sticker:
                await app.send_sticker(hanuman, msg.sticker.file_id)
            elif msg.voice:
                await app.send_voice(hanuman, msg.voice.file_id)
            elif msg.audio:                
                await app.send_audio(hanuman, msg.audio.file_id, caption=caption)
            elif msg.document:               
                await app.send_document(hanuman, msg.document.file_id, caption=caption)
            elif msg.text:
                await app.copy_message(hanuman, chat_username, message_id)
            else:
                await app.send_message(hanuman, "Unsupported message type.")
        except Exception as e:
            await message.reply_text(f"Bot is not in the channel send invite link or add your session.")


async def join(userbot, invite_link):
    try:
        await userbot.join_chat(invite_link)
        return "Successfully joined the Channel"
    except UserAlreadyParticipant:
        return "User is already a participant."
    except (InviteHashInvalid, InviteHashExpired):
        return "Could not join. Maybe your link is expired or Invalid."
    except FloodWait:
        return "Too many requests, try again later."
    except Exception as e:
        print(e)
        return f"{e} \nCould not join, try joining manually."

# Define the join_channel function
async def join_channel(userbot, invite_link):
    try:
        result = await join(userbot, invite_link)
        return result
    except Exception as e:
        print(f"Error joining channel: {e}")
        return f"Could not join channel: {e}"

# Define the on_message handler for bot
@app.on_message(filters.text & ~filters.me)
async def handle_messages(_, message):
    text = message.text

    # Check if the message contains a t.me link
    if "t.me/+" in text or "t.me/join" in text:
        # Extract t.me link(s) from the message
        links = re.findall(r"(https?://t\.me/(?:\+[^\s/]+|joinchat/[^\s/]+))", text)
        for link in links:
            # Attempt to join the channel using userbot
            result = await join_channel(userbot, link)
            await message.reply_text(result)
            
# Start the client
app.run()
