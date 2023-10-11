import scrapy
from curacao.items import CuracaoItem
from datetime import datetime
from datetime import date
from curacao.spiders import url_list 
import pymongo
from decouple import config
import logging
import time



import uuid




def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now


class CuraSpider(scrapy.Spider):
    name = "cura"
    allowed_domains = ["lacuracao.pe"]
    def __init__(self, *args, **kwargs):
        super(CuraSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b

    def brand_allowed(self):
        collection1 = self.db["shoes"]
        collection2 = self.db["electro"]
        collection3 = self.db["tv"]
        collection4 = self.db["cellphone"]
        collection5 = self.db["laptop"]
        collection6 = self.db["consola"]
        collection7 = self.db["audio"]
        collection8 = self.db["colchon"]
        collection9 = self.db["nada"]
        collection10 = self.db["sport"]
        
        shoes = collection1.find({})
        electro = collection2.find({})
        tv = collection3.find({})
        cellphone = collection4.find({})
        laptop = collection5.find({})
        consola = collection6.find({})
        audio = collection7.find({})
        colchon = collection8.find({})
        nada = collection9.find({})
        sport = collection10.find({})


        shoes_list = [doc["brand"] for doc in shoes]
        electro_list = [doc["brand"] for doc in electro]
        tv_list = [doc["brand"] for doc in tv]
        cellphone_list = [doc["brand"] for doc in cellphone]
        laptop_list = [doc["brand"] for doc in laptop]
        consola_list = [doc["brand"] for doc in consola]
        audio_list = [doc["brand"] for doc in audio]
        colchon_list = [doc["brand"] for doc in colchon]
        nada_list = [doc["brand"] for doc in nada]
        sport_list = [doc["brand"] for doc in sport]
        return shoes_list ,electro_list,tv_list,cellphone_list,laptop_list, consola_list, audio_list, colchon_list,nada_list,sport_list
    

    def start_requests(self):
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))

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

        elif u == 5:
                urls = url_list.list5

        elif u == 6:
                
                urls = url_list.list6
        elif u == 7:
                urls = url_list.list7
        elif u == 8:
                urls = url_list.list8

        elif u ==9:
                urls = url_list.list9
        elif u == 10:
                urls = url_list.list10
        else:
            urls = []
        
        count = 12
        # for i, v in enumerate(urls):
        #     count = 12
        #     for e in range(200):
        #         if e == 0:
        #              url = v[0]+str(0)+v[1]
        #         else:   
        #             url = v[0]+str(count*e)+v[1]
        for i, v in enumerate(urls):
                for i in range (v[1]):
                    url = v[0]+str(i+1)
                    print(url)
                
                    yield scrapy.Request(url, self.parse)


    def parse(self, response):
        count = 0
        item = CuracaoItem()
      
        products = response.css('li.item.product')
        for product in products:
            count = count +1
           
            item["sku"] = product.css('form.tocart-form::attr(data-product-sku)').extract_first()

           
          
            #item["_id"] = item["sku"]+str(load_datetime()[0])
            #item["_id"] = item["sku"]
            item["_id"] :str(uuid.uuid4())
     
            item["brand"] = product.css('span.brand-name::text').get()
            producto = item["brand"]
            print(producto.lower())
            print(self.lista)
     

            if self.b != 8:
                if producto.lower() not in self.lista:
                    continue
            

            
            item["product"] =  product.css('a.product-item-link::text').get()
            item["product"]  = item["product"].strip() if item["product"]  else None
            
           
            item["link"] = product.css('a::attr(href)').get()

            try:
                item["image"] = product.css('span.product-image-wrapper img.product-image-photo::attr(src)').get()
            except:  item["image"] = None 

            try:
                item["list_price"] = product.css('span.old-price span.price-wrapper span.price::text').get()
                #item["list_price"] = product.css('.old_price::text').get()
                item["list_price"] =item["list_price"].strip().replace(",", "").replace("S/", "").replace('\xa0', '').strip()
            except :item["list_price"]  = 0

            try:
                item["best_price"] = product.css('span.special-price span.price-wrapper span.price::text').get()
                #item["best_price"] = product.css('#offerPriceValue::text').get()
                item["best_price"] = item["best_price"].strip().replace(",", "").replace("S/", "").replace('\xa0', '').strip()
     
            except:
                try:
                    item["best_price"] = product.css("div.product_price span.price::text").get()
                    item["best_price"] = item["best_price"].strip().replace(",", "").replace("S/", "")
                   
                except:
                    item["best_price"] = 0

            #try:
            if item["best_price"] == 0:
                item["best_price"] = product.css('div.price-box.price-final_price span.price-container.price-final_price.tax.weee span.price-wrapper > span.price::text').get()#.replace('S/', '').strip()
                item["best_price"] = item["best_price"].strip().replace(",", "").replace("S/", "").replace('\xa0', '').strip()

      
         
            try:
                item["web_dsct"] =  product.css('span.badge-label.show-pecentage.special-price-discount-label::text').get()

                item["web_dsct"] =  item["web_dsct"].replace("%","").replace("-","")
                item["web_dsct"] = int(item["web_dsct"])
                # if float(item["best_price"]) > 0:
                #             web_dsct = (float(item["best_price"]) * 100) / float(item["list_price"])
                #             # web_dsct = 100 - web_dsct
                #             web_dsct = str(round(web_dsct)).replace("-","")
                # item["web_dsct"]= 100- float(web_dsct)
            except: item["web_dsct"]= 0
            


            #item["best_price"] =  "date": load_datetime()[0]date, "price": item"["best_price"], 
        
            item["card_price"] = 0
            item["card_dsct"] = 0
            item["market"] = "curacao"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]
            item["home_list"]=response.url
           
        
            yield item        
        if count < 12:
            logging.info("ESTA PAGINA SOLO TIENE MENOS ELEMENTOS\n"+str(response ))
        if count == 12:
            logging.info("PASO CON EXITO EL SCRAPPING" )

             



