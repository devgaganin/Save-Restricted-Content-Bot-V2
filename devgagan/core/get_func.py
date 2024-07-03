#devggn

import asyncio
import time
import os
import pymongo
import subprocess
import requests
import re
from devgagan import app
from devgagan import batch
from devgagan import seer as gggn
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid, PeerIdInvalid
from pyrogram.enums import MessageMediaType
from devgagan.core.func import progress_bar, screenshot, video_metadata
from devgagan.core.mongo import db
from config import LOG_GROUP
from config import MONGO_DB as MONGODB_CONNECTION_STRING
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    
    
def thumbnail(sender):
    return f'{sender}.jpg' if os.path.exists(f'{sender}.jpg') else None

async def get_msg(userbot, sender, edit_id, msg_link, i, message):
    edit = ""
    chat = ""
    round_message = False
    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]
    msg_id = int(msg_link.split("/")[-1]) + int(i)

    
    if 't.me/c/' in msg_link or 't.me/b/' in msg_link:
        if 't.me/b/' not in msg_link:
            chat = int('-100' + str(msg_link.split("/")[-2]))
        else:
            chat = msg_link.split("/")[-2]       
        file = ""
        try:
            chatx = message.chat.id
            msg = await userbot.get_messages(chat, msg_id)
            if msg.media:
                if msg.media == MessageMediaType.WEB_PAGE:
                    edit = await app.edit_message_text(sender, edit_id, "Cloning...")
                    await app.send_message(sender, msg.text.markdown)
                    await edit.delete()
                    return
            if not msg.media:
                if msg.text:
                    edit = await app.edit_message_text(sender, edit_id, "Cloning...")
                    devggn = await app.send_message(sender, msg.text.markdown)
                    await devggn.copy(LOG_GROUP)
                    await edit.delete()
                    return
            
            edit = await app.edit_message_text(sender, edit_id, "Trying to Download...")
            file = await userbot.download_media(
                msg,
                progress=progress_bar,
                progress_args=("**__Downloading : __**\n",edit,time.time()))
            
            custom_rename_tag = get_user_rename_preference(chatx)
            last_dot_index = str(file).rfind('.')
            if last_dot_index != -1 and last_dot_index != 0:
                ggn_ext = str(file)[last_dot_index + 1:]
                if ggn_ext.isalpha() and len(ggn_ext) <= 4:
                    original_file_name = str(file)[:last_dot_index]
                    file_extension = str(file)[last_dot_index + 1:]
                else:
                    original_file_name = str(file)
                    file_extension = 'mp4'
            else:
                original_file_name = str(file)
                file_extension = 'mp4'

            delete_words = load_delete_words(chatx)
            for word in delete_words:
                original_file_name = original_file_name.replace(word, "")
            new_file_name = original_file_name + " " + custom_rename_tag + "." + file_extension
            os.rename(file, new_file_name)
            file = new_file_name            
            
            await edit.edit('`Preparing to Upload!`')

            # c = await db.get_data(sender)
            # caption = None
            
            # if c.get("caption"):
            #     caption = c.get("caption")
            # else:
            #     caption = msg.caption
            #     if c.get("clean_words"):
            #         words = c.get("clean_words")
            #         caption = remove_elements(words, caption)
                    
            #     if c.get("replace_txt") and c.get("to_replace"):
            #         replace_txt = c.get("replace_txt")
            #         to_replace = c.get("to_replace")
            #         caption = replace_text(caption, replace_txt, to_replace)

            
            if msg.media == MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"]:

                metadata = video_metadata(file)      
                width= metadata['width']
                height= metadata['height']
                duration= metadata['duration']

                if duration <= 300:
                    devggn = await app.send_video(chat_id=sender, video=file, caption=caption, height=height, width=width, duration=duration, thumb=None, progress=progress_bar, progress_args=('**UPLOADING:**\n', edit, time.time())) 
                    await devggn.copy(LOG_GROUP)
                    await edit.delete()
                    return
                
                delete_words = load_delete_words(sender)
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
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(chatx, chatx)
                
                thumb_path = await screenshot(file, duration, chatx)              
                try:
                    devggn = await app.send_video(
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
                        '**UPLOADING:**\n',
                        edit,
                        time.time()
                        )
                       )
                    await devggn.copy(LOG_GROUP)
                except:
                    await app.edit_message_text(sender, edit_id, "The bot is not an admin in the specified chat.")

                os.remove(file)
                    
            elif msg.media == MessageMediaType.PHOTO:
                await edit.edit("**`Uploading photo...`")
                delete_words = load_delete_words(sender)
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
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(sender, sender)
                devggn = await app.send_photo(chat_id=target_chat_id, photo=file, caption=caption)
                await devggn.copy(LOG_GROUP)

                thumb_path = thumbnail(chatx)
                delete_words = load_delete_words(sender)
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
                replacements = load_replacement_words(chatx)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(chatx, chatx)
                try:
                    devggn = await app.send_document(
                        chat_id=target_chat_id,
                        document=file,
                        caption=caption,
                        thumb=thumb_path,
                        progress=progress_bar,
                        progress_args=(
                        '**`Uploading...`**\n',
                        edit,
                        time.time()
                        )
                    )
                    await devggn.copy(LOG_GROUP)
                except:
                    await app.edit_message_text(sender, edit_id, "The bot is not an admin in the specified chat.") 
                
                os.remove(file)
                        
            await edit.delete()
        
        except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
            await app.edit_message_text(sender, edit_id, "Have you joined the channel?")
            return
        except Exception as e:
            await app.edit_message_text(sender, edit_id, f'Failed to save: `{msg_link}`\n\nError: {str(e)}')       
        
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
        
        caption = f"`{final_caption}\n\n__**{custom_caption}**__`" if custom_caption else f"`{final_caption}`\n\n__**[Team SPY](https://t.me/devggn)**__"
        
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


