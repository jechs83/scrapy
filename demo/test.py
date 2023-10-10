import scrapy
import json
from demo.items import DemoItem
from datetime import datetime
from datetime import date
from  demo.spiders import url_list 
import uuid
import pymongo
import time

from decouple import config



def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
    
 return date_now, time_now, today




# def skip_brand():
#     client = pymongo.MongoClient(config("MONGODB"))
#     db = client[config("db_saga")] 
#     collection = db["skip"] 

#     skip_list = []
#     skip = collection.find({})

#     for doc in skip:
        
#         skip_list.append(doc["brand"])
#     skip_list = list(skip_list)

#     return skip_list



def brand_allowed():
        
        client = pymongo.MongoClient(config("MONGODB"))
        db = client["brand_allowed"]
        collection1 = db["shoes"]
        collection2 = db["electro"]
        collection3 = db["tv"]
        collection4 = db["cellphone"]
        collection5 = db["laptop"]
        
        shoes = collection1.find({})
        electro = collection2.find({})
        tv = collection3.find({})
        cellphone = collection4.find({})
        laptop = collection5.find({})

        shoes_list = [doc["brand"] for doc in shoes]
        electro_list = [doc["brand"] for doc in electro]
        tv_list = [doc["brand"] for doc in tv]
        cellphone_list = [doc["brand"] for doc in cellphone]
        laptop_list = [doc["brand"] for doc in laptop]
        return shoes_list ,electro_list,tv_list,cellphone_list,laptop_list

print(brand_allowed()[1])
