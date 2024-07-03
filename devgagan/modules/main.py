import asyncio
from pyrogram import filters, Client
from devgagan import app
from config import API_ID, API_HASH
from devgagan.core.get_func import get_msg
from devgagan.core.func import *
from devgagan.core.mongo import db
from pyrogram.errors import FloodWait
from devgagan.core.func import chk_user

# Dictionary to store user steps and states
user_steps = {}
users_in_batch = set()

@app.on_message(filters.regex(r'https?://[^\s]+'))
async def single_link(_, message):
    user_id = message.chat.id
    
    # Skip if user is in the batch process
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

@app.on_message(filters.command("batch"))
async def batch_link(_, message):
    user_id = message.chat.id    
    lol = await chk_user(message, user_id)
    if lol == 1:
        return    

    user_steps[user_id] = {'step': 'waiting_for_start_link'}
    users_in_batch.add(user_id)  # Add user to the batch process set

    await app.send_message(user_id, "Please send the start link.")

@app.on_message(filters.text & filters.private)
async def handle_user_responses(_, message):
    user_id = message.chat.id

    if user_id in user_steps:
        step = user_steps[user_id].get('step')

        if step == 'waiting_for_start_link':
            user_steps[user_id]['start_id'] = message.text
            s = user_steps[user_id]['start_id'].split("/")[-1]
            user_steps[user_id]['cs'] = int(s)

            user_steps[user_id]['step'] = 'waiting_for_end_link'
            await app.send_message(user_id, "Please send the end link.")

        elif step == 'waiting_for_end_link':
            user_steps[user_id]['last_id'] = message.text
            l = user_steps[user_id]['last_id'].split("/")[-1]
            user_steps[user_id]['cl'] = int(l)

            if user_steps[user_id]['cl'] - user_steps[user_id]['cs'] > 1000:
                await app.send_message(user_id, "Only 1000 messages allowed in batch size. Make sure your start and end message have a difference of less than 1000.")
                user_steps.pop(user_id)
                users_in_batch.remove(user_id)  # Remove user from the batch process set
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
                    users_in_batch.remove(user_id)  # Remove user from the batch process set
                    return
            else:
                await app.send_message(user_id, "Please generate a session first.")
                user_steps.pop(user_id)
                users_in_batch.remove(user_id)  # Remove user from the batch process set
                return

            try:
                users_loop[user_id] = True
                
                for i in range(user_steps[user_id]['cs'], user_steps[user_id]['cl']):
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
                            sleep_msg = app.send_message(user_id, "Sleeping for 10 seconds to avoid flood...")
                            await asyncio.sleep(8)
                            await sleep_msg.delete()
                            await asyncio.sleep(2)
                        except Exception as e:
                            print(f"Error processing link {url}: {e}")
                            continue
                    else:
                        break
                users_in_batch.remove(user_id)  # Remove user from the batch process set after completion
            except Exception as e:
                await app.send_message(user_id, f"Error: {str(e)}")
                users_in_batch.remove(user_id)  # Remove user from the batch process set in case of error
                        
        except FloodWait as fw:
            await app.send_message(user_id, f'Try again after {fw.x} seconds due to floodwait from Telegram.')
            users_in_batch.remove(user_id)  # Remove user from the batch process set in case of flood wait
        except Exception as e:
            await app.send_message(user_id, f"Error: {str(e)}")
            users_in_batch.remove(user_id)  # Remove user from the batch process set in case of error

@app.on_message(filters.command("cancel"))
async def stop_batch(_, message):
    user_id = message.chat.id
    if user_id in users_loop:
        users_loop[user_id] = False
        await app.send_message(user_id, "Batch processing stopped.")
        users_in_batch.remove(user_id)  # Remove user from the batch process set
    else:
        await app.send_message(user_id, "No active batch processing to stop.")
