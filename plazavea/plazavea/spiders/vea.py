import scrapy
from plazavea.items import PlazaveaItem
from datetime import datetime
from datetime import date
from plazavea.spiders.urls_db import *
from link_json import get_json
import pymongo
from decouple import config
import json
import uuid 

import time

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

current_day = load_datetime()[0]
current_time = load_datetime()[1]

class VeaSpider(scrapy.Spider):
    name = "vea"
    allowed_domains = ["plazavea.com.pe"]

    def __init__(self, *args, **kwargs):

        super(VeaSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client['plazavea']
        self.collection_name = self.db['scrap']
        #self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b
        self.urls = links()[int(int(self.u)-1)]

        self.db2 = self.client["brand_allowed"]
        self.collection_brand = self.db2["todo"]
        self.lista_marcas =[]
        for i in self.collection_brand.find():
            self.lista_marcas.append(i["brand"])

    def brand_allowed(self):
        collection1 = self.db["todo"]
        shoes = collection1.find({})
        shoes_list = [doc["brand"] for doc in shoes]
        collection1 = self.db["nada"]
        nada = collection1.find({})
        return shoes_list ,nada
    
    def start_requests(self):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))

        for i,v in enumerate(self.urls):
            web = get_json(v[0])
            home_web = v[0]+"?page="+str(i+1)

            for i in range (100):
                link = web+"/&_from="+ str(i*48)+"&_to="+ str(((i+1)*48)-1)+"&O=OrderByScoreDESC&"
                yield scrapy.Request(link, self.parse, meta={'home_web':home_web})

    def parse(self, response):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        home = response.meta['home_web']
        item = PlazaveaItem()
        json_data = json.loads(response.body)

        for i in json_data:

            item["product"]=  i["productName"]
            item["image"]=  i["items"][0]["images"][0]["imageUrl"]
            item["brand"]=  i["brand"]


            product = item["brand"].lower()
  
            if self.lista_marcas == []:
                pass
            else:
                if product not in self.lista_marcas:

                    continue

            item["link"]=  i["link"]
            item["sku"] = i["productReference"]
   
            if  item["sku"] =="-":
                continue


            item["list_price"] =   round(float(i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]))

            try:
                item["best_price"] =   round(float(i["items"][0]["sellers"][0]["commertialOffer"]["Price"]))
            except:item["best_price"] = float(0)
 
            if item["best_price"] == item["list_price"]:
                item["web_dsct"] = float(0)

            elif item["best_price"] != 0:
                item["web_dsct"]  = round(float(100-(item["best_price"]*100/item["list_price"])))
            else:
                item["web_dsct"] = float(0)

            try:
                dcst_tarjeta =   round(float(i["items"][0]["sellers"][0]["commertialOffer"]["PromotionTeasers"][0]["Effects"]["Parameters"][1]["Value"]))
           
            except: dcst_tarjeta = None
            if dcst_tarjeta != None:
                item["card_price"] =item["list_price"] - dcst_tarjeta
                item["card_dsct"] = round(float(100-(item["card_price"] *100/item["list_price"])))
            else:
                item["card_price"]= float(0)
                item["card_dsct"] =float(0) 

            if item["list_price"] and item["card_price"] and item["best_price"] == 0:
                continue

            item["home_list"] = home 
            item["_id"]=   item["sku"]
            item["date"] = current_day
            item["time"] = current_time
            item["market"] = "plazavea"
            
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
   
