
from utils.query import search_keyword, search_parcel
import re


def read_messages(user_message: str):
    '''
                查詢
    -------------------------------
    REQUIRED:
    -- @查詢地號           / @查詢
    -- (.*區)(.*段)(.*號)  / 申請人
    
    OPTIONAL:
    -- @鄰近100[公尺|米|公里|m|km]
    -------------------------------
    '''
    #? <--  parse user messages -->
    message_lists = user_message.lower().replace('＠', '@').splitlines()
    if not len(message_lists) >= 2: 
        return (400, )
    
    operator, keyword, *kwargs = user_message.lower().replace('＠', '@').splitlines()
    nearby, maxDistance = _kwargs_parser(kwargs)
    
    if operator == '@查詢':
        results = search_keyword(keyword, nearby, maxDistance)
        if not results:
            return 300, None
        return 201, results
    
    if operator == '@查詢地號':
        results = search_parcel(keyword, nearby, maxDistance)
        if not results:
            return 300, None
        return 202, results
    

    #! cannot use 3.10 yet?!
    # #? <--  search for the user queries -->
    # match operator:
    #     case '@查詢':rd, nearby, maxDistance)
    #         if not results:
    #         results = search_keyword(keywo
    #             return 300, None
    #         return 201, results
        
    #     case '@查詢地號':
    #         results = search_parcel(keyword, nearby, maxDistance)
    #         if not results:
    #             return 300, None
    #         return 202, results
        
    #     #TODO
    #     case '@統計申請人':
    #         return 
        
    #     case '@統計':
    #         return
        
    #     case _: 
    #         return
    #! the fuck 

    
    
def _kwargs_parser(kwargs: list): #! kwargs is "LIST"
    nearby = False
    maxDistance = 100
    UNIT = {
        '公尺': 1,
        '米': 1,
        '公里': 1000,
        'm': 1, 
        'km': 1000, 
        '': 1,
    }
    
    for kwarg in kwargs:
        if kwarg.startswith('@鄰近'):
            l = re.findall(
                r'([0-9]*[.]?[0-9]+)(公里|公尺|米|m|km)?', kwarg)
            if not l:
                return nearby, maxDistance

            dist, unit = l[0]
            nearby = True
            maxDistance = float(dist) * UNIT[unit]
    return nearby, maxDistance


