
import logging
import pymongo
from ripley.settings import COLLECTION_NAME

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
    #     filter = {'_id': item['_id'], "sku": item["sku"]}
    #     update = {'$set': dict(item)}
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

        # Find the existing document by ID
        filter = { "_id": item["_id"] }
        existing_document = collection.find_one(filter)

        # Check if the document exists and compare fields
        if existing_document:
            update_fields = {
                        'best_price': 1689.0,
                        'brand': item["brand"],
                        'card_dsct': item["card_dsct"],
                        'card_price': item["card_price"],
                        'date': item["date"],
                        'home_list': item["home_list"],
                        'image': item["image"],
                        'link': item["link"],
                        'list_price': item["list_price"],
                        'market': item["market"],
                        'product': item["product"],
                        'sku': item["sku"],
                        'time':item["time"],
                        'web_dsct': item["web_dsct"],
                        }
            for key, value in item.items():
                # Check if the field exists and if it's different from the existing document
                if key != "_id" and key in existing_document and existing_document[key] != value:
                    update_fields[key] = value
                

            # If there are fields to update, perform the update
            if update_fields:
                update = {'$set': update_fields}
                result = collection.update_one(filter, update)
                spider.logger.debug('Item updated in MongoDB: %s', result)
        else:
            # If the document doesn't exist, insert the new item
            result = collection.insert_one(dict(item))
            spider.logger.debug('New item inserted in MongoDB: %s', result.inserted_id)

        return item
