# ---------------------------------------------------
# File Name: main.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

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

async def process_and_upload_link(userbot, user_id, msg_id, link, retry_count, message):
    try:
        await get_msg(userbot, user_id, msg_id, link, retry_count, message)
        await asyncio.sleep(3.5)
    finally:
        pass



# Function to check if the user can proceed
async def check_interval(user_id, freecheck):
    if freecheck != 1 or await is_user_verified(user_id):  # Premium or owner users can always proceed
        return True, None

    now = datetime.now()

    # Check if the user is on cooldown
    if user_id in interval_set:
        cooldown_end = interval_set[user_id]
        if now < cooldown_end:
            remaining_time = (cooldown_end - now).seconds // 60
            return False, f"Please wait {remaining_time} minute(s) before sending another link. Alternatively, purchase premium for instant access.\n\n> Hey 👋 You can use /token to use the bot free for 3 hours without any time limit."
        else:
            del interval_set[user_id]  # Cooldown expired, remove user from interval set

    return True, None

async def set_interval(user_id, interval_minutes=5):
    now = datetime.now()
    # Set the cooldown interval for the user
    interval_set[user_id] = now + timedelta(minutes=interval_minutes)
    

@app.on_message(filters.regex(r'https?://(?:www\.)?t\.me/[^\s]+') & filters.private)
async def single_link(_, message):
    join = await subscribe(_, message)
    if join == 1:
        return
     
    user_id = message.chat.id
    if user_id in batch_mode:
        return
    
    # Check if the user is already in the loop
    if users_loop.get(user_id, False):
        await message.reply(
            "You already have an ongoing process. Please wait for it to finish or cancel it with /cancel."
        )
        return    
        
    freecheck = await chk_user(message, user_id)
    if freecheck == 1 and FREEMIUM_LIMIT == 0 and user_id not in OWNER_ID:
        await message.reply("Freemium service is currently not available. Upgrade to premium for access.")
        return
    
    # Call the set_interval function to handle the cooldown
    can_proceed, response_message = await check_interval(user_id, freecheck)
    if not can_proceed:
        await message.reply(response_message)
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
        
        if 't.me/' in link and 't.me/+' not in link and 't.me/c/' not in link and 't.me/b/' not in link:
            data = await db.get_data(user_id)
            if data and data.get("session"):
                session = data.get("session")
                try:
                    device = 'Vivo Y20'
                    userbot = Client(
                        ":userbot:",
                        api_id=API_ID,
                        api_hash=API_HASH,
                        device_model=device,
                        session_string=session
                    )
                    await userbot.start()
                except Exception as e:
                    userbot = None
            else:
                userbot = None
                
            await process_and_upload_link(userbot, user_id, msg.id, link, 0, message)
            await set_interval(user_id, interval_minutes=5)
            users_loop[user_id] = False
            return
            
        data = await db.get_data(user_id)
        
        if data and data.get("session"):
            session = data.get("session")
            try:
                device = 'Vivo Y20'
                userbot = Client(":userbot:", api_id=API_ID, api_hash=API_HASH, device_model=device, session_string=session)
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
            elif 't.me/c/' in link or 't.me/b/' in link:
                await process_and_upload_link(userbot, user_id, msg.id, link, 0, message)
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
        if userbot and userbot.is_connected:  # Ensure userbot was initialized and started
            await userbot.stop()
        users_loop[user_id] = False  # Remove user from the loop after processing

# New Update


