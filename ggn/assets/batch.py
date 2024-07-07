import time
import os
import logging
import json
from .. import bot as gagan
from .. import Bot
from telethon import events, Button, errors
from pyrogram.errors import FloodWait
from ggn.assets.pyroplug import get_msg, check, get_bulk_msg
from ggn.assets.functions import get_link, join, screenshot, force_sub
from ggn.assets.login import get_session
import logging
import asyncio
import pymongo
from telethon.tl.types import DocumentAttributeVideo
from pyrogram import Client 
from config import API_ID, API_HASH

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)



# --------------------- BATCH BEGINS ------------------ 

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
      await event.respond("Login in bot to continue send /login or for session based send /settings")
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
        timer = 15  # Increased default timer value

        if i < 250:
            timer = 20
        elif 250 <= i < 1000:
            timer = 25
        elif 1000 <= i < 10000:
            timer = 30
        elif 10000 <= i < 50000:
            timer = 35
        elif 50000 <= i < 100000:
            timer = 40
        elif 100000 <= i < 200000:
            timer = 45
        elif i >= 200000:
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
