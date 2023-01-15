
from pymongo import MongoClient
import os

USERNAME = os.getenv("MONGODB_USERNAME")
PASSWORD = os.getenv("MONGODB_PASSWORD")

USERNAME, PASSWORD = 'cookie', 'Cokie7523'


def connect_mongo(username=USERNAME,
                   password=PASSWORD) -> MongoClient:
    mongo_uri = f"mongodb+srv://{username}:{password}@cluster0.xveirqo.mongodb.net/test?retryWrites=true&w=majority"
    client = MongoClient(mongo_uri)

    return client