async def s_msg(userbot, sender, edit_id, msg_link, i, message):
    edit = ""
    chat = ""
    round_message = False
    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]
    msg_id = int(msg_link.split("/")[-1]) + int(i)

    
    if 't.me/c/' in msg_link or 't.me/b/' in msg_link:
        if 't.me/b/' not in msg_link:
            chat = int('-100' + str(msg_link.split("/")[-2]))
        else:
            chat = msg_link.split("/")[-2]       
        file = ""
        try:
            chatx = message.chat.id
            msg = await userbot.get_messages(chat, msg_id)
            if msg.media:
                if msg.media == MessageMediaType.WEB_PAGE:
                    edit = await batch.edit_message_text(sender, edit_id, "Cloning...")
                    await batch.send_message(sender, msg.text.markdown)
                    await edit.delete()
                    return
            if not msg.media:
                if msg.text:
                    edit = await batch.edit_message_text(sender, edit_id, "Cloning...")
                    devggn = await batch.send_message(sender, msg.text.markdown)
                    await devggn.copy(LOG_GROUP)
                    await edit.delete()
                    return
            
            edit = await batch.edit_message_text(sender, edit_id, "Trying to Download...")
            file = await userbot.download_media(
                msg,
                progress=progress_bar,
                progress_args=("**__Downloading : __**\n",edit,time.time()))
            
            custom_rename_tag = get_user_rename_preference(chatx)
            last_dot_index = str(file).rfind('.')
            if last_dot_index != -1 and last_dot_index != 0:
                ggn_ext = str(file)[last_dot_index + 1:]
                if ggn_ext.isalpha() and len(ggn_ext) <= 4:
                    original_file_name = str(file)[:last_dot_index]
                    file_extension = str(file)[last_dot_index + 1:]
                else:
                    original_file_name = str(file)
                    file_extension = 'mp4'
            else:
                original_file_name = str(file)
                file_extension = 'mp4'

            delete_words = load_delete_words(chatx)
            for word in delete_words:
                original_file_name = original_file_name.replace(word, "")
            new_file_name = original_file_name + " " + custom_rename_tag + "." + file_extension
            os.rename(file, new_file_name)
            file = new_file_name            
            
            await edit.edit('`Preparing to Upload!`')

            # c = await db.get_data(sender)
            # caption = None
            
            # if c.get("caption"):
            #     caption = c.get("caption")
            # else:
            #     caption = msg.caption
            #     if c.get("clean_words"):
            #         words = c.get("clean_words")
            #         caption = remove_elements(words, caption)
                    
            #     if c.get("replace_txt") and c.get("to_replace"):
            #         replace_txt = c.get("replace_txt")
            #         to_replace = c.get("to_replace")
            #         caption = replace_text(caption, replace_txt, to_replace)

            
            if msg.media == MessageMediaType.VIDEO and msg.video.mime_type in ["video/mp4", "video/x-matroska"]:

                metadata = video_metadata(file)      
                width= metadata['width']
                height= metadata['height']
                duration= metadata['duration']

                if duration <= 300:
                    devggn = await batch.send_video(chat_id=sender, video=file, caption=caption, height=height, width=width, duration=duration, thumb=None, progress=progress_bar, progress_args=('**UPLOADING:**\n', edit, time.time())) 
                    await devggn.copy(LOG_GROUP)
                    await edit.delete()
                    return
                
                delete_words = load_delete_words(sender)
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
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(chatx, chatx)
                
                thumb_path = await screenshot(file, duration, chatx)              
                try:
                    devggn = await batch.send_video(
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
                        '**UPLOADING:**\n',
                        edit,
                        time.time()
                        )
                       )
                    await devggn.copy(LOG_GROUP)
                except:
                    await batch.edit_message_text(sender, edit_id, "The bot is not an admin in the specified chat.")

                os.remove(file)
                    
            elif msg.media == MessageMediaType.PHOTO:
                await edit.edit("**`Uploading photo...`")
                delete_words = load_delete_words(sender)
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
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(sender, sender)
                devggn = await batch.send_photo(chat_id=target_chat_id, photo=file, caption=caption)
                await devggn.copy(LOG_GROUP)

                thumb_path = thumbnail(chatx)
                delete_words = load_delete_words(sender)
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
                replacements = load_replacement_words(chatx)
                for word, replace_word in replacements.items():
                    final_caption = final_caption.replace(word, replace_word)
                caption = f"{final_caption}\n\n__**{custom_caption}**__" if custom_caption else f"{final_caption}"

                target_chat_id = user_chat_ids.get(chatx, chatx)
                try:
                    devggn = await batch.send_document(
                        chat_id=target_chat_id,
                        document=file,
                        caption=caption,
                        thumb=thumb_path,
                        progress=progress_bar,
                        progress_args=(
                        '**`Uploading...`**\n',
                        edit,
                        time.time()
                        )
                    )
                    await devggn.copy(LOG_GROUP)
                except:
                    await batch.edit_message_text(sender, edit_id, "The bot is not an admin in the specified chat.") 
                
                os.remove(file)
                        
            await edit.delete()
        
        except (ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid):
            await batch.edit_message_text(sender, edit_id, "Have you joined the channel?")
            return
        except Exception as e:
            await batch.edit_message_text(sender, edit_id, f'Failed to save: `{msg_link}`\n\nError: {str(e)}')       
        
    else:
        edit = await batch.edit_message_text(sender, edit_id, "Cloning...")
        try:
            chat = msg_link.split("/")[-2]
            await copy_message_with_chat_id(batch, sender, chat, msg_id) 
            await edit.delete()
        except Exception as e:
            await batch.edit_message_text(sender, edit_id, f'Failed to save: `{msg_link}`\n\nError: {str(e)}')


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

