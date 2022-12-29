
from db.mongo import _connect_mongo

def search_applicants_by_parcel(district, section, number,
                                parcel=_connect_mongo().ls.parcel):
    result = parcel.aggregate([
            {
                "$match":{
                    "$and":[
                        {"districtName": {"$regex": f"{district}"}},
                        {"sectionName": f"{section}"},
                        {"prcl": {"$regex": f"{number}"}}
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
            # {
            #     "$project":{
            #         "districtName":1,
            #         "sectionName":1,
            #         "prcl":1,
            #         "applicantCount": {
            #             "$size": { "$ifNull": [ "$applicants", [] ] }},
            #         "applicants": 1
            #     }
            # }
        ])
    
    
    return result


def search_info_by_applicant(name: str,
                             applicant=_connect_mongo().ls.applicant):
    result = applicant.aggregate([
    {
        "$match":{ 
            "$and":[
                {"name": {"$regex": name}},
                # {"status": "已核准"}
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