
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
h.inspect('@查詢\n你媽\n＃七股區')
response = h.response

pprint(h)
