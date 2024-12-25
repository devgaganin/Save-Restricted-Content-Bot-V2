import time
import random
import string
import asyncio
from pyrogram import filters, Client
from devgagan import app
from config import API_ID, API_HASH, FREEMIUM_LIMIT, PREMIUM_LIMIT, OWNER_ID
from devgagan.core.get_func import get_msg
from devgagan.core.func import *
from devgagan.core.mongo import db
from devgagan.modules.shrink import is_user_verified
from pyrogram.errors import FloodWait
from datetime import datetime, timedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
async def generate_random_name(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))
users_loop = {}
interval_set = {}
batch_mode = {}
async def check_interval(user_id, freecheck):
    if freecheck != 1 or await is_user_verified(user_id):
        return True, None
    now = datetime.now()
    if user_id in interval_set:
        cooldown_end = interval_set[user_id]
        if now < cooldown_end:
            remaining_time = (cooldown_end - now).seconds // 60
            return False, f"Please wait {remaining_time} minute(s) before sending another link. Alternatively, purchase premium for instant access.\n\n> Hey 👋 You can use /token to use the bot free for 3 hours without any time limit."
        else:
            del interval_set[user_id]
    return True, None
async def set_interval(user_id, interval_minutes=5):
    now = datetime.now()
    interval_set[user_id] = now + timedelta(minutes=interval_minutes)
@app.on_message(filters.regex(r'https?://(?:www\.)?t\.me/[^\s]+'))
async def single_link(_, message):
    user_id = message.chat.id
    if user_id in batch_mode:
        return
    if users_loop.get(user_id, False):
        await message.reply(
            "You already have an ongoing process. Please wait for it to finish or cancel it with /cancel."
        )
        return    
    freecheck = await chk_user(message, user_id)
    if freecheck == 1 and FREEMIUM_LIMIT == 0 and user_id not in OWNER_ID:
        await message.reply("Freemium service is currently not available. Upgrade to premium for access.")
        return
    can_proceed, response_message = await check_interval(user_id, freecheck)
    if not can_proceed:
        await message.reply(response_message)
        return
    users_loop[user_id] = True
    link = get_link(message.text) 
    userbot = None
    try:
        join = await subscribe(_, message)
        if join == 1:
            users_loop[user_id] = False
            return
        msg = await message.reply("Processing...")
        if 't.me/' in link and 't.me/+' not in link and 't.me/c/' not in link and 't.me/b/' not in link:
            await get_msg(None, user_id, msg.id, link, 0, message)
            await set_interval(user_id, interval_minutes=5)
            return
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
            elif 't.me/c/' in link:
                await get_msg(userbot, user_id, msg.id, link, 0, message)
                await set_interval(user_id, interval_minutes=5)
            else:
                await msg.edit_text("Invalid link format.")
        except Exception as e:
            await msg.edit_text(f"Link: `{link}`\n\n**Error:** {str(e)}")
    except FloodWait as fw:
        await msg.edit_text(f'Try again after {fw.x} seconds due to floodwait from telegram.')
    except Exception as e:
        await msg.edit_text(f"Link: `{link}`\n\n**Error:** {str(e)}")
    finally:
        if userbot and userbot.is_connected:
            await userbot.stop()
        users_loop[user_id] = False
