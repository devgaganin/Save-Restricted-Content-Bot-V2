<h1 align="center">
  <b>Save restricted Content Bot by <a href="https://devgagan.in"> devgagan </a> | Enterprise Release June 2024.
</h1> 
    
Contact: [Telegram](https://t.me/devggn)

---

## ENTERPRISE RELEASE INFO

**Update**: This bot is updated with login functionalities, custom rename tag adding, log group, caption changing and and many more scroll down to last to see the latest update i.e. on 18 June 2024.

### Try Live Bot based on `main` branch (my code, not on `leakrepo` branch)
Bot link - [Advance Content Saver Bot](https://t.me/advance_content_saver_bot)
---

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

## Deploying Guide - [TEAM SPY](https://t.me/devggn)

**Note** : This repository contains three branches `leakrepo` as default branch `main` as main branch and `standalone` | `main` branch codes and `standalone` branch code written by me while `leakrepo` branch code is leaked premium source.
So before deploying select branch as per your needs..

### How to get required vars
 
- API_ID and API_HASH from [telegram.org](https://my.telegram.org/auth)
- BOT_TOKEN: @Botfather on telegram
- OWNER_ID : Go to @missrose_bot on telegram and send `/info` to know your ID
- CHANNEL_ID : This will be used as Force Subscribe channel
- LOG_GROUP: Create a Group or Channel add you bot there and forward any message of that channel/group to @userinfobot to know the ID of you channel/group
- MONGO_DB: It is recommended to use your mongoDB to avoid session hacks and all
Note : You must make bot admin in both channels

### Deploy on `VPS`

Easy Method:
- Fork repo
- Go to ```config.py``` as below
- Fill variables inside the double quoted commas `""`  
- Now run following commands one by one...
```
sudo apt update
sudo apt install ffmpeg git python3-pip
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
source ~/.bashrc
nvm install v18 #nodejs 18+
git clone your_repo_link
cd you_repo_name
pip3 install -r requirements.txt
python3 -m Restriction
```

- if you want bot to be running in background then enter `screen -S gagan` before `python3 -m Restriction` 
- after `python3 -m Restriction`, click `ctrl+A`, `ctrl+D`
- if you want to stop bot, then enter `screen -r gagan` and to kill screen enter `screen -S gagan -X quit`.


## Deploy your bot on `heroku`
- Star the repo, and fork it in desktop mode
- Click on  [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
- Fill your values and click deploy ✅

## Terms of USE / Modification 
Visit [Terms](https://github.com/devgaganin/Save-Restricted-Content-Bot-Repo/blob/main/TERMS_OF_USE.md) and accept the guidelines.

# Updates

## Update: 24 June 2024

- Added `/login` method via phone number
- Session saving permanently
- Fixed old bugs
- Added /add_premium and /remove_premium along with parameters of `user_id` and `time` for the period of premium subscription.
- All old features along with `button` handler


## Contributers
My group members ... Join @devggn to know them.
Credit goes to them not to me | Special thanks to Yash for leaking this Repo

Thanks!

