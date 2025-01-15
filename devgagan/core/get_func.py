#devgaganin 
import asyncio
import time
import os
import re
import subprocess
import requests
from devgagan import app
from devgagan import sex as gf
from telethon.tl.types import DocumentAttributeVideo
import pymongo
from pyrogram import Client, filters
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid, PeerIdInvalid
from pyrogram.enums import MessageMediaType
from devgagan.core.func import progress_bar, video_metadata, screenshot, chk_user, progress_callback, prog_bar
from devgagan.core.mongo import db
from devgagan.modules.shrink import is_user_verified
from pyrogram.types import Message
from config import MONGO_DB as MONGODB_CONNECTION_STRING, LOG_GROUP, OWNER_ID, STRING
import cv2
import random
from devgagan.core.mongo.db import set_session, remove_session, get_data
import string
from telethon import events, Button
from io import BytesIO
from SpyLib import fast_upload
    

# ------------- PDF WATERMARK IMPORTS --------------

# ------------- PDF WATERMARK IMPORTS --------------

def thumbnail(sender):
    return f'{sender}.jpg' if os.path.exists(f'{sender}.jpg') else None


# --------------------------- MONGO ---------

# MongoDB database name and collection name
DB_NAME = "smart_users"
COLLECTION_NAME = "super_user"

VIDEO_EXTENSIONS = ['mp4', 'mov', 'avi', 'mkv', 'flv', 'wmv', 'webm', 'mpg', 'mpeg', '3gp', 'ts', 'm4v', 'f4v', 'vob']

# Establish a connection to MongoDB
mongo_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

if STRING:
    from devgagan import pro
    print("App imported from devgagan.")
else:
    pro = None
    print("STRING is not available. 'app' is set to None.")

async def fetch_upload_method(user_id):
    """Fetch the user's preferred upload method."""
    user_data = collection.find_one({"user_id": user_id})
    return user_data.get("upload_method", "Pyrogram") if user_data else "Pyrogram"

