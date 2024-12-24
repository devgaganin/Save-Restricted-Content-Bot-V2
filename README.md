<h1 align="center">
  <b>V3 branch</b> | Summer Release V2
</h1>

[Telegram](https://t.me/save_restricted_content_bots) | [See Recent Updates](https://github.com/devgaganin/Save-Restricted-Content-Bot-V2/tree/v3#updates)

---

---

## 📚 About This Branch
This branch is based on `Pyrogram V2` offering enhanced stability and a forced login feature. Users must log in to use the bot. For no-login usage, consider the `v4` branch.

---

<details>
<summary><b>⚠️ Must Do: Secure Your Sensitive Variables</b></summary>

**Do not expose sensitive variables (e.g., `API_ID`, `API_HASH`, `BOT_TOKEN`) on GitHub. Use environment variables to keep them secure.**

### Configuring Variables Securely:

- **On VPS or Local Machine:**
  - Use a text editor to edit `config.py`:
    ```bash
    nano config.py
    ```
  - Alternatively, export as environment variables:
    ```bash
    export API_ID=your_api_id
    export API_HASH=your_api_hash
    export BOT_TOKEN=your_bot_token
    ```

- **For Cloud Platforms (Heroku, Railway, etc.):**
  - Set environment variables directly in your platform’s dashboard.

- **Using `.env` File:**
  - Create a `.env` file and add your credentials:
    ```
    API_ID=your_api_id
    API_HASH=your_api_hash
    BOT_TOKEN=your_bot_token
    ```
  - Make sure to add `.env` to `.gitignore` to prevent it from being pushed to GitHub.

**Why This is Important?**
Your credentials can be stolen if pushed to a public repository. Always keep them secure by using environment variables or local configuration files.

</details>

---
## ⚡ Commands

<details>
<summary><b>List of Commands</b></summary>

- **`start`**: 🚀 Start the bot.
- **`batch`**: 🫠 Extract in bulk.
- **`login`**: 🔑 Get into the bot.
- **`logout`**: 🚪 Get out of the bot.
- **`token`**: 🎲 Get 3 hours of free access.
- **`adl`**: 👻 Download audio from 30+ sites.
- **`dl`**: 💀 Download videos from 30+ sites.
- **`transfer`**: 💘 Gift premium to others.
- **`myplan`**: ⌛ Get your plan details.
- **`add`**: ➕ Add user to premium.
- **`rem`**: ➖ Remove user from premium.
- **`session`**: 🧵 Generate Pyrogramv2 session.
- **`settings`**: ⚙️ Personalize settings.
- **`stats`**: 📊 Get stats of the bot.
- **`plan`**: 🗓️ Check our premium plans.
- **`terms`**: 🥺 Terms and conditions.
- **`speedtest`**: 🚅 Check the server speed.
- **`get`**: 🗄️ Get all user IDs.
- **`lock`**: 🔒 Protect channel from extraction.
- **`gcast`**: ⚡ Broadcast message to bot users.
- **`help`**: ❓ Help if you're new.
- **`cancel`**: 🚫 Cancel batch process.

</details>
---
## Features:

- Able to extarct the content the from private or public entities/channels/group
- direct rename and forward to channel/group/users
- Custome caption/thumbnail
- auto default thumbnail removal from videos
- Deleting/Replacing words from file name and caption
- Easy to use and deploy
- auto pin messages(if they are pinned)
- login via phone number

## 🚀 Deployment Guide

<details>
<summary><b>Deploy on VPS</b></summary>

1. Fork the repo.
2. Update `config.py` with your values.
3. Run the following:
   ```bash
   sudo apt update
   sudo apt install ffmpeg git python3-pip
   git clone your_repo_link
   cd your_repo_name
   pip3 install -r requirements.txt
   python3 -m devgagan
   ```

- To run the bot in the background:
  ```bash
  screen -S gagan
  python3 -m devgagan
  ```
  - Detach: `Ctrl + A`, then `Ctrl + D`
  - To stop: `screen -r gagan` and `screen -S gagan -X quit`

</details>

<details>
<summary><b>Deploy on Heroku</b></summary>

1. Fork and Star the repo.
2. Click [Deploy on Heroku](https://heroku.com/deploy).
3. Enter required variables and click deploy ✅.

</details>

<details>
<summary><b>Deploy on Render</b></summary>

1. Fork and star the repo.
2. Edit `config.py` or set environment variables on Render.
3. Go to [render.com](https://render.com), sign up/log in.
4. Create a new web service, select the free plan.
5. Connect your GitHub repo and deploy ✅.

</details>

<details>
<summary><b>Deploy on Koyeb</b></summary>

1. Fork and star the repo.
2. Edit `config.py` or set environment variables on Koyeb.
3. Create a new service, select `Dockerfile` as build type.
4. Connect your GitHub repo and deploy ✅.

</details>

---


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
