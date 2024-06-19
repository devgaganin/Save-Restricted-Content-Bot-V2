import logging
import time
import os
import sys
import asyncio
import json
import pymongo
import zipfile
import requests
import shutil
import asyncio
import re
from .. import bot as gagan
from .. import userbot, Bot, AUTH, SUDO_USERS
from main.plugins.pyroplug import check, get_bulk_msg
from main.plugins.helpers import get_link, screenshot
from main.plugins.pyroplug import user_sessions
from telethon import events, Button, errors
from telethon.tl.types import DocumentAttributeVideo
from pyrogram import Client 
from main.plugins.config import MONGODB_CONNECTION_STRING, LOG_GROUP, OWNER_ID
from pyrogram.errors import FloodWait

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)



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

# Define chunk tasks globally
chunk_tasks = {}


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


@gagan.on(events.NewMessage(incoming=True, pattern='/bulk'))
async def _batch(event):
    user_id = event.sender_id
    if user_id not in AUTHORIZED_USERS:
        return await event.respond("This command is available to Paid Plan users! Send /plan to know more.")
  
    user_session = user_sessions.get(user_id)
    if user_session:
        return await event.respond("You can't use the /bulk command because you have added a session. Please use the /batch command instead.")

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
                    return await conv.send_message("You can only get upto 1000 files in a single batch...")
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

            cd = await conv.send_message("**Batch process ongoing...**\n\nChunks processed: 0", 
                                    buttons=[[Button.url("Join Channel", url="http://t.me/devggn")]])
            co, is_canceled = await run_batch(userbot, Bot, user_id, cd, _link) 
            try: 
                if co == -2:
                    await Bot.send_message(user_id, "Batch successfully completed!")
                    await cd.edit(f"**Batch process ongoing.**\n\nChunks processed: {len(chunk_tasks.get(str(user_id), []))} \n\nBatch successfully completed! ")
            except:
                await Bot.send_message(user_id, "Reached to destination ....")
            finally:
                if is_canceled:
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
        
        # If the user has an ongoing batch, remove it from the batch data
        if str(user_id) in batch_data:
            del batch_data[str(user_id)]
            save_batch_data(batch_data)
            
        # Check if the user has ongoing chunk tasks
        if str(user_id) in chunk_tasks:
            # Cancel ongoing tasks
            for task in chunk_tasks[str(user_id)]:
                task.cancel()
                
            # Clear the chunk tasks list
            del chunk_tasks[str(user_id)]
            
        await event.respond("Operation canceled.")
    else:
        await event.respond("There is no operation to cancel.")


user_preferences = {}
@gagan.on(events.NewMessage(incoming=True, pattern='/set'))
async def set_command_handler(event):
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.respond("You are not authorized to use this command. Purchase premium to use this command")

    # Parse the command arguments using regular expressions
    pattern = r'/set (\d+) (\d+) (\d+) (\d+)'
    match = re.match(pattern, event.text)
    if not match:
        return await event.respond("Invalid command format. Format is ```/set b bt l t```\nSend /help to know more...")
    
    # Extract the arguments from the match object
    batch_size, base_timer, timer_increase_threshold, timer_increase_value = map(int, match.groups())

    # Check if any value is negative
    if batch_size < 0 or base_timer < 0 or timer_increase_threshold < 0 or timer_increase_value < 0:
        return await event.respond("Values cannot be negative!")

    # Check if the sender is the owner
    if event.sender_id == OWNER_ID:
        # Save the user's preferences without validation checks
        user_preferences[event.sender_id] = {
            "batch_size": batch_size,
            "base_timer": base_timer,
            "timer_increase_threshold": timer_increase_threshold,
            "timer_increase_value": timer_increase_value
        }

        response = f"Settings saved successfully!\n\nBatch Size: {batch_size}\nBase Timer: {base_timer}\nTimer Increase Threshold: {timer_increase_threshold}\nTimer Increase Value: {timer_increase_value}\n\nPowered by **__Team SPY__**"
        return await event.respond(response)

    # Your validation checks go here
    # Check if batch_size is valid
    if batch_size > 9:
        return await event.respond("Batch size cannot be greater than 9!")

    # Check if base_timer is valid
    if base_timer < 30:
        return await event.respond("Base timer cannot be less than 30!")

    # Check if timer_increase_threshold is valid
    if timer_increase_threshold < 9 or timer_increase_threshold % batch_size != 0:
        return await event.respond("Timer increase threshold must be at least 9 and a multiple of batch size!")

    # Check if timer_increase_value is valid
    if timer_increase_value < 10:
        return await event.respond("Timer increase value cannot be less than 10!")

    # Save the user's preferences
    user_preferences[event.sender_id] = {
        "batch_size": batch_size,
        "base_timer": base_timer,
        "timer_increase_threshold": timer_increase_threshold,
        "timer_increase_value": timer_increase_value
    }

    response = f"Settings saved successfully!\n\nBatch Size: {batch_size}\nBase Timer: {base_timer}\nTimer Increase Threshold: {timer_increase_threshold}\nTimer Increase Value: {timer_increase_value}\n\nPowered by **__Team SPY__**"
    await event.respond(response)


