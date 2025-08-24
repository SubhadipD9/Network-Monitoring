# Wi-Fi Network Monitor & Telegram Alerter 📡

A simple Python script that monitors your local network for new, unknown devices and sends an instant alert to a private Telegram bot. This tool helps you keep track of who is connecting to your Wi-Fi using either Docker or a native Python installation.

---

## ## Working Demo

<img width="348" height="218" alt="Screenshot 2025-08-24 004401" src="https://github.com/user-attachments/assets/3d9f962f-36a1-483a-957a-6d889397980c" />

## ## Project Structure

The project is organized with the following file structure to facilitate easy configuration and deployment:

```bash
/wifi-monitor
├── .env.sample # Sample environment file
├── .gitignore # Files to ignore for version control
├── Dockerfile # Instructions to build the Docker image
├── README.md # This file
├── known_devices.txt # Your list of approved device MACs
├── requirements.txt # Python dependencies
├── sample.known_devices.txt # Sample known devices file
└── wifi_monitor.py # The main monitoring script
```

---

## Features ⭐

- **Periodic Scanning:** Automatically scans your local network at a set interval.
- **Unknown Device Detection:** Compares found devices against a pre-approved "known devices" list.
- **Instant Telegram Alerts:** Sends a formatted, private notification when an unknown device is found.
- **Docker Support:** Can be run as a lightweight, isolated Docker container.
- **Easy Configuration:** All settings are managed in a simple `.env` file.
- **Spam Prevention:** Remembers notified devices to avoid sending repeated alerts.

---

## First Setup your Machine 💻

## Installation and Setup ⚙️

Follow these steps to get the monitor up and running.

### Step 1: Install Prerequisites

First, install the necessary software on your computer.

#### 🖥️ On Windows

**Install Python 3:**

- Download from [python.org](https://www.python.org).
- **Important:** On the first screen of the installer, check the box **"Add Python.exe to PATH"**.

**Install Nmap 🛜🔎:**

- Download the installer from [nmap.org](https://nmap.org).
- Run the installer and accept all default options.

#### 🍎 On macOS

**Install Homebrew:**

- If you don't have it, open the Terminal and follow the instructions at [brew.sh](https://brew.sh).

**Install Python 3 and Nmap:**

- In the Terminal, run:

  ```bash
  brew install python nmap
  ```

#### 🐧 On Linux (Debian, Ubuntu, Raspberry Pi)

**Install Python 3, pip, and Nmap:**

- Open your terminal and run:

  ```bash
  sudo apt-get update && sudo apt-get install python3 python3-pip nmap -y
  ```

## Setup and Configuration ⚙️

Follow these steps to get the monitor up and running.

### ### 1. Get the Project Files

Clone this repository or create the files listed in the project structure above.

### ### 2. Set Up Your Telegram Bot

You need a bot to send you messages. You can create one by talking to the **`@BotFather`** on Telegram.

1.  Start a chat with `@BotFather` and send the command `/newbot`.
2.  Follow the prompts to choose a name and username for your bot.
3.  BotFather will give you a **Bot Token**. Save this token.
4.  Find your bot in Telegram, send it a `/start` message, and then visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` in a browser (with your token) to find your **Chat ID**.

### ### 3. Configure Your Environment

The project uses a `.env` file to manage configuration and secrets.

1.  Rename the sample file `.env.sample` to **`.env`**.
2.  Open the `.env` file and fill in your **Telegram Bot Token**, **Chat ID**, and your **Network Range**.

### ### 4. Create Your Device Whitelist

This file tells the script which devices are yours and should be ignored.

1.  Rename the sample file `sample.known_devices.txt` to **`known_devices.txt`**.
2.  Open `known_devices.txt` and add the MAC addresses of your trusted devices (phone, laptop, etc.), one per line.

---

### Method : Running Natively

Follow these steps if you prefer to run the script directly on your OS.

1.  **Prerequisites:** Install **Python 3** and **Nmap** on your system. (See previous instructions for platform-specific installation details).

2.  **Install Dependencies:**

    - Create a virtual environment

    ```bash
      python -m venv myvenv  # Replace 'myvenv' with your preferred environment name
    ```

    - Activate the Virtual Environment:

      #### On Windows (Command Prompt/Git Bash):

      ```bash
      # For Windows Command Prompt
      myenv\Scripts\activate
      ```

      ##### For Git Bash

      ```bash
      # For Git Bash for Windows
      myenv\Scripts\activate
      ```

      #### On Linux/macOS (Bash/Zsh):

      ```bash
      source myenv/bin/activate
      ```

    - Open a terminal in the project directory.
    - (Optional but recommended) Create and activate a virtual environment (See the previous steps).
    - Run: `pip install -r requirements.txt`

3.  **Run the Script:**
    - You must run the script with **administrator/root privileges** for `nmap` to work.
    - **On Windows:** Open Command Prompt **as Administrator** and run `python wifi_monitor.py`.
    - **On macOS/Linux:** Run `sudo python3 wifi_monitor.py`.

---

## Troubleshooting

- **Problem:** The scan fails or finds 0 devices.

  - **Solution:** This is almost always a permission issue. If running natively, ensure you are using **Administrator/`sudo`**. If using Docker, ensure you have included the `--network host` flag.

- **Problem:** I'm not getting Telegram notifications.
  - **Solution:** Double-check your `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in your `.env` file. Ensure they are correct and have no extra spaces.
