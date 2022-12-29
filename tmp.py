# import re
# from pprint import pprint

# from linebot import LineBotApi, WebhookHandler
# # 載入對應的函式庫
# from linebot.models import (
#     TextSendMessage,
#     FlexSendMessage,
# )

# from msg.read import _is_valid_parcel
# from msg.carousel import *
# from utils.ls_search import *

# line_bot_api = LineBotApi(
#     "cKElXBSd7IPz/OWxOhOxdtowD6S+1ApYDkbulNjtgWgvd5NBbcyAyO1bWqiStrR5ervVxbgtti/BN+JUPzeqxVspnOI72bjNlsAsO7jnBwR7qwn+PwDTzU/4xhKmhT0s58zcdh5dFOFxmzCJPKVCYAdB04t89/1O/w1cDnyilFU="
# )

# user_message = "地號\n七股區\n七股段\n445-10"

# def tmp():
#     if re.match("地1231號", user_message):
#         if not _is_valid_parcel(user_message):
#             print(1)
#             reply_message = "請輸入正確格式:\n查詢地號\nＯＯ區\nＯＯ段\nＯＯＯ"
#             line_bot_api.reply_message(
#                 'U24b0637188410e7322658cd63fbe85b9', TextSendMessage(reply_message)
#             )
#         else:
#             print(2)
#             CAROUSEL_CONTAINER = {"type": "carousel", "contents": []}
#             _, district, section, parcel = user_message.split("\n")

#             result = search_applicants_by_parcel(district, section, parcel)
#             insert_search_result(result, CAROUSEL_CONTAINER)

#             line_bot_api.reply_message(
#                 'U24b0637188410e7322658cd63fbe85b9',
#                 FlexSendMessage(alt_text="Search results", 
#                                 contents=CAROUSEL_CONTAINER),
#             )
#     else:
#         line_bot_api.reply_message(
#                 'U24b0637188410e7322658cd63fbe85b9', 
#                 TextSendMessage('what is going on')
#             )
#     return CAROUSEL_CONTAINER
