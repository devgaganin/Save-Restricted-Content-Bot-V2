import logging
import time
import os
import asyncio
import json
import pymongo
import shutil
import zipfile
from .. import bot as gagan
from .. import userbot, Bot
from ggn.assets.pyroplug import check, get_bulk_msg
from ggn.assets.functions import get_link, screenshot
from telethon.tl.types import DocumentAttributeVideo
from telethon import events, Button, errors
from pyrogram import Client 
from pyrogram.errors import FloodWait
from config import OWNER_ID, MONGODB_CONNECTION_STRING


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)



def save_batch_data(batch_data):
    with open("batch_data.json", "w") as f:
        json.dump(batch_data, f)

def load_batch_data():
    if os.path.exists("batch_data.json"):
        with open("batch_data.json", "r") as f:
            return json.load(f)
    else:
        return {}

batch_data = load_batch_data()

def save_ids_data(ids_data):
    with open("ids_data.json", "w") as f:
        json.dump(ids_data, f)

def load_ids_data():
    if os.path.exists("ids_data.json"):
        with open("ids_data.json", "r") as f:
            return json.load(f)
    else:
        return {}

ids_data = load_ids_data()

@gagan.on(events.NewMessage(incoming=True, pattern='/batch'))
async def _batch(event):
    user_id = event.sender_id
   #  if user_id not in AUTHORIZED_USERS:
       # return await event.respond("This command is available to Paid Plan users! Send /plan to know more.")

    if user_id in batch_data:
        return await event.reply("You've already started one batch, wait for it to complete!")

    async with gagan.conversation(event.chat_id) as conv: 
        try:
            await conv.send_message(f"Send me the message link you want to start saving from, as a reply to this message.", buttons=Button.force_reply())
            link = await conv.get_reply()
            try:
                _link = get_link(link.text)
            except Exception:
                await conv.send_message("No link found...")
                return
            await conv.send_message(f"Send me the number of files/range you want to save from the given message, as a reply to this message.", buttons=Button.force_reply())
            _range = await conv.get_reply()
            try:
                value = int(_range.text)
                if value > 1000:
                    return await conv.send_message("You can only get up to 1000 files in a single batch.\n\nPurchase premium to go beyong limit send /plan to know more...")
            except ValueError:
                return await conv.send_message("Range must be an integer!")

            ids_data[str(user_id)] = list(range(value))
            save_ids_data(ids_data)

            s, r = await check(userbot, Bot, _link, event)
            if s != True:
                await conv.send_message(r)
                return

            batch_data[str(user_id)] = True
            save_batch_data(batch_data)

            cd = await conv.send_message("**Batch process ongoing...**\n\nProcess completed: ", 
                                    buttons=[[Button.url("Join Channel", url="http://t.me/devggn")]])
            co = await run_batch(userbot, Bot, user_id, cd, _link) 
            try: 
                if co == -2:
                    await Bot.send_message(user_id, "Batch successfully completed!")
                    await cd.edit(f"**Batch process ongoing.**\n\nProcess completed: {value} \n\n Batch successfully completed! ")
            except:
                await Bot.send_message(user_id, "ERROR!\n\n maybe last msg didn't exist yet")
            finally:
                conv.cancel()
                del batch_data[str(user_id)]
                save_batch_data(batch_data)
                del ids_data[str(user_id)]
                save_ids_data(ids_data)
        except Exception as e:
            logger.info(e)
            await conv.send_message("Processed")

@gagan.on(events.NewMessage(incoming=True, pattern='/cancel'))
async def cancel_command(event):
    user_id = event.sender_id
    if str(user_id) in ids_data:
        del ids_data[str(user_id)]
        save_ids_data(ids_data)
        await event.respond("Operation canceled.")
    else:
        await event.respond("There is no operation to cancel.")


