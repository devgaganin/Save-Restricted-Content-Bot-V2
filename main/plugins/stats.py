#from pyrogram import Client, filters  d
from .. import bot as gagan
#from .. import Bot
#from .. import FORCESUB as fs                        d
from telethon import events
from main.__main__ import botStartTime
###from config import Config               d
##from pyrogram.types.messages_and_media.message import Message                d
import random
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from time import time
import requests

##from helper_funcs.auth_user_check import AuthUserCheck                d
##from helper_funcs.force_sub import ForceSub                      d
from main.plugins.helpers import TimeFormatter,  humanbytes




@gagan.on(events.NewMessage(incoming=True, func=lambda e: e.is_private, pattern='/stats'))
async def stats(event):
    
   # duz = event.reply("...")
    currentTime = TimeFormatter((time() - botStartTime))
    osUptime = TimeFormatter((time() - boot_time()))
    total, used, free, disk= disk_usage('/')
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = humanbytes(swap.total)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = humanbytes(memory.total)
    mem_a = humanbytes(memory.available)
    mem_u = humanbytes(memory.used)
    stats = f'Bot Uptime: {currentTime}\n'\
            f'OS Uptime: {osUptime}\n'\
            f'Total Disk Space: {total}\n'\
            f'Used: {used} | Free: {free}\n'\
            f'Upload: {sent}\n'\
            f'Download: {recv}\n'\
            f'CPU: {cpuUsage}%\n'\
            f'RAM: {mem_p}%\n'\
            f'DISK: {disk}%\n'\
            f'Physical Cores: {p_core}\n'\
            f'Total Cores: {t_core}\n'\
            f'SWAP: {swap_t} | Used: {swap_p}%\n'\
            f'Memory Total: {mem_t}\n'\
            f'Memory Free: {mem_a}\n'\
            f'Memory Used: {mem_u}\n'\
            f'Powered by **__[Team SPY](https://t.me/dev_gagan)__**\n'
    
    await event.reply(f"{stats}")
   #duz.edit(stats)
