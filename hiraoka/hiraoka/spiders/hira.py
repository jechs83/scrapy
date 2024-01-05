import scrapy
from hiraoka.items import HiraokaItem
from datetime import datetime
from datetime import date
from hiraoka.spiders.urls_db import *
import pymongo
from decouple import config
def load_datetime():

    
    today = date.today()
    now = datetime.now()
    date_now = today.strftime("%d/%m/%Y")  
    time_now = now.strftime("%H:%M:%S")
        
    return date_now, time_now, today

class HiraSpider(scrapy.Spider):
    name = "hira"
    allowed_domains = ["hiraoka.com"]
    start_urls = ["https://hiraoka.com"]


    def __init__(self, *args, **kwargs):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        super(HiraSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed() # Initialize self.lista based on self.b
        self.urls = links()[int(int(self.u)-1)]
    
    def brand_allowed(self):

        collection1 = self.db["todo"]
        shoes = collection1.find({})
        allowed_brands = [doc["brand"] for doc in shoes]
        return allowed_brands


    def start_requests(self):
         
         for i, v in enumerate(self.urls):
   
                for e in range (v[1]+6):
                    url = v[0]+"?p="+(str(e+1))
                    yield scrapy.Request(url, self.parse)
           
       
      

    def parse(self, response):
        item = HiraokaItem()

        productos  =response.css('li.item.product.product-item')

        for i in productos:
            item["brand"] = i.css(".product-item-link::text").get()
            item["brand"] = item["brand"].strip()

            if self.lista == []:
                pass
            else:
                if item["brand"].lower() not in self.lista:
                    continue



            item["product"] = i.css(".product-item-link::attr(title)").get()
            item["link"] = i.css("a::attr(href)").get()
            item["image"] = i.css("img::attr(src)").get()


            sku = i.css('strong.product-item-sku::text').get()
            item["sku"] = sku.replace("Código","").strip()

            item["_id"]=  item["sku"] 


          
            try:
                list_price = i.css("span.old-price").css("span.price::text").get()
                item["list_price"] = float(list_price.replace("S/","").replace(",","").strip())
            except: item["list_price"] = 0
            try:
                best_price = i.css("span.special-price").css("span.price::text").get()
                item["best_price"] = float(best_price.replace("S/","").replace(",","").strip())
            except: item["best_price"] = 0


            if item["best_price"]   or item["list_price"] != 0:
                item["web_dsct"] = round(100-(item["best_price"] *100/item["list_price"] ))
            
            else:
                item["web_dsct"] = 0

            item["market"] = "hiraoka"
            item["card_dsct"]= 0
            item["card_price"]= 0

            if item["list_price"] and item["card_price"] and item["best_price"] == 0:
                continue
            item["date"]= load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"] = response.url


            yield item

           
            print()
           

            
        pass
