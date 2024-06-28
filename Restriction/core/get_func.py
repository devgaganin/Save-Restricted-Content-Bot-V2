#devggn

import asyncio
import time
import os
import subprocess
import requests
from Restriction import app
from pyrogram import filters
from pyrogram.errors import ChannelBanned, ChannelInvalid, ChannelPrivate, ChatIdInvalid, ChatInvalid, PeerIdInvalid
from pyrogram.enums import MessageMediaType
from Restriction.core.func import progress_bar
from Restriction.core.mongo import db
from config import LOG_GROUP
import cv2

def video_metadata(file):
    vcap = cv2.VideoCapture(f'{file}')
    width = round(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = round(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vcap.get(cv2.CAP_PROP_FPS)
    frame_count = vcap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = round(frame_count / fps)
    return {'width': width, 'height': height, 'duration': duration}
    
    
async def download_thumbnail(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename


def replace_text(original_text, replace_txt, to_replace):
    return original_text.replace(replace_txt, to_replace)

def remove_elements(words, cap):
    lol = cap
    for i in words:
        lol = lol.replace(i, '')
    return lol


# Initialize the dictionary to store user preferences for renaming
user_rename_preferences = {}

# Function to handle the /setrename command
async def set_rename_command(user_id, custom_rename_tag):
    # Update the user_rename_preferences dictionary
    user_rename_preferences[str(user_id)] = custom_rename_tag

# Function to get the user's custom renaming preference
def get_user_rename_preference(user_id):
    # Retrieve the user's custom renaming tag if set, or default to '@devggn'
    return user_rename_preferences.get(str(user_id), '@devggn')

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
                progress_args=("**DOWNLOADING:**\n",edit,time.time()))
            
            chatx = message.chat.id
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
            
            await edit.edit('Preparing to Upload!')

            c = await db.get_data(sender)
            caption = None
            
            if c.get("caption"):
                caption = c.get("caption")
            else:
                caption = msg.caption
                if c.get("clean_words"):
                    words = c.get("clean_words")
                    caption = remove_elements(words, caption)
                    
                if c.get("replace_txt") and c.get("to_replace"):
                    replace_txt = c.get("replace_txt")
                    to_replace = c.get("to_replace")
                    caption = replace_text(caption, replace_txt, to_replace)

            
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
                
                th = await db.get_data(sender)
                if th and th.get("thumb"):
                    thumb_url = th.get("thumb")
                    thumb_path = await download_thumbnail(thumb_url)
                else:
                    try:
                        subprocess.run(f'ffmpeg -i "{file}" -ss 00:01:00 -vframes 1 "{sender}.jpg"', shell=True)
                        thumb_path = f"{sender}.jpg"
                    except:
                        print("failed to genrate thumb")
                        thumb_path = None
                    

                if c.get("chat_id"):
                    channel_id = c.get("chat_id")
                    try:
                        devggn = await app.send_video(
                          chat_id=channel_id,
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
                else:
                    devggn = await app.send_video(
                      chat_id=sender,
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

                if not th.get("thumb") and thumb_path and os.path.exists(thumb_path):
                    os.remove(thumb_path)
                else:
                    print("Thumbnail file not found or failed to generate.")

                os.remove(file)
                    
            elif msg.media == MessageMediaType.PHOTO:
                await edit.edit("Uploading photo...")
                devggn = await app.send_photo(chat_id=sender, photo=file, caption=caption)
                await devggn.copy(LOG_GROUP)
            else:
                th = await db.get_data(sender)
                if th and th.get("thumb"):
                    thumb_url = th.get("thumb")
                    thumb_path = await download_thumbnail(thumb_url)
                else:
                    thumb_path = f"{sender}.jpg"
                    try:
                        if os.path.exists(thumb_path):
                            os.remove(thumb_path)
                        subprocess.run(f'ffmpeg -i "{file}" -ss 00:01:00 -vframes 1 "{sender}.jpg"', shell=True)
                        await message.reply_photo(thumb_path)
                    except:
                        print("failed to genrate thumb")
                        thumb_path = None

                if c.get("chat_id"):
                    channel_id = c.get("chat_id")
                    try:
                        devggn = await app.send_document(
                          chat_id=channel_id,
                          document=file,
                          caption=caption,
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
                else:
                    devggn = await app.send_document(
                      chat_id=sender,
                      document=file,
                      caption=caption,
                      thumb=thumb_path,
                      progress=progress_bar,
                      progress_args=(
                        '**UPLOADING:**\n',
                        edit,
                        time.time()
                      )
                    )
                    await devggn.copy(LOG_GROUP)

                if not th.get("thumb") and thumb_path and os.path.exists(thumb_path):
                    os.remove(thumb_path)
                else:
                    print("Thumbnail file not found or failed to generate.")

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

# ---------------------- devggn edits custom caption for public entities and rename for private entities -----------------------#

user_chat_ids = {}
user_caption_preferences = {}

# Function to set custom caption preference for a user
async def set_caption_command(user_id, custom_caption):
    user_caption_preferences[str(user_id)] = custom_caption
    # You can optionally save this preference to MongoDB if needed

# Function to get user's custom caption preference
def get_user_caption_preference(user_id):
    return user_caption_preferences.get(str(user_id), '')

@app.on_message(filters.command("setcaption"))
async def setcaption_command_handler(_, message):
    user_id = message.from_user.id
    custom_caption = ' '.join(message.command[1:])
    
    if not custom_caption:
        await message.reply_text("Please provide a custom caption.")
        return
    
    await set_caption_command(user_id, custom_caption)
    await message.reply_text(f"Custom caption set to: {custom_caption}")

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

# Dictionary to store delete words for each user
user_delete_words = {}

# Function to load delete words for a user
def load_delete_words(user_id):
    return user_delete_words.get(user_id, [])

# Command to add delete words for a user
@app.on_message(filters.command("delete") & filters.private)
async def add_delete_words(app, message):
    user_id = message.from_user.id
    words_to_delete = message.text.split()[1:]  # Get words after the command

    if not words_to_delete:
        await message.reply("Please provide words to delete after the /delete command.")
        return

    if user_id not in user_delete_words:
        user_delete_words[user_id] = set()

    user_delete_words[user_id].update(words_to_delete)
    await message.reply(f"Words to delete updated: {', '.join(words_to_delete)}")

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
