import scrapy
from oechsle.items import OechsleItem
from datetime import datetime
from datetime import date
#from oechsle.spiders import url_list 
import uuid
import pymongo
from oechsle.spiders.urls_db import *
from decouple import config

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

current_date =  load_datetime()[0]


class OhSpider(scrapy.Spider):
    name = "oh"
    allowed_domains = ["oechsle.pe"]    

    def __init__(self, *args, **kwargs):
        super(OhSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed() # Initialize self.lista based on self.b

    def brand_allowed(self):
        collection1 = self.db["todo"]
        shoes = collection1.find({})
        shoes_list = [doc["brand"] for doc in shoes]
        return shoes_list 
    
    def start_requests(self):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        urls = links()[int(u-1)]
       
        for i, v in enumerate(urls):
            for e in range (v[1]+10):
                url = v[0]+"?&optionOrderBy=OrderByScoreDESC&O=OrderByScoreDESC&page="+str(e+1)
                yield scrapy.Request(url, self.parse)
                

    def parse(self, response):
        item = OechsleItem()
        productos = response.css('li')  

        for i in productos:

            item["sku"] = i.css("div.product.instock::attr(data-id)").get()
            if  item["sku"] == None:
                 continue
            
            item["_id"] =str(item["sku"])
            item["brand"]= i.css("div.product.instock::attr(data-brand)").get()
            product = item["brand"]
            if self.lista == []:
                pass
            else:
                if product.lower() not in self.lista:
                    continue
                        
            item["product"] =i.css("div.product.instock::attr(data-name)").get()
            item["link"] =i.css("div.product.instock::attr(data-link)").get()
            item["image"]= i.css("div.productImage.prod-img.img_one img::attr(src)").get()
            try:
                item["list_price"] = i.css("span.text.text-gray-light.text-del.fz-11.fz-lg-13.ListPrice::text").get()
                item["list_price"] = round(float(item["list_price"].replace(",","").replace("S/.","")))
            except:item["list_price"]  = 0

            try:
                item["best_price"]  =i.css("span.text.fz-lg-15.fw-bold BestPrice::text").get()
                item["best_price"] = round(float(str(item["best_price"]).replace(",","").replace("S/.","")))
            except: item["best_price"] = None

            if item["best_price"] == None:
                    item["best_price"] = i.css("span.text.fz-lg-15.fw-bold.BestPrice::text").get()
                    try:
                        item["best_price"] = round(float(str(item["best_price"]).replace(",","").replace("S/.","")))
                    except:  item["best_price"] = 0

            item["web_dsct"] = i.css("span.flag-of.ml-10::text").get()
            if item["web_dsct"] != None:
                item["web_dsct"] = item["web_dsct"].replace("-","").replace("%","").replace(",",".")
                item["web_dsct"] = round(float( item["web_dsct"]))
            else: item["web_dsct"]  = 0

            item["home_list"]=response.url
            item["card_dsct"] = 0
            item["card_price"] = 0 
            item["market"]= "oechsle"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]

            yield item
             

 

