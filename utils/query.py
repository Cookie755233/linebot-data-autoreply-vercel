
from pymongo.database import Database

from utils.aggregation import StageOperator
from db._connect import _connect_mongo


so = StageOperator()
USE_DATABASE = _connect_mongo().reip

def search_keyword(keyword: str, 
                   min_searchScore=1,
                   
                   nearby=False,
                   maxDistance=100, 
                   
                   limit=0,
                   db: Database=USE_DATABASE,
                   deafult_searchScore_name = 'searchScore'
                   ) -> list:

        
    pipeline = [
        so.text_search(query=keyword, path=['applicantName'], index='keyword_index', maxEdits=1),
        so.set_field(field=deafult_searchScore_name, expression={'$meta': deafult_searchScore_name}),
        so.match(field=deafult_searchScore_name, expression={ '$gt': min_searchScore }),
        so.sort(field=deafult_searchScore_name),
    ]
    
    if limit: 
        pipeline.append(so.limit(2))
    search_results = list(db.applicants.aggregate(pipeline))
    
    #? if nearby not required
    if not nearby: 
        return search_results #! [ {applicants}, ... ]
    
    #? if to get all nearby applicants
    applicant_to_nearby_applicants = []
    for item in search_results:
        x, y = item['center']['coordinates']
        geo_pipeline = [
            so.geo_near(coordinates=[x, y], maxDistance=maxDistance)
        ]
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
    return
    # pipeline = _search_parcel(district, section, number)
    # search_results = db.parcels.aggregate(pipeline)
    
    
    # parcel_to_applicant_information = []
    # for result in search_results:
    #     dist, sect, num = result['distrestulictName'], result['sectionName'], result['prcl']
    #     parcel_to_applicant_information.append( (dist+sect+num, 
    #                                              result['relatedParcels']) )
    # if not nearby: 
    #            #! [ tuple( str, list[set] ) ]
    #            #! [ (parcel_string, `relatedParcels`), ... ]
    #     return parcel_to_applicant_information  
    
    
    # parcel_to_nearby_applicants = []
    # for parcel_string, relatedParcels in parcel_to_applicant_information:
    #     for parcels in relatedParcels:
    #         x, y = parcels['center']['coordinates']
    #         geo_pipeline = _search_nearby(x, y, maxDistance=maxDistance)
    #         geo_results = list(db.applicants.aggregate(geo_pipeline))
            
    #         parcel_to_nearby_applicants.append( (parcel_string, geo_results) )

    #        #! [ tuple( str, list[set] ) ]
    #        #! [ ( parcel_string, [{applicants}, ...}] ), ... ]
    # return parcel_to_nearby_applicants 

