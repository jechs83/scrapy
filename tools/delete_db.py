import pymongo
from decouple import config

# Conéctate a la base de datos MongoDB
client = pymongo.MongoClient(config("MONGODB"))
db = client["saga"]
collection = db["scrap"]


    # Delete the collection
collection.drop()

client.close()