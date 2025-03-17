<h1 align="center">
  Winter Release v3
</h1>

# Important Note : 
- New repo link : https://github.com/devgaganin/Save-Restricted-Content-Bot-v3/tree/main
- the every branch of this repo have uniques features and all are working branches so you can migrate and test from `v1` to `v4` the `v3` is more advance than all
- thanks continue fork and edit


[Telegram](https://t.me/save_restricted_content_bots) | [See Recent Updates](https://github.com/devgaganin/Save-Restricted-Content-Bot-V2/tree/v3#updates)

### Star the repo it motivate us to update new features
see our live bot kn telegram to check the features [Advance Content Saver Bot](https://t.me/advance_content_saver_bot)

## 📚 About This Branch
- This branch is based on `Pyrogram V2` offering enhanced stability and a forced login feature. User are not forced to login in bot for public channels but for public groups and private channel they have to do login.
- for detailed features scroll down to features section

---

## 🔧 Features
- Extract content from both public and private channels/groups.
- Rename and forward content to other channels or users.
- extract restricted content from other bots how to use format link like `https://b/botusername(without @)/message_id(get it from plus messenger)`
- `/login` method along with `session` based login
- Custom captions and thumbnails.
- Auto-remove default video thumbnails.
- Delete or replace words in filenames and captions.
- Auto-pin messages if enabled.
- download yt/insta/Twitter/fb ect normal ytdlp supported sites that supports best format
- Login via phone number.
- **Supports 4GB file uploads**: The bot can handle large file uploads, up to 4GB in size.
- file splitter if not premium string
- **Enhanced Timer**: Distinct timers for free and paid users to limit usage and improve service.
- **Improved Looping**: Optimized looping for processing multiple files or links, reducing delays and enhancing performance.
- **Premium Access**: Premium users enjoy faster processing speeds and priority queue management.
- ads setup shorlink ads token system
- fast uploader via `SpyLib` using Telethon modules and `mautrix bridge repo`
- Directly upload to `topic` in any topic enabled group

  
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


## ⚙️ Required Variables

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
- **`STRING`**: (Optional) Add your **premium account session string** here to allow 4GB file uploads. This is **optional** and can be left empty if not used.
- **`FREEMIUM_LIMIT`**: Default is `0`. Set this to any value you want to allow free users to extract content. If set to `0`, free users will not have access to any extraction features.
- **`PREMIUM_LIMIT`**: Default is `500`. This is the batch limit for premium users. You can customize this to allow premium users to process more links/files in one batch.
- **`YT_COOKIES`**: Yt cookies for downloading yt videos 
- **`INSTA_COOKIES`**: If you want to enable instagram downloading fill cookiesn

**How to get cookies ??** : use mozila firfox if on android or use chrome on desktop and download extension get this cookie or any Netscape Cookies (HTTP Cookies) extractor and use that 

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

## Updates
<details>
<summary><b>Update: 14 Feb 2025</b></summary>
  Removed forced `login` user now can proceed with invite link if they do not want to login in bot due security concerns, BOT OWNER must have to fill `DEFAULT_SESSION` var when deploying.
  done ✅
</details>
  
<details>
<summary><b>Update: 1 Feb 2025</b></summary>
  
- Added support to upload in `topics` (in group)
- seperated function from direct loop of `get_msg` and `copy_message_with_chat_id` function
- & some more advancements 
  
</details>
<details>
<summary><b>Update: 22 Jan 2025</b></summary>
  
- Added public user ID or channel story downloader support (see our tutorial for this how to save) 
- Renaming made asynchronous
- added support for `tg://openmessage` type link for bots and users (see tutorial on channel how to use)
- fixed directory type filename problems using sanitizer func
- & some more advancements 
  
</details>

<details>
<summary><b>Update: 12 Jan 2025</b></summary>
  
- Fixed blocking and stopping of bot
- Fixed public topic or not topic group extraction (no need of formatting link) login required
- added upload method for public group also
- added `freez` command to remove the expired user with summary (auto removal of funtion is added but still if you want to execute)
- rest explore the updates
</details>

<details>
  
<summary><b>Update: 24 DEC 2024</b></summary>

**1. 4GB Upload Support**  
   - **New feature**: The bot now supports **uploading files as large as 4GB**. This is particularly useful for users working with larger media content.  
   - **How to enable**: To allow **4GB file uploads**, you must add your **premium session string** in the `STRING` variable in the `config.py` file. This session string is only required for **premium users**.

**2. New Upload Method**  
   - A new, optimized **upload method** has been added for handling large file uploads more efficiently.  
   - **What changed**: Previously, large files could cause slow uploads or issues. This method helps avoid those problems and ensures smoother processing.  
   - **Note**: The upload method now handles large files seamlessly, reducing upload time and improving performance.

**3. Fixed Blocking Issue**  
   - **Resolved blocking issues**: We identified and fixed an issue that caused the bot to get blocked during the extraction or upload process, particularly when processing certain content.  
   - **How it works now**: The bot will continue to process and extract content without interruptions or blocks, improving reliability and reducing downtime.

**4. Added `/token` Method**  
   - **New command**: A new `/token` method has been added for **short link functionality**. This command generates a token for using monetization features.  
   - **Configuration**:  
     - To use this feature, you must configure the **API key** and **URL** for your short link provider.  
     - Fill in the `AD_API` (API key) and `WEBSITE_URL` (short link service domain) in the `config.py`.  
     - **Note**: This feature is optional and only needed if you plan to use the bot for monetizing links.

**5. Spylib Integration**  
   - **Spylib added**: We have integrated **Spylib** functionality to enhance certain features. Spylib helps improve the bot’s ability to extract and handle content.  
   - **How to set up**: For details on how to configure **Spylib**, refer to the **Spylib Code Section** in the README for a step-by-step guide.

**6. Fixed Button Issues**  
   - **Fixed broken button functionality**: There were issues where the bot’s buttons were not responding or clicking properly. This has been resolved, and now the buttons will work as expected.  
   - **What’s fixed**: Buttons for commands like `/start`, `/help`, `/cancel`, and others should now work smoothly.
**7. Added ytdlp back in this version:**
   - You can use command /dl or /adl for enabling this fill up ytdlp vars i.e. YT_COOKIES and INSTA_COOKIES
   - you have to rename `ytdl.txt` to `ytdl.py` if want to enable from `devgagan/modules/ytdl.txt`

### 🛠 Important Changes and Notes

**1. Filename Deletion Behavior**  
   - **Delete Word Behavior**: 
     - If a word is added to the **"delete words list"**, it **will not be used in the filename**. This ensures that unwanted words are completely excluded from the filenames.  
     - Example: If the word `deleteword` is added to the list, it will **not appear in the filename** under any circumstances.
  
   - **What’s the catch**:  
     - The **delete word functionality** now applies specifically to **filenames only**.  
     - For captions, you should use the **replacement method** (using spaces as a separator).

**2. Deleting Words in Captions**  
   - **How to delete words in captions**:  
     - If you want to delete words from captions, you should use the **replacement method**, where the word will be replaced with a space (`<space>`).  
     - This will ensure that words are replaced or deleted from captions but **not filenames**.  
     - **Example**:  
       - If you have the word `deleteword` in the caption, you can configure it in the replacement list like:  
         - `'deleteword' '<space>'`.  
       - This will replace `deleteword` with an empty space in the caption.

**3. More About the `/token` Method**  
   - **How to use**:  
     - After configuring the **AD_API** and **WEBSITE_URL** in the `config.py` file, use the `/token` command to generate short links.  
     - This allows you to generate monetized links for users, where you can set up a **link shortener** (e.g., **UpShrink**, **AdFly**) and monetize the bot’s links.
   - **Why use it**: This is helpful for people who want to earn revenue from the links processed by the bot. It's fully configurable, and you can integrate it with any supported short link provider.

**4. Other Fixes and Improvements**  
   - **Improved handling for batch processes**: The bot now handles **batch processes** more effectively and allows users to process multiple links at once.  
   - **Bug fixes**: Several minor bugs related to session management and batch cancellations have been addressed, ensuring a smoother user experience.

**⚙️ How to Configure</summary**

- **Set up `STRING` for 4GB Upload**:  
   - If you want to upload large files (up to 4GB), make sure to add your **premium session string(PYROGRAM V2)** in the `STRING` variable in `config.py`. This is optional and only needed for premium owner who want to allow 4GB upload.

- **Set up `AD_API` and `WEBSITE_URL` for Monetization**:  
   - To use the link shortener service for monetization, collect the API key and website URL from your shortener provider (e.g., **UpShrink**, **AdFly**) and add them to the `AD_API` and `WEBSITE_URL` variables in `config.py`.

- **Delete Word Configuration**:  
   - If you wish to configure words to be deleted from filenames, list them in the **delete word list**.  
   - For captions, use the replacement method where words will be replaced with `<space>`.

</details>

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

### Special thanks to:
- [King of Patal](https://github.com/alreadydea) for base development of this repository.
- [Mautrix Bridge](https://github.com/mautrix/telegram) for fast uploader connectivity bridge.

