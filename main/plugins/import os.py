import os
from .. import bot as gagan
from telethon import events, Button
from telethon.tl.types import InputMediaPhoto

S = "/start"
START_PIC = "https://graph.org/file/da97ceca70e55983b4891.png"
TEXT = "Send me the Link of any message of Restricted Channels to Clone it here.\nFor private channel's messages, send the Invite Link first.\n\n👉🏻Execute /batch for bulk process upto 10K files range."

def is_set_button(data):
    return data == "set"

def is_rem_button(data):
    return data == "rem"

@gagan.on(events.CallbackQuery(pattern=b"set"))
async def sett(event):    
    gagan = event.client
    button = await event.get_message()
    msg = await button.get_reply_message()
    await event.delete()
    async with gagan.conversation(event.chat_id) as conv: 
        xx = await conv.send_message("Send me any image for thumbnail as a `reply` to this message.")
        x = await conv.get_reply()
        if not x.media:
            xx.edit("No media found.")
            return
        mime = x.file.mime_type
        if 'png' not in mime and 'jpg' not in mime and 'jpeg' not in mime:
            return await xx.edit("No image found.")
        await xx.delete()
        t = await event.client.send_message(event.chat_id, 'Trying.')
        path = await event.client.download_media(x.media)
        if os.path.exists(f'{event.sender_id}.jpg'):
            os.remove(f'{event.sender_id}.jpg')
        os.rename(path, f'./{event.sender_id}.jpg')
        await t.edit("Temporary thumbnail saved!")

@gagan.on(events.CallbackQuery(pattern=b"rem"))
async def remt(event):  
    gagan = event.client            
    await event.edit('Trying... to save Bamby ... Wait')
    try:
        os.remove(f'{event.sender_id}.jpg')
        await event.edit('Removed!')
    except Exception:
        await event.edit("No thumbnail saved.")                        

@gagan.on(events.NewMessage(pattern=f"^{S}"))
async def start_command(event):
    # Creating inline keyboard with buttons
    buttons = [
        [Button.inline("SET THUMB", data="set"),
         Button.inline("REM THUMB", data="rem")],
        [Button.url("Join Channel", url="https://telegram.dog/dev_gagan")]
    ]

    # Sending photo with caption and buttons
    await gagan.send_file(
        event.chat_id,
        file=START_PIC,
        caption=TEXT,
        buttons=buttons
    )

M = "/plan"
PREMIUM_PIC = "https://graph.org/file/05971cbfdf6987150b9ae.png"
PRE_TEXT = """🌟 Premium Plan Features 🌟\n\n
💰 **Premium Price**: Starting from $1 or 70 INR accepted via **__AMAZON GIFT CARD__** (terms and conditions apply).\n
📥 **Download Limit**: Users can download up to 10,000 files in a single batch command.\n
🛑 **Batch Command Interruption**: Once the batch command is initiated, it cannot be stopped immediately due to security and user interruption concerns.\n
   - Users are advised to wait for the process to automatically cancel before proceeding with any downloads or uploads.\n\n
📜 **Terms and Conditions**: For further details and complete terms and conditions, please send /terms.
"""


@gagan.on(events.NewMessage(pattern=f"^{M}"))
async def plan_command(event):
    # Creating inline keyboard with buttons
    buttons = [
        [Button.url("Send Gift Card Code", url="https://t.me/team_spy_bot")],
        [Button.url("Join Channel", url="https://telegram.dog/dev_gagan")]
    ]

    # Sending photo with caption and buttons
    await gagan.send_file(
        event.chat_id,
        file=PREMIUM_PIC,
        caption=PRE_TEXT,
        buttons=buttons
    )
T = "/terms"
TERM_PIC = "https://graph.org/file/82df13b938b182509081e.png"
TERM_TEXT = """📜 **Terms and Conditions** 📜\n\n
- We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n
- Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.\n
- Payment to us does not guarantee authorization for the /batch command. All decisions regarding authorization are made at our discretion and mood.\n\n
Thank you,\n
Team SPY
"""


@gagan.on(events.NewMessage(pattern=f"^{T}"))
async def term_command(event):
    # Creating inline keyboard with buttons
    buttons = [
        [Button.url("Have a Query?", url="https://t.me/gagan_yan")],
         [Button.url("Join Channel", url="https://telegram.dog/dev_gagan")]
    ]

    # Sending photo with caption and buttons
    await gagan.send_file(
        event.chat_id,
        file=TERM_PIC,
        caption=TERM_TEXT,
        buttons=buttons
    )