
from db._parcel_handler import reip_to_geojson
from db._reip_handler import reip_to_json
from db._pandas_util import reip_readfile

from db._connect import _connect_mongo
from pprint import pprint

def mainf():
    df = reip_readfile('/Users/cookie/Desktop/prcl_.csv', 'pr')
    edf = reip_readfile('/Users/cookie/Documents/Work/494計畫/陽光電城資訊網/案場介接/設備登記/RAWDATA/設備登記總表_2022120700.xlsx', 'er')

    j = reip_to_json(df, edf)

    return j


def mainp():
    df = reip_readfile('/Users/cookie/Desktop/prcl_.csv', 'parcel')
    return reip_to_geojson(df)

def con():
    client = _connect_mongo('cookie', 'Cokie7523')
    return client

# import numpy as np
# def q(applicants=con().reip.applicants):
#     pipe = _search_keyword('陸永祥', min_searchScore=3)
#     res = list(applicants.aggregate(pipe))
#     # for i, r in enumerate(res):
#     #     pprint((
#     #         r['applicantName'], r['position'], r['type'], 
#     #         r['totalCapacity'], r['landArea'],
#     #         ))
        
#     #     x, y = r['center']['coordinates']

#     #     pipe2 = _search_nearby(x, y, maxDistance=100)
#     #     resnb = list(applicants.aggregate(pipe2))
#     #     for n in resnb: 
#     #         pprint((
#     #         i, n['applicantName'], n['landArea'], n['totalCapacity']
#     #         ))


# def p(db=con().reip):
#     d, s, n = '七股區', '七股段', '10'
#     pipe = _search_parcel(d,s,n)
#     res = db.parcels.aggregate(pipe)
    
#     p2a = []
#     for idx, r in enumerate(res):
#         d,s,n = r['districtName'], r['sectionName'], r['prcl']
#         p2a.append((d+s+n, r['relatedParcels']))
#         # for i in r['relatedParcels']:
#         #     pprint((
#         #         i['applicantName'], i['position'], i['type'], 
#         #         i['totalCapacity'], i['landArea'], i['center']
#         #         ))
#     p2na = []
#     for p, rs in p2a:
#         for r in rs:
#             x, y = r['center']['coordinates']
#             geo_pipeline = _search_nearby(x, y, maxDistance=100)
#             geo_results = list(db.applicants.aggregate(geo_pipeline))
#             p2na.append( (p, geo_results) )
    
#     pprint(len(p2na))

from utils.query import search_parcels
from pprint import pprint
from utils.compose import compose_parcel_nearby_results

pprint(
    compose_parcel_nearby_results(
    search_parcels('七股區', '七股段', '10',
                           nearby=True, db=con().reip, 
                           limit=1, maxDistance=1000))
)