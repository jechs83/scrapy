import scrapy
from oechsle.items import OechsleItem
from datetime import datetime
from datetime import date
#from oechsle.spiders import url_list 
import uuid
import json
import pymongo
from oechsle.spiders.urls_db import *
from decouple import config
import time 
from link_json import json_link

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

current_day = load_datetime()[0]
current_time = load_datetime()[1]


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
       
        # for i, v in enumerate(urls):
        #     for e in range (v[1]+10):
        #         url = v[0]+"?&optionOrderBy=OrderByScoreDESC&O=OrderByScoreDESC&page="+str(e+1)
        #         yield scrapy.Request(url, self.parse)

        for i,v in enumerate(self.urls):
          

            for i in range (50):
               
                home_web = v[1]+str(i+1)
                print(home_web)
                web  =json_link(home_web)
                
                
            
                yield scrapy.Request(web, self.parse) #, meta={'home_web':home_web})

    def parse(self, response):

        item = OechsleItem()
        print(response.status)
     
    
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


            pro = item["brand"].lower()
        

        
            if pro.lower()  in self.lista[0]:
                    print("ASLATA AL OTRO PRODUCTO ")
                    pass
            else:
                    print("PASASASASASASASASASAS")
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
            item["date"] = current_day
            item["time"] = current_time
            item["market"] = "oechsle"

            print(count)
            print("##############")


           
            
            yield item
   
