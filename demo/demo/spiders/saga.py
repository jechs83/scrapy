import scrapy
import json
from demo.items import DemoItem
from datetime import datetime
from datetime import date
#from  demo.spiders import url_list 
import uuid
import pymongo
import time
from demo.spiders.urls_db import *

from decouple import config

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
    
 return date_now, time_now, today



class SagaSpider(scrapy.Spider):
    #list_to_skip = skip_brand()
    name = "saga"
    allowed_domains = ["falabella.com.pe"]


    def __init__(self, *args, **kwargs):
        super(SagaSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b
    
    def brand_allowed(self):
     
        collection1 = self.db["todo"]
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
    


    
    



    # def skip_brand(self):
    #     client = pymongo.MongoClient(config("MONGODB"))
    #     db = client[config("db_saga")] 
    #     collection = db["skip"] 

    #     skip_list = []
    #     skip = collection.find({})

    #     for doc in skip:
            
    #         skip_list.append(doc["brand"])
    #     skip_list = list(skip_list)

    #     return skip_list


    def start_requests(self):
       
        u = int(getattr(self, 'u', '0'))
        b = int(getattr(self, 'b', '0'))
       

       
        # Define a dictionary to map 'u' values to the corresponding url_list
        # url_mapping = {
        #     1: links()[0], 2: links()[1], 3: links()[2], 4: links()[3], 5: links()[4], 6: links()[6],
        #     7: links()[6], 8: links()[7], 9: links()[8], 10: links()[9], 11: links()[10], 12: links()[11], 13: links()[12],
        #     14: links()[13], 15: links()[14], 16: links()[15],  17: links()[16],  18: links()[17],  
        #     19: links()[18], 20: links()[19]
        #     }
        

        # Retrieve the appropriate list based on the value of 'u'
        #urls = url_mapping.get(u, [])

        urls = links()[int(u-1)]
     
        for i, v in enumerate(urls):
            if "tottus" in v[0]:
                for e in range (v[1]+10):
                    url = v[0]+ "?subdomain=tottus&page="+str(e+1) +"&store=tottus"
                    yield scrapy.Request(url, self.parse)
            if "sodimac" in v[0]:
                for e in range (v[1]+10):
                    url = v[0]+ "?subdomain=sodimac&page="+str(e+1)+"&store=sodimac"
                    yield scrapy.Request(url, self.parse)
            else:
    
                for e in range (v[1]+10):
                    url = v[0]+ "?page="+str(e+1) 
                    yield scrapy.Request(url, self.parse)
                

        # Now you can use the 'urls

    def parse(self, response):
      
        
        
        if response.status != 200:
        # If the response status is not 200, skip processing this link and move to the next one
                self.logger.warning(f"Skipping URL {response.url} due to non-200 status code: {response.status}")
                return
        
        if "/noResult" in response.url:
                # Move to the next URL in the array (since it is a "noResult" page)
                self.logger.info("Skipping this URL and moving to the next one.")
                return
    
        item = DemoItem()

        # Find the script tag with the JSON data
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()


        if script_tag:
            json_content = json.loads(script_tag)

            

            # Assuming the relevant JSON data is under "props" -> "pageProps" in the JSON response
            page_props = json_content.get('props', {}).get('pageProps', {}).get("results",{})
        #     with open ("source", "w+") as f:
        #         f.write(str(page_props))


        productos = page_props
        
        for i in productos:
                
                try:
                    item["brand"]= i["brand"]
                    product = item["brand"]
                    # if product.lower() in ["generico", "generica", "genérico","genérica","cc group","importado"]:
                    # # if product.lower() in list_to_skip:
                    #     continue
            
                    #if product.lower() not in lista:
                    #if product.lower() not in self.brand_allowed()[int(self.b)]:
                    if self.lista == []:
                        pass
                    else:
                        if product.lower() not in self.lista:
                            continue
            
                    
                except: item["brand"]= None
               


          

               
                

                item["product"]=  i["displayName"]

                item["sku"] = i["skuId"]
                #item["_id"] = i["skuId"]#+str(load_datetime()[0])
                item["_id"] :str(uuid.uuid4())

                try:
                 item["best_price"] = float(i["prices"][1]["price"][0].replace(",",""))
        
                except:
                 item["best_price"] = 0
                print("#######")
                # print(item["best_price"])
        
                try:
                 item["list_price"] = float(i["prices"][2]["price"][0].replace(",",""))
                except: 
                        item["list_price"] = 0
        
                try:

                 item["card_price"] = float(i["prices"][0]["price"][0].replace(",",""))
                except:item["card_price"] =0


                item["link"]=i["url"]

                try:
                 item["image"]=i["mediaUrls"][0]
                except:
                 item["image"]=str(i["mediaUrls"])
        
                try:
                 item["web_dsct"]=float(i["discountBadge"]["label"].replace("-","").replace("%",""))
                except:
                        item["web_dsct"]=0

                item["market"]= "saga"


                item["date"]= load_datetime()[0]
                item["time"]= load_datetime()[1]
                item["home_list"] = response.url
                item["card_dsct"] = 0

                yield item

            

                