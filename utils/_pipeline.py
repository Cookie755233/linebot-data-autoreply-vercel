
from pymongo.collection import Collection

def _search_nearby(x: float, y: float,
                   maxDistance=1000) -> list[set]:
    stage = [
        {
            '$geoNear': {
                'near': {
                    'type': 'Point', 
                    'coordinates': [x, y]
                }, 
                'distanceField': 'dist', 
                'maxDistance': maxDistance, 
                'query': {}, 
                'spherical': True
            }
        }
    ]
    
    return stage


def _search_keyword(keyword: str, 
                    maxEdits=2,
                    min_searchScore=1, 
                    limit=0) -> list[set]:
    stage = [
        {
            '$search': {
                'index': 'keyword_index', 
                'text': {
                    'query': keyword, 
                    'path': 'applicantName', 
                    'fuzzy': {
                        'maxEdits': maxEdits
                    }
                }
            }
        },
        {
            '$set': {
                'searchScore': {
                    '$meta': 'searchScore'
                }
            }
        },
        {
            '$match': {
                'searchScore': { '$gt': min_searchScore }
            }
        },
        {
            '$sort': { 'searchScore': 1}
        },
    ]
    if limit:
        stage.append(
            {
                '$limit': limit
            }
            )
    
    return stage


def _search_parcel(district: str,
                   section: str,
                   number: str) -> list[set]:
    stage = [
        {
            '$match': {
                "$and":[
                    {"districtName": district},
                    {"sectionName": section},
                    {"prcl": {"$regex": f"{number}"}}
                ]
            } 
        }, 
        {
            '$lookup': {
                'from': 'applicants', 
                'localField': '_id', 
                'foreignField': 'georeferencedParcels', 
                'as': 'relatedParcels'
            }
        }
    ]
    return stage