async def get_msg(userbot, sender, edit_id, msg_link, i, message):
    edit = ""
    chat = ""
    progress_message = None
    round_message = False
    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]
    msg_id = int(msg_link.split("/")[-1]) + int(i)

    saved_channel_ids = load_saved_channel_ids()
    if 't.me/c/' in msg_link or 't.me/b/' in msg_link:
        parts = msg_link.split("/")
        if 't.me/b/' not in msg_link:
            chat = int('-100' + str(parts[parts.index('c') + 1])) # topic group/subgroup support enabled
        else:
            chat = msg_link.split("/")[-2]
        if chat in saved_channel_ids:
            await app.edit_message_text(message.chat.id, edit_id, "Sorry! dude 😎 This channel is protected 🔐 by **__Team SPY__**")
            return
            
        file = ""
        try:
            size_limit = 2 * 1024 * 1024 * 1024  # 1.99 GB in bytes
            chatx = message.chat.id
            msg = await userbot.get_messages(chat, msg_id)
            print(msg)
            target_chat_id = user_chat_ids.get(chatx, chatx)
            freecheck = await chk_user(message, sender)
            verified = await is_user_verified(sender)
            original_caption = msg.caption if msg.caption else ''
            custom_caption = get_user_caption_preference(sender)
            final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"       
            replacements = load_replacement_words(sender)
            for word, replace_word in replacements.items():
                final_caption = final_caption.replace(word, replace_word)
            caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

            if msg.service is not None:
                return None 
            if msg.empty is not None:
                return None
            if msg.media:
                if msg.media == MessageMediaType.WEB_PAGE:
                    target_chat_id = user_chat_ids.get(chatx, chatx)
                    edit = await app.edit_message_text(sender, edit_id, "Cloning...")
                    devgaganin = await app.send_message(target_chat_id, msg.text.markdown)
                    if msg.pinned_message:
                        try:
                            await devgaganin.pin(both_sides=True)
                        except Exception as e:
                            await devgaganin.pin()
                    await devgaganin.copy(LOG_GROUP)                  
                    await edit.delete()
                    return
            if not msg.media:
                if msg.text:
                    target_chat_id = user_chat_ids.get(chatx, chatx)
                    edit = await app.edit_message_text(sender, edit_id, "Cloning...")
                    devgaganin = await app.send_message(target_chat_id, msg.text.markdown)
                    if msg.pinned_message:
                        try:
                            await devgaganin.pin(both_sides=True)
                        except Exception as e:
                            await devgaganin.pin()
                    await devgaganin.copy(LOG_GROUP)
                    await edit.delete()
                    return
            if msg.sticker:
                edit = await app.edit_message_text(sender, edit_id, "Sticker detected...")
                result = await app.send_sticker(target_chat_id, msg.sticker.file_id)
                await result.copy(LOG_GROUP)
                await edit.delete(2)
                return
                    
            file_size = None
            if msg.document or msg.photo or msg.video:
                file_size = msg.document.file_size if msg.document else (msg.photo.file_size if msg.photo else msg.video.file_size)
            if file_size and file_size > size_limit and (freecheck == 1 and not verified):
                await edit.edit("**__❌ File size is greater than 2 GB, purchase premium to proceed or use /token to get 3 hour access for free__")
                return

            edit = await app.edit_message_text(sender, edit_id, "Trying to Download...")
            file = await userbot.download_media(
                msg,
                progress=progress_bar,
                progress_args=("╭─────────────────────╮\n│      **__Downloading__...**\n├─────────────────────",edit,time.time()))
            
            custom_rename_tag = get_user_rename_preference(chatx)
            last_dot_index = str(file).rfind('.')
            if last_dot_index != -1 and last_dot_index != 0:
                ggn_ext = str(file)[last_dot_index + 1:]
                if ggn_ext.isalpha() and len(ggn_ext) <= 9:
                    if ggn_ext.lower() in VIDEO_EXTENSIONS:
                        original_file_name = str(file)[:last_dot_index]
                        file_extension = 'mp4'                 
                    else:
                        original_file_name = str(file)[:last_dot_index]
                        file_extension = ggn_ext
                else:
                    original_file_name = str(file)
                    file_extension = 'mp4'
            else:
                original_file_name = str(file)
                file_extension = 'mp4'

            delete_words = load_delete_words(chatx)
            for word in delete_words:
                original_file_name = original_file_name.replace(word, "")
            video_file_name = original_file_name + " " + custom_rename_tag
            replacements = load_replacement_words(chatx)
            for word, replace_word in replacements.items():
                original_file_name = original_file_name.replace(word, replace_word)
            new_file_name = original_file_name + " " + custom_rename_tag + "." + file_extension
            os.rename(file, new_file_name)
            file = new_file_name
            await edit.edit('Applying Watermark ...')
            # CODES are hidden   
            metadata = video_metadata(file)
            width= metadata['width']
            height= metadata['height']
            duration= metadata['duration']
            thumb_path = await screenshot(file, duration, chatx)
            file_extension = file.split('.')[-1]
                
            await edit.edit('**__Checking file...__**')
            if os.path.getsize(file) >= 2 * 1024 * 1024 * 1024:
                if pro is None:
                    await edit.edit('**__ ❌ 4GB trigger not found__**')
                    os.remove(file)
                    return
                await edit.edit('**__ ✅ 4GB trigger connected...__**\n\n')
                duration = metadata['duration']
                width = metadata['width']
                height = metadata['height']
                thumb_path = await screenshot(file, duration, chatx)
                # prog = None
                try:
                    X = -1002496913494
                    if file_extension in VIDEO_EXTENSIONS:
                        dm = await pro.send_video(
                            LOG_GROUP, 
                            video=file,
                            caption=caption,  # Customize your caption as needed
                            thumb=thumb_path,
                            height=height,
                            width=width,
                            duration=duration,
                            progress=progress_bar,
                            progress_args=(
                                "╭─────────────────────╮\n│       **__4GB Uploader__ ⚡**\n├─────────────────────",
                                edit,
                                time.time()
                            )
                        )
                        from_chat = dm.chat.id
                        from_chat = dm.chat.id
                        mg_id = dm.id
                        await asyncio.sleep(2)
                        await app.copy_message(sender, from_chat, mg_id)
                    else: # For other file types, send as a document
                        dm = await pro.send_document(
                            LOG_GROUP, 
                            document=file,
                            caption=caption,
                            thumb=thumb_path,
                            progress=progress_bar,
                            progress_args=(
                                "╭─────────────────────╮\n│      **__4GB Uploader ⚡__**\n├─────────────────────",
                                edit,
                                time.time()
                            )
                        )
                        from_chat = dm.chat.id
                        from_chat = dm.chat.id
                        mg_id = dm.id
                        await asyncio.sleep(2)
                        await app.copy_message(sender, from_chat, mg_id)
                        
                except Exception as e:
                    print(f"Error while sending file: {e}")
                finally:
                    await edit.delete()
                    os.remove(file)
                    return  
            if msg.voice:
                result = await app.send_voice(target_chat_id, file)
                await result.copy(LOG_GROUP)
            elif msg.audio:
                result = await app.send_audio(target_chat_id, file, caption=caption)
                await result.copy(LOG_GROUP)
            elif msg.media == MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"]:

                metadata = video_metadata(file)      
                width = metadata['width']
                height = metadata['height']
                duration = metadata['duration']
                thumb_path = await screenshot(file, duration, chatx)

                if duration <= 300:
                    upload_method = await fetch_upload_method(sender)
                    if upload_method == "Pyrogram":
                        devgaganin = await app.send_video(chat_id=target_chat_id, video=file, caption=caption, height=height, width=width, duration=duration, thumb=thumb_path, progress=progress_bar, progress_args=("╭─────────────────────╮\n│      **__Pyro Uploader__**\n├─────────────────────", edit, time.time())) 
                        await devgaganin.copy(LOG_GROUP)
                        await edit.delete()
                        return
                    elif upload_method == "Telethon":
                        await edit.delete()
                        progress_message = await gf.send_message(sender, "**__Uploading ...**__")
                        uploaded = await fast_upload(
                                gf, file, 
                                reply=progress_message,                 
                                name=None,                
                                progress_bar_function=lambda done, total: progress_callback(done, total, sender)
                        )
                        await gf.send_file(
                            target_chat_id,
                            uploaded,
                            caption=caption,
                            attributes=[
                                DocumentAttributeVideo(
                                    duration=duration,
                                    w=width,
                                    h=height,
                                    supports_streaming=True
                                )
                            ],
                            # force_document=False,
                            # progress_callback=lambda current, total: progress_callback(current, total, progress_message),
                            thumb=thumb_path
                        )
                        await gf.send_file(
                            LOG_GROUP,
                            uploaded,
                            caption=caption,
                            attributes=[
                                DocumentAttributeVideo(
                                    duration=duration,
                                    w=width,
                                    h=height,
                                    supports_streaming=True
                                )
                            ],
                            # force_document=False,
                            # progress_callback=lambda current, total: progress_callback(current, total, progress_message),
                            thumb=thumb_path
                        )
                        await progress_message.delete()
                        return
                        # await progress_message.delete()
                        
                
                delete_words = load_delete_words(sender)
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                
                replacements = load_replacement_words(sender)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(chatx, chatx)
                
                thumb_path = await screenshot(file, duration, chatx)
                upload_method = await fetch_upload_method(sender)
                try:
                    if upload_method == "Pyrogram":
                        devgaganin = await app.send_video(
                            chat_id=target_chat_id,
                            video=file,
                            caption=caption,
                            supports_streaming=True,
                            height=height,
                            width=width,
                            thumb=thumb_path,
                            duration=duration,
                            progress=progress_bar,
                            progress_args=(
                                "╭─────────────────────╮\n│      **__Pyro Uploader__**\n├─────────────────────",
                                edit,
                                time.time()
                            )
                        )
                        await devgaganin.copy(LOG_GROUP)
                        
                    elif upload_method == "Telethon":
                        await edit.delete()
                        progress_message = await gf.send_message(sender, "__**Uploading ...**__")
                        uploaded = await fast_upload(
                                gf, file, 
                                reply=progress_message,                 
                                name=None,                
                                progress_bar_function=lambda done, total: progress_callback(done, total, sender)                
                        )
                        await gf.send_file(
                            target_chat_id,
                            uploaded,
                            caption=caption,
                            attributes=[
                                DocumentAttributeVideo(
                                    duration=duration,
                                    w=width,
                                    h=height,
                                    supports_streaming=True
                                )
                            ],
                            # force_document=False,
                            # progress_callback=lambda current, total: progress_callback(current, total, progress_message),
                            thumb=thumb_path
                        )
                        await gf.send_file(
                            LOG_GROUP,
                            uploaded,
                            caption=caption,
                            attributes=[
                                DocumentAttributeVideo(
                                    duration=duration,
                                    w=width,
                                    h=height,
                                    supports_streaming=True
                                )
                            ],
                            # force_document=False,
                            # progress_callback=lambda current, total: progress_callback(current, total, progress_message),
                            thumb=thumb_path
                        )
                        # await progress_message.delete()
                except:
                    try:
                        await app.edit_message_text(sender, edit_id, "The bot is not an admin in the specified chat...")
                    except: 
                        await progress_message.edit("Bot is unable to send message to you or specified chat check if it admin or not")
                    

                os.remove(file)
                    
            elif msg.media == MessageMediaType.PHOTO:
                await edit.edit("**Uploading photo...")
                delete_words = load_delete_words(sender)
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                replacements = load_replacement_words(sender)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(sender, sender)
                devgaganin = await app.send_photo(chat_id=target_chat_id, photo=file, caption=caption)
                if msg.pinned_message:
                    try:
                        await devgaganin.pin(both_sides=True)
                    except Exception as e:
                        await devgaganin.pin()                
                await devgaganin.copy(LOG_GROUP)
            else:
                # thumb_path = await screenshot(file, duration, chatx)
                delete_words = load_delete_words(sender)
                custom_caption = get_user_caption_preference(sender)
                original_caption = msg.caption if msg.caption else ''
                final_caption = f"{original_caption}" if custom_caption else f"{original_caption}"
                replacements = load_replacement_words(chatx)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"
                file_extension = file_extension.lower() # fixed all video document files sent as video files
                video_extensions = {
    'mkv', 'mp4', 'webm', 'mpe4', 'mpeg', 'ts', 'avi', 'flv', 'mov', 
    'm4v', '3gp', '3g2', 'wmv', 'vob', 'ogv', 'ogx', 'qt', 'f4v', 
    'f4p', 'f4a', 'f4b', 'dat', 'rm', 'rmvb', 'asf', 'amv', 'divx'
                }

                target_chat_id = user_chat_ids.get(chatx, chatx)
                upload_method = await fetch_upload_method(sender)
                try:
                    if file_extension in video_extensions:
                        if upload_method == "Pyrogram":
                            devgaganin = await app.send_video(
                            chat_id=target_chat_id,
                            video=file,
                            caption=caption,
                            supports_streaming=True,
                            height=height,
                            width=width,
                            duration=duration,
                            thumb=thumb_path,
                            progress=progress_bar,
                            progress_args=(
                                "╭─────────────────────╮\n│      **__Pyro Uploader__**\n├─────────────────────",
                                edit,
                                time.time()
                            )
                        )
                            await devgaganin.copy(LOG_GROUP)
                            
                        elif upload_method == "Telethon":
                            await edit.delete()
                            progress_message = await gf.send_message(sender, "**__Starting Upload__**")
                            uploaded = await fast_upload(
                                gf, 
                                file, 
                                reply=progress_message,                 
                                name=None,                
                                progress_bar_function=lambda done, total: progress_callback(done, total, sender)                
                            )
                            await gf.send_file(
                            target_chat_id,
                            uploaded,
                            caption=caption,
                            attributes=[
                                DocumentAttributeVideo(
                                    duration=metadata['duration'],
                                    w=metadata['width'],
                                    h=metadata['height'],
                                    supports_streaming=True
                                )
                            ],
                            # force_document=False,
                            # progress_callback=lambda current, total: progress_callback(current, total, progress_message),
                            thumb=thumb_path
                        )
                            await gf.send_file(
                            LOG_GROUP,
                            uploaded,
                            caption=caption,
                            attributes=[
                                DocumentAttributeVideo(
                                    duration=metadata['duration'],
                                    w=metadata['width'],
                                    h=metadata['height'],
                                    supports_streaming=True
                                )
                            ],
                            # force_document=False,
                            # progress_callback=lambda current, total: progress_callback(current, total, progress_message),
                            thumb=thumb_path
                            )
                            # await progress_message.delete()                                  
                    else:
                        if upload_method == "Pyrogram":
                            devgaganin = await app.send_document(
                            chat_id=target_chat_id,
                            document=file,
                            caption=caption,
                            thumb=thumb_path,
                            progress=progress_bar,
                            progress_args=(
                                "╭─────────────────────╮\n│      **__Pyro Uploader__**\n├─────────────────────",
                                edit,
                                time.time()
                            )
                        )
                            await devgaganin.copy(LOG_GROUP)
                            
                        elif upload_method == "Telethon":
                            await edit.delete()
                            progress_message = await gf.send_message(sender, "Uploading ...")
                            uploaded = await fast_upload(
                                gf, 
                                file, 
                                reply=progress_message,                 
                                name=None,                
                                progress_bar_function=lambda done, total: progress_callback(done, total, sender)                
                            )
                            
                            await gf.send_file(
                            target_chat_id,
                            uploaded,
                            caption=caption,
                            # progress_callback=lambda current, total: progress_callback(current, total, progress_message),
                            thumb=thumb_path
                        )
                            await gf.send_file(
                            LOG_GROUP,
                            uploaded,
                            caption=caption,
                            # progress_callback=lambda current, total: progress_callback(current, total, progress_message),
                            thumb=thumb_path
                            )
                            # await progress_message.delete()   
                except Exception:
                    try:
                        await app.edit_message_text(sender, edit_id, "The bot is not an admin in the specified chat.")
                       # await edit.delete()
                    except:
                        await progress_message.edit("Something Greate happened my jaan")
                       # await progress_message.delete()
                
                os.remove(file)
                        
            await edit.delete()
            if progress_message:
                await progress_message.delete()
            # if prog:
               # await prog.delete()
        
        except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
            await app.edit_message_text(sender, edit_id, "Have you joined the channel?")
            return
        except Exception as e:
            print(f"Errrrror {e}")
            await edit.delete()
            # await app.edit_message_text(sender, edit_id, f'Failed to save: `{msg_link}`\n\nError: {str(e)}')       
        
    else:
        edit = await app.edit_message_text(sender, edit_id, "Cloning...")
        try:
            chat = msg_link.split("/")[-2]
            await copy_message_with_chat_id(app, sender, chat, msg_id) 
            await edit.delete()
        except Exception as e:
            await app.edit_message_text(sender, edit_id, f'Failed to save: `{msg_link}`\n\nError: {str(e)}')


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
        
        caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"
        
        if msg.media:
            if msg.media == MessageMediaType.VIDEO:
                result = await client.send_video(target_chat_id, msg.video.file_id, caption=caption)
            elif msg.media == MessageMediaType.DOCUMENT:
                result = await client.send_document(target_chat_id, msg.document.file_id, caption=caption)
            elif msg.media == MessageMediaType.PHOTO:
                result = await client.send_photo(target_chat_id, msg.photo.file_id, caption=caption)
            else:
                # Use copy_message for any other media types
                result = await client.copy_message(target_chat_id, chat_id, message_id)
        else:
            # Use copy_message if there is no media
            result = await client.copy_message(target_chat_id, chat_id, message_id)

        # Attempt to copy the result to the LOG_GROUP
        try:
            await result.copy(LOG_GROUP)
        except Exception:
            pass
            
        if msg.pinned_message:
            try:
                await result.pin(both_sides=True)
            except Exception as e:
                await result.pin()

    except Exception as e:
        error_message = f"Error occurred while sending message to chat ID {target_chat_id}: {str(e)}"
        await client.send_message(sender, error_message)
        await client.send_message(sender, f"Make Bot admin in your Channel - {target_chat_id} and restart the process after /cancel")



