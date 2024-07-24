import scrapy
import sys
import json
from demo.items import DemoItem
from datetime import datetime

import datetime
import pymongo

from demo.spiders.urls_db import *
from decouple import config
from scrapy.exceptions import CloseSpider

import time



class SagaSpider(scrapy.Spider):
    #list_to_skip = skip_brand()
    name = "saga"
    allowed_domains = ["falabella.com.pe"]
    handle_httpstatus_list = [200, 206]


    def __init__(self, *args, **kwargs):
        super(SagaSpider, self).__init__(*args, **kwargs)
        self.u = int(getattr(self, 'u', '0'))
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.urls = links()[self.u - 1]
        self.db = self.client['saga']
        self.collection_name = self.db['scrap3']

        self.seen_skus = set()
        self.duplicate_count = 0


    def page_exists(self, response):
        # Check if the page contains products or if it's a "no results" page
        return "/noResult" not in response.url and response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

    def start_requests(self):
        
        for i, v in enumerate(self.urls):
                for e in range (v[1]+10):              
                    url = v[0]+ "&page="+str(e)  
                    yield scrapy.Request(url, self.parse)


    def check_page_and_parse(self, response):
        if self.page_exists(response):
            yield from self.parse(response)
        else:
            # If the page doesn't exist, don't yield any more requests for this URL
            self.logger.info(f"Reached non-existent page: {response.url}")
            return            

    def parse(self, response):

        if not self.page_exists(response):
            # If the page doesn't exist, raise a CloseSpider exception to stop the spider
            raise scrapy.exceptions.CloseSpider(reason='Reached non-existent page')
      
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
             
                try:
                    item["brand"]= i["brand"]
             
                except:
                    item["brand"]="generico"




        
                #producto = item["brand"].lower()

                # if self.lista[0] == []:
                #     pass
                # else:
                #     if producto not in self.lista[0]:

                #         continue
          
                item["product"]=  i["displayName"]

                item["sku"] = i["skuId"]

                if item["sku"] in self.seen_skus:
                    self.duplicate_count += 1
                else:
                    self.seen_skus.add(item["sku"])
              
        

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

                # if item["dsct_app"] and item["web_dsct"] >0 <=59:
                #     continue

                item["market"]= "saga"
                current_datetime = datetime.datetime.now()
                item["date"] = current_datetime.strftime("%d/%m/%Y")
                item["time"] = current_datetime.strftime("%H:%M:%S")
                item["home_list"] = response.url
                item["card_dsct"] = 0

                print()
                print(i["brand"])
                print(i["displayName"])
                print(i["url"])
                print(item["best_price"])
                print(item["card_price"] )
                print(item["list_price"] )
 
                collection = self.db["scrap"]
                filter = { "sku": item["sku"]}
                update = {'$set': dict(item)}
                result = collection.update_one(filter, update, upsert=True)


    def closed(self, reason):
        self.logger.info(f"Total de SKUs únicos: {len(self.seen_skus)}")
        self.logger.info(f"Total de SKUs duplicados: {self.duplicate_count}")


