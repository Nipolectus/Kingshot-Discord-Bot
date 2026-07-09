# 👑 Kingshot Discord Bot

A self-hosted Discord bot for [Kingshot](https://www.centurygames.com/games/kingshot/) that helps alliances manage members, track events, redeem gift codes, schedule ministers, and much more.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏰 **Alliance Management** | Add/remove alliances, manage members, track kingdom transfers |
| 👥 **Member Operations** | Browse members, view furnace levels, export member lists |
| 🎁 **Gift Code Redemption** | Automatically redeem gift codes for all registered members |
| 📣 **Notification System** | Flexible event notifications (Bear Trap, Vikings, KE, and any custom event) |
| 📋 **Attendance Tracking** | Record and report event attendance; export to CSV/TSV/HTML |
| 🏛️ **Minister Scheduling** | Schedule Construction, Research, and Training minister appointments |
| 🆔 **ID Channel** | Automatic in-game ID verification channel |
| 📝 **Self-Registration** | Players can register themselves with `/register` |
| 💾 **Backup & Restore** | Automatic and manual database backups with AES encryption; restore via `/restore_backup` |
| 🔄 **Auto-Update** | Bot checks for new releases on startup and updates itself |

---

## 🚀 Installation

The bot requires **Python 3.10 or newer** and a Discord bot token.

### Obtain a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a **New Application** and go to the **Bot** tab.
3. Click **Reset Token** and copy your token – you will need it during setup.
4. Under **Privileged Gateway Intents**, enable **Message Content Intent**.
5. Under **OAuth2 → URL Generator**, select `bot` and `applications.commands` scopes, then invite the bot to your server.

---

### Option 1 – Local / VPS (Linux, macOS)

This is the recommended method for a Linux VPS or local server.

```bash
# 1. Clone the repository (or download and unzip a release)
git clone https://github.com/kingshot-project/Kingshot-Discord-Bot.git kingshot-bot
cd kingshot-bot

# 2. Run the bot (virtual environment is created automatically)
python3 main.py
```

On first start, the bot will:
- Create a Python virtual environment (`bot_venv/`) automatically.
- Install all required dependencies from `requirements.txt`.
- Ask you to enter your **bot token** (saved to `bot_token.txt` for future starts).
- Create the `db/` folder and all required database tables.

> **Note:** Auto-update is disabled in this fork (it would overwrite the fork's custom code with upstream files). Update manually with `git pull`. The `--autoupdate`, `--no-update`, `--repair` and `--beta` flags therefore have no effect.

Other useful flags:

| Flag | Description |
|---|---|
| `--no-venv` | Skip virtual environment creation (use system Python) |

---

### Option 2 – Linux / Raspberry Pi with systemd service (runs on boot, auto-restarts)

One command sets up everything — venv, dependencies, token, and the systemd service:

```bash
# 1. Clone the repository
git clone https://github.com/Nipolectus/Kingshot-Discord-Bot.git kingshot-bot
cd kingshot-bot

# 2. Run the installer (creates venv, installs deps, asks for token,
#    then installs and starts the systemd service as your user)
sudo python3 main.py
```

```bash
# Check status
sudo systemctl status kingshot-bot

# View live logs
sudo journalctl -u kingshot-bot -f
```

If you prefer to set the service up manually, run `python3 main.py` once without sudo (creates venv and asks for the token), stop it with Ctrl+C, then copy `install/kingshot-bot.service` to `/etc/systemd/system/`, adjust the `User`, `WorkingDirectory` and `ExecStart` paths, and run `sudo systemctl daemon-reload && sudo systemctl enable --now kingshot-bot`.

---

### Option 3 – Docker / Docker Compose

```bash
# 1. Create directory for persistent data
mkdir -p /opt/docker/kingshot/db /opt/docker/kingshot/backups

# 2. Copy docker-compose.yml
cp docker/docker-compose.yml /opt/docker/kingshot/docker-compose.yml
```

Edit `/opt/docker/kingshot/docker-compose.yml` and set your bot token:

```yaml
services:
  kingshot-discord-bot:
    image: ghcr.io/kingshot-project/kingshot-discord-bot:latest
    container_name: kingshot-discord-bot
    volumes:
      - /opt/docker/kingshot/db/:/app/db
      - /opt/docker/kingshot/backups/:/app/backups   # optional: persist backups
    restart: unless-stopped
    environment:
      - DISCORD_BOT_TOKEN=your_token_here
      # - UPDATE=0      # set to 0 to disable auto-update
      # - BETA=1        # set to 1 for beta/dev channel
      # - DEBUG=1       # set to 1 for verbose logging
```

```bash
# 3. Start the bot
cd /opt/docker/kingshot
docker compose up -d

# View logs
docker compose logs -f
```

---

### Option 4 – Windows

Double-click `install/windowsAutoRun.bat`. It will:
1. Install Python if not already installed (via `winget`).
2. Download the bot files.
3. Create a virtual environment.
4. Start the bot and ask for your token on first run.

On subsequent launches, just double-click the `.bat` file again – the bot will start automatically.

---

## 📁 File Structure

```
kingshot-bot/
├── main.py              # Bot entry point
├── requirements.txt     # Python dependencies
├── bot_token.txt        # Your bot token (created on first run, do not share!)
├── version              # Current installed version
├── cogs/                # Bot modules (features)
├── db/                  # SQLite databases (your data lives here)
├── backups/             # Local backup ZIP files
├── log/                 # Log files
├── fonts/               # Fonts used for image generation
├── docker/              # Docker and Docker Compose files
└── install/             # Installation helpers (service file, bat script)
```

---

## 💾 Backup & Restore

The bot includes a built-in backup system:

- Automatic backups run every 3 hours and are kept in the local `backups/` folder (last 2 are kept). Note: a Global Admin must be configured or automatic backups do not run.
- Manual backups can be created from the backup menu (saved locally or sent via DM).
- AES password encryption can be enabled per admin in the backup menu.
- Restore a backup by uploading the ZIP with `/restore_backup`, then restart the bot. This also works for moving data from another instance of this bot to a fresh install.

### Off-device backup copies (recommended on Raspberry Pi / SD cards)

Local backups live on the same disk as the databases, so a disk failure loses both. To automatically copy every local backup to a second location (mounted USB stick, NAS mount, synced cloud folder), create a file named `external_backup_dir.txt` in the bot's root directory containing the target directory path, e.g.:

```
/mnt/usb-backup/kingshot
```

The directory must already exist (the bot will not create it, so an unmounted drive is never written to). The newest 10 automatic backups are kept there; manual backups are never pruned.

---

## ⚙️ Bot Setup After Installation

Once the bot is running and has joined your Discord server:

1. Use `/settings` (or the main menu command) to open the bot control panel.
2. Add yourself as a **Global Admin**.
3. Create your alliances with **Alliance Management → Add Alliance**.
4. Configure a gift code channel under **Bot Operations**.
5. Add players to the database via **Alliance Member Operations → Add Member** or enable self-registration under **Other Features → Registration System**.

---

## 🆘 Help & Support

If you encounter issues, you can:

- Run `python main.py --repair` to re-download and restore all bot files.
- Check `log/` for error logs.
- Open an [issue on GitHub](https://github.com/kingshot-project/Kingshot-Discord-Bot/issues).
