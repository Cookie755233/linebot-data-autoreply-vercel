
from pymongo.database import Database

from utils._pipeline import _search_keyword, _search_nearby, _search_parcel
from db._connect import _connect_mongo

USE_DATABASE = _connect_mongo().reip

def search_keyword(keyword: str, 
                   nearby=False,
                   maxDistance=100, 
                   limit=0,
                   db: Database=USE_DATABASE,
                   ) -> list:

    pipeline = _search_keyword(keyword,
                               maxEdits=1,
                               min_searchScore=1,
                               limit=limit)

    search_results = list(db.applicants.aggregate(pipeline))
    #? nearby not required
    if not nearby: 
        return search_results #! [ {applicants}, ... ]
    
    
    #? users wants all the cases nearby
    applicant_to_nearby_applicants = []
    for item in search_results:
        x, y = item['center']['coordinates']
        geo_pipeline = _search_nearby(x, y, maxDistance=maxDistance)
        geo_results = list(db.applicants.aggregate(geo_pipeline))
        applicant_to_nearby_applicants.append( (item, geo_results) )

    return applicant_to_nearby_applicants #! [ ({applicants}, {geo_results}), ... ]


def search_parcel(district: str,
                  section: str,
                  number:str,
                  db: Database=USE_DATABASE, 
                  nearby=False, 
                  maxDistance=100
                  ) -> list:
    pipeline = _search_parcel(district, section, number)
    search_results = db.parcels.aggregate(pipeline)
    
    
    parcel_to_applicant_information = []
    for result in search_results:
        dist, sect, num = result['distrestulictName'], result['sectionName'], result['prcl']
        parcel_to_applicant_information.append( (dist+sect+num, 
                                                 result['relatedParcels']) )
    if not nearby: 
               #! [ tuple( str, list[set] ) ]
               #! [ (parcel_string, `relatedParcels`), ... ]
        return parcel_to_applicant_information  
    
    
    parcel_to_nearby_applicants = []
    for parcel_string, relatedParcels in parcel_to_applicant_information:
        for parcels in relatedParcels:
            x, y = parcels['center']['coordinates']
            geo_pipeline = _search_nearby(x, y, maxDistance=maxDistance)
            geo_results = list(db.applicants.aggregate(geo_pipeline))
            
            parcel_to_nearby_applicants.append( (parcel_string, geo_results) )

           #! [ tuple( str, list[set] ) ]
           #! [ ( parcel_string, [{applicants}, ...}] ), ... ]
    return parcel_to_nearby_applicants 

