
import asyncio
import importlib
from pyrogram import idle
from devgagan.modules import ALL_MODULES
from aiojobs import create_scheduler
from devgagan.core.mongo.plans_db import check_and_remove_expired_users
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

loop = asyncio.get_event_loop()

async def schedule_expiry_check():
    # This function now just runs the task without any loop or sleep
    await check_and_remove_expired_users()

async def devggn_boot():
    for all_module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + all_module)
    print("Bot deployed...🎉")

    # Start the background task for checking expired users
    asyncio.create_task(schedule_expiry_check())
    # Keep the bot running
    await idle()
    print("Lol ...")

if __name__ == "__main__":
    loop.run_until_complete(devggn_boot())
