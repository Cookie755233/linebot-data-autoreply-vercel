import os
import re
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, PostbackEvent,
    TextMessage, TextSendMessage, FlexSendMessage, LocationSendMessage
)
from utils.read_message import inspect_user_message
from utils.compose import (
    compose_applicant_results, compose_applicant_nearby_results,
    compose_parcel_results, compose_parcel_nearby_results
)

import const.error as ERROR_MESSAGE

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
    status, return_value = inspect_user_message(user_message)
    
    reply_message[status](return_value)
    
    if status == 201:
        flex_message = compose_applicant_results(return_value)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Search results", 
                            contents=flex_message))
    if status == 202:
        flex_message = compose_applicant_nearby_results(return_value)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Search results", 
                            contents=flex_message))

    if status == 203:
        flex_message = compose_parcel_results(return_value)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Search results", 
                            contents=flex_message))

    if status == 204:
        flex_message = compose_parcel_nearby_results(return_value)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Search results", 
                            contents=flex_message))

    if status == 400:
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(ERROR_MESSAGE.USER_INPUT_ERROR)
        )

@line_handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data.startswith('location'):
        longitude, latitude = re.findall(
            r'[0-9]*[.]?[0-9]+', event.postback.data)
        
        line_bot_api.reply_message(
            event.reply_token,
            LocationSendMessage(
                title = "TITLE",
                address = "ADDRESS",
                latitude = float(latitude),
                longitude = float(longitude)
                )
            )   

if __name__ == "__main__":
    app.run(debug=True)

