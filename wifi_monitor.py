import subprocess
import re
import os
import time
import requests
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()

# --- Configuration is now loaded from your .env file ---
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
NETWORK_RANGE = os.getenv('NETWORK_RANGE', '192.168.1.0/24')
SCAN_INTERVAL_SECONDS = int(os.getenv('SCAN_INTERVAL_SECONDS', 300))

# --- Constants ---
KNOWN_DEVICES_FILE = 'known_devices.txt'
notified_unknown_devices = set()

def send_telegram_notification(mac_address, ip_address):
    """Sends a simplified notification with IP and MAC address."""
    message = (
        f"🚨 *Unknown Device Detected* 🚨\n\n"
        f"*IP Address:* `{ip_address}`\n"
        f"*MAC Address:* `{mac_address}`"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ Notification sent for {mac_address}")
        else:
            print(f"❌ Failed to send notification. Status: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        print(f"❌ An error occurred while sending notification: {e}")

def get_known_devices():
    """Reads the known MAC addresses from the known_devices.txt file."""
    try:
        with open(KNOWN_DEVICES_FILE, 'r') as f:
            known_macs = {line.split('#')[0].strip().upper() for line in f if line.strip() and not line.startswith('#')}
        return known_macs
    except FileNotFoundError:
        print(f"⚠️ WARNING: {KNOWN_DEVICES_FILE} not found. A 'known_devices.txt' file is needed.")
        return set()

def scan_network():
    """Scans the network and returns a simple dictionary of {mac: ip}."""
    print("Scanning network...")
    try:
        process = subprocess.run(
            ['nmap', '-sn', '-PR', NETWORK_RANGE],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Simple regex to find IP and MAC addresses
        found_devices = re.findall(r"Nmap scan report for ([\d\.]+)\n.*?MAC Address: ([0-9A-F:]{17})", process.stdout, re.DOTALL)
        # Convert list of tuples to a dictionary of {mac: ip}
        return {mac.upper(): ip for ip, mac in found_devices}

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ Error during nmap scan: {e}.")
        return {}

def main():
    """Main loop to continuously scan the network."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ CRITICAL: Ensure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set in your .env file.")
        return

    print("--- Wi-Fi Monitor Service Starting ---")
    
    while True:
        known_devices = get_known_devices()
        current_devices_on_network = scan_network()
        
        print(f"Found {len(current_devices_on_network)} devices. Known devices: {len(known_devices)}")
        
        for mac, ip in current_devices_on_network.items():
            if mac not in known_devices and mac not in notified_unknown_devices:
                print(f"🚨 Found new unknown device: {ip} ({mac})")
                send_telegram_notification(mac, ip)
                notified_unknown_devices.add(mac)
        
        print(f"--- Scan complete. Waiting for {SCAN_INTERVAL_SECONDS} seconds... ---")
        time.sleep(SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()