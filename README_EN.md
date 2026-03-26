# 🌌 NOVA — Personal AI Assistant
> **Jarvis Edition** · Task management & workflow automation for developers

---

## 📋 Overview

**NOVA** is a smart assistant built for developers who need to stay organized. It delivers voice notifications, weather reports, and automated environment setup — all controlled via Telegram.

---

## 🖥️ System Requirements

| Requirement | Details |
|-------------|---------|
| **OS** | Windows 10 / 11 (optimized for `cmd` + `cursor`) |
| **Python** | `3.10` or higher |
| **FFmpeg** | Required for the neural voice engine (`edge-tts`) |

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/nova-bot.git
cd nova-bot
```

### 2. Create a Virtual Environment

Keeps your project libraries isolated from the rest of the system:

```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate
```

### 3. Install Python Dependencies

Create `requirements.txt` with the following content, then run `pip install -r requirements.txt`:

```
pyTelegramBotAPI
requests
edge-tts
pygame
```

### 4. Install FFmpeg ⚠️

NOVA requires FFmpeg to process and play neural voice audio:

1. Download the **"Essentials"** build from [ffmpeg.org](https://ffmpeg.org).
2. Extract the folder to `C:\ffmpeg`.
3. Open **"Edit the system environment variables"** from the Windows search bar.
4. Click **Environment Variables** → find `Path` under *System variables* → click **Edit**.
5. Add `C:\ffmpeg\bin` to the list and save.

---

## ⚙️ Configuration

Open `nova.py` and update the following variables at the top of the script:

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_TOKEN` | Your bot token from `@BotFather` | `'8616169584:AAEz...'` |
| `PROYECTO_PATH` | Path to your main coding project | `r"D:\Repositories\tally-ai"` |
| `HORA_SALUDO` | Morning report time (24h format) | `"06:00"` |
| `VOZ_NEURAL` | Voice ID for text-to-speech | `"es-MX-JorgeNeural"` |

---

## 📲 Telegram Commands

| Command | Action |
|---------|--------|
| `Nova, [Task], [Date], [Time]` | Schedules a new task — e.g., `Nova, Gym, 2026-03-25, 18:00` |
| `Nova, modo trabajo` | Opens Cursor and starts the `npm run dev` server |
| `Nova, clima` | Detailed weather report for Suba (Bogotá) in Spanish |
| `Nova, tareas` | Summary of all your tasks for today |
| `Hola` | Connection test — checks if NOVA is online |

---

## 📂 Project Structure

```
nova-bot/
├── nova.py              # Main logic, DB handlers & background watcher threads
├── nova_memoria.db      # SQLite database for task persistence (auto-generated)
├── requirements.txt     # Python dependencies
└── .gitignore           # Excludes temp files, audio & venv from GitHub
```

---

## 🧠 Developer Notes

- **Multithreading** — Uses Python `threading` to run the task monitor and the Telegram bot simultaneously.
- **Audio Handling** — Uses `pygame` for local playback and `edge-tts` for high-quality Microsoft neural voices.
- **Data Persistence** — Tasks are stored in SQLite so no data is lost if the script restarts.

---

## 🛡️ `.gitignore`

Create a `.gitignore` file at the project root to avoid uploading temporary or private files to GitHub:

```gitignore
# Python
__pycache__/
*.pyc
venv/

# Nova Files
nova_neural.mp3
nova_memoria.db
config_saludo.txt

# Environment
.env
```

---

*Built with Python · Powered by edge-tts & Telegram Bot API*
