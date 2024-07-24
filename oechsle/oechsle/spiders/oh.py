import scrapy
from oechsle.items import OechsleItem
import datetime
import json
import pymongo
import time
from oechsle.spiders.urls_db import *
from decouple import config
from oechsle.spiders.link_json import json_link



class OhSpider(scrapy.Spider):
    name = "oh"
    allowed_domains = ["oechsle.pe"]    

    def __init__(self, *args, **kwargs):
        super(OhSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed() # Initialize self.lista based on self.b
        self.urls = links()[int(int(self.u)-1)]

    def brand_allowed(self):
        collection1 = self.db["todo"]
        shoes = collection1.find({})
        shoes_list = [doc["brand"] for doc in shoes]
        collection1 = self.db["nada"]
        x = collection1.find({})
        return shoes_list , x
    
    def start_requests(self):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
       
        for i,v in enumerate(self.urls):  
         
            pages = v[2]
            if pages == 50:
                pages = 45
            for i in range (pages+5):
                # aqui se jala la url de oechsle directa
                home_web = v[1]+str(i+1)
                #print(home_web)
                web  =json_link(home_web)
                yield scrapy.Request(web, self.parse) #, meta={'home_web':home_web})

    count = 0
    def parse(self, response):
    

        item = OechsleItem()
        #print(response.status)
     
    
        #home = response.meta['home_web']
        json_data = json.loads(response.text)
        # if not json_data:
        #     return

        count = 0
        for i in json_data:
            count = count+1
        
            item["product"]=  i["productName"]
            
            item["image"]=  i["items"][0]["images"][0]["imageUrl"]
            item["brand"]=  i["brand"]

            try:
                seller = i["Vendido por"]
                item["market"] = str(seller[0]).lower()
            except:
              
                continue
            #print(seller)
            vendedor = seller[0]

            if vendedor.lower() not in ["plazavea", "oechsle", "promart"]:
                continue

            # i["market"] = "oechsle"
            


            pro = item["brand"].lower()
        

        
            if pro.lower()  in self.lista[0]:
                    # print("ASLATA AL OTRO PRODUCTO ")
                    pass
            else:
                    continue
           

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

            item["home_list"] = "oechsle.com.pe" 
            item["_id"]=   item["sku"]

            current_datetime = datetime.datetime.now()
            item["date"] = current_datetime.strftime("%d/%m/%Y")
            item["time"] = current_datetime.strftime("%H:%M:%S")


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

            print(count+1)
 
   
