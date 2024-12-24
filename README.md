<h1 align="center">
  <b>V3 branch</b> | Summer Release V2
</h1>

[Telegram](https://t.me/save_restricted_content_bots) | [See Recent Updates](https://github.com/devgaganin/Save-Restricted-Content-Bot-V2/tree/v3#updates)

---
## ABOUT THIS BRANCH
This branch is purely based on `Pyrogram V2` with more stability And this is based on forced login means user must have to login in bot to use the bot you can use `v4` branch to avoid this.

---
### **⚠️ Must Do: Configure Sensitive Variables Securely**

**Do not edit sensitive variables (e.g., `API_ID`, `API_HASH`, `BOT_TOKEN`, etc.) directly in `config.py` or any file in the repository on GitHub. Doing so can expose your credentials publicly, leading to security risks.**

### **How to Configure Variables Safely:**

1. **For VPS or Local Machine:**
   - Use a text editor like `nano` to edit the `config.py` file directly on your system:
     ```bash
     nano config.py
     ```
   - Alternatively, export your variables as environment variables:
     ```bash
     export API_ID=your_api_id
     export API_HASH=your_api_hash
     export BOT_TOKEN=your_bot_token
     ```

2. **For Cloud Deployment (e.g., Heroku, Railway):**
   - Set the variables as **Environment Variables** in the platform's settings.

3. **Using `.env` File:**
   - Create a `.env` file in the root of your project and add your variables:
     ```
     API_ID=your_api_id
     API_HASH=your_api_hash
     BOT_TOKEN=your_bot_token
     etc
     ```
   - Make sure to exclude `.env` from version control by adding it to `.gitignore`.

### **Why This is Important?**
Your credentials can be stolen if pushed to a public repository. Always keep them secure by using environment variables or local configuration files.

---

## Commands

- **`start`**: Launch the application.
- **`myplan`**: View your personalized plan.
- **`add`**: Add a new item or entry.
- **`rem`**: Remove an existing item.
- **`gcast`**: Broadcast a message or notification.
- **`stats`**: Display statistics and insights.
- **`speedtest`**: Run a network speed test.
- **`settings`**: Access and modify your settings.

## Features:

- Able to extarct the content the from private or public entities/channels/group
- direct rename and forward to channel/group/users
- Custome caption/thumbnail
- auto default thumbnail removal from videos
- Deleting/Replacing words from file name and caption
- Easy to use and deploy
- auto pin messages(if they are pinned)
- login via phone number

## Deploying Guide - [TEAM SPY](https://t.me/save_restricted_content_bots)

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
git clone your_repo_link
cd you_repo_name
pip3 install -r requirements.txt
python3 -m devgagan
```

- if you want bot to be running in background then enter `screen -S gagan` before `python3 -m devgagan` 
- after `python3 -m devgagan`, click `ctrl+A`, `ctrl+D`
- if you want to stop bot, then enter `screen -r gagan` and to kill screen enter `screen -S gagan -X quit`.


## Deploy your bot on `heroku`
- Star the repo, and fork it in desktop mode
- Click on  [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
- Fill your values and click deploy ✅

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
Visit [Terms](https://github.com/devgaganin/Save-Restricted-Content-Bot-Repo/blob/master/TERMS_OF_USE.md) and accept the guidelines.

---

## 📢 Updates

<details>
<summary><b>Update: 21 NOV 2024</b></summary>

- **Public Channels**: Removed login requirement for processing links from public channels.
- **Batch Size Limits**: New variables `FREEMIUM_LIMIT` and `PREMIUM_LIMIT` to manage batch sizes based on user type.
- **Important Note**: Set `FREEMIUM_LIMIT` to `0` to restrict link extraction.

</details>

<details>
<summary><b>Update: 20 NOV 2024</b></summary>

- **Batch Processing**: Prevents overlapping batch processes.
- **UserBot Management**: Safely stops `userbot` after all processes.
- **Bug Fixes**: Fixed issues with `userbot` stopping and overlapping processes.

</details>

<details>
<summary><b>Update: 16 NOV 2024</b></summary>

- Fixed issues with `.MOV` file handling and file renaming.
- Improved caption formatting.

</details>

<details>
<summary><b>Update: 15 NOV 2024</b></summary>

- Fixed reset button.
- Added support for topic-based groups.

</details>

<details>
<summary><b>Update: 16 AUG 2024</b></summary>

- Added `/logout` command to clear session data.
- Fixed premium membership expiration.

</details>

<details>
<summary><b>Update: 7 JULY 2024</b></summary>

- Introduced `/login` via phone number.
- Added auto-pinning of messages and other improvements.

</details>

---
## Important Note

**Note**: Changing the terms and commands doesn't magically make you a developer. Real development involves understanding the code, writing new functionalities, and debugging issues, not just renaming things. If only it were that easy!

## Contributers
My group members contact... Join @save_restricted_content_bots to know them.

Thanks!
