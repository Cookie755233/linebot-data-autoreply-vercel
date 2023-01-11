
from db._parcel_handler import reip_to_geojson
from db._reip_handler import reip_to_json
from db._pandas_util import reip_readfile
from db._connect import _connect_mongo
from pprint import pprint
from utils.message import MessageHandler


def con():
    client = _connect_mongo('cookie', 'Cokie7523')
    return client

h =  MessageHandler()
h.inspect('@查詢地號\n七股區七股段1號').execute()

pprint(h.search_result)
