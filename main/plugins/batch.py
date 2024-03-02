#Join t.me/dev_gagan

import logging
import time, os, asyncio
import json

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


batch = []
ids = []

'''async def get_pvt_content(event, chat, id):
    msg = await userbot.get_messages(chat, ids=id)
    await event.client.send_message(event.chat_id, msg) 
'''

@gagan.on(events.NewMessage(incoming=True, pattern='/batch'))
async def _batch(event):
    s = False
    if f'{event.sender_id}' in batch:
        return await event.reply("You've already started one batch, wait for it to complete you dumbfuck owner!")
    async with gagan.conversation(event.chat_id) as conv: 
        if not s:
            await conv.send_message(f"Send me the message link you want to start saving from, as a reply to this message.", buttons=Button.force_reply())
            try:
                link = await conv.get_reply()
                try:
                    _link = get_link(link.text)
                except Exception:
                    await conv.send_message("No link found.")
            except Exception as e:
                #print(e)
                logger.info(e)
                return await conv.send_message("Cannot wait more longer for your response!")
            await conv.send_message(f"Send me the number of files/range you want to save from the given message, as a reply to this message.", buttons=Button.force_reply())
            try:
                _range = await conv.get_reply()
            except Exception as e:
                logger.info(e)
                #print(e)
                return await conv.send_message("Cannot wait more longer for your response!")
            try:
                value = int(_range.text)
                if value > 1000000:
                    return await conv.send_message("You can only get upto 100000 files in a single batch.")
            except ValueError:
                return await conv.send_message("Range must be an integer!")
            for i in range(value):
                ids.append(i)
            s, r = await check(userbot, Bot, _link)
            if s != True:
                await conv.send_message(r)
                return
            batch.append(f'{event.sender_id}')
            cd = await conv.send_message("**Batch process ongoing...**\n\nProcess completed: ", 
                                    buttons=[[Button.url("Join Channel", url="http://t.me/dev_gagan")]])
            co = await run_batch(userbot, Bot, event.sender_id, cd, _link) 
            try: 
                if co == -2:
                    await Bot.send_message(event.sender_id, "Batch successfully completed!")
                    await cd.edit(f"**Batch process ongoing.**\n\nProcess completed: {value} \n\n Batch successfully completed! ")
            except:
                await Bot.send_message(event.sender_id, "ERROR!\n\n maybe last msg didnt exist yet")
            conv.cancel()
            ids.clear()
            batch.clear()

@gagan.on(events.callbackquery.CallbackQuery(data="cancel"))
async def cancel(event):
    ids.clear()
    batch.clear()

    
async def run_batch(userbot, client, sender, countdown, link):
    for i in range(len(ids)):
        timer = 6
        if i < 250:
            timer = 2
        elif i < 1000 and i > 100:
            timer = 3
        elif i < 10000 and i > 1000:
            timer = 4
        elif i < 50000 and i > 10000:
            timer = 5
        elif i < 100000 and i > 50000:
            timer = 6
        elif i < 200000 and i > 100000:
            timer = 8
        elif i < 1000000: 
            timer = 10
        
        if 't.me/c/' not in link:
            timer = 1 if i < 500 else 2
        try: 
            count_down = f"**Batch process ongoing.**\n\nProcess completed: {i+1}"
            #a =ids[i]
            try:
                msg_id = int(link.split("/")[-1])
            except ValueError:
                if '?single' not in link:
                    return await client.send_message(sender, "**Invalid Link! .**")
                link_ = link.split("?single")[0]
                msg_id = int(link_.split("/")[-1])
            integer = msg_id + int(ids[i])
            await get_bulk_msg(userbot, client, sender, link, integer)
            protection = await client.send_message(sender, f"Sleeping for `{timer}` seconds to avoid Floodwaits and Protect account!")
            await countdown.edit(count_down, 
                                 buttons=[[Button.url("Join Channel", url="https://t.me/dev_gagan")]])
            await asyncio.sleep(timer)
            await protection.delete()
        except IndexError as ie:
            await client.send_message(sender, f" {i}  {ie}  \n\nBatch ended completed!")
            await countdown.delete()
            break
        except FloodWait as fw:
            if int(fw.value) > 300:
                await client.send_message(sender, f'You have floodwaits of {fw.value} seconds, cancelling batch') 
                ids.clear()
                break
            else:
                fw_alert = await client.send_message(sender, f'Sleeping for {fw.value + 5} second(s) due to telegram flooodwait.')
                ors = fw.value + 5
                await asyncio.sleep(ors)
                await fw_alert.delete()
                try:
                    await get_bulk_msg(userbot, client, sender, link, integer)
                except Exception as e:
                    #print(e)
                    logger.info(e)
                    if countdown.text != count_down:
                        await countdown.edit(count_down, buttons=[[Button.url("Join Channel", url="http://t.me/dev_gagan")]])
        except Exception as e:
            #print(e)
            logger.info(e)
            await client.send_message(sender, f"An error occurred during cloning, batch will continue.\n\n**Error:** {str(e)}")
            if countdown.text != count_down:
                await countdown.edit(count_down, buttons=[[Button.url("Join Channel", url="https://t.me/dev_gagan")]])
        n = i + 1
        if n == len(ids):
            return -2

C = "/cancel"
START_PIC = "https://graph.org/file/da97ceca70e55983b4891.png"
TEXT = "👋 Hi, This is 'Paid Restricted Content Saver' bot Made with ❤️ by __**Team SPY**__."

@gagan.on(events.NewMessage(pattern=f"^{C}"))
async def start_command(event):
    # Creating inline keyboard with buttons
    buttons = [
        [Button.inline("Cancel", data="cancel"),
         Button.inline("Cancel", data="cancel")],
        [Button.url("Join Channel", url="https://telegram.dog/dev_gagan")]
    ]

    # Sending photo with caption and buttons
    await gagan.send_file(
        event.chat_id,
        file=START_PIC,
        caption=TEXT,
        buttons=buttons
    )
            
TEXTING = """
```
Execute /batch command only when you 100% sure.
Bcz /cancel event is removed to make bot work perfectly.
Thanks - Team SPY

```
"""
