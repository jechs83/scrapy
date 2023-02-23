import scrapy
from scrapy import Selector
from shopstar.items import ShopstarItem
from datetime import datetime
from datetime import date
from shopstar.spiders import url_list 
import time


def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["shopstar.pe"]

    def start_requests(self):
        u = int(getattr(self, 'u', '0'))

        if u == 0:
            urls = url_list.list0
      
        elif u == 1:
                urls = url_list.list1
        else:
            urls = []

        for i, v in enumerate(urls):
            for e in range(51):
                url = v+str(e+1)
                yield scrapy.Request(url, self.parse)


    def parse(self, response):
        item = ShopstarItem()

     
        elements = response.xpath("/html[1]/body[1]/div[1]/ul[1]/li")
        print(elements)
        
 
        for idx, i in enumerate(elements):
           
    
            
            item["sku"] = i.xpath("/html[1]/body[1]/div[1]/ul[1]/li/div[1]/div[4]/div[1]/@id").get()

            item["_id"] = item["sku"] 
           
              

            # try:
            #  item["brand"]  = i.xpath("//h6[@class='x-brand']").get()
            # except:item["brand"]   =  None
           
    
            # try:
            #  item["product"] = i.xpath("//h6[@class='x-name']").get()
            # except:   item["product"] = None

            # try:
            #     item["best_price"] = i.xpath("//span[@class='product__price']//strong/text()").get()
            #     item["best_price"] = float(item["best_price"].replace("S/. ", "").replace(",", ""))
            # except:
            #     item["best_price"] = 0
            # try:
            #     item["list_price"] = i.xpath("//span[@class='product__old-price']/text()").get()
                      
            #     item["list_price"] = float(item["list_price"].replace("S/. ", "").replace(",", ""))
            # except:
            #     item["list_price"] = 0

            # try:
            #     item["web_dsct"] = i.xpath("/html[1]/body[1]/div[1]/ul[1]/li/div[1]/div[2]/span[1]/p/text()").get()
            #     item["web_dsct"] = float(item["web_dsct"].replace("-", "").replace(",", ".").replace(" %", "").replace(" ", ""))
               
            # except:
            #     item["web_dsct"] = 0

            # try:
            #     ibk_dsct = i.xpath(".//div[@class='contentFlag']/text()")[0].get()
            #     ibk_dsct = ibk_dsct.split()[1].replace("%", "")
            #     item["card_dsct"] = float(item["web_dsct"]) + float(ibk_dsct)
            #     item["card_dsct"] = round(item["card_dsct"], 2)
            #     item["card_price"] = (float(item["best_priece"]) * (100 - float(ibk_dsct)) / 100)
            #     item["card_price"] = round(item["card_price"], 2)
            # except:
            #     item["card_dsct"] = 0

            # if item["card_dsct"] == 0:
            #     item["card_price"] = 0

            # try:
            #       item["image"] = i.xpath("//noscript").get().split()[1].replace("src=","").replace('"','')
            # except:
            #       item["image"] = "Null"

            # try:
            #  item["link"] = i.xpath("/html[1]/body[1]/div[1]/ul[1]/li/div[1]/div[3]/div[1]/h6[2]/a[1]/@href").get()
            # except: item["link"] =  None





            item["market"] = "shopstar"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]

            # Yield the scraped data
            yield item