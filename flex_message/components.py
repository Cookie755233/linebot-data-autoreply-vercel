
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
                                  subtitle,             #* subtitle
                                  *args,                #* must have paired key & val, or will raise StopIteration
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
                        "wrap": True,
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

