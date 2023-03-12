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
        elif u == 2:
                urls = url_list.list2
        elif u == 3:
                urls = url_list.list3
        else:
            urls = []

        for i, v in enumerate(urls):
            for e in range(51):
                url = v+str(e+1)
                yield scrapy.Request(url, self.parse)


    def parse(self, response):
        item = ShopstarItem()

     
        #elements = response.xpath("//li[@id][@class='slider__slide']")
        elements = response.css('div.product')

        count = 0
        for i in elements:
           
    
            item["sku"] = i.css('div.buy-button-normal::attr(id)').get()
            item["_id"] =   item["sku"]
          
            try:
             item["brand"]  = i.css('h6.x-brand strong::text').get()
            except:item["brand"]   =  None
           
  
            try:
             item["product"] = i.css('h6.x-name a::text').get()
            except:   item["product"] = None

            try:
                item["best_price"] = i.css('span.product__price strong::text').get()
                item["best_price"] = float(item["best_price"].replace("S/. ", "").replace(",", ""))
            except:
                item["best_price"] = 0

            try:
                item["list_price"] = i.css('span.product__old-price::text').get()
                item["list_price"] = float(item["list_price"].replace("S/. ", "").replace(",", ""))
            except:
                item["list_price"] = 0


            try:
                
                item["web_dsct"] = i.xpath("/html[1]/body[1]/div[1]/ul[1]/li/div[1]/div[2]/span[1]/p/text()").get()
                item["web_dsct"] = round(float(item["web_dsct"].replace("-", "").replace(",", ".").replace(" %", "").replace(" ", "")))
                
                if item["web_dsct"] == None :
                    item["web_dsct"] = round(100-(float(item["best_price"])*100/float(item["list_price"])))
                

               
            except:
                item["web_dsct"] = 0

            if item["list_price"]== 0:
                      item["web_dsct"] = 0

            try:
                ibk_dsct = i.xpath(".//div[@class='contentFlag']/text()")[0].get()
                ibk_dsct = ibk_dsct.split()[1].replace("%", "")
                item["card_dsct"] = float(item["web_dsct"]) + float(ibk_dsct)
                item["card_dsct"] = round(item["card_dsct"])
                item["card_price"] = (float(item["best_priece"]) * (100 - float(ibk_dsct)) / 100)
                item["card_price"] = round(item["card_price"])
            except:
                item["card_dsct"] = 0

            if item["card_dsct"] == 0:
                item["card_price"] = 0

            try:


                  item["image"] = i.css('div.product__image img::attr(src)').get()

            except:
                  item["image"] = "Null"

            try:
             item["link"] = i.css('a::attr(href)').get()
            except: item["link"] =  None


            item["market"] = "shopstar"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"]= "https://shopstar.pe"

            #Yield the scraped data
            yield item