from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from msg.reply import read_user_message
from msg.carousel import *
# from msg.reply import read_user_message
import os

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
    reply = read_user_message(user_message)
    
    if isinstance(reply, str):
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(reply))
        
    else:
        carousel_container = {"type": "carousel", 
                              "contents": []}
        insert_search_result(reply, carousel_container)
        
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text='Search results',
                            contents=carousel_container))


if __name__ == "__main__":
    app.run(debug=True)
