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
    name = "saga"
    allowed_domains = ["falabella.com.pe"]


    def __init__(self, *args, **kwargs):
        super(SagaSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(config("MONGODB"))
        self.db = self.client["brand_allowed"]
        self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b

       
    
    def brand_allowed(self):
     
        collection1 = self.db["todo"]
        todo = collection1.find({})
        return todo    



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
            productos = json_content.get('props', {}).get('pageProps', {}).get("results",{})
            with open ("source.txt", "w+") as f:
                f.write(str(productos))
        
        for i in productos:
                
                try:
                    item["brand"]= i["brand"]
                    product = item["displayName"]
                    print(product)
                    print(item["brand"])
                    time.sleep(100)
            
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

            

                