async def run_batch(userbot, client, sender, countdown, link):
    for i in range(len(ids_data[str(sender)])):
        timer = 10  # Increased default timer value

        if i < 250:
            timer = 15
        elif 250 <= i < 1000:
            timer = 18
        elif 1000 <= i < 10000:
            timer = 22
        elif 10000 <= i < 50000:
            timer = 25
        elif 50000 <= i < 100000:
            timer = 30
        elif 100000 <= i < 200000:
            timer = 35
        elif i >= 200000:
            timer = 30  # Increased timer value for larger counts

        # Adjust the timer for links other than channel links
        if 't.me/c/' not in link:
            timer = 10 if i < 500 else 30  # Increased timer values for non-channel links

        try: 
            count_down = f"**Batch process ongoing.**\n\nProcess completed: {i+1}"
            integer = int(link.split("/")[-1]) + int(ids_data[str(sender)][i])
            await get_bulk_msg(userbot, client, sender, link, integer)
            protection = await client.send_message(sender, f"Sleeping for `{timer}` seconds to avoid Floodwaits and Protect account!")
            await countdown.edit(count_down, 
                                 buttons=[[Button.url("Join Channel", url="https://t.me/devggn")]])
            await asyncio.sleep(timer)
            await protection.delete()
        except IndexError as ie:
            await client.send_message(sender, f" {i}  {ie}  \n\nBatch ended completed!")
            await countdown.delete()
            break
        except FloodWait as fw:
            if int(fw.value) > 300:
                await client.send_message(sender, f'You have floodwaits of {fw.value} seconds, cancelling batch') 
                ids_data.pop(str(sender))
                break
            else:
                fw_alert = await client.send_message(sender, f'Sleeping for {fw.value + 15} second(s) due to Telegram floodwait.')
                ors = fw.value + 5
                await asyncio.sleep(ors)
                await fw_alert.delete()
                try:
                    await get_bulk_msg(userbot, client, sender, link, integer)
                except Exception as e:
                    logger.info(e)
                    if countdown.text != count_down:
                        await countdown.edit(count_down, buttons=[[Button.url("Join Channel", url="http://t.me/devggn")]])
        except Exception as e:
            #logger.info(e)
            #await client.send_message(sender, f"An error occurred during cloning, batch will continue.\n\n**Error:** {str(e)}")
            if countdown.text != count_down:
                await countdown.edit(count_down, buttons=[[Button.url("Join Channel", url="https://t.me/devggn")]])
        n = i + 1
        if n == len(ids_data[str(sender)]):
            return -2
        


# ------------------------------- USERBOT HOSTING ------------------------