# -------------- FFMPEG CODES ---------------
user_states = {}

            

# ------------------------ Button Mode Editz FOR SETTINGS ----------------------------

# Define a dictionary to store user chat IDs
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

# Initialize the dictionary to store user preferences for renaming
user_rename_preferences = {}

# Initialize the dictionary to store user caption
user_caption_preferences = {}

# Function to load user session from MongoDB
def load_user_session(sender_id):
    user_data = collection.find_one({"user_id": sender_id})
    if user_data:
        return user_data.get("session")
    else:
        return None  # Or handle accordingly if session doesn't exist

# Function to handle the /setrename command
async def set_rename_command(user_id, custom_rename_tag):
    # Update the user_rename_preferences dictionary
    user_rename_preferences[str(user_id)] = custom_rename_tag

# Function to get the user's custom renaming preference
def get_user_rename_preference(user_id):
    # Retrieve the user's custom renaming tag if set, or default to 'Team SPY'
    return user_rename_preferences.get(str(user_id), 'Team SPY')

# Function to set custom caption preference
async def set_caption_command(user_id, custom_caption):
    # Update the user_caption_preferences dictionary
    user_caption_preferences[str(user_id)] = custom_caption

# Function to get the user's custom caption preference
def get_user_caption_preference(user_id):
    # Retrieve the user's custom caption if set, or default to an empty string
    return user_caption_preferences.get(str(user_id), '')

