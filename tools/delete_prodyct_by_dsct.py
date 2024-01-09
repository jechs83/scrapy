

import pymongo
import time
from decouple import config

client = pymongo.MongoClient("mongodb://192.168.9.66:27017")
db = client["saga"]

market = ["saga", "ripley", "curacao", "plazavea", "tailoy", "oechsle","promart" ]

# Select the database and collection
for i,v in enumerate (market):
    db = client[v]
    collection = db["scrap"]

    # Define the deletion criteria
    criteria = {"web_dsct": {"$gte": 70}}

    # Delete documents that match the criteria
    result = collection.delete_many(criteria)

    # Print the number of documents deleted
    print(f"Deleted {result.deleted_count} documents "+v)
