from pymongo import MongoClient
import pandas as pd
# password = os.getenv("MONGO_DB_PASSWORD")
USERNAME = 'cookie'
PASSWORD = "Cokie7523"

mongo_uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.xveirqo.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)


def _connect_mongo(username=USERNAME,
                   password=PASSWORD,
                   db='basic'):
    """ A util for making a connection to mongo """
    
    mongo_uri = f"mongodb+srv://{username}:{password}@cluster0.xveirqo.mongodb.net/test?retryWrites=true&w=majority"
    conn = MongoClient(mongo_uri)

    return conn[db]


def read_mongo(db, 
               collection='basic', 
               query={}, 
               host='localhost', 
               username=None,
               password=None) -> pd.DataFrame:
    
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo()
    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)
    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(iter(cursor))
    # # Delete the _id
    # if no_id:
    #     del df['_id']

    return df