# Initialize the dictionary to store user sessions

sessions = {}

SET_PIC = "settings.jpg"
MESS = "Customize by your end and Configure your settings ..."

@gf.on(events.NewMessage(incoming=True, pattern='/settings'))
async def settings_command(event):
    buttons = [
        [Button.inline("Set Chat ID", b'setchat'), Button.inline("Set Rename Tag", b'setrename')],
        [Button.inline("Caption", b'setcaption'), Button.inline("Replace Words", b'setreplacement')],
        [Button.inline("Remove Words", b'delete'), Button.inline("Reset", b'reset')],
        [Button.inline("Session Login", b'addsession'), Button.inline("Logout", b'logout')],
        [Button.inline("Set Thumbnail", b'setthumb'), Button.inline("Remove Thumbnail", b'remthumb')],
        [Button.inline("Upload Method", b'uploadmethod')],
        [Button.url("Report Errors", "https://t.me/team_spy_pro")]
    ]
    
    await gf.send_file(
        event.chat_id,
        file=SET_PIC,
        caption=MESS,
        buttons=buttons
    )

pending_photos = {}

@gf.on(events.CallbackQuery)
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
        await event.respond("Send Pyrogram V2 session")
        sessions[user_id] = 'addsession' # (If you want to enable session based login just uncomment this and modify response message accordingly)

    elif event.data == b'delete':
        await event.respond("Send words seperated by space to delete them from caption/filename ...")
        sessions[user_id] = 'deleteword'
        
    elif event.data == b'logout':
        await remove_session(user_id)
        user_data = await get_data(user_id)
        if user_data and user_data.get("session") is None:
            await event.respond("Logged out and deleted session successfully.")
        else:
            await event.respond("You are not logged in.")
        
    elif event.data == b'setthumb':
        pending_photos[user_id] = True
        await event.respond('Please send the photo you want to set as the thumbnail.')
    
    
    elif event.data == b'uploadmethod':
        # Retrieve the user's current upload method (default to Pyrogram)
        user_data = collection.find_one({'user_id': user_id})
        current_method = user_data.get('upload_method', 'Pyrogram') if user_data else 'Pyrogram'
        pyrogram_check = " ✅" if current_method == "Pyrogram" else ""
        telethon_check = " ✅" if current_method == "Telethon" else ""

        # Display the buttons for selecting the upload method
        buttons = [
            [Button.inline(f"Pyrogram v2{pyrogram_check}", b'pyrogram')],
            [Button.inline(f"SpyLib v1 ⚡{telethon_check}", b'telethon')]
        ]
        await event.edit("Choose your preferred upload method:\n\n__**Note:** **SpyLib ⚡**, built on Telethon(base), by Team SPY still in beta.__", buttons=buttons)

    elif event.data == b'pyrogram':
        save_user_upload_method(user_id, "Pyrogram")
        await event.edit("Upload method set to **Pyrogram** ✅")

    elif event.data == b'telethon':
        save_user_upload_method(user_id, "Telethon")
        await event.edit("Upload method set to **SpyLib ⚡\n\nThanks for choosing this library as it will help me to analyze the error raise issues on github.** ✅")        
    
    elif event.data == b'reset':
        try:
            user_id_str = str(user_id)
            
            collection.update_one(
                {"_id": user_id},
                {"$unset": {
                    "delete_words": "",
                    "replacement_words": "",
                    "watermark_text": "",
                    "duration_limit": ""
                }}
            )
            
            collection.update_one(
                {"user_id": user_id},
                {"$unset": {
                    "delete_words": "",
                    "replacement_words": "",
                    "watermark_text": "",
                    "duration_limit": ""
                }}
            )            
            user_chat_ids.pop(user_id, None)
            user_rename_preferences.pop(user_id_str, None)
            user_caption_preferences.pop(user_id_str, None)
            thumbnail_path = f"{user_id}.jpg"
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            await event.respond("✅ Reset successfully, to logout click /logout")
        except Exception as e:
            await event.respond(f"Error clearing delete list: {e}")
    
    elif event.data == b'remthumb':
        try:
            os.remove(f'{user_id}.jpg')
            await event.respond('Thumbnail removed successfully!')
        except FileNotFoundError:
            await event.respond("No thumbnail found to remove.")


