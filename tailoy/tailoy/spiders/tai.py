import scrapy
from scrapy import Selector
from tailoy.items import TailoyItem
from datetime import datetime
from datetime import date

from tailoy.settings import ROTATING_PROXY_LIST
from tailoy.spiders import url_list
import time


def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class TaiSpider(scrapy.Spider):
    name = "tai"
    allowed_domains = ["tailoy.com.pe"]
   
        
    def start_requests(self):
        for url in self.start_urls:
            return scrapy.Request(url=url, callback=self.parse,
                       meta={"proxy": "http://"+ROTATING_PROXY_LIST})
            

        u = int(getattr(self, 'u', '0'))

        if u == 1:
            urls = url_list.list1

        elif u == 3:
                urls = url_list.list3
        else:
            urls = []

        for i, v in enumerate(urls):
            for e in range(v[1]):
                url = v[0]+str(e+1)
                yield scrapy.Request(url, self.parse)


    def parse(self, response):
        item = TailoyItem()

        productos = response.css("li.item.product.product-item")

      

        for i in productos:
            print("######")

            item["sku"]= i.css("div.price-box.price-final_price::attr(data-product-id)").get()
            item["_id"] =i.css("div.price-box.price-final_price::attr(data-product-id)").get()
            item["link"] = i.css("a::attr(href)").get()
            item["brand"] = i.css("div.brand-label  span::text").get()
            item["product"] = i.css("strong.product.name.product-item-name a.product-item-link::text").get()
            item["product"] = item["product"].strip()

            try:
                item["best_price"] = i.css('span.price-container span.price-wrapper span.price::text').get()
                item["best_price"] = str(item["best_price"]).replace("S/","").replace(",","")
                item["best_price"]= float(item["best_price"])
            except: item["best_price"] = 0

   
        
            try:
                item["list_price"] = i.css('span.old-price span.price-container.price-final_price.tax.weee span.price-wrapper span.price::text').get()

                item["list_price"] = str(item["list_price"]).replace("S/","").replace(",","")
                item["list_price"] = float(item["list_price"] )
            except: item["list_price"] = None

            if item["list_price"] == None:
                try:
                    item["list_price"] = i.css("span.price-container.price-final_price.tax.weee").get()
                    item["list_price"] = str(item["list_price"]).replace("S/","") .replace(",","")
                    item["list_price"] = float(item["list_price"])
                except: item["list_price"] = 0

            item["image"] = i.css("img::attr(src)").get()

            try:
                item["web_dsct"] = i.css("span.discount-value::text").get()
                item["web_dsct"] = round(float(str(item["web_dsct"]).replace("-","").replace("%","")))
            except:
                item["web_dsct"] = 0


            item["market"]= "tailoy"
            item["date"] =load_datetime()[0]
            item["time"] = load_datetime()[1]
            item["home_list"] = "https://www.tailoy.com.pe/"
            item["card_price"] = 0
            item["card_dsct"] = 0



            yield item
            