#devggn

from Restriction import app
from pyrogram import filters
from config import OWNER_ID
from Restriction.core.mongo.users_db import get_users, add_user, get_user
from Restriction.core.mongo.plans_db import premium_users




@app.on_message(group=10)
async def chat_watcher_func(_, message):
    try:
        if message.from_user:
            us_in_db = await get_user(message.from_user.id)
            if not us_in_db:
                await add_user(message.from_user.id)
    except:
        pass




@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    users = len(await get_users())
    premium = await premium_users()
    await message.reply_text(f"""
**Total Stats of** {(await client.get_me()).mention} :

**Total Users** : {users}
**Premium Users** : {len(premium)}
""")
  
