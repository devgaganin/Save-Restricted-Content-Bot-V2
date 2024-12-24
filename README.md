<h1 align="center">
  <b>V3 branch</b> | Summer Release V2
</h1>

[Telegram](https://t.me/save_restricted_content_bots) | [See Recent Updates](https://github.com/devgaganin/Save-Restricted-Content-Bot-V2/tree/v3#updates)



## 📚 About This Branch
This branch is based on `Pyrogram V2` offering enhanced stability and a forced login feature. Users must log in to use the bot. For no-login usage, consider the `v4` branch.

### ⚠️ Must Do: Secure Your Sensitive Variables

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

---

## ⚡ Commands

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

## 🔧 Features
- Extract content from both public and private channels/groups.
- Rename and forward content to other channels or users.
- Custom captions and thumbnails.
- Auto-remove default video thumbnails.
- Delete or replace words in filenames and captions.
- Auto-pin messages if enabled.
- Login via phone number.
- **Supports 4GB file uploads**: The bot can handle large file uploads, up to 4GB in size.
- **Enhanced Timer**: Distinct timers for free and paid users to limit usage and improve service.
- **Improved Looping**: Optimized looping for processing multiple files or links, reducing delays and enhancing performance.
- **Premium Access**: Premium users enjoy faster processing speeds and priority queue management.

---
## ⚙️ Required Variables (see collect before deployment)

<details>
<summary><b>Click to view required variables</b></summary>

To run the bot, you'll need to configure a few sensitive variables. Here's how to set them up securely:

- **`API_ID`**: Your API ID from [telegram.org](https://my.telegram.org/auth).
- **`API_HASH`**: Your API Hash from [telegram.org](https://my.telegram.org/auth).
- **`BOT_TOKEN`**: Get your bot token from [@BotFather](https://t.me/botfather).
- **`OWNER_ID`**: Use [@missrose_bot](https://t.me/missrose_bot) to get your user ID by sending `/info`.
- **`CHANNEL_ID`**: The ID of the channel for forced subscription.
- **`LOG_GROUP`**: A group or channel where the bot logs messages. Forward a message to [@userinfobot](https://t.me/userinfobot) to get your channel/group ID.
- **`MONGO_DB`**: A MongoDB URL for storing session data (recommended for security).
  
### Additional Configuration Options:
- **`PREMIUM_SESSION`**: (Optional) Add your **premium account session string** here to allow 4GB file uploads. This is **optional** and can be left empty if not used.
- **`FREEMIUM_LIMIT`**: Default is `0`. Set this to any value you want to allow free users to extract content. If set to `0`, free users will not have access to any extraction features.
- **`PREMIUM_LIMIT`**: Default is `500`. This is the batch limit for premium users. You can customize this to allow premium users to process more links/files in one batch.

### Monetization (Optional):
- **`WEBSITE_URL`**: (Optional) This is the domain for your monetization short link service. Provide the shortener's domain name, for example: `upshrink.com`. Do **not** include `www` or `https://`. The default link shortener is already set.
- **`AD_API`**: (Optional) The API key from your link shortener service (e.g., **Upshrink**, **AdFly**, etc.) to monetize links. Enter the API provided by your shortener.

> **Important:** Always keep your credentials secure! Never hard-code them in the repository. Use environment variables or a `.env` file.

</details>

---

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

## Updates

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
## 🛠️ Terms of Use

Visit the [Terms of Use](https://github.com/devgaganin/Save-Restricted-Content-Bot-Repo/blob/master/TERMS_OF_USE.md) page to review and accept the guidelines.
## Important Note

**Note**: Changing the terms and commands doesn't magically make you a developer. Real development involves understanding the code, writing new functionalities, and debugging issues, not just renaming things. If only it were that easy!

## Contributers
My group members contact... Join @save_restricted_content_bots to know them.

Thanks!
