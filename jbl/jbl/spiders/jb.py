import scrapy
from jbl.items import JblItem
from datetime import datetime
from datetime import date
from jbl.settings import ROTATING_PROXY_LIST
from jbl.spiders import url_list
from jbl.spiders.urls_db import *
from bs4 import BeautifulSoup
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

class JBSpider(scrapy.Spider):
    name = "jb"
    allowed_domains = ["jbl.com.pe"]

    def __init__(self, *args, **kwargs):
        super(JBSpider, self).__init__(*args, **kwargs)
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
        # for url in self.start_urls:
        #     return scrapy.Request(url=url, callback=self.parse,
        #                meta={"proxy": "http://"+ROTATING_PROXY_LIST})
            

        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
        urls = links()[int(u-1)]

    
                
        # arrays_of_urls = []  
        # for id,i  in enumerate (urls):
        #     temp_array = []  # Create a temporary array for each iteration
        #     for e in range(int(i[1]/50)):
        #         temp_array.append(i[0] + str(e + 1))
        #     arrays_of_urls.append(temp_array)  # Append the temporary array to the main list
            

        urls = links()[int(u-1)]
        for i in urls:

            print(i[0])
       
       
        yield scrapy.Request(i[0], self.parse)


    def parse(self, response):



    


        item = JblItem()


        productos = response.css("div.search-result-items").get()




        soup = BeautifulSoup(productos, 'html.parser')


        for i in soup:

            print()
            try:
                print(i.find_all("a").get("href"))
            except: return False
            print()
 
        # for i in productos:

        #     item["sku"]= i.css("div.price-box.price-final_price::attr(data-product-id)").get()
        #     #item["_id"] =i.css("div.price-box.price-final_price::attr(data-product-id)").get()
        #     #item["_id"] =  item["sku"]+str(load_datetime()[0])
        #     item["_id"] = item["sku"]
          


            
        #     item["link"] = i.css("a::attr(href)").get()
        #     item["brand"] = i.css("div.brand-label  span::text").get()
            
        #     # product = item["brand"]
        #     # if product == None:
        #     #     return "None"
        
        #     # if self.lista == []:
        #     #     pass
        #     # else:
        #     #     if product == None:
        #     #         product = "sin marca"
        #     #     else:
        #     #         if product.lower() not in self.lista:
        #     #                 continue
                
        #     item["product"] = i.css("strong.product.name.product-item-name a.product-item-link::text").get()
        #     item["product"] = item["product"].strip()

        #     try:
        #         item["best_price"] = i.css('span.price-container span.price-wrapper span.price::text').get()
        #         item["best_price"] = str(item["best_price"]).replace("S/","").replace(",","")
        #         item["best_price"]= float(item["best_price"])
        #     except: item["best_price"] = 0

   
        
        #     try:
        #         item["list_price"] = i.css('span.old-price span.price-container.price-final_price.tax.weee span.price-wrapper span.price::text').get()

        #         item["list_price"] = str(item["list_price"]).replace("S/","").replace(",","")
        #         item["list_price"] = float(item["list_price"] )
        #     except: item["list_price"] = None

        #     if item["list_price"] == None:
        #         try:
        #             item["list_price"] = i.css("span.price-container.price-final_price.tax.weee").get()
        #             item["list_price"] = str(item["list_price"]).replace("S/","") .replace(",","")
        #             item["list_price"] = float(item["list_price"])
        #         except: item["list_price"] = 0

        #     item["image"] = i.css("img::attr(src)").get()

        #     try:
        #         item["web_dsct"] = i.css("span.discount-value::text").get()
        #         item["web_dsct"] = round(float(str(item["web_dsct"]).replace("-","").replace("%","")))
        #     except:
        #         item["web_dsct"] = 0


        #     item["market"]= "tailoy"
        #     item["date"] =load_datetime()[0]
        #     item["time"] = load_datetime()[1]
        #     item["home_list"] = response.url
        #     item["card_price"] = 0
        #     item["card_dsct"] = 0





        #     yield item
            