@app.on_message(filters.command("batch"))
async def batch_link(_, message):
    user_id = message.chat.id
    if users_loop.get(user_id, False):
        await app.send_message(
            message.chat.id,
            "You already have a batch process running. Please wait for it to complete before starting a new one."
        )
        return
    freecheck = await chk_user(message, user_id)
    if freecheck == 1 and FREEMIUM_LIMIT == 0 and user_id not in OWNER_ID:
        await message.reply("Freemium service is currently not available. Upgrade to premium for access.")
        return    
    toker = await is_user_verified(user_id)
    if toker:
        max_batch_size = (FREEMIUM_LIMIT + 20)
        freecheck = 0
    else:
        freecheck = await chk_user(message, user_id)
        if freecheck == 1:
            max_batch_size = FREEMIUM_LIMIT
        else:
            max_batch_size = PREMIUM_LIMIT
    
    while True:
        start = await app.ask(message.chat.id, text="Please send the start link.")
        start_id = start.text.strip()
        s = start_id.split("/")[-1]
        try:
            cs = int(s)
            break
        except ValueError:
            await app.send_message(message.chat.id, "Invalid link. Please send again ...")
    while True:
        num_messages = await app.ask(message.chat.id, text="How many messages do you want to process?")
        try:
            cl = int(num_messages.text.strip())
            if cl <= 0 or cl > max_batch_size:
                raise ValueError(f"Number of messages must be between 1 and {max_batch_size}.")
            break
        except ValueError as e:
            await app.send_message(message.chat.id, f"Invalid number: {e}. Please enter a valid number again ...")
    can_proceed, response_message = await check_interval(user_id, freecheck)
    if not can_proceed:
        await message.reply(response_message)
        return
    join_button = InlineKeyboardButton("Join Channel", url="https://t.me/team_spy_pro")
    keyboard = InlineKeyboardMarkup([[join_button]])
    pin_msg = await app.send_message(
        user_id,
        "Batch process started ⚡\n__Processing: 0/{cl}__\n\n**__Powered by Team SPY__**",
        reply_markup=keyboard
    )
    try:
        await pin_msg.pin()
    except Exception as e:
        await pin_msg.pin(both_sides=True)
    users_loop[user_id] = True
    try:
        for i in range(cs, cs + cl):
            if user_id in users_loop and users_loop[user_id]:
                try:
                    x = start_id.split('/')
                    y = x[:-1]
                    result = '/'.join(y)
                    url = f"{result}/{i}"
                    link = get_link(url)
                    if 't.me/' in link and 't.me/b/' not in link and 't.me/c' not in link:
                        msg = await app.send_message(message.chat.id, f"Processing link {url}...")
                        await get_msg(None, user_id, msg.id, link, 0, message)
                        await pin_msg.edit_text(
                        f"Batch process started ⚡\n__Processing: {i - cs + 1}/{cl}__\n\n**__Powered by Team SPY__**",
                        reply_markup=keyboard
                        )
                        await asyncio.sleep(5)
                except Exception as e:
                    print(f"Error processing link {url}: {e}")
                    continue
        if not any(prefix in start_id for prefix in ['t.me/c/', 't.me/b/']):
            await set_interval(user_id, interval_minutes=20)
            await app.send_message(message.chat.id, "Batch completed successfully! 🎉")
            await pin_msg.edit_text(
                        f"Batch process completed for {cl} messages enjoy 🌝\n\n**__Powered by Team SPY__**",
                        reply_markup=keyboard
            )
            return
        data = await db.get_data(user_id)
        if data and data.get("session"):
            session = data.get("session")
            device = 'Vivo Y20'
            session_name = await generate_random_name()
            userbot = Client(
                session_name,
                api_id=API_ID,
                api_hash=API_HASH,
                device_model=device,
                session_string=session
            )
            await userbot.start()
        else:
            await app.send_message(message.chat.id, "Login in bot first ...")
            return
        try:
            for i in range(cs, cs + cl):
                if user_id in users_loop and users_loop[user_id]:
                    try:
                        x = start_id.split('/')
                        y = x[:-1]
                        result = '/'.join(y)
                        url = f"{result}/{i}"
                        link = get_link(url)
                        if 't.me/b/' in link or 't.me/c/' in link:
                            msg = await app.send_message(message.chat.id, f"Processing link {url}...")
                            await get_msg(userbot, user_id, msg.id, link, 0, message)
                            sleep_msg = await app.send_message(
                                message.chat.id,
                                "Sleeping for 5 seconds to avoid flood..."
                            )
                            await asyncio.sleep(2)
                            await pin_msg.edit_text(
                            f"Batch process started ⚡\n__Processing: {i - cs + 1}/{cl}__\n\n**__Powered by Team SPY__**",
                            reply_markup=keyboard
                            )
                            await asyncio.sleep(10)
                            await sleep_msg.delete()
                    except Exception as e:
                        print(f"Error processing link {url}: {e}")
                        continue
        finally:
            if userbot.is_connected:
                await userbot.stop()
        await app.send_message(message.chat.id, "Batch completed successfully! 🎉")
        await set_interval(user_id, interval_minutes=20)
        await pin_msg.edit_text(
                        f"Batch completed for {cl} messages ⚡\n\n**__Powered by Team SPY__**",
                        reply_markup=keyboard
        )
    except FloodWait as fw:
        await app.send_message(
            message.chat.id,
            f"Try again after {fw.x} seconds due to floodwait from Telegram."
        )
    except Exception as e:
        await app.send_message(message.chat.id, f"Error: {str(e)}")
    finally:
        users_loop.pop(user_id, None)
@app.on_message(filters.command("cancel"))
async def stop_batch(_, message):
    user_id = message.chat.id
    if user_id in users_loop and users_loop[user_id]:
        users_loop[user_id] = False
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
