import scrapy
from scrapy import Selector
from plazavea.items import PlazaveaItem
from datetime import datetime
from datetime import date
from plazavea.spiders import url_list 
import time
import json


def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class VeaSpider(scrapy.Spider):
    name = "vea"
    allowed_domains = ["plazavea.com.pe"]
    
    def start_requests(self):
        u = int(getattr(self, 'u', '0'))

        if u == 1:
            urls = url_list.list1

        elif u == 2:
                urls = url_list.list2
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
            time.sleep(100)




    def parse(self, response):
    
        item = PlazaveaItem()
        data = json.loads(response.body)
        
        productos = data#["data"]["results"]
        for i in productos:

            print()
            item["sku"] = i["items"][0]["referenceId"][0]["Value"]
            item["_id"] = item["sku"]
            item["brand"]= i["brand"]
            item["product"] =i["productName"]
            item["link"] =i["link"]
            item["image"]= i["items"][0]["images"][0]["imageUrl"]
            
            item["best_price"] = i["items"][0]["sellers"][0]["commertialOffer"]["Price"]

            item["list_price"]  =i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]
            item["web_dsct"] = round((item["best_price"]*100 /item["list_price"]))
            item["web_dsct"] = round((item["web_dsct"]))
            if item["web_dsct"] > 0:
                item["web_dsct"] = 100-item["web_dsct"]
                item["web_dsct"] =round((item["web_dsct"]))
            if  item["web_dsct"] == 100:
                 item["web_dsct"] = 0
            item["home_list"]="https://wwww.plazavea.com.pe"
            item["card_dsct"] = 0
            item["card_price"] = 0 
            item["market"]= "plazavea"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]

            yield item
             

        pass
