import scrapy
import json
from demo.items import DemoItem
from datetime import datetime
from datetime import date
from  demo.spiders import url_list 
import uuid



def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
    
 return date_now, time_now, today


class SagaSpider(scrapy.Spider):
    name = "saga"
    allowed_domains = ["falabella.com.pe"]


    def start_requests(self):
        u = int(getattr(self, 'u', '0'))

        # Define a dictionary to map 'u' values to the corresponding url_list
        url_mapping = {
            1: url_list.list1, 2: url_list.list1, 3: url_list.list3, 4: url_list.list4, 5: url_list.list5, 6: url_list.list6,
            7: url_list.list7, 8: url_list.list8, 9: url_list.list9, 10: url_list.list10, 11: url_list.list11, 12: url_list.list12, 13: url_list.list13,
            14: url_list.list14, 15: url_list.list15, 16: url_list.list16,  17: url_list.list17,  18: url_list.list18,  
            19: url_list.list19, 1000: url_list.list1000,
      
            }
        

        # Retrieve the appropriate list based on the value of 'u'
        urls = url_mapping.get(u, [])
    

        for i, v in enumerate(urls):
            for e in range (v[1]):
                url = v[0]+ str(e+1) 

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
                except: item["brand"]= None
                if item["brand"].lower() in ["generico", "generica", "genérico", "genérica"]:
                     continue
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

            

                