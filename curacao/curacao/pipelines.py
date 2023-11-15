# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import time
from curacao.settings import COLLECTION_NAME
from decouple import config

from datetime import date, datetime, timedelta

def load_datetime():
    
    today = date.today()
    now = datetime.now()
    date_now = today.strftime("%d/%m/%Y")  
    time_now = now.strftime("%H:%M:%S")
        
    return date_now, time_now, today

class MongoPipeline(object):
    collection_name = COLLECTION_NAME

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()




    # def process_item(self, item, spider):
        
    #     collection = self.db[self.collection_name]
    #     filter = {"_id": item['_id'], "sku":item["sku"]}
      

    #     update = {'$set':
    #         {
    #         "sku" : item["sku"],
    #         "_id" : item["_id"],
    #         "product" : item["product"],
    #         "brand" : item["brand"],
    #         "link" : item["link"],
    #         # "best_price" : item[""],
    #         "list_price" : item["list_price"],
    #         "web_dsct" : item["web_dsct"],
    #         "image" : item["image"],
    #         "market": item["market"],
    #         "date" :item["date"],
    #         "time" : item["time"],
    #         "home_list" : item["home_list"],
    #         "card_price" : item["card_price"],
    #         "card_dsct" : item["card_dsct"],
    #         }
    #     }
                
    #     result = collection.update_one(filter, update, upsert=True)
    #     update =  {'$push':{'best_price': {'$each': [{'_id': item['best_price']['_id'], 'price': item['best_price']['price'], 'date': item['best_price']['date']}]}}}
    #     result = collection.update_one(filter,update, upsert=True)

    #     # result = collection.insert_one(filter, update, upsert=True)
    #     spider.logger.debug('Item updated in MongoDB: %s', result)
    #     return item
    



    # def process_item(self, item, spider):
    #     collection = self.db[self.collection_name]
    #     filter = {'_id': item['_id'], "sku": item["sku"]}
    #     update = {'$set': dict(item)}
    #     result = collection.update_one(filter, update, upsert=True)
    #     spider.logger.debug('Item updated in MongoDB: %s', result)
    #     return item
#####################################################################
    # def process_item(self, item, spider):
    #     collection = self.db[self.collection_name]
    #     filter = { "sku": item["sku"],"list_price":item["list_price"], "best_price": item["best_price"],"card_price": item["card_price"], }
    #     update = {'$set': dict(item)}
    #     result = collection.update_one(filter, update, upsert=True)
    #     spider.logger.debug('Item updated in MongoDB: %s', result)
    #     return item
    
  

    def process_item(self, item, spider):
        collection = self.db[self.collection_name]
        filter = {"sku": item["sku"], "date":load_datetime()[0] }
        existing_record = collection.find_one(filter)
        
        if existing_record:
            # Compare prices before updating
            if (existing_record["list_price"] != item["list_price"] or
                existing_record["best_price"] != item["best_price"] or
                existing_record["card_price"] != item["card_price"]):
                # Prices are different, update the record
                update = {'$set': dict(item)}
                result = collection.update_one(filter, update)
                spider.logger.debug('Item updated in MongoDB: %s', result)
        else:
            # If the SKU is not found, insert a new record
            collection.insert_one(dict(item))
            spider.logger.debug('New item inserted into MongoDB')
        
        return item
    
   