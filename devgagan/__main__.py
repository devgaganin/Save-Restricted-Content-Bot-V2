#devggn


import asyncio
import importlib
from pyrogram import idle
from devgagan.modules import ALL_MODULES

 

loop = asyncio.get_event_loop()


async def terima_ki_choot():
    for all_module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + all_module)
    print("»»»» Bot deployed ... ✨ 🎉")
    await idle()
    print("»» Stopped....")


if __name__ == "__main__":
    loop.run_until_complete(terima_ki_choot())
