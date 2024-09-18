import sys
from pyrogram import Client
from telethon.sync import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, DEFAULT_SESSION

# Initialize uvloop if you plan to use it
# import uvloop
# uvloop.install()

device = "Telegram Android 10.11.1"

# Module-level variables for the clients
Bot = None
modi = None
sigma = None
defaultbot = None
bot = None

# Function to start Pyrogram clients
def start_pyrogram_client(name, bot_token, api_id, api_hash, device, max_concurrent_transmissions=20):
    try:
        client = Client(
            name,
            bot_token=bot_token,
            api_id=int(api_id),
            api_hash=api_hash,
            device_model=device,
            sleep_threshold=20,
            max_concurrent_transmissions=max_concurrent_transmissions,
            workers=50 if name == "clientone" else 10  # Customize workers for 'clientone'
        )
        client.start()
        return client
    except Exception as e:
        print(f"Error starting Pyrogram client {name}: {e}")
        sys.exit(1)

# Function to start Telethon clients
def start_telethon_client(name, api_id, api_hash, bot_token=None):
    try:
        if bot_token:
            client = TelegramClient(name, api_id, api_hash).start(bot_token=bot_token)
        else:
            client = TelegramClient(name, api_id, api_hash)
        return client
    except Exception as e:
        print(f"Error starting Telethon client {name}: {e}")
        sys.exit(1)


# Function to start the defaultbot using session string
def start_defaultbot(session_string, api_id, api_hash):
    try:
        client = Client(
            "defaultbot",
            api_id=int(api_id),
            api_hash=api_hash,
            session_string=session_string
        )
        client.start()
        return client
    except Exception as e:
        print(f"Error starting defaultbot: {e}")
        sys.exit(1)
        
# Start all clients
def start_all_clients():
    global Bot, modi, sigma, defaultbot, bot  # Access global variables

    # Start Pyrogram clients
    Bot = start_pyrogram_client("clientone", BOT_TOKEN, API_ID, API_HASH, device, 20)
    modi = start_pyrogram_client("modiji", BOT_TOKEN, API_ID, API_HASH, device, 10)
    sigma = start_pyrogram_client("sigma", BOT_TOKEN, API_ID, API_HASH, device, 10)
    defaultbot = start_defaultbot(DEFAULT_SESSION, API_ID, API_HASH)

    # Start Telethon clients
    bot = start_telethon_client('sexypne', API_ID, API_HASH, BOT_TOKEN)

# Initialize clients when the module is imported
start_all_clients()
        
