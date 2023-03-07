import scrapy
from scrapy import Selector
from oechsle.items import OechsleItem
from datetime import datetime
from datetime import date
from oechsle.spiders import url_list 


def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now


class OhSpider(scrapy.Spider):
    name = "oh"
    allowed_domains = ["oechsle.pe"]
    #start_urls = ["https://www.oechsle.pe/buscapagina?fq=C:/160/&O=OrderByScoreDESC&PS=36&sl=cc1f325c-7406-439c-b922-9b2e850fcc90&cc=36&sm=0&PageNumber=2&"]
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
        elif u == 10:
                urls = url_list.list10
        else:
            urls = []

        for i, v in enumerate(urls):
     
            for e in range(50):
        
                url = v+str(e)
                print(url)
    
                yield scrapy.Request(url, self.parse)



    def parse(self, response):
        item = OechsleItem()
        productos = response.css('li')  

        for i in productos:

            item["sku"] = i.css("div.product.instock::attr(data-id)").get()
            if  item["sku"] == None:
                 continue
            item["_id"] = item["sku"]
            item["brand"]= i.css("div.product.instock::attr(data-brand)").get()
            item["product"] =i.css("div.product.instock::attr(data-name)").get()
            item["link"] =i.css("div.product.instock::attr(data-link)").get()
            item["image"]= i.css("div.productImage.prod-img.img_one img::attr(src)").get()
            try:
                item["list_price"] = i.css("span.text.text-gray-light.text-del.fz-11.fz-lg-13.ListPrice::text").get()
                item["list_price"] = round(float(item["list_price"].replace(",","").replace("S/.","")))
            except:item["list_price"]  = 0

            try:
                item["best_price"]  =i.css("span.text.fz-lg-15.fw-bold BestPrice::text").get()
                item["best_price"] = round(float(str(item["best_price"]).replace(",","").replace("S/.","")))


            except: item["best_price"] = None

            if item["best_price"] == None:
                    item["best_price"] = i.css("span.text.fz-lg-15.fw-bold.BestPrice::text").get()
                    try:
                        item["best_price"] = round(float(str(item["best_price"]).replace(",","").replace("S/.","")))
                    except:  item["best_price"] = 0

           

            item["web_dsct"] = i.css("span.flag-of.ml-10::text").get()
            if item["web_dsct"] != None:
                item["web_dsct"] = item["web_dsct"].replace("-","").replace("%","").replace(",",".")
                item["web_dsct"] = round(float( item["web_dsct"]))
            else: item["web_dsct"]  = 0

           
            item["home_list"]="https://wwww.oechsle.com.pe"
            item["card_dsct"] = 0
            item["card_price"] = 0 
            item["market"]= "oechsle"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]

            yield item
             

        pass

