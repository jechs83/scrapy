import scrapy
from coolbox.items import CoolboxItem
from datetime import datetime
from datetime import date
from coolbox.spiders import url_list 
import time
import logging


class CoolSpider(scrapy.Spider):
    name = "cool"
    allowed_domains = ["www.coolbox.pe"]
    start_urls = ["https://www.coolbox.pe/audio?page=1"]

    # def start_requests(self):
    #     u = int(getattr(self, 'u', '0'))

    #     if u == 1:
    #         urls = url_list.list1
    #     elif u == 2:
    #         urls = url_list.list2
    #     elif u == 3:
    #             urls = url_list.list3
    #     elif u == 4:
    #             urls = url_list.list4
    #     elif u == 5:
    #             urls = url_list.list5
    #     elif u == 6:
    #             urls = url_list.list6
    #     elif u == 7:
    #             urls = url_list.list7
    #     else:
    #         urls = []

    #     for i, v in enumerate(urls):
    #         for e in range(20):
    #             url = v[0] + str(e+1) 
    #             yield scrapy.Request(url, self.parse)








    def parse(self, response):
        #productos = response.css("div.flex.mt0.mb0.pt0.pb0.justify-between.vtex-flex-layout-0-x-flexRowContent.vtex-flex-layout-0-x-flexRowContent--desktop-edinson-cabrera-list.items-stretch.w-100")
        productos = response.css("body.bg-base")
        print("################################")
        print(productos)
        # count = 0
        # for i in productos:
  
        #     count=count+1
        #     product = i.css("::text").get()
        #     print()
        #     print(count)
        #     print(product)
        #     print(count)
        #     time.sleep(4)

        #class="coolboxpe-search-result-0-x-galleryItem coolboxpe-search-result-0-x-galleryItem--container-galleryProductos coolboxpe-search-result-0-x-galleryItem--normal coolboxpe-search-result-0-x-galleryItem--container-galleryProductos--normal coolboxpe-search-result-0-x-galleryItem--list coolboxpe-search-result-0-x-galleryItem--container-galleryProductos--list pa4"
        pass


