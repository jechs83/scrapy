import scrapy
from scrapy import Selector
from plazavea.items import PlazaveaItem
from datetime import datetime
from datetime import date
from plazavea.spiders import url_list 
import time
import json

from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))
bot_token = '6594474232:AAF39jlHxRJepEaOYcxo9NZhe-pQgzl43lo'
chat_id = "-960438482"


def brand ():

    db = client["brands"]
    collection= db["tecno"]

    t9 = collection.find({})

    array_brand= []

    for i in t9:
        array_brand.append(i["brand"])
    print(array_brand)
    
    return array_brand
  

    


def send_telegram(message,foto, bot_token, chat_id):

    if not foto:
        foto="https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"
    
    if len(foto)<=4:
            foto="https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"

    response = requests.post(
        
        f'https://api.telegram.org/bot{bot_token}/sendPhoto',
        data={'chat_id': chat_id, 'caption': str(message), "parse_mode": "HTML"},
        files={'photo': requests.get(foto).content},
    
        )


def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class VeaSpider(scrapy.Spider):
    name = "vea"
    allowed_domains = ["plazavea.com.pe"]
    #start_urls=[ "https://www.plazavea.com.pe/api/catalog_system/pub/products/search?fq=C:/679/&_from=2041&_to=2061&O=OrderByScoreDESC&"]
 
    
    
    def start_requests(self):
        u = int(getattr(self, 'u', '0'))

        if u == 1:
            urls = url_list.list1

        elif u == 2:
                urls = url_list.list2
        elif u == 3:
                urls = url_list.list3
        else:
            urls = []
        count= 20
        for i, v in enumerate(urls):
            for e in range(120):
                if e ==0:
                     url = v[0]+str(0)+v[1]+str(count)+v[2]
                else:
                    url = v[0]+str(count*e+1)+v[1]+str((count*e+1)+20)+v[2]

                    print(url)

                    yield scrapy.Request(url, self.parse)
           

      

    def parse(self, response):
    
        item = PlazaveaItem()
        data = json.loads(response.body)
        
        productos = data#["data"]["results"]
        for i in productos:

            print()
            item["sku"] = i["items"][0]["referenceId"][0]["Value"]
            if not  item["sku"] :
                continue 
            item["_id"] =  item["sku"]+str(load_datetime()[0])
            item["brand"]= i["brand"]
            product = item["brand"]
            if product.lower() in ["GENERICO", "generico", "GENERICA", "generica","GENÉRICO","GENÉRICA", "GENERIC" , "genérico","genérica"]:
                        continue
            item["product"] =i["productName"]
            item["link"] =i["link"]
            item["image"]= i["items"][0]["images"][0]["imageUrl"]
            
            item["best_price"] = i["items"][0]["sellers"][0]["commertialOffer"]["Price"]

            item["list_price"]  =i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]
            if item["list_price"] == 0 :
                item["web_dsct"] =0
            else:
                item["web_dsct"] = round((item["best_price"]*100 /item["list_price"]))
           

            item["web_dsct"] = round((item["web_dsct"]))
            if item["web_dsct"] > 0:
                item["web_dsct"] = 100-item["web_dsct"]
                item["web_dsct"] =round((item["web_dsct"]))
            if  item["web_dsct"] == 100:
                 item["web_dsct"] = 0
            item["home_list"]=response.url
            item["card_dsct"] = 0
            item["card_price"] = 0 
            item["market"]= "plazavea"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]
            if item["list_price"]  and item["best_price"] == 0.0:
                continue


            # element = item["brand"]
            # if item["web_dsct"]>= 70 and   any(item.lower() == element.lower() for item in brand()):
                
            #         if  item["card_price"] == 0:
            #              card_price = ""
            #         else:
            #             card_price = '\n👉Precio Tarjeta :'+str(item["card_price"])

            #         if item["list_price"] == 0:
            #                 list_price = ""
            #         else:
            #             list_price = '\n\n➡️Precio Lista :'+str(item["list_price"])

            #         if item["web_dsct"] <= 50:
            #             dsct = "🟡"
            #         if item["web_dsct"] > 50 and item["web_dsct"]  <=69:
            #             dsct = "🟢"
            #         if item["web_dsct"] >=70:
            #             dsct = "🔥🔥🔥🔥🔥"

            #         message =  "✅Marca: "+str(item["brand"])+"\n✅"+str(item["product"])+list_price+"\n👉Precio web :"+str(item["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(item["web_dsct"])+"\n"+"\n\n⌛"+item["date"]+" "+ item["time"]+"\n🔗Link :"+str(item["link"])+"\n🏠home web:"+item["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
            #         foto = item["image"]

            #         send_telegram(message,foto, bot_token, chat_id)


            yield item
             

        pass
