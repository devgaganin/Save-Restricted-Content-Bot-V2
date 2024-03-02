#Github.com/devgaganin

from pyrogram.errors import FloodWait, InviteHashInvalid, InviteHashExpired, UserAlreadyParticipant
from telethon import errors, events

import asyncio, subprocess, re, os, time
from pathlib import Path
from datetime import datetime as dt
import math
import cv2

from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)


#to get width, height and duration(in sec) of a video
def video_metadata(file):
    vcap = cv2.VideoCapture(f'{file}')
    width = round(vcap.get(cv2.CAP_PROP_FRAME_WIDTH ))
    height = round(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT ))
    fps = vcap.get(cv2.CAP_PROP_FPS)
    frame_count = vcap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = round(frame_count / fps)
    return {'width' : width, 'height' : height, 'duration' : duration }

#Join private chat-------------------------------------------------------------------------------------------------------------

async def join(client, invite_link):
    try:
        await client.join_chat(invite_link)
        return "Successfully joined the Channel"
    except UserAlreadyParticipant:
        return "User is already a participant."
    except (InviteHashInvalid, InviteHashExpired):
        return "Could not join. Maybe your link is expired or Invalid."
    except FloodWait:
        return "Too many requests, try again later."
    except Exception as e:
        print(e)
        return f"{e} \nCould not join, try joining manually."
    
    
    
#----------------------------------
async def force_sub(client, channel, id, ft):
    s, r = False, None
    try:
        x = await client(GetParticipantRequest(channel=channel, participant=int(id)))
        left = x.stringify()
        s, r = (True, ft) if 'left' in left else (False, None)
    except UserNotParticipantError:
        s, r = True, f"To use this bot you've to join @{channel}."
    except Exception:
        s, r = True, "ERROR: Add in ForceSub channel, or check your channel id."
    return s, r

#------------------------------
def TimeFormatter(milliseconds) -> str:
    milliseconds = int(milliseconds) * 1000
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)}d, " if days else "")
        + (f"{str(hours)}h, " if hours else "")
        + (f"{str(minutes)}m, " if minutes else "")
        + (f"{str(seconds)}s, " if seconds else "")
        + (f"{str(milliseconds)}ms, " if milliseconds else "")
    )
    return tmp[:-2]

#--------------------------------------------
def humanbytes(size):
    size = int(size)
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return f"{str(round(size, 2))} {Dic_powerN[n]}B"


#Regex---------------------------------------------------------------------------------------------------------------
#to get the url from event

def get_link(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)
    try:
        return link if (link := [x[0] for x in url][0]) else False
    except Exception:
        return False
    
#Screenshot---------------------------------------------------------------------------------------------------------------

def hhmmss(seconds):
    return time.strftime('%H:%M:%S',time.gmtime(seconds))

async def screenshot(video, duration, sender):
    if os.path.exists(f'{sender}.jpg'):
        return f'{sender}.jpg'
    time_stamp = hhmmss(int(duration)/2)
    out = dt.now().isoformat("_", "seconds") + ".jpg"
    cmd = ["ffmpeg",
           "-ss",
           f"{time_stamp}", 
           "-i",
           f"{video}",
           "-frames:v",
           "1", 
           f"{out}",
           "-y"
          ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    x = stderr.decode().strip()
    y = stdout.decode().strip()
    if os.path.isfile(out):
        return out
    else:
        None       
