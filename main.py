import time
from datetime import datetime
import requests
import pygetwindow as gw  # pip install pygetwindow

# Discord Webhook URLを設定
WEBHOOK_URL = "https://discord.com/api/webhooks/XXXX/XXXXX"

# ウィンドウが開いているか確認する関数
def is_window_open(window_name):
    return bool(gw.getWindowsWithTitle(window_name))

# Discordに通知を送信する関数
def send_discord_notification(window_name):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        "content": "<@&1288048132709421077>",  # ロールIDでメンション
        "embeds": [
            {
                "title": "Task Closed",
                "description": f"The task '{window_name}' has been closed.",
                "color": 16711680,  # 赤色 (0xFF0000)
                "footer": {
                    "text": f"Notification sent at {current_time}"
                }
            }
        ]
    }
    
    # Webhookを送信
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Notification sent successfully!")
    else:
        print("Failed to send notification:", response.status_code, response.text)

# 常にウィンドウを監視する関数
def monitor_window(window_name):
    window_was_open = False  # 最初の状態を閉じていると仮定
    
    while True:
        window_open = is_window_open(window_name)
        
        # ウィンドウが閉じた瞬間に通知を送信
        if window_was_open and not window_open:
            print(f"The window '{window_name}' has been closed. Sending notification...")
            send_discord_notification(window_name)
        
        # 状態を更新
        window_was_open = window_open
        
        # 10秒ごとにチェック
        time.sleep(10)

# 監視したいウィンドウ名を設定
window_name = "Gameserver"  # 監視したいウィンドウ名
monitor_window(window_name)
