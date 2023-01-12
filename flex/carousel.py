
from utils.helper import pairwise

class Carousel:
    def __init__(self) -> None:
        self.container = {"type": "carousel", "contents": []}
    
    def insert_bubble(self, bubble):
        self.container["contents"].append(bubble)
        
class Bubble:
    def __init__(self) -> None:
        self.bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical", 
                    "contents": []
                    },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "spacing": "sm"
                }
            }

    def insert_body_contents_TITLE(self, 
                                   status,          #* 上標（綠字:核准/ 紅字:else）
                                   title,
                                   appendix,
                                   top_color='#46844f',
                                   title_color="#000000",
                                   top_size='sm',
                                   title_size='lg',
                                   appendix_size='xxs',
                                   top_right_text='-',
                                   top_right_size='sm'):
        self.bubble["body"]["contents"] += [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": status,
                    "weight": "bold",
                    "color": top_color,
                    "size": top_size
                },
                {
                    "type": "text",
                    "text": top_right_text,
                    "align": "end",
                    "color": "#aaaaaa",
                    "size": top_right_size
                }
                ]
            },
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "size": title_size,
                "margin": "md",
                "wrap": True,
                "color": title_color
            },
            {
                "type": "text",
                "text": appendix,
                "size": appendix_size,
                "color": "#aaaaaa",
                "wrap": True,
            },
        ]
    
    
    def insert_body_contents_ITEM(self,
                                  subtitle,     #* subtitle
                                  *args,        #* must have paired key & val, or will raise StopIteration
                                  subtitle_size='md',
                                  subtitle_color='#46844f',
                                  item_size='sm', 
                                  ):
        args = list(args)
        items = []
        for key, val in pairwise(args):
            items.append(_create_box(key, val, size=item_size))
        
        self.bubble["body"]["contents"] += [
            {
                "type": "box",
                "layout": "vertical",
                "margin": "xxl",
                "spacing": "sm",
                "contents": [
                    #? <-- subtitle -->
                    {
                        "type": "text",
                        "text": subtitle,
                        "size": subtitle_size,
                        "weight": "bold",
                        "color": subtitle_color,
                        "wrap": True
                    },
                    #? <-- items -->
                    *items
                ],
            },
        ]
        
    
    def insert_body_contents_FOOTER(self, 
                                    key,
                                    val):
        self.bubble["body"]["contents"] += [
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": key,
                        "size": "xxs",
                        "color": "#aaaaaa",
                        "flex": 0,
                    },
                    {
                        "type": "text",
                        "text": val,
                        "color": "#aaaaaa",
                        "size": "xxs",
                        "align": "end",
                    },
                ],
            }
        ]


    def insert_body_contents_SEP(self):
        self.bubble["body"]["contents"].append({"type": "separator", "margin": "xxl"})
        
        
    def insert_footer_contents_BOTTOM(self,
                                      longitude: float,
                                      latitude: float, 
                                      title=None,
                                      address=None,
                                      label='取得位置資訊', 
                                      displayText='取得位置資訊'):
        self.bubble['footer']['contents'].append(
            {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": label,
                    "data": f"location: {longitude}, {latitude} | title: {title} | address: {address}",
                    "displayText": displayText
                },
            }
        )


def _create_box(key, val, size='sm') -> dict:
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": key,
                "size": size,
                "color": "#555555",
                "flex": 0,
            },
            {
                "type": "text",
                "text": val,
                "size": size,
                "color": "#111111",
                "align": "end",
            },
        ],
    }



# #! <===== deprecated =====>
# #? <-- create bubble container --> 
# def _create_bubble():
#     return {
#         "type": "bubble",
#         "body": {
#             "type": "box",
#             "layout": "vertical", 
#             "contents": []
#             },
#         "footer": {
#             "type": "box",
#             "layout": "vertical",
#             "contents": [],
#             "spacing": "sm"
#         }
#     }


# #? <-- insert contents into bubbles: sub functions -->
# def _insert_body_contents_TITLE(bubble, 
#                                top,     #* 上標（綠字/紅字）
#                                title,   
#                                appendix,
#                                top_color="#46844f"
#                                ):    
#     bubble["body"]["contents"] += [
#         {
#             "type": "text",
#             "text": top,
#             "weight": "bold",
#             "color": top_color,
#             "size": "sm",
#         },
#         {
#             "type": "text",
#             "text": title,
#             "weight": "bold",
#             "size": "lg",
#             "margin": "md",
#             "wrap": True
#         },
#         {
#             "type": "text",
#             "text": appendix,
#             "size": "xs",
#             "color": "#aaaaaa",
#             "wrap": True,
#         },
#     ]
#     return bubble


