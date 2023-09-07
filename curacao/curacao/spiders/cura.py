import scrapy
from curacao.items import CuracaoItem
from datetime import datetime
from datetime import date
from curacao.spiders import url_list 
import time
import logging
from bson.objectid import ObjectId

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


class CuraSpider(scrapy.Spider):
    name = "cura"
    allowed_domains = ["lacuracao.pe"]

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
        
        count = 12
        for i, v in enumerate(urls):
            count = 12
            for e in range(200):
                if e == 0:
                     url = v[0]+str(0)+v[1]
                else:   
                    url = v[0]+str(count*e)+v[1]
    
                yield scrapy.Request(url, self.parse)


    def parse(self, response):
        count = 0
        item = CuracaoItem()
      
        products = response.css('li')
        for product in products:
            count = count +1
           
            item["sku"] = product.css("div.PartNumber::text").get()
           
          
            #item["_id"] = item["sku"]+str(load_datetime()[0])
            item["_id"] = item["sku"]
            # item['_id'] = ObjectId()
     
            item["brand"] = product.css('div.Manufacturer::text').get()
            
            item["product"] = product.css('a::attr(title)').get()
           
            item["link"] = product.css('a::attr(href)').get()

            try:
                item["image"] = product.css('img::attr(data-src)').get()
                item["image"] = 'https://www.lacuracao.pe'+item["image"]
            except:  item["image"] = None 

            try:
                item["list_price"] = product.css('.old_price::text').get()
                item["list_price"] =item["list_price"].strip().replace(",", "").replace("S/", "")
            except :item["list_price"]  = 0

            try:
                item["best_price"] = product.css('#offerPriceValue::text').get()
                item["best_price"] = item["best_price"].strip().replace(",", "").replace("S/", "")
     
            except:
                try:
                    item["best_price"] = product.css("div.product_price span.price::text").get()
                    item["best_price"] = item["best_price"].strip().replace(",", "").replace("S/", "")
                   
                except:
                    item["best_price"] = 0

      
         
            try:
                if float(item["best_price"]) > 0:
                            web_dsct = (float(item["best_price"]) * 100) / float(item["list_price"])
                            # web_dsct = 100 - web_dsct
                            web_dsct = str(round(web_dsct)).replace("-","")
                item["web_dsct"]= 100- float(web_dsct)
            except: item["web_dsct"]= 0
            


            #item["best_price"] =  "date": load_datetime()[0]date, "price": item"["best_price"], 
        
            item["card_price"] = 0
            item["card_dsct"] = 0
            item["market"] = "curacao"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"]="https://curacao.pe"


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
        if count < 12:
            logging.info("ESTA PAGINA SOLO TIENE MENOS ELEMENTOS\n"+str(response ))
        if count == 12:
            logging.info("PASO CON EXITO EL SCRAPPING" )

             



