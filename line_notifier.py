import os
from linebot import LineBotApi #Line Messaging API 互動的核心類別
from linebot.models import TextMessage, FlexSendMessage

# 從 GitHub Actions 的環境變數讀取 Token
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# 初始化 LineBotApi 物件
line_bot_api = LineBotApi(channel_access_token)

def send_pm25_flex_message(exceed_pm25_dataframe):
    message = f"超標地區：{exceed_pm25_dataframe["sitename"]}"
    flex_meaasge = FlexSendMessage(
        alt_text = "PM2.5觀測數據",
        contents={
            "type":"bubble",
            "header":{
                "type":"box",
                "layout":"vertical",
                "contents":[
                    {
                        "type":"text",
                        "text":"最新PM2.5觀測結果",
                        "weight":"bold",
                        "size":"xl",
                        "color":"#000000"
                    }
                ]
            },
            "body":{
                "type":"box",
                "layout":"vertical",
                "contents":[
                    {
                        "type":"text",
                        "text":message
                    },
                    {
                        "type":"buttom",
                        "sytle":"primary",
                        "action":{
                            "type":"uri",
                            "label":"查看全台PM2.5觀測結果",
                            "uri":"https://eishinchen.github.io/aether_bot/pm25_map.html"
                        }
                    }
                ]
            }
        }
    )
    try:
        line_bot_api.broadcast(flex_meaasge)
        print("訊息發送成功")
    except Exception as e:
        print("發送失敗:", e)