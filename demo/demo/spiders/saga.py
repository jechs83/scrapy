import scrapy
import sys
import json
from demo.items import DemoItem
from datetime import datetime
from datetime import date
import pymongo
from demo.spiders.urls_db import *
from  demo.spiders import url_list 
from decouple import config
import time




def load_datetime():
    
    today = date.today()
    now = datetime.now()
    date_now = today.strftime("%d/%m/%Y")  
    time_now = now.strftime("%H:%M:%S")
        
    return date_now, time_now, today

current_day = load_datetime()[0]

class SagaSpider(scrapy.Spider):
    #list_to_skip = skip_brand()
    name = "saga"
    allowed_domains = ["falabella.com.pe"]
    handle_httpstatus_list = [200, 206]


    def __init__(self, *args, **kwargs):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        super(SagaSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed() # Initialize self.lista based on self.b
        self.urls = links()[int(int(self.u)-1)]
    
    def brand_allowed(self):
        collection1 = self.db["todo"]
        shoes = collection1.find({})
        shoes_list = [doc["brand"] for doc in shoes]
        collection1 = self.db["nada"]
        nada = collection1.find({})
        return shoes_list ,nada


    def start_requests(self):
       
        for i, v in enumerate(self.urls):
            if "tottus" in v[0]:
                for e in range (v[1]+10):
                    url = v[0]+ "?subdomain=tottus&page="+str(e+1) +"&store=tottus"
                    yield scrapy.Request(url, self.parse)
            if "sodimac" in v[0]:
                for e in range (v[1]+10):
                    url = v[0]+ "?subdomain=sodimac&page="+str(e+1)+"&store=sodimac"
                    yield scrapy.Request(url, self.parse)
            else:
                for e in range (v[1]+10):
                    url = v[0]+ "?page="+str(e+1) 
                    yield scrapy.Request(url, self.parse)
                

    def parse(self, response):
      
        if response.status != 200:
        # If the response status is not 200, skip processing this link and move to the next one
                self.logger.warning(f"Skipping URL {response.url} due to non-200 status code: {response.status}")
                return
        
        if "/noResult" in response.url:
                # Move to the next URL in the array (since it is a "noResult" page)
                self.logger.info("Skipping this URL and moving to the next one.")
                return
    
        item = DemoItem()

        # Find the script tag with the JSON data
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

        if script_tag:
            json_content = json.loads(script_tag)

            # Assuming the relevant JSON data is under "props" -> "pageProps" in the JSON response
            page_props = json_content.get('props', {}).get('pageProps', {}).get("results",{})

        productos = page_props
        
        for i in productos:
            
                
    
                item["brand"]= i["brand"]


        
                producto = item["brand"].lower()

                if self.lista[0] == []:
                    pass
                else:
                    if producto not in self.lista[0]:

                        continue

                item["product"]=  i["displayName"]

                item["sku"] = i["skuId"]
                item["_id"] =i["skuId"]

                if len(i["prices"])== 1:

                    item["best_price"] = 0
                    item["card_price"] = 0
                    item["list_price"] = float(i["prices"][0]["price"][0].replace(",",""))

                elif len(i["prices"])== 2:
                    item["best_price"] = float(i["prices"][0]["price"][0].replace(",",""))
                    item["card_price"] = 0
                    item["list_price"] = float(i["prices"][1]["price"][0].replace(",",""))

                elif len(i["prices"])== 3:
                    item["best_price"] = float(i["prices"][1]["price"][0].replace(",",""))
                    item["card_price"] = float(i["prices"][0]["price"][0].replace(",",""))
                    item["list_price"] = float(i["prices"][2]["price"][0].replace(",",""))

             

                item["link"]=i["url"]

                try:
                 item["image"]=i["mediaUrls"][0]
                except:
                 item["image"]=str(i["mediaUrls"])
        
                try:
                 item["web_dsct"]=float(i["discountBadge"]["label"].replace("-","").replace("%",""))
                except:
                        item["web_dsct"]=0


                try:
                    item["dsct_app"] = i["multipurposeBadges"][0]["label"]
                
                    if item["dsct_app"]=="Dscto extra por app" :
                        item["dsct_app"]  = 1
                    else:
                        item["dsct_app"] = 0
                except: 
                    item["dsct_app"] = 0

                if item["list_price"] and item["card_price"] and item["best_price"] == 0:
                 continue


                item["market"]= "saga"
                item["date"]= load_datetime()[0]
                item["time"]= load_datetime()[1]
                item["home_list"] = response.url
                item["card_dsct"] = 0

                yield item
         

            



