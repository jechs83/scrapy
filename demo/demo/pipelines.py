
import time
import logging
import pymongo
from demo.settings import COLLECTION_NAME
from datetime import date, datetime, timedelta

def load_datetime():
    
    today = date.today()
    now = datetime.now()
    date_now = today.strftime("%d/%m/%Y")  
    time_now = now.strftime("%H:%M:%S")
        
    return date_now, time_now, today
current_date = load_datetime()[0]




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
    #     filter = { "_id":item["_id"], "sku": item["sku"]}
    #     update = {'$set': dict(item)}
    #     result = collection.update_one(filter, update, upsert=True)
    #     spider.logger.debug('Item updated in MongoDB: %s', result)
    #     return item
       
   

    # def process_item(self, item, spider):
    #     collection = self.db[self.collection_name]
    #     filter = {"sku": item["sku"], "best_prices": {"date": item["date"]} }
    #     update = {"$set": dict(item), "$push": {"best_prices": {"date": item["date"], "price": item["best_price"]}}}
    #     result = collection.update_one(filter, update, upsert=True)
    #     spider.logger.debug('Item updated in MongoDB: %s', result)
    #     return item

  
    
    
    # def process_item(self, item, spider):
    #     collection = self.db[self.collection_name]
    #     filter = { "sku": item["sku"],"list_price":item["list_price"], "best_price": item["best_price"],"card_price": item["card_price"], }
    #     update = {'$set': dict(item)}
    #     result = collection.update_one(filter, update, upsert=True)
    #     spider.logger.debug('Item updated in MongoDB: %s', result)
    #     return item

    def process_item(self, item, spider):
        collection = self.db[self.collection_name]

        filter = { "sku": item["sku"],"list_price":item["list_price"], "best_price": item["best_price"],"card_price": item["card_price"], }
        update = {'$set': dict(item)}
        result = collection.update_one(filter, update, upsert=True)
        spider.logger.debug('Item updated in MongoDB: %s', result)
        return item
    
   

    # def process_item(self, item, spider):
    #     collection = self.db[self.collection_name]
    #     filter = {"sku": item["sku"], "date":load_datetime()[0] }
    #     existing_record = collection.find_one(filter)
        
    #     if existing_record:
    #         # Compare prices before updating
    #         if (existing_record["list_price"] != item["list_price"] or
    #             existing_record["best_price"] != item["best_price"] or
    #             existing_record["card_price"] != item["card_price"]):
    #             # Prices are different, update the record
    #             update = {'$set': dict(item)}
    #             result = collection.update_one(filter, update)
    #             spider.logger.debug('Item updated in MongoDB: %s', result)
    #     else:
    #         # If the SKU is not found, insert a new record
    #         collection.insert_one(dict(item))
    #         spider.logger.debug('New item inserted into MongoDB')
        
    #     return item
    