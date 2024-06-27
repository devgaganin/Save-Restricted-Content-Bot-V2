#devggn

import time
import asyncio
from pyrogram import filters, Client
from Restriction import app
from config import API_ID, API_HASH
from Restriction.core.get_func import get_msg
from Restriction.core.func import *
from Restriction.core.mongo import db
from pyrogram.errors import FloodWait
from Restriction.core.func import chk_user



@app.on_message(filters.regex(r'https?://[^\s]+'))
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


users_loop = {}

@app.on_message(filters.command("batch"))
async def batch_link(_, message):
    user_id = message.chat.id    
    lol = await chk_user(message, user_id)
    if lol == 1:
        return    
        
    start = await app.ask(message.chat.id, text="Please send the start link.")
    start_id = start.text
    s = start_id.split("/")[-1]
    cs = int(s)
    
    last = await app.ask(message.chat.id, text="Please send the end link.")
    last_id = last.text
    l = last_id.split("/")[-1]
    cl = int(l)

    if cl - cs > 1000:
        await app.send_message(message.chat.id, "Only 1000 messages allowed in batch size... Make sure your start and end message have difference less than 1000")
        return
    
    try:     
        data = await db.get_data(user_id)
        
        if data and data.get("session"):
            session = data.get("session")
            try:
                userbot = Client(":userbot:", api_id=API_ID, api_hash=API_HASH, session_string=session)
                await userbot.start()                
            except:
                return await app.send_message(message.chat.id, "Please generate a new session.")
        else:
            await app.send_message(message.chat.id, "Please generate a session first.")

        try:
            users_loop[user_id] = True
            
            for i in range(int(s), int(l)):
                if user_id in users_loop and users_loop[user_id]:
                    msg = await app.send_message(message.chat.id, "Processing!")
                    try:
                        x = start_id.split('/')
                        y = x[:-1]
                        result = '/'.join(y)
                        url = f"{result}/{i}"
                        link = get_link(url)
                        await asyncio.sleep(5)
                        await get_msg(userbot, user_id, msg.id, link, 0, message)
                        sleep_msg = app.send_message(message.chat.id, "Sleeping for 10 seconds to avoid flood...")
                        await asyncio.sleep(8) # isko kam jyada kr lena bc
                        await sleep_msg.delete()
                        await sleep(2)
                    except Exception as e:
                        print(f"Error processing link {url}: {e}")
                        continue
                else:
                    break
        except Exception as e:
            await app.send_message(message.chat.id, f"Error: {str(e)}")
                    
    except FloodWait as fw:
        await app.send_message(message.chat.id, f'Try again after {fw.x} seconds due to floodwait from Telegram.')
    except Exception as e:
        await app.send_message(message.chat.id, f"Error: {str(e)}")


@app.on_message(filters.command("cancel"))
async def stop_batch(_, message):
    user_id = message.chat.id
    if user_id in users_loop:
        users_loop[user_id] = False
        await app.send_message(message.chat.id, "Batch processing stopped.")
    else:
        await app.send_message(message.chat.id, "No active batch processing to stop.")

