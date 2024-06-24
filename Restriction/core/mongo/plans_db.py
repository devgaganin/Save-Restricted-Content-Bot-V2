#devggn


import datetime
from config import MONGO_DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_DB)
db = mongo.premium
db = db.premium_db




async def add_premium(user_id, expire_date):
    data = await check_premium(user_id)
    if data and data.get("_id"):
        await db.update_one({"_id": user_id}, {"$set": {"expire_date": expire_date}})
    else:
        await db.insert_one({"_id": user_id, "expire_date": expire_date})


async def remove_premium(user_id):
    await db.delete_one({"_id": user_id})


async def check_premium(user_id):
    x = await db.find_one({"_id": user_id})
    return x


async def premium_users():
    id_list = []
    async for data in db.find():
        id_list.append(data["_id"])
    return id_list

