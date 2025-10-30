# Rock Cloner V2 Discord Server Cloner (Windows EXE)

![Rock Cloner V2](ROCK_CLONER.png)

A standalone **Windows desktop application** that allows you to **clone a complete Discord server structure** — including roles, categories, channels, emojis, and icons from one server to another.  

No Python setup or terminal required.  
Built with **PyQt6** and compiled via **Nuitka** for a native Windows experience.

---

<p align="center">
  <a href="https://github.com/devrock07/rock-cloner/releases/tag/2.0">
    <img src="https://img.shields.io/badge/⬇️%20Download%20Rock%20Cloner%20V2-blue?style=for-the-badge&logo=github" alt="Download Rock Cloner V2">
  </a>
</p>

---

## Overview

| Attribute | Information |
|------------|-------------|
| **Application Name** | Rock Cloner V2 |
| **Version** | 2.0 |
| **Type** | Standalone Windows Executable |
| **Framework** | PyQt6 GUI |
| **Compiler** | Nuitka (Optimized Build) |
| **Platform** | Discord |
| **License** | Educational / Research |
| **Developer** | Devrock |

---

## Features

### Server Structure Cloning

| Component | Description |
|------------|--------------|
| **Roles & Permissions** | Fully replicates all roles with associated permissions and hierarchy. |
| **Categories** | Copies category structure for proper organization. |
| **Text Channels** | Duplicates text channels along with slowmode, topics, and permissions. |
| **Voice Channels** | Clones voice channels including bitrate, user limits, and permissions. |
| **Emojis (Optional)** | Downloads and re-uploads emojis to the target server if selected. |
| **Server Metadata** | Optionally copies the server name, region, and icon. |

---

### Additional Features

| Feature | Description |
|----------|--------------|
| **Modern GUI** | Built with PyQt6 for a clean, intuitive user experience. |
| **Settings Tab** | Configure default clone behavior (e.g., skip emojis, skip categories). |
| **Pre-clone Cleanup** | Optionally clears the target server before cloning to avoid conflicts. |
| **Clone Summary Log** | Displays a detailed summary after each cloning session. |
| **Built-in Documentation** | Accessible from the menu bar for quick help and usage instructions. |
| **Progress Tracker** | Visual progress bar and terminal-style log viewer during clone execution. |

---

## How It Works

Rock Cloner V2 uses the official **Discord Bot API** to replicate server structure safely.  
It does **not** use user tokens or selfbot APIs — only bot accounts.

When cloning:
1. The bot fetches data from the source server using read permissions.  
2. It creates matching roles, categories, and channels in the destination server.  
3. If enabled, it downloads all emojis and re-uploads them.  
4. Finally, it logs the cloning summary in the application window.

All operations respect Discord rate limits and API safety measures.

---

## How to Use

1. **Download** the latest Rock Cloner V2 ZIP file from the [Releases page](https://github.com/devrock07/rock-cloner/releases/tag/2.0).  
2. **Extract** the ZIP anywhere on your computer.  
3. Open the extracted folder and **run `main.exe`**.  
4. Enter your **Discord Bot Token**.  
5. Input:
   - **Source Server ID** — the server you want to clone.  
   - **Destination Server ID** — the server to clone into.  
6. Select your desired clone options (roles, channels, emojis, icon, etc.).  
7. Click **Start Clone** — Rock Cloner V2 will do the rest.

---

## Notes

- You must **add the bot** to both servers (source & destination).  
- The bot must have the following **permissions**:
  - `Manage Roles`  
  - `Manage Channels`  
  - `Manage Emojis and Stickers`  
  - `Manage Server`  
  - `Read Messages / Message History`  

- Designed for:
  - **Windows 10/11 (x64)**  
  - No external dependencies or Python required  
  - Runs entirely offline once initialized  

---

## Performance

| Operation | Average Time |
|------------|---------------|
| Role Cloning | 1–3 seconds (per role) |
| Channel Cloning | 1–5 seconds (per category) |
| Emoji Upload | 3–8 seconds (per emoji, based on size) |
| Total Server Clone | 30 seconds – 2 minutes (average) |

Performance may vary depending on server size, network, and API rate limits.

---

## Credits

| Role | Contributor |
|------|--------------|
| **Lead Developer** | [Dev Bhakat](https://github.com/devrock07) |
| **UI/UX Design** | Devrock |
| **Frameworks Used** | PyQt6, Requests, Nuitka |
| **Logo & Branding** | Inbora Studio |
| **Testing & QA** | Community Testers |

---

## Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend (UI)** | PyQt6 |
| **Core Logic** | Python 3.12 |
| **Compiler** | Nuitka |
| **API Communication** | Discord REST API |
| **Async Handling** | `asyncio` + `aiohttp` |
| **Styling** | QSS (Custom Themes) |

---

## Troubleshooting

| Issue | Possible Fix |
|--------|---------------|
| **EXE doesn’t open** | Right-click and select *Run as Administrator*. |
| **Windows SmartScreen warning** | Click *More Info → Run Anyway* (Nuitka apps are unsigned). |
| **Antivirus false positive** | Temporarily disable or whitelist the EXE (Nuitka builds may be flagged). |
| **Clone stops midway** | Check bot permissions and API limits. Try again after a few minutes. |
| **No server found** | Ensure your bot is invited to both servers with correct permissions. |

If issues persist, create a [GitHub Issue](https://github.com/devrock07/rock-cloner/issues) with screenshots and logs.

---

## Security & Safety

- Rock Cloner V2 **does not store or send** your bot token anywhere.  
- All credentials remain **local** to your device.  
- Network communication occurs **only between Discord’s API** and your machine.  
- Logging is minimal and saved only for user review.  

---

## License & Disclaimer

| Notice | Description |
|--------|-------------|
| **License** | Educational / Research Use Only |
| **Terms of Use** | Comply with Discord's [Terms of Service](https://discord.com/terms). |
| **Liability** | The developer is not responsible for misuse or account actions resulting from API violations. |
| **Security** | No data collection or external communication beyond official Discord API. |

---

## Future Updates

Planned features for upcoming releases:

- Multi-server cloning support  
- Clone export/import (JSON format)  
- Partial cloning (select channels/roles only)  
- Cloud backups for saved configurations  
- Theme customization for UI  

Stay updated via the [GitHub Releases](https://github.com/devrock07/rock-cloner/releases) section.

---

## Final Words

Rock Cloner V2 was built to simplify server management and automation for developers, moderators, and community managers who want a safe and efficient cloning experience.  

If you find this project useful, **consider starring the repository** it helps support further development.

---

⭐ **[Star the Repository](https://github.com/devrock07/rock-cloner)**  
🪶 Crafted with precision and dedication by **Devrock**
