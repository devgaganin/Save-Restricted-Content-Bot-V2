<h1 align="center">
  <b>Save restricted Content Bot by <a href="https://devgagan.in"> devgagan </a> | Enterprise Release June 2024.
</h1> 
    
Contact: [Telegram](https://t.me/devggn)

---

## ENTERPRISE RELEASE INFO

**Update**: This bot is updated with login functionalities, custom rename tag adding, log group, caption changing and and many more scroll down to last to see the latest update i.e. on 28 June 2024.

### Try Live Bot
Bot link - [CLICK HERE](https://t.me/advance_content_saver_bot)
---
A stable telegram bot to get restricted messages from group/channel/bot with custom thumbnail support , made by [TEAM SPY](https://t.me/devggn) This bot can run in channels directly.


## How to get vars - [TEAM SPY](https://t.me/devggn)

- `BOT TOKEN`: @Botfather on telegram

- `OWNER_ID`: Go to @missrose_bot, start and send /info to get your id

- `FORCESUB`: Before starting building bots create a public channel and get the username without '@'Make bot admin in that channel.

- `LOG_GROUP`: Get is by copying any post link and extract value just after `https:t.me/c/` and next `/` then after put `-100` before it. Make bot ADMIN in that channel or group.
 
- `API_ID` and `API_HASH`: [Telegram.org](https://my.telegram.org/auth)

- `PYROGRAM_V2_SESSION`: Search for it ... Make sure the source be trusted otherwise it will lead to accound delete or ban

- `MONGO_DB`: Create new mongo db it is not recommended to use the default one if you dont know how to create you can use otherwise dont use bcz it may lead to account hack/deletion through session.

## Deploying Guide - [TEAM SPY](https://t.me/devggn)

### Deploy on `VPS`

Easy Method:
- Fork and star the repo
- Go to main then edit ```config.py``` as below
- Put respective values in `""` and save.

```
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = int(getenv("OWNER_ID", ""))
MONGODB_CONNECTION_STRING = getenv("MONGO_DB", "mongodb+srv://ggn:ggn@ggn.upuljx5.mongodb.net/?retryWrites=true&w=majority&appName=ggn")
LOG_GROUP = int(getenv("LOG_GROUP", ""))
SESSION = getenv("PYROGRAM_V2_SESSION", "")
FORCESUB = getenv("FORCESUB", "")
```

- Now run following commands one by one...

```
sudo apt update
sudo apt install ffmpeg git python3-pip
git clone your_repo_link
cd you_repo_name
pip3 install -r requirements.txt
python3 -m ggn
```

- if you want bot to be running in background then enter `screen -S gagan` before `python3 -m ggn` 
- after `python3 -m ggn`, click `ctrl+A`, `ctrl+D`
- if you want to stop bot, then enter `screen -r gagan` and to kill screen enter `screen -S gagan -X quit`.


## Deploy your bot on `heroku`

» Method - 1:
- Star the repo, and fork it in desktop mode
- Click on  [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/devgaganin/Save-Restricted-Content-Bot-Repo/)
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

## Deploy on Render
see following tutorial 👇
https://t.me/save_restricted_content_bots/759

## Koyeb Deployment

Just select repo and do build by dockerfile 

## Terms of USE / Modification 
Visit [Terms](https://github.com/devgaganin/Save-Restricted-Content-Bot-Repo/blob/main/TERMS_OF_USE.md) and accept the guidelines.

# Updates

## Update: 28 June 2024
- New fresh files uploaded by fixing old errors for ex. `float division by zero` for know filetypes / `peer_id invalid` for some chats not all
- VPS Deployment guide updated
Removed unwanted behaviour of MONGO_DB
- Permanent session storage
- Removed bunches of commands handlers and merged them in button format under a single command `/settings`.

  
- Note: I can add the phone based login but it may lead to account ban that's why I prefer SESSION based login. If you want phone number based login try `leakrepo` branch of this repository.

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
batch - 😎 batch method
dl - 🎞 Download videos from YouTube, Xsite, Instagram, Amazon Mini TV, Pinterest, LinkedIn, Internet Archive, etc. /dl <link>
auth - authorize users
unauth - revoke access
settings - Get all settings in a single command for rename, replace delete, setchat everything
broadcast - send message to bot users
plan - 💰 Learn about premium plan details
terms - 📋 View the bot's terms and conditions
stats - 📊 Check the statistics
speedtest - 🔴 Check speed (Only for sudo users)
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

