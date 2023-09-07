import scrapy

import time
from ripley.spiders import url_list 
import scrapy
import json
from ripley.items import RipleyItem
from datetime import datetime
from datetime import date
import requests

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

class RippleScrapSpider(scrapy.Spider):
    name = "ripley_scrap"
    allowed_domains = ["ripley.com.pe"]

    links =[]
    def start_requests(self):
        u = int(getattr(self, 'u', '0'))
        if u == 1:
            urls = url_list.list1
        elif u == 2:
                urls = url_list.list2
        elif u == 3:
                urls = url_list.list3
        elif u == 4:
                urls = url_list.list4
        elif u == 0:
                urls = url_list.list0

        elif u == 100:
                urls = url_list.list100
        elif u == 200:
                urls = url_list.list200
        elif u == 300:
                urls = url_list.list300
        elif u == 400:
                urls = url_list.list400


        else:
            urls = []

        for i, v in enumerate(urls):
            for e in range((round(v[1]/48)+1)):
                url = v[0] + str(e + 1)           
                #yield scrapy.Request(url, self.parse, errback=self.error_handler)
                yield scrapy.Request(url, self.parse)
               


    def parse(self, response):
            item = RipleyItem()
            productos = response.css("div.catalog-product-item.catalog-product-item__container.col-xs-6.col-sm-6.col-md-4.col-lg-4")

            for i in productos:
            
                item["brand"] = i.css('div.brand-logo span::text').get()
                if item["brand"] == None:
                    item["brand"] = "Revisar codigo"
                
                try:
                    item["product"] = i.css(".catalog-product-details__name::text").get()
                except: item["product"] = None

                try:
                    item["image"] = i.css("img::attr(data-src)").get()
                except:  item["image"] = None

                image_start = item["image"][:6]
                if image_start != "https:":
                    item["image"] = "https:" + item["image"]

                item["sku"] = i.css(".catalog-product-item.catalog-product-item__container.undefined::attr(id)").get()
                item["sku"] = str( item["sku"])
                item["sku"] = item["sku"][:-1]

                item["_id"] =  item["sku"]+str(load_datetime()[0])
                
                try:
                    item["web_dsct"] = round(float(i.css(".catalog-product-details__discount-tag::text").get().replace("-", "").replace("%", "")))
                except:
                    item["web_dsct"] = 0
                
                try:
                    item["list_price"] = i.css(".catalog-prices__list-price.catalog-prices__lowest.catalog-prices__line_thru::text").get().replace("S/", "").replace(",", "")
                except:
                    item["list_price"] = 0

                try:
                    item["best_price"] = i.css(".catalog-prices__offer-price::text").get().strip().replace("S/", "").replace(",", "")
                except:
                    item["best_price"] = 0

                try:
                    item["card_price"] = i.css(".catalog-prices__card-price::text").get().replace("S/", "").replace(",", "")
                except:
                    item["card_price"] = 0

                item["list_price"]     = float(item["list_price"] )
                item["best_price"]     = float(item["best_price"] )
                item["web_dsct"]     = float(item["web_dsct"] )

                item["link"] = i.css(".catalog-product-item.catalog-product-item__container.undefined::attr(href)").get()
                item["link"] = "https://simple.ripley.com.pe" + item["link"]
                item["card_dsct"] = 0
                item["market"]= "ripley"
                item["date"]= load_datetime()[0]
                item["time"]= load_datetime()[1]
                item["home_list"] = "https://www.ripley.com.pe/"


                # element = item["brand"]
                # if item["web_dsct"]>= 70 and   any(item.lower() == element.lower() for item in brand()):
                
                #     if  item["card_price"] == 0:
                #          card_price = ""
                #     else:
                #         card_price = '\n👉Precio Tarjeta :'+str(item["card_price"])

                #     if item["list_price"] == 0:
                #             list_price = ""
                #     else:
                #         list_price = '\n\n➡️Precio Lista :'+str(item["list_price"])

                #     if item["web_dsct"] <= 50:
                #         dsct = "🟡"
                #     if item["web_dsct"] > 50 and item["web_dsct"]  <=69:
                #         dsct = "🟢"
                #     if item["web_dsct"] >=70:
                #         dsct = "🔥🔥🔥🔥🔥"

                #     message =  "✅Marca: "+str(item["brand"])+"\n✅"+str(item["product"])+list_price+"\n👉Precio web :"+str(item["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(item["web_dsct"])+"\n"+"\n\n⌛"+item["date"]+" "+ item["time"]+"\n🔗Link :"+str(item["link"])+"\n🏠home web:"+item["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
                #     foto = item["image"]

                #     send_telegram(message,foto, bot_token, chat_id)

            
            
                yield item


            time.sleep(0.6)
