import scrapy
import time
from ripley.spiders import url_list 
import scrapy
from ripley.items import RipleyItem
from datetime import datetime
from datetime import date
import random
import uuid
from ripley.spiders.urls_db import *
import pymongo
from decouple import config

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class RippleScrapSpider(scrapy.Spider):
    name = "ripley_scrap"

    user_agents = [

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/80.0.361.62",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140",
        # Add more user-agent strings here
    ]

    def __init__(self, *args, **kwargs):
        super(RippleScrapSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed()# Initialize self.lista based on self.b

    def brand_allowed(self):
        collection1 = self.db["todo"]
        shoes = collection1.find({})
        shoes_list = [doc["brand"] for doc in shoes]
        return shoes_list 
    
    links =[]
    def start_requests(self):

        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        urls = links()[int(u-1)]


        for i, v in enumerate(urls):
            for e in range((round(v[1]/48)+1)):
                if "&page=" in v[0]:
                     web = v[0]
                   
                     url = web + str(e + 1) +"&s=mdco"
                     print(url)
                    
                     
                else:
                    web = v[0].replace("s=mdco","page=")
                
                    url = web + str(e + 1)  
                      
                
                # Select a random user-agent
                user_agent = random.choice(self.user_agents)

                headers = {'User-Agent': user_agent}
                
                yield scrapy.Request(url, self.parse, headers=headers  )
        
            
    def parse(self, response):
            item = RipleyItem()
            productos = response.css("div.catalog-product-item.catalog-product-item__container.col-xs-6.col-sm-6.col-md-4.col-lg-4")

            for i in productos:
            
                item["brand"] = i.css('div.brand-logo span::text').get()
                if item["brand"] == None:
                    item["brand"] = "Revisar codigo"
                product = item["brand"]
                if self.lista == []:
                    pass
                else:
                    if product.lower() not in self.lista:
                        continue
                try:
                    item["product"] = i.css(".catalog-product-details__name::text").get()
                except: item["product"] = None

                try:
                    item["image"] = i.css("img::attr(data-src)").get()
                except:  item["image"] = None

                image_start = item["image"][:6]
                if image_start != "https:":
                    item["image"] = "https:" + item["image"]

                part_number = i.css("a::attr(id)")
                sku_id = i.css("a::attr(data-partnumber)")
                print(part_number)
                print(sku_id)
                part_number = i.css("a::attr(id)").get()
                sku_id = i.css("a::attr(data-partnumber)").get()
                print()
                print(part_number)
                print(sku_id)

                if len(part_number) > len(sku_id):
                    item["sku"] = str(part_number)
                
                else:
                    item["sku"] = str(sku_id)


                


      

                item["_id"] =  item["sku"]

                try:
                    item["web_dsct"] = round(float(i.css(".catalog-product-details__discount-tag::text").get().replace("-", "").replace("%", "")))
                except:
                    item["web_dsct"] = 0
                
                try:
                    item["list_price"] = i.css(".catalog-prices__list-price.catalog-prices__lowest.catalog-prices__line_thru::text").get().replace("S/", "").replace(",", "")
                except:
                    item["list_price"] = 0

                try:
                    item["best_price"] = i.css(".catalog-prices__offer-price::text").get().strip().replace("S/", "").replace(",", "")
                except:
                    item["best_price"] = 0

                try:
                    item["card_price"] = i.css(".catalog-prices__card-price::text").get().replace("S/", "").replace(",", "")
                except:
                    item["card_price"] = 0

                item["list_price"]     = float(item["list_price"] )
                item["best_price"]     = float(item["best_price"] )
                item["web_dsct"]     = float(item["web_dsct"] )
                item["card_price"]     = float(item["card_price"] )

                if item["list_price"] and item["card_price"] and item["best_price"] == 0:
                 continue

                item["link"] = i.css(".catalog-product-item.catalog-product-item__container.undefined::attr(href)").get()
                item["link"] = "https://simple.ripley.com.pe" + item["link"]
                item["card_dsct"] = float(0)
                item["market"]= "ripley"
                item["date"]= load_datetime()[0]
                item["time"]= load_datetime()[1]
                item["home_list"] = response.url       


             
                yield item
         
       
