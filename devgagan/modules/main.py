#devgagn

import time
import asyncio
from pyrogram import filters, Client
from devgagan import app
from config import API_ID, API_HASH
from devgagan.core.get_func import get_msg
from devgagan.core.func import *
from devgagan.core.mongo import db
from pyrogram.errors import FloodWait


async def generate_random_name(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


users_loop = {}

@app.on_message(filters.regex(r'https?://[^\s]+'))
async def single_link(_, message):
    user_id = message.chat.id
    
    # Check if the user is already in the loop
    if users_loop.get(user_id, False):
        await message.reply(
            "You already have an ongoing process. Please wait for it to finish or cancel it with /cancel."
        )
        return    
        
    lol = await chk_user(message, user_id)
    if lol == 1:
        return
    

    # Add the user to the loop
    users_loop[user_id] = True
    link = get_link(message.text) 
    userbot = None
    try:
        join = await subscribe(_, message)
        if join == 1:
            users_loop[user_id] = False
            return
     
        msg = await message.reply("Processing...")
        data = await db.get_data(user_id)
        
        if data and data.get("session"):
            session = data.get("session")
            try:
                device = 'Vivo Y20'
                session_name = await generate_random_name()
                userbot = Client(session_name, api_id=API_ID, api_hash=API_HASH, device_model=device, session_string=session)
                await userbot.start()                
            except:
                users_loop[user_id] = False
                return await msg.edit_text("Login expired /login again...")
        else:
            users_loop[user_id] = False
            await msg.edit_text("Login in bot first ...")
            return

        try:
            if 't.me/+' in link:
                q = await userbot_join(userbot, link)
                await msg.edit_text(q)
            elif 't.me/' in link:
                await get_msg(userbot, user_id, msg.id, link, 0, message)
            else:
                await msg.edit_text("Invalid link format.")
        except Exception as e:
            await msg.edit_text(f"Link: `{link}`\n\n**Error:** {str(e)}")
            
    except FloodWait as fw:
        await msg.edit_text(f'Try again after {fw.x} seconds due to floodwait from telegram.')
        
    except Exception as e:
        await msg.edit_text(f"Link: `{link}`\n\n**Error:** {str(e)}")
    finally:
        if userbot and userbot.is_connected:  # Ensure userbot was initialized and started
            await userbot.stop()
        users_loop[user_id] = False  # Remove user from the loop after processing


@app.on_message(filters.command("batch"))
async def batch_link(_, message):
    user_id = message.chat.id
    
    if users_loop.get(user_id, False): # fixed already started batch process message
        await app.send_message(message.chat.id, "You already have a batch process running. Please wait for it to complete before starting a new one.")
        return
        
    lol = await chk_user(message, user_id)
    if lol == 1:
        max_batch_size = 0 # increase this if you want to give free access
    else:
        max_batch_size = float('inf')
        
    start = await app.ask(message.chat.id, text="Please send the start link.")
    start_id = start.text
    s = start_id.split("/")[-1]
    cs = int(s)
    
    last = await app.ask(message.chat.id, text="Please send the end link.")
    last_id = last.text
    l = last_id.split("/")[-1]
    cl = int(l)

    if user_id != OWNER_ID and (cl - cs) > max_batch_size:
        await app.send_message(message.chat.id, "Only 3 messages allowed in batch size. Purchase premium to fly @kingofpatal 💸")
        return
    
    try:     
        data = await db.get_data(user_id)
        
        if data and data.get("session"):
            session = data.get("session")
            try:
                device = 'Vivo Y20'
                session_name = await generate_random_name()
                userbot = Client(session_name, api_id=API_ID, api_hash=API_HASH, device_model=device, session_string=session)
                await userbot.start()                
            except:
                return await app.send_message(message.chat.id, "Your login expired ... /login again")
        else:
            await app.send_message(message.chat.id, "Login in bot first ...")

        try:
            users_loop[user_id] = True # making this true to check later gagan
            
            for i in range(int(s), int(l)):
                if user_id in users_loop and users_loop[user_id]:
                    msg = await app.send_message(message.chat.id, "Processing!")
                    try:
                        x = start_id.split('/')
                        y = x[:-1]
                        result = '/'.join(y)
                        url = f"{result}/{i}"
                        link = get_link(url)
                        await get_msg(userbot, user_id, msg.id, link, 0, message)
                        sleep_msg = await app.send_message(message.chat.id, "Sleeping for 10 seconds to avoid flood...")
                        await asyncio.sleep(8)
                        await sleep_msg.delete()
                        await asyncio.sleep(2)                                                
                    except Exception as e:
                        print(f"Error processing link {url}: {e}")
                        continue
                else:
                    break
            await app.send_message(message.chat.id, "Batch completed successfully! 🎉")                    
        except Exception as e:
            await app.send_message(message.chat.id, f"Error: {str(e)}")
        finally:
            await userbot.stop()
            users_loop.pop(user_id, None)
                    
    except FloodWait as fw:
        await app.send_message(message.chat.id, f'Try again after {fw.x} seconds due to floodwait from Telegram.')
        users_loop.pop(user_id, None)
    except Exception as e:
        await app.send_message(message.chat.id, f"Error: {str(e)}")
        users_loop.pop(user_id, None)


@app.on_message(filters.command("cancel"))
async def stop_batch(_, message):
    user_id = message.chat.id

    # Check if there is an active batch process for the user
    if user_id in users_loop and users_loop[user_id]:
        users_loop[user_id] = False  # Set the loop status to False
        await app.send_message(
            message.chat.id, 
            "Batch processing has been stopped successfully. You can start a new batch now if you want."
        )
    elif user_id in users_loop and not users_loop[user_id]:
        await app.send_message(
            message.chat.id, 
            "The batch process was already stopped. No active batch to cancel."
        )
    else:
        await app.send_message(
            message.chat.id, 
            "No active batch processing is running to cancel."
        )
        
