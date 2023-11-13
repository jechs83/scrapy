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





def brand_allowed():
        client = pymongo.MongoClient(config("MONGODB"))
        db = client["brand_allowed"]
        collection1 =db["todo"]
        todo = collection1.find({})
        array = []
        for document in todo:
                array.append(document["brand"])
        
        return array    



print(brand_allowed())