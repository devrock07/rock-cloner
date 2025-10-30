# Rock Cloner V2 Discord Server Cloner

A **powerful Python-based Discord server cloning tool** that replicates server structure from one Discord server to another, including roles, categories, channels, and more all through an interactive terminal interface.

---

## Overview

| Key Information | Details |
|-----------------|----------|
| **Name** | Rock Cloner V2 |
| **Language** | Python |
| **Platform** | Discord |
| **Interface** | Interactive Terminal (CLI) |
| **Developer** | DEVROCK |

---

## Features

| Category | Description |
|-----------|--------------|
| **Server Structure Cloning** | Clone server elements such as Roles, Categories, Channels, and Server Settings. |
| **Emoji Cloning** | Optionally clone emojis from the source server. |
| **Server Metadata** | Copy server icon and name. |
| **Interactive UI** | Built using `questionary`, `inquirer`, `pyfiglet`, and `rich` for a modern terminal experience. |

---

## Installation

### Prerequisites

Ensure you have **Python 3.10 – 3.12** installed.

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/rock-cloner-v2.git
cd rock-cloner-v2

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

Follow these steps to run **Rock Cloner V2**:

1. Open a terminal inside the project folder  
2. Run the following command:
   ```bash
   python main.py
   ```
3. When prompted, provide your **Discord user token**  
4. Enter the following details:
   - **Source Server ID** (server to clone from)  
   - **Destination Server ID** (server to clone into)  
5. Choose what to clone (Roles, Channels, Emojis, etc.)  
6. The program will automatically begin cloning the selected components.

---

## Requirements

| Dependency | Purpose |
|-------------|----------|
| **questionary** | Interactive terminal prompts |
| **inquirer** | Command-line input management |
| **pyfiglet** | ASCII-styled banners and headers |
| **rich** | Beautiful terminal formatting and progress display |

---

## Legal Disclaimer

| Notice | Description |
|---------|-------------|
| **Educational Use Only** | This project is intended solely for learning and demonstration purposes. |
| **Discord Terms** | Self-bots and automation using user tokens are against Discord’s [Terms of Service](https://discord.com/terms). |
| **User Responsibility** | The author is not responsible for any misuse or violations resulting from this software. Use it at your own risk. |

---

## Author

| Name | Role | Contact |
|------|------|----------|
| **DEVROCK** | Developer & Maintainer | [Python.org](https://www.python.org) / [Discord](https://github.com/devrock07) |
