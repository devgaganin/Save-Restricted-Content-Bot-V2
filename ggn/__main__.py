#devggn

import logging
import time
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)

botStartTime = time.time()

if __name__ == "__main__":
    from . import bot
    import glob
    from pathlib import Path
    from ggn.importer import load_plugins
    
    path = "ggn/assets/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem
            load_plugins(plugin_name.replace(".py", ""))

    logger.info("Bot Started :)")
    print("\033[31m  ____  \033[33m_____ \033[32m_    _ \033[34m ____ \033[35m ____ \033[36m _   _ ")
    print("\033[31m |  _ \ \033[33m| ____|\033[32m |  | |\033[34m/ ___|\033[35m|  _ \ \033[36m| \ | |")
    print("\033[31m | | | |\033[33m  _|  |\033[32m |  | |\033[34m |  _ |\033[35m | | | |\033[36m  \| |")
    print("\033[31m | |_| |\033[33m| |___|\033[32m |__| |\033[34m |_| |\033[35m |_| |\033[36m |\  |")
    print("\033[31m |____/ \033[33m|_____|\033[32m\____/ \033[34m\____|\033[35m|____/ \033[36m|_| \_|")
    print("\033[0m")
    
    bot.run_until_disconnected()
