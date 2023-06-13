from pymongo import MongoClient
from decouple import config

# Configure the MongoDB connection
MONGODB_URL = config("MONGO_DB")
MONGODB_DB = config("database")
MONGODB_COLLECTION =  "TEST"



# Create a MongoDB client
client = MongoClient(MONGODB_URL)

# Access the database
db = client[MONGODB_DB]

# Access the collection
collection = db[MONGODB_COLLECTION]

# Drop the collection
collection.drop()

# Close the MongoDB client
client.close()
