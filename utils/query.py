
import re

from utils.aggregation import StageOperator 
from database.connect import connect_mongo

operator = StageOperator()
REIP = connect_mongo().reip

class Config:
    UNIT = {'公尺': 1, '米': 1, 'm': 1, '': 1, '公里': 1000, 'km': 1000}
    RESULT = ["#全文檢還", "#審查中", "#撤件", "#核准", "#補正", "#駁回"]

    def __init__(self) -> None:     
        self.search_nearby = False
        self.maxDistance = None

        self.subquery = {}
        
    def __repr__(self) -> str:
        return f'''
            [ CONFIG ]
            >> nearby         : {self.search_nearby}
            >> maxDistance    : {self.maxDistance}
            >> subquery
              -- districtName : {self.districtName}
              -- result       : {self.result}'''

    @classmethod
    def from_configs(cls, configs):
        c = cls()
        c.parse(configs)

        return c
    
    def parse(self, configs):
        for config in configs:
            if config.startswith('#鄰近'):
                self._register_nearby_configs(config)
                continue
            
            if config.startswith('#'):
                self._register_subquery_configs(config)
        return self
    
    
    def _register_nearby_configs(self, config: str) -> None:
        try:
            distance, unit = re.findall(
                r'([0-9]*[.]?[0-9]+)(公里|公尺|米|m|km)?', config)[0]
        except ValueError:
            return 
        
        self.search_nearby = True
        self.maxDistance = float(distance) * self.UNIT[unit]
    
    def _register_subquery_configs(self, config: str) -> None:
        if '區' in config:
            try:
                districtName, _ = re.findall(r'(.*?區)(.*?段)?', config[1:])[0]
                districtName = None if not districtName else districtName
            except IndexError: 
                return 
            
            self.subquery['districtName'] = districtName
            
        elif config in self.RESULT:
            self.subquery['result'] = config[1:] #parse the '#' in front of '#result'

class Query:
    minimum_text_search_threshold = 1
    db = REIP
    
    def __init__(self, instruction=None, query=None, config=None) -> None:
        self.instruction=instruction
        self.query = query
        self.config = config
        self.search_nearby = self.config.search_nearby
        
        
    @property
    def mode(self):
        return { '@查詢': 'a', '@查詢地號': 'p' }.get(self.instruction) 
        
        
    @classmethod
    def from_messages(cls, instruction: str, query: str, config: Config):
        return cls(instruction=instruction, query=query, config=config)
    
    #! <--- MAIN FUNCTION --->
    def execute(self):        
        pipeline = self._default_pipeline(self.mode) + self._sub_pipeline(self.config)
        collection = self._use_collection(self.mode)
        search_results = self._qeury_search(collection, pipeline)
        
        if self.search_nearby:
            search_nearby_results = self._nearby_search(search_results)
            return self._to_response(search_nearby_results)
        
        return self._to_response(search_results)
    #! <--- MAIN FUNCTION --->

    
    def _qeury_search(self, collection, pipeline):
        return list(collection.aggregate(pipeline))
    
    def _nearby_search(self, search_results):
        total_geo_search_results = []
        for result in search_results:
            coordinates = result['location']['coordinates']
            geo_pipeline = [
                operator.geo_near(coordinates=coordinates,
                                  maxDistance=self.config.maxDistance,
                                  query={}),
                operator.limit(7)
            ]
            geo_search_results = (list(self.db.applicants.aggregate(geo_pipeline)))
            #? <--- exclude itself --->
            if self.mode == 'a':
                geo_search_results = [ i for i in geo_search_results if result['PRSN'] != i['PRSN'] ]
                
            total_geo_search_results.append( (result, geo_search_results) )
        
        return total_geo_search_results
                
    
    def _default_pipeline(self, mode):
        if mode == 'a':
            pipeline = [
                operator.text_search(query=self.query, path=['applicantName'], index='keyword_index', maxEdits=1),
                operator.set_field(field='searchScore', expression={'$meta': 'searchScore'}),
                operator.match( 'searchScore', { '$gt': self.minimum_text_search_threshold } ),
                operator.sort(field='searchScore'),
            ]

        if mode == 'p':
            districtName, sectionName, prcl = re.findall(r'(.*區)(.*段)(\d{1,4}-?\d{0,4})地?號?', self.query)[0]
            pipeline = [
                operator.match('districtName', districtName, 
                               'sectionName', sectionName,
                               'prcl', operator.regex(prcl)),
                operator.lookup(from_='applicants', 
                                local_field='_id',
                                foreign_field='georeferencedParcels',
                                as_='relatedApplicants'),
            ]
        return pipeline
    
    
    def _sub_pipeline(self, config):
        pipeline = []
        for k, v in config.subquery.items():
            if v: 
                pipeline.append(operator.match(k, v))
        return pipeline


    def _use_collection(self, mode):
        return {
            'a': self.db.applicants,
            'p': self.db.parcels
        }.get(mode)
        

    def _to_response(self, respond_obj):    
        if self.mode == 'a':
            if respond_obj: return 201 + self.search_nearby, respond_obj
            return 301, None

        if self.mode== 'p': 
            if respond_obj: return 203 + self.search_nearby, respond_obj
            return 303, None



 
#@ TODO: creaet abc for Query?
# from abc import ABC, abstractmethod

# class Query(ABC):
#     def __init__(self,
#                  query=None,
#                  db=None,
#                  ) -> None:
#         self.db = db
#         self.query = query
#         self.applicants_collection = self.db.applicants
#         self.parcels_collection = self.db.parcels
        
#     @property
#     @abstractmethod
#     def pipeline(self, minimum_text_search_threshold=None, maxEdits=None):
#         pass
        
#     @abstractmethod
#     def execute(self):
#         pass
    
#     def 
    

# class ApplicantSearch(Query):
#     def __init__(self, 
#                  query=None,
#                  db=None,
#                  search_nearby=False,
#                  ) -> None:
#         super().__init__(query=query, db=db)
#         self.search_nearby=search_nearby
        

#     @property
#     def pipeline(self,
#                  minimum_text_search_threshold=1,
#                  maxEdits=1):
#         return [
#                 operator.text_search(query=self.query, path=['applicantName'], index='keyword_index', maxEdits=maxEdits),
#                 operator.set_field(field='searchScore', expression={'$meta': 'searchScore'}),
#                 operator.match( 'searchScore', { '$gt': minimum_text_search_threshold } ),
#                 operator.sort(field='searchScore'),
#             ]
    

# class ParcelSearch(Query):
#     def __init__(self, 
#                  query=None,
#                  db=None,
#                  search_nearby=False,
#                  ) -> None:
#         super().__init__(query=query, db=db)
#         self.search_nearby=search_nearby


#     @property
#     def pipeline(self,
#                  minimum_text_search_threshold=1,
#                  maxEdits=1):
#         districtName, sectionName, prcl = re.match(r'(.*區)(.*段)(\d{1,4}-?\d{0,4})地?號?', self.query)
#         pipeline = [
#             operator.match('districtName', districtName, 
#                             'sectionName', sectionName,
#                             'prcl', operator.regex(prcl)),
#             operator.lookup(from_='applicants', 
#                             local_field='_id',
#                             foreign_field='georeferencedParcels',
#                             as_='relatedApplicants')
#         ]
#         return pipeline