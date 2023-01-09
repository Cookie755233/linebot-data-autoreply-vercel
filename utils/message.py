
from utils.query import search_keyword, search_parcel
import re


def inspect_user_message(user_message: str):
    '''            
    REQUIRED:
        - @查詢地號           / @查詢
        - (.*區)(.*段)(.*號)  / 申請人
    
    OPTIONAL:
        - #鄰近ＯＯ[公尺|米|公里|m|km]
        - #ＯＯ區 / ＯＯ段
        - #核准 / ...
    -------------------------------
    RETURNS:
        - status: int 
            201, 202, 203, 204, 301, 302, 400, 
        - resutls: list
            restuls of the user queries, None if status > 300
    
    '''
    
    #? <--  parse user messages -->
    message_lists = list(map(
        lambda x: x.replace('＠', '@').replace('＃', '#'), 
        user_message.splitlines()))
    if not len(message_lists) >= 2: 
        return (400, )
    
    config = Config()
    
    operator, keyword, *configs = message_lists
    config.parse(configs)
        
    #? <-- use search_keyword -->
    if operator == '@查詢':
        results = search_keyword(keyword=keyword, 
                                 nearby=config.nearby,
                                 maxDistance=config.maxDistance, 
                                #  selectDistrict=config.selectDistrict,
                                #  selectSection=config.selectSection, 
                                #  selectResult=config.selectResult
                                 )
        if not results:
            return 301+config.nearby, None
        return 201+config.nearby, results
    
    
    #? <-- use search_parcel -->
    if operator == '@查詢地號':
        results = search_parcel(keyword=keyword,
                                nearby=config.nearby,
                                maxDistance=config.maxDistance)
        if not results:
            return 302, None
        return 202, results
    
    
    
    
class Config:
    UNIT = {'公尺': 1, '米': 1, 'm': 1, '': 1, '公里': 1000, 'km': 1000}
    RESULT = ["#全文檢還", "#審查中", "#撤件", "#核准", "#補正", "#駁回"]
    def __init__(self, 
                 nearby=None, 
                 maxDistance=None, 
                 selectDistrict=None,
                 selectSection=None, 
                 selectResult=None) -> None:
        self.nearby = nearby
        self.maxDistance = maxDistance
        self.selectDistrict = selectDistrict
        self.selectSection = selectSection
        self.selectResult = selectResult
    
    def parse(self, configs: list):
        for config in configs:
            if config.startswith('#鄰近'):
                self.__register_nearby_config(config)
                continue
            
            if config.startswith('#'):
                self.__register_subquery_config(config)
    
    def __register_nearby_config(self, config: str) -> None:
        try:
            distance, unit = re.findall(
                r'([0-9]*[.]?[0-9]+)(公里|公尺|米|m|km)?', config)[0]
        except ValueError:
            return 
        
        self.nearby = True
        self.maxDistance = float(distance) * self.UNIT[unit]
    
    def __register_subquery_config(self, config: str) -> None:
        if '區' in config or '段' in config:
            try:
                district, section = re.findall(r'(.*?區)?(.*?段)?', config[1:])[0]
                district = None if not district else district
                section = None if not section else section
            except ValueError: 
                return 
            
            self.selectDistrict = district or self.selectDistrict
            self.selectSection = section or self.selectSection
            
        elif config in self.RESULT:
            self.selectResult = config[1:]
        
        
        
# def _kwargs_parser(kwargs: list): #! kwargs is "LIST"
#     nearby = False
#     maxDistance = 100
#     UNIT = {
#         '公尺': 1,
#         '米': 1,
#         '公里': 1000,
#         'm': 1, 
#         'km': 1000, 
#         '': 1,
#     }
    
#     for kwarg in kwargs:
#         if kwarg.startswith('@鄰近'):
#             l = re.findall(
#                 r'([0-9]*[.]?[0-9]+)(公里|公尺|米|m|km)?', kwarg)
#             if not l:
#                 return nearby, maxDistance

#             dist, unit = l[0]
#             nearby = True
#             maxDistance = float(dist) * UNIT[unit]
#     return nearby, maxDistance
