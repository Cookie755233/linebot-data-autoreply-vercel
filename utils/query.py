
from pymongo.database import Database

from utils.aggregation import StageOperator
from db._connect import _connect_mongo


so = StageOperator()
USE_DATABASE = _connect_mongo().reip

def search_applicants(query: str, 
                      nearby: bool=False,
                      maxDistance: float=100.0, 
                      
                      limit: int=0,
                      min_searchScore: int=1,
                      db: Database=USE_DATABASE,
                      deafult_searchScore_name: str = 'searchScore'
                      ) -> list:

        
    pipeline = [
        so.text_search(query=query, path=['applicantName'], index='keyword_index', maxEdits=1),
        so.set_field(field=deafult_searchScore_name, expression={'$meta': deafult_searchScore_name}),
        so.match( deafult_searchScore_name, { '$gt': min_searchScore } ),
        so.sort(field=deafult_searchScore_name),
    ]

    if limit: 
        pipeline.append(so.limit(limit))
    search_results = list(db.applicants.aggregate(pipeline))
    
    #? if nearby not required
    if not nearby: 
        return search_results #! [ {applicants}, ... ]
    
    #? if to get all nearby applicants
    applicant_to_nearby_applicants = []
    for item in search_results:
        coordinates = item['center']['coordinates']
        geo_pipeline = [
            so.geo_near(coordinates=coordinates, maxDistance=maxDistance)
        ]
        geo_results = list(db.applicants.aggregate(geo_pipeline))
        applicant_to_nearby_applicants.append( (item, geo_results) )

    return applicant_to_nearby_applicants #! [ ({applicants}, {geo_results}), ... ]


def search_parcels(district: str,
                   section: str,
                   prcl: str,
                   
                   nearby: bool=False, 
                   maxDistance: float=100.0,
                   limit: int=0,
                   db: Database=USE_DATABASE, 
                   ) -> list:

    pipeline = [
        so.match('districtName', district,
                 'sectionName', section,
                 'prcl',so.regex(prcl)),
        so.lookup(from_='applicants', 
                  local_field='_id',
                  foreign_field='georeferencedParcels',
                  as_='relatedApplicants'),
    ]
    if limit: 
        pipeline.append(so.limit(limit))
    search_results = list(db.parcels.aggregate(pipeline))
    
    if not nearby: 
        return search_results

    parcel_to_nearby_applicants = []
    for result in search_results:
        coordinates = result['location']['coordinates']
        geo_pipeline = [
            so.geo_near(coordinates=coordinates, maxDistance=maxDistance)
        ]
        geo_results = list(db.applicants.aggregate(geo_pipeline))

        parcel_to_nearby_applicants.append( (result, geo_results) ) 
        
    return parcel_to_nearby_applicants
    
    # parcel_to_applicant_information = []
    # for result in search_results:
    #     dist, sect, num = result['districtName'], result['sectionName'], result['prcl']
    #     parcel_to_applicant_information.append( (dist+sect+num, 
    #                                              result['relatedApplicants']) )
    # if not nearby: 
    #            #! [ tuple( str, list[set] ) ]
    #            #! [ (parcel_string, `relatedApplicants`), ... ]
    #     return parcel_to_applicant_information  
    
    
    # parcel_to_nearby_applicants = []
    # for parcel_string, relatedApplicants in parcel_to_applicant_information:
    #     for applicant in relatedApplicants:
    #         coordinates = applicant['center']['coordinates']
    #         geo_pipeline = [
    #             so.geo_near(coordinates=coordinates, maxDistance=maxDistance)
    #         ]
    #         geo_results = list(db.applicants.aggregate(geo_pipeline))
            
    #         parcel_to_nearby_applicants.append( (parcel_string, geo_results) )

    #        #! [ tuple( str, list[set] ) ]
    #        #! [ ( parcel_string, [{applicants}, ...}] ), ... ]
    # return parcel_to_nearby_applicants 

