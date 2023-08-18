import scrapy
import json
from demo.items import DemoItem
from datetime import datetime
from datetime import date
from  demo.spiders import url_list 
from  demo.spiders import json_extractor 
import sys
import time

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
    
 return date_now, time_now, today


class SagaSpider(scrapy.Spider):
    name = "saga"
    allowed_domains = ["falabella.com.pe"]


  

    # def start_requests(self):
    #     u = int(getattr(self, 'u', '0'))
    
    #     if u == 1:
    #         urls = url_list.list1
    #     if u == 2:
    #         urls = url_list.list1
    #     if u == 3:
    #         urls = url_list.list3
    #     if u == 4:
    #         urls = url_list.list4
    #     if u == 5:
    #         urls = url_list.list5
    #     if u == 6:
    #         urls = url_list.list6
    #     if u == 7:
    #         urls = url_list.list7

    #     if u == 8:
    #         urls = url_list.list8

    #     if u == 9:
    #         urls = url_list.list9

        
    #     if u == 10:
    #         urls = url_list.list10



 
       
       
    #     for i, v in enumerate(urls):
    #         for e in range (200):
    #             url = v+ str(e+1) 
    #             yield scrapy.Request(url, self.parse)



    def start_requests(self):
        u = int(getattr(self, 'u', '0'))

        # Define a dictionary to map 'u' values to the corresponding url_list
        url_mapping = {
            1: url_list.list1, 2: url_list.list1, 3: url_list.list3, 4: url_list.list4, 5: url_list.list5, 6: url_list.list6,
            7: url_list.list7, 8: url_list.list8, 9: url_list.list9, 10: url_list.list10, 11: url_list.list11, 12: url_list.list12, 13: url_list.list13,
            14: url_list.list14, 15: url_list.list15, 16: url_list.list16,  17: url_list.list17, 18: url_list.list18, 19: url_list.list19, 20: url_list.list20,
            21: url_list.list21, 22: url_list.list22,
        }

        # Retrieve the appropriate list based on the value of 'u'
        urls = url_mapping.get(u, [])
        print(urls)
        print("33333333")

        for i, v in enumerate(urls):
            for e in range (200):
                url = v+ str(e+1) 
                yield scrapy.Request(url, self.parse)
                

        # Now you can use the 'urls

    def parse(self, response):

        if response.status != 200:
        # If the response status is not 200, skip processing this link and move to the next one
                self.logger.warning(f"Skipping URL {response.url} due to non-200 status code: {response.status}")
                return
        
        if "/noResult" in response.url:
                # Move to the next URL in the array (since it is a "noResult" page)
                self.logger.info("Skipping this URL and moving to the next one.")
                return
    
        item = DemoItem()

        # Find the script tag with the JSON data
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()


        if script_tag:
            json_content = json.loads(script_tag)

            

            # Assuming the relevant JSON data is under "props" -> "pageProps" in the JSON response
            page_props = json_content.get('props', {}).get('pageProps', {}).get("results",{})
        #     with open ("source", "w+") as f:
        #         f.write(str(page_props))


        productos = page_props
        for i in productos:
            
                try:
                 item["brand"]= i["brand"]
                except: item["brand"]= None

                item["product"]=  i["displayName"]

                item["sku"] = i["skuId"]
                item["_id"] = i["skuId"]+str(load_datetime()[0])

                try:
                 item["best_price"] = float(i["prices"][1]["price"][0].replace(",",""))
        
                except:
                 item["best_price"] = 0
                print("#######")
                print(item["best_price"])
        
                try:
                 item["list_price"] = float(i["prices"][2]["price"][0].replace(",",""))
                except: 
                        item["list_price"] = 0
        
                try:

                 item["card_price"] = float(i["prices"][0]["price"][0].replace(",",""))
                except:item["card_price"] =0


                item["link"]=i["url"]

                try:
                 item["image"]=i["mediaUrls"][0]
                except:
                 item["image"]=str(i["mediaUrls"])
        
                try:
                 item["web_dsct"]=float(i["discountBadge"]["label"].replace("-","").replace("%",""))
                except:
                        item["web_dsct"]=0

                item["market"]= "saga"


                item["date"]= load_datetime()[0]
                item["time"]= load_datetime()[1]
                item["home_list"] = "https://www.falabella.com.pe/"
                item["card_dsct"] = 0

                element = item["brand"]
                if item["web_dsct"]>= 70 and   any(item.lower() == element.lower() for item in brand()):
                
                    if  item["card_price"] == 0:
                         card_price = ""
                    else:
                        card_price = '\n👉Precio Tarjeta :'+str(item["card_price"])

                    if item["list_price"] == 0:
                            list_price = ""
                    else:
                        list_price = '\n\n➡️Precio Lista :'+str(item["list_price"])

                    if item["web_dsct"] <= 50:
                        dsct = "🟡"
                    if item["web_dsct"] > 50 and item["web_dsct"]  <=69:
                        dsct = "🟢"
                    if item["web_dsct"] >=70:
                        dsct = "🔥🔥🔥🔥🔥"

                    message =  "✅Marca: "+str(item["brand"])+"\n✅"+str(item["product"])+list_price+"\n👉Precio web :"+str(item["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(item["web_dsct"])+"\n"+"\n\n⌛"+item["date"]+" "+ item["time"]+"\n🔗Link :"+str(item["link"])+"\n🏠home web:"+item["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
                    foto = item["image"]

                    send_telegram(message,foto, bot_token, chat_id)


                
                yield item

            
            
            # Process the JSON data as needed
            # For example, you can extract product information, prices, etc.
            # ...

        # Find the next page URL and continue scraping the next page
#                 next_page_url = self.get_next_page_url(response)
#                 if next_page_url:
#                  yield scrapy.Request(next_page_url, callback=self.parse)

#     def get_next_page_url(self, response):
#         # Find the link to the next page using CSS selector
#         next_page_link = response.css('i.jsx-1794558402.jsx-1490357007.csicon-arrow_right.arrow_right-mkp::attr(data-page-number)').get()

#         if next_page_link:
#             # Get the absolute URL of the next page
#             next_page_url = response.urljoin(next_page_link)
#             return next_page_url

#         return None


  
                