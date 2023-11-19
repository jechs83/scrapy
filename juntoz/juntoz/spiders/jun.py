import scrapy
from juntoz.spiders import url_list 
import time
from juntoz.items import JuntozItem
from datetime import datetime
import pymongo
from decouple import config
from datetime import date

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now


class JunSpider(scrapy.Spider):
    name = "jun"
    allowed_domains = ["juntoz.com"]
    
    def __init__(self, *args, **kwargs):
        super(JunSpider, self).__init__(*args, **kwargs)
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
    



    links =[]

    def start_requests(self):
       

        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        #urls = links()[int(u-1)]

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

        elif u == 0:
                urls = url_list.list0
        else:
            urls = []
        x = 0
        for i, v in enumerate(urls):
            for e in range((round(v[2]/28))):
                if e != 0:
                    x += 28

                url = v[0] + str(x)     
                #yield scrapy.Request(url, self.parse, errback=self.error_handler)
                yield scrapy.Request(url, self.parse)
               




    def parse(self, response):
        item = JuntozItem()
        productos = response.css("div#product-preview-card")
     

        if not productos:
            return

        for product in productos:
            # print()
            item["brand"] = product.css("a::attr(title)").get()
            # print(item["brand"] )

            marca_producto = item["brand"]
            if self.lista == []:
                        pass
            
            else:
                if marca_producto.lower() not in self.lista:
                    continue




            item["product"] = product.css("img::attr(alt)").get()
            # print(item["product"] )
            item["image"] = product.css("img::attr(src)").get()
            # print(item["image"] )
            item["link"] = product.css("div[jztm-prop='productSeoUrl']::attr(jztm-content)").get()
            item["link"] = "https://juntoz.com/p/"+item["link"]
            # print(item["link"] )
            try:
                item["list_price"] = product.css("span.product-preview-card__wrapper__footer__product-price__current-price::attr(jztm-content)").get()
                item["list_price"]     = float(item["list_price"] )
                
                # print(item["list_price"] )

            except: 
                 item["list_price"]=0
                #  print(item["list_price"] )
            try:
                item["best_price"] = product.css("span.product-preview-card__wrapper__footer__product-price__old-price::attr(jztm-content)").get()
                item["best_price"]     = float(item["best_price"] )
                # print(item["best_price"] )
            except:
                item["best_price"]=0
                # print(item["best_price"] )
            try:
                item["web_dsct"] = product.css("div.product-preview-card__wrapper__heading__product-discount::text").get()
                item["web_dsct"] =  item["web_dsct"].strip()
                item["web_dsct"]     = float(item["web_dsct"] )
               
            except:
                  item["web_dsct"] = 0
            # print( item["web_dsct"] )

            item["sku"] = product.css("input.skuProductCatalog::attr(value)").get()
            item["_id"] =  item["sku"]

      

            item["card_dsct"] = 0
            item["card_price"] = 0
            item["market"]= "juntoz"
            item["date"]= load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"] = "https://www.juntoz.com.pe/"
            time.sleep(0.1)



   

            yield item
        
