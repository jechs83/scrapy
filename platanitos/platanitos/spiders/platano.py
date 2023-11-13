import scrapy
from platanitos.items import PlatanitosItem
from scrapy import Selector
from pymongo import MongoClient

from datetime import datetime
from datetime import date
from platanitos.spiders import url_list 
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

class PlatanoSpider(scrapy.Spider):
    name = "platano"
    allowed_domains = ["platanitos.com"]
    start_urls = ["http://platanitos.com/"]

    def __init__(self, *args, **kwargs):
        super(PlatanoSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient("mongodb://192.168.9.66:27017")
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b

    def brand_allowed(self):
        collection1 = self.db["todo"]
        collection2 = self.db["electro"]
        collection3 = self.db["tv"]
        collection4 = self.db["cellphone"]
        collection5 = self.db["laptop"]
        collection6 = self.db["consola"]
        collection7 = self.db["audio"]
        collection8 = self.db["colchon"]
        collection9 = self.db["nada"]
        collection10 = self.db["sport"]
        
        shoes = collection1.find({})
        electro = collection2.find({})
        tv = collection3.find({})
        cellphone = collection4.find({})
        laptop = collection5.find({})
        consola = collection6.find({})
        audio = collection7.find({})
        colchon = collection8.find({})
        nada = collection9.find({})
        sport = collection10.find({})


        shoes_list = [doc["brand"] for doc in shoes]
        electro_list = [doc["brand"] for doc in electro]
        tv_list = [doc["brand"] for doc in tv]
        cellphone_list = [doc["brand"] for doc in cellphone]
        laptop_list = [doc["brand"] for doc in laptop]
        consola_list = [doc["brand"] for doc in consola]
        audio_list = [doc["brand"] for doc in audio]
        colchon_list = [doc["brand"] for doc in colchon]
        nada_list = [doc["brand"] for doc in nada]
        sport_list = [doc["brand"] for doc in sport]
        return shoes_list ,electro_list,tv_list,cellphone_list,laptop_list, consola_list, audio_list, colchon_list,nada_list,sport_list
    

    #start_urls=[ "https://www.plazavea.com.pe/api/catalog_system/pub/products/search?fq=C:/679/&_from=2041&_to=2061&O=OrderByScoreDESC&"]
 
    
    
    def start_requests(self):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))

        if u == 1:
            urls = url_list.list1

        elif u == 2:
                urls = url_list.list2
        elif u == 3:
                urls = url_list.list3
        elif u == 4:
                urls = url_list.list4
        else:
            urls = []
        count= 20
        for i, v in enumerate(urls):
            print(v[0])

            # for e in range(120):
            #       if e ==0:
            #         url = v[0]+str(e+1)
            #         yield scrapy.Request(url, self.parse)


            for e in range(120):
                url = v[0]+(str(e+100))
                print(url)

                yield scrapy.Request(url, self.parse)


    def parse(self, response):
        for product in response.css("div.col-flt.col-3"):
            item = PlatanitosItem()

            item['brand'] = product.css("p.nd-ct__item-title.line-clamp-2::text").get()
            item['product'] = product.css("p.nd-ct__item-title.line-clamp-2::text").get()
            item['list_price'] = product.css("p.nd-ct__item-prices::text").re_first(r'\d+\.\d+')
            item['best_price'] = product.css("p.nd-ct__item-prices::text").re_first(r'\d+\.\d+')
            item['image'] = product.css("img::attr(src)").get()
            item['link'] = response.urljoin(product.css("a::attr(href)").get())
            item['sku'] = item['product'].replace(" ", "")
            item['dsct'] = self.calculate_discount(item['best_price'], item['list_price'])

            yield item

        # Handle pagination if necessary
        next_page = response.css("your-pagination-selector::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def calculate_discount(self, best_price, list_price):
        if best_price and list_price:
            best_price = float(best_price)
            list_price = float(list_price)
            return 100 - (best_price * 100 / list_price)
        return 0
