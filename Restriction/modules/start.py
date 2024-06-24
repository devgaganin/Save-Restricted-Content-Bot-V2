#devggn

from pyrogram import filters
from Restriction import app
from Restriction.core import script
from Restriction.core.func import subscribe
from config import OWNER_ID
from Restriction.modules.settings import *
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton



# ------------------------------------------------------------------------------- #

# ------------------- Start-Buttons ------------------- #

buttons = InlineKeyboardMarkup(
         [[
               InlineKeyboardButton("Join Channel", url="https://t.me/devggn"),
	       InlineKeyboardButton("Contact Me", url="https://t.me/ggnhere"), 
         ],[
               InlineKeyboardButton("Don't Click", callback_data="admin_"),    
         ],[
	       InlineKeyboardButton("Take Help", callback_data="help2_"), 
               InlineKeyboardButton("Know Commands", callback_data="help_"),    
         ]])


# ------------------- Back-Button ------------------- #

back_button  = [[
                    InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="home_"),                    
                ]]


# ------------------- Settings-Buttons ------------------- #

buttons1 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏜 ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="thumb_")                
            ],
	    [
                InlineKeyboardButton("📝 ᴄᴀᴘᴛɪᴏɴ", callback_data="caption_"),
		InlineKeyboardButton("🌐 ᴄʜᴀɴɴᴇʟ", callback_data="channel_")
            ],
	    [
                InlineKeyboardButton("📊 sᴇssɪᴏɴ", callback_data="session_"),
		InlineKeyboardButton("📇 ᴡᴀᴛᴇʀᴍᴀʀᴋ", callback_data="maintainer_")
            ]])


# ------------------- Thumb-Buttons ------------------- #

buttons2 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✚ sᴇᴛ ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="set_thumb")              
            ],
            [
		InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_thumb"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_thumb"),
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_"),
            ] 
        ])



# ------------------- Session-Buttons ------------------- #

buttons3 = InlineKeyboardMarkup([
	    [                
                InlineKeyboardButton("✚ sᴇᴛ sᴇssɪᴏɴ", callback_data="set_session")
            ],
            [                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_session"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_session")
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_"),
            ]
        ])


# ------------------- Caption-Buttons ------------------- #

buttons4 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🖍️ʀᴇɴᴇᴡ ᴄᴀᴘᴛɪᴏɴ", callback_data="renew_"),
                InlineKeyboardButton("🖋️ʀᴇᴘʟᴀᴄᴇ ᴄᴀᴘᴛɪᴏɴ", callback_data="replace_")
            ],
            [
                InlineKeyboardButton("✚ ᴅᴇʟᴇᴛᴇ ᴡᴏʀᴅs", callback_data="words_"),
		InlineKeyboardButton("sᴏᴏɴ", callback_data="soon")
            ],    
	    [            
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_")		
            ]
        ])


# ------------------- Renew-Caption-Buttons ------------------- #

renew_button = InlineKeyboardMarkup([
	    [                
                InlineKeyboardButton("✚ ᴀᴅᴅ ʀᴇɴᴇᴡ ᴄᴀᴘᴛɪᴏɴ", callback_data="set_caption"),
            ],
            [                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_caption"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_caption")
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="c_back"),
            ]
        ])


# ------------------- Replace-Caption-Buttons ------------------- #

replace_button = InlineKeyboardMarkup([
	    [                
                InlineKeyboardButton("✚ ᴀᴅᴅ ʀᴇᴘʟᴀᴄᴇ ᴄᴀᴘᴛɪᴏɴ", callback_data="re_caption"),
            ],
            [                
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="del_replace"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_replace")
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="c_back"),
            ]
        ])


# ------------------- Remove-Caption-Buttons ------------------- #

words_button = InlineKeyboardMarkup([
	    [                
                InlineKeyboardButton("✚ ᴀᴅᴅ ᴍᴏʀᴇ ᴡᴏʀᴅs", callback_data="add_words"),
            ],
            [          
                InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_words"),
		InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_words")                		
            ],
            [
		InlineKeyboardButton("📑 ᴅᴇʟᴇᴛᴇ ᴀʟʟ", callback_data="delall_words"),
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="c_back"),
            ]
        ])

