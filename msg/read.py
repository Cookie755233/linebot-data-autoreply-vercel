
import re

def read_user_message(user_message: str):
    if re.match("hello", user_message):
        return "Hi! what can i help"
    
    if re.match("bye", user_message):
        return "Cya!"

    
def _is_valid_parcel(user_message: str) -> bool:
    return len(user_message.split('\n')) == 4
    
def _is_valid_name(user_message: str) -> bool:
    return 1 < len(user_message.split('\n')) < 4