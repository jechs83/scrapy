import scrapy
from scrapy import Selector
from plazavea.items import PlazaveaItem
from datetime import datetime
from datetime import date
from plazavea.spiders import url_list 
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
        super(VeaSpider, self).__init__(*args, **kwargs)
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
        elif u == 5:
                urls = url_list.list5
        elif u == 6:
                urls = url_list.list6
        elif u == 7:
                urls = url_list.list7

        elif u == 8:
                urls = url_list.list8
        elif u == 9:
                urls = url_list.list9
        elif u == 10:
                urls = url_list.list10
        
        else:
            urls = []
   
        for i, v in enumerate(urls):
            for e in range(v[1]):
                url = v[0]+"?page="+str(e+1)
                yield scrapy.Request(url, self.parse)

    def parse(self, response):
    
        item = PlazaveaItem()
        #data = json.loads(response.body)

        #data = response.css('div.Showcase__content')
        productos = response.css("div.Showcase")

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


        pass
