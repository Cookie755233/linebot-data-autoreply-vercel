
# class Pipeline:
#     def __init__(self) -> None:
#         self.pipeline = []
    
#     def add_stage(self, stage: dict) -> None:
#         self.pipeline.append(stage)


class StageOperator:
    def geo_near(self,
                type='Point',
                coordinates=[0, 0], 
                distanceField='distance',
                maxDistance=100,
                query={},
                spherical=True) -> dict:
        return\
        {
            '$geoNear': {
                'near': {
                    'type': 'Point', 
                    'coordinates': coordinates
                }, 
                'distanceField': 'dist', 
                'maxDistance': maxDistance, 
                'query': {}, 
                'spherical': True
            }
        }


    def text_search(self,
                    query: str,
                    path: str | list[str],
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
              field: str,
              expression: dict):
        return\
        {
            '$match': {
                field : expression
            }
        }
    
    def sort(self,
             field: str):
        return { '$sort': { field: 1 }}


    def limit(self, 
              limit: int):
        return { '$limit': limit }




# def __geoNear(x: float, 
#             y: float,
#             maxDistance: float=100.0) -> list[dict]:
#     stage = [
#         {
#             '$geoNear': {
#                 'near': {
#                     'type': 'Point', 
#                     'coordinates': [x, y]
#                 }, 
#                 'distanceField': 'dist', 
#                 'maxDistance': maxDistance, 
#                 'query': {}, 
#                 'spherical': True
#             }
#         }
#     ]
    
#     return stage

# def __textSearch(keyword: str,
#                    maxEdits: int=2,
#                    min_searchScore: int=1, 
#                    limit: int=0) -> list[dict]:
#     stage = [
#         {
#             '$search': {
#                 'index': 'keyword_index', 
#                 'text': {
#                     'query': keyword, 
#                     'path': 'applicantName', 
#                     'fuzzy': {
#                         'maxEdits': maxEdits
#                     }
#                 }
#             }
#         },
#         {
#             '$set': {
#                 'searchScore': {
#                     '$meta': 'searchScore'
#                 }
#             }
#         },
#         {
#             '$match': {
#                 'searchScore': { '$gt': min_searchScore }
#             }
#         },
#         {
#             '$sort': { 'searchScore': 1}
#         },
#     ]
#     if limit:
#         stage.append(
#             {
#                 '$limit': limit
#             }
#             )
    
#     return stage