# ------------------- Channel-Buttons ------------------- #

buttons5 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✚ sᴇᴛ ᴄʜᴀɴɴᴇʟ", callback_data="set_chat")              
            ],
            [
		InlineKeyboardButton("❌ ʀᴇᴍᴏᴠᴇ", callback_data="rm_chat"),
                InlineKeyboardButton("📖 ᴠɪᴇᴡ", callback_data="views_chat"),
            ],
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_"),
            ] 
        ])

# ------------------------------------------------------------------------------- #


@app.on_message(filters.command("start"))
async def start(_,message):
  join = await subscribe(_,message)
  if join ==1:
    return
  await message.reply_photo(photo="https://graph.org/file/4e80dc2f4f6f2ddadb4d2.jpg",
                                  caption=script.START_TXT.format(message.from_user.mention), reply_markup=buttons)



@app.on_callback_query()
async def handle_callback(_, query):

    if query.data == "home_":                
        await query.message.edit_text(
            script.START_TXT.format(query.from_user.mention),
            reply_markup=buttons
        )

    elif query.data == "admin_":
        user_id = query.from_user.id
        if user_id in OWNER_ID:
            reply_markup = InlineKeyboardMarkup(back_button)
            await query.message.edit_text(
                script.ADMIN_TXT,
                reply_markup=reply_markup
            )
        else:
            await query.answer("You are not authorized to use this command...", show_alert=True)

    elif query.data == "help_":
        reply_markup = InlineKeyboardMarkup(back_button)
        await query.message.edit_text(
            script.HELP_TXT,
            reply_markup=reply_markup
        )
	    
    elif query.data == "help2_":
        reply_markup = InlineKeyboardMarkup(back_button)
        await query.message.edit_text(
            script.HELP2_TXT,
            reply_markup=reply_markup
        )

	

    elif query.data == "thumb_":
        await query.message.edit_text(script.THUMBNAIL_TXT, reply_markup=buttons2)
    elif query.data == "caption_":
        await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=buttons4)
    elif query.data == "session_":
        await query.message.edit_text(script.SESSION_TXT, reply_markup=buttons3)
    elif query.data == "channel_":
        await query.message.edit_text(script.CHANNEL_TXT, reply_markup=buttons5)
    elif query.data == "back_":
        await query.message.edit_text(script.SETTINGS_TXT, reply_markup=buttons1)

    elif query.data == "renew_":
        await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=renew_button)
    elif query.data == "replace_":
        await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=replace_button)
    elif query.data == "words_":
        await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=words_button)    
    elif query.data == "c_back":
        await query.message.edit_text(script.CAPTI0NS_TXT, reply_markup=buttons4)

    elif query.data == "set_thumb":
        await add_thumb(query)
    elif query.data == "rm_thumb":
        await remove_thumb(query)
    elif query.data == "views_thumb":
        await view_thumb(query)

    elif query.data == "set_caption":
        await add_caption(query)
    elif query.data == "rm_caption":
        await delete_caption(query)
    elif query.data == "views_caption":
        await see_caption(query)

    elif query.data == "re_caption":
        await replace_func(query)
    elif query.data == "del_replace":
        await rm_replace(query)
    elif query.data == "views_replace":
        await see_replace(query)

    elif query.data == "views_session":
        await view_session(query)
    elif query.data == "rm_session":
        await delete_session(query)
    elif query.data == "set_session":
        await add_session(query)

    elif query.data == "add_words":
        await add_clearwords(query)
    elif query.data == "views_words":
        await view_clearwords(query)
    elif query.data == "rm_words":
        await remove_clearwords(query)
    elif query.data == "delall_words":
        await deleteall_clearwords(query)

    elif query.data == "set_chat":
        await add_channel(query)
    elif query.data == "views_chat":
        await view_channel(query)
    elif query.data == "rm_chat":
        await delete_channel(query)
	
    elif query.data == "maintainer_":    
        await query.answer("sᴏᴏɴ.... \n ʙᴏᴛ ᴜɴᴅᴇʀ ɪɴ ᴍᴀɪɴᴛᴀɪɴᴀɴᴄᴇ", show_alert=True)

    elif query.data == "close_data":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass






		