MDB_NAME = "ggndata"
MCOLLECTION_NAME = "userdata"

# Establish a connection to MongoDB
client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
db = client[MDB_NAME]
collection = db[MCOLLECTION_NAME]

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

async def set_rename_command(user_id, custom_rename_tag):
    user_rename_preferences[str(user_id)] = custom_rename_tag

def get_user_rename_preference(user_id):
    return user_rename_preferences.get(str(user_id), '@devggn')

async def set_caption_command(user_id, custom_caption):
    user_caption_preferences[str(user_id)] = custom_caption

def get_user_caption_preference(user_id):
    return user_caption_preferences.get(str(user_id), '')

sessions = {}

SET_PIC = "settings.jpg"
MESS = "Customize by your end and Configure your settings ..."

@gggn.on_message(filters.command("settings"))
async def settings_command(client, message):
    buttons = [
        [InlineKeyboardButton("Set Chat ID", callback_data='setchat'), InlineKeyboardButton("Set Rename Tag", callback_data='setrename')],
        [InlineKeyboardButton("Caption", callback_data='setcaption'), InlineKeyboardButton("Replace Words", callback_data='setreplacement')],
        [InlineKeyboardButton("Remove Words", callback_data='delete'), InlineKeyboardButton("Login", callback_data='addsession')],
        [InlineKeyboardButton("Set Thumbnail", callback_data='setthumb'), InlineKeyboardButton("Remove Thumbnail", callback_data='remthumb')],
        [InlineKeyboardButton("Report Errors", url="https://t.me/devggn")]
    ]
    
    await client.send_photo(
        chat_id=message.chat.id,
        photo=SET_PIC,
        caption=MESS,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

pending_photos = {}
user_states = {}

@gggn.on_callback_query()
async def callback_query_handler(client, callback_query):
    user_id = callback_query.from_user.id

    if callback_query.data == 'setchat':
        await callback_query.message.edit_text("Send me the ID of that chat:")
        sessions[user_id] = 'setchat'

    elif callback_query.data == 'setrename':
        await callback_query.message.edit_text("Send me the rename tag:")
        sessions[user_id] = 'setrename'

    elif callback_query.data == 'setcaption':
        await callback_query.message.edit_text("Send me the caption:")
        sessions[user_id] = 'setcaption'

    elif callback_query.data == 'setreplacement':
        await callback_query.message.edit_text("Send me the replacement words in the format: 'WORD(s)' 'REPLACEWORD'")
        sessions[user_id] = 'setreplacement'

    elif callback_query.data == 'addsession':
        await callback_query.message.edit_text("Method depreciated ... use /login to do login.")

    elif callback_query.data == 'delete':
        await callback_query.message.edit_text("Send words separated by space to delete them from caption/filename ...")
        sessions[user_id] = 'deleteword'

    elif callback_query.data == 'setthumb':
        pending_photos[user_id] = True
        await callback_query.message.edit_text('Please send the photo you want to set as the thumbnail.')

    elif callback_query.data == 'remthumb':
        try:
            os.remove(f'{user_id}.jpg')
            await callback_query.message.edit_text('Thumbnail removed successfully!')
        except FileNotFoundError:
            await callback_query.message.edit_text("No thumbnail found to remove.")


@gggn.on_message(filters.photo & filters.user(list(pending_photos.keys())))
async def save_thumbnail(client, message):
    user_id = message.from_user.id

    if message.photo:
        temp_path = await message.download()
        if os.path.exists(f'{user_id}.jpg'):
            os.remove(f'{user_id}.jpg')
        os.rename(temp_path, f'./{user_id}.jpg')
        await message.reply_text('Thumbnail saved successfully!')

    else:
        await message.reply_text('Please send a photo... Retry')

    pending_photos.pop(user_id, None)


@gggn.on_message()
async def handle_user_input(client, message):
    user_id = message.from_user.id
    if user_id in sessions:
        session_type = sessions[user_id]

        if session_type == 'setchat':
            try:
                chat_id = int(message.text)
                user_chat_ids[user_id] = chat_id
                await message.reply_text("Chat ID set successfully!")
            except ValueError:
                await message.reply_text("Invalid chat ID!")
        
        elif session_type == 'setrename':
            custom_rename_tag = message.text
            await set_rename_command(user_id, custom_rename_tag)
            await message.reply_text(f"Custom rename tag set to: {custom_rename_tag}")
        
        elif session_type == 'setcaption':
            custom_caption = message.text
            await set_caption_command(user_id, custom_caption)
            await message.reply_text(f"Custom caption set to: {custom_caption}")

        elif session_type == 'setreplacement':
            match = re.match(r"'(.+)' '(.+)'", message.text)
            if not match:
                await message.reply_text("Usage: 'WORD(s)' 'REPLACEWORD'")
            else:
                word, replace_word = match.groups()
                delete_words = load_delete_words(user_id)
                if word in delete_words:
                    await message.reply_text(f"The word '{word}' is in the delete set and cannot be replaced.")
                else:
                    replacements = load_replacement_words(user_id)
                    replacements[word] = replace_word
                    save_replacement_words(user_id, replacements)
                    await message.reply_text(f"Replacement saved: '{word}' will be replaced with '{replace_word}'")
                
        elif session_type == 'deleteword':
            words_to_delete = message.text.split()
            delete_words = load_delete_words(user_id)
            delete_words.update(words_to_delete)
            save_delete_words(user_id, delete_words)
            await message.reply_text(f"Words added to delete list: {', '.join(words_to_delete)}")       

        del sessions[user_id]
