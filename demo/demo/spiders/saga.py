import scrapy
import json
from demo.items import DemoItem
from datetime import datetime
from datetime import date
from  demo.spiders import url_list 
import uuid
import pymongo
import time

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

        # if self.b == 0:
        #     self.lista =  self.brand_allowed()[0]
        # if self.b == 1:
        #     self.lista =  self.brand_allowed()[1]
        # if self.b == 2:
        #     self.lista =  self.brand_allowed()[2]
        # if self.b == 3:
        #     self.lista =  self.brand_allowed()[3]
        
    
    # def skip_brand(self):
    #     collection = self.db["add"]
    #     skip = collection.find({})
    #     skip_list = [doc["skip"] for doc in skip]
    #     return skip_list
    
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
        url_mapping = {
            1: url_list.list1, 2: url_list.list2, 3: url_list.list3, 4: url_list.list4, 5: url_list.list5, 6: url_list.list6,
            7: url_list.list7, 8: url_list.list8, 9: url_list.list9, 10: url_list.list10, 11: url_list.list11, 12: url_list.list12, 13: url_list.list13,
            14: url_list.list14, 15: url_list.list15, 16: url_list.list16,  17: url_list.list17,  18: url_list.list18,  
            19: url_list.list19, 20: url_list.list20,21: url_list.list21, 22: url_list.list22,23: url_list.list23, 24: url_list.list24
            }
        

        # Retrieve the appropriate list based on the value of 'u'
        urls = url_mapping.get(u, [])
        
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
                    if self.b != 8:
                        if product.lower() not in self.lista:
                            continue
                    pass
                    
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

            

                