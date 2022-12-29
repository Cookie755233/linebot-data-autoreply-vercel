import os
import re
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

from msg.carousel import *
from utils.ls_search import search_applicants_by_parcel, search_info_by_applicant


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
        line_bot_api.reply_message(event.reply_token, TextSendMessage("Hello!"))

    if re.match("查詢地號", user_message):
        if not len(user_message.split('\n')) == 4:
            reply_message = "請輸入正確格式:\n查詢地號\nＯＯ區(必須輸入正確行政區)\nＯＯ段(必須輸入正確地段)\nＯＯＯ(支持模糊匹配)"
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(reply_message))
            return
        CAROUSEL_CONTAINER = {"type": "carousel", "contents": []}
        _, district, section, parcel = user_message.split("\n")

        result = list(search_applicants_by_parcel(district, section, parcel))
        if not result:
            reply_message = f"查無「{district}{section}{parcel}地號」資料!"
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(reply_message))
            return
            
        insert_parcel_search_result(result, CAROUSEL_CONTAINER)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Search results", 
                            contents=CAROUSEL_CONTAINER))
        
    if re.match("查詢申請人", user_message):
        if len(user_message.split('\n')) != 2: 
            reply_message = "請輸入正確格式:\n查詢申請人\nＯＯＯ(支持模糊匹配)"
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(reply_message))
            return
        
        CAROUSEL_CONTAINER = {"type": "carousel", "contents": []}
        _, name = user_message.split('\n')
        
        result = list(search_info_by_applicant(name))
        
        
        insert_applicant_search_result(result, CAROUSEL_CONTAINER)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Search results", 
                            contents=CAROUSEL_CONTAINER))


if __name__ == "__main__":
    app.run(debug=True)
