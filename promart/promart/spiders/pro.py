import scrapy
from scrapy import Selector
from promart.items import PromartItem
from datetime import datetime
from datetime import date
from promart.spiders import url_list 

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



class ProSpider(scrapy.Spider):
    name = "pro"
    allowed_domains = ["promart.pe"]
    #start_urls = ["http://promart.pe/"]


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

                
        
                url = v[0]+str(e)+v[1]
                print(url)

    
                yield scrapy.Request(url, self.parse)




    def parse(self, response):
        item = PromartItem()
        productos = response.css("div.item-product.product-listado")  

        for i in productos:

            item["sku"] = i.css("div::attr(data-id)").get()
            if  item["sku"] == None:
                 continue
            item["_id"] =  item["sku"]+str(load_datetime()[0])
            item["brand"]= i.css("div.brand.js-brand p::text").get()
            item["product"] =i.css("input.insert-sku-quantity::attr(title)").get()
            item["link"] =i.css("a.prod-det-enlace::attr(href)").get()
            item["image"]= i.css("img::attr(src)").get()
        
            try:
                item["best_price"] = i.css("div.bestPrice div.vcenter.bestPrice.js-bestPrice span.sin-fto::text").get()
                item["best_price"] =round(float(str(item["best_price"]). strip().replace(",","").replace(" ","").replace("S/","")))

            except: item["best_price"] = 0
        
            if item["best_price"] == None:
                 item["best_price"] = 0


            # if  item["best_price"] != 0 or None:
            #     try: 
            #         item["best_price"] = str(item["best_price"]).replace(",","").replace("S/.","")
            
            #         item["best_price"] = round(float(str(item["best_price"])))
            #     except: item["best_price"] = 0
          
  


            item["list_price"]  =i.css("div.vcenter.listPrice.js-listPrice span.sin-fto::text").get()
            if item["list_price"] != None:
                item["list_price"] = round(float(str(item["list_price"]).replace(",","").replace("S/ ","")))
            else:
                   item["list_price"] =0
        

            # if item["list_price"] == None:
            #      item["list_price"] = 0



            # except: item["list_price"] = 0
            # if item["list_price"] == None:
            #      item["list_price"] = 0


            if item["best_price"] == 0:
                    item["best_price"] = i.css("span.text.fz-lg-15.fw-bold.BestPrice::text").get()
                    try:
                        item["best_price"] = round(float(str(item["best_price"]).replace(",","").replace("S/.","")))
                    except:  item["best_price"] = 0

           

          
            if item["best_price"]  and item["list_price"] !=0:
                item["web_dsct"] = 100-(float(item["best_price"])*100/float(item["list_price"]))
                item["web_dsct"] = round(float( item["web_dsct"]))
            else:
                 item["web_dsct"] = 0
                

          
            

           
            item["home_list"]=response.url
            item["card_dsct"] = 0
            item["card_price"] = 0 
            item["market"]= "promart"  # COLECCION
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
