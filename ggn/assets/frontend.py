# devgaganin

import time
import os
import logging
import json
from .. import bot as gagan
from .. import Bot, defaultbot
from config import FORCESUB as fs
from telethon import events, Button, errors
from pyrogram.errors import FloodWait
from ggn.assets.pyroplug import get_msg, check, get_bulk_msg
from ggn.assets.functions import get_link, join, screenshot, force_sub
from ggn.assets.login import get_session
import logging
import asyncio
import pymongo
from telethon.tl.types import DocumentAttributeVideo
from pyrogram import Client 
from config import API_ID, API_HASH

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)


ft = f"To use this bot you've to join @{fs}."
message = "Send me the message link you want to start saving from, as a reply to this message."

process = []
timer = []
user = []

# List of commands that should bypass the link check
commands = ['/dl', '/pdl', '/adl']  # Add other commands as needed

@gagan.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def clone(event):
    logging.info(event)
    file_name = ''

    # Check if the message starts with a command
    if any(event.message.text.startswith(command) for command in commands):
        # Command detected, bypass link check and do nothing
        return

    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.text == message:
            return

    lit = event.text
    li = lit.split("\n")

    if len(li) > 10:
        await event.respond("Max 10 links allowed")
        return

    for li in li:
        try:
            link = get_link(li)
            if not link:
                return
        except TypeError:
            return

        s, r = await force_sub(event.client, fs, event.sender_id, ft)
        if s is True:
            await event.respond(r)
            return

        if f'{int(event.sender_id)}' in user:
            return await event.respond("Please don't spam links, wait until ongoing process is done.")
        user.append(f'{int(event.sender_id)}')

        edit = await event.respond("Processing!")

        if "|" in li:
            url = li
            url_parts = url.split("|")
            if len(url_parts) == 2:
                file_name = url_parts[1]

        if file_name is not None:
            file_name = file_name.strip()

        try:
            if 't.me/' not in link:
                await edit.edit("invalid link")
                ind = user.index(f'{int(event.sender_id)}')
                user.pop(int(ind))
                return

            if 't.me/+' in link:
                q = await join(defaultbot, link)
                await edit.edit(q)
                ind = user.index(f'{int(event.sender_id)}')
                user.pop(int(ind))
                return

            if 't.me/' in link:
                msg_id = 0
                try:
                    msg_id = int(link.split("/")[-1])
                except ValueError:
                    if '?single' in link:
                        link_ = link.split("?single")[0]
                        msg_id = int(link_.split("/")[-1])
                    else:
                        msg_id = -1
                m = msg_id
                user_id = event.sender_id
                session_data = get_session(user_id)
                if session_data:
                    try:
                        userbot = Client(":userbot:", api_id=API_ID, api_hash=API_HASH, session_string=session_data)
                        await userbot.start()
                    except Exception as e:
                        await edit.delete()
                        await event.respond("Login in bot to continue send /login")
                        ind = user.index(f'{int(event.sender_id)}')
                        user.pop(int(ind))
                        return
                else:
                  userbot = defaultbot
                  
                await get_msg(userbot, Bot, event.sender_id, edit.id, link, m, file_name)
              

        except FloodWait as fw:
            await gagan.send_message(event.sender_id, f'Try again after {fw.value} seconds due to floodwait from telegram.')
            await edit.delete()
        except Exception as e:
            logging.info(e)
            await gagan.send_message(event.sender_id, f"An error occurred during cloning of `{link}`\n\n**Error:** {str(e)}")
            await edit.delete()

        ind = user.index(f'{int(event.sender_id)}')
        user.pop(int(ind))
        time.sleep(1)


#### ----------------------- THE END ---------------------
