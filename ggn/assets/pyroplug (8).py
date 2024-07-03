# Join t.me/devggn

import re
import asyncio, time, os
import pymongo
from pyrogram.enums import ParseMode , MessageMediaType
from .. import bot as teamspy
from ggn.assets.progress import progress_for_pyrogram
from ggn.assets.functions import screenshot
from pyrogram import Client
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid
from ggn.assets.functions import video_metadata
from telethon import events, Button
import subprocess
import logging
from config import MONGODB_CONNECTION_STRING, LOG_GROUP, OWNER_ID

# ------------- PDF WATERMARK IMPORTS --------------
# Removed from this purchase from me to the things conact @ggnhere
# ------------- PDF WATERMARK IMPORTS --------------


# ---------------------- SENDING FUNCTIONS - TEAM SPY (@devggn) ----------------

async def copy_message_with_chat_id(client, sender, chat_id, message_id):
    target_chat_id = user_chat_ids.get(sender, sender)
    
    try:
        msg = await client.get_messages(chat_id, message_id)
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
                result = await client.send_video(target_chat_id, msg.video.file_id, caption=caption)
                try:
                  await result.copy(LOG_GROUP)
                except Exception:
                  pass
            elif msg.media == MessageMediaType.DOCUMENT:
                result = await client.send_document(target_chat_id, msg.document.file_id, caption=caption)
                try:
                  await result.copy(LOG_GROUP)
                except Exception:
                  pass
            elif msg.media == MessageMediaType.PHOTO:
                result = await client.send_photo(target_chat_id, msg.photo.file_id, caption=caption)
                try:
                  await result.copy(LOG_GROUP)
                except Exception:
                  pass
            else:
                result = await client.copy_message(target_chat_id, chat_id, message_id)
                try:
                  await result.copy(LOG_GROUP)
                except Exception:
                  pass
        else:
            result = await client.copy_message(target_chat_id, chat_id, message_id)
            try:
              await result.copy(LOG_GROUP)
            except Exception:
              pass

    except Exception as e:
        error_message = f"Error occurred while sending message to chat ID {target_chat_id}: {str(e)}"
        await client.send_message(sender, error_message)
        await client.send_message(sender, f"Make Bot admin in your Channel - {target_chat_id} and restart the process after /cancel")

async def send_message_with_chat_id(client, sender, message, parse_mode=None):
    chat_id = user_chat_ids.get(sender, sender)
    try:
        result = await client.send_message(chat_id, message, parse_mode=parse_mode)
        try:
          await result.copy(LOG_GROUP)
        except Exception:
          pass
    except Exception as e:
        error_message = f"Error occurred while sending message to chat ID {chat_id}: {str(e)}"
        await client.send_message(sender, error_message)
        await client.send_message(sender, f"Make Bot admin in your Channel - {chat_id} and restart the process after /cancel")

