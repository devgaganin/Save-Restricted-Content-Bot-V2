# Join me @dev_gagan

import logging
import time
import os
from flask import Flask
from threading import Thread

# Logging setup
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)

botStartTime = time.time()

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Successfully deployed! Bot Deployed: Team SPY"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Start the Flask web server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    # Import and start the bot
    from . import bot
    import glob
    from pathlib import Path
    from main.utils import load_plugins
    
    path = "main/plugins/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem
            load_plugins(plugin_name.replace(".py", ""))
    
    logger.info("Bot Started :)")
    # Run the bot
    bot.run_until_disconnected()
  
