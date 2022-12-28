from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
# from msg.flex import reply_flex
# from msg.reply import read_user_message
import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)

# domain root
@app.route('/')
def home():
    return 'Hello Cookie!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.type != "text":
        return
    
    # user_message = event.message.text
    # reply_message = read_user_message(user_message)
    
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
{
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "weight": "bold",
                "color": "#1DB446",
                "size": "sm",
                "text": "已核准"
            },
            {
                "type": "text",
                "text": "公雞叫股份有限公司",
                "weight": "bold",
                "size": "xxl",
                "margin": "md"
            },
            {
                "type": "text",
                "text": "台南市七股區七股段000號",
                "size": "xs",
                "color": "#999999",
                "wrap": True
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "xxl",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "土地面積",
                        "size": "sm",
                        "color": "#555555",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "999 ㎡ ",
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "設置容量",
                        "size": "sm",
                        "color": "#555555",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": "999 kW",
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xxl",
                    "contents": [
                    {
                        "type": "text",
                        "text": "土地使用分區",
                        "size": "sm",
                        "color": "#555555"
                    },
                    {
                        "type": "text",
                        "text": "3",
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "size": "sm",
                        "color": "#555555",
                        "text": "土地所有權人"
                    },
                    {
                        "type": "text",
                        "text": "$7.31",
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                    ]
                }
                ]
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                {
                    "type": "text",
                    "text": "同意備案編號 ",
                    "size": "xs",
                    "color": "#aaaaaa",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": "TNN-NMSL69420",
                    "color": "#aaaaaa",
                    "size": "xs",
                    "align": "end"
                }
                ]
            }
            ]
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
    }
        )
        )


if __name__ == "__main__":
    app.run(debug=True)
