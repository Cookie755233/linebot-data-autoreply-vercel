import os
import re
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, PostbackEvent, TextMessage, LocationSendMessage
)

from utils.message import ContentManager
import const.error as ERROR_MESSAGE



line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

content_manager = ContentManager()

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
    # process user message
    content_manager.inspect(user_message=user_message)
    line_bot_api.reply_message(
        event.reply_token, 
        content_manager.response
    )
    #@ TODO: 
    #@ content_manger = ContentManager(api=line_bot_api)  #top
    #@ content_manager.response(user_message)
    
    
@line_handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data.startswith('location'):
        longitude, latitude, title, address = re.findall(
            r'location: ([0-9]*[.]?[0-9]+), ([0-9]*[.]?[0-9]+) \| title: (.*) \| address: (.*)',
            event.postback.data)[0]
        
        line_bot_api.reply_message(
            event.reply_token,
            LocationSendMessage(
                title = title,
                address = address,
                latitude = float(latitude),
                longitude = float(longitude)
                )
            )   



if __name__ == "__main__":
    app.run(debug=True)

