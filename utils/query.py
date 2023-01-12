
import re
from pymongo.database import Database

from utils.aggregation import StageOperator
from db._connect import _connect_mongo


operator = StageOperator()
USE_DATABASE = _connect_mongo('cookie', 'Cokie7523').reip  #@ for debugging purpose
# USE_DATABASE = _connect_mongo().reip

def search_applicants(query: str, 
                      nearby: bool=False,
                      maxDistance: float=100.0, 
                      selectDistrict=None,
                      selectResult=None,

                      limit: int=0,
                      min_searchScore: int=1,
                      db: Database=USE_DATABASE,
                      deafult_searchScore_name: str = 'searchScore'
                      ) -> list:

        
    pipeline = [
        operator.text_search(query=query, path=['applicantName'], index='keyword_index', maxEdits=1),
        operator.set_field(field=deafult_searchScore_name, expression={'$meta': deafult_searchScore_name}),
        operator.match( deafult_searchScore_name, { '$gt': min_searchScore } ),
        operator.sort(field=deafult_searchScore_name),
    ]
    if selectDistrict: pipeline.append(operator.match( 'districtName', selectDistrict ) )
    if selectResult: pipeline.append(operator.match( 'result', selectResult) )
    if limit: pipeline.append(operator.limit(limit))

    search_results = list(db.applicants.aggregate(pipeline))[:12] #! narrow down to carousel limit: 12
    
    #? if nearby not required
    if not nearby: 
        if search_results: return 201, search_results
        return 301, None
    
    #? if to get all nearby applicants
    applicant_to_nearby_applicants = []
    for item in search_results:
        coordinates = item['center']['coordinates']
        geo_pipeline = [
            operator.geo_near(coordinates=coordinates, maxDistance=maxDistance),
            operator.limit(6) #! prevent size>5000
        ]
        geo_results = list(db.applicants.aggregate(geo_pipeline))[1:] #? exclude itslf
        applicant_to_nearby_applicants.append( (item, geo_results) )

    if applicant_to_nearby_applicants:
        return 202, applicant_to_nearby_applicants
    
    return 301, None


def search_parcels(query: str,
                   nearby: bool=False, 
                   maxDistance: float=100.0,
                   selectDistrict=None,
                   selectResult=None,
                   limit: int=0,
                   db: Database=USE_DATABASE, 
                   ) -> list:
    
    try:
        district, section, prcl = re.findall(
            r'(.*區)(.*段)(\d{1,4}-?\d{0,4})地?號?', query)[0]
    except IndexError:
        return 400, None
    
    pipeline = [
        operator.match('districtName', district,
                 'sectionName', section,
                 'prcl', operator.regex(prcl)),
        operator.lookup(from_='applicants', 
                  local_field='_id',
                  foreign_field='georeferencedParcels',
                  as_='relatedApplicants'),
    ]

    if selectResult: pipeline.append(operator.match( 'result', selectResult) )
    if limit: pipeline.append(operator.limit(limit))
    search_results = list(db.parcels.aggregate(pipeline))[:12]
    
    if not nearby:
        if search_results: return 203, search_results
        else: return 303, None    
    
    sub_query = dict()
    if selectDistrict: sub_query['distictName'] = district
    if selectResult: sub_query['result'] = result

    parcel_to_nearby_applicants = []
    for result in search_results:
        coordinates = result['location']['coordinates']
        geo_pipeline = [
            operator.geo_near(coordinates=coordinates, 
                        maxDistance=maxDistance,
                        query=sub_query),
            operator.limit(5)
        ]

        geo_results = list(db.applicants.aggregate(geo_pipeline))
        parcel_to_nearby_applicants.append( (result, geo_results) ) 
    
    
    #? <-- return -->
    if parcel_to_nearby_applicants: 
        return 204, parcel_to_nearby_applicants
    
    return 303, None