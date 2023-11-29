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
from shopstar.spiders.urls_db import links


def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
    
 return date_now, time_now, today


# def get_json(url):
    
#         response = requests.get(url)
#         if response.status_code == 200:
#             html_content = response.text
            
#             # Using regular expression to find and extract JSON-like content from the HTML
#             pattern = r'<template data-type="json" data-varname="__STATE__">.*?<script>(.*?)</script>.*?</template>'
#             match = re.search(pattern, html_content, re.DOTALL)
            
#             if match:
#                 json_str = match.group(1)
#                 #print(json_str)  # Printing the extracted JSON-like content
#             else:
#                 print("No JSON-like content found in the HTML.")
#             json_data = json.loads(json_str)

#             productos = []
#             for i,v in json_data.items():
#                 try:
#                     pro = v["cacheId"].replace("sp-","")

#                     #print(pro)
#                     productos.append("fq=productId:"+pro+"&")
#                 except: 
#                     continue 
                    
#             #print(productos)

#             web1 = "https://shopstar.pe/api/catalog_system/pub/products/search?"
#             url = web1 + ''.join(productos)
#             return url
        


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

    def start_requests(self):

        for i,v in enumerate (self.urls):

            for e in range (50):

                url = self.get_json(v[0]+"&page="+str(e+1))
                yield scrapy.Request(url, self.parse)




            
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
        web = response

        #print(type(web))
        web =   json.loads(response.body)
        
        for i in web:
            
            item["sku"] = i["productId"]
            item["_id"] = item["sku"]
            item["product"] =  i["productName"]


            item["brand"] =  i["brand"]

            try:
                item["brand"]= i["brand"]
                product = item["brand"]
            
                if self.lista == []:
                    pass
                else:
                        if product.lower() not in self.lista:
                            continue
            except: item["brand"]= None
            
            try:
                item["image"] = i["items"][0]["images"][0]["imageUrl"]
            except:  item["image"]  = None
            item["link"] = i["link"]
            item["best_price"] = float(i["items"][0]["sellers"][0]["commertialOffer"]["Price"])
            item["list_price"] =   float(i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"])
            item["market"] = "shopstar"
            item["date"] =load_datetime()[0]
            item["time"] =load_datetime()[1]
            try:
                item["web_dsct"] = round(float(100- item["best_price"]*100/item["list_price"]))
            except:  item["web_dsct"] = 0

            try:
                card_dsct =  i["items"][0]["sellers"][0]["commertialOffer"]["PromotionTeasers"][0]["Effects"]["Parameters"][0]
                card_dsct =float(item["card_dsct"]["Value"])
            except: card_dsct = 0

            # try:
            #     item["plin_dsct"] =  i["items"][0]["sellers"][0]["commertialOffer"]["PromotionTeasers"][1]["Effects"]["Parameters"][0]
            #     item["plin_dsct"] = float(item["plin_dsct"]["Value"])
            # except: item["plin_dsct"] = 0
           
            # print(item["ibk_dsct"])
            item["card_dsct"] = 0

            if card_dsct !=0:
                item["card_price"] = float((item["best_price"]*(100-card_dsct ))/100)
            else: 
                item["card_price"] = 0

            # try:
            #     item["plin_dsct"] =  i["items"][0]["sellers"][0]["commertialOffer"]["PromotionTeasers"][1]["Effects"]["Value"]
            # except:  item["plin_dsct"] = 0

            item["home_list"] = "shopstar.pe"
         
            #print(item["plin_dsct"])

            

            yield item
        
       
        pass
