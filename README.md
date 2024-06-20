<h1 align="center">
  <b>Save restricted Content Bot by <a href="https://devgagan.in"> devgagan </a> | Enterprise Release June 2024.
</h1> 
    
Contact: [Telegram](https://t.me/devggn)

---

## ENTERPRISE RELEASE INFO

**Update**: This bot is updated with login functionalities, custom rename tag adding, log group, caption changing and and many more scroll down to last to see the latest update i.e. on 18 June 2024.

## Try Live Bot
Bot link -https://t.me/advance_content_saver_bot
---
### A stable telegram bot to get restricted messages with custom thumbnail support , made by [TEAM SPY](https://t.me/devggn) This bot can run in channels directly.

- works for both public and private chats
- Custom thumbnail support for Pvt medias
- supports text and webpage media messages
- Faster speed
- Force subscribe available
- To save from bots send link in this format : `t.me/b/bot_username/message_id` (use plus messenger for message_id)
- `/batch` - (For owner only) Use this command to save upto 10000 files from a pvt or public restricted channel at once.
- `/cancel` -  Use this to stop batch
- Time delay is added to avoid FloodWait and keep user account safe.
- `/setchat` directly upload in channel or group
## Variables

- `API_ID`
- `API_HASH`
- `SESSION`
- `BOT_TOKEN` 
- `AUTH` - Owner user id
- `FORCESUB` - Public channel username without '@'. Don't forget to add bot in channel as administrator. 

## Get API & PYROGRAM:
 
API: [Telegram.org](https://my.telegram.org/auth)

PYROGRAM SESSION: Search for it ... Make sure the source be trusted otherwise it will lead to accound delete or ban

## How to get vars - [TEAM SPY](https://t.me/devggn)

BOT TOKEN: @Botfather on telegram

AUTH: Go to @missrose_bot, start and send /info to get your id

FORCESUB: Before starting building bots create a public channel and get the username without '@'

## Deploying Guide - [TEAM SPY](https://t.me/devggn)

### Deploy on `VPS`

Easy Method:
- Fork repo
- Go to main then edit ```__init__.py``` as below
- Place `#` before every `config` and after `=` write your vars in single inverted comma. see example below

```
# variables
API_ID = "1234567" #config("API_ID", default=None, cast=int)
API_HASH = "1167433546577f90e4519b65634b7" #config("API_HASH", default=None)
BOT_TOKEN = "7173773796:AAEYdIdgUg1_SYR7wSaMpgY0" #config("BOT_TOKEN", default=None)
SESSION = "BQHDMOUAIOGZHesmwkhKztZ1bU7NokB1HVLtNKHAnr35ElBp-FQ7IPkvayF0s5JoOGLN44ksi4kqeUNxnG56Vd8Mh_2Lo3ICHSN2J2u0WyYIOj96FBxN2gq_iekABQkL-vdXTB1DrOswqzBJBG9RaGPFVoiEYDAd0iD2vqgT3x2wOz98gBZNKPCGpWQYbGR6GKe66W5SRZRlLWJaEDQcTEIxNF48nIEGW7cwK2AG3eR4-iyVg5Zxaje_ACeNuCN5kLtQsNkGEV23f7-EdLQTG1zKnZ57AjUvYQdJ7o1pdGhkKknUUmOcfG4xn42RbHUwccqD1CmsGLU5Zh-vTbgBGh9AiP79HAAAAAGlHSMFAA" #config("SESSION", default=None)
FORCESUB = "channel username without @" #config("FORCESUB", default=None)
AUTH = "1234567" #config("AUTH", default=None)

```
EDIT `main/plugins/pyroplug.py`, `main/plugins/batch.py` and `main/plugins/start.py` file and fill some variables there also
1) MONGO_DB
2) OWNER_ID
3) LOG_GROUP ID with -100 after `=`

- Now run following commands one by one...

```
sudo apt update
sudo apt install ffmpeg git python3-pip
git clone your_repo_link
cd you_repo_name
pip3 install -r requirements.txt
python3 -m main
```

- if you want bot to be running in background then enter `screen -S gagan` before `python3 -m main` 
- after `python3 -m main`, click `ctrl+A`, `ctrl+D`
- if you want to stop bot, then enter `screen -r gagan` and to kill screen enter `screen -S gagan -X quit`.


## Deploy your bot on `heroku`

