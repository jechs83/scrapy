import scrapy
from vivanda.items import VivandaItem
from datetime import datetime
from datetime import date
from vivanda.spiders.urls_db import *
from link_json import get_json
import pymongo
from decouple import config
import json
from bs4 import BeautifulSoup

import time

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

current_day = load_datetime()[0]
current_time = load_datetime()[1]

class VivaSpider(scrapy.Spider):
    name = "viva"
    allowed_domains = ["plazavea.com.pe"]

    def __init__(self, *args, **kwargs):

        super(VivaSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b
        self.urls = links()[int(int(self.u)-1)]

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
            
            for i in range(50):
                web = v[0]+"?page="+str(i+1)

                yield scrapy.Request(web, self.parse)


        # for i,v in enumerate(self.urls):
        #     web = get_json(v[0])
        #     home_web = v[0]+"?page="+str(i+1)

        #     for i in range (100):
        #         link = web+"/&_from="+ str(i*48)+"&_to="+ str(((i+1)*48)-1)+"&O=OrderByScoreDESC&"
        #         yield scrapy.Request(link, self.parse, meta={'home_web':home_web})

    def parse(self, response):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        item = VivandaItem()


        data = response.body

        soup = BeautifulSoup(response.text, 'html.parser')

        web_data = soup.find_all("script")

        for i in web_data:
            if "__STATE__ = " in i.text:

                datos = i.text
                datos = datos.split("__STATE__ =")
                datos = datos[1].strip()
                break
                
        
      
                
        json_data = json.loads(str(datos))


        for i,v in json_data.items():
            print()

            print()
            try:
                cache_id = v["cacheId"]+".priceRange.sellingPrice"
            except:
                continue

            print(cache_id)
            print(i)
            #print(v["highPrice"])
            print(v)


           

            try:
           
                print("##########################################")
                print(v["brand"])
                print(v["productName"])
                print(v["link"])
                print(v["linkText"])
              
                try:
                     print(v["highPrice"])
                except:
                    print(0)
                try:
                  print(v["lowPrice"])
                except: 
                    print(0)
                print("##########################################")
                


             
                print()
                time.sleep(2)
            except:
                return True
            try:
                  print(v["highPrice"])
            except:
                  print("no hay")

           


        json_data = json.loads(response.body)

        for i in json_data:

            item["product"]=  i["productName"]
            item["image"]=  i["items"][0]["images"][0]["imageUrl"]
            item["brand"]=  i["brand"]


            product = item["brand"].lower()
            marca_not_allowed = []
            if self.lista == []:
                pass
            else:
                if product not in self.lista:

                    continue

            item["link"]=  i["link"]
            item["sku"] = i["productReference"]
            item["list_price"] =   float(i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"])

            try:
                item["best_price"] =   float(i["items"][0]["sellers"][0]["commertialOffer"]["Price"])
            except:item["best_price"] = float(0)
 
            if item["best_price"] == item["list_price"]:
                item["web_dsct"] = float(0)

            elif item["best_price"] != 0:
                item["web_dsct"]  = round(float(100-(item["best_price"]*100/item["list_price"])))
            else:
                item["web_dsct"] = float(0)

            try:
                dcst_tarjeta =   float(i["items"][0]["sellers"][0]["commertialOffer"]["PromotionTeasers"][0]["Effects"]["Parameters"][1]["Value"])
           
            except: dcst_tarjeta = None
            if dcst_tarjeta != None:
                item["card_price"] =item["list_price"] - dcst_tarjeta
                item["card_dsct"] = round(float(100-(item["card_price"] *100/item["list_price"])))
            else:
                item["card_price"]= float(0)
                item["card_dsct"] =float(0) 

            item["home_list"] = home 
            item["_id"]=   item["sku"]
            item["date"] = current_day
            item["time"] = current_time
            item["market"] = "plazavea"
            yield item
   
