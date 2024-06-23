#devggn

from telegraph import upload_file
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Restriction.core.mongo import db
from Restriction import app
from Restriction.core import script
from Restriction.core.func import subscribe, chk_user


# --------------------Thumbnail--------------------- #

async def add_thumb(query):
    mkn = await app.ask(query.message.chat.id, text="Please send me your thumbnail photo.")
    if mkn.photo:
        file_name = str(query.from_user.id) + "set_thumb.jpg"
        photo_id = mkn.photo.file_id
        photo_path = await app.download_media(photo_id, file_name=file_name)
        fk = upload_file(photo_path)
        for x in fk:
            url = "https://telegra.ph" + x
        await db.set_thumbnail(query.from_user.id, url)
        await query.message.reply_text("✅️ Your thumbnail has been successfully saved.")        	
    else:
        await query.message.reply_text("❌️ Please send a valid photo for your thumbnail.")

async def remove_thumb(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("thumb"):
        thumb = data.get("thumb")
        await db.remove_thumbnail(query.from_user.id)
        await query.answer("☘️ Your thumbnail has been successfully deleted.", show_alert=True)
    else:
        await query.answer("😜 You haven't set any thumbnails.", show_alert=True)
	
async def view_thumb(query):    
    data = await db.get_data(query.from_user.id)
    if data and data.get("thumb"):
       thumb = data.get("thumb")    
       await query.message.reply_photo(thumb)
    else:
        await query.answer("😜 You haven't set any thumbnails.", show_alert=True) 



# --------------------Caption--------------------- #

async def add_caption(query):    
    cap = await app.ask(query.message.chat.id, text="» ɢɪᴠᴇ ᴍᴇ ᴀ ᴄᴀᴘᴛɪᴏɴ ᴛᴏ sᴇᴛ.")
    caption = cap.text
    await db.set_caption(query.from_user.id, caption=caption)
    await query.message.reply_text("✅ Your caption has been successfully set.")

async def delete_caption(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("caption"):
      await db.remove_caption(query.from_user.id)
      await query.answer("☘️ Your caption has been successfully deleted.", show_alert=True)

    else:
      await query.answer("👀 You haven't set any caption !!", show_alert=True)    

async def replace_func(query):    
    replace = await app.ask(query.message.chat.id, text="Send me the text you want to replace.")
    replace = replace.text
    to_replace = await app.ask(query.message.chat.id, text="Send me the text you'd like to have replaced.")
    to_replace = to_replace.text
    await db.replace_caption(query.from_user.id, replace, to_replace)
    await query.message.reply_text("✅ Your replace caption has been successfully set.")

async def rm_replace(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("replace_txt") and data.get("to_replace"):
      await db.remove_replace(query.from_user.id)
      await query.answer("☘️ Your replace caption has been successfully deleted.", show_alert=True)
    else:
      await query.answer("👀 You haven't set any replace caption !!", show_alert=True)    


async def see_caption(query):
    data = await db.get_data(query.from_user.id)
    if data and data.get("caption"):
       caption = data.get("caption")
       await query.message.reply_text(f"**Your Caption:** `{caption}`")
    else:
       await query.answer("👀 You haven't set any caption !!", show_alert=True)


async def see_replace(query):
    data = await db.get_data(query.from_user.id)
    if data and data.get("replace_txt") and data.get("to_replace"):
       replace = data.get("replace_txt")
       to_replace = data.get("to_replace")
       await query.message.reply_text(f"**Your replace text:** `{replace}`\n\nYour to replace text: `{to_replace}`")
    else:
       await query.answer("👀 You haven't set any caption !!", show_alert=True)


# --------------------String-Session--------------------- #

async def add_session(query):    
    sos = await app.ask(query.message.chat.id, text="Give me a caption to set.")
    session = sos.text
    await db.set_session(query.from_user.id, session=session)
    await query.message.reply_text("✅ Your caption has been successfully set.")

async def delete_session(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("session"):
      await db.remove_session(query.from_user.id)
      await query.answer("☘️ Your session has been successfully deleted.", show_alert=True)
    else:
      await query.answer("👀 You haven't set any session !!", show_alert=True)    
                                             
async def view_session(query):
    data = await db.get_data(query.from_user.id)
    if data and data.get("session"):
       string_session = data.get("session")
       await query.message.reply_text(f"**Here is your string session**\n\n`{string_session}`")
    else:
       await query.answer("👀 You haven't set any session !!", show_alert=True)



# --------------------Clear-Words--------------------- #

async def add_clearwords(query):    
    sos = await app.ask(query.message.chat.id, text="📝 Send me the words you want to remove from the caption. For example: hello,how are you,test,use, etc.")
    words = sos.text
    data = words.split(",")
    add_words = list(data)
    await db.clean_words(query.from_user.id, add_words)
    await query.message.reply_text("✅ Your deleted words has been successfully set.")

async def view_clearwords(query):
    data = await db.get_data(query.from_user.id)
    if data and data.get("clean_words"):
        words = data.get("clean_words")
        lol = ""
        for woe in words:
            lol += f"•> {woe}\n"
        await query.message.reply_text(f"**Here are your deleted words**\n\n`{lol}`")
    else:
        await query.answer("👀 You haven't set any deleted words !!", show_alert=True)


async def remove_clearwords(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("clean_words"):
      sos = await app.ask(query.message.chat.id, text="📝 Send me the words you want to remove from the deleted words db. For example: hello,how are you,test,use, etc.")
      words = sos.text
      data = words.split(",")
      rm_words = list(data)
      await db.remove_clean_words(query.from_user.id, rm_words)    
      await query.message.reply_text("☘️ Your deleted words has been successfully deleted.")
    else:
      await query.answer("👀 You haven't set any deleted words !!", show_alert=True)    


async def deleteall_clearwords(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("clean_words"):
      await db.all_words_remove(query.from_user.id)
      await query.answer("☘️ Your deleted words has been successfully deleted.", show_alert=True)
    else:
      await query.answer("👀 You haven't set any deleted words !!", show_alert=True)    


# --------------------Channel--------------------- #

async def add_channel(query):    
    sos = await app.ask(query.message.chat.id, text="Give me your channel id.")
    chat_id = sos.text
    await db.set_channel(query.from_user.id, chat_id=int(chat_id))
    await query.message.reply_text("✅ Your channel id has been successfully set.")

async def delete_channel(query):
    data = await db.get_data(query.from_user.id)  
    if data and data.get("chat_id"):
      await db.remove_channel(query.from_user.id)
      await query.answer("☘️ Your channel id has been successfully deleted.", show_alert=True)
    else:
      await query.answer("👀 You haven't set any channel id !!", show_alert=True)    
                                             
async def view_channel(query):
    data = await db.get_data(query.from_user.id)
    if data and data.get("chat_id"):
       channel_id = data.get("chat_id")
       await query.message.reply_text(f"**Here is your channel id**\n\n`{channel_id}`")
    else:
       await query.answer("👀 You haven't set any channel id !!", show_alert=True)




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



@app.on_message(filters.command("settings") & filters.private)
async def settings(_, message):
    join = await subscribe(_, message)
    if join == 1:
      return
    lol = await chk_user(message, message.from_user.id)
    if lol == 1:
        return
    await message.reply_photo(photo="https://graph.org/file/914e6257251a02fde4203.jpg", caption=script.SETTINGS_TXT, reply_markup=buttons1)

	
