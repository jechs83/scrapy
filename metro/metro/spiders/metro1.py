import scrapy
from scrapy import Selector
from metro.items import MetroItem
from datetime import datetime
from datetime import date
#from metro.settings import ROTATING_PROXY_LIST
from metro.spiders import url_list
import time

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class Metro1Spider(scrapy.Spider):
    name = "metro1"
    allowed_domains = ["metro.pe"]

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
            for e in range(100):
                url = v[0]+str(e+1)+v[1]
                yield scrapy.Request(url, self.parse)

    def parse(self, response):
        item = MetroItem()

        productos = response.css("div.product-item.product-item")
        for i in productos:

            item["sku"] = i.css('button.product-item__add-to-cart::attr(data-productid)').get()
			#<button class="product-item__add-to-cart product-add-to-cart btn red add-to-cart" data-productid="957181">
            item["_id"]=item["sku"] 
            item["link"] = i.css("a.product-item__image-link::attr('href')").get()
            item["image"] = i.css('a.product-item__image-link div.js--lazyload img::attr(src)').get()
            item["product"] = i.css('div.product-item__info a::text').get()
            item["brand"] = i.css('div.product-item__brand p::text').get()
    
            item["best_price"] = i.css('span.product-prices__value.product-prices__value--best-price::text').get()
            if item["best_price"] == None:
                item["best_price"] = 0
            

            
            item["list_price"] = i.css('div.product-prices__price.product-prices__price--former-price span.product-prices__value::text').get()
            if item["list_price"] == None:
                item["list_price"] = 0
            
            item["web_dsct"] = i.css('div.flag.discount-percent::text').get()
            item["web_dsct"] = str(item["web_dsct"]).replace(",",".").replace("%","")
            item["web_dsct"] = float(item["web_dsct"])
            
            item["market"] = str("metro") # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"] = "http://metro.pe/"
            item["card_price"] =0
            item["card_dsct"] = 0

            yield item

        
        # for i in productos:
                        
        #     #sku: i.xpath("/html[1]/body[1]/div[1]/ul[1]//@data-id").get()
        #     #_id :   item["sku"] 
        #     product : i.css('a.product-item__name::attr("title")').get()
        #     #item["product"] = i.css('div.product-item__info.product-item_name::text').get(
        #     #try
        #     brand: i.css('p.texto.brand::text').get()
        #     #except: item["brand"] = Non
        #     link: i.css('a.product-item__name::attr(href)').get()
        #     image: i.css('div.js--lazyload img::attr(src)').get()
        #     #try
        #     best_price : i.css("span.product-prices__value::text").get()
        #     #except: item["best_price"] = 
        #     #item["best_price"] = str(item["best_price"]).strip().replace("S/.",""
        #     #item["best_price"] = float(item["best_price"]
        #     #try
        #     list_price : i.css("span.product-prices__value::nth-of-type(2)").get()
        #     #except: item["list_price"] =
        #     #item["list_price"] = str(item["list_price"]).strip().replace("S/.",""
        #     #item["list_price"] = float(item["list_price"]
        #     #try
        #     web_dsct : i.css('div.flag.discount-percent::attr("data-discount")').get()
        #     # item["web_dsct"] : str(item["web_dsct"]).replace("%","")
        #     # item["web_dsct"] : float(item["web_dsct"])
        #     #except:    item["web_dsct"]=
        #     #item["web_dsct"]= str(item["web_dsct"]).rstrip().replace(",",".").replace("%",""
        #     #item["web_dsct"]=float(item["web_dsct"]
        #     market : str("metro") # COLECCION
        #     date : load_datetime()[0]
        #     time: load_datetime()[1]
        #     # home : "http://metro.pe/"
        #     # item["card_price"] : 0
        #     # item["card_dsct"] : 0

        #     yield{
                 
        #         #sku,
        #         #_id,
        #         product,
        #         #item["product"] = i.css('div.product-item__info.product-item_
        #         brand,
        #         #except: it
        #         link,
        #         image,
        #         best_price,
        #         #except: item
        #         #item["best_price"] = str(item["best_price"]).strip()
        #         #item["best_price"] = float(i
        #         list_price ,
        #         #except: ite
        #         #item["list_price"] = str(item["list_price"]).strip()
        #         #item["list_price"] = float(i
        #         web_dsct,
        #         # item["web_dsct"] : str(item["web_dsct"]
        #         # item["web_dsct"] : float(
        #         #except:    
        #         #item["web_dsct"]= str(item["web_dsct"]).rstrip().replace(",",".
        #         #item["web_dsct"]=float
        #         market,
        #         date ,
                 

        #     }
                             
        #     #yield  item