# def _insert_body_contents_ITEM(bubble, 
#                               subtitle,     #* subtitle
#                               key_1, val_1, #* attribute 1
#                               key_2, val_2, #* attribute 2
#                               key_3, val_3, #* attribute 3
#                               ):
#     bubble["body"]["contents"] += [
#         {
#             "type": "box",
#             "layout": "vertical",
#             "margin": "xxl",
#             "spacing": "sm",
#             "contents": [
#                 {
#                     "type": "text",
#                     "text": subtitle,
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
#                             "text": key_1,
#                             "size": "sm",
#                             "color": "#555555",
#                             "flex": 0,
#                         },
#                         {
#                             "type": "text",
#                             "text": val_1,
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
#                             "text": key_2,
#                             "size": "sm",
#                             "color": "#555555",
#                             "flex": 0,
#                         },
#                         {
#                             "type": "text",
#                             "text": val_2,
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
#                             "text": key_3,
#                             "size": "sm",
#                             "color": "#555555",
#                             "flex": 0,
#                         },
#                         {
#                             "type": "text",
#                             "text": val_3,
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


# def _insert_body_contents_FOOTER(bubble, 
#                                 key_1, val_1):
#     bubble["body"]["contents"] += [
#         {
#             "type": "box",
#             "layout": "horizontal",
#             "margin": "md",
#             "contents": [
#                 {
#                     "type": "text",
#                     "text": key_1,
#                     "size": "xs",
#                     "color": "#aaaaaa",
#                     "flex": 0,
#                 },
#                 {
#                     "type": "text",
#                     "text": val_1,
#                     "color": "#aaaaaa",
#                     "size": "xs",
#                     "align": "end",
#                 },
#             ],
#         }
#     ]
#     return bubble


# def _insert_body_contents_SEP(bubble):
#     bubble["body"]["contents"].append({"type": "separator", "margin": "xxl"})
#     return bubble


# def _insert_footer_contents_BOTTOM(bubble):
#     bubble['footer']['contents'].append(
#         {
#             "type": "button",
#             "action": {
#                 "type": "postback",
#                 "label": "取得位置資訊",
#                 "data": "location",
#                 "displayText": "取得位置資訊"
#             },
#         }
#     )
#     return bubble





# # #? <-- insert ls search result into bubbles: main functions -->
# def __insert_parcel_search_result(search_result, carousel_container):
#     for i, result in enumerate(search_result):
#         _id  = result['_id']
#         dist = result["districtName"]
#         sect = result["sectionName"]
#         prcl = result["prcl"]
#         luz  = result['landUseZoning']
#         lut  = result['landUseType']
#         applicants = result["applicants"]
        
#         bubble = _create_bubble()
#         bubble = _insert_body_contents_TITLE(bubble, 
#                                             f'RESULT {i+1}',
#                                             f"{dist}{sect}{prcl}地號",
#                                             f"{luz} - {lut}")
#         bubble = _insert_body_contents_SEP(bubble)

#         for a in applicants:
#             name = a["name"]
#             cap = float(a["capacity"].replace(',', ''))
#             area = float(a["caseArea"].replace(',', ''))
#             stat = a["status"]

#             bubble = _insert_body_contents_ITEM(bubble, 
#                                                name, 
#                                                "設置容量", f"{cap:,.2f}  kW",
#                                                "土地面積", f"{area:,.2f}  m2",
#                                                "案件狀態", stat)
#             bubble = _insert_body_contents_SEP(bubble)

#         bubble = _insert_body_contents_FOOTER(bubble, 
#                                              "PARCEL ID", f"#{_id}")
#         bubble = _insert_footer_contents_BOTTOM(bubble)
#         carousel_container["contents"].append(bubble)


# def __insert_applicant_search_result(search_result, carousel_container):
#     for i, result in enumerate(search_result):
#         if i >= 11: break

#         _id  = str(result['_id'])
#         sess = result['session']
#         name = result['name']
#         cap  = float(result['capacity'].replace(',', ''))
#         area = float(result['caseArea'].replace(',', ''))
#         stat = result['status']
#         top_color = "#46844f" if stat == '已核准' else "#C28285"
        
#         bubble = _create_bubble()
#         bubble = _insert_body_contents_TITLE(bubble, 
#                                             stat,
#                                             name,
#                                             f"第 {sess} 次聯審會議",
#                                             top_color=top_color)
        
            
        
#         bubble = _insert_body_contents_SEP(bubble)
#         bubble = _insert_body_contents_ITEM(bubble,
#                                            "案件資訊概覽",
#                                            "設置容量", f"{cap:,.2f}  kW",
#                                            "土地面積", f"{area:,.2f}  m2",
#                                            "_placeHolder", "---")
#         bubble = _insert_body_contents_SEP(bubble)
#         bubble = _insert_body_contents_FOOTER(bubble, 
#                                              "ID", f"#{_id}")
#         bubble = _insert_footer_contents_BOTTOM(bubble)
#         carousel_container["contents"].append(bubble)
