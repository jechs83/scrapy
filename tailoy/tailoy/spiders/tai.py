import scrapy
from scrapy import Selector
from tailoy.items import TailoyItem
from datetime import datetime
from datetime import date

#from tailoy.settings import ROTATING_PROXY_LIST
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
        # for url in self.start_urls:
        #     return scrapy.Request(url=url, callback=self.parse,
        #                meta={"proxy": "http://"+ROTATING_PROXY_LIST})
            

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
        item = TailoyItem

        productos = response.css("li.item.product.product-item")

      

        for i in productos:
            print("######")
            link = i.css("a.product-item-link::attr(href)").get()
            print(link)
            print("#######3")
            time.sleep(200)
    




            yield 
            {
               "link":link,

            }
