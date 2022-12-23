import os
from pymongo import MongoClient

# password = os.getenv("MONGO_DB_PASSWORD")
password = "Cokie7523"
cluster = f"mongodb+srv://cookie:{password}@cluster0.xveirqo.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(cluster)

db = client["test"]
basics_database = db["basic"]

# infos = [
#     {"name": "Cookie", 
#      "text": "Hello world", 
#      "gender": "Male"},
#     {"name": "Latte", 
#      "text": "Hello there", 
#      "gender": "Male"},
# ]

# basics_database.insert_many(infos)
basics_database.delete_one({'name': 'Cookie'})
print(basics_database.count_documents({}))

