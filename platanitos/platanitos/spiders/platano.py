import scrapy
from platanitos.items import PlatanitosItem
from datetime import datetime
from datetime import date
from platanitos.spiders import url_list 
import time
import pymongo
import uuid

from decouple import config


def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class PlatanoSpider(scrapy.Spider):
    name = "platano"
    allowed_domains = ["platanitos.com"]

    def __init__(self, *args, **kwargs):
        super(PlatanoSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
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

        for i, v in enumerate(urls):

            for e in range(120):
                url = v+(str(e+100))
             
                yield scrapy.Request(url, self.parse)


    def parse(self, response):
        item = PlatanitosItem()
        #productos = response.css("div.col-flt.col-3")
        productos = response.xpath('//*[@id="body-productos"]/div[3]/div[2]/div[2]/div')

        print(productos)
     

        for product in productos:
      
            item['brand'] = product.xpath('//div[@class="col-12"]/p/label/text()').get()

            item['product'] =product.xpath('//div[@class="col-12"]/p/text()').get()

            try:
                item['best_price']= product.xpath('//div[contains(@class, "col-12")]/p[contains(@class, "nd-ct__item-prices")]/label/text()').get()
                item['best_price'] = float(item['best_price'].replace("S/","").replace(",",""))

            except:
                 item['best_price'] = 0
            try:
                item['list_price'] = product.xpath('//div[contains(@class, "col-12")]/p[contains(@class, "nd-ct__item-prices")]/text()').get()
                item['list_price'] = float(item['list_price'].replace("S/","").replace(",",""))
            except:
                 item['list_price'] = 0

            item['image'] = product.css("img::attr(src)").get()
            item['link'] = response.urljoin(product.css("a::attr(href)").get())
            item['sku'] = item['product'].replace(" ", "")
            item["sku"] =  product.xpath('.//a/@data-object-id').get()
            item["_id"] =item["sku"] 

            item["card_price"] =0
            item["card_dsct"] =0
            if item["list_price"] and item["card_price"] and item["best_price"] == 0:
                continue
            item["date"] =load_datetime()[0]
            item["time"] =load_datetime()[1]
            item["home_list"] =response.url       
            item["market"] ="platanitos"

            try:
                item['web_dsct'] = product.xpath('//div[contains(@class, "col-12")]/div[contains(@class, "nd-ct__label-porc")]/text()').get()
                item['web_dsct'] = int(item['web_dsct'].replace("-","").replace("%",""))
            except:
                 item['web_dsct'] =0

            #item['web_dsct'] = round(self.calculate_discount(item['best_price'], item['list_price']))
           

            yield item



    # def calculate_discount(self, best_price, list_price):
    #     if best_price and list_price:
    #         best_price = float(best_price)
    #         list_price = float(list_price)
    #         return 100 - (best_price * 100 / list_price)
    #     return 0
