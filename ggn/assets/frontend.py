import time
import os
import logging
import json
from telethon import events, Button, errors
from pyrogram.errors import FloodWait
from .. import bot as gagan
from .. import Bot
from .. import FORCESUB as fs
from main.plugins.pyroplug import get_msg, check, get_bulk_msg
from main.plugins.helpers import get_link, join, screenshot, get_link, screenshot
from main.plugins.helpers import force_sub
from main.plugins.login import get_session
import logging
import asyncio
import pymongo
from telethon.tl.types import DocumentAttributeVideo
from pyrogram import Client 
# from config import API_ID, API_HASH

API_ID = "19748984" #config("API_ID", default=None, cast=int)
API_HASH = "2141e30f96dfbd8c46fbb5ff4b197004" #config("API_HASH", default=None)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger("telethon").setLevel(logging.INFO)

ft = f"To use this bot you've to join @{fs}."
message = "Send me the message link you want to start saving from, as a reply to this message."

process = []
timer = []
user = []

# List of commands that should bypass the link check
commands = ['/dl', '/pdl', '/adl']  # Add other commands as needed

@gagan.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def clone(event):
    logging.info(event)
    file_name = ''

    # Check if the message starts with a command
    if any(event.message.text.startswith(command) for command in commands):
        # Command detected, bypass link check and do nothing
        return

    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.text == message:
            return

    lit = event.text
    li = lit.split("\n")

    if len(li) > 10:
        await event.respond("max 10 links per message")
        return

    for line in li:
        try:
            link = get_link(line)
            if not link:
                return
        except TypeError:
            return

        s, r = await force_sub(event.client, fs, event.sender_id, ft)
        if s is True:
            await event.respond(r)
            return

        if f'{int(event.sender_id)}' in user:
            return await event.respond("Please don't spam links, wait until ongoing process is done.")
        user.append(f'{int(event.sender_id)}')

        edit = await event.respond("Processing!")

        if "|" in line:
            url = line
            url_parts = url.split("|")
            if len(url_parts) == 2:
                file_name = url_parts[1]

        if file_name is not None:
            file_name = file_name.strip()

        try:
            if 't.me/' not in link:
                await edit.edit("invalid link")
                ind = user.index(f'{int(event.sender_id)}')
                user.pop(int(ind))
                return

            if 't.me/+' in link:
                q = await join(userbot, link)
                await edit.edit(q)
                ind = user.index(f'{int(event.sender_id)}')
                user.pop(int(ind))
                return

            if 't.me/' in link:
                msg_id = 0
                try:
                    msg_id = int(link.split("/")[-1])
                except ValueError:
                    if '?single' in link:
                        link_ = link.split("?single")[0]
                        msg_id = int(link_.split("/")[-1])
                    else:
                        msg_id = -1
                m = msg_id
                user_id = event.sender_id
                userbot = None
                session_data = get_session(user_id)
                if session_data:
                    try:
                        userbot = Client(":userbot:", api_id=API_ID, api_hash=API_HASH, session_string=session_data)
                        await userbot.start()
                    except Exception as e:
                        await edit.delete()
                        await event.respond("Login in bot to continue send /login")
                        ind = user.index(f'{int(event.sender_id)}')
                        user.pop(int(ind))
                        return
                else:
                    await event.respond("Login in the bot to use send /login")
                    ind = user.index(f'{int(event.sender_id)}')
                    user.pop(int(ind))
                    return
                await get_msg(userbot, Bot, event.sender_id, edit.id, link, m, file_name)

        except FloodWait as fw:
            await gagan.send_message(event.sender_id, f'Try again after {fw.value} seconds due to floodwait from telegram.')
            await edit.delete()
        except Exception as e:
            logging.info(e)
            await gagan.send_message(event.sender_id, f"An error occurred during cloning of `{link}`\n\n**Error:** {str(e)}")
            await edit.delete()

        ind = user.index(f'{int(event.sender_id)}')
        user.pop(int(ind))
        time.sleep(1)
                  


# -------------------------------- BATCH FETURES ---------------------------------

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
    userbot = None
    # if user_id not in AUTHORIZED_USERS:
        # return await event.respond("This command is available to Paid Plan users! Send /plan to know more.")
    session_data = get_session(user_id)
    if session_data:
        try:
            userbot = Client(":userbot:", api_id=API_ID, api_hash=API_HASH, session_string=session_data)
            await userbot.start()
        except Exception as e:
            await event.respond("Login in bot to continue send /login")
    else:
      await event.respond("Login in bot to continue send /login")
      return
      
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
                if value > 3:
                    return await conv.send_message("You can only get up to 3 files in a single batch.\n\nPurchase premium to go beyong limit send /plan to know more...")
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
