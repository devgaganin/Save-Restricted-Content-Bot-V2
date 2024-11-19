# devggn

import asyncio
import importlib
import psutil
import gc  # For garbage collection
from pyrogram import idle
from aiojobs import create_scheduler
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users

# Subprocess monitoring interval (in seconds)
CHECK_INTERVAL = 1800  # 30 minutes
# Memory optimization interval (in seconds)
MEMORY_OPTIMIZATION_INTERVAL = 600  # 10 minutes


# Function to monitor and terminate idle subprocesses
async def close_idle_subprocesses():
    while True:
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                # Terminate subprocesses spawned by the current process
                if proc.ppid() == psutil.Process().pid:
                    proc.terminate()
                    print(f"Terminated subprocess: PID {proc.pid}, Name: {proc.name()}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        await asyncio.sleep(CHECK_INTERVAL)


# Function to reduce memory usage
async def optimize_memory():
    while True:
        gc.collect()
        process = psutil.Process()
        memory_info = process.memory_info()
        print(f"Memory Usage: {memory_info.rss / 1024 / 1024:.2f} MB")
        await asyncio.sleep(MEMORY_OPTIMIZATION_INTERVAL)


# Function to schedule expiry checks
async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(3600)  # Check every hour


# Main bot function
async def devggn_boot():
    # Import modules
    for all_module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + all_module)

    # print("»»»» ʙᴏᴛ ᴅᴇᴘʟᴏʏ sᴜᴄᴄᴇssғᴜʟʟʏ ✨ 🎉")
    print("Bot started!")  # Added print statement here

    # Start background tasks
    asyncio.create_task(schedule_expiry_check())
    asyncio.create_task(close_idle_subprocesses())
    asyncio.create_task(optimize_memory())

    # Keep the bot running
    await idle()
    print("Lol ...")


# Run the bot
if __name__ == "__main__":
    # Reuse the existing event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(devggn_boot())
    
