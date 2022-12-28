
from pymongo import MongoClient
import numpy as np
import pymongo
import datetime as dt
# password = os.getenv("MONGO_DB_PASSWORD")
USERNAME = 'cookie'
PASSWORD = "Cokie7523"

def _connect_mongo(username=USERNAME,
                   password=PASSWORD,
                   db='basic') -> MongoClient:
    """ A util for making a connection to mongo """
    mongo_uri = f"mongodb+srv://{username}:{password}@cluster0.xveirqo.mongodb.net/test?retryWrites=true&w=majority"
    client = MongoClient(mongo_uri)

    return client



# def create_parcel_collection(collection: pymongo.collection.Collection):
#     df = pd.read_excel('/Users/cookie/Desktop/ls20221220_tmp.xlsx')
#     df.fillna(np.nan)
#     df = df[['PN', 'TNAME', 'SECNAME', 'SECT', 'LANDNO8', 'LAND_NO', 
#             'AREA', 'AA11', 'AA12', 'AA08', 'AA16', 'AA17',
#             'BBType', 'BB09', 'Mng']]
#     df.columns = ['_id', 'districtName', 'sectionName', 'prefix', 'prcl8', 'prcl',
#                 'area', 'landUseZoning', 'landUseType', 'landCategory', 'presentValue', 'landValue',
#                 'ownershipType', 'owner', 'admin']
#     df = df.drop_duplicates()
#     df = df.astype({
#         '_id': 'str',
#         'prefix': 'str',
#         'prcl8': 'str',
#         'prcl': 'str',
#         'landCategory': 'category',
#         'landUseZoning': 'category',
#         'landUseType': 'category',
#         })
#     parcel_data = df.to_dict('records')
#     collection.insert_many(parcel_data)

# def create_applicants_collection(collection: pymongo.collection.Collection):
#     df = pd.read_excel('/Users/cookie/Desktop/ls20221220_tmp.xlsx')
#     df.fillna(np.nan)

#     df = df[['APPL', 'SESS', 'C_AREA', "CAP", 'STAT', 'PN',
#             'ALUC_DT', 'EA_DT', 'LCC_DT', 'LCR_DT', 
#             'AJOC', 'BLDG', 'NBR', 'ESA', 'INR', 'EXPLICIT']]
#     df.columns = ['name', 'session', 'caseArea', 'capacity', 'status', 'parcels',
#                 'agriLandUseChangeDate', 'establishmentApprovalDate', 'landUseChangeDate', 'landUseChangeRegisDate',
#                 'isAdjacent', 'isBuilding', 'isNearbyResident', 'isSensitive', 'isInner', 'isExplicit']

#     def is_true(s):
#         try:    return 'X' in s.lower()
#         except: return True

#     def correct_dt(s):
#         if not s: return pd.NaT
#         try:
#             s = str(s)
#             y,m,d = map(int, map(float, [s[:3], s[3:5], s[5:]]))
#             y = y + 1911
#         except:
#             return pd.NaT
        
#         return dt.datetime.strptime(f'{y}-{m}-{d}', '%Y-%m-%d')

#     df.agriLandUseChangeDate = df.agriLandUseChangeDate.apply(correct_dt)
#     df.establishmentApprovalDate = df.establishmentApprovalDate.apply(correct_dt)
#     df.landUseChangeDate = df.landUseChangeDate.apply(correct_dt)
#     df.landUseChangeRegisDate = df.landUseChangeRegisDate.apply(correct_dt)
#     df[['isAdjacent', 'isBuilding', 'isNearbyResident', 'isSensitive', 'isInner', 'isExplicit']] =\
#         df[['isAdjacent', 'isBuilding', 'isNearbyResident', 'isSensitive', 'isInner', 'isExplicit']].apply(is_true)
#     df.status = df.status.astype('category')

#     gf = df.groupby(['name', 'session', "caseArea"]).agg( lambda x: ','.join(map(str, list(set(x)))) ).reset_index()
#     gf.parcels = gf.parcels.apply(lambda x : x.split(','))
#     appl_data = gf.to_dict('records')
#     collection.insert_many(appl_data)

# * connect to db
# client = _connect_mongo()
# ls = client.ls
# * create collection
# parcel = ls.parcel
# applicant = ls.applicant
# * insert data
# create_parcel_collection(parcel)
# create_applicants_collection(applicant)


def search_applicants_by_parcel(user_input: str,
                                parcel: pymongo.collection.Collection):
    _, district, section, number = user_input.split('\n')
    result = parcel.aggregate([
            {
                "$match":{
                    "$and":[
                        {"districtName": {"$regex": f'{district}'}},
                        {"sectionName": f'{section}'},
                        {"prcl": {"$regex": f'{number}'}}
                    ]
                } 
            },
            {
                "$lookup":{
                    "from": "applicant",
                    "localField": "_id",
                    "foreignField": "parcels",
                    "as": "applicants"
                }
            },
            {
                "$project":{
                    "districtName":1,
                    "sectionName":1,
                    "prcl":1,
                    "applicantCount": {
                        "$size": { "$ifNull": [ "$applicants", [] ] }},
                    "applicants": 1
                }
            }
        ])
    
    
    return result


def search_info_by_keywords(user_input: str,
                            applicant: pymongo.collection.Collection):
    _, keyword = user_input.split('\n')
    result = applicant.aggregate([
    {
        "$match":{ 
            "$and":[
                {"name": {"$regex": keyword}},
                {"status": "已核准"}
            ]
        }
    },
    {
        "$lookup":{
            "from": "parcel",
            "localField": "parcels",
            "foreignField": "_id",
            "as": "parcel_comprehensive"
        }
    },
    ])
    
    return result

# pprint(list(search_applicants_by_parcel('查詢地號\n新營區\n後鎮段\n676', parcel)))
# pprint(list(search_info_by_keywords('查詢關鍵字\n山', applicant)))