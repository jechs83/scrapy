import scrapy
from scrapy import Selector
from plazavea.items import PlazaveaItem
from datetime import datetime
from datetime import date
from plazavea.spiders import url_list 
from plazavea.spiders.urls_db import *

import time
import pymongo
from decouple import config
import json





def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

current_day = load_datetime()[0]
current_time = load_datetime()[1]

class VeaSpider(scrapy.Spider):
    name = "vea"
    allowed_domains = ["plazavea.com.pe"]

    def __init__(self, *args, **kwargs):
        # u = int(getattr(self, 'u', '0'))
        # b = int(getattr(self, 'b', '0'))
        super(VeaSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b
        self.urls = links()[int(int(self.u)-1)]

    def brand_allowed(self):
        collection1 = self.db["todo"]
        shoes = collection1.find({})
        allowed_brands = [doc["brand"] for doc in shoes]
        return allowed_brands 
    
    
    def start_requests(self):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))

        # if u == 1:
        #     urls = url_list.list1

        # elif u == 2:
        #         urls = url_list.list2
        # elif u == 3:
        #         urls = url_list.list3
        # elif u == 4:
        #         urls = url_list.list4
        # elif u == 5:
        #         urls = url_list.list5
        # elif u == 6:
        #         urls = url_list.list6
        # elif u == 7:
        #         urls = url_list.list7
        # elif u == 8:
        #         urls = url_list.list8
        # elif u == 9:
        #         urls = url_list.list9
        # elif u == 10:
        #         urls = url_list.list10
        
        # else:
        #     urls = []
   
        for i, v in enumerate(self.urls):
            
            for e in range(v[1]):
                url = v[0]+"?page="+str(e+1)
                print(url)
                yield scrapy.Request(url, self.parse)

    def parse(self, response):
    
        item = PlazaveaItem()

        productos = response.css('div.Showcase__content')

        for i in productos:
            item["product"]=  i.css('div.Showcase__content::attr(title)').get()
            item["image"]=  i.css( 'img::attr(src)').get()
            item["brand"]=  i.css('div.Showcase__brand a::text').get()
            item["link"]=  i.css('a.Showcase__name::attr(href)').get()
            prices =    i.css( "div.Showcase__priceBox__row")
            try:
                price1 = prices.css("div.Showcase__oldPrice::text").get()
                item["list_price"] = float(price1.replace("S/","").replace(",",""))
            except:
                 item["list_price"] = 0

            try:
                price2 = prices.css("div.Showcase__salePrice::text").get()
                item["best_price"] = float(price2.replace("S/","").replace(",",""))
            except:
                  item["best_price"] = 0

            item["card_price"] = 0

            try:
             item["web_dsct"] =  round(100-(item["best_price"]*100/ item["list_price"]) )
            except:
                item["web_dsct"] = 0


            item["home_list"] = response.url

            item["sku"] = i.css("[data-sku]::attr(data-sku)").get()
            item["_id"]=   item["sku"]

            item["card_dsct"] = 0

            item["date"] = current_day
            item["time"] = current_time
            item["market"] = "pla"
            
            yield item
        
