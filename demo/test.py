from decouple import config

MONGO_URI = config("MONGODB")
MONGO_DATABASE = config("data_base")
COLLECTION_NAME = config("collection")

print(MONGO_DATABASE)

print(COLLECTION_NAME)