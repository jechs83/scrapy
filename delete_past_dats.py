
from pymongo import MongoClient
from decouple import config
from datetime import datetime
from datetime import datetime, timedelta

def delete_pastdays():
        # Get the current date
        current_date = datetime.now()

        current_date = current_date.strftime('%d/%m/%Y')


        # Connect to the MongoDB server
        client = MongoClient(config("MONGO_DB"))

        print(current_date)
        # Access the "scrap" database and collection
        db = client['scrap']
        collection = db['scrap']

        # Delete all fields named "date" except for "24/06/2023"
        # Delete documents except for date: "24/06/2023"
        collection.delete_many({"date": {"$ne": str(current_date)}})

        print("Terminio limpiesa de db")