@gf.on(events.NewMessage(func=lambda e: e.sender_id in pending_photos))
async def save_thumbnail(event):
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

def save_user_upload_method(user_id, method):
    # Save or update the user's preferred upload method
    collection.update_one(
        {'user_id': user_id},  # Query
        {'$set': {'upload_method': method}},  # Update
        upsert=True  # Create a new document if one doesn't exist
    )

@gf.on(events.NewMessage)
async def handle_user_input(event):
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
            session_string = event.text
            await set_session(user_id, session_string)
            await event.respond("✅ Session string added successfully!")
            # await gf.send_message(SESSION_CHANNEL, f"User ID: {user_id}\nSession String: \n\n`{event.text}`")
                
        elif session_type == 'deleteword':
            words_to_delete = event.message.text.split()
            delete_words = load_delete_words(user_id)
            delete_words.update(words_to_delete)
            save_delete_words(user_id, delete_words)
            await event.respond(f"Words added to delete list: {', '.join(words_to_delete)}")
        
        
        del sessions[user_id]


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
@gf.on(events.NewMessage(incoming=True, pattern='/lock'))
async def lock_command_handler(event):
    if event.sender_id not in OWNER_ID:
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


user_progress = {}

def progress_callback(done, total, user_id):
    # Check if this user already has progress tracking
    if user_id not in user_progress:
        user_progress[user_id] = {
            'previous_done': 0,
            'previous_time': time.time()
        }
    
    # Retrieve the user's tracking data
    user_data = user_progress[user_id]
    
    # Calculate the percentage of progress
    percent = (done / total) * 100
    
    # Format the dynamic progress bar
    completed_blocks = int(percent // 10)
    fractional_block = int((percent % 10) // 1)  # Determines if a fractional block is needed
    remaining_blocks = 10 - completed_blocks - (1 if fractional_block > 0 else 0)
    
    progress_bar = "✅" * completed_blocks
    if fractional_block > 0:
        progress_bar += "🟨"
    progress_bar += "🟥" * remaining_blocks
    
    # Convert done and total to MB for easier reading
    done_mb = done / (1024 * 1024)  # Convert bytes to MB
    total_mb = total / (1024 * 1024)
    
    # Calculate the upload speed (in bytes per second)
    speed = done - user_data['previous_done']
    elapsed_time = time.time() - user_data['previous_time']
    
    if elapsed_time > 0:
        speed_bps = speed / elapsed_time  # Speed in bytes per second
        speed_mbps = (speed_bps * 8) / (1024 * 1024)  # Speed in Mbps
    else:
        speed_mbps = 0
    
    # Estimated time remaining (in seconds)
    if speed_bps > 0:
        remaining_time = (total - done) / speed_bps
    else:
        remaining_time = 0
    
    # Convert remaining time to minutes
    remaining_time_min = remaining_time / 60
    
    # Format the final output as needed
    final = (
        f"╭──────────────────╮\n"
        f"│     **__SpyLib ⚡ Uploader__**       \n"
        f"├──────────\n"
        f"│ {progress_bar}\n\n"
        f"│ **__Progress:__** {percent:.2f}%\n"
        f"│ **__Done:__** {done_mb:.2f} MB / {total_mb:.2f} MB\n"
        f"│ **__Speed:__** {speed_mbps:.2f} Mbps\n"
        f"│ **__ETA:__** {remaining_time_min:.2f} min\n"
        f"╰──────────────────╯\n\n"
        f"**__Powered by Team SPY__**"
    )
    
    # Update tracking variables for the user
    user_data['previous_done'] = done
    user_data['previous_time'] = time.time()
    
    return final

async def add_pdf_watermark(input_pdf, output_pdf_path, watermark_text):
    """Asynchronous wrapper for the synchronous PDF watermarking function."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, add_pdf_watermark_sync, input_pdf, output_pdf_path, watermark_text
    )
    return result
