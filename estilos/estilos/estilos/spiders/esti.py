import scrapy
from estilos.items import EstilosItem
from datetime import datetime
from datetime import date
#from metro.settings import ROTATING_PROXY_LIST
#from estilos.spiders import url_list
import time

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

class EstiSpider(scrapy.Spider):
    name = "esti"
    allowed_domains = ["estilos.com.pe"]
    start_urls = ["https://www.estilos.com.pe/727-computadoras"]


    def parse(self, response):
        item = EstilosItem()

        productos=  response.css('div.ajax_block_product.col-sp-6.col-xs-6.col-sm-4.col-md-6.col-lg-4.col-xl-3')
        # Extract data from the product div

        # print(productos)
        # print("############")
        # time.sleep(4)

        for i in productos:
   
            item["sku"] = i.css('div.leo-more-info::attr(data-idproduct)').get()
            item["_id"] =  item["sku"]+str(load_datetime()[0])
            item["link"] = i.css('h3.product-title a::attr(href)').get()
            item["image"] =  i.css('img::attr(src)').get()

            item["product"] = i.css('h3.product-title a::text').get()
            # item["brand"] = i.css('div.product-item__brand p::text').get()
            item["brand"] = "estilos"

            try:
                print(item["product"] )
                print(item["link"] )
                
            except :print("no hay ")

            try:
                item["best_price"] = i.css('div.product-price-and-shipping span.price span[itemprop="price"]::text').get().strip()



                # item["best_price"] = float(item["best_price"].replace(",","").replace("S/.",""))
            except:  item["best_price"]  = None

            if item["best_price"] == None:
                item["best_price"] = 0
                

            try:
                item["list_price"] =    i.css('div.product-price-and-shipping span.regular-price::text').get().strip() 

                # item["list_price"] = float(item["list_price"].replace(",","").replace("S/.",""))
            except: item["list_price"]  = None

            if item["list_price"] == None:
                item["list_price"] = 0

            
            print(item["list_price"])
            print(item["best_price"])
            print(item["image"])
            print(item["sku"])
            print()
        

            # item["web_dsct"] = i.css('div.flag.discount-percent::text').get()
            # item["web_dsct"] = str(item["web_dsct"]).replace(",",".").replace("%","")
            # item["web_dsct"] = round(float(item["web_dsct"]))
            
            item["market"] = str("estilos") # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"] = "http://estilos.pe/"
            item["card_price"] =0
            item["card_dsct"] = 0

            yield item
 
