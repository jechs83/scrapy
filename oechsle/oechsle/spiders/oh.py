import scrapy
from scrapy import Selector
from oechsle.items import OechsleItem
from datetime import datetime
from datetime import date
from oechsle.spiders import url_list 
import uuid
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


class OhSpider(scrapy.Spider):
    name = "oh"
    allowed_domains = ["oechsle.pe"]
    #start_urls = ["https://www.oechsle.pe/buscapagina?fq=C:/160/&O=OrderByScoreDESC&PS=36&sl=cc1f325c-7406-439c-b922-9b2e850fcc90&cc=36&sm=0&PageNumber=2&"]
    def start_requests(self):
        u = int(getattr(self, 'u', '0'))

        if u == 0:
            urls = url_list.list0
      
        elif u == 1:
                urls = url_list.list1
        elif u == 2:
                urls = url_list.list2
        elif u == 3:
                urls = url_list.list3
        elif u == 4:
                urls = url_list.list4
        elif u == 10:
                urls = url_list.list10
        else:
            urls = []

        for i, v in enumerate(urls):
     
            for e in range(50):
        
                url = v+str(e)
                print(url)
    
                yield scrapy.Request(url, self.parse)



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

