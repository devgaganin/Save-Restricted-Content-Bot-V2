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

from telethon import events, Button, errors
from telethon.tl.types import DocumentAttributeVideo

from pyrogram import Client 
from pyrogram.errors import FloodWait

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


# Define the log file path
temp_log_file = "logs.txt"

# Create the log file if it doesn't exist
if not os.path.exists(temp_log_file):
    with open(temp_log_file, "w"):
        pass

# Define a class to redirect stdout and stderr to a log file
class StreamToLogger:
    def __init__(self, logger, log_level, log_file):
        self.logger = logger
        self.log_level = log_level
        self.log_file = log_file

    def write(self, buf):
        with open(self.log_file, 'a') as f:
            f.write(buf)
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

    def fileno(self):
        return 0  # Dummy fileno implementation

# Close existing logging handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure logging to write to the log file
logging.basicConfig(filename=temp_log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Redirect stdout and stderr to the log file
stdout_logger = logging.getLogger('STDOUT')
sl_out = StreamToLogger(stdout_logger, logging.INFO, temp_log_file)
sys.stdout = sl_out

stderr_logger = logging.getLogger('STDERR')
sl_err = StreamToLogger(stderr_logger, logging.ERROR, temp_log_file)
sys.stderr = sl_err

# Function to reset the log file
def reset_log_file():
    try:
        if os.path.exists(temp_log_file):
            os.remove(temp_log_file)
        with open(temp_log_file, "w"):
            pass
        print("Log file reset")  # Debugging statement
        
        # Recreate StreamToLogger instances after resetting the log file
        recreate_log_handlers()
    except Exception as e:
        print("Error resetting log file:", e)  # Debugging statement

# Function to recreate StreamToLogger instances and update root logger handlers
def recreate_log_handlers():
    global sl_out, sl_err
    stdout_logger = logging.getLogger('STDOUT')
    sl_out = StreamToLogger(stdout_logger, logging.INFO, temp_log_file)
    sys.stdout = sl_out

    stderr_logger = logging.getLogger('STDERR')
    sl_err = StreamToLogger(stderr_logger, logging.ERROR, temp_log_file)
    sys.stderr = sl_err
    
    # Update root logger handlers
    logging.root.handlers = []
    logging.basicConfig(filename=temp_log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initial creation of StreamToLogger instances
recreate_log_handlers()

# Schedule the task to reset the log file every 120 seconds
async def schedule_log_reset():
    while True:
        await asyncio.sleep(180)
        reset_log_file()

# Start the task scheduler
asyncio.ensure_future(schedule_log_reset())

@gagan.on(events.NewMessage(incoming=True, pattern='/logs'))
async def send_log(event):
    user_id = event.sender_id
    
    # Check if the log file exists
    if os.path.exists(temp_log_file):
        # Send the log file as a document to the user
        await gagan.send_file(user_id, temp_log_file, caption="Here is the log file of last 2 min.")
    else:
        await event.respond("Log file not found.")


@gagan.on(events.NewMessage(incoming=True, pattern='/batch'))
async def _bulk(event):
    user_id = event.sender_id
  
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
                if value > 10000:
                  return await conv.send_message("You can only get upto 10000 files in a single batch...")
            except ValueError:
                return await conv.send_message("Range must be an integer!")

            ids_data[str(user_id)] = list(range(value))
            save_ids_data(ids_data)

            s, r = await check(userbot, Bot, _link)
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

        if i < 25:
            timer = 20
        elif 250 <= i < 100:
            timer = 25
        elif 100 <= i < 1000:
            timer = 30
        elif 1000 <= i < 5000:
            timer = 35
        elif 5000 <= i < 10000:
            timer = 40
        elif 10000 <= i < 20000:
            timer = 45
        elif i >= 20000:
            timer = 60  # Increased timer value for larger counts

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

