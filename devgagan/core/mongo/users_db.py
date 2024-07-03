#devggn

from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli


mongo = MongoCli(MONGO_DB)
db = mongo.users
db = db.users_db


async def get_users():
  user_list = []
  async for user in db.users.find({"user": {"$gt": 0}}):
    user_list.append(user['user'])
  return user_list


async def get_user(user):
  users = await get_users()
  if user in users:
    return True
  else:
    return False

async def add_user(user):
  users = await get_users()
  if user in users:
    return
  else:
    await db.users.insert_one({"user": user})


async def del_user(user):
  users = await get_users()
  if not user in users:
    return
  else:
    await db.users.delete_one({"user": user})
    