async def run_main_py(user_id, session_string):
    folder_name = f"{user_id}pro"
    file_path = os.path.join(folder_name, "user.py")

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Write the Python code into ggn.py
    with open(file_path, "w") as file:
        file.write(f"""
from pyrogram import Client, filters

# Your API ID, API HASH, and String Session
API_ID = 23536615
API_HASH = "0731650e848c3791823e19eee62b891c"
STRING_SESSION = "{session_string}"
# Create a Pyrogram Client
app = Client(
    name="gagan",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

# Define a handler for the /start command
@app.on_message(filters.command("start"))
async def start(_, message):
    # Reply to the user with a greeting
    await message.reply_text('Pro!!!!!!')


@app.on_message(filters.command("nice") & filters.reply)
async def save_file(_, message):
    # Check if the replied message has any media
    await message.delete()
    if message.reply_to_message and message.reply_to_message.media:
        # Download the media
        file_path = await app.download_media(message.reply_to_message)

        # Send the downloaded media to yourself based on its type
        if message.reply_to_message.photo:
            await app.send_photo('me', file_path)
        elif message.reply_to_message.video:
            await app.send_video('me', file_path)
        elif message.reply_to_message.document:
            await app.send_document('me', file_path)
        else:
            await app.send_message('me', "Unsupported file type.")

        # Delete the downloaded file
        os.remove(file_path)
    else:
        # If the replied message does not contain any media, inform the user
        await message.reply_text("Please reply to a message containing media to save it.")

# Start the client
app.run()

""")

    # Run the ggn.py file in a subprocess
    process = await asyncio.create_subprocess_exec(
        "python", "user.py", f"--user_id={user_id}",
        cwd=folder_name,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    print(f"Process completed with stdout: {stdout} and stderr: {stderr}")

@gagan.on(events.NewMessage(incoming=True, pattern='/pro (.+)'))
async def start_pro(event):
    user_id = event.sender_id
    user_folder = f"{user_id}pro"

    # Check if the user already has a folder
    if os.path.exists(user_folder):
        await event.respond("You've already hosted a bot. Please remove the existing (send /unhost) one to host again.")
        return

    # Extract session string from the command
    session_string = event.pattern_match.group(1)

    # Start the hosting process
    await event.respond("You are pro now...")
    await run_main_py(user_id, session_string)

    await event.respond("You are now pro... Can save files from DM even they are restricted/like restricted photos from bots etc...")

async def kill_process(user_id):
    user_folder = f"{user_id}pro"
    process = await asyncio.create_subprocess_exec(
        "pkill", "-f", f"python user.py --user_id={user_id}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await process.communicate()
    # Delete the user folder after killing the process
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)

@gagan.on(events.NewMessage(incoming=True, pattern='/noob'))
async def kill_pro(event):
    user_id = event.sender_id
    await kill_process(user_id)
    await event.respond("Sorry to see you again noob...")



#---------------------------- HOSTING / UNHOSTING MULTIPLE BOT WITH MULTIPLE IDs -------------- 

async def download_and_unzip(user_id, bot_token, session, event):
    user_folder = str(user_id)
    try:
        os.mkdir(user_folder)
    except FileExistsError:
        pass

    # Copy the ZIP file to the user folder
    src_zip = "src.zip"  # Provide the path to your src.zip file
    dst_zip = os.path.join(user_folder, "src.zip")
    shutil.copy(src_zip, dst_zip)

    # Unzip the file
    with zipfile.ZipFile(dst_zip, 'r') as zip_ref:
        zip_ref.extractall(user_folder)

    init_file_content = f"""
#Join @devggn

from pyrogram import Client
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from decouple import config
import logging, time, sys

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)

# variables
API_ID = "19748984" #config("API_ID", default=None, cast=int)
API_HASH = "2141e30f96dfbd8c46fbb5ff4b197004" #config("API_HASH", default=None)
BOT_TOKEN = "{bot_token}"
SESSION = "{session}"
FORCESUB = "save_restricted_content_bots" #config("FORCESUB", default=None)
AUTH = "6964148334" #config("AUTH", default=None)
SUDO_USERS = []

if len(AUTH) != 0:
    SUDO_USERS = {{int(AUTH.strip()) for AUTH in AUTH.split()}}
else:
    SUDO_USERS = set()

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 

#userbot = Client(
#    session_name=SESSION, 
#    api_hash=API_HASH, 
#    api_id=API_ID)
userbot = Client("myacc",api_id=API_ID,api_hash=API_HASH,session_string=SESSION)

try:
    userbot.start()
except BaseException:
    print("Your session expired please re add that... thanks @devggn.")
    sys.exit(1)

Bot = Client(
    "SaveRestricted",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)    

try:
    Bot.start()
except Exception as e:
    #print(e)
    #logger.info(e)
    sys.exit(1)
"""

    init_file_path = os.path.join(user_folder, "main", "__init__.py")
    
    # Write the content to the new __init__.py file
    with open(init_file_path, "w") as f:
        f.write(init_file_content)

    # Start the process
    process = await asyncio.create_subprocess_exec(
        "python", "-m", "main", f"--user_id={user_id}",
        cwd=user_folder,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    logging.info(f"Process completed with stdout: {stdout} and stderr: {stderr}")

    # Cleanup
    os.remove(dst_zip)

    return stdout, stderr


@gagan.on(events.NewMessage(incoming=True, pattern='/host (.+) (.+)'))
async def _host(event):
    if event.sender_id != OWNER_ID:
        return await event.respond("this command is now available on @srchostbot. Purchase premium and host...")
    user_id = event.sender_id
    user_folder = str(user_id)

    # Check if the user already has a folder
    if os.path.exists(user_folder):
        await event.respond("You've already hosted a bot. Please remove the existing (send /unhost) one to host again.")
        return

    # Extract BOT_TOKEN and SESSION from the command
    bot_token = event.pattern_match.group(1)
    session = event.pattern_match.group(2)

    # Start the hosting process
    await event.respond("SRC BOT hosted Successfully... It might take few seconds to start")
    stdout, stderr = await download_and_unzip(user_id, bot_token, session, event)

    if stdout:
        await event.respond("Advance SRC Bot hosted successfully! Check your bot if not started then send /logs to check error of session expiration or else.")
    else:
        await event.respond(f"An error occurred during hosting:\n{stderr.decode()}")

@gagan.on(events.NewMessage(incoming=True, pattern='/unhost'))
async def _unhost(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.respond("Darlinggg! Purchase premium to unlock this command")
    user_id = event.sender_id
    user_folder = str(user_id)

    # Check if the user has a folder (if already hosted)
    if os.path.exists(user_folder):
        # Remove the user's folder to unhost the bot
        shutil.rmtree(user_folder)
        await event.respond("Advance SRC bot unhosted successfully!")

        # Stop the running process associated with the hosted bot
        process = await asyncio.create_subprocess_exec(
            "pkill", "-f", f"python -m main --user_id={user_id}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if stderr:
            print(f"Error stopping process: {stderr.decode()}")
    else:
        await event.respond("No SRC bot found for your account.")


# ---------------------- AUTH FUNCTIONS --------------


# ------------------------------------- AUTHORIZATION AND UNAUTHORIZATION for BATCH COMMAND -----------------------

# MongoDB database name and collection name
DB_NAME = "authors"
COLLECTION_NAME = "auth_users"

# Establish a connection to MongoDB
mongo_client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

def load_authorized_users():
    """
    Load authorized user IDs from the MongoDB collection
    """
    authorized_users = set()
    for user_doc in collection.find():
        if "user_id" in user_doc:
            authorized_users.add(user_doc["user_id"])
    return authorized_users

def save_authorized_users(authorized_users):
    """
    Save authorized user IDs to the MongoDB collection
    """
    collection.delete_many({})
    for user_id in authorized_users:
        collection.insert_one({"user_id": user_id})

AUTHORIZED_USERS = load_authorized_users()

@gagan.on(events.NewMessage(incoming=True, pattern='/auth'))
async def _auth(event):
    """
    Command to authorize users
    """
    # Check if the command is initiated by the owner
    if event.sender_id == OWNER_ID:
        # Parse the user ID from the command
        try:
            user_id = int(event.message.text.split(' ')[1])
        except (ValueError, IndexError):
            return await event.respond("Invalid /auth command. Use /auth USER_ID.")

        #Add the user ID to the authorized set
        AUTHORIZED_USERS.add(user_id)
        save_authorized_users(AUTHORIZED_USERS)
        await event.respond(f"User {user_id} has been authorized.")
    else:
        await event.respond("You are not authorized to use this command.")

@gagan.on(events.NewMessage(incoming=True, pattern='/unauth'))
async def _unauth(event):
    """
    Command to revoke authorization for users
    """
    # Check if the command is initiated by the owner
    if event.sender_id == OWNER_ID:
        # Parse the user ID from the command
        try:
            user_id = int(event.message.text.split(' ')[1])
        except (ValueError, IndexError):
            return await event.respond("Invalid /unauth command. Use /unauth USER_ID.")

        # Remove the user ID from the authorized set
        if user_id in AUTHORIZED_USERS:
            AUTHORIZED_USERS.remove(user_id)
            save_authorized_users(AUTHORIZED_USERS)
            await event.respond(f"Authorization revoked for user {user_id}.")
        else:
            await event.respond(f"User {user_id} is not authorized.")
    else:
        await event.respond("You are not authorized to use this command.")

# ----------------- List Authorized Users --------------------------------------------------------

@gagan.on(events.NewMessage(incoming=True, pattern='/list'))
async def list_authorized_users(event):
    """
    Command to list authorized users
    """
    # Check if the command is initiated by the owner
    if event.sender_id == OWNER_ID:
        # Retrieve authorized users from MongoDB
        authorized_users = load_authorized_users()

        if authorized_users:
            # Format the list of authorized users
            user_list = "\n".join(str(user_id) for user_id in authorized_users)
            await event.respond(f"Authorized Users:\n{user_list}")
        else:
            await event.respond("No authorized users found.")
    else:
        await event.respond("You are not authorized to use this command.")
