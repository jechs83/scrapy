
from pymongo import MongoClient
from datetime import date, datetime, time

# Connect to MongoDB

# Create a datetime object from the date object
my_date = date.today()
print(my_date)
my_datetime = datetime.combine(my_date, time.min)

print(my_datetime)