import scrapy
from scrapy import Selector
from metro.items import MetroItem
from datetime import datetime
from datetime import date
from metro.spiders.urls_db import *

from metro.spiders import url_list 
import json
import requests
from bs4 import BeautifulSoup
import pymongo
from decouple import config
import time
from product_toJson import productId_extract





def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

current_day = load_datetime()[0]
current_time = load_datetime()[1]

class Metro1Spider(scrapy.Spider):
    name = "metro1"
    allowed_domains = ["metro.pe"]

    def __init__(self, *args, **kwargs):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        super(Metro1Spider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client['metro']
        self.collection_name = self.db['scrap']
        self.db2 = self.client["brand_allowed"]
        self.collection_brand = self.db2["todo"]
        self.lista_marcas =[]
        for i in self.collection_brand.find():
            self.lista_marcas.append(i["brand"])

        self.urls = links()[int(int(self.u)-1)]
    
    



    def start_requests(self):
    
        for i, v in enumerate(self.urls):
            
                for e in range (15):
                    
                    link = v[0]+"?page="+str(e+1)
                    print("#######")
              
            
          
                    web = productId_extract(link)
            
                    print("")
                    print("######")
                    
                    yield scrapy.Request(web, self.parse)

        

    def parse(self, response):
        item = MetroItem()

        html_content = response.body
        json_data = json.loads(html_content)

    

        count = 0
        for i in json_data:
            count = count +1
            print(count)
      
            item["product"]=  i["productName"]

    
            item["image"]=  i["items"][0]["images"][0]["imageUrl"]
            item["brand"]=  i["brand"]


            # product = item["brand"].lower()
         
            # if product not in self.lista[0]:

            #         continue

            item["link"]=  i["link"]
            item["sku"] = i["productReference"]
            item["list_price"] =   float(i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"])

            try:
                item["best_price"] =   float(i["items"][0]["sellers"][0]["commertialOffer"]["Price"])
            except:item["best_price"] = 0
 
            if item["best_price"] == item["list_price"]:
                item["web_dsct"] = 0

            elif item["best_price"] != 0:
                item["web_dsct"]  = round(100-(item["best_price"]*100/item["list_price"]))
            else:
                item["web_dsct"] = 0

            try:
                dcst_tarjeta =   float(i["items"][0]["sellers"][0]["commertialOffer"]["PromotionTeasers"][0]["Effects"]["Parameters"][1]["Value"])
           
            except: dcst_tarjeta = None
            if dcst_tarjeta != None:
                item["card_price"] =item["list_price"] - dcst_tarjeta
                item["card_dsct"] = round(100-(item["card_price"] *100/item["list_price"]))
            else:
                item["card_price"]= 0
                item["card_dsct"] =0 

            if item["list_price"] and item["card_price"] and item["best_price"] == 0:
                continue

            item["home_list"] = "metro.pe "
            item["_id"]=   item["sku"]
            item["date"] = current_day
            item["time"] = current_time
            item["market"] = "metro"

            print()
            print(item["brand"])
            print(item["product"])
            print(item["link"])
            print(item["best_price"])
            print(item["card_price"] )
            print(item["list_price"] )

            collection = self.db["scrap"]
            filter = { "sku": item["sku"]}
            update = {'$set': dict(item)}
            result = collection.update_one(filter, update, upsert=True)



           
   