async def send_video_with_chat_id(client, sender, path, caption, duration, hi, wi, thumb_path, upm):
    chat_id = user_chat_ids.get(sender, sender)
    try:
        result = await client.send_video(
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
          await result.copy(LOG_GROUP)
        except Exception:
          pass
    except Exception as e:
        error_message = f"Error occurred while sending video to chat ID {chat_id}: {str(e)}"
        await client.send_message(sender, error_message)
        await client.send_message(sender, f"Make Bot admin in your Channel - {chat_id} and restart the process after /cancel")


async def send_document_with_chat_id(client, sender, path, caption, thumb_path, upm):
    chat_id = user_chat_ids.get(sender, sender)
    try:
        result = await client.send_document(
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
          await result.copy(LOG_GROUP)
        except Exception:
          pass
    except Exception as e:
        error_message = f"Error occurred while sending document to chat ID {chat_id}: {str(e)}"
        await client.send_message(sender, error_message)
        await client.send_message(sender, f"Make Bot admin in your Channel - {chat_id} and restart the process after /cancel")

# --------------------------------------- END SENDING FUNCTIONS - TEAM SPY (@devggn) ---------------------

# ------------------------------- AUTHORIZATION FUNCTIONS ---------------------------------

@teamspy.on(events.NewMessage(incoming=True, pattern='/auth'))
async def _auth(event):
    if event.sender_id == OWNER_ID:
        try:
            user_id = int(event.message.text.split(' ')[1])
        except (ValueError, IndexError):
            return await event.respond("Invalid /auth command. Use /auth USER_ID.")
        SUPER_USERS.add(user_id)
        save_authorized_users(SUPER_USERS)
        await event.respond(f"User {user_id} has been authorized for commands.")
    else:
        await event.respond("You are not authorized to use this command.")

@teamspy.on(events.NewMessage(incoming=True, pattern='/clean'))
async def clear_all_delete_words_command_handler(event):
    if event.sender_id != OWNER_ID:
        return await event.respond("You are not authorized to use this command!")   
    try:
        collection.delete_many({})
        await event.respond("All saved delete words have been cleared for all users.")
    except Exception as e:
        print(f"Error clearing all delete words: {e}")
        await event.respond("An error occurred while clearing all delete words.")

def thumbnail(sender):
    return f'{sender}.jpg' if os.path.exists(f'{sender}.jpg') else None

@teamspy.on(events.NewMessage(incoming=True, pattern='/unauth'))
async def _unauth(event):
    if event.sender_id == OWNER_ID:
        try:
            user_id = int(event.message.text.split(' ')[1])
        except (ValueError, IndexError):
            return await event.respond("Invalid /unauth command. Use /unauth USER_ID.")
        if user_id in SUPER_USERS:
            SUPER_USERS.remove(user_id)
            save_authorized_users(SUPER_USERS)
            await event.respond(f"Authorization revoked for user {user_id}.")
            # Clear user's custom rename preference if set
            if str(user_id) in user_rename_preferences:
                del user_rename_preferences[str(user_id)]
                await event.respond(f"Custom rename preference cleared for user {user_id}.")
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

# ----------------------------- END AUTHORIZATION FUNCTIONS -- TEAM SPY:DEVAGAGAN ---------------------

# Note you can modify the commands if you need authorization for use and want for commercial purposes...
# Edit '#' before rename setchat setcaption etc if you want to restrict them for not using this 

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
            user_session = load_user_session(sender_id)
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
            return False, "**__Invalid Link try again ...__ **"
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
    saved_channel_ids = set()
    try:
        for channel_doc in collection.find({"channel_id": {"$exists": True}}):
            saved_channel_ids.add(channel_doc["channel_id"])
    except Exception as e:
        print(f"Error loading saved channel IDs: {e}")
    return saved_channel_ids

@teamspy.on(events.NewMessage(incoming=True, pattern='/lock'))
async def lock_gagan_handler(event):
    if event.sender_id != OWNER_ID:
        return await event.respond("You are not authorized to use this command.")
    try:
        channel_id = int(event.text.split(' ')[1])
    except (ValueError, IndexError):
        return await event.respond("Invalid /lock command. Use /lock CHANNEL_ID.")
    
    try:
        collection.insert_one({"channel_id": channel_id})
        await event.respond(f"Channel ID {channel_id} locked successfully.")
    except Exception as e:
        await event.respond(f"Error occurred while locking channel ID: {str(e)}")

async def get_msg(userbot, client, sender, edit_id, msg_link, i, file_n):
    edit = ""
    chat = ""
    msg_id = int(i)  
    if msg_id == -1:
        await client.edit_message_text(sender, edit_id, "**__Invalid Link___**")
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
            user_session = load_user_session(sender)
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
                if sender != OWNER_ID:
                    await client.edit_message_text(sender, edit_id, "Please log in via session to use this bot.")
                    return None
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
                edit = await client.edit_message_text(sender, edit_id, "Cloning....")
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
            user_session = load_user_session(sender)
            if user_session:
              file = await user_bot.download_media(msg, progress=progress_for_pyrogram, progress_args=(client, "**__Unrestricting__: __[Team SPY](https://t.me/devggn)__**\n ", edit, time.time()))
              await user_bot.stop()
            else:
              file = await userbot.download_media(msg, progress=progress_for_pyrogram, progress_args=(client, "**__Unrestricting__: __[Team SPY](https://t.me/devggn)__**\n ", edit, time.time()))            # Retrieve user's custom renaming preference if set, default to '@devggn' otherwise
            if not file:
              await client.send_message(sender, "Failed to download the media.")
              return None
            await edit.delete()
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
            new_file_name = video_file_name + "." + file_extension
            os.rename(file, new_file_name)
            file = new_file_name

            path = file
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
                lines = final_caption.split('\n')
                processed_lines = []
                for line in lines:
                    for word in delete_words:
                        line = line.replace(word, '')
                    if line.strip():
                        processed_lines.append(line.strip())
                final_caption = '\n'.join(processed_lines)
                replacements = load_replacement_words(sender)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
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
                await teamspy.send_file(sender, path, caption=caption)
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
                lines = final_caption.split('\n')
                processed_lines = []
                for line in lines:
                    for word in delete_words:
                        line = line.replace(word, '')
                    if line.strip():
                        processed_lines.append(line.strip())
                final_caption = '\n'.join(processed_lines)
                replacements = load_replacement_words(sender)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
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
    
async def get_bulk_msg(userbot, client, sender, msg_link, i):
    x = await client.send_message(sender, "Processing!")
    file_name = ''
    await get_msg(userbot, client, sender, x.id, msg_link, i, file_name) 

# ------------------------------------ PDF WATERMARK FUNCTIONS -----------------------------------------------------------------------

# Contact me and Purchase this code part ... @ggnhere on telegram


#------------------------ FFMPEG CODES and Functions ----------------------------------------------- 

# Puchase Repo from me to get this ... contact @ggnhere on telegram


# ------------------------ Button Mode Editz FOR SETTINGS ----------------------------

DB_NAME = "smart_users"
COLLECTION_NAME = "super_user"

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

user_chat_ids = {}

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

user_rename_preferences = {}

user_caption_preferences = {}

def load_user_session(sender_id):
    user_data = collection.find_one({"user_id": sender_id})
    if user_data:
        return user_data.get("session")
    else:
        return None 

async def set_rename_command(user_id, custom_rename_tag):
    user_rename_preferences[str(user_id)] = custom_rename_tag

def get_user_rename_preference(user_id):
    return user_rename_preferences.get(str(user_id), '@devggn')

# Function to set custom caption preference
async def set_caption_command(user_id, custom_caption):
    # Update the user_caption_preferences dictionary
    user_caption_preferences[str(user_id)] = custom_caption

def get_user_caption_preference(user_id):
    return user_caption_preferences.get(str(user_id), '')

sessions = {}

SET_PIC = "settings.jpg"
MESS = "Customize by your end and Configure your settings ..."

@teamspy.on(events.NewMessage(incoming=True, pattern='/settings'))
async def settings_command(event):
    buttons = [
        [Button.inline("Set Chat ID", b'setchat'), Button.inline("Set Rename Tag", b'setrename')],
        [Button.inline("Caption", b'setcaption'), Button.inline("Replace Words", b'setreplacement')],
        [Button.inline("Remove Words", b'delete'), Button.url("Developer", 'https://t.me/ggnhere')],
        [Button.inline("Login", b'addsession'), Button.inline("Logout", b'logout')],
        [Button.inline("Set Thumbnail", b'setthumb'), Button.inline("Remove Thumbnail", b'remthumb')],
        [Button.url("Repo Link", "https://github.com/devgaganin/Save-Restricted-Content-Bot-Repo/")]
    ]
    
    await teamspy.send_file(
        event.chat_id,
        file=SET_PIC,
        caption=MESS,
        buttons=buttons
    )

pending_photos = {}

@teamspy.on(events.CallbackQuery)
async def callback_query_handler(event):
    user_id = event.sender_id

    if event.data == b'setchat':
        await event.respond("Send me the ID of that chat:")
        sessions[user_id] = 'setchat'

    elif event.data == b'setrename':
        await event.respond("Send me the rename tag:")
        sessions[user_id] = 'setrename'

    elif event.data == b'setcaption':
        await event.respond("Send me the caption:")
        sessions[user_id] = 'setcaption'

    elif event.data == b'setreplacement':
        await event.respond("Send me the replacement words in the format: 'WORD(s)' 'REPLACEWORD'")
        sessions[user_id] = 'setreplacement'

    elif event.data == b'addsession':
        await event.respond("Send your Pyrogram V2 session string to login in bot ...")
        sessions[user_id] = 'addsession'

    elif event.data == b'delete':
        await event.respond("Send words seperated by space to delete them from caption/filename ...")
        sessions[user_id] = 'deleteword'
        
    elif event.data == b'logout':
        result = collection.delete_one({"user_id": user_id})
        if result.deleted_count > 0:
          await event.respond("Logged out and deleted session successfully.")
        else:
          await event.respond("You are not logged in...")

    elif event.data == b'setthumb':
        pending_photos[user_id] = True
        await event.respond('Please send the photo you want to set as the thumbnail.')

    elif event.data == b'remthumb':
        try:
            os.remove(f'{user_id}.jpg')
            await event.respond('Thumbnail removed successfully!')
        except FileNotFoundError:
            await event.respond("No thumbnail found to remove.")


@teamspy.on(events.NewMessage(func=lambda e: e.sender_id in pending_photos))
async def ggn_thumbnail(event):
    user_id = event.sender_id  # Use event.sender_id as user_id

    if event.photo:
        temp_path = await event.download_media()
        if os.path.exists(f'{user_id}.jpg'):
            os.remove(f'{user_id}.jpg')
        os.rename(temp_path, f'./{user_id}.jpg')
        await event.respond('Thumbnail saved successfully!')

    else:
        await event.respond('Please send a photo... Retry')

    # Remove user from pending photos dictionary in both cases
    pending_photos.pop(user_id, None)

@teamspy.on(events.NewMessage)
async def ggn_user_input(event):
    user_id = event.sender_id
    if user_id in sessions:
        session_type = sessions[user_id]

        if session_type == 'setchat':
            try:
                chat_id = int(event.text)
                user_chat_ids[user_id] = chat_id
                await event.respond("Chat ID set successfully!")
            except ValueError:
                await event.respond("Invalid chat ID!")
        
        elif session_type == 'setrename':
            custom_rename_tag = event.text
            await set_rename_command(user_id, custom_rename_tag)
            await event.respond(f"Custom rename tag set to: {custom_rename_tag}")
        
        elif session_type == 'setcaption':
            custom_caption = event.text
            await set_caption_command(user_id, custom_caption)
            await event.respond(f"Custom caption set to: {custom_caption}")

        elif session_type == 'setreplacement':
            match = re.match(r"'(.+)' '(.+)'", event.text)
            if not match:
                await event.respond("Usage: 'WORD(s)' 'REPLACEWORD'")
            else:
                word, replace_word = match.groups()
                delete_words = load_delete_words(user_id)
                if word in delete_words:
                    await event.respond(f"The word '{word}' is in the delete set and cannot be replaced.")
                else:
                    replacements = load_replacement_words(user_id)
                    replacements[word] = replace_word
                    save_replacement_words(user_id, replacements)
                    await event.respond(f"Replacement saved: '{word}' will be replaced with '{replace_word}'")

        elif session_type == 'addsession':
            # Store session string in MongoDB
            session_data = {
                "user_id": user_id,
                "session": event.text
            }
            collection.update_one(
                {"user_id": user_id},
                {"$set": session_data},
                upsert=True
            )
            await event.respond("Session string added successfully.")

        elif session_type == 'deleteword':
            words_to_delete = event.message.text.split()
            delete_words = load_delete_words(user_id)
            delete_words.update(words_to_delete)
            save_delete_words(user_id, delete_words)
            await event.respond(f"Words added to delete list: {', '.join(words_to_delete)}")         

        del sessions[user_id]
