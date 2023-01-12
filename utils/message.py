
import re
from typing import Optional
from linebot.models import TextSendMessage, FlexSendMessage

from utils.query import *
from utils.compose import *
import const.error as ERROR


class ConfigParser:
    UNIT = {'公尺': 1, '米': 1, 'm': 1, '': 1, '公里': 1000, 'km': 1000}
    RESULT = ["#全文檢還", "#審查中", "#撤件", "#核准", "#補正", "#駁回"]

    
    def __init__(self) -> None:
        self.nearby = None
        self.maxDistance = None
        self.selectDistrict = None
        self.selectResult = None

    def __repr__(self) -> str:
        return f'''\
            [ CONFIG ]
            >> nearby: {self.nearby}
            >> maxDistance: {self.maxDistance}
            >> selectDistrict: {self.selectDistrict}
            >> selectResult: {self.selectResult}'''
    
    def parse(self, configs):
        for config in configs:
            if config.startswith('#鄰近'):
                self._register_nearby_config(config)
                continue
            
            if config.startswith('#'):
                self._register_subquery_config(config)
        return self
    
    def _register_nearby_config(self, config: str) -> None:
        try:
            distance, unit = re.findall(
                r'([0-9]*[.]?[0-9]+)(公里|公尺|米|m|km)?', config)[0]
        except ValueError:
            return 
        
        self.nearby = True
        self.maxDistance = float(distance) * self.UNIT[unit]
    
    def _register_subquery_config(self, config: str) -> None:
        if '區' in config or '段' in config:
            try:
                district, _ = re.findall(r'(.*?區)?(.*?段)?', config[1:])[0]
                district = None if not district else district
            except ValueError: 
                return 
            
            self.selectDistrict = district or self.selectDistrict
            
        elif config in self.RESULT:
            self.selectResult = config[1:]
    
    
class MessageHandler:
    def __init__(self) -> None:
        self.user_messages = None
        self.status = None
        self.config = None
        self.search_result = []
        
    def inspect(self, user_message: str):
        self.user_messages = self._unify(user_message)
        self.status = self._validate() or None
        
        if self.status: 
            return
        
        query_type, query, *configs = self.user_messages
        self.config = ConfigParser().parse(configs)
        self.status, self.search_result = \
            self._select_query(query_type)(query=query,
                                            nearby=self.config.nearby,
                                            maxDistance=self.config.maxDistance, 
                                            selectDistrict=self.config.selectDistrict,
                                            selectResult=self.config.selectResult)
            
    @property    
    def response(self): # -> linebot.models
        return self._compose_response(self.status, self.search_result)
        
        
    def _unify(self, message: str) -> list:
        return list(map(lambda x: x.replace('＠', '@').replace('＃', '#'),
                        message.splitlines())) 
        
    def _validate(self) -> Optional[int]:
        if len(self.user_messages) < 2:
            return 400
        if self.user_messages[0] not in ['@查詢', '@查詢地號']:
            return 400
        

    def _select_query(self, query_type):
        USE_FUNC = {
            '@查詢': search_applicants,
            '@查詢地號': search_parcels
        }
        return USE_FUNC.get(query_type)
    
    
    def _compose_response(self, status, search_result=None):
        if status > 300:
            return {
                301: TextSendMessage(ERROR.APPLICANT_NOT_FOUND_ERROR),
                303: TextSendMessage(ERROR.PARCEL_NOT_FOUND_ERROR),
                400: TextSendMessage(ERROR.USER_INPUT_ERROR)
            }.get(status)
            
        else:
            f = {
                201: compose_applicant_results,
                202: compose_applicant_nearby_results,
                203: compose_parcel_results,
                204: compose_parcel_nearby_results
            }.get(status)

            return FlexSendMessage(alt_text="Search Results",
                                   contents = f(search_result))