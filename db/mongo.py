import os
from pymongo import MongoClient

# password = os.getenv("MONGO_DB_PASSWORD")
password = "Cokie7523"
cluster = f"mongodb+srv://cookie:{password}@cluster0.xveirqo.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(cluster)

db = client["test"]
basics_database = db["basic"]

def count_docs():
    return basics_database.count_documents({})

