import scrapy
from scrapy import Selector
from shopstar.items import ShopstarItem
from datetime import datetime
from datetime import date
from shopstar.spiders import url_list 


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
        elif u == 0:
                urls = url_list.list0
        else:
            urls = []

        for i, v in enumerate(urls):
            for e in range(51):
                url = v+str(e+1)
                yield scrapy.Request(url, self.parse)


    def parse(self, response):
        item = ShopstarItem()

     
        elements = response.xpath("//div[@class='product']")

        for idx, i in enumerate(elements):
    
        
            item["sku"] = i.xpath(".//div[@class='buy-button-normal']/@id").get()

            item["_id"] = item["sku"] 
           
              

            try:
             item["brand"]  = i.xpath(".//h6[@class='x-brand']/text()")[0].get()
            except:  item["brand"]  = i.xpath(".//h6[@class='x-brand']/text()").get()

            try:
             item["product"] = i.xpath(".//h6[@class='x-name']/text()")[0].get()
            except:   item["product"] = i.xpath(".//h6[@class='x-name']/text()").get()

            try:
                item["list_price"] = i.xpath(".//span[@class='product__old-price']/text()")[0].get()
                item["list_price"] = item["list_price"].replace("S/. ", "").replace(",", "")
            except:
                item["list_price"] = 0
            try:
                item["best_price"] = i.xpath(".//span[@class='product__price']/text()")[0].get()
                item["best_price"] = item["best_price"].replace("S/. ", "").replace(",", "")
            except:
                item["best_price"] = 0

            try:
                item["web_dsct"] = i.xpath(".//span[@class='product__discount']/text()")[0].get()
                item["web_dsct"] = item["web_dsct"].replace("-", "").replace(",", ".").replace(" %", "").replace(" ", "")
               
            except:
                item["web_dsct"] = 0

            try:
                ibk_dsct = i.xpath(".//div[@class='contentFlag']/text()")[0].get()
                ibk_dsct = ibk_dsct.split()[1].replace("%", "")
                item["card_dsct"] = float(item["web_dsct"]) + float(ibk_dsct)
                item["card_dsct"] = round(item["card_dsct"], 2)
                item["card_price"] = (float(item["best_priece"]) * (100 - float(ibk_dsct)) / 100)
                item["card_price"] = round(item["card_price"], 2)
            except:
                item["card_dsct"] = 0

            if item["card_dsct"] == 0:
                item["card_price"] = 0

            try:
                  item["image"] = i.xpath(".//img/@src")[0].get()
            except:
                  item["image"] = "Null"
            item["link"] = i.xpath(".//a/@href")[0].get()
            #item["category"] = i.xpath("./@data-cate").get()

            # bd_name_store = "shopstar"
            # collection = "market"  # NOMBRE DE BASE DE DATOS
            item["market"] = "shopstar"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]

            # Yield the scraped data
            yield item