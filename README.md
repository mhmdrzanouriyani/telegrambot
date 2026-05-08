<h1 align="center">🤖 MohixBot — YouTube & Instagram Downloader Bot</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/aiogram-3.x-blue?style=for-the-badge&logo=telegram&logoColor=white" />
  <img src="https://img.shields.io/badge/yt--dlp-powered-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Async-asyncio-green?style=for-the-badge" />
  <img src="https://img.shields.io/github/stars/mhmdrzanouriyani/telegrambot?style=for-the-badge" />
</p>

<p align="center">
  A production-ready Telegram bot that downloads YouTube videos, YouTube Shorts,<br>
  and Instagram content on demand — built with aiogram 3.x and full async architecture.
</p>

---

## ✨ Features

- ✅ Download YouTube videos in best quality
- ✅ Download YouTube Shorts
- ✅ Download Instagram photos and videos
- ✅ Async background download queue — handles multiple users simultaneously
- ✅ Smart URL analyzer — detects YouTube vs Instagram automatically
- ✅ Custom inline keyboards for video quality selection
- ✅ Description extractor for video metadata
- ✅ Auto file cleaner after upload
- ✅ Message splitter for long content
- ✅ Secure token loading via environment variable
- ✅ Full logging system

---

## 🏗️ Architecture

```bash
telegrambot/
└── telegrammohixbot/
    └── bot/
        ├── main.py                        # Entry point
        ├── handlers/
        │   ├── start.py                   # /start command
        │   ├── messages.py                # URL message handler
        │   └── callbacks.py               # Inline keyboard callbacks
        ├── downloaders/
        │   ├── youtube.py                 # yt-dlp YouTube downloader
        │   └── instagram.py               # Instagram downloader
        ├── services/
        │   ├── queue.py                   # Async download queue worker
        │   ├── uploader.py                # File uploader to Telegram
        │   ├── analyzer.py                # URL analyzer (YT vs Instagram)
        │   ├── description_extractor.py   # Video metadata extractor
        │   └── url_storage.py             # URL deduplication storage
        ├── keyboards/
        │   ├── start_keyboard.py          # Welcome menu keyboard
        │   └── video_menu.py              # Video options keyboard
        └── utils/
            ├── logger.py                  # Logging setup
            ├── cleaner.py                 # Temp file cleanup
            └── message_splitter.py        # Long message handler
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/mhmdrzanouriyani/telegrambot.git
cd telegrambot
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your bot token

**Option A — Environment variable (recommended):**
```bash
set BOT_TOKEN=your_telegram_bot_token    # Windows
export BOT_TOKEN=your_telegram_bot_token # Linux/Mac
```

**Option B — File:**
```bash
echo your_telegram_bot_token > telegrammohixbot/bot/api_key_bot.txt
```

> 🔑 Get your token from [@BotFather](https://t.me/BotFather) on Telegram

### 5. Run the bot
```bash
cd telegrammohixbot
python -m bot.main
```

---

## 💬 How to Use

1. Start the bot with `/start`
2. Send any YouTube or Instagram link
3. Bot automatically detects the platform
4. Choose quality if prompted
5. Bot downloads and sends the file directly to chat

---

## 🔒 Security Notes

- **Never commit** `api_key_bot.txt` or `.env` files
- Always use environment variables in production
- The `.gitignore` in this repo protects your token

---

## ⚙️ Requirements

```
aiogram>=3.0.0
yt-dlp>=2024.1.1
aiohttp>=3.9.0
instaloader>=4.10
```

---

## 📌 Roadmap

- [ ] Add TikTok download support
- [ ] Add download progress bar in chat
- [ ] Add admin panel with usage statistics
- [ ] Deploy to VPS with systemd auto-restart
- [ ] Add support for playlists

---

## 👨‍💻 Author

**Mohammadreza Nouriyani**

[![YouTube](https://img.shields.io/badge/YouTube-Mohix_Code-red?style=flat&logo=youtube)](https://www.youtube.com/@Mohixcode)
[![Instagram](https://img.shields.io/badge/Instagram-mohix_code-purple?style=flat&logo=instagram)](https://www.instagram.com/mohix_code)
[![GitHub](https://img.shields.io/badge/GitHub-mhmdrzanouriyani-black?style=flat&logo=github)](https://github.com/mhmdrzanouriyani)

---

⭐ If this helped you, please give it a star!
