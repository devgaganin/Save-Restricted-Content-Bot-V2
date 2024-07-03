import asyncio

from .bot import start_clients, madarchod_bot, stop_clients, terima_ki_choot

async def main():
    await start_clients()
    await madarchod_bot()
    await terima_ki_choot()

def run_bot():
    asyncio.run(main())
