#devggn

import time
import asyncio
from pyrogram import filters, Client
from devgagan import app as ggn
from config import API_ID, API_HASH
from devgagan.core.get_func import get_msg
from devgagan.core.func import *
from devgagan.core.mongo import db
from pyrogram.errors import FloodWait
from devgagan.core.func import chk_user
from devgagan.core import script
from devgagan.core.func import subscribe
from config import OWNER_ID
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


# ---------------------- pyromod is mother fucker, it gives peer_id invalid error bcz it use pyrogram unmodified version
#  that's why i implemented step method (noob hai apn) 

users_loop = {}
user_steps = {}  
user_data = {}  

@ggn.on_message(filters.command("batch"))
async def batch_link(_, message):
    user_id = message.chat.id
    if user_id in users_loop and users_loop[user_id]:
        await ggn.send_message(user_id, "A batch process is already ongoing. Please /cancel or wait for it to finish.")
        return

    lol = await chk_user(message, user_id)
    if lol == 1:
        return

    user_steps[user_id] = "start_link"
    await ggn.send_message(user_id, text="Please send the start link.")

@ggn.on_message(filters.command("cancel"))
async def stop_batch(_, message):
    user_id = message.chat.id
    if user_id in users_loop:
        users_loop[user_id] = False
        await ggn.send_message(user_id, "Batch processing stopped.")
        user_steps.pop(user_id, None)
        user_data.pop(user_id, None)
    else:
        await ggn.send_message(user_id, "No active batch processing to stop.")

@ggn.on_message(filters.text & filters.private)
async def handle_response(_, message):
    user_id = message.chat.id

    if user_id not in user_steps:
        return

    step = user_steps[user_id]

    if step == "start_link":
        start_id = message.text
        s = start_id.split("/")[-1]
        user_data[user_id] = {"start_id": start_id, "start_num": int(s)}
        user_steps[user_id] = "end_link"
        await ggn.send_message(user_id, text="Please send the end link.")
    
    elif step == "end_link":
        last_id = message.text
        l = last_id.split("/")[-1]
        user_data[user_id]["last_id"] = last_id
        user_data[user_id]["last_num"] = int(l)
        
        start_num = user_data[user_id]["start_num"]
        last_num = user_data[user_id]["last_num"]

        if last_num - start_num > 1000:
            await ggn.send_message(user_id, "Only 1000 messages allowed in batch size... Make sure your start and end message have difference less than 1000")
            user_steps.pop(user_id, None)
            user_data.pop(user_id, None)
            return

        user_steps[user_id] = "processing"
        await process_batch(user_id)

async def process_batch(user_id):
    try:
        data = await db.get_data(user_id)
        
        if data and data.get("session"):
            session = data.get("session")
            try:
                userbot = Client(":userbot:", api_id=API_ID, api_hash=API_HASH, session_string=session)
                await userbot.start()                
            except:
                await ggn.send_message(user_id, "Please generate a new session.")
                return
        else:
            await ggn.send_message(user_id, "Please generate a session first.")
            return

        users_loop[user_id] = True
        start_num = user_data[user_id]["start_num"]
        last_num = user_data[user_id]["last_num"]
        start_id = user_data[user_id]["start_id"]
        
        for i in range(start_num, last_num + 1):
            if user_id in users_loop and users_loop[user_id]:
                msg = await ggn.send_message(user_id, "Processing!")
                try:
                    x = start_id.split('/')
                    y = x[:-1]
                    result = '/'.join(y)
                    url = f"{result}/{i}"
                    link = get_link(url)
                    await asyncio.sleep(5)
                    await get_msg(userbot, user_id, msg.id, link, 0, message)
                    sleep_msg = await ggn.send_message(user_id, "Sleeping for 5 seconds to avoid flood...")
                    await asyncio.sleep(3)  # Adjust sleep time as needed
                    await sleep_msg.delete()
                    await asyncio.sleep(2)
                except Exception as e:
                    print(f"Error processing link {url}: {e}")
                    continue
            else:
                break
    except FloodWait as fw:
        await ggn.send_message(user_id, f'Try again after {fw.x} seconds due to floodwait from Telegram.')
    except Exception as e:
        await ggn.send_message(user_id, f"Error: {str(e)}")
    finally:
        user_steps.pop(user_id, None)
        user_data.pop(user_id, None)
        users_loop.pop(user_id, None)



# ------------------------------------------------------------------------------- #

# ------------------- Start-Buttons ------------------- #

buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Join Channel", url="https://t.me/devggn"),
            InlineKeyboardButton("Contact Me", url="https://t.me/ggnhere")
        ]
    ]
)

@ggn.on_message(filters.regex(r'https?://[^\s]+'))
async def single_link(_, message):
    user_id = message.chat.id
    lol = await chk_user(message, user_id)
    if lol == 1:
        return
    
    link = get_link(message.text) 
    
    try:
        join = await subscribe(_, message)
        if join == 1:
            return
     
        msg = await message.reply("Processing!")
        data = await db.get_data(user_id)
        
        if data and data.get("session"):
            session = data.get("session")
            try:
                userbot = Client(":userbot:", api_id=API_ID, api_hash=API_HASH, session_string=session)
                await userbot.start()                
            except:
                return await msg.edit_text("Please login in bot...")
        else:
            await msg.edit_text("Login in bot first ...")
            return

        try:
            if 't.me/+' in link:
                q = await userbot_join(userbot, link)
                await msg.edit_text(q)
                return
                                        
            if 't.me/' in link:
                await get_msg(userbot, user_id, msg.id, link, 0, message)
        except Exception as e:
            await msg.edit_text(f"Link: `{link}`\n\n**Error:** {str(e)}")
                    
    except FloodWait as fw:
        await msg.edit_text(f'Try again after {fw.x} seconds due to floodwait from telegram.')
    except Exception as e:
        await msg.edit_text(f"Link: `{link}`\n\n**Error:** {str(e)}")