async def run_batch(userbot, client, sender, countdown, link):
    user_pref = user_preferences.get(sender, None)

    batch_size = user_pref["batch_size"] if user_pref else 3  # Default batch size for non-authorized users
    base_timer = user_pref["base_timer"] if user_pref else 60  # Default base timer value for non-authorized users
    timer_increase_threshold = user_pref["timer_increase_threshold"] if user_pref else 10  # Default threshold for non-authorized users
    timer_increase_value = user_pref["timer_increase_value"] if user_pref else 30  # Default increase value for non-authorized users

    total_ids = len(ids_data[str(sender)])  # Total number of IDs

    # Divide the total number of IDs into chunks based on batch size
    chunks = [ids_data[str(sender)][i:i + batch_size] for i in range(0, total_ids, batch_size)]

    # List to store tasks for each chunk
    chunk_tasks[str(sender)] = []

    # Counter for processed IDs
    processed_ids = 0

    current_timer = base_timer  # Initial timer value

    is_canceled = False

    # Iterate through each chunk
    for chunk in chunks:
        if is_canceled:
            break  # Exit the loop if the batch process is canceled

        chunk_tasks[str(sender)].clear()

        # Create tasks for each ID in the chunk
        for id_num in chunk:
            if is_canceled:
                break  # Exit the loop if the batch process is canceled

            timer = current_timer  # Use the current timer value

            # Adjust timer based on the index within the batch
            if id_num < 2:
                timer = 5
            elif 2 <= id_num < 4:
                timer = 8
            elif id_num == 4:
                timer = 12

            try:
                if 't.me/c/' in link:
                    integer = int(link.split("/")[-1]) + id_num
                else:
                    integer = id_num  # Just use the ID if it's not a channel link
                task = asyncio.create_task(get_bulk_msg(userbot, client, sender, link, integer))
                chunk_tasks[str(sender)].append(task)
                processed_ids += 1

                # Check if it's time to increase the timer
                if processed_ids % timer_increase_threshold == 0:
                    current_timer += timer_increase_value
            except IndexError as ie:
                await client.send_message(sender, f"{i} {ie}\n\nBatch completed!")
                await countdown.delete()
                return -1, is_canceled
            except FloodWait as fw:
                if int(fw.value) > 10:
                    await client.send_message(sender, f'You have floodwaits of {fw.value + 15} seconds, cancelling batch')
                    ids_data.pop(str(sender))
                    return -1, True
                else:
                    fw_alert = await client.send_message(sender,
                                                         f'Sleeping for {fw.value + 15} second(s) due to Telegram floodwait.')
                    ors = fw.value + 5
                    await asyncio.sleep(ors)
                    await fw_alert.delete()
                    try:
                        task = asyncio.create_task(get_bulk_msg(userbot, client, sender, link, integer))
                        chunk_tasks[str(sender)].append(task)
                    except Exception as e:
                        logger.info(e)
                        if countdown.text != count_down:
                            await countdown.edit(count_down,
                                                 buttons=[[Button.url("Join Channel", url="http://t.me/devggn")]])
            except Exception as e:
                if countdown.text != count_down:
                    await countdown.edit(count_down,
                                         buttons=[[Button.url("Join Channel", url="https://t.me/devggn")]])

        # Wait for all tasks in the chunk to complete
        await asyncio.gather(*chunk_tasks[str(sender)])

        # Add a delay after processing every 5 IDs
        if processed_ids % batch_size == 0:
            # Show message about sleeping
            sleep_message = f"Sleeping for {current_timer} seconds before processing the next batch."
            sleep_msg = await client.send_message(sender, sleep_message)
            # Edit countdown message to show processed value only
            await countdown.edit(f"**Batch process ongoing...**\n\nProcessed: {processed_ids} Links", buttons=[[Button.url("Join Channel", url="http://t.me/devggn")]])

            try:
                await asyncio.sleep(current_timer)  # Sleep for the current timer value
            except asyncio.CancelledError:
                is_canceled = True
            finally:
              await sleep_msg.delete()
    # Batch completed or canceled
    if is_canceled:
        await countdown.edit("**Batch process canceled.**")
    else:
        await countdown.edit("**Batch process completed.**")
    await countdown.delete()
    return -2, is_canceled


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
    if event.sender_id not in AUTHORIZED_USERS:
        return await event.respond("You are not authorized to use this command!")
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


@gagan.on(events.NewMessage(incoming=True, pattern='/batch'))
async def _bulk(event):
    user_id = event.sender_id
    if user_id != OWNER_ID and user_id not in AUTHORIZED_USERS:
        return await event.respond("The batch command is not available in public. You have to host your own bot to use this. Send /host BOT_TOKEN SESSION to host your own bot.")

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
                    return await conv.send_message("You can only get upto 1000 files in a single batch...")
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
            co = await r_batch(userbot, Bot, user_id, cd, _link) 
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


async def r_batch(userbot, client, sender, countdown, link):
    for i in range(len(ids_data[str(sender)])):
        timer = 30  # Increased default timer value

        if i < 250:
            timer = 5
        elif 250 <= i < 1000:
            timer = 10
        elif 1000 <= i < 10000:
            timer = 15
        elif 10000 <= i < 50000:
            timer = 20
        elif 50000 <= i < 100000:
            timer = 25
        elif 100000 <= i < 200000:
            timer = 30
        elif i >= 200000:
            timer = 35  # Increased timer value for larger counts

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


#user's account bot hosting
      
async def run_main_py(user_id, session_string):
    folder_name = f"{user_id}pro"
    file_path = os.path.join(folder_name, "user.py")

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Write the Python code into main.py
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


@app.on_message(filters.command("wow") & filters.reply)
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

    # Run the main.py file in a subprocess
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

    await event.respond("You are now pro.")

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
