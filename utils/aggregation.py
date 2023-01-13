
from utils.helper import pairwise

class StageOperator:
    def geo_near(self,
                 coordinates=[0, 0], 
                 maxDistance=100,
                 
                 type='Point',
                 distanceField='distance',
                 query={}) -> dict:
        return\
        {
            '$geoNear': {
                'near': {
                    'type': 'Point', 
                    'coordinates': coordinates
                }, 
                'distanceField': distanceField, 
                'maxDistance': maxDistance, 
                'query': query, 
                'spherical': True
            }
        }


    def lookup(self,
               from_,
               local_field,
               foreign_field,
               as_
               ):
        return\
        {
            '$lookup': {
                "from": from_,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": as_
            }
        }
    
    
    def text_search(self,
                    query: str,
                    path: list[str],
                    index='keyword_index',
                    maxEdits=1):
        
        return\
        {
            '$search': {
                'index': index, 
                'text': {
                    'query': query, 
                    'path': path, 
                    'fuzzy': {
                        'maxEdits': maxEdits
                    }
                }
            }
        }
    
    def set_field(self,
             field: str, 
             expression: dict):
        return\
        {
            '$set': {
                field: expression
            }
        }
        
    def match(self,
              *expressions):
        
        expressions = list(expressions)
        match_items = []
        for key, val in pairwise(expressions):
            match_items.append({key: val})
        
        return\
        {
        '$match': {
            '$and': match_items
            }
        }
    
    def sort(self,
             field: str):
        return { '$sort': { field: -1 }}


    def limit(self, 
              limit: int):
        return { '$limit': limit }

    def regex(self, pattern):
        return { '$regex': pattern }

