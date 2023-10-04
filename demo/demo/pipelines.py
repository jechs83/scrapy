# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# from itemadapter import ItemAdapter


# class DemoPipeline:
#     def process_item(self, item, spider):
#         return item
from datetime import date, datetime, timedelta
import time
import logging
import pymongo
from demo.settings import COLLECTION_NAME

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
    
 return date_now, time_now, today

date_local = load_datetime()[0]

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
       
    '''

    # def process_item(self, item, spider):
    #     collection = self.db[self.collection_name]
    #     filter = {"sku": item["sku"], "best_prices": {"date": item["date"]} }
    #     update = {"$set": dict(item), "$push": {"best_prices": {"date": item["date"], "price": item["best_price"]}}}
    #     result = collection.update_one(filter, update, upsert=True)
    #     spider.logger.debug('Item updated in MongoDB: %s', result)
    #     return item

  '''
    
    
    # def process_item(self, item, spider):
    #     collection = self.db[self.collection_name]
    #     filter = {'_id': item['_id'], "sku": item["sku"]}
    #     update = {'$set': dict(item)}
    #     result = collection.update_one(filter, update, upsert=True)
    #     spider.logger.debug('Item updated in MongoDB: %s', result)
    #     return item
  
   
 

        
    def process_item(self, item, spider):
        collection = self.db[self.collection_name]
        filter = {'_id': item['_id'], "sku": item["sku"]}
        print( item["date"])
        
        # Check if the document already exists
        existing_item = collection.find_one(filter)
        print("######FFFFF##")
        print(existing_item)
        print("existe productos deberia agregar precios")
        print( item.get('best_price'))
        print(item.get('list_price'))
        print( item.get('card_price'))


        
        if existing_item :
            # Document exists; update price histories and other fields
            best_price_history = existing_item.get('best_price_history', [])
            list_price_history = existing_item.get('list_price_history', [])
            card_price_history = existing_item.get('card_price_history', [])
            print(best_price_history)
            print(list_price_history)
            print(card_price_history)
  
            
            
            best_price_history.append(item.get('best_price'))
            list_price_history.append(item.get('list_price'))
            card_price_history.append(item.get('card_price'))
 
            update = {
                '$set': {
                   
                    'best_price_history': best_price_history,
                    'list_price_history': list_price_history,
                    'card_price_history': card_price_history,
                    "date": item.get("date"),
                    #**item  # Include other fields from the item
                }
            }
        else:
            # Document does not exist; create a new one with price histories and other fields
            update = {
                '$set': {
                    'best_price': item.get('best_price'),
                    'list_price': item.get('list_price'),
                    'card_price': item.get('card_price'),
                    'best_price_history': [{"price": item.get('best_price'), "date": date_local}],
                    'list_price_history': [{"price": item.get('list_price'), "date": date_local}],
                    'card_price_history': [{"price": item.get('card_price'), "date": date_local}],
                    "date": item.get("date"),
                    #**item  # Include other fields from the item
                }
            }

        result = collection.update_one(filter, update, upsert=True)
        spider.logger.debug('Item updated in MongoDB: %s', result)
        return item
