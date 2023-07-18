import scrapy
import json
from demo.items import DemoItem
from datetime import datetime
from datetime import date
from  demo.spiders import url_list 
import sys
import time



urls2= []


def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
    
 return date_now, time_now, today



class SagaSpider(scrapy.Spider):
    name = "saga"
    allowed_domains = ["falabella.com.pe"]


  

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
        elif u == 11:
                urls = url_list.list11

        elif u == 12:
                urls = url_list.list12

        elif u == 13:
                urls = url_list.list13

        elif u == 14:
                urls = url_list.list14

        elif u == 15:
                urls = url_list.list15

        elif u == 16:
                urls = url_list.list16

        elif u == 100:
                urls = url_list.list100
        elif u == 200:
                urls = url_list.list200
        elif u == 300:
                urls = url_list.list300

        elif u == 400:
                urls = url_list.list400

        elif u == 500:
                urls = url_list.list500
        else:
            urls = []

        for i, v in enumerate(urls):
            for e in range(int(v[2]/56)):
                url = v[0] + str(e+1) + v[1]
                yield scrapy.Request(url, self.parse)





    def parse(self, response):
        item = DemoItem()
        data = json.loads(response.body)
        
        productos = data["data"]["results"]
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

        

                    
                    yield item



  
                