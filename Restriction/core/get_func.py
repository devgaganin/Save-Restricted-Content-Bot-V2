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
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from Restriction.core.func import progress_bar
from Restriction.core.mongo import db



def get_duration(filepath):
    try:
        metadata = extractMetadata(createParser(filepath))
        if metadata:
            duration = metadata.get("duration").seconds if metadata.has("duration") else 0
            width = metadata.get("width") if metadata.has("width") else 1280
            height = metadata.get("height") if metadata.has("height") else 720
            return duration, width, height
    except:
        return 0, 1280, 720
    
    
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



async def get_msg(userbot, sender, edit_id, msg_link, i):
    edit = ""
    chat = ""
    round_message = False
    if "?single" in msg_link:
        msg_link = msg_link.split("?single")[0]
    msg_id = int(msg_link.split("/")[-1]) + int(i)

    
    if 't.me/c/' in msg_link or 't.me/b/' in msg_link or 't.me/' in msg_link:
        if 't.me/b/' in msg_link:
            chat = str(msg_link.split("/")[-2])
        elif 't.me/c/' in msg_link:
            chat = int('-100' + str(msg_link.split("/")[-2]))
        else:
            chat_name = msg_link.split('/')[-2]
            try:
                gp = await app.get_chat(f"@{chat_name}")
                chat = gp.id
            except Exception as e:
                print(e)
                return
        
        file = ""
        try:
            msg = await userbot.get_messages(chat, msg_id)
            if msg.media:
                if msg.media == MessageMediaType.WEB_PAGE:
                    edit = await app.edit_message_text(sender, edit_id, "Cloning.")
                    await app.send_message(sender, msg.text.markdown)
                    await edit.delete()
                    return
            if not msg.media:
                if msg.text:
                    edit = await app.edit_message_text(sender, edit_id, "Cloning.")
                    await app.send_message(sender, msg.text.markdown)
                    await edit.delete()
                    return
            
            edit = await app.edit_message_text(sender, edit_id, "Trying to Download.")
            file = await userbot.download_media(
                msg,
                progress=progress_bar,
                progress_args=("**DOWNLOADING:**\n",edit,time.time()))
            
            
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
                duration ,width, height = get_duration(file)      

                if duration <= 300:
                    await app.send_video(chat_id=sender, video=file, caption=caption, height=height, width=width, duration=duration, thumb=None, progress=progress_bar, progress_args=('**UPLOADING:**\n', edit, time.time())) 
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
                        await app.send_video(
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
                    except:
                        await app.edit_message_text(sender, edit_id, "The bot is not an admin in the specified chat.") 
                else:
                    await app.send_video(
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

                if not th.get("thumb") and thumb_path and os.path.exists(thumb_path):
                    os.remove(thumb_path)
                else:
                    print("Thumbnail file not found or failed to generate.")

                os.remove(file)
                    
            elif msg.media == MessageMediaType.PHOTO:
                await edit.edit("Uploading photo.")
                await app.send_photo(chat_id=sender, photo=file, caption=caption)
            else:
                th = await db.get_data(sender)
                if th and th.get("thumb"):
                    thumb_url = th.get("thumb")
                    thumb_path = await download_thumbnail(thumb_url)
                else:
                    try:
                        subprocess.run(f'ffmpeg -i "{file}" -ss 00:01:00 -vframes 1 "{sender}.jpg"', shell=True)
                        thumb_path = f"{sender}.jpg"
                        await message.reply_photo(thumb_path)
                    except:
                        print("failed to genrate thumb")
                        thumb_path = None

                if c.get("chat_id"):
                    channel_id = c.get("chat_id")
                    try:
                        await app.send_document(
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
                    except:
                        await app.edit_message_text(sender, edit_id, "The bot is not an admin in the specified chat.") 
                else:
                    await app.send_document(
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
        edit = await app.edit_message_text(sender, edit_id, "Cloning.")
        try:            
            await userbot.copy_message(sender, chat, msg_id)
        except Exception as e:
            await app.edit_message_text(sender, edit_id, f'Failed to save: `{msg_link}`\n\nError: {str(e)}')

