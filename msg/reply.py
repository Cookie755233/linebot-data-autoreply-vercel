
import re
from db.mongo import _connect_mongo, search_applicants_by_parcel

def read_user_message(user_message: str):
    if re.match("hello", user_message):
        return "Hi! what can i help"
    
    if re.match("bye", user_message):
        return "Cya!"

    if re.match("@地號", user_message):
        parcel = _connect_mongo().ls.parcel
        applicant_search_result = search_applicants_by_parcel(user_message, parcel)
        if not len(list(applicant_search_result)):
            return '查無案件'
        return applicant_search_result

    else:
        return "wat"