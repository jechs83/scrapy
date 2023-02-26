import scrapy
from curacao.items import CuracaoItem
from datetime import datetime
from datetime import date
from curacao.spiders import url_list 
import time



def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now


class CuraSpider(scrapy.Spider):
    name = "cura"
    allowed_domains = ["lacuracao.pe"]

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
        elif u == 4:
                urls = url_list.list4
        else:
            urls = []
        count = 0
        for i, v in enumerate(urls):
            for e in range(v[2]):
                if e == 0:
                     url = v[0]+str(0)+v[1]
                else:   
                    url = v[0]+str(count*e)+v[1]
                yield scrapy.Request(url, self.parse)


    def parse(self, response):
        item = CuracaoItem()
        products = response.css('li')
        for product in products:

            item["sku"] = product.css("div.PartNumber::text").get()
            item["_id"] = item["sku"] 
            item["brand"] = product.css('div.Manufacturer::text').get()
            item["product"] = product.css('a::attr(title)').get()
            item["link"] = product.css('a::attr(href)').get()

            try:
                item["image"] = product.css('img::attr(data-src)').get()
                item["image"] = 'https://www.lacuracao.pe'+item["image"]
            except:  item["image"] = None 

            try:
                item["list_price"] = product.css('.old_price::text').get()
                item["list_price"] =item["list_price"].strip().replace(",", "").replace("S/", "")
            except :item["list_price"]  = 0

            try:
                item["best_price"] = product.css('#offerPriceValue::text').get()
                item["best_price"] = item["best_price"].strip().replace(",", "")
            except:
                item["best_price"] = 0

         
            
            if float(item["best_price"]) > 0:
                        web_dsct = (float(item["best_price"]) * 100) / float(item["list_price"])
                        # web_dsct = 100 - web_dsct
                        web_dsct = str(round(web_dsct)).replace("-","")
            item["web_dsct"]= 100- float(web_dsct)
            
        
            item["card_price"] = 0
            item["card_dsct"] = 0
            item["market"] = "curacao"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"]="https://curacao.pe"


            yield item



