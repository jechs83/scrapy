import scrapy
from coolbox.items import CoolboxItem
from datetime import datetime
from datetime import date
from coolbox.spiders import url_list 
from coolbox.spiders.urls_db import *
import time
from bs4 import BeautifulSoup
import json
import logging
import requests

import scrapy
from datetime import datetime
from datetime import date
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
        
    return date_now, time_now, today

current_day = load_datetime()[0]


class CoolboxSpider(scrapy.Spider):
    name = 'cool'
    allowed_domains = ['coolbox.pe']
    start_urls = ['https://www.coolbox.pe/audio?page=27']


    def __init__(self, *args, **kwargs):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        super(CoolboxSpider, self).__init__(*args, **kwargs)
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
        for i,v  in enumerate (self.urls):
      
            for i in range(50):

                url = v[0]+str(i+1)
     
                response = requests.get(url) 
                soup = BeautifulSoup(response.text, 'html.parser')

                template_element = soup.find_all('script')

                for i in template_element:
                
                    if  "__STATE__" in i.text:
                            data = i.text.strip()

                            state_index = data.find("__STATE__ =")

                            if  state_index  != -1:
                                    # Remove the portion of the string from "__STATE__" to the beginning
                                result_string = data[state_index: ]
                                result_string =  result_string.replace("__STATE__ =","")
                    
                                json_data = json.loads(result_string)

                                productId_web = []
                                for product_key, product_info in json_data.items():
                                    try:
                                        product_id = product_info['productId']
                                        productId_web.append("fq=productId:"+product_id+"&")
                                    except: 
                                        continue
                                productId_web = "".join(productId_web)

                                web = "https://www.coolbox.pe/api/catalog_system/pub/products/search?"+productId_web

                                yield scrapy.Request(web, self.parse)





    def parse(self, response):

        item = CoolboxItem()
        print(response.status)
        html_content = response.body
        json_data = json.loads(html_content)
        #elements = response.xpath("//li[@id][@class='slider__slide']")
        elements = json_data

        count = 0
        for i in elements:
            count = count +1
           
            count = count +1
           
            item["product"] = i["productName"]
            item["brand"]= i["brand"]



            # product = item["brand"]


            # if product.lower() not in (self.lista[0]):
            #     print("no hay producto ")
            #     continue
            


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


            if item["best_price"] and float(plin_dsct)>0 :
                item["card_dsct"] = round(float(100-(item["card_price"]*100/item["list_price"])),1)
                
                #card_dsct = float(100-(item["best_price"]*ibk_dsct/100))
            else:
                 item["card_dsct"]= 0


            if item["best_price"] and float(ibk_dsct)>0 :
                 item["card_price"]= round( float(item["best_price"] -float(item["best_price"]*ibk_dsct/100)),2)
                
            else:
                item["card_price"]= 0

            if item["list_price"] and item["card_price"] and item["best_price"] == 0:
                continue


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

            item["market"] = "coolbox"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"]= "https://coolbox.pe"
           
            yield item