import os
import re
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

from msg.read import _is_valid_parcel
from msg.carousel import *
from utils.ls_search import search_applicants_by_parcel


line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

app = Flask(__name__)

# domain root
@app.route("/")
def home():
    return "Hello Cookie!"


@app.route("/webhook", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.type != "text":
        return

    user_message = event.message.text
    if re.match("hi", user_message):
        line_bot_api.reply_message(event.reply_token, 
                                   TextMessage("Hello!"))

    if re.match("地號", user_message):
        if not _is_valid_parcel(user_message):
            reply_message = "請輸入正確格式:\n查詢地號\nＯＯ區\nＯＯ段\nＯＯＯ"
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(reply_message))
            return

        CAROUSEL_CONTAINER = {"type": "carousel", "contents": []}
        _, district, section, parcel = user_message.split("\n")

        result = search_applicants_by_parcel(district, section, parcel)
        insert_search_result(result, CAROUSEL_CONTAINER)

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Search results", 
                            contents=CAROUSEL_CONTAINER),
        )


if __name__ == "__main__":
    app.run(debug=True)
