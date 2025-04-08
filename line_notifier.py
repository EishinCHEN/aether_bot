import os
from linebot import LineBotApi #Line Messaging API 互動的核心類別
from linebot.models import TextMessage

# 從 GitHub Actions 的環境變數讀取 Token
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# 初始化 LineBotApi 物件
line_bot_api = LineBotApi(channel_access_token)

def send_text_message(message):
    try:
        line_bot_api.broadcast(TextMessage(text=message))
        print("訊息發送成功")
    except Exception as e:
        print("發送失敗:", e)