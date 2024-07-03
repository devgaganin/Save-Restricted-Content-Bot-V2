import asyncio
from pyrogram import filters, Client
from Restriction import app
from config import API_ID, API_HASH
from Restriction.core.get_func import get_msg
from Restriction.core.func import *
from Restriction.core.mongo import db
from pyrogram.errors import FloodWait
from Restriction.core.func import chk_user


users_in_batch = set()
@app.on_message(filters.regex(r'https?://[^\s]+'))
async def single_link(_, message):
    user_id = message.chat.id
    if user_id in users_in_batch:
      return
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
user_steps = {}
@app.on_message(filters.command("batch"))
async def batch_link(_, message):
    user_id = message.chat.id    
    lol = await chk_user(message, user_id)
    if lol == 1:
        return    
    
    user_steps[user_id] = {}\
    users_in_batch.add(user_id)  # Add user to the batch process set

    # Send the first prompt
    await app.send_message(user_id, "Please send the start link.")
    user_steps[user_id]['step'] = 'waiting_for_start_link'
    

@app.on_message(filters.text & filters.private)
async def collect_batch_links(_, message):
    user_id = message.chat.id
    
    if user_id in user_steps:
        step = user_steps[user_id].get('step')
        
        if step == 'waiting_for_start_link':
            user_steps[user_id]['start_id'] = message.text
            s = user_steps[user_id]['start_id'].split("/")[-1]
            cs = int(s)

            # Send the second prompt
            await app.send_message(user_id, "Please send the end link.")
            user_steps[user_id]['step'] = 'waiting_for_end_link'
        
        elif step == 'waiting_for_end_link':
            user_steps[user_id]['last_id'] = message.text
            l = user_steps[user_id]['last_id'].split("/")[-1]
            cl = int(l)
            
            if cl - cs > 1000:
                await app.send_message(user_id, "Only 1000 messages allowed in batch size. Make sure your start and end message have a difference of less than 1000.")
                user_steps.pop(user_id)
                return
            
            data = await db.get_data(user_id)
            
            if data and data.get("session"):
                session = data.get("session")
                try:
                    userbot = Client(":userbot:", api_id=API_ID, api_hash=API_HASH, session_string=session)
                    await userbot.start()                
                except:
                    await app.send_message(user_id, "Please generate a new session.")
                    user_steps.pop(user_id)
                    return
            else:
                await app.send_message(user_id, "Please generate a session first.")
                user_steps.pop(user_id)
                return

            users_loop[user_id] = True

            for i in range(cs, cl):
                if user_id in users_loop and users_loop[user_id]:
                    msg = await app.send_message(user_id, "Processing!")
                    try:
                        x = user_steps[user_id]['start_id'].split('/')
                        y = x[:-1]
                        result = '/'.join(y)
                        url = f"{result}/{i}"
                        link = get_link(url)
                        await asyncio.sleep(5)
                        await get_msg(userbot, user_id, msg.id, link, 0, message)
                        sleep_msg = await app.send_message(user_id, "Sleeping for 10 seconds to avoid flood...")
                        await asyncio.sleep(8)
                        await sleep_msg.delete()
                        await asyncio.sleep(2)
                    except Exception as e:
                        print(f"Error processing link {url}: {e}")
                        continue
                else:
                    break
            users_in_batch.remove(user_id)            
            user_steps.pop(user_id)


@app.on_message(filters.command("cancel"))
async def stop_batch(_, message):
    user_id = message.chat.id
    if user_id in users_loop:
        users_loop[user_id] = False
        await app.send_message(user_id, "Batch processing stopped.")
    else:
        await app.send_message(user_id, "No active batch processing to stop.")
