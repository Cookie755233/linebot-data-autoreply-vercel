
from db._connect import _connect_mongo
from db._pandas_util import reip_readfile
from db._reip_handler import reip_to_json
from db._reip_handler import reip_to_json
from db._parcel_handler import reip_to_geojson
from pymongo import GEO2D

DATE = input('請選擇同意備案日期（由GIS導出，請存到桌面，csv格式），格式：yyyymmdd\n')

#? <-- Load mongo client -->
client = _connect_mongo('cookie', 'Cokie7523')
applicants = client.reip.applicants
parcels = client.reip.parcels

#? <-- Drop both collections -->
print('drop collections')
applicants.drop()
parcels.drop()

#? <-- push newer version to MongoDB --> 
## select data
pr = reip_readfile(f'/Users/cookie/Desktop/{DATE}.csv', 'pr')
er = reip_readfile(f'/Users/cookie/Documents/Work/494計畫/陽光電城資訊網/案場介接/設備登記/RAWDATA/設備登記總表_{DATE}00.xlsx', 'er')
prcl = reip_readfile(f'/Users/cookie/Desktop/{DATE}.csv', 'parcel')
## insert applicants into db
print('inserting applicants')
applicants.insert_many(reip_to_json(pr, er))
## insert parcels into db
print('inserting parcels')
parcels.insert_many(reip_to_geojson(prcl))

#? <-- create "center" field in `applicants` -->
print('creating `center` field')
applicants.aggregate([
    {
        '$lookup': {
            'from': 'parcels', 
            'localField': 'georeferencedParcels', 
            'foreignField': '_id', 
            'pipeline': [
                {
                    '$project': {
                        '_id': 0, 
                        'x': {'$first': '$location.coordinates'}, 
                        'y': {'$last': '$location.coordinates'}
                    }
                }
            ], 
            'as': 'detailedParcels'
        }
    },
    {
        "$set": {
            "center": {
                "type": "Point",
                "coordinates": [
                    {"$avg": "$detailedParcels.x"},
                    {"$avg": "$detailedParcels.y"}
                    ]
                },
        "detailedParcels": "$$REMOVE"
        }
    },
    {
        "$merge": {
            "into": "applicants"
        }
    }
])

#? <-- create 2dsphere index -->
print('create 2dsphere index')
applicants.create_index([('center', GEO2D)])
parcels.create_index([('location', GEO2D)])