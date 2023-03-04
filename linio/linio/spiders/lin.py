import scrapy
import time
from linio.spiders import url_list 
import scrapy
import json
from linio.items import LinioItem
from datetime import datetime
from datetime import date



def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class LinSpider(scrapy.Spider):
    name = "lin"
    allowed_domains = ["linio.com.pe"]
    start_urls = ["http://linio.com.pe/"]


    def start_requests(self):
        u = int(getattr(self, 'u', '0'))

        if u == 1:
            urls = url_list.list1
    
        elif u == 0:
                urls = url_list.list0
        else:
            urls = []

        for i, v in enumerate(urls):
            for e in range(v[1]):
                url = v[0]+str(e+1)
                yield scrapy.Request(url, self.parse)



    def parse(self, response):
        item = LinioItem()
     
        productos = response.css("div.catalogue-product.row.catalogue-sponsored-product")
       
        for i in productos:
           
          
            # try:
            #     item["brand"] = i.css(".brand-logo::text").get()
            # except:
            #     item["brand"] = "None"
            try:
                item["brand"] = i.css('meta.itemprop::attr(brand)').get()
            except:item["brand"] = None
            
            try:
              item["product"] = i.css('span.title-section::text()').get()
            except: item["product"] = None

            try:
                item["image"] = i.css("img::attr(data-src)").get()
            except:  item["image"] = None

            image_start = item["image"][:6]
            if image_start != "https:":
                item["image"] = "https:" + item["image"]

            item["sku"] = i.css('meta.itemprop::attr(sku)').get()
            item["sku"] = str( item["sku"])

            item["_id"] = item["sku"] 
            
            try:
                item["web_dsct"] = float(i.css(".catalog-product-details__discount-tag::text").get().replace("-", "").replace("%", ""))
            except:
                item["web_dsct"] = 0
            
            try:
                item["list_price"] = i.css(".catalog-prices__list-price.catalog-prices__lowest.catalog-prices__line_thru::text").get().replace("S/", "").replace(",", "")
            except:
                item["list_price"] = 0

            try:
                item["best_price"] = i.css(".catalog-prices__offer-price::text").get().strip().replace("S/", "").replace(",", "")
            except:
                item["best_price"] = 0

            try:
                item["card_price"] = i.css(".catalog-prices__card-price::text").get().replace("S/", "").replace(",", "")
            except:
                item["card_price"] = 0

            item["link"] = i.css(".catalog-product-item.catalog-product-item__container.undefined::attr(href)").get()
            item["link"] = "https://simple.ripley.com.pe" + item["link"]
            item["card_dsct"] = 0
            item["market"]= "ripley"
            item["date"]= load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"] = "https://www.ripley.com.pe/"
           
            
         

            yield item
           