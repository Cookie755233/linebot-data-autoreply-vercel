
import re
from db.mongo import read_mongo

def read_user_message(user_message: str):
    if re.match('hello', user_message):
        return 'Hi! what can i help'
    
    if re.match('bye', user_message):
        return 'Cya!'

    if re.match('title', user_message):
        df = read_mongo()
        
        return ','.join(df.columns)
    
    return