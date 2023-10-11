import scrapy
from metro.items import MetroItem
from datetime import datetime
from datetime import date
#from metro.settings import ROTATING_PROXY_LIST
from metro.spiders import url_list
import time
import uuid
import pymongo
from decouple import config






def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class Metro1Spider(scrapy.Spider):
    name = "metro1"
    allowed_domains = ["metro.pe"]

    def __init__(self, *args, **kwargs):
        super(Metro1Spider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b

    def brand_allowed(self):
        collection1 = self.db["shoes"]
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
        # for url in self.start_urls:
        #     return scrapy.Request(url=url, callback=self.parse,
        #                meta={"proxy": "http://"+ROTATING_PROXY_LIST})
            

        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))


        if u == 1:
            urls = url_list.list1

        elif u == 2:
                urls = url_list.list2
        else:
            urls = []

        for i, v in enumerate(urls):
            for e in range(100):
                url = v[0]+str(e+1)+v[1]
                yield scrapy.Request(url, self.parse)

    def parse(self, response):
        item = MetroItem()

        productos = response.css("div.product-item.product-item")
        for i in productos:

            item["sku"] = i.css('button.product-item__add-to-cart::attr(data-productid)').get()
			#<button class="product-item__add-to-cart product-add-to-cart btn red add-to-cart" data-productid="957181">
            #item["_id"] =  item["sku"]+str(load_datetime()[0])
            item["_id"] :str(uuid.uuid4())

            item["link"] = i.css("a.product-item__image-link::attr('href')").get()
            item["image"] = i.css('a.product-item__image-link div.js--lazyload img::attr(src)').get()
            item["product"] = i.css('div.product-item__info a::text').get()
            item["brand"] = i.css('div.product-item__brand p::text').get()
            product = item["brand"]
            if self.b != 8:
                        if product.lower() not in self.lista:
                            continue

            try:
                item["best_price"] = i.css('span.product-prices__value.product-prices__value--best-price::text').get()
                item["best_price"] = float(item["best_price"].replace(",","").replace("S/.",""))
            except:  item["best_price"]  = None

            if item["best_price"] == None:
                item["best_price"] = 0
                

            try:
                item["list_price"] = i.css('div.product-prices__price.product-prices__price--former-price span.product-prices__value::text').get()
                item["list_price"] = float(item["list_price"].replace(",","").replace("S/.",""))
            except: item["list_price"]  = None

            if item["list_price"] == None:
                item["list_price"] = 0

            
            
            item["web_dsct"] = i.css('div.flag.discount-percent::text').get()
            item["web_dsct"] = str(item["web_dsct"]).replace(",",".").replace("%","")
            item["web_dsct"] = round(float(item["web_dsct"]))
            
            item["market"] = str("metro") # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"] = response.url
            item["card_price"] =0
            item["card_dsct"] = 0



            yield item
 
        
