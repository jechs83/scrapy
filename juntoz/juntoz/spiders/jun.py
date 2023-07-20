import scrapy
from juntoz.spiders import url_list 
import time
from juntoz.items import JuntozItem
from datetime import datetime
from datetime import date

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class JunSpider(scrapy.Spider):
    name = "jun"
    allowed_domains = ["juntoz.com"]
    
    links =[]

    def start_requests(self):
        u = int(getattr(self, 'u', '0'))
        if u == 1:
            urls = url_list.list1
        elif u == 2:
                urls = url_list.list2
        elif u == 3:
                urls = url_list.list3
        elif u == 0:
                urls = url_list.list0
        else:
            urls = []
        x = 0
        for i, v in enumerate(urls):
            for e in range((round(v[2]/28))):
                if e != 0:
                    x += 28

                url = v[0] + str(x)     
                print(url)     
                #yield scrapy.Request(url, self.parse, errback=self.error_handler)
                yield scrapy.Request(url, self.parse)
               




    def parse(self, response):
        item = JuntozItem()
        print(response)
        productos = response.css("div#product-preview-card")
        # print(productos)
        # time.sleep(5)
 

        if not productos:
            return

        for product in productos:
            print()
            item["brand"] = product.css("a::attr(title)").get()
            print(item["brand"] )
            item["product"] = product.css("img::attr(alt)").get()
            print(item["product"] )
            item["image"] = product.css("img::attr(src)").get()
            print(item["image"] )
            item["link"] = product.css("div[jztm-prop='productSeoUrl']::attr(jztm-content)").get()
            item["link"] = "https://juntoz.com/p/"+item["link"]
            print(item["link"] )
            try:
                item["list_price"] = product.css("span.product-preview-card__wrapper__footer__product-price__current-price::attr(jztm-content)").get()
                item["list_price"]     = float(item["list_price"] )
                
                print(item["list_price"] )

            except: 
                 item["list_price"]=0
                 print(item["list_price"] )
            try:
                item["best_price"] = product.css("span.product-preview-card__wrapper__footer__product-price__old-price::attr(jztm-content)").get()
                item["best_price"]     = float(item["best_price"] )
                print(item["best_price"] )
            except:
                item["best_price"]=0
                print(item["best_price"] )
            try:
                item["web_dsct"] = product.css("div.product-preview-card__wrapper__heading__product-discount::text").get()
                item["web_dsct"] =  item["web_dsct"].strip()
                item["web_dsct"]     = float(item["web_dsct"] )
               
            except:
                  item["web_dsct"] = 0
            print( item["web_dsct"] )

            item["sku"] = product.css("input.skuProductCatalog::attr(value)").get()
            item["_id"] =  item["sku"]+str(load_datetime()[0])

      

            item["card_dsct"] = 0
            item["card_price"] = 0
            item["market"]= "juntoz"
            item["date"]= load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"] = "https://www.juntoz.com.pe/"


            time.sleep(0.05)

            yield item
        time.sleep(0.5)