@app.on_message(filters.command("batch") & filters.private)
async def batch_link(_, message):
    join = await subscribe(_, message)
    if join == 1:
        return
     
    user_id = message.chat.id
    # Check if a batch process is already running
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

    # Determine user's limits based on their subscription
    toker = await is_user_verified(user_id)
    if toker:
        max_batch_size = (FREEMIUM_LIMIT + 1)
        freecheck = 0  # Pass
    else:
        freecheck = await chk_user(message, user_id)
        if freecheck == 1:
            max_batch_size = FREEMIUM_LIMIT  # Limit for free users
        else:
            max_batch_size = PREMIUM_LIMIT

    # Loop for start link input
    attempts = 0
    while attempts < 3:
        start = await app.ask(message.chat.id, text="Please send the start link.")
        start_id = start.text.strip()
        s = start_id.split("/")[-1]  # Extract the last part of the link

        try:
            cs = int(s)  # Try to convert the extracted part to an integer
            break  # Exit loop if conversion is successful
        except ValueError:
            attempts += 1
            if attempts == 3:
                await app.send_message(message.chat.id, "You have exceeded the maximum number of attempts. Please try again later.")
                return
            await app.send_message(message.chat.id, "Invalid link. Please send again ...")

    # Loop for the number of messages input
    attempts = 0
    while attempts < 3:
        num_messages = await app.ask(message.chat.id, text="How many messages do you want to process?")
        try:
            cl = int(num_messages.text.strip())  # Try to convert input to an integer
            if cl <= 0 or cl > max_batch_size:
                raise ValueError(f"Number of messages must be between 1 and {max_batch_size}.")
            break  # Exit loop if conversion is successful
        except ValueError as e:
            attempts += 1
            if attempts == 3:
                await app.send_message(message.chat.id, "You have exceeded the maximum number of attempts. Please try again later.")
                return
            await app.send_message(message.chat.id, f"Invalid number: {e}. Please enter a valid number again ...")
    
    # Final validation before proceeding
    can_proceed, response_message = await check_interval(user_id, freecheck)
    if not can_proceed:
        await message.reply(response_message)
        return
        
 # Create an inline button for the channel link
    join_button = InlineKeyboardButton("Join Channel", url="https://t.me/team_spy_pro")
    keyboard = InlineKeyboardMarkup([[join_button]])

    # Send and Pin message to indicate the batch process has started
    pin_msg = await app.send_message(
        user_id,
        "Batch process started ⚡\n__Processing: 0/{cl}__\n\n**__Powered by Team SPY__**",
        reply_markup=keyboard
    )
    try:
        await pin_msg.pin()
    except Exception as e:
        await pin_msg.pin(both_sides=True)
    # Start processing links
    users_loop[user_id] = True
    try:
        # FIRST ITERATION: Process t.me/ links without userbot
        for i in range(cs, cs + cl):
            if user_id in users_loop and users_loop[user_id]:
                try:
                    # Construct the link
                    x = start_id.split('/')
                    y = x[:-1]
                    result = '/'.join(y)
                    url = f"{result}/{i}"
                    link = get_link(url)
                    
                    # Directly process links like t.me/ (no userbot needed)
                    if 't.me/' in link and 't.me/b/' not in link and 't.me/c' not in link:
                        userbot = None
                        data = await db.get_data(user_id)
                        if data and data.get("session"):
                            session = data.get("session")
                            try:
                                device = 'Vivo Y20'
                                userbot = Client(
                                    ":userbot:",
                                    api_id=API_ID,
                                    api_hash=API_HASH,
                                    device_model=device,
                                    session_string=session
                                )
                                await userbot.start()
                            except Exception as e:
                                userbot = None
                        else:
                            userbot = None
                        msg = await app.send_message(message.chat.id, f"Processing...")
                        await process_and_upload_link(userbot, user_id, msg.id, link, 0, message)
                        await pin_msg.edit_text(
                        f"Batch process started ⚡\n__Processing: {i - cs + 1}/{cl}__\n\n**__Powered by Team SPY__**",
                        reply_markup=keyboard
                        )
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

        # SECOND ITERATION: Process t.me/+ or t.me/c/ links with userbot
        data = await db.get_data(user_id)
        if data and data.get("session"):
            session = data.get("session")
            device = 'Vivo Y20'
            userbot = Client(
                ":userbot:",
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
                        # Construct the link
                        x = start_id.split('/')
                        y = x[:-1]
                        result = '/'.join(y)
                        url = f"{result}/{i}"
                        link = get_link(url)
                        # Process links requiring userbot
                        if 't.me/b/' in link or 't.me/c/' in link:
                            msg = await app.send_message(message.chat.id, f"Processing...")
                            await process_and_upload_link(userbot, user_id, msg.id, link, 0, message)
                            await pin_msg.edit_text(
                            f"Batch process started ⚡\n__Processing: {i - cs + 1}/{cl}__\n\n**__Powered by Team SPY__**",
                            reply_markup=keyboard
                            )
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
