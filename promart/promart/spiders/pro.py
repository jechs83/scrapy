import scrapy
from promart.items import PromartItem
from datetime import datetime
from datetime import date
from promart.spiders import url_list 
import uuid
import pymongo
from decouple import config
import time



def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now



class ProSpider(scrapy.Spider):
    name = "pro"
    allowed_domains = ["promart.pe"]
    def __init__(self, *args, **kwargs):
        super(ProSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["promart"]
        self.collection_name = self.db['scrap']
        self.db2 = self.client["brand_allowed"]
        self.collection_brand = self.db2["todo"]
        self.lista_marcas =[]
        for i in self.collection_brand.find():
            self.lista_marcas.append(i["brand"])

        #self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b


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
        elif u == 10:
                urls = url_list.list10
        else:
            urls = []

        for i, v in enumerate(urls):
     
            for e in range(50):
                url = v[0]+str(e)+v[1]
                print(url)
                yield scrapy.Request(url, self.parse)




    def parse(self, response):
        item = PromartItem()
        productos = response.css("div.item-product.product-listado")  

        for i in productos:

            item["sku"] = i.css("div::attr(data-id)").get()
            item["sku"] = item["sku"]+str(load_datetime()[0])
            if  item["sku"] == None:
                 continue
            item["_id"] =  item["sku"]

            item["brand"]= i.css("div.brand.js-brand p::text").get()

            product = item["brand"]
            if self.lista_marcas == []:
                pass
            else:
                if product.lower() not in self.lista_marcas:
                   
                    continue


            item["product"] =i.css("input.insert-sku-quantity::attr(title)").get()
            item["link"] =i.css("a.prod-det-enlace::attr(href)").get()
            item["image"]= i.css("img::attr(src)").get()
        
            try:
                item["best_price"] = i.css("div.bestPrice div.vcenter.bestPrice.js-bestPrice span.sin-fto::text").get()
                item["best_price"] =round(float(str(item["best_price"]). strip().replace(",","").replace(" ","").replace("S/","")))

            except: item["best_price"] = 0
        
            if item["best_price"] == None:
                 item["best_price"] = 0


            # if  item["best_price"] != 0 or None:
            #     try: 
            #         item["best_price"] = str(item["best_price"]).replace(",","").replace("S/.","")
            
            #         item["best_price"] = round(float(str(item["best_price"])))
            #     except: item["best_price"] = 0
          
  


            item["list_price"]  =i.css("div.vcenter.listPrice.js-listPrice span.sin-fto::text").get()
            if item["list_price"] != None:
                item["list_price"] = round(float(str(item["list_price"]).replace(",","").replace("S/ ","")))
            else:
                   item["list_price"] =0
        

            # if item["list_price"] == None:
            #      item["list_price"] = 0



            # except: item["list_price"] = 0
            # if item["list_price"] == None:
            #      item["list_price"] = 0


            if item["best_price"] == 0:
                    item["best_price"] = i.css("span.text.fz-lg-15.fw-bold.BestPrice::text").get()
                    try:
                        item["best_price"] = round(float(str(item["best_price"]).replace(",","").replace("S/.","")))
                    except:  item["best_price"] = 0

           

          
            if item["best_price"]  and item["list_price"] !=0:
                item["web_dsct"] = 100-(float(item["best_price"])*100/float(item["list_price"]))
                item["web_dsct"] = round(float( item["web_dsct"]))
            else:
                 item["web_dsct"] = 0
                

          
            

           
            item["home_list"]=response.url
            item["card_dsct"] = 0
            item["card_price"] = 0 
            if item["list_price"] and item["card_price"] and item["best_price"] == 0:
                continue
            item["market"]= "promart"  # COLECCION
            item["date"] = load_datetime()[0]
            item["time"]= load_datetime()[1]

           



            print()
            print(item["brand"])
            print(item["product"])
            print(item["link"])
            print(item["best_price"])
            print(item["card_price"] )
            print(item["list_price"] )

            collection = self.db["scrap"]
            filter = { "sku": item["sku"]}
            update = {'$set': dict(item)}
            result = collection.update_one(filter, update, upsert=True)
