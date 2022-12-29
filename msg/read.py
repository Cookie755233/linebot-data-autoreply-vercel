
import re

def read_user_message(user_message: str):
    if re.match("bye", user_message):
        return "Cya!"

    
def _is_valid_parcel(user_message: str) -> bool:
    return len(user_message.split('\n')) == 4
    
def _is_valid_name(user_message: str) -> bool:
    return 1 < len(user_message.split('\n')) < 4




'''
status = None?

read user message
    -> search parcel

        [ check is query valid ]
        -> valid:
            -> result = query output
                -> if null:
                    status = 301
                    send text(error message)

                -> else:
                    status = 201
                    send flex(result)


        -> invalid:
            status = 401
            -> use send text(constants.status.message)

'''