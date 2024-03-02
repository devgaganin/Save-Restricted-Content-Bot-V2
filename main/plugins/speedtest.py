#from threading import Thread   #
from time import time
#from charset_normalizer import logging
from speedtest import Speedtest
import math
#from bot.helper.ext_utils.bot_utils import get_readable_time
#from telegram.ext import CommandHandler #no
#from bot.helper.telegram_helper.filters import CustomFilters #n
#from bot import botStartTime #e
from main.__main__ import botStartTime
#from bot.helper.telegram_helper.bot_commands import BotCommands #no
#from bot.helper.telegram_helper.message_utils import auto_delete_message, sendMessage, deleteMessage, sendPhoto, editMessage  #wow
#from bot.helper.ext_utils.bot_utils import get_readable_file_size
from telethon import events
from .. import bot as gagan
from .. import Bot, AUTH, SUDO_USERS

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'


@gagan.on(events.NewMessage(incoming=True, from_users=SUDO_USERS, pattern='/speedtest'))
async def speedtest(event):
    speed = await event.reply("Running Speed Test. Wait about some secs.")  #edit telethon
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    path = (result['share'])
    currentTime = get_readable_time(time() - botStartTime)
    string_speed = f'''
╭─《 🚀 SPEEDTEST INFO 》
├ <b>Upload:</b> <code>{speed_convert(result['upload'], False)}</code>
├ <b>Download:</b>  <code>{speed_convert(result['download'], False)}</code>
├ <b>Ping:</b> <code>{result['ping']} ms</code>
├ <b>Time:</b> <code>{result['timestamp']}</code>
├ <b>Data Sent:</b> <code>{get_readable_file_size(int(result['bytes_sent']))}</code>
╰ <b>Data Received:</b> <code>{get_readable_file_size(int(result['bytes_received']))}</code>
╭─《 🌐 SPEEDTEST SERVER 》
├ <b>Name:</b> <code>{result['server']['name']}</code>
├ <b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
├ <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
├ <b>Latency:</b> <code>{result['server']['latency']}</code>
├ <b>Latitude:</b> <code>{result['server']['lat']}</code>
╰ <b>Longitude:</b> <code>{result['server']['lon']}</code>
╭─《 👤 CLIENT DETAILS 》
├ <b>IP Address:</b> <code>{result['client']['ip']}</code>
├ <b>Latitude:</b> <code>{result['client']['lat']}</code>
├ <b>Longitude:</b> <code>{result['client']['lon']}</code>
├ <b>Country:</b> <code>{result['client']['country']}</code>
├ <b>ISP:</b> <code>{result['client']['isp']}</code>
╰ <b>ISP Rating:</b> <code>{result['client']['isprating']}</code>
'''
    try:
        #pho = sendPhoto(text=string_speed, bot=context.bot, message=update.message, photo=path)  #edit
        #await bot.send_file(event.sender_id, path, caption=string_speed, parse_mode='html')
        await event.reply(string_speed,file=path,parse_mode='html')
        await speed.delete()
        #deleteMessage(context.bot, speed) #e  speed.delete
        #Thread(target=auto_delete_message, args=(context.bot, update.message, pho)).start() #r
    except Exception as g:
        print(g)
        logger.info(g)
        #logging.error(str(g))  #r
        #editMessage(string_speed, speed)
        await speed.delete()
        await event.reply(string_speed,parse_mode='html' )
        #await speed.edit(string_speed)
        #Thread(target=auto_delete_message, args=(context.bot, update.message, speed)).start() #r

def speed_convert(size, byte=True):
    if not byte: size = size / 8
    power = 2 ** 10
    zero = 0
    units = {0: "B/s", 1: "KB/s", 2: "MB/s", 3: "GB/s", 4: "TB/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

#speed_handler = CommandHandler(BotCommands.SpeedCommand, speedtest,
 #   CustomFilters.authorized_chat | CustomFilters.authorized_user)

#dispatcher.add_handler(speed_handler)
