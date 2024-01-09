import scrapy
from bs4 import BeautifulSoup
import time
import requests
import re
#from shopstar.spiders.gteurls import get_json
import json
from shopstar.items import ShopstarItem
import pymongo
from decouple import config
from datetime import datetime
from datetime import date
#from shopstar.spiders.urls_db import *
from shopstar.spiders.urls_db_json import *

import json
import requests
from bs4 import BeautifulSoup
import pymongo
from decouple import config
import time
from jsonTolink import productId_extract






def load_datetime():
    
    today = date.today()
    now = datetime.now()
    date_now = today.strftime("%d/%m/%Y")  
    time_now = now.strftime("%H:%M:%S")
        
    return date_now, time_now, today

current_day = load_datetime()[0]

class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["shopstar.pe"]   
    start_urls = ["https://shopstar.pe"]

    def __init__(self, *args, **kwargs):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        super(ShopSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b
        self.urls = links()[int(int(self.u)-1)]

    def get_json(self, url):
    
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            
            # Using regular expression to find and extract JSON-like content from the HTML
            pattern = r'<template data-type="json" data-varname="__STATE__">.*?<script>(.*?)</script>.*?</template>'
            match = re.search(pattern, html_content, re.DOTALL)
            
            if match:
                json_str = match.group(1)
                #print(json_str)  # Printing the extracted JSON-like content
            else:
                print("No JSON-like content found in the HTML.")
            json_data = json.loads(json_str)

            productos = []
            for i,v in json_data.items():
                try:
                    pro = v["cacheId"].replace("sp-","")

                    #print(pro)
                    productos.append("fq=productId:"+pro+"&")
                except: 
                    continue 
                    
            #print(productos)

            web1 = "https://shopstar.pe/api/catalog_system/pub/products/search?"
            url = web1 + ''.join(productos)
            return url
        
    def brand_allowed(self):
        collection1 = self.db["todo"]
        shoes = collection1.find({})
        shoes_list = [doc["brand"] for doc in shoes]
        return shoes_list 

    def __init__(self, *args, **kwargs):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        super(ShopSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed() # Initialize self.lista based on self.b
        self.urls = links()[int(int(self.u)-1)]

    
    def brand_allowed(self):

        collection1 = self.db["todo"]
        collection2 = self.db["nada"]
        shoes = collection1.find({})
        nada = collection2.find({})

        allowed_brands = [doc["brand"] for doc in shoes]
        allowed_brands2 = [doc["brand"] for doc in nada]

        return allowed_brands,allowed_brands2




    def start_requests(self):

    

        count = 0
        for i, v in enumerate(self.urls):
            count = count+1


            
                # for e in range (50):
                    
                #     link = v[0]+"&page="+str(e+1)
          
                #     url = productId_extract(link)
      
                #     yield scrapy.Request(url, self.parse)
          
            
            yield scrapy.Request(v, self.parse)

        



            
        #web_json = []
            
            
            #self.urls = [(url,page), (url,page)]
            #v = (url,page)
      
            # for e in range (50):
            #     # print(v[0])
            #     # print(v[1])
            #     url = get_json(v[0]+"&page="+str(e+1))
                # try:
                #     web_json.append(url)
                # except:
                #     continue
              
        # for i in web_json:
        #     # print(i)
        # web1 = "https://shopstar.pe/api/catalog_system/pub/products/search?"
        # for i in range(0, 100000000000, 50):
        #     part = []
        #     for e in range(i, i + 50):
        #         if e < 100000000000:
        #             web2 = "fq=productId:" + str(e) + "&"
        #             part.append(web2)
        #     url = web1 + "".join(part)
        #     yield scrapy.Request(url, self.parse)
        #     #web_json = None

    def parse(self, response):

        item = ShopstarItem()
        print(response.status)
     
        #print(response.body)
        html_content = response.body
        json_data = json.loads(html_content)
        #elements = response.xpath("//li[@id][@class='slider__slide']")
        elements = json_data

        count = 0
        for i in elements:
            count = count +1
           
            item["product"] = i["productName"]
            item["brand"]= i["brand"]


#######################################
            product = item["brand"]
            if product.lower() not in (self.lista[0]):
                continue
            
###############################

            item["image"]=i["items"][0]["images"][0]["imageUrl"]#image
            item["sku"]=i["items"][0]["itemId"]
            item["_id"] =  item["sku"]
            item["link"]=i["link"]
            try:
                item["best_price"]= i["items"][0]["sellers"][0]["commertialOffer"]["Price"]
            except:item["best_price"] = 0

            try:
                item["list_price"]= i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]
            except: item["list_price"] = 0
            # available = i["items"][0]["sellers"][0]["commertialOffer"]["IsAvailable"]


           
            try:
                ibk_dsct = float(i["items"][0]["sellers"][0]["commertialOffer"]["Teasers"][0]["<Effects>k__BackingField"]["<Parameters>k__BackingField"][0]["<Value>k__BackingField"]    )  
            except:
                ibk_dsct = 0  
                
            try:
                plin_dsct = float(i["items"][0]["sellers"][0]["commertialOffer"]["PromotionTeasers"][0]["Effects"]["Parameters"][0]["Value"]  )  
            except:
                plin_dsct = 0

            if item["best_price"] and  item["list_price"] !=0:
                item["web_dsct"] =    round(float(100-(item["best_price"]*100/item["list_price"])))
            else:
                item["web_dsct"] = 0

            if item["best_price"] and float(ibk_dsct)>0 :
                 item["card_price"]= round( float(item["best_price"] -float(item["best_price"]*ibk_dsct/100)),2)
                
            else:
                item["card_price"]= 0


            if item["best_price"] and float(ibk_dsct)>0 :
                item["card_dsct"] = round(float(100-(item["card_price"]*100/item["list_price"])),1)
                
                #card_dsct = float(100-(item["best_price"]*ibk_dsct/100))
            else:
                 item["card_dsct"]= 0

            if item["list_price"] and item["card_price"] and item["best_price"] == 0:
                continue

           
            # if item["best_price"] and float(ibk_dsct)>0 :
            #      item["card_price"]= round( float(item["best_price"] -float(item["best_price"]*ibk_dsct/100)),2)
                
            # else:
            #     item["card_price"]= 0

            item["list_price"] = float(item["list_price"])
            item["best_price"] = float(item["best_price"])
            item["card_price"] = float(item["card_price"])
            item["web_dsct"] = float(item["web_dsct"])
            item["card_dsct"] = float(item["card_dsct"])



            print( item["product"] )
            print( item["brand"] )
            print( item["link"] )
            print( item["image"] )
            print( item["sku"] )
            print(self.urls)
            print("best price " + str(item["best_price"]))
            print("list price "+ str(item["list_price"]))
            print("card price "+str(item["card_price"]))
            print("web dsct "+str(item["web_dsct"])+"%")
            # print(ibk_dsct)
            print("card dsct "+str(item["card_dsct"])+"%")
            # print(card_dsct)
            print()


            item["market"] = "shopstar"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"]= "https://shopstar.pe"
           


            print("ese producto es el "+str(count))
       
        
          
            yield item
