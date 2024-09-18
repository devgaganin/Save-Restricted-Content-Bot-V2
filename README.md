<h1 align="center">
  <b>Branch V2 | Enterprise Release September 2024. </b>
</h1>

    
Contact: [Telegram](https://t.me/devgaganin)

---

## About V2 branch 

**Must Read**: This branch is an ideal branch have all practices and holding old and new functionalities together, this branch have just a difference of forced login in bot. This bot is updated with login functionalities, custom rename tag adding, log group, caption changing and and many more scroll down to last to see the latest update i.e. on 28 June 2024.

## Features:

- Able to extract the content the from private or public enntities/channels/group
- direct rename and forward to channel/group/users
- Custome caption/thumbnail
- auto default thumbnail removal from videos
- Deleting/Replacing words from file name and caption
- Easy to use and deploy
- auto pin messages(if they are pinned)
- login via phone number
- Able to download Youtube videos + 30 more sites supported via `/dl` command 

### Try Live Bot
Bot link - [CLICK HERE](https://t.me/advance_content_saver_bot)
---
A stable telegram bot to get restricted messages from group/channel/bot with custom thumbnail support , made by [TEAM SPY](https://t.me/devgaganin) This bot can run in channels directly.


## How to get vars - [TEAM SPY](https://t.me/devgaganin)

- `BOT TOKEN`: @Botfather on telegram

- `OWNER_ID`: Go to @missrose_bot, start and send /info to get your id

- `FORCESUB`: Before starting building bots create a public channel and get the username without '@'Make bot admin in that channel.

- `LOG_GROUP`: Get is by copying any post link and extract value just after `https:t.me/c/` and next `/` then after put `-100` before it. Make bot ADMIN in that channel or group.
 
- `API_ID` and `API_HASH`: [Telegram.org](https://my.telegram.org/auth)

- `MONGO_DB`: Create new mongo db it is not recommended to use the default one if you dont know how to create you can use otherwise dont use bcz it may lead to account hack/deletion through session.
- `DEFAULT_SESSION` : Generate a Pyrogram V2 session and use string for allowing users to extract without login.

## Deploying Guide - [TEAM SPY](https://t.me/devgaganin)

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
MONGODB_CONNECTION_STRING = getenv("MONGO_DB", "")
LOG_GROUP = int(getenv("LOG_GROUP", ""))
FORCESUB = getenv("FORCESUB", "")
DEFAULT_SESSION = getenv("DEFAULT_SESSION", "")
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
- Click on  [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
- Fill your values and done ✅
 
» Method - 2:
- Star the repo, rate and fork it in desktop mode
- create app in heroku
- go to settings of ```app›› reveal config vars››``` add all variables as shown above by typing their correct name and value.
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
- Fork and star the repo
- edit `config.py` same as guided for VPS deployment (you can edit on render also by filling enviroment variables)
- Go to render.com and singup/signin
- create new web service and select free plan
- connect github and your repository
- Click Deploy
- Done ✅

## Koyeb Deployment

- Fork and star the repo
- edit `config.py` same as guided for VPS deployment (you can edit on koyeb also by filling enviroment variables)
- Go to koyeb.com and singup/signin
- create new web service make sure you must choose build type `Dokerfile` because in Koyeb as a default it is checked to `buildpacks` so you have to change that.
- connect github and your repository
- Click Deploy
- Done ✅

## Terms of USE / Modification 
Visit [Terms](https://github.com/devgaganin/Save-Restricted-Content-Bot-Repo/blob/main/TERMS_OF_USE.md) and accept the guidelines.

# Updates

Last update 8 JULY 2024

### Available Commands

You can copy and paste the following commands into @BotFather:

```plaintext
start - ✅ Check if I am alive!
batch - 😎 batch method
dl - 🎞 Download videos from YouTube, Xsite, Instagram, Amazon Mini TV, Pinterest, LinkedIn, Internet Archive, etc. /dl <link>
login - login via phone number
logout - nikal be
auth - authorize users
unauth - revoke access
settings - Get all settings in a single command for rename, replace delete, setchat everything
broadcast - send message to bot users
session - generate Pyrogram V2 session
plan - 💰 Learn about premium plan details
terms - 📋 View the bot's terms and conditions
stats - 📊 Check the statistics
speedtest - 🔴 Check speed (Only for sudo users)
get - 🙃 Get a list of current users
list - 🍏 List authorized users
lock - ⚡ Add channels to the protected list to prevent extraction
help - 😧 Get command help
cancel - ❌ Cancel ongoing process
```

---

## Important Note

**Note**: Changing the terms and commands doesn't magically make you a developer. Real development involves understanding the code, writing new functionalities, and debugging issues, not just renaming things. If only it were that easy!

