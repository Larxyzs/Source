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
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Webhook failed: {e}" + Style.RESET_ALL)
