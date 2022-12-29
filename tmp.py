# from linebot import LineBotApi, WebhookHandler
# from pprint import pprint
# from db.mongo import _connect_mongo, search_applicants_by_parcel

# # 載入對應的函式庫
# from linebot.models import (
#     FlexSendMessage,
#     BubbleContainer,
#     ImageComponent,
#     CarouselTemplate,
#     CarouselColumn,
#     PostbackAction,
#     Action,
#     MessageAction,
#     URIAction,
#     TemplateSendMessage,
# )

# line_bot_api = LineBotApi(
#     "cKElXBSd7IPz/OWxOhOxdtowD6S+1ApYDkbulNjtgWgvd5NBbcyAyO1bWqiStrR5ervVxbgtti/BN+JUPzeqxVspnOI72bjNlsAsO7jnBwR7qwn+PwDTzU/4xhKmhT0s58zcdh5dFOFxmzCJPKVCYAdB04t89/1O/w1cDnyilFU="
# )


# ls = _connect_mongo().ls
# parcel = ls.parcel

# usr_input = "查詢地號\n七股區\n七股段\n10"
# applicant_search_result = search_applicants_by_parcel(usr_input, parcel)

# def create_bubble():
#     return {
#         "type": "bubble",
#         "body": {"type": "box", 
#                  "layout": "vertical",
#                  "contents": []},
#         "styles": {"footer": {"separator": True}}
#     }


# def insert_body_contents_TITLE(bubble, dist, sect, prcl, i, cnt):
#     bubble['body']['contents'] += [
#         {
#             "type": "text",
#             "text": f"RESULT {i+1}",
#             "weight": "bold",
#             "color": "#1DB446",
#             "size": "xs",
#         },
#         {
#             "type": "text",
#             "text": f"{dist}{sect}{prcl}地號",
#             "weight": "bold",
#             "size": "lg",
#             "margin": "md",
#         },
#         {
#             "type": "text",
#             "text": f"共計 {cnt} 個申請案件",
#             "size": "xs",
#             "color": "#aaaaaa",
#             "wrap": True,
#         },
#     ]
#     return bubble


# def insert_body_contents_SEP(bubble):
#     bubble['body']['contents'].append(
#         {"type": "separator", "margin": "xxl"}
#     )
#     return bubble


# def insert_body_contents_ITEM(bubble, name, cap, area, stat):
#     bubble['body']['contents'] += [
#         {
#             "type": "box",
#             "layout": "vertical",
#             "margin": "xxl",
#             "spacing": "sm",
#             "contents": [
#                 {
#                     "type": "text",
#                     "text": f"{name}",
#                     "size": "md",
#                     "weight": "bold",
#                     "color": "#46844f",
#                 },
#                 {
#                     "type": "box",
#                     "layout": "horizontal",
#                     "contents": [
#                         {
#                             "type": "text",
#                             "text": "設置容量",
#                             "size": "sm",
#                             "color": "#555555",
#                             "flex": 0,
#                         },
#                         {
#                             "type": "text",
#                             "text": f"{cap:,.2f}  kW",
#                             "size": "sm",
#                             "color": "#111111",
#                             "align": "end",
#                         },
#                     ],
#                 },
#                 {
#                     "type": "box",
#                     "layout": "horizontal",
#                     "contents": [
#                         {
#                             "type": "text",
#                             "text": "土地面積",
#                             "size": "sm",
#                             "color": "#555555",
#                             "flex": 0,
#                         },
#                         {
#                             "type": "text",
#                             "text": f"{area:,.2f}  m2",
#                             "size": "sm",
#                             "color": "#111111",
#                             "align": "end",
#                         },
#                     ],
#                 },
#                 {
#                     "type": "box",
#                     "layout": "horizontal",
#                     "contents": [
#                         {
#                             "type": "text",
#                             "text": "案件狀態",
#                             "size": "sm",
#                             "color": "#555555",
#                             "flex": 0,
#                         },
#                         {
#                             "type": "text",
#                             "text": f"{stat}",
#                             "size": "sm",
#                             "color": "#111111",
#                             "align": "end",
#                         },
#                     ],
#                 },
#             ],
#         },
#     ]
#     return bubble


# carousel_container = {"type": "carousel", "contents": []}

# for i, result in enumerate(applicant_search_result):
#     dist = result["districtName"]
#     sect = result["sectionName"]
#     prcl = result["prcl"]
#     cnt = int(result["applicantCount"])
#     applicants = result["applicants"]
    
#     bubble = create_bubble()
#     bubble = insert_body_contents_TITLE(bubble, dist, sect, prcl, i, cnt)
#     bubble = insert_body_contents_SEP(bubble)
    
#     for j, a in enumerate(applicants):
#         name = a["name"]
#         cap = float(a["capacity"])
#         area = float(a["caseArea"])
#         stat = a['status']
#         bubble = insert_body_contents_ITEM(bubble, name, cap, area, stat)
        
#         if j < cnt - 1:
#              bubble = insert_body_contents_SEP(bubble)

#     carousel_container["contents"].append(bubble)



# try:
#     line_bot_api.push_message(
#         "U24b0637188410e7322658cd63fbe85b9",
#         FlexSendMessage(alt_text="hello", contents=carousel_container),
#     )
# except Exception as e:
#     pprint(e)

