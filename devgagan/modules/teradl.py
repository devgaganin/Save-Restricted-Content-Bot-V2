import os
import time
import logging
import asyncio
import subprocess
import cv2
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters, enums
import asyncio
import re
import aiohttp
from devgagan.core.func import *
from devgagan import app
from config import LOG_GROUP
from tera import session_string, allowed_groups, owner_id, extract_links, LOG_GROUP, my_cookie, my_headers

logging.basicConfig(level=logging.INFO)

# Initialize a session with the provided cookies and headers
my_session = aiohttp.ClientSession(cookies=my_cookie, headers=my_headers)

async def get_formatted_size_async(size_bytes):
    try:
        size_bytes = int(size_bytes)
        size = size_bytes / (1024 * 1024) if size_bytes >= 1024 * 1024 else (
            size_bytes / 1024 if size_bytes >= 1024 else size_bytes
        )
        unit = "MB" if size_bytes >= 1024 * 1024 else ("KB" if size_bytes >= 1024 else "bytes")

        return f"{size:.2f} {unit}"
    except Exception as e:
        print(f"Error getting formatted size: {e}")
        return None


async def is_valid_url_async(url):
    try:
        async with my_session.get(url) as response:
            return response.status == 200
    except Exception as e:
        return False


async def check_url_patterns_async(url):
    patterns = [
        r"ww\.mirrobox\.com",
        r"www\.nephobox\.com",
        r"freeterabox\.com",
        r"www\.freeterabox\.com",
        r"1024tera\.com",
        r"4funbox\.co",
        r"www\.4funbox\.com",
        r"mirrobox\.com",
        r"nephobox\.com",
        r"terabox\.app",
        r"terabox\.com",
        r"www\.terabox\.ap",
        r"terabox\.fun",
        r"www\.terabox\.com",
        r"www\.1024tera\.co",
        r"www\.momerybox\.com",
        r"teraboxapp\.com",
        r"momerybox\.com",
        r"tibibox\.com",
        r"www\.tibibox\.com",
        r"www\.teraboxapp\.com",
    ]

    if not await is_valid_url_async(url):
        return False

    for pattern in patterns:
        if re.search(pattern, url):
            return True
    return False


async def find_between(string, start, end):
    start_index = string.find(start) + len(start)
    end_index = string.find(end, start_index)
    return string[start_index:end_index]


async def fetch_download_link_async(url):
    try:
        async with my_session.get(url) as response:
            response.raise_for_status()
            response_data = await response.text()

            js_token = await find_between(response_data, 'fn%28%22', '%22%29')
            log_id = await find_between(response_data, 'dp-logid=', '&')

            if not js_token or not log_id:
                return None

            request_url = str(response.url)
            surl = request_url.split('surl=')[1]
            params = {
                'app_id': '250528',
                'web': '1',
                'channel': 'dubox',
                'clienttype': '0',
                'jsToken': js_token,
                'dplogid': log_id,
                'page': '1',
                'num': '20',
                'order': 'time',
                'desc': '1',
                'site_referer': request_url,
                'shorturl': surl,
                'root': '1'
            }

            async with my_session.get('https://www.1024tera.com/share/list', params=params) as response2:
                response_data2 = await response2.json()
                print("res2", response_data2)
                if 'list' not in response_data2:
                    return None
                if response_data2['list'][0]['isdir'] == "1":
                    params.update({
                        'dir': response_data2['list'][0]['path'],
                        'order': 'asc',
                        'by': 'name',
                        'dplogid': log_id
                    })
                    params.pop('desc')
                    params.pop('root')
                    async with my_session.get('https://www.1024tera.com/share/list', params=params) as response3:
                        response_data3 = await response3.json()
                        print("res3", response_data3)
                        if 'list' not in response_data3:
                            return None
                        return response_data3['list']
                return response_data2['list']

    except aiohttp.ClientResponseError as e:
        print(f"Error fetching download link: {e}")
        return None

