import os
from linebot import LineBotApi #Line Messaging API 互動的核心類別
from linebot.models import TextMessage, FlexSendMessage

# 從 GitHub Actions 的環境變數讀取 Token
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# 初始化 LineBotApi 物件
line_bot_api = LineBotApi(channel_access_token)

def send_pm25_flex_message(exceed_pm25_dataframe):
    exceed_site = exceed_pm25_dataframe["site"].tolist()
    if len(exceed_site) > 0:
        message = "超標地區：" + ", ".join(exceed_site)
    else: 
        message = "目前全台觀測站都沒有超標喔，是個適合透透風的日子呢＾＾"

    flex_message = FlexSendMessage(
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
                        "color":"#262625"
                    }
                ]
            },
            "body":{
                "type":"box",
                "layout":"vertical",
                "contents":[
                    {
                        "type":"text",
                        "text":message,
                          "wrap":True
                    },
                    {
                        "type":"button",
                        "style":"primary",
                        "action":{
                            "type":"uri",
                            "label":"查看全台PM2.5觀測結果",
                            "uri":"https://eishinchen.github.io/aether_bot"
                        }
                    }
                ]
            }
        }
    )
    try:
        line_bot_api.broadcast(flex_message)
        print("訊息發送成功")
    except Exception as e:
        print("發送失敗:", e)