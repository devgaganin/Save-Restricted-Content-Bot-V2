# Join t.me/devggn
import re
import asyncio, time, os
import pymongo
from pyrogram.enums import ParseMode , MessageMediaType
from .. import Bot, bot
from main.plugins.progress import progress_for_pyrogram
from main.plugins.helpers import screenshot
from pyrogram import Client, filters
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid, FloodWait
from pyrogram.raw.functions.channels import GetMessages
# from pyrogram.raw.types import InputChannel, InputMessage
from main.plugins.helpers import video_metadata
from main.plugins.config import MONGODB_CONNECTION_STRING, LOG_GROUP, OWNER_ID
from telethon import events
import logging
logging.basicConfig(level=logging.debug,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger("telethon").setLevel(logging.INFO)


# MongoDB database name and collection name
DB_NAME = "smart_users"
COLLECTION_NAME = "super_user"

# Establish a connection to MongoDB
mongo_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

def load_authorized_users():
    """
    Load authorized user IDs from the MongoDB collection
    """
    authorized_users = set()
    for user_doc in collection.find():
        if "user_id" in user_doc:
            authorized_users.add(user_doc["user_id"])
    return authorized_users

def save_authorized_users(authorized_users):
    """
    Save authorized user IDs to the MongoDB collection
    """
    collection.delete_many({})
    for user_id in authorized_users:
        collection.insert_one({"user_id": user_id})

SUPER_USERS = load_authorized_users()

# Define a dictionary to store user chat IDs
user_chat_ids = {}


async def copy_message_with_chat_id(client, sender, chat_id, message_id):
    # Get the user's set chat ID, if available; otherwise, use the original sender ID
    target_chat_id = user_chat_ids.get(sender, sender)
    
    try:
        # Fetch the message using get_message
        msg = await client.get_messages(chat_id, message_id)
        
        # Modify the caption based on user's custom caption preference
        custom_caption = get_user_caption_preference(sender)
        original_caption = msg.caption if msg.caption else ''
        final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
        
        delete_words = load_delete_words(sender)
        for word in delete_words:
            final_caption = final_caption.replace(word, '  ')
        
        replacements = load_replacement_words(sender)
        for word, replace_word in replacements.items():
            final_caption = final_caption.replace(word, replace_word)
        
        caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}\n\n__**[Team SPY](https://t.me/devggn)**__"
        
        if msg.media:
            if msg.media == MessageMediaType.VIDEO:
                gagn = await client.send_video(target_chat_id, msg.video.file_id, caption=caption)
                try:
                  await gagn.copy(LOG_GROUP)
                except Exception:
                  pass
            elif msg.media == MessageMediaType.DOCUMENT:
                gagn = await client.send_document(target_chat_id, msg.document.file_id, caption=caption)
                try:
                  await gagn.copy(LOG_GROUP)
                except Exception:
                  pass
            elif msg.media == MessageMediaType.PHOTO:
                gagn = await client.send_photo(target_chat_id, msg.photo.file_id, caption=caption)
                try:
                  await gagn.copy(LOG_GROUP)
                except Exception:
                  pass
            else:
                # Use copy_message for any other media types
                gagn = await client.copy_message(target_chat_id, chat_id, message_id)
                try:
                  await gagn.copy(LOG_GROUP)
                except Exception:
                  pass
        else:
            # Use copy_message if there is no media
            gagn = await client.copy_message(target_chat_id, chat_id, message_id)
            try:
              await gagn.copy(LOG_GROUP)
            except Exception:
              pass

    except Exception as e:
        error_message = f"Error occurred while sending message to chat ID {target_chat_id}: {str(e)}"
        await client.send_message(sender, error_message)
        await client.send_message(sender, f"Make Bot admin in your Channel - {target_chat_id} and restart the process after /cancel")

async def send_message_with_chat_id(client, sender, message, parse_mode=None):
    # Get the user's set chat ID, if available; otherwise, use the original sender ID
    chat_id = user_chat_ids.get(sender, sender)
    try:
        gagn = await client.send_message(chat_id, message, parse_mode=parse_mode)        
        try:
          await gagn.copy(LOG_GROUP)
        except Exception:
          pass  # Just pass silently if copying fails
  
    except Exception as e:
        error_message = f"Error occurred while sending message to chat ID {chat_id}: {str(e)}"
        await client.send_message(sender, error_message)
        await client.send_message(sender, f"Make Bot admin in your Channel - {chat_id} and restart the process after /cancel")

#thumb_path = screenshot(file, duration, sender)
async def send_video_with_chat_id(client, sender, path, caption, duration, hi, wi, thumb_path, upm):
    # Get the user's set chat ID, if available; otherwise, use the original sender ID
    chat_id = user_chat_ids.get(sender, sender)
    try:
        gagn = await client.send_video(
            chat_id=chat_id,
            video=path,
            caption=caption,
            supports_streaming=True,
            duration=duration,
            height=hi,
            width=wi,
            thumb=thumb_path,
            progress=progress_for_pyrogram,
            progress_args=(
                client,
                '**__Uploading: [Team SPY](https://t.me/devggn)__**\n ',
                upm,
                time.time()
            )
        )
        try:
          await gagn.copy(LOG_GROUP)
        except Exception:
          pass
    except Exception as e:
        error_message = f"Error occurred while sending video to chat ID {chat_id}: {str(e)}"
        await client.send_message(sender, error_message)
        await client.send_message(sender, f"Make Bot admin in your Channel - {chat_id} and restart the process after /cancel")


async def send_document_with_chat_id(client, sender, path, caption, thumb_path, upm):
    # Get the user's set chat ID, if available; otherwise, use the original sender ID
    chat_id = user_chat_ids.get(sender, sender)
    try:
        gagn = await client.send_document(
            chat_id=chat_id,
            document=path,
            caption=caption,
            thumb=thumb_path,
            progress=progress_for_pyrogram,
            progress_args=(
                client,
                '**__Uploading:__**\n**__Bot made by [Team SPY](https://t.me/devggn)__**',
                upm,
                time.time()
            )
        )
        try:
          await gagn.copy(LOG_GROUP)
        except Exception:
          pass
    except Exception as e:
        error_message = f"Error occurred while sending document to chat ID {chat_id}: {str(e)}"
        await client.send_message(sender, error_message)
        await client.send_message(sender, f"Make Bot admin in your Channel - {chat_id} and restart the process after /cancel")




def load_delete_words(user_id):
    """
    Load delete words for a specific user from MongoDB
    """
    try:
        words_data = collection.find_one({"_id": user_id})
        if words_data:
            return set(words_data.get("delete_words", []))
        else:
            return set()
    except Exception as e:
        print(f"Error loading delete words: {e}")
        return set()

def save_delete_words(user_id, delete_words):
    """
    Save delete words for a specific user to MongoDB
    """
    try:
        collection.update_one(
            {"_id": user_id},
            {"$set": {"delete_words": list(delete_words)}},
            upsert=True
        )
    except Exception as e:
        print(f"Error saving delete words: {e}")

def load_replacement_words(user_id):
    try:
        words_data = collection.find_one({"_id": user_id})
        if words_data:
            return words_data.get("replacement_words", {})
        else:
            return {}
    except Exception as e:
        print(f"Error loading replacement words: {e}")
        return {}

def save_replacement_words(user_id, replacements):
    try:
        collection.update_one(
            {"_id": user_id},
            {"$set": {"replacement_words": replacements}},
            upsert=True
        )
    except Exception as e:
        print(f"Error saving replacement words: {e}")


@bot.on(events.NewMessage(incoming=True, pattern='/replace'))
async def replace_command(event):
    if event.sender_id not in SUPER_USERS:
        return await event.respond("This command is restricted.")
    
    user_id = event.sender_id
    if not user_id:
        return await event.respond("User ID not found!")
    
    # Parse the command arguments
    match = re.match(r"/replace '(.+)' '(.+)'", event.raw_text)
    if not match:
        return await event.respond("Usage: /replace 'WORD(s)' 'REPLACEWORD'")
    
    word, replace_word = match.groups()
    
    # Load delete words
    delete_words = load_delete_words(user_id)
    if word in delete_words:
        return await event.respond(f"The word '{word}' is in the delete set and cannot be replaced.")
    
    # Load replacement words
    replacements = load_replacement_words(user_id)
    replacements[word] = replace_word
    save_replacement_words(user_id, replacements)

    await event.respond(f"Replacement saved: '{word}' will be replaced with '{replace_word}'")

@bot.on(events.NewMessage(incoming=True, pattern='/auth'))
async def _auth(event):
    """
    Command to authorize users
    """
    # Check if the command is initiated by the owner
    if event.sender_id == OWNER_ID:
        # Parse the user ID from the command
        try:
            user_id = int(event.message.text.split(' ')[1])
        except (ValueError, IndexError):
            return await event.respond("Invalid /auth command. Use /auth USER_ID.")

        #Add the user ID to the authorized set
        SUPER_USERS.add(user_id)
        save_authorized_users(SUPER_USERS)
        await event.respond(f"User {user_id} has been authorized for commands.")
    else:
        await event.respond("You are not authorized to use this command.")

@bot.on(events.NewMessage(incoming=True, pattern='/clean'))
async def clear_all_delete_words_command_handler(event):
    """
    Command to clear all saved delete words for all users
    """
    # Check if the command is used by the owner
    if event.sender_id != OWNER_ID:
        return await event.respond("You are not authorized to use this command!")
    
    try:
        # Clear all delete words from the database
        collection.delete_many({})
        await event.respond("All saved delete words have been cleared for all users.")
    except Exception as e:
        print(f"Error clearing all delete words: {e}")
        await event.respond("An error occurred while clearing all delete words.")


@bot.on(events.NewMessage(incoming=True, pattern='/delete'))
async def delete_word_command_handler(event):
    if event.sender_id not in SUPER_USERS:
        return await event.respond("Purchase premium to unlock this command")
    # Parse the user ID
    user_id = event.sender_id
    if not user_id:
        return await event.respond("User ID not found!")
    
    # Parse the words from the command
    words_to_delete = event.text.split()[1:]
    if not words_to_delete:
        await event.respond("Please provide word(s) to delete!")
        return
    
    # Load user's delete words
    user_delete_words = load_delete_words(user_id)
    
    # Add the word(s) to the list of user's delete words
    for word in words_to_delete:
        user_delete_words.add(word)
    
    # Save user's delete words
    save_delete_words(user_id, user_delete_words)
    
    await event.respond(f"Word(s) added to your list of words to delete: {', '.join(words_to_delete)}")


def thumbnail(sender):
    return f'{sender}.jpg' if os.path.exists(f'{sender}.jpg') else None

# Initialize the dictionary to store user preferences for renaming
user_rename_preferences = {}

# Initialize the dictionary to store user caption
user_caption_preferences = {}

# Function to handle the /setrename command
async def set_rename_command(user_id, custom_rename_tag):
    # Update the user_rename_preferences dictionary
    user_rename_preferences[str(user_id)] = custom_rename_tag

# Function to get the user's custom renaming preference
def get_user_rename_preference(user_id):
    # Retrieve the user's custom renaming tag if set, or default to '@devggn'
    return user_rename_preferences.get(str(user_id), '@devggn')

# Function to set custom caption preference
async def set_caption_command(user_id, custom_caption):
    # Update the user_caption_preferences dictionary
    user_caption_preferences[str(user_id)] = custom_caption

# Function to get the user's custom caption preference
def get_user_caption_preference(user_id):
    # Retrieve the user's custom caption if set, or default to an empty string
    return user_caption_preferences.get(str(user_id), '')

@bot.on(events.NewMessage(incoming=True, pattern='/setchat'))
async def set_chat_id(event):
    # Check if the command is used by an authorized user
    user_id = event.sender_id
    if user_id not in SUPER_USERS:
        return await event.respond("This command is available to authorized users only.")
    
    # Extract chat ID from the message
    try:
        chat_id = int(event.raw_text.split(" ", 1)[1])
        # Store user's chat ID
        user_chat_ids[event.sender_id] = chat_id
        await event.reply("Chat ID set successfully!")
    except ValueError:
        await event.reply("Invalid chat ID!")

@bot.on(events.NewMessage(incoming=True, pattern='/setrename'))
async def set_rename_command_handler(event):
    # Check if the command is used by an authorized user
    user_id = event.sender_id
    if user_id not in SUPER_USERS:
        return await event.respond("This command is available to Paid Plan users! Send /plan to know more.")
    
    # Parse the custom rename tag from the command
    custom_rename_tag = ' '.join(event.text.split(' ')[1:])
    if not custom_rename_tag:
        await event.respond("Please provide a custom rename tag!")
        return
    
    # Call the function to set the custom rename tag
    await set_rename_command(event.sender_id, custom_rename_tag)
    await event.respond(f"Custom rename tag set to: {custom_rename_tag}")

@bot.on(events.NewMessage(incoming=True, pattern='/unauth'))
async def _unauth(event):
    """
    Command to revoke authorization for users
    """
    # Check if the command is initiated by the owner
    if event.sender_id == OWNER_ID:
        # Parse the user ID from the command
        try:
            user_id = int(event.message.text.split(' ')[1])
        except (ValueError, IndexError):
            return await event.respond("Invalid /unauth command. Use /unauth USER_ID.")

        # Remove the user ID from the authorized set
        if user_id in SUPER_USERS:
            SUPER_USERS.remove(user_id)
            save_authorized_users(SUPER_USERS)
            await event.respond(f"Authorization revoked for user {user_id}.")
            # Clear user's custom rename preference if set
            if str(user_id) in user_rename_preferences:
                del user_rename_preferences[str(user_id)]
                await event.respond(f"Custom rename preference cleared for user {user_id}.")
            # Clear user's custom caption preference if set
            if str(user_id) in user_caption_preferences:
                del user_caption_preferences[str(user_id)]
                await event.respond(f"Custom caption preference cleared for user {user_id}.")
            if str(user_id) in user_chat_ids:
              del user_chat_ids[str(user_id)]
              await event.respond(f"Chat ID preference cleared for user {user_id}.")
        else:
            await event.respond(f"User {user_id} is not authorized.")
    else:
        await event.respond("You are not authorized to use this command.")

@bot.on(events.NewMessage(incoming=True, pattern='/setcaption'))
async def set_caption_command_handler(event):
    # Check if the command is used by an authorized user
    if event.sender_id not in SUPER_USERS:
        return await event.respond("This command is available to paid plan users! Send /plan to know more.")

    # Parse the custom caption from the command
    custom_caption = ' '.join(event.message.text.split(' ')[1:])
    if not custom_caption:
        return await event.respond("Please provide a custom caption!")

    # Call the function to set the custom caption
    await set_caption_command(event.sender_id, custom_caption)
    await event.respond(f"Custom caption set to: {custom_caption}")

user_sessions = {}

@bot.on(events.NewMessage(incoming=True, pattern='/addsession'))
async def add_session_command_handler(event):
    """
    Command to add user session
    """
    # Parse the user session string from the command
    try:
        _, user_session = event.text.split(' ', 1)  # Split only once to capture the session string
    except ValueError:
        return await event.respond("Invalid /addsession command. Use /addsession SESSION_STRING.")

    # Store the session string for the user (identified by sender_id)
    sender_id = event.sender_id
    user_sessions[sender_id] = user_session
    await event.respond("Session string added successfully.")

@bot.on(events.NewMessage(incoming=True, pattern='/logout'))
async def del_session_command_handler(event):
    """
    Command to delete user session
    """
    # Get the sender ID
    sender_id = event.sender_id

    # Check if the user has a session
    if sender_id in user_sessions:
        # Delete the session
        del user_sessions[sender_id]
        await event.respond("Session string deleted successfully.")
    else:
        await event.respond("No session found for the user.")


API_ID = "19748984" 
API_HASH = "2141e30f96dfbd8c46fbb5ff4b197004"

async def check(userbot, client, link, event):
    logging.info(link)
    msg_id = 0
    sender_id = event.sender_id  # Retrieve sender_id from the event
    try:
        msg_id = int(link.split("/")[-1])
    except ValueError:
        if '?single' not in link:
            return False, "**Invalid Link!**"
        link_ = link.split("?single")[0]
        msg_id = int(link_.split("/")[-1])
    
    if 't.me/c/' in link:
        try:
            chat = int('-100' + str(link.split("/")[-2]))
            # Check if user session is available
            user_session = user_sessions.get(sender_id)
            if user_session:
                # Create and start userbot instance
                session_name = f"{sender_id}app"
                user_bot = Client(
                    session_name,
                    api_id=API_ID,
                    api_hash=API_HASH,
                    session_string=user_session
                )
                await user_bot.start()
                # Get messages using userbot instance
                await user_bot.get_messages(chat, msg_id)
                # Stop userbot instance
                await user_bot.stop()
                return True, None  # Return True if user session is available
            else:
                await userbot.get_messages(chat, msg_id)
                return True, None
        except ValueError:
            return False, "**Invalid Link!**"
        except Exception as e:
            logging.error(e)
            # If user_bot instance fails, fall back to using userbot
            return False, "Bot is not there add your session to save without link or send invite link...\n\nTo generate session you can use our official bot - @stringsessionAK47bot.."
    else:
        try:
            chat = str(link.split("/")[-2])
            await client.get_messages(chat, msg_id)
            return True, None
        except Exception as e:
            logging.error(e)
            return False, "Maybe bot is banned from the chat, or your link is invalid!"

def load_saved_channel_ids():
    """
    Load saved channel IDs from MongoDB collection
    """
    saved_channel_ids = set()
    try:
        # Retrieve channel IDs from MongoDB collection
        for channel_doc in collection.find({"channel_id": {"$exists": True}}):
            saved_channel_ids.add(channel_doc["channel_id"])
    except Exception as e:
        print(f"Error loading saved channel IDs: {e}")
    return saved_channel_ids

# Command to store channel IDs
@bot.on(events.NewMessage(incoming=True, pattern='/lock'))
async def lock_command_handler(event):
    # Check if the command is initiated by the owner
    if event.sender_id != OWNER_ID:
        return await event.respond("You are not authorized to use this command.")
    
    # Extract the channel ID from the command
    try:
        channel_id = int(event.text.split(' ')[1])
    except (ValueError, IndexError):
        return await event.respond("Invalid /lock command. Use /lock CHANNEL_ID.")
    
    # Save the channel ID to the MongoDB database
    try:
        # Insert the channel ID into the collection
        collection.insert_one({"channel_id": channel_id})
        await event.respond(f"Channel ID {channel_id} locked successfully.")
    except Exception as e:
        await event.respond(f"Error occurred while locking channel ID: {str(e)}")

async def get_msg(userbot, client, sender, edit_id, msg_link, i, file_n):
    edit = ""
    chat = ""
    msg_id = int(i)
    if msg_id == -1:
        await client.edit_message_text(sender, edit_id, "**Invalid Link!**")
        return None
    if 't.me/c/'  in msg_link or 't.me/b/' in msg_link:
        if "t.me/b" not in msg_link:
          chat = int('-100' + str(msg_link.split("/")[-2]))
        else:
          chat = msg_link.split("/")[-2]
        if chat in load_saved_channel_ids():
          await client.edit_message_text(sender, edit_id, "This channel is protected by the owner...")
          return None
        file = ""
        try:
            user_session = user_sessions.get(sender)
            session_name = f"{sender}app"
            if user_session:
              user_bot = Client(
                session_name,
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=user_session
              )
              await user_bot.start()
              msg = await user_bot.get_messages(chat_id=chat, message_ids=msg_id)
            else:
              msg = await userbot.get_messages(chat_id=chat, message_ids=msg_id)
            logging.info(msg)
            if msg.service is not None:
                await client.delete_messages(chat_id=sender, message_ids=edit_id)
                return None
            if msg.empty is not None:
                await client.delete_messages(chat_id=sender, message_ids=edit_id)
                return None            
            if msg.media and msg.media == MessageMediaType.WEB_PAGE:
                a = b = True
                edit = await client.edit_message_text(sender, edit_id, "Cloning.")
                if '--'  in msg.text.html or '**' in msg.text.html or '__' in msg.text.html or '~~' in msg.text.html or '||' in msg.text.html or '```' in msg.text.html or '`' in msg.text.html:
                    await send_message_with_chat_id(client, sender, msg.text.html, parse_mode=ParseMode.HTML)
                    a = False
                if '<b>' in msg.text.markdown or '<i>' in msg.text.markdown or '<em>' in msg.text.markdown  or '<u>' in msg.text.markdown or '<s>' in msg.text.markdown or '<spoiler>' in msg.text.markdown or '<a href=>' in msg.text.markdown or '<pre' in msg.text.markdown or '<code>' in msg.text.markdown or '<emoji' in msg.text.markdown:
                    await send_message_with_chat_id(client, sender, msg.text.markdown, parse_mode=ParseMode.MARKDOWN)
                    b = False
                if a and b:
                    await send_message_with_chat_id(client, sender, msg.text.markdown, parse_mode=ParseMode.MARKDOWN)
                await edit.delete()
                return None
            if not msg.media and msg.text:
                a = b = True
                edit = await client.edit_message_text(sender, edit_id, "Cloning.")
                if '--'  in msg.text.html or '**' in msg.text.html or '__' in msg.text.html or '~~' in msg.text.html or '||' in msg.text.html or '```' in msg.text.html or '`' in msg.text.html:
                    await send_message_with_chat_id(client, sender, msg.text.html, parse_mode=ParseMode.HTML)
                    a = False
                if '<b>' in msg.text.markdown or '<i>' in msg.text.markdown or '<em>' in msg.text.markdown  or '<u>' in msg.text.markdown or '<s>' in msg.text.markdown or '<spoiler>' in msg.text.markdown or '<a href=>' in msg.text.markdown or '<pre' in msg.text.markdown or '<code>' in msg.text.markdown or '<emoji' in msg.text.markdown:
                    await send_message_with_chat_id(client, sender, msg.text.markdown, parse_mode=ParseMode.MARKDOWN)
                    b = False
                if a and b:
                    await send_message_with_chat_id(client, sender, msg.text.markdown, parse_mode=ParseMode.MARKDOWN)
                await edit.delete()
                return None
            if msg.media == MessageMediaType.POLL:
                await client.edit_message_text(sender, edit_id, 'poll media cant be saved')
                return 
            edit = await client.edit_message_text(sender, edit_id, "Trying to Download.")
            user_session = user_sessions.get(sender)
            if user_session:
              file = await user_bot.download_media(msg, progress=progress_for_pyrogram, progress_args=(client, "**__Unrestricting__: __[Team SPY](https://t.me/devggn)__**\n ", edit, time.time()))
              await user_bot.stop()
            else:
              file = await userbot.download_media(msg, progress=progress_for_pyrogram, progress_args=(client, "**__Unrestricting__: __[Team SPY](https://t.me/devggn)__**\n ", edit, time.time()))            # Retrieve user's custom renaming preference if set, default to '@devggn' otherwise
            custom_rename_tag = get_user_rename_preference(sender)
            # retriving name 
            last_dot_index = str(file).rfind('.')
            if last_dot_index != -1 and last_dot_index != 0:
              original_file_name = str(file)[:last_dot_index]
              file_extension = str(file)[last_dot_index + 1:]
            else:
              original_file_name = str(file)
              file_extension = 'mp4'
            
            #Removing Words
            delete_words = load_delete_words(sender)
            for word in delete_words:
              original_file_name = original_file_name.replace(word, "")
            
            # Rename the file with the updated file name and custom renaming tag
            video_file_name = original_file_name + " " + custom_rename_tag
            new_file_name = original_file_name + " " + custom_rename_tag + "." + file_extension
            os.rename(file, new_file_name)
            file = new_file_name   
          
            path = file
            await edit.delete()
            upm = await client.send_message(sender, 'Preparing to Upload!')
            
            caption = str(file)
            if msg.caption is not None:
                caption = msg.caption
            if file_extension in ['mkv', 'mp4', 'webm', 'mpe4', 'mpeg', 'ts', 'avi', 'flv', 'org', 'm4v']:
                if file_extension in ['webm', 'mkv', 'mpe4', 'mpeg', 'ts', 'avi', 'flv', 'org', 'm4v']:
                    path = video_file_name + ".mp4"
                    os.rename(file, path) 
                    file = path
                data = video_metadata(file)
                duration = data["duration"]
                wi = data["width"]
                hi = data["height"]
                logging.info(data)

                if file_n != '':
                    if '.' in file_n:
                        path = f'/app/downloads/{file_n}'
                    else:
                        path = f'/app/downloads/{file_n}.' + str(file).split(".")[-1]

                    os.rename(file, path)
                    file = path
                thumb_path = await screenshot(file, duration, sender)
                # Modify the caption based on user's custom caption preference
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                delete_words = load_delete_words(sender)
                for word in delete_words:
                  final_caption = final_caption.replace(word, '  ')
                replacements = load_replacement_words(sender)
                for word, replace_word in replacements.items():
                  final_caption = final_caption.replace(word, replace_word)  
                # final_caption = re.sub(r'\s{2,}', '  ', final_caption.strip())
                # final_caption = re.sub(r'\n{2,}', '\n\n', final_caption)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}\n\n__**[Team SPY](https://t.me/devggn)**__"
                await send_video_with_chat_id(client, sender, path, caption, duration, hi, wi, thumb_path, upm)
            elif str(file).split(".")[-1] in ['jpg', 'jpeg', 'png', 'webp']:
                if file_n != '':
                    if '.' in file_n:
                        path = f'/app/downloads/{file_n}'
                    else:
                        path = f'/app/downloads/{file_n}.' + str(file).split(".")[-1]
                    os.rename(file, path)
                    file = path
                caption = msg.caption if msg.caption is not None else str(file).split("/")[-1]
                await upm.edit("Uploading photo...")
                await bot.send_file(sender, path, caption=caption)
            else:
                if file_n != '':
                    if '.' in file_n:
                        path = f'/app/downloads/{file_n}'
                    else:
                        path = f'/app/downloads/{file_n}.' + str(file).split(".")[-1]
                    os.rename(file, path)
                    file = path
                thumb_path = thumbnail(sender)
                # Modify the caption based on user's custom caption preference
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                delete_words = load_delete_words(sender)
                for word in delete_words:
                  final_caption = final_caption.replace(word, '  ')
                replacements = load_replacement_words(sender)
                for word, replace_word in replacements.items():
                  final_caption = final_caption.replace(word, replace_word)  
                # final_caption = re.sub(r'\s{2,}', '  ', final_caption.strip())
                # final_caption = re.sub(r'\n{2,}', '\n\n', final_caption)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}\n\n__**[Team SPY](https://t.me/devggn)**__"
                await send_document_with_chat_id(client, sender, path, caption, thumb_path, upm)
                    
            os.remove(file)
            await upm.delete()
            return None
        except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
            await client.edit_message_text(sender, edit_id, "Bot is not in that channel/group \nsend the invite or add session vioa command /addsession link so that bot can join the channel\n\nTo generate session you can use our official bot - @stringsessionAK47bot")
            return None
    else:
        edit = await client.edit_message_text(sender, edit_id, "Cloning.")
        chat =  msg_link.split("/")[-2]
        await copy_message_with_chat_id(client, sender, chat, msg_id)
        await edit.delete()
        return None   

async def x(userbot, client, sender, edit_id, msg_link, i, file_n):
    edit = ""
    chat = ""
    msg_id = int(i)
    if msg_id == -1:
        await client.edit_message_text(sender, edit_id, "**Invalid Link!**")
        return None
    if 't.me/c/'  in msg_link or 't.me/b/' in msg_link:
        if "t.me/b" not in msg_link:
            parts = msg_link.split("/")
            chat = int('-100' + str(parts[4]))
        else:
            chat = int(msg_link.split("/")[-2])
        if chat in load_saved_channel_ids():
          await client.edit_message_text(sender, edit_id, "This channel is protected by the owner...")
          return None          
        file = ""
        try:
            msg = await userbot.get_messages(chat_id = chat, message_ids = msg_id)
            logging.info(msg)
           # medi =  msg.document or msg.video or msg.audio or None
            if msg.service is not None:
                await client.delete_messages(
                    chat_id=sender,
                    message_ids=edit_id
                )
                #await client.edit_message_text(sender, edit_id, f"{msg.service}")
                return None
            if msg.empty is not None:
                await client.delete_messages(
                    chat_id=sender,
                    message_ids=edit_id
                )
                #await client.edit_message_text(sender, edit_id, f"message dosnt exist \n{msg.empty}")
                return None            
            
            if msg.media and msg.media==MessageMediaType.WEB_PAGE:
                a = b = True
                edit = await client.edit_message_text(sender, edit_id, "Cloning.")
                if '--'  in msg.text.html or '**' in msg.text.html or '__' in msg.text.html or '~~' in msg.text.html or '||' in msg.text.html or '```' in msg.text.html or '`' in msg.text.html:
                    await send_message_with_chat_id(client, sender, msg.text.html, parse_mode=ParseMode.HTML)
                    a = False
                if '<b>' in msg.text.markdown or '<i>' in msg.text.markdown or '<em>' in msg.text.markdown  or '<u>' in msg.text.markdown or '<s>' in msg.text.markdown or '<spoiler>' in msg.text.markdown or '<a href=>' in msg.text.markdown or '<pre' in msg.text.markdown or '<code>' in msg.text.markdown or '<emoji' in msg.text.markdown:
                    await send_message_with_chat_id(client, sender, msg.text.markdown, parse_mode=ParseMode.MARKDOWN)
                    b = False
                if a and b:
                    await send_message_with_chat_id(client, sender, msg.text.markdown, parse_mode=ParseMode.MARKDOWN)
                await edit.delete()
                return None
            if not msg.media and msg.text:
                a = b = True
                edit = await client.edit_message_text(sender, edit_id, "Cloning.")
                if '--'  in msg.text.html or '**' in msg.text.html or '__' in msg.text.html or '~~' in msg.text.html or '||' in msg.text.html or '```' in msg.text.html or '`' in msg.text.html:
                    await send_message_with_chat_id(client, sender, msg.text.html, parse_mode=ParseMode.HTML)
                    a = False
                if '<b>' in msg.text.markdown or '<i>' in msg.text.markdown or '<em>' in msg.text.markdown  or '<u>' in msg.text.markdown or '<s>' in msg.text.markdown or '<spoiler>' in msg.text.markdown or '<a href=>' in msg.text.markdown or '<pre' in msg.text.markdown or '<code>' in msg.text.markdown or '<emoji' in msg.text.markdown:
                    await send_message_with_chat_id(client, sender, msg.text.markdown, parse_mode=ParseMode.MARKDOWN)
                    b = False
                if a and b:
                    await send_message_with_chat_id(client, sender, msg.text.markdown, parse_mode=ParseMode.MARKDOWN)
                
                '''await client.send_message(sender, msg.text.html, parse_mode = 'html')
                   await client.send_message(sender, msg.text.html, parse_mode = 'md')
                   await client.send_message(sender, msg.text.markdown, parse_mode = 'html')
                   await client.send_message(sender, msg.text.markdown, parse_mode = 'md')
                   await client.send_message(sender, msg.text.markdown)
                '''
                await edit.delete()
                return None
            if msg.media==MessageMediaType.POLL:
                #await client.send_message(sender,'poll media cant be saved')
                await client.edit_message_text(sender, edit_id, 'poll media cant be saved')
                #await edit.delete()
                return 
            edit = await client.edit_message_text(sender, edit_id, "Trying to Download.")
            
            file = await userbot.download_media(
                msg,
                progress=progress_for_pyrogram,
                progress_args=(
                    client,
                    "**__Unrestricting__: __[Team SPY](https://t.me/dev_gagan)__**\n ",
                    edit,
                    time.time()
                )
            )  
          
            path = file
            await edit.delete()
            upm = await client.send_message(sender, '__Preparing to Upload!__')
            
            caption = str(file)
            if msg.caption is not None:
                caption = msg.caption
            if str(file).split(".")[-1] in ['mkv', 'mp4', 'webm', 'mpe4', 'mpeg', 'ts', 'avi', 'flv', 'org']:
                if str(file).split(".")[-1] in ['webm', 'mkv', 'mpe4', 'mpeg', 'ts', 'avi', 'flv', 'org']:
                    path = str(file).split(".")[0] + ".mp4"
                    os.rename(file, path) 
                    file = str(file).split(".")[0] + ".mp4"
                data = video_metadata(file)
                duration = data["duration"]
                wi= data["width"]
                hi= data["height"]
                logging.info(data)

                if file_n != '':
                    #path = ''
                    if '.' in file_n:
                        
                        path = f'/app/downloads/{file_n}'
                    else:
                        
                        path = f'/app/downloads/{file_n}.' + str(file).split(".")[-1]

                    os.rename(file, path)
                    file = path
                try:
                    thumb_path = await screenshot(file, duration, sender)
                except Exception as e:
                    logging.info(e)
                    thumb_path = None
                
                caption = f"{msg.caption}\n\n__Unrestricted by **[Team SPY](https://t.me/dev_gagan)**__" if msg.caption else "__Unrestricted by **[Team SPY](https://t.me/dev_gagan)**__"
                await send_video_with_chat_id(client, sender, path, caption, duration, hi, wi, thumb_path, upm)
            elif str(file).split(".")[-1] in ['jpg', 'jpeg', 'png', 'webp']:
                if file_n != '':
                    #path = ''
                    if '.' in file_n:
                        path = f'/app/downloads/{file_n}'
                    else:
                        path = f'/app/downloads/{file_n}.' + str(file).split(".")[-1]

                    os.rename(file, path)
                    file = path

                
                caption = f"{msg.caption}\n\n__Unrestricted by **[Team SPY](https://t.me/dev_gagan)**__" if msg.caption else "__Unrestricted by **[Team SPY](https://t.me/dev_gagan)**__"
                await upm.edit("__Uploading photo...__")

                await bot.send_file(sender, path, caption=caption)
            else:
                if file_n != '':
                    #path = ''
                    if '.' in file_n:
                        path = f'/app/downloads/{file_n}'
                    else:
                        path = f'/app/downloads/{file_n}.' + str(file).split(".")[-1]

                    os.rename(file, path)
                    file = path
                thumb_path = await screenshot(file, duration, sender)
                
                caption = f"{msg.caption}\n\n__Unrestricted by **[Team SPY](https://t.me/dev_gagan)**__" if msg.caption else "__Unrestricted by **[Team SPY](https://t.me/dev_gagan)**__"
                await send_document_with_chat_id(client, sender, path, caption, thumb_path, upm)
            os.remove(file)
            await upm.delete()
            return None
        except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
            await client.edit_message_text(sender, edit_id, "Bot is not in that channel/ group \n send the invite link so that bot can join the channel ")
            return None
    else:
        edit = await client.edit_message_text(sender, edit_id, "Cloning.")
        chat =  msg_link.split("/")[-2]
        await copy_message_with_chat_id(client, sender, chat, msg_id)
        await edit.delete()
        return None   
    
async def get_bulk_msg(userbot, client, sender, msg_link, i):
    x = await client.send_message(sender, "Processing!")
    file_name = ''
    await get_msg(userbot, client, sender, x.id, msg_link, i, file_name) 

async def ggn_new(userbot, client, sender, edit_id, msg_link, i, file_n):
    edit = ""
    chat = ""
    msg_id = int(i)
    if msg_id == -1:
        await client.edit_message_text(sender, edit_id, "**Invalid Link!**")
        return None
    if 't.me/c/'  in msg_link or 't.me/b/' in msg_link:
        if "t.me/b" not in msg_link:
          parts = msg_link.split("/")
          chat = parts[4]
          chat = int(f"-100{chat}")
          
        else:
          chat = msg_link.split("/")[-2]
        if chat in load_saved_channel_ids():
          await client.edit_message_text(sender, edit_id, "This channel is protected by the owner...")
          return None
        file = ""
        try:
            user_session = user_sessions.get(sender)
            session_name = f"{sender}app"
            if user_session:
              user_bot = Client(
                session_name,
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=user_session
              )
              await user_bot.start()
              msg = await user_bot.get_messages(chat_id=chat, message_ids=msg_id)
            else:
              msg = await userbot.get_messages(chat_id=chat, message_ids=msg_id)
            logging.info(msg)
            if msg.service is not None:
                await client.delete_messages(chat_id=sender, message_ids=edit_id)
                return None
            if msg.empty is not None:
                await client.delete_messages(chat_id=sender, message_ids=edit_id)
                return None            
            if msg.media and msg.media == MessageMediaType.WEB_PAGE:
                a = b = True
                edit = await client.edit_message_text(sender, edit_id, "Cloning.")
                if '--'  in msg.text.html or '**' in msg.text.html or '__' in msg.text.html or '~~' in msg.text.html or '||' in msg.text.html or '```' in msg.text.html or '`' in msg.text.html:
                    await send_message_with_chat_id(client, sender, msg.text.html, parse_mode=ParseMode.HTML)
                    a = False
                if '<b>' in msg.text.markdown or '<i>' in msg.text.markdown or '<em>' in msg.text.markdown  or '<u>' in msg.text.markdown or '<s>' in msg.text.markdown or '<spoiler>' in msg.text.markdown or '<a href=>' in msg.text.markdown or '<pre' in msg.text.markdown or '<code>' in msg.text.markdown or '<emoji' in msg.text.markdown:
                    await send_message_with_chat_id(client, sender, msg.text.markdown, parse_mode=ParseMode.MARKDOWN)
                    b = False
                if a and b:
                    await send_message_with_chat_id(client, sender, msg.text.markdown, parse_mode=ParseMode.MARKDOWN)
                await edit.delete()
                return None
            if not msg.media and msg.text:
                a = b = True
                edit = await client.edit_message_text(sender, edit_id, "Cloning.")
                if '--'  in msg.text.html or '**' in msg.text.html or '__' in msg.text.html or '~~' in msg.text.html or '||' in msg.text.html or '```' in msg.text.html or '`' in msg.text.html:
                    await send_message_with_chat_id(client, sender, msg.text.html, parse_mode=ParseMode.HTML)
                    a = False
                if '<b>' in msg.text.markdown or '<i>' in msg.text.markdown or '<em>' in msg.text.markdown  or '<u>' in msg.text.markdown or '<s>' in msg.text.markdown or '<spoiler>' in msg.text.markdown or '<a href=>' in msg.text.markdown or '<pre' in msg.text.markdown or '<code>' in msg.text.markdown or '<emoji' in msg.text.markdown:
                    await send_message_with_chat_id(client, sender, msg.text.markdown, parse_mode=ParseMode.MARKDOWN)
                    b = False
                if a and b:
                    await send_message_with_chat_id(client, sender, msg.text.markdown, parse_mode=ParseMode.MARKDOWN)
                await edit.delete()
                return None
            if msg.media == MessageMediaType.POLL:
                await client.edit_message_text(sender, edit_id, 'poll media cant be saved')
                return 
            edit = await client.edit_message_text(sender, edit_id, "Trying to Download.")
            user_session = user_sessions.get(sender)
            if user_session:
              file = await user_bot.download_media(msg, progress=progress_for_pyrogram, progress_args=(client, "**__Unrestricting__: __[Team SPY](https://t.me/devggn)__**\n ", edit, time.time()))
              await user_bot.stop()
            else:
              file = await userbot.download_media(msg, progress=progress_for_pyrogram, progress_args=(client, "**__Unrestricting__: __[Team SPY](https://t.me/devggn)__**\n ", edit, time.time()))            # Retrieve user's custom renaming preference if set, default to '@devggn' otherwise
            custom_rename_tag = get_user_rename_preference(sender)
            # retriving name 
            last_dot_index = str(file).rfind('.')
            if last_dot_index != -1 and last_dot_index != 0:
              original_file_name = str(file)[:last_dot_index]
              file_extension = str(file)[last_dot_index + 1:]
            else:
              original_file_name = str(file)
              file_extension = 'mp4'
            
            #Removing Words
            delete_words = load_delete_words(sender)
            for word in delete_words:
              original_file_name = original_file_name.replace(word, "")
            
            # Rename the file with the updated file name and custom renaming tag
            video_file_name = original_file_name + " " + custom_rename_tag
            new_file_name = original_file_name + " " + custom_rename_tag + "." + file_extension
            os.rename(file, new_file_name)
            file = new_file_name   
          
            path = file
            await edit.delete()
            upm = await client.send_message(sender, 'Preparing to Upload!')
            
            caption = str(file)
            if msg.caption is not None:
                caption = msg.caption
            if file_extension in ['mkv', 'mp4', 'webm', 'mpe4', 'mpeg', 'ts', 'avi', 'flv', 'org', 'm4v']:
                if file_extension in ['webm', 'mkv', 'mpe4', 'mpeg', 'ts', 'avi', 'flv', 'org', 'm4v']:
                    path = video_file_name + ".mp4"
                    os.rename(file, path) 
                    file = path
                data = video_metadata(file)
                duration = data["duration"]
                wi = data["width"]
                hi = data["height"]
                logging.info(data)

                if file_n != '':
                    if '.' in file_n:
                        path = f'/app/downloads/{file_n}'
                    else:
                        path = f'/app/downloads/{file_n}.' + str(file).split(".")[-1]

                    os.rename(file, path)
                    file = path
                thumb_path = await screenshot(file, duration, sender)
                # Modify the caption based on user's custom caption preference
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                delete_words = load_delete_words(sender)
                for word in delete_words:
                  final_caption = final_caption.replace(word, '  ')
                replacements = load_replacement_words(sender)
                for word, replace_word in replacements.items():
                  final_caption = final_caption.replace(word, replace_word)  
                # final_caption = re.sub(r'\s{2,}', '  ', final_caption.strip())
                # final_caption = re.sub(r'\n{2,}', '\n\n', final_caption)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}\n\n__**[Team SPY](https://t.me/devggn)**__"
                await send_video_with_chat_id(client, sender, path, caption, duration, hi, wi, thumb_path, upm)
            elif str(file).split(".")[-1] in ['jpg', 'jpeg', 'png', 'webp']:
                if file_n != '':
                    if '.' in file_n:
                        path = f'/app/downloads/{file_n}'
                    else:
                        path = f'/app/downloads/{file_n}.' + str(file).split(".")[-1]
                    os.rename(file, path)
                    file = path
                caption = msg.caption if msg.caption is not None else str(file).split("/")[-1]
                await upm.edit("Uploading photo...")
                await bot.send_file(sender, path, caption=caption)
            else:
                if file_n != '':
                    if '.' in file_n:
                        path = f'/app/downloads/{file_n}'
                    else:
                        path = f'/app/downloads/{file_n}.' + str(file).split(".")[-1]
                    os.rename(file, path)
                    file = path
                thumb_path = thumbnail(sender)
                # Modify the caption based on user's custom caption preference
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                delete_words = load_delete_words(sender)
                for word in delete_words:
                  final_caption = final_caption.replace(word, '  ')
                replacements = load_replacement_words(sender)
                for word, replace_word in replacements.items():
                  final_caption = final_caption.replace(word, replace_word)  
                # final_caption = re.sub(r'\s{2,}', '  ', final_caption.strip())
                # final_caption = re.sub(r'\n{2,}', '\n\n', final_caption)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}\n\n__**[Team SPY](https://t.me/devggn)**__"
                await send_document_with_chat_id(client, sender, path, caption, thumb_path, upm)
                    
            os.remove(file)
            await upm.delete()
            return None
        except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
            await client.edit_message_text(sender, edit_id, "Bot is not in that channel/group \nsend the invite or add session vioa command /addsession link so that bot can join the channel\n\nTo generate session you can use our official bot - @stringsessionAK47bot")
            return None
    else:
        edit = await client.edit_message_text(sender, edit_id, "Cloning.")
        chat =  msg_link.split("/")[-2]
        await copy_message_with_chat_id(client, sender, chat, msg_id)
        await edit.delete()
        return None   
      
