
import re
from typing import Optional
from linebot.models import TextSendMessage, FlexSendMessage

from utils.query import Config, Query
from utils.compose import (
    compose_applicant_results, compose_applicant_nearby_results, 
    compose_parcel_results, compose_parcel_nearby_results
)
import const.error as ERROR


class NoIndicatorError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self):
        return f'The user is not calling LineBot!'
    
    
    

class ContentManager:
    def __init__(self, user_message=None, status=None, search_result=None) -> None:
        self.user_messages = user_message
        self.status = status
        self.search_result = search_result
        
    def inspect(self, user_message: str):
        self.user_messages = self._unify(user_message)
        self.status = self._validate() or None
        if self.status: 
            return self
        
        instruction, query, *configs = self.user_messages
        query = Query(instruction=instruction,
                      query=query,
                      config = Config.from_configs(configs))
        self.status, self.search_result = query.execute()
        
        return self

    @property
    def have_search_result(self):
        if self.search_result: return True
        return False
    
    @property    
    def response(self): # -> linebot.models?
        return self._compose_response(self.status, self.search_result)
        
        
    def _unify(self, message: str) -> list:
        return list(map(lambda x: x.replace('＠', '@').replace('＃', '#'),
                        message.splitlines())) 
        
        
    def _validate(self) -> Optional[int]:
        if not self.user_messages[0].startswith('@'):
            return 999
        if len(self.user_messages) < 2:
            return 400
        if not self.user_messages[0].startswith('@'): #? Not a search attempt
            return 999
        if self.user_messages[0] not in ['@查詢', '@查詢地號']:
            return 400
        if self.user_messages[0] == '@查詢地號' and \
            not re.match(r'(.*區)(.*段)(\d{1,4}-?\d{0,4})地?號?', self.user_messages[1]):
                return 400
            
    
    def _compose_response(self, status, search_result=None):
        if status == 999:
            raise NoIndicatorError
        
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