» Method - 1:
- Star the repo, and fork it in desktop mode
- Click on  [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
- Fill your values and done ✅
 
» Method - 2:
- Star the repo, rate and fork it in desktop mode
- create app in heroku
- go to settings of ```app›› config vars››``` add all variables
- add buildpacks i.e. `python` and `https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git`
- connect to github and deploy
- turn on dynos
- Note: you must add buildpack in heroku to get the original video thumbnail and to remove already set thumbnail otherwise you will get black video
<b> How to add? </b>
- Go to heroku settings
- scroll down and click add buildpack
- now paste following link i.e `https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git` in input bar and click add buildpack
- Now go back and redeploy

## Editing Repo - [TEAM SPY](https://t.me/devggn)

You can freely edit repo the customisation you can do is -
- Change command pattern like `/batch` to other name (edit this in ```main/plugins/batch.py```) by searching and replacing `/batch` to desired command.
- Adding Custom Text in caption (edit this in ```main/plugins/pyroplug.py```) search for 
```
caption = f"{msg.caption}\n\n__Unrestricted by **[Team SPY](https://t.me/devggn)**__" if msg.caption else "__Unrestricted by **[Team SPY](https://t.me/devggn)**__"
``` 
change accordingly within ```f""```

- Change Start pic and text (edit this in ```main/plugins/start.py```) search for ```TEXT=```, ```START_PIC=``` and then edit those after ```=```
- Change Default thumbnail in main directory there is file named ```thumb.jpg``` remove that and upload your custom ```thumb.jpg```
- Change cancel command (edit this also in ```batch.py```) search for ```/cancel``` and then change the command accordingly

## Terms of USE / Modification 
Visit [Terms](https://github.com/devgaganin/Save-Restricted-Content-Bot-Repo/blob/main/TERMS_OF_USE.md) and accept the guidelines.

# Updates

## Update: 20 June 2024

Added remaining variables direct input from `env` no need to edit the `batch.py`, `pyroplug.py`, `start.py` when working with environment based deployer

## Update: 18 June 2024

This release introduces enterprise-level features with advanced authentication logic, empowering users with the `/auth` and `/unauth` commands.

### New Features

- **Login Functionality**: User can add their session via `/addsession SESSION` command to extract without links.
- **Custom Rename**: Set custom filenames using the `/setrename` command.
- **Custom Caption**: Define personalized captions with the `/setcaption` command.
- **Delete Functionality**: Remove unwanted words from filenames and captions via the `/delete` command.
- **Word Replacer**: Replace specific words in captions using the `/replace 'OLD_WORD', 'NEW_WORD'` command.
- **Broadcast**: Send messages to all users using the `/broadcast MESSAGE` command.
- **Batch Processing**: Two modes available, `/bulk` and `/batch`, for efficient batch operations.
- **User Bot Login**: The `pro` method allows saving restricted pictures from DMs or bots.
- **Multiple Hosting**: The `/host` method allows to host many bot in a single process.

&&&&& and many more have a look below 

### Available Commands

You can copy and paste the following commands into @BotFather:

```plaintext
start - ✅ Check if I am alive!
bulk - ☠ V1 batch method
batch - 😎 V2 batch method
dl - 🎞 Download videos from YouTube, Xsite, Instagram, Amazon Mini TV, Pinterest, LinkedIn, Internet Archive, etc. /dl <link>
auth - authorize users
unauth - revoke access
broadcast - send message to bot users
addsession - 🔗 Add your own session to extract without an invite link
set - 👉 Basic settings
remthumb - ❌ Remove saved thumbnail
setchat - 📡 For channel or group forwarding
setcaption - 🖊️ Set your custom caption (Pro plan)
setrename - 🔄 Add text and rename file (Pro plan)
replace - 🖋️ Replace words in captions
delete - 🥳 Prevent a word from appearing in filenames and captions
plan - 💰 Learn about premium plan details
terms - 📋 View the bot's terms and conditions
stats - 📊 Check the statistics
speedtest - 🔴 Check speed (Only for sudo users)
logout - 🚪 Delete session and logout
get - 🙃 Get a list of current users
list - 🍏 List authorized users
lock - ⚡ Add channels to the protected list to prevent extraction
pro - 💎 Add session to save restricted files from private chats/bots
noob - 😭 Delete the Pro activation
host - ☁️ Host your own SRC Bot
unhost - 🌨️ Unhost the SRC and FWD Bot
help - 😧 Get command help
cancel - ❌ Cancel ongoing process
```

---

## Important Note

**Note**: Changing the terms and commands doesn't magically make you a developer. Real development involves understanding the code, writing new functionalities, and debugging issues, not just renaming things. If only it were that easy!

