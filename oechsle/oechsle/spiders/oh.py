import scrapy
from oechsle.items import OechsleItem
from datetime import datetime
from datetime import date
from oechsle.spiders import url_list 
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


class OhSpider(scrapy.Spider):
    name = "oh"
    allowed_domains = ["oechsle.pe"]    

    def __init__(self, *args, **kwargs):
        super(OhSpider, self).__init__(*args, **kwargs)
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
    


    #start_urls = ["https://www.oechsle.pe/buscapagina?fq=C:/160/&O=OrderByScoreDESC&PS=36&sl=cc1f325c-7406-439c-b922-9b2e850fcc90&cc=36&sm=0&PageNumber=2&"]
    def start_requests(self):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))

        urls = links()[int(u-1)]
       
        for i, v in enumerate(urls):

            for e in range (v[1]+10):
                url = v[0]+"?&optionOrderBy=OrderByScoreDESC&O=OrderByScoreDESC&page="+str(e+1)
                yield scrapy.Request(url, self.parse)
     
            # for e in range(50):
        
            #     url = v+str(e)
            #     print(url)
    
            #     yield scrapy.Request(url, self.parse)



    def parse(self, response):
        item = OechsleItem()
        productos = response.css('li')  

        for i in productos:

            item["sku"] = i.css("div.product.instock::attr(data-id)").get()
            if  item["sku"] == None:
                 continue
            #item["_id"] =  item["sku"]+str(load_datetime()[0])
            item["_id"] :str(uuid.uuid4())

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
             

        pass