# Function to download using aria2c and get downloaded file path
async def download_with_aria2c(download_link, output_filename):
    try:
        process = await asyncio.create_subprocess_exec(
            'aria2c', '-x', '16', '-s', '16', '-o', output_filename, download_link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            downloaded_file = os.path.join(os.getcwd(), output_filename)
            
            # Add @devggn to the filename without changing the extension
            new_filename = os.path.splitext(downloaded_file)[0] + '@devggn' + os.path.splitext(downloaded_file)[1]
            os.rename(downloaded_file, new_filename)
            
            # Assign new filename to downloaded_file variable
            downloaded_file = new_filename
            
            return downloaded_file
        else:
            logging.error(f"aria2c process returned non-zero exit code: {process.returncode}")
            logging.error(f"aria2c stdout: {stdout.decode()}")
            logging.error(f"aria2c stderr: {stderr.decode()}")
            return None
    except Exception as e:
        logging.error(f"Error downloading with aria2c: {e}")
        return None

# Function to send video or message back to user
async def send_video_or_message_to_user(chat_id, file_path, caption):
    try:
        if file_path.endswith((".mp4", ".mkv", ".webm", ".avi", ".flv", ".mov", ".wmv", ".ts")):
            metadata = video_metadata(file_path)
            thumb_path = "thumb.jpg"
            await app.send_video(chat_id, video=file_path, thumb=thumb_path, caption=caption)
        elif file_path.endswith((".jpg", ".png", ".ttf")):
            await app.send_photo(chat_id, photo=file_path, caption=caption)
        else:
            thumb_path = "logo.jpg"
            await app.send_document(chat_id, document=file_path, thumb=thumb_path, caption=caption)
        
        os.remove(file_path)
        return True
    except Exception as e:
        logging.error(f"Error sending video or message to user: {e}")
        return False

@app.on_message(filters.command("ping"))
async def ping(client, message):
    if str(message.from_user.id) != owner_id:
        return
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    start_time = time.time()
    sent_message = await message.reply_text("Pong!", quote=True)
    end_time = time.time()
    time_taken = end_time - start_time
    await sent_message.edit_text(f"Pong!\nTime Taken: {time_taken:.2f} seconds")

async def format_message(link_data):
    file_name = link_data["server_filename"]
    file_size = await get_formatted_size_async(link_data["size"])
    download_link = link_data["dlink"]
    return f"┎ <b>Title</b>: `{file_name}`\n┠ <b>Size</b>: `{file_size}`\n┖ <b>Link</b>: <a href={download_link}>Link</a>"

@app.on_message(filters.command("tera"))
async def link_handler(client, message):
    if message.chat.type.value != "private" and str(message.chat.id) not in allowed_groups:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await message.reply_text("⚠️ Forbidden! For groups access.\nContact @devggn", quote=True)
        return

    # Extract the URL from the command
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) < 2:
        return  # Do nothing if no URL is provided

    url = command_parts[1].strip()

    # Original regex pattern for URL validation
    pattern = r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
    if not re.match(pattern, url):
        return  # Do nothing if the URL doesn't match the pattern

    try:
        start_time = time.time()

        # Check URL pattern (replace with your custom function if needed)
        if not await check_url_patterns_async(url):
            return  # Do nothing if the URL pattern isn't valid for processing

        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        process_url = await message.reply_text("🔎 Processing URL...", quote=True)
        link_data = await fetch_download_link_async(url)

        end_time = time.time()
        time_taken = end_time - start_time
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)

        link_message = "\n\n".join([await format_message(link) for link in link_data])
        download_message = (
            f"🔗 <b>Link Bypassed!</b>\n\n{link_message}\n\n<b>Time Taken</b>: {time_taken:.2f} seconds"
        )
        await process_url.edit_text(download_message)

        if link_data:
            download_link = link_data[0]["dlink"]
            title = link_data[0].get("server_filename", "file")
            output_filename = title
            downloading_message = await message.reply_text("📥 Downloading...", quote=True)
            downloaded_file = await download_with_aria2c(download_link, output_filename)
            await downloading_message.delete()

            if downloaded_file:
                uploading_message = await message.reply_text("📤 Uploading...", quote=True)
                caption = link_data[0]["server_filename"]
                result = await send_video_or_message_to_user(message.chat.id, downloaded_file, caption)
                await result.copy(LOG_GROUP)
                await uploading_message.delete()
                await message.reply_text("✅ File uploaded!", quote=True)
            else:
                await message.reply_text("❌ Failed to download.", quote=True)

    except Exception as e:
        pass  # Do nothing if an error occurs
