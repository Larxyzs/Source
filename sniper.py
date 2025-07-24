import hashlib
import os
import sys
import time
import requests
from colorama import Fore, Style, init

init()

LICENSE_FILE = os.path.join(os.getenv("APPDATA"), "roblox_sniper", "license.dat")

def load_license():
    if not os.path.exists(LICENSE_FILE):
        return None
    try:
        import json
        with open(LICENSE_FILE, "r") as f:
            data = json.load(f)
        return data
    except Exception:
        return None

def verify_license_file(data):
    expected_token = hashlib.sha256(f"{data['key']}_{data['machine_id']}".encode()).hexdigest()
    return data.get("token") == expected_token

def send_webhook(webhook_url, message):
    if webhook_url:
        data = {
            "content": message,
            "username": "Roblox Sniperz - Made by Larxy",
            "avatar_url": "https://cdn.discordapp.com/avatars/1356540370367938622/archived/1389152101388783686/6ea566985a56c61c890ade62fe1aeea3.png?size=1280"
        }
        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
        except Exception as e:
            print(Fore.RED + f"Webhook failed: {e}" + Style.RESET_ALL)

def check_username(username, webhook_url, max_retries=3):
    url = f"https://auth.roblox.com/v1/usernames/validate?Username={username}&Birthday=2000-01-01"
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            response_data = response.json()
            code = response_data.get("code")

            if code == 0:
                print(Fore.GREEN + f"VALID: {username}" + Style.RESET_ALL)
                with open("valid.txt", "a") as valid_file:
                    valid_file.write(username + "\n")
                if webhook_url:
                    send_webhook(webhook_url, f"@everyone @here NEW SNIPE! : user : {username}")
                sys.exit(0)
            elif code == 1:
                print(Fore.LIGHTBLACK_EX + f"TAKEN: {username}" + Style.RESET_ALL)
            elif code == 2:
                print(Fore.RED + f"CENSORED: {username}" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"Unknown code ({code}): {username}" + Style.RESET_ALL)
            return
        except requests.exceptions.RequestException as e:
            retries += 1
            print(Fore.YELLOW + f"Network error for {username} (attempt {retries}): {e}" + Style.RESET_ALL)
            time.sleep(1)  # wait before retrying

    print(Fore.RED + f"Failed to check {username} after {max_retries} attempts." + Style.RESET_ALL)

def main():
    if len(sys.argv) < 2:
        print("Usage: python sniper.py <length> [webhook_url]")
        sys.exit(1)

    length = sys.argv[1]
    webhook_url = sys.argv[2] if len(sys.argv) > 2 else ""

    license_data = load_license()
    if not license_data or not verify_license_file(license_data):
        print(Fore.RED + "No valid license found. Please run the setup first." + Style.RESET_ALL)
        sys.exit(1)

    filename = f"usernames{length}.txt"
    if not os.path.exists(filename):
        print(Fore.RED + f"File '{filename}' not found." + Style.RESET_ALL)
        sys.exit(1)

    with open(filename, "r") as file:
        usernames = file.read().splitlines()

    if webhook_url:
        send_webhook(webhook_url, "Webhook successfully set!")

    for username in usernames:
        check_username(username, webhook_url)
        time.sleep(0.3)

    print(Fore.YELLOW + "Finished checking all usernames. No valid username found." + Style.RESET_ALL)
    sys.exit(0)

if __name__ == "__main__":
    main()
