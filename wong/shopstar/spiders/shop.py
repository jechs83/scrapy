import scrapy
from scrapy import Selector
from shopstar.items import ShopstarItem
from datetime import datetime
from datetime import date
from shopstar.spiders.urls_db import *

from shopstar.spiders import url_list 
import json
import requests
from bs4 import BeautifulSoup
import pymongo
from decouple import config
import time




def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

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
      

        def productId_extract(web):

            response = requests.get(web)
            productId_web = []

            # if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            template_element = soup.find('template', {'data-type': 'json', 'data-varname': '__STATE__'})
            script_element = template_element.find('script')

           
            json_content = script_element.get_text(strip=True)
        
            json_data = json.loads(json_content)

            for product_key, product_info in json_data.items():
                try:
                    product_id = product_info['productId']
                    #print(f"Product ID for {product_id}")
                    productId_web.append("fq=productId:"+product_id+"&")
                except: 
                    continue
            productId_web = "".join(productId_web)
            web = "https://www.wong.pe/api/catalog_system/pub/products/search?"+productId_web

            return web

        for i, v in enumerate(self.urls):
            
                for e in range (10):
                    
                    link = v[0]+"&page="+str(e+1)
          
                    url = productId_extract(link)
      
                    yield scrapy.Request(url, self.parse)

        

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
          



            #product = item["brand"]
    
    
            # if self.lista == []:
            #     pass
            # else:
            # print((self.lista[0]))
            # print(product.lower())

            # if product.lower() not in (self.lista[0]):
            #     print("no hay producto ")
            #     continue
            


            item["image"]=i["items"][0]["images"][0]["imageUrl"]#image
            item["sku"]=i["items"][0]["itemId"]
            item["_id"] =  item["sku"]
            item["link"]=i["link"]
            '''
            try:
                item["best_price"]= i["items"][0]["sellers"][0]["commertialOffer"]["Price"]
            except:item["best_price"] = 0

            try:
                item["list_price"]= i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]
            except: item["list_price"] = 0
            # available = i["items"][0]["sellers"][0]["commertialOffer"]["IsAvailable"]


           
            # try:
            #     ibk_dsct = float(i["items"][0]["sellers"][0]["commertialOffer"]["Teasers"][0]["<Effects>k__BackingField"]["<Parameters>k__BackingField"][0]["<Value>k__BackingField"]    )  
            # except:
            #     ibk_dsct = 0  
                
            # try:
            #     plin_dsct = float(i["items"][0]["sellers"][0]["commertialOffer"]["PromotionTeasers"][0]["Effects"]["Parameters"][0]["Value"]  )  
            # except:
            #     plin_dsct = 0

            if item["best_price"] and  item["list_price"] !=0:
                item["web_dsct"] =    round(float(100-(item["best_price"]*100/item["list_price"])))
            else:
                item["web_dsct"] = 0

            # if item["best_price"] and float(ibk_dsct)>0 :
            #      item["card_price"]= round( float(item["best_price"] -float(item["best_price"]*ibk_dsct/100)),2)
                
            # else:
            item["card_price"]= 0


            # if item["best_price"] and float(plin_dsct)>0 :
            #     item["card_dsct"] = round(float(100-(item["card_price"]*100/item["list_price"])),1)
                
            #     #card_dsct = float(100-(item["best_price"]*ibk_dsct/100))
            # else:
            #      item["card_dsct"]= 0


            # if item["best_price"] and float(ibk_dsct)>0 :
            #      item["card_price"]= round( float(item["best_price"] -float(item["best_price"]*ibk_dsct/100)),2)
                
            # else:
            #     item["card_price"]= 0


            print( item["product"] )
            print( item["brand"] )
            print( item["link"] )
            print( item["image"] )
            print( item["sku"] )
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
            # print(product)
            # print(item["product"])
            # print(item["image"])
            # print(item["sku"])
            # print(item["link"])
            # print(item["best_price"])
            # print(item["list_price"])


            print("ese producto es el "+str(count))
            '''
        
          
            yield item