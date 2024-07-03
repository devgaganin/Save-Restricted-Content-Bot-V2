import pymongo
import os
from devgagan import sexxx as app
import random
import string
from devgagan.core.mongo import db
from devgagan.core.func import subscribe, chk_user
from pyrogram import Client, filters
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
import asyncio
from config import API_ID as api_id, API_HASH as api_hash, LOG_GROUP 


user_steps = {}
user_data = {}


def generate_random_name(length=7):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))  # kuchh chutiye isko 12 names me hi defined kiye the maine isko random 7 characters autogenrator kar diya hu


async def process_step(client, message):
    user_id = message.chat.id
    step = user_steps.get(user_id, None)

    if step == "phone_number":
        user_data[user_id] = {"phone_number": message.text}
        user_steps[user_id] = "otp"
        omsg = await message.reply("Sending OTP...")
        temp_client = Client(generate_random_name(), api_id, api_hash)
        user_data[user_id]["client"] = temp_client
        await temp_client.connect()
        try:
            code = await temp_client.send_code(user_data[user_id]["phone_number"])
            user_data[user_id]["phone_code_hash"] = code.phone_code_hash
            await omsg.delete()
            await message.reply("OTP has been sent. Please enter the OTP in the format: '1 2 3 4 5'.")
        except ApiIdInvalid:
            await message.reply('❌ Invalid combination of API ID and API HASH. Please restart the session.')
            reset_user(user_id)
        except PhoneNumberInvalid:
            await message.reply('❌ Invalid phone number. Please restart the session.')
            reset_user(user_id)
    elif step == "otp":
        phone_code = message.text.replace(" ", "")
        temp_client = user_data[user_id]["client"]
        try:
            await temp_client.sign_in(user_data[user_id]["phone_number"], user_data[user_id]["phone_code_hash"], phone_code)
            session_string = await temp_client.export_session_string()
            session_data = {
                "user_id": user_id,
                "session_string": session_string
            }
            collection.update_one(
                {"user_id": user_id},
                {"$set": session_data},
                upsert=True
            )
            await db.set_session(user_id, string_session)
            await message.reply(f"✅ Login successful!")
            await temp_client.disconnect()
            reset_user(user_id)
        except PhoneCodeInvalid:
            await message.reply('❌ Invalid OTP. Please restart the session.')
            reset_user(user_id)
        except PhoneCodeExpired:
            await message.reply('❌ Expired OTP. Please restart the session.')
            reset_user(user_id)
        except SessionPasswordNeeded:
            user_steps[user_id] = "password"
            await message.reply('Your account has two-step verification enabled. Please enter your password.')
    elif step == "password":
        temp_client = user_data[user_id]["client"]
        try:
            password = message.text
            await temp_client.check_password(password=password)
            session_string = await temp_client.export_session_string()
            await db.set_session(user_id, string_session)
            await message.reply(f"✅ Login successful!")
            await temp_client.disconnect()
            reset_user(user_id)
        except PasswordHashInvalid:
            await message.reply('❌ Invalid password. Please restart the session.')
            reset_user(user_id)
    else:
        await message.reply('Please enter your phone number along with the country code. \n\nExample: +19876543210')
        user_steps[user_id] = "phone_number"

def reset_user(user_id):
    user_steps.pop(user_id, None)
    user_data.pop(user_id, None)

@app.on_message(filters.command("login"))
async def login_command(client, message):
    joined = await subscribe(client, message)
    if joined == 1:
        return        
    user_checked = await chk_user(message, message.from_user.id)
    if user_checked == 1:
        return
    await process_step(client, message)

@app.on_message(filters.text & filters.private)
async def handle_steps(client, message):
    user_id = message.chat.id
    if user_id in user_steps:
        await process_step(